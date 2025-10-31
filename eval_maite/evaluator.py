"""
LegalBench Evaluator for Maite AI Agent.

Orchestrates the canonical evaluation workflow:
1. Load task data
2. Generate prompts (using canonical generate_prompts)
3. Execute agent
4. Evaluate results (using canonical evaluate)
5. Aggregate metrics

CRITICAL: This module MUST use canonical LegalBench functions:
- utils.generate_prompts() - DO NOT reimplement
- evaluation.evaluate() - DO NOT reimplement
"""

from typing import List, Optional

from termcolor import cprint
from tqdm.auto import tqdm

# Canonical LegalBench functions (DO NOT REIMPLEMENT)
from evaluation import evaluate
from utils import generate_prompts

# eval_maite modules
from eval_maite.agent_wrapper import MaiteAgentWrapper
from eval_maite.models import TaskResult, TaskTrace
from eval_maite.task_loader import get_task_category, get_test_df, load_prompt_template
from eval_maite.utils import get_metric_name


class LegalBenchEvaluator:
    """
    Evaluator for running Maite agent on LegalBench tasks.

    Follows canonical LegalBench evaluation workflow from UsingLegalBench.ipynb.

    Example:
        ```python
        from eval_maite.evaluator import LegalBenchEvaluator
        from eval_maite.agent_wrapper import MaiteAgentWrapper
        from eval_maite.models import AgentConfig

        config = AgentConfig(model="claude-sonnet-4")
        agent = MaiteAgentWrapper(config)
        evaluator = LegalBenchEvaluator(agent)

        # Evaluate single task
        result = evaluator.evaluate_task("hearsay", sample_size=10)
        print(f"Score: {result.score}")

        # Evaluate multiple tasks
        results = evaluator.evaluate_multiple(["hearsay", "contract_qa"], sample_size=5)
        ```
    """

    def __init__(self, agent_wrapper: MaiteAgentWrapper):
        """
        Initialize evaluator with agent wrapper.

        Args:
            agent_wrapper: Configured MaiteAgentWrapper instance
        """
        self.agent_wrapper = agent_wrapper
        cprint("✅ LegalBenchEvaluator initialized", "green")

    def evaluate_task(
        self,
        task_name: str,
        sample_size: Optional[int] = None,
        include_traces: bool = False,
    ) -> TaskResult:
        """
        Evaluate agent on a single LegalBench task.

        Implements canonical workflow from UsingLegalBench.ipynb:
        1. Load test DataFrame
        2. Load prompt template
        3. Generate prompts (canonical generate_prompts)
        4. Limit samples if requested
        5. Execute agent on each sample
        6. Evaluate results (canonical evaluate)
        7. Aggregate metrics

        Args:
            task_name: Name of task (e.g., "hearsay", "contract_qa")
            sample_size: Optional limit on samples (None = use all test samples)
            include_traces: Whether to include detailed traces in result

        Returns:
            TaskResult with aggregated metrics

        Raises:
            ValueError: If task_name is invalid
            Exception: If evaluation fails
        """
        cprint(f"\n{'='*80}", "cyan", attrs=["bold"])
        cprint(f"Evaluating Task: {task_name}", "cyan", attrs=["bold"])
        cprint(f"{'='*80}", "cyan", attrs=["bold"])

        # Step 1: Load test DataFrame
        cprint(f"\n📥 Loading task data...", "cyan")
        test_df = get_test_df(task_name)
        cprint(f"✅ Loaded {len(test_df)} test samples", "green")

        # Step 2: Load prompt template
        cprint(f"📄 Loading prompt template...", "cyan")
        template = load_prompt_template(task_name)
        cprint(f"✅ Loaded template ({len(template)} chars)", "green")

        # Step 3: Generate prompts (CANONICAL)
        cprint(f"📝 Generating prompts...", "cyan")
        prompts = generate_prompts(prompt_template=template, data_df=test_df)
        cprint(f"✅ Generated {len(prompts)} prompts", "green")

        # Step 4: Sample if needed (slice both DataFrame and prompts)
        if sample_size is not None and sample_size < len(test_df):
            cprint(f"📊 Sampling {sample_size} of {len(test_df)} samples", "yellow")
            test_df = test_df.iloc[:sample_size].copy()
            prompts = prompts[:sample_size]
            cprint(f"✅ Using {len(prompts)} samples for evaluation", "green")

        # Step 5: Execute agent on each prompt
        cprint(f"\n🤖 Executing agent on {len(prompts)} samples...", "cyan")
        traces: List[TaskTrace] = []
        answers = test_df["answer"].tolist()

        for i, prompt in enumerate(tqdm(prompts, desc=f"{task_name}", unit="sample")):
            sample_id = f"{task_name}_test_{i}"
            expected = answers[i]

            # Execute agent (includes retry logic and error handling)
            trace = self.agent_wrapper.execute(prompt, expected, sample_id)
            traces.append(trace)

        # Step 6: Extract generations from traces
        generations = [trace.actual_output for trace in traces]

        # Step 7: Evaluate (CANONICAL)
        cprint(f"\n📊 Evaluating results with canonical evaluate()...", "cyan")
        score = evaluate(task_name, generations, answers)
        cprint(f"✅ Score: {score:.4f}", "green")

        # Step 8: Get task metadata
        category = get_task_category(task_name)
        metric_name = get_metric_name(task_name)

        # Step 9: Build TaskResult
        result = self._build_task_result(
            task_name=task_name,
            category=category,
            traces=traces,
            score=score,
            metric_name=metric_name,
            include_traces=include_traces,
        )

        cprint(f"\n✅ Task evaluation complete", "green", attrs=["bold"])
        return result

    def evaluate_multiple(
        self,
        task_names: List[str],
        sample_size: Optional[int] = None,
        include_traces: bool = False,
    ) -> List[TaskResult]:
        """
        Evaluate agent on multiple LegalBench tasks.

        Args:
            task_names: List of task names (e.g., ["hearsay", "contract_qa"])
            sample_size: Optional limit on samples per task
            include_traces: Whether to include detailed traces

        Returns:
            List of TaskResults (one per task successfully evaluated)

        Note:
            If a task fails, it will be skipped and an error will be printed.
            Other tasks will continue to be evaluated.
        """
        cprint(f"\n{'='*80}", "cyan", attrs=["bold"])
        cprint(f"Evaluating {len(task_names)} Tasks", "cyan", attrs=["bold"])
        cprint(f"{'='*80}", "cyan", attrs=["bold"])

        results = []
        failed_tasks = []

        for idx, task_name in enumerate(task_names, 1):
            cprint(f"\n[Task {idx}/{len(task_names)}]", "cyan", attrs=["bold"])

            try:
                result = self.evaluate_task(task_name, sample_size, include_traces)
                results.append(result)
            except Exception as e:
                cprint(f"❌ Failed to evaluate {task_name}: {e}", "red")
                failed_tasks.append(task_name)
                # Continue with other tasks

        # Print summary
        cprint(f"\n{'='*80}", "cyan", attrs=["bold"])
        cprint(f"Evaluation Summary", "cyan", attrs=["bold"])
        cprint(f"{'='*80}", "cyan", attrs=["bold"])
        cprint(f"✅ Completed: {len(results)}/{len(task_names)} tasks", "green")

        if failed_tasks:
            cprint(f"❌ Failed: {len(failed_tasks)} tasks", "red")
            for task in failed_tasks:
                cprint(f"   - {task}", "red")

        return results

    def _build_task_result(
        self,
        task_name: str,
        category: str,
        traces: List[TaskTrace],
        score: float,
        metric_name: str,
        include_traces: bool = False,
    ) -> TaskResult:
        """
        Aggregate traces into TaskResult.

        Computes average execution time, tokens, tool calls, and error count.

        Args:
            task_name: Task name
            category: Task category (e.g., "CONCLUSION_TASKS")
            traces: List of execution traces
            score: Evaluation score from canonical evaluate()
            metric_name: Name of metric used (e.g., "balanced_accuracy")
            include_traces: Whether to include traces in result

        Returns:
            TaskResult with aggregated metrics
        """
        # Count errors
        errors = sum(1 for t in traces if t.error is not None)

        # Aggregate execution times
        total_time = sum(t.execution_time for t in traces)
        avg_time = total_time / len(traces) if traces else 0.0

        # Aggregate tokens (handle None values)
        token_traces = [t for t in traces if t.tokens is not None]
        if token_traces:
            total_tokens = sum(t.tokens["total"] for t in token_traces)
            avg_tokens = total_tokens / len(token_traces)
        else:
            avg_tokens = None

        # Aggregate tool calls (currently always empty from agent wrapper)
        tool_call_traces = [t for t in traces if t.tool_calls]
        if tool_call_traces:
            total_tool_calls = sum(len(t.tool_calls) for t in tool_call_traces)
            avg_tool_calls = total_tool_calls / len(traces)
        else:
            avg_tool_calls = None

        # Print summary
        cprint(f"\n📊 Task Summary:", "cyan", attrs=["bold"])
        cprint(f"   Task: {task_name}", "white")
        cprint(f"   Category: {category}", "white")
        cprint(f"   Samples: {len(traces)}", "white")
        cprint(f"   Metric: {metric_name}", "white")
        cprint(f"   Score: {score:.4f}", "white")
        cprint(f"   Avg time: {avg_time:.2f}s", "white")
        if avg_tokens:
            cprint(f"   Avg tokens: {avg_tokens:.1f}", "white")
        if errors > 0:
            cprint(f"   Errors: {errors}", "red")

        return TaskResult(
            task_name=task_name,
            category=category,
            samples_evaluated=len(traces),
            metric=metric_name,
            score=score,
            avg_execution_time=avg_time,
            avg_tokens=avg_tokens,
            avg_tool_calls=avg_tool_calls,
            errors=errors,
            traces=traces if include_traces else None,
        )
