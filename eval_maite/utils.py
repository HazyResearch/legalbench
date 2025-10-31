"""
Helper utilities for Maite evaluation system.

Provides functions for run ID generation, result persistence, and colored output.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from termcolor import colored, cprint

from eval_maite.models import EvaluationRun

# Import from canonical LegalBench evaluation module
try:
    from evaluation import EXACT_MATCH_BALANCED_ACC_TASKS
except ImportError:
    # Fallback if import fails (e.g., testing environment)
    EXACT_MATCH_BALANCED_ACC_TASKS = []


def generate_run_id(prefix: str = "run") -> str:
    """
    Generate a timestamped run ID.

    Args:
        prefix: Prefix for the run ID (default: "run")

    Returns:
        Run ID string (e.g., "run_20251028_153000")
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = f"{prefix}_{timestamp}"
    cprint(f"🆔 Generated run ID: {run_id}", "cyan")
    return run_id


def save_results(run: EvaluationRun, output_path: Optional[Path] = None) -> Path:
    """
    Save evaluation results to JSON file.

    Args:
        run: EvaluationRun instance to save
        output_path: Optional custom output path. If None, saves to results/{run_id}.json

    Returns:
        Path to saved file
    """
    if output_path is None:
        results_dir = Path(__file__).parent.parent / "results"
        results_dir.mkdir(exist_ok=True)
        output_path = results_dir / f"{run.run_id}.json"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    cprint(f"💾 Saving results to: {output_path}", "cyan")

    # Convert to dict and handle datetime serialization
    data = run.model_dump(mode="json")

    # Pretty-print JSON with indent=2
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    file_size = output_path.stat().st_size / 1024  # KB
    cprint(f"✅ Results saved ({file_size:.1f} KB)", "green")

    return output_path


def load_results(path: Path) -> EvaluationRun:
    """
    Load evaluation results from JSON file.

    Args:
        path: Path to JSON file

    Returns:
        EvaluationRun instance

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If JSON is invalid or doesn't match schema
    """
    path = Path(path)

    if not path.exists():
        cprint(f"❌ File not found: {path}", "red")
        raise FileNotFoundError(f"Results file not found: {path}")

    cprint(f"📂 Loading results from: {path}", "cyan")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    try:
        run = EvaluationRun(**data)
        cprint(f"✅ Loaded run: {run.run_id}", "green")
        cprint(f"   Tasks: {len(run.tasks)}, Results: {len(run.results)}", "white")
        return run
    except Exception as e:
        cprint(f"❌ Failed to parse results: {e}", "red")
        raise ValueError(f"Invalid results file format: {e}")


def print_header(text: str, color: str = "cyan") -> None:
    """
    Print a formatted header with color.

    Args:
        text: Header text
        color: Color name for termcolor
    """
    separator = "=" * 60
    cprint(separator, color)
    cprint(text.center(60), color, attrs=["bold"])
    cprint(separator, color)


def print_section(title: str, color: str = "cyan") -> None:
    """
    Print a section divider.

    Args:
        title: Section title
        color: Color name for termcolor
    """
    cprint(f"\n{'─' * 60}", color)
    cprint(f"  {title}", color, attrs=["bold"])
    cprint(f"{'─' * 60}", color)


def print_metric(label: str, value: any, color: str = "white") -> None:
    """
    Print a labeled metric.

    Args:
        label: Metric label
        value: Metric value
        color: Color for the value
    """
    print(f"  {label:<30} {colored(str(value), color)}")


def print_error(message: str) -> None:
    """Print an error message with formatting."""
    cprint(f"❌ ERROR: {message}", "red", attrs=["bold"])


def print_warning(message: str) -> None:
    """Print a warning message with formatting."""
    cprint(f"⚠️  WARNING: {message}", "yellow")


def print_success(message: str) -> None:
    """Print a success message with formatting."""
    cprint(f"✅ {message}", "green", attrs=["bold"])


def print_info(message: str) -> None:
    """Print an info message with formatting."""
    cprint(f"ℹ️  {message}", "cyan")


def get_metric_name(task_name: str) -> str:
    """
    Determine evaluation metric used for a task.

    Replicates logic from evaluation.evaluate() to determine which
    metric is used for scoring. This is necessary because evaluate()
    returns only a float score without identifying the metric used.

    IMPORTANT: Order matters! Check specific tasks before EXACT_MATCH_BALANCED_ACC_TASKS.

    Args:
        task_name: Name of LegalBench task (e.g., "hearsay")

    Returns:
        Metric name string (e.g., "balanced_accuracy", "f1_score")
    """
    # Replicate evaluation.py logic - ORDER MATTERS!
    # Check specific tasks BEFORE general categories
    if task_name == "sara_numeric":
        return "numeric_tolerance"
    elif task_name == "successor_liability":
        return "f1_score"
    elif task_name == "citation_prediction_open":
        return "contains_match"
    elif task_name == "definition_extraction":
        return "balanced_accuracy_stemmed"
    elif task_name.startswith("ssla_"):
        return "f1_score"
    elif task_name == "rule_qa":
        return "manual_evaluation"
    elif task_name in EXACT_MATCH_BALANCED_ACC_TASKS:
        return "balanced_accuracy"
    else:
        # Default fallback for most tasks
        return "balanced_accuracy"
