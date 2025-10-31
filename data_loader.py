"""
Data loading utilities for LegalBench tasks.

Provides local-first data loading with automatic HuggingFace fallback.
"""

import pandas as pd
from pathlib import Path
from typing import Literal, Optional
from termcolor import cprint
import datasets


def load_task_data(
    task_name: str,
    split: Literal["train", "test"] = "test",
    use_hf_fallback: bool = True,
) -> pd.DataFrame:
    """
    Load task data from local TSV file with optional HuggingFace fallback.

    Strategy:
    1. First attempts to load from local tasks/{task_name}/{split}.tsv
    2. If local file missing and use_hf_fallback=True, downloads from HuggingFace and saves locally
    3. If local file missing and use_hf_fallback=False, raises FileNotFoundError

    Args:
        task_name: Name of the LegalBench task (e.g., "hearsay", "contract_qa")
        split: Which split to load ("train" or "test")
        use_hf_fallback: Whether to download from HuggingFace if local file missing

    Returns:
        DataFrame with task data (columns depend on task)

    Raises:
        FileNotFoundError: If local file missing and use_hf_fallback=False
        ValueError: If task_name not found on HuggingFace

    Examples:
        >>> # Load from local file (or download if missing)
        >>> test_df = load_task_data("hearsay", split="test")

        >>> # Require local file only
        >>> train_df = load_task_data("hearsay", split="train", use_hf_fallback=False)
    """
    local_path = Path(f"tasks/{task_name}/{split}.tsv")

    # Try loading from local file first
    if local_path.exists():
        return pd.read_csv(local_path, sep="\t", encoding="utf-8")

    # Local file doesn't exist
    if not use_hf_fallback:
        raise FileNotFoundError(
            f"Local file not found: {local_path}\n"
            f"Run: python scripts/download_legalbench_data.py"
        )

    # Fallback: Download from HuggingFace and save locally
    cprint(f"⚠️  Local file not found: {local_path}", "yellow")
    cprint(f"📥 Downloading from HuggingFace: nguha/legalbench/{task_name}", "cyan")

    try:
        # Download from HuggingFace
        dataset_dict = datasets.load_dataset(
            "nguha/legalbench",
            task_name,
            download_mode=datasets.DownloadMode.REUSE_DATASET_IF_EXISTS,
            trust_remote_code=True,
        )

        # Convert to pandas
        df = dataset_dict[split].to_pandas()

        # Save locally for future use
        local_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(local_path, sep="\t", index=False, encoding="utf-8")

        cprint(f"✅ Downloaded and saved to: {local_path}", "green")

        return df

    except Exception as e:
        raise ValueError(
            f"Failed to download task '{task_name}' from HuggingFace: {str(e)}\n"
            f"Available tasks listed in tasks.py"
        ) from e


def load_prompt_template(
    task_name: str,
    variant: str = "base"
) -> str:
    """
    Load prompt template for a task.

    Args:
        task_name: Name of the LegalBench task
        variant: Prompt variant ("base", "application", "rule_description", "claude", etc.)

    Returns:
        Prompt template string with {{column_name}} placeholders

    Raises:
        FileNotFoundError: If prompt file doesn't exist

    Examples:
        >>> template = load_prompt_template("hearsay", variant="base")
        >>> # Use with utils.generate_prompts(template, data_df)
    """
    prompt_path = Path(f"tasks/{task_name}/{variant}_prompt.txt")

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Prompt template not found: {prompt_path}\n"
            f"Available variants depend on task (check tasks/{task_name}/ directory)"
        )

    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def task_data_exists_locally(task_name: str) -> dict[str, bool]:
    """
    Check if task data files exist locally.

    Args:
        task_name: Name of the LegalBench task

    Returns:
        Dictionary with keys "train" and "test", values are boolean (file exists)

    Examples:
        >>> status = task_data_exists_locally("hearsay")
        >>> print(status)  # {'train': True, 'test': False}
    """
    return {
        "train": Path(f"tasks/{task_name}/train.tsv").exists(),
        "test": Path(f"tasks/{task_name}/test.tsv").exists(),
    }


def get_local_task_status(task_names: list[str]) -> pd.DataFrame:
    """
    Get status of multiple tasks (which files exist locally).

    Args:
        task_names: List of task names to check

    Returns:
        DataFrame with columns: task_name, train_exists, test_exists

    Examples:
        >>> from tasks import ISSUE_TASKS
        >>> status_df = get_local_task_status(ISSUE_TASKS)
        >>> print(status_df)
    """
    results = []

    for task_name in task_names:
        status = task_data_exists_locally(task_name)
        results.append({
            "task_name": task_name,
            "train_exists": status["train"],
            "test_exists": status["test"],
        })

    return pd.DataFrame(results)
