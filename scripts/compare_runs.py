"""
Comparison tool for Maite evaluation runs.

Compares two evaluation runs and generates detailed comparison reports
with improvement/regression indicators.

Usage:
    python scripts/compare_runs.py results/run1.json results/run2.json
    python scripts/compare_runs.py run1.json run2.json --format markdown
    python scripts/compare_runs.py run1.json run2.json --threshold 0.05 --output comparison.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

from termcolor import colored, cprint

from eval_maite.models import EvaluationRun, TaskResult
from eval_maite.utils import load_results, print_error, print_header, print_success


def parse_arguments() -> argparse.Namespace:
    """
    Parse CLI arguments for comparison.

    Returns:
        Parsed arguments with run1_path, run2_path, format, threshold, output
    """
    parser = argparse.ArgumentParser(
        description="Compare two Maite evaluation runs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/compare_runs.py results/run1.json results/run2.json
  python scripts/compare_runs.py run1.json run2.json --format markdown
  python scripts/compare_runs.py run1.json run2.json --threshold 0.05 --output comparison.json
        """,
    )

    # Positional arguments
    parser.add_argument(
        "run1_path",
        type=str,
        help="Path to first evaluation run JSON file",
    )
    parser.add_argument(
        "run2_path",
        type=str,
        help="Path to second evaluation run JSON file",
    )

    # Optional arguments
    parser.add_argument(
        "--format",
        type=str,
        choices=["table", "json", "markdown"],
        default="table",
        help="Output format (default: table)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.01,
        help="Significance threshold for 'unchanged' classification (default: 0.01)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Optional path to save comparison JSON",
    )

    args = parser.parse_args()

    # Only print argument summary for non-JSON formats
    if args.format != "json":
        cprint(f"📋 Parsed arguments:", "cyan")
        cprint(f"   Run 1: {args.run1_path}", "white")
        cprint(f"   Run 2: {args.run2_path}", "white")
        cprint(f"   Format: {args.format}", "white")
        cprint(f"   Threshold: {args.threshold}", "white")
        if args.output:
            cprint(f"   Output: {args.output}", "white")

    return args


def load_runs(path1: Path, path2: Path) -> Tuple[EvaluationRun, EvaluationRun]:
    """
    Load two evaluation runs from JSON files.

    Args:
        path1: Path to first evaluation run
        path2: Path to second evaluation run

    Returns:
        Tuple of (run1, run2) EvaluationRun objects

    Raises:
        FileNotFoundError: If either file doesn't exist
        ValueError: If either file is invalid JSON or doesn't match schema
    """
    cprint(f"\n📂 Loading evaluation runs...", "cyan")

    # Load run 1
    run1 = load_results(path1)

    # Load run 2
    run2 = load_results(path2)

    cprint(f"✅ Successfully loaded both runs", "green")
    return run1, run2


def build_task_comparison_map(
    run1: EvaluationRun, run2: EvaluationRun, verbose: bool = True
) -> Dict[str, Dict[str, Any]]:
    """
    Create unified comparison map of all tasks across both runs.

    Args:
        run1: First evaluation run
        run2: Second evaluation run
        verbose: Whether to print status messages

    Returns:
        Dictionary mapping task_name to comparison data:
        {
            "task_name": {
                "run1_result": TaskResult | None,
                "run2_result": TaskResult | None,
                "status": "both" | "run1_only" | "run2_only"
            }
        }
    """
    if verbose:
        cprint(f"\n🔍 Building task comparison map...", "cyan")

    comparison_map: Dict[str, Dict[str, Any]] = {}

    # Add all tasks from run1
    for result in run1.results:
        comparison_map[result.task_name] = {
            "run1_result": result,
            "run2_result": None,
            "status": "run1_only",
        }

    # Add/update tasks from run2
    for result in run2.results:
        if result.task_name in comparison_map:
            # Task exists in both runs
            comparison_map[result.task_name]["run2_result"] = result
            comparison_map[result.task_name]["status"] = "both"
        else:
            # Task only in run2
            comparison_map[result.task_name] = {
                "run1_result": None,
                "run2_result": result,
                "status": "run2_only",
            }

    # Count task distribution
    if verbose:
        both_count = sum(1 for v in comparison_map.values() if v["status"] == "both")
        run1_only = sum(1 for v in comparison_map.values() if v["status"] == "run1_only")
        run2_only = sum(1 for v in comparison_map.values() if v["status"] == "run2_only")

        cprint(f"   Tasks in both runs: {both_count}", "white")
        if run1_only > 0:
            cprint(f"   Tasks only in run1: {run1_only}", "yellow")
        if run2_only > 0:
            cprint(f"   Tasks only in run2: {run2_only}", "yellow")

    return comparison_map


def calculate_delta(
    score1: float, score2: float, threshold: float = 0.01
) -> Dict[str, Any]:
    """
    Calculate delta with direction and indicator.

    Args:
        score1: Score from first run
        score2: Score from second run
        threshold: Minimum absolute difference to consider "changed"

    Returns:
        Dictionary with:
        - absolute: Absolute delta (score2 - score1)
        - percentage: Percentage change (0.0 when score1 == 0, indicating undefined)
        - direction: "improvement" | "regression" | "unchanged"
        - indicator: "↑" | "↓" | "→"

    Note:
        When score1 is 0, percentage is set to 0.0 to avoid division by zero.
        This indicates the percentage change is undefined, not that there was no change.
    """
    absolute = score2 - score1
    # Percentage is 0.0 when score1 == 0 (undefined percentage, not "no change")
    percentage = ((score2 - score1) / score1 * 100) if score1 != 0 else 0.0

    # Determine direction based on threshold
    if abs(absolute) < threshold:
        direction = "unchanged"
        indicator = "→"
    elif absolute > 0:
        direction = "improvement"
        indicator = "↑"
    else:
        direction = "regression"
        indicator = "↓"

    return {
        "absolute": absolute,
        "percentage": percentage,
        "direction": direction,
        "indicator": indicator,
    }


def format_delta_string(delta: Dict[str, Any]) -> str:
    """
    Format delta for colored display.

    Args:
        delta: Delta dictionary from calculate_delta()

    Returns:
        Colored string like "+0.020↑" (green), "-0.015↓" (red), or " 0.000→" (yellow)
    """
    absolute = delta["absolute"]
    indicator = delta["indicator"]
    direction = delta["direction"]

    # Format with sign and indicator
    if absolute >= 0:
        text = f"+{absolute:.4f}{indicator}"
    else:
        text = f"{absolute:.4f}{indicator}"

    # Apply color based on direction
    if direction == "improvement":
        return colored(text, "green")
    elif direction == "regression":
        return colored(text, "red")
    else:  # unchanged
        return colored(text, "yellow")


def _get_sorted_tasks(comparison_map: Dict[str, Dict], threshold: float) -> List[Tuple[str, Dict]]:
    """
    Sort tasks by delta magnitude (descending), then by name (ascending).

    Args:
        comparison_map: Task comparison map
        threshold: Significance threshold for delta calculation

    Returns:
        Sorted list of (task_name, data) tuples
    """
    def get_sort_key(item):
        task_name, data = item
        if data["status"] == "both":
            score1 = data["run1_result"].score
            score2 = data["run2_result"].score
            magnitude = abs(score2 - score1)
        else:
            magnitude = 0.0
        # Return tuple: (magnitude descending, task_name ascending)
        return (-magnitude, task_name)

    return sorted(comparison_map.items(), key=get_sort_key)


def print_comparison_table(
    comparison_map: Dict[str, Dict], threshold: float
) -> None:
    """
    Print formatted comparison table.

    Args:
        comparison_map: Task comparison map from build_task_comparison_map()
        threshold: Significance threshold for delta calculation
    """
    cprint(f"\n📊 Task-by-Task Comparison:", "cyan", attrs=["bold"])

    # Sort tasks by magnitude (descending), then name (ascending)
    sorted_tasks = _get_sorted_tasks(comparison_map, threshold)

    # Print table header
    print("─" * 100)
    print(
        f"{'Task Name':<40} {'Run 1':>10} {'Run 2':>10} {'Delta':>15} {'Metric':<20}"
    )
    print("─" * 100)

    # Print each task
    for task_name, data in sorted_tasks:
        status = data["status"]

        if status == "both":
            # Task in both runs - show comparison
            result1 = data["run1_result"]
            result2 = data["run2_result"]

            score1 = result1.score
            score2 = result2.score
            metric = result1.metric

            # Check for metric mismatch
            if result1.metric != result2.metric:
                metric = f"{result1.metric}/{result2.metric} ⚠️"

            delta = calculate_delta(score1, score2, threshold)
            delta_str = format_delta_string(delta)

            # Truncate task name if too long
            display_name = task_name[:38] + ".." if len(task_name) > 40 else task_name

            print(
                f"{display_name:<40} {score1:>10.4f} {score2:>10.4f} {delta_str:>23} {metric:<20}"
            )

        elif status == "run1_only":
            # Task only in run1 (removed in run2)
            result1 = data["run1_result"]
            score1 = result1.score
            metric = result1.metric

            display_name = task_name[:38] + ".." if len(task_name) > 40 else task_name
            warning = colored("⚠️  N/A", "yellow")

            print(
                f"{display_name:<40} {score1:>10.4f} {warning:>18} {'(removed)':>15} {metric:<20}"
            )

        else:  # run2_only
            # Task only in run2 (new in run2)
            result2 = data["run2_result"]
            score2 = result2.score
            metric = result2.metric

            display_name = task_name[:38] + ".." if len(task_name) > 40 else task_name
            warning = colored("⚠️  N/A", "yellow")

            print(
                f"{display_name:<40} {warning:>18} {score2:>10.4f} {'(new in run2)':>15} {metric:<20}"
            )

    print("─" * 100)


def print_summary_comparison(run1: EvaluationRun, run2: EvaluationRun) -> None:
    """
    Print overall statistics comparison.

    Args:
        run1: First evaluation run
        run2: Second evaluation run
    """
    cprint(f"\n📈 Overall Statistics Comparison:", "cyan", attrs=["bold"])
    print("─" * 80)

    # Get summaries
    summary1 = run1.compute_summary()
    summary2 = run2.compute_summary()

    # Total samples
    samples1 = summary1["total_samples"]
    samples2 = summary2["total_samples"]
    samples_diff = samples2 - samples1
    samples_sign = "+" if samples_diff >= 0 else ""
    print(
        f"   Total Samples:        {samples1} → {samples2} ({samples_sign}{samples_diff})"
    )

    # Average accuracy
    acc1 = summary1["avg_accuracy"]
    acc2 = summary2["avg_accuracy"]
    acc_delta = calculate_delta(acc1, acc2, threshold=0.01)
    acc_delta_str = format_delta_string(acc_delta)
    print(f"   Average Score:        {acc1:.4f} → {acc2:.4f} ({acc_delta_str})")

    # Total time
    time1 = summary1["total_time"]
    time2 = summary2["total_time"]
    time_diff = time2 - time1
    time_sign = "+" if time_diff >= 0 else ""
    print(
        f"   Total Time:           {time1:.1f}s → {time2:.1f}s ({time_sign}{time_diff:.1f}s)"
    )

    # Total errors
    errors1 = summary1["total_errors"]
    errors2 = summary2["total_errors"]
    errors_diff = errors2 - errors1
    errors_sign = "+" if errors_diff >= 0 else ""
    error_color = "red" if errors2 > errors1 else "green" if errors2 < errors1 else "white"
    errors_text = colored(
        f"{errors1} → {errors2} ({errors_sign}{errors_diff})", error_color
    )
    print(f"   Total Errors:         {errors_text}")

    print("─" * 80)


def print_metadata_comparison(run1: EvaluationRun, run2: EvaluationRun) -> None:
    """
    Print run metadata comparison.

    Args:
        run1: First evaluation run
        run2: Second evaluation run
    """
    cprint(f"\n📋 Run Metadata:", "cyan", attrs=["bold"])
    print("─" * 80)

    # Run IDs and timestamps
    print(f"   Run 1: {run1.run_id} ({run1.timestamp})")
    print(f"   Run 2: {run2.run_id} ({run2.timestamp})")
    print()

    # Agent configuration
    config1 = run1.agent_config
    config2 = run2.agent_config

    print(f"   Agent: {config1.name}")

    # Model
    if config1.model == config2.model:
        print(f"   Model: {config1.model} (same)")
    else:
        print(
            f"   Model: {colored(config1.model, 'yellow')} → {colored(config2.model, 'yellow')} (DIFFERENT)"
        )

    # Temperature
    if config1.temperature == config2.temperature:
        print(f"   Temperature: {config1.temperature} (same)")
    else:
        print(
            f"   Temperature: {colored(str(config1.temperature), 'yellow')} → {colored(str(config2.temperature), 'yellow')} (DIFFERENT)"
        )

    # Timeout
    if config1.timeout == config2.timeout:
        print(f"   Timeout: {config1.timeout}s (same)")
    else:
        print(
            f"   Timeout: {colored(str(config1.timeout), 'yellow')}s → {colored(str(config2.timeout), 'yellow')}s (DIFFERENT)"
        )

    # Samples per task
    if run1.samples_per_task == run2.samples_per_task:
        print(f"   Samples per task: {run1.samples_per_task} (same)")
    else:
        print(
            f"   Samples per task: {colored(str(run1.samples_per_task), 'yellow')} → {colored(str(run2.samples_per_task), 'yellow')} (DIFFERENT)"
        )

    print("─" * 80)


def print_comparison_markdown(
    comparison_map: Dict[str, Dict], threshold: float
) -> None:
    """
    Print comparison in markdown table format.

    Args:
        comparison_map: Task comparison map from build_task_comparison_map()
        threshold: Significance threshold for delta calculation
    """
    print("\n## Task-by-Task Comparison\n")

    # Sort tasks by magnitude (descending), then name (ascending)
    sorted_tasks = _get_sorted_tasks(comparison_map, threshold)

    # Print markdown table header
    print("| Task Name | Run 1 | Run 2 | Delta | Metric |")
    print("|-----------|-------|-------|-------|--------|")

    # Print each task
    for task_name, data in sorted_tasks:
        status = data["status"]

        if status == "both":
            # Task in both runs - show comparison
            result1 = data["run1_result"]
            result2 = data["run2_result"]

            score1 = result1.score
            score2 = result2.score
            metric = result1.metric

            delta = calculate_delta(score1, score2, threshold)

            # Format delta without color codes for markdown
            if delta["absolute"] >= 0:
                delta_text = f"+{delta['absolute']:.4f}{delta['indicator']}"
            else:
                delta_text = f"{delta['absolute']:.4f}{delta['indicator']}"

            # Check for metric mismatch
            metric_display = metric
            if result2.metric != result1.metric:
                metric_display = f"{result1.metric} → {result2.metric}"

            print(f"| {task_name} | {score1:.4f} | {score2:.4f} | {delta_text} | {metric_display} |")

        elif status == "run1_only":
            # Task only in run1 (removed in run2)
            result1 = data["run1_result"]
            score1 = result1.score
            metric = result1.metric

            print(f"| {task_name} | {score1:.4f} | N/A | (removed) | {metric} |")

        else:  # run2_only
            # Task only in run2 (new in run2)
            result2 = data["run2_result"]
            score2 = result2.score
            metric = result2.metric

            print(f"| {task_name} | N/A | {score2:.4f} | (new) | {metric} |")


def print_comparison_json(
    comparison_map: Dict[str, Dict],
    run1: EvaluationRun,
    run2: EvaluationRun,
    threshold: float,
) -> None:
    """
    Print comparison in JSON format to stdout.

    Args:
        comparison_map: Task comparison map
        run1: First evaluation run
        run2: Second evaluation run
        threshold: Significance threshold
    """
    # Build task comparisons
    task_comparisons = []
    sorted_tasks = _get_sorted_tasks(comparison_map, threshold)

    for task_name, data in sorted_tasks:
        task_comp = {
            "task_name": task_name,
            "status": data["status"],
        }

        if data["status"] == "both":
            result1 = data["run1_result"]
            result2 = data["run2_result"]
            delta = calculate_delta(result1.score, result2.score, threshold)

            task_comp["run1_score"] = result1.score
            task_comp["run2_score"] = result2.score
            task_comp["delta"] = delta
            task_comp["metric"] = result1.metric

            # Flag metric mismatch
            if result1.metric != result2.metric:
                task_comp["metric_mismatch"] = True
                task_comp["run1_metric"] = result1.metric
                task_comp["run2_metric"] = result2.metric

        elif data["status"] == "run1_only":
            task_comp["run1_score"] = data["run1_result"].score
            task_comp["metric"] = data["run1_result"].metric
            task_comp["delta"] = None

        else:  # run2_only
            task_comp["run2_score"] = data["run2_result"].score
            task_comp["metric"] = data["run2_result"].metric
            task_comp["delta"] = None

        task_comparisons.append(task_comp)

    # Build full comparison
    comparison = {
        "comparison_timestamp": str(run2.timestamp),
        "run1": {
            "run_id": run1.run_id,
            "timestamp": str(run1.timestamp),
            "summary": run1.compute_summary(),
        },
        "run2": {
            "run_id": run2.run_id,
            "timestamp": str(run2.timestamp),
            "summary": run2.compute_summary(),
        },
        "task_comparisons": task_comparisons,
        "config_differences": detect_configuration_differences(run1, run2),
    }

    # Print formatted JSON
    print(json.dumps(comparison, indent=2, ensure_ascii=False))


def detect_configuration_differences(
    run1: EvaluationRun, run2: EvaluationRun
) -> List[str]:
    """
    Detect and return configuration difference warnings.

    Args:
        run1: First evaluation run
        run2: Second evaluation run

    Returns:
        List of warning messages for configuration differences
    """
    warnings = []

    config1 = run1.agent_config
    config2 = run2.agent_config

    # Check model
    if config1.model != config2.model:
        warnings.append(
            f"Different models: {config1.model} vs {config2.model}"
        )

    # Check temperature
    if config1.temperature != config2.temperature:
        warnings.append(
            f"Different temperatures: {config1.temperature} vs {config2.temperature}"
        )

    # Check timeout
    if config1.timeout != config2.timeout:
        warnings.append(
            f"Different timeouts: {config1.timeout}s vs {config2.timeout}s"
        )

    # Check samples per task
    if run1.samples_per_task != run2.samples_per_task:
        warnings.append(
            f"Different sample sizes: {run1.samples_per_task} vs {run2.samples_per_task}"
        )

    # Check max retries
    if config1.max_retries != config2.max_retries:
        warnings.append(
            f"Different max retries: {config1.max_retries} vs {config2.max_retries}"
        )

    return warnings


def export_comparison_json(
    comparison_map: Dict,
    run1: EvaluationRun,
    run2: EvaluationRun,
    output_path: Path,
) -> None:
    """
    Export comparison to JSON file.

    Args:
        comparison_map: Task comparison map
        run1: First evaluation run
        run2: Second evaluation run
        output_path: Path to save JSON file
    """
    cprint(f"\n💾 Exporting comparison to JSON...", "cyan")

    # Build comparison data
    task_comparisons = []
    for task_name, data in comparison_map.items():
        task_comp = {
            "task_name": task_name,
            "status": data["status"],
        }

        if data["status"] == "both":
            result1 = data["run1_result"]
            result2 = data["run2_result"]
            delta = calculate_delta(result1.score, result2.score)

            task_comp["run1_score"] = result1.score
            task_comp["run2_score"] = result2.score
            task_comp["delta"] = delta
            task_comp["metric"] = result1.metric

        elif data["status"] == "run1_only":
            task_comp["run1_score"] = data["run1_result"].score
            task_comp["metric"] = data["run1_result"].metric

        else:  # run2_only
            task_comp["run2_score"] = data["run2_result"].score
            task_comp["metric"] = data["run2_result"].metric

        task_comparisons.append(task_comp)

    # Build full comparison document
    comparison = {
        "comparison_timestamp": str(run2.timestamp),  # Convert datetime to string
        "run1": {
            "run_id": run1.run_id,
            "timestamp": str(run1.timestamp),  # Convert datetime to string
            "summary": run1.compute_summary(),
        },
        "run2": {
            "run_id": run2.run_id,
            "timestamp": str(run2.timestamp),  # Convert datetime to string
            "summary": run2.compute_summary(),
        },
        "task_comparisons": task_comparisons,
        "config_differences": detect_configuration_differences(run1, run2),
    }

    # Save to file
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(comparison, f, indent=2, ensure_ascii=False)

    file_size = output_path.stat().st_size / 1024  # KB
    cprint(f"✅ Comparison saved to {output_path} ({file_size:.1f} KB)", "green")


def main() -> int:
    """
    CLI entry point.

    Returns:
        Exit code (0 = success, 1 = error)
    """
    try:
        # Parse arguments first to check format
        args = parse_arguments()

        # Only print headers/status for non-JSON formats (to avoid polluting JSON output)
        verbose = args.format != "json"

        if verbose:
            # Print header
            print_header("Evaluation Comparison Report")

        # Convert paths
        path1 = Path(args.run1_path)
        path2 = Path(args.run2_path)

        # Load runs (suppress verbose output for JSON format)
        if verbose:
            run1, run2 = load_runs(path1, path2)
        else:
            # Quiet loading for JSON output
            run1 = load_results(path1)
            run2 = load_results(path2)

        # Detect configuration differences
        config_diffs = detect_configuration_differences(run1, run2)
        if config_diffs and verbose:
            cprint(f"\n⚠️  Configuration Differences Detected:", "yellow", attrs=["bold"])
            for diff in config_diffs:
                cprint(f"   - {diff}", "yellow")
            cprint(
                f"\n💡 Note: Results may not be directly comparable due to configuration differences.",
                "cyan",
            )

        # Build comparison map
        comparison_map = build_task_comparison_map(run1, run2, verbose=verbose)

        # Output in requested format
        if args.format == "json":
            # JSON format to stdout
            print_comparison_json(comparison_map, run1, run2, args.threshold)
        elif args.format == "markdown":
            # Markdown format
            print_metadata_comparison(run1, run2)
            print_comparison_markdown(comparison_map, args.threshold)
            print_summary_comparison(run1, run2)
        else:  # table (default)
            # Standard table format
            print_metadata_comparison(run1, run2)
            print_comparison_table(comparison_map, args.threshold)
            print_summary_comparison(run1, run2)

        # Export JSON if requested (separate from stdout format)
        if args.output:
            export_comparison_json(comparison_map, run1, run2, Path(args.output))

        # Success message (skip for JSON stdout to avoid polluting output)
        if args.format != "json":
            print_success("Comparison complete!")

        return 0

    except FileNotFoundError as e:
        print_error(f"File not found: {e}")
        return 1
    except ValueError as e:
        print_error(f"Invalid data: {e}")
        return 1
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
