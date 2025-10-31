"""
Utility functions for agent execution.

Provides retry logic, timeout handling, and message parsing helpers.
"""

import asyncio
import time
from typing import Any, Dict, List, Optional

from termcolor import cprint

from eval_maite.models import TaskTrace


async def retry_with_backoff(
    func,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 10.0,
    backoff_factor: float = 2.0,
):
    """
    Retry an async function with exponential backoff.

    Args:
        func: Async callable to retry
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        backoff_factor: Multiplier for delay after each retry

    Returns:
        Result from successful function call

    Raises:
        Last exception if all retries exhausted
    """
    delay = initial_delay
    last_exception = None

    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            last_exception = e
            if attempt < max_retries - 1:
                cprint(
                    f"⚠️  Attempt {attempt + 1}/{max_retries} failed: {str(e)[:100]}",
                    "yellow",
                )
                cprint(f"   Retrying in {delay:.1f}s...", "yellow")
                await asyncio.sleep(delay)
                delay = min(delay * backoff_factor, max_delay)
            else:
                cprint(f"❌ All {max_retries} attempts failed", "red")

    # All retries exhausted
    raise last_exception


async def execute_with_timeout(coro, timeout: float):
    """
    Execute coroutine with timeout.

    Args:
        coro: Coroutine to execute
        timeout: Timeout in seconds

    Returns:
        Result from coroutine

    Raises:
        asyncio.TimeoutError: If execution exceeds timeout
    """
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        cprint(f"⏱️  Execution timed out after {timeout}s", "red")
        raise


def build_error_trace(
    sample_id: str,
    input_text: str,
    expected_output: str,
    error_message: str,
    execution_time: float,
) -> TaskTrace:
    """
    Build a TaskTrace for a failed execution.

    Args:
        sample_id: Sample identifier
        input_text: Input prompt
        expected_output: Ground truth answer
        error_message: Error message
        execution_time: Time spent before failure

    Returns:
        TaskTrace with error populated
    """
    return TaskTrace(
        sample_id=sample_id,
        input_text=input_text,
        expected_output=expected_output,
        actual_output="",  # Empty on error
        is_correct=False,
        execution_time=execution_time,
        tokens=None,
        tool_calls=[],  # Not available on error
        chain_steps=[],
        error=error_message,
    )


def normalize_answer(answer: str) -> str:
    """
    Normalize answer for comparison (basic version).

    Args:
        answer: Raw answer string

    Returns:
        Normalized answer (stripped, lowercase)
    """
    return answer.strip().lower()


def check_correctness(actual: str, expected: str) -> bool:
    """
    Check if actual output matches expected output.

    Uses basic normalization for comparison.

    Args:
        actual: Agent's output
        expected: Ground truth answer

    Returns:
        True if match, False otherwise
    """
    return normalize_answer(actual) == normalize_answer(expected)
