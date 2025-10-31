"""
Agent wrapper for Maite AI agent integration.

Provides a unified interface to execute Maite agent and capture execution traces.
"""

import asyncio
import sys
import time
from pathlib import Path
from typing import Optional

from termcolor import cprint

from eval_maite.agent_config import discover_workbench_path
from eval_maite.agent_utils import (
    build_error_trace,
    check_correctness,
    execute_with_timeout,
    retry_with_backoff,
)
from eval_maite.models import AgentConfig, TaskTrace


class MaiteAgentWrapper:
    """
    Wrapper for Maite AI agent with execution tracing.

    Handles dynamic import, async execution, and trace capture.
    """

    def __init__(self, agent_config: AgentConfig):
        """
        Initialize the Maite agent wrapper.

        Args:
            agent_config: Configuration for the agent

        Raises:
            ImportError: If Maite agent cannot be imported
        """
        self.config = agent_config
        self.workbench_path = discover_workbench_path()

        # Add s_c_workbench to Python path for imports
        workbench_str = str(self.workbench_path)
        if workbench_str not in sys.path:
            sys.path.insert(0, workbench_str)
            cprint(f"📦 Added to sys.path: {workbench_str}", "cyan")

        # Import Maite agent
        try:
            from src.agents.maite.agent import MaiteAgent

            self.MaiteAgent = MaiteAgent
            cprint("✅ MaiteAgent imported successfully", "green")
        except ImportError as e:
            cprint(f"❌ Failed to import MaiteAgent: {e}", "red")
            raise ImportError(
                f"Cannot import MaiteAgent from {self.workbench_path}. "
                "Ensure s_c_workbench is set up correctly."
            ) from e

        # Import SDK message types
        try:
            from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock

            self.AssistantMessage = AssistantMessage
            self.ResultMessage = ResultMessage
            self.TextBlock = TextBlock
            cprint("✅ Claude Agent SDK messages imported", "green")
        except ImportError as e:
            cprint(f"❌ Failed to import SDK messages: {e}", "red")
            raise

    def execute(self, prompt: str, expected_output: str, sample_id: str = "unknown") -> TaskTrace:
        """
        Execute a prompt and return execution trace.

        This is a synchronous wrapper around async execution.

        Args:
            prompt: Input prompt to send to agent
            expected_output: Ground truth answer for correctness check
            sample_id: Identifier for this sample (e.g., "hearsay_test_0")

        Returns:
            TaskTrace with execution details
        """
        cprint(f"\n🤖 Executing sample: {sample_id}", "cyan")

        # Handle both normal scripts and notebooks with existing event loops
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No event loop running - use asyncio.run()
            return asyncio.run(self._execute_async(prompt, expected_output, sample_id))
        else:
            # Event loop exists (e.g., in Jupyter) - raise informative error
            raise RuntimeError(
                "Cannot use MaiteAgentWrapper.execute() in an environment with a running event loop "
                "(e.g., Jupyter notebook). Please use the async version directly: "
                "await wrapper._execute_async(prompt, expected_output, sample_id)"
            )

    async def _execute_async(
        self, prompt: str, expected_output: str, sample_id: str
    ) -> TaskTrace:
        """
        Async execution with retry logic and timeout enforcement.

        Args:
            prompt: Input prompt
            expected_output: Ground truth answer
            sample_id: Sample identifier

        Returns:
            TaskTrace with execution details
        """
        max_retries = self.config.max_retries
        timeout = float(self.config.timeout)

        async def attempt_execution():
            # Wrap single execution with timeout
            return await execute_with_timeout(
                self._single_execution(prompt, expected_output, sample_id),
                timeout=timeout,
            )

        try:
            return await retry_with_backoff(
                attempt_execution, max_retries=max_retries, initial_delay=1.0
            )
        except Exception as e:
            # All retries exhausted - return error trace
            cprint(f"❌ Execution failed after {max_retries} retries: {e}", "red")
            return build_error_trace(
                sample_id=sample_id,
                input_text=prompt,
                expected_output=expected_output,
                error_message=str(e),
                execution_time=0.0,
            )

    async def _single_execution(
        self, prompt: str, expected_output: str, sample_id: str
    ) -> TaskTrace:
        """
        Single execution attempt.

        Creates fresh agent instance, executes prompt, captures response.

        Args:
            prompt: Input prompt
            expected_output: Ground truth answer
            sample_id: Sample identifier

        Returns:
            TaskTrace with execution details

        Raises:
            Exception: If execution fails
        """
        start_time = time.time()
        response_parts = []
        tokens = None

        try:
            # Create fresh agent instance (no context leak)
            async with self.MaiteAgent(
                cwd=str(self.workbench_path),  # Run from Maite's directory
                matter_id="111111-0002",  # LegalBench evaluation matter
            ) as agent:
                # Skip memory initialization for clean state
                # await agent.init_memory()  # COMMENTED OUT

                # Send query
                cprint(f"   Sending query to agent...", "white")
                await agent.query(prompt)

                # Stream response and collect messages
                async for message in agent.stream_response():
                    # Extract text from AssistantMessage
                    if isinstance(message, self.AssistantMessage):
                        for block in message.content:
                            if isinstance(block, self.TextBlock):
                                response_parts.append(block.text)

                    # Extract token usage from ResultMessage
                    if isinstance(message, self.ResultMessage):
                        usage = getattr(message, "usage", None)
                        if usage:
                            input_tokens = usage.get("input_tokens", 0)
                            output_tokens = usage.get("output_tokens", 0)
                            tokens = {
                                "input": input_tokens,
                                "output": output_tokens,
                                "total": input_tokens + output_tokens,
                            }
                            cprint(f"   Tokens: {tokens['total']} total", "white")
                        else:
                            tokens = None
                            cprint(f"   ⚠️ No token usage data available", "yellow")

            # Process response
            execution_time = time.time() - start_time
            actual_output = "".join(response_parts).strip()

            # Check correctness
            is_correct = check_correctness(actual_output, expected_output)

            cprint(f"   ✓ Execution complete in {execution_time:.2f}s", "green")
            cprint(f"   Expected: {expected_output}", "white")
            cprint(f"   Actual: {actual_output[:100]}...", "white")
            cprint(f"   Correct: {'✅' if is_correct else '❌'}", "white")

            # Build trace
            return TaskTrace(
                sample_id=sample_id,
                input_text=prompt,
                expected_output=expected_output,
                actual_output=actual_output,
                is_correct=is_correct,
                execution_time=execution_time,
                tokens=tokens,
                tool_calls=[],  # Not exposed by SDK - leave empty
                chain_steps=[],  # Not exposed by SDK - leave empty
                error=None,
            )

        except Exception as e:
            execution_time = time.time() - start_time
            cprint(f"   ❌ Execution error: {e}", "red")
            raise  # Re-raise for retry logic
