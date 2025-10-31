#!/usr/bin/env python3
"""
CLI script for running Maite AI agent evaluation on LegalBench tasks.

Usage:
    python scripts/run_eval.py --tasks hearsay,contract_qa --samples 20
    python scripts/run_eval.py --category CONCLUSION_TASKS --samples 10
    python scripts/run_eval.py --quick

Produces:
    results/run_YYYYMMDD_HHMMSS.json with complete evaluation results
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import List

from termcolor import colored, cprint

# LegalBench task lists
from tasks import (
    CONCLUSION_TASKS,
    INTERPRETATION_TASKS,
    ISSUE_TASKS,
    RHETORIC_TASKS,
    RULE_TASKS,
    TASKS,
)

# eval_maite modules
from eval_maite.agent_wrapper import MaiteAgentWrapper
from eval_maite.evaluator import LegalBenchEvaluator
from eval_maite.models import AgentConfig, EvaluationRun
from eval_maite.utils import generate_run_id, print_header, print_success, save_results

# Quick test configuration: 5 tasks (one per category)
QUICK_TEST_TASKS = [
    "learned_hands_torts",  # Issue
    "international_citizenship_questions",  # Rule
    "hearsay",  # Conclusion
    "contract_qa",  # Interpretation
    "overruling",  # Rhetoric
]

# Category mapping
CATEGORY_MAP = {
    "ISSUE_TASKS": ISSUE_TASKS,
    "RULE_TASKS": RULE_TASKS,
    "CONCLUSION_TASKS": CONCLUSION_TASKS,
    "INTERPRETATION_TASKS": INTERPRETATION_TASKS,
    "RHETORIC_TASKS": RHETORIC_TASKS,
}


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Run Maite AI agent evaluation on LegalBench tasks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run specific tasks
  %(prog)s --tasks hearsay,personal_jurisdiction --samples 20

  # Run all tasks in a category
  %(prog)s --category CONCLUSION_TASKS --samples 10

  # Quick smoke test (5 tasks, 5 samples each)
  %(prog)s --quick

  # Custom output path
  %(prog)s --tasks hearsay --samples 10 --output my_run.json
        """,
    )

    # Task selection (mutually exclusive)
    task_group = parser.add_mutually_exclusive_group(required=True)
    task_group.add_argument(
        "--tasks",
        type=str,
        help="Comma-separated task names (e.g., 'hearsay,contract_qa')",
    )
    task_group.add_argument(
        "--category",
        type=str,
        choices=list(CATEGORY_MAP.keys()),
        help="Evaluate all tasks in a category",
    )
    task_group.add_argument(
        "--quick", action="store_true", help="Quick smoke test (5 tasks, 5 samples each)"
    )

    # Evaluation configuration
    parser.add_argument(
        "--samples",
        type=int,
        default=20,
        help="Number of samples per task (default: 20)",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Custom output path (default: results/run_TIMESTAMP.json)",
    )
    parser.add_argument(
        "--include-traces",
        action="store_true",
        help="Include detailed execution traces in output (increases file size)",
    )

    # Agent configuration
    parser.add_argument(
        "--model",
        type=str,
        default="claude-sonnet-4",
        help="Model to use (default: claude-sonnet-4)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Model temperature (default: 0.0)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Timeout per sample in seconds (default: 60)",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Maximum retries per sample (default: 3)",
    )

    return parser.parse_args()


def get_task_list(args: argparse.Namespace) -> List[str]:
    """
    Convert arguments to list of task names.

    Args:
        args: Parsed command-line arguments

    Returns:
        List of task names to evaluate
    """
    if args.tasks:
        # Parse comma-separated task list
        return [t.strip() for t in args.tasks.split(",")]
    elif args.category:
        # Get all tasks in category
        return CATEGORY_MAP[args.category].copy()
    elif args.quick:
        # Quick smoke test
        return QUICK_TEST_TASKS.copy()
    else:
        # Should never reach here due to mutually exclusive group
        raise ValueError("No task selection method specified")


def validate_tasks(task_names: List[str]) -> None:
    """
    Validate all task names exist in LegalBench.

    Args:
        task_names: List of task names to validate

    Raises:
        ValueError: If any task names are invalid
    """
    invalid_tasks = [t for t in task_names if t not in TASKS]

    if invalid_tasks:
        cprint(f"\n❌ Invalid task names:", "red", attrs=["bold"])
        for task in invalid_tasks:
            cprint(f"   - {task}", "red")

        cprint(f"\n💡 Hint: Use tasks from the LegalBench task list", "yellow")
        cprint(f"   Total available tasks: {len(TASKS)}", "yellow")
        cprint(f"   Example valid tasks: hearsay, contract_qa, personal_jurisdiction", "yellow")

        raise ValueError(f"Invalid task names: {', '.join(invalid_tasks)}")

    cprint(f"✅ Validated {len(task_names)} task(s)", "green")


def print_summary(evaluation_run: EvaluationRun) -> None:
    """
    Print formatted summary of evaluation results to console.

    Args:
        evaluation_run: Completed EvaluationRun with results
    """
    cprint("\n" + "=" * 80, "cyan", attrs=["bold"])
    cprint("Evaluation Summary".center(80), "cyan", attrs=["bold"])
    cprint("=" * 80, "cyan", attrs=["bold"])

    # Print run metadata
    cprint(f"\n📋 Run Information:", "cyan", attrs=["bold"])
    cprint(f"   Run ID: {evaluation_run.run_id}", "white")
    cprint(f"   Timestamp: {evaluation_run.timestamp}", "white")
    cprint(f"   Agent: {evaluation_run.agent_config.name}", "white")
    cprint(f"   Model: {evaluation_run.agent_config.model}", "white")
    cprint(f"   Tasks Evaluated: {len(evaluation_run.tasks)}", "white")
    cprint(f"   Samples per Task: {evaluation_run.samples_per_task}", "white")

    # Print per-task results
    cprint(f"\n📊 Task Results:", "cyan", attrs=["bold"])
    cprint("-" * 80, "cyan")

    # Header
    print(f"{'Task Name':<40} {'Metric':<25} {'Score':<10}")
    print("-" * 80)

    # Results
    for result in evaluation_run.results:
        score_str = f"{result.score:.4f}"

        # Color code based on score
        if result.score >= 0.8:
            score_color = "green"
        elif result.score >= 0.6:
            score_color = "yellow"
        else:
            score_color = "red"

        # Truncate task name if too long
        task_name = result.task_name
        if len(task_name) > 38:
            task_name = task_name[:35] + "..."

        print(
            f"{task_name:<40} {result.metric:<25} "
            + colored(f"{score_str:<10}", score_color, attrs=["bold"])
        )

        # Print errors if any
        if result.errors > 0:
            cprint(f"   ⚠️  {result.errors} error(s)", "yellow")

    # Print summary statistics
    summary = evaluation_run.compute_summary()

    cprint(f"\n📈 Overall Statistics:", "cyan", attrs=["bold"])
    cprint("-" * 80, "cyan")
    cprint(f"   Total Samples Evaluated: {summary['total_samples']}", "white")
    cprint(f"   Average Score: {summary['avg_accuracy']:.4f}", "white")
    cprint(f"   Total Execution Time: {summary['total_time']:.1f}s", "white")

    # Compute average time per sample
    if summary['total_samples'] > 0:
        avg_time_per_sample = summary['total_time'] / summary['total_samples']
        cprint(f"   Average Time per Sample: {avg_time_per_sample:.2f}s", "white")

    if summary.get("avg_tokens"):
        cprint(f"   Average Tokens per Sample: {summary['avg_tokens']:.1f}", "white")

    if summary.get("total_errors", 0) > 0:
        cprint(f"   Total Errors: {summary['total_errors']}", "red")

    cprint("\n" + "=" * 80, "cyan", attrs=["bold"])


def main() -> int:
    """
    Main CLI entry point.

    Returns:
        Exit code (0 = success, 1 = error)
    """
    try:
        # Print header
        print_header("Maite Agent Evaluation System")
        cprint("LegalBench Task Evaluation", "cyan")

        # Parse arguments
        cprint("\n📥 Parsing arguments...", "cyan")
        args = parse_arguments()

        # Get and validate task list
        cprint("\n🔍 Validating tasks...", "cyan")
        task_names = get_task_list(args)
        validate_tasks(task_names)

        # Print configuration
        cprint("\n⚙️  Configuration:", "cyan", attrs=["bold"])
        cprint(f"   Tasks: {', '.join(task_names[:3])}", "white")
        if len(task_names) > 3:
            cprint(f"   ... and {len(task_names) - 3} more", "white")
        cprint(f"   Samples per task: {args.samples if not args.quick else 5}", "white")
        cprint(f"   Model: {args.model}", "white")
        cprint(f"   Temperature: {args.temperature}", "white")
        cprint(f"   Timeout: {args.timeout}s", "white")
        cprint(f"   Include traces: {args.include_traces}", "white")

        # Initialize agent configuration
        cprint("\n🤖 Initializing agent...", "cyan")
        agent_config = AgentConfig(
            name="maite",
            model=args.model,
            temperature=args.temperature,
            timeout=args.timeout,
            max_retries=args.max_retries,
        )
        cprint("✅ Agent configuration created", "green")

        # Initialize agent wrapper
        agent_wrapper = MaiteAgentWrapper(agent_config)
        cprint("✅ Agent wrapper initialized", "green")

        # Initialize evaluator
        cprint("\n📋 Initializing evaluator...", "cyan")
        evaluator = LegalBenchEvaluator(agent_wrapper)

        # Create evaluation run
        run_id = generate_run_id(prefix="run")
        samples_per_task = 5 if args.quick else args.samples

        evaluation_run = EvaluationRun(
            run_id=run_id,
            agent_config=agent_config,
            tasks=task_names,
            samples_per_task=samples_per_task,
            results=[],
        )

        cprint(
            f"✅ Evaluation run created: {run_id}",
            "green",
        )

        # Run evaluation
        cprint(f"\n🚀 Starting evaluation on {len(task_names)} task(s)...", "cyan", attrs=["bold"])
        results = evaluator.evaluate_multiple(
            task_names=task_names,
            sample_size=samples_per_task,
            include_traces=args.include_traces,
        )

        # Add results to evaluation run
        for result in results:
            evaluation_run.add_result(result)

        # Print summary
        print_summary(evaluation_run)

        # Save results
        cprint("\n💾 Saving results...", "cyan")
        output_path = Path(args.output) if args.output else None
        saved_path = save_results(evaluation_run, output_path)

        # Final success message
        cprint("\n" + "=" * 80, "green", attrs=["bold"])
        print_success(f"Evaluation complete! Results saved to: {saved_path}")
        cprint("=" * 80, "green", attrs=["bold"])

        return 0

    except KeyboardInterrupt:
        cprint("\n\n⚠️  Evaluation interrupted by user", "yellow", attrs=["bold"])
        cprint("   Partial results not saved", "yellow")
        return 1

    except Exception as e:
        cprint(f"\n\n❌ Evaluation failed: {e}", "red", attrs=["bold"])
        import traceback

        cprint("\nTraceback:", "red")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
