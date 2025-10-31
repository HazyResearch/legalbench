#!/usr/bin/env python3
"""
Download all LegalBench task data from HuggingFace.

Pre-downloads all 162 tasks (train.tsv + test.tsv) for offline use.
Run once to enable local-first data loading in notebooks and scripts.

Usage:
    python scripts/download_legalbench_data.py
"""

import sys
import time
from pathlib import Path
from typing import Optional

import datasets
import pandas as pd
from termcolor import colored, cprint

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tasks import TASKS


def download_task(
    task_name: str,
    overwrite: bool = False,
    verbose: bool = True
) -> tuple[bool, Optional[str]]:
    """
    Download a single task from HuggingFace and save locally.

    Args:
        task_name: Name of the task to download
        overwrite: Whether to overwrite existing files
        verbose: Whether to print progress messages

    Returns:
        Tuple of (success: bool, error_message: Optional[str])
    """
    task_dir = Path(f"tasks/{task_name}")
    train_path = task_dir / "train.tsv"
    test_path = task_dir / "test.tsv"

    # Check if files already exist
    if not overwrite:
        if train_path.exists() and test_path.exists():
            if verbose:
                cprint(f"  ⏭️  {task_name:<40} Already exists (both splits)", "cyan")
            return True, None

    try:
        # Download from HuggingFace
        if verbose:
            print(f"  📥 {task_name:<40} Downloading...", end="\r")

        dataset_dict = datasets.load_dataset(
            "nguha/legalbench",
            task_name,
            download_mode=datasets.DownloadMode.REUSE_DATASET_IF_EXISTS,
            trust_remote_code=True,
        )

        # Ensure directory exists
        task_dir.mkdir(parents=True, exist_ok=True)

        # Save test split first (needed for zero-shot tasks)
        test_df = dataset_dict["test"].to_pandas()
        test_df.to_csv(test_path, sep="\t", index=False, encoding="utf-8")
        test_count = len(test_df)

        # Save train split (if exists - some tasks are zero-shot)
        if "train" in dataset_dict:
            train_df = dataset_dict["train"].to_pandas()
            train_df.to_csv(train_path, sep="\t", index=False, encoding="utf-8")
            train_count = len(train_df)
        else:
            # Zero-shot task - create empty train file with same columns as test
            empty_train = pd.DataFrame(columns=test_df.columns)
            empty_train.to_csv(train_path, sep="\t", index=False, encoding="utf-8")
            train_count = 0

        if verbose:
            zero_shot = " (zero-shot)" if train_count == 0 else ""
            cprint(
                f"  ✅ {task_name:<40} Downloaded (train: {train_count}, test: {test_count}){zero_shot}",
                "green"
            )

        return True, None

    except Exception as e:
        error_msg = str(e)[:60]
        if verbose:
            cprint(f"  ❌ {task_name:<40} Error: {error_msg}", "red")
        return False, error_msg


def download_all_tasks(overwrite: bool = False) -> dict:
    """
    Download all LegalBench tasks.

    Args:
        overwrite: Whether to overwrite existing files

    Returns:
        Dictionary with download statistics
    """
    cprint("\n" + "=" * 80, "cyan", attrs=["bold"])
    cprint("  LegalBench Data Download", "cyan", attrs=["bold"])
    cprint("=" * 80 + "\n", "cyan", attrs=["bold"])

    cprint(f"📊 Total tasks to process: {len(TASKS)}", "white", attrs=["bold"])
    cprint(f"📁 Target directory: tasks/", "white")
    cprint(f"🔄 Overwrite existing: {overwrite}\n", "white")

    start_time = time.time()

    stats = {
        "total": len(TASKS),
        "success": 0,
        "skipped": 0,
        "failed": 0,
        "errors": [],
    }

    # Download each task
    for i, task_name in enumerate(TASKS, 1):
        # Progress indicator
        progress = f"[{i}/{len(TASKS)}]"
        print(colored(progress, "yellow", attrs=["bold"]), end=" ")

        # Download
        success, error_msg = download_task(task_name, overwrite=overwrite, verbose=True)

        if success:
            # Check if it was skipped or downloaded
            train_path = Path(f"tasks/{task_name}/train.tsv")
            test_path = Path(f"tasks/{task_name}/test.tsv")
            if not overwrite and train_path.exists() and test_path.exists():
                stats["skipped"] += 1
            else:
                stats["success"] += 1
        else:
            stats["failed"] += 1
            stats["errors"].append((task_name, error_msg))

    # Print summary
    elapsed_time = time.time() - start_time

    cprint("\n" + "=" * 80, "cyan", attrs=["bold"])
    cprint("  Download Summary", "cyan", attrs=["bold"])
    cprint("=" * 80 + "\n", "cyan", attrs=["bold"])

    cprint(f"✅ Successfully downloaded: {stats['success']}", "green", attrs=["bold"])
    cprint(f"⏭️  Skipped (already exists): {stats['skipped']}", "cyan")
    cprint(f"❌ Failed: {stats['failed']}", "red" if stats["failed"] > 0 else "green")
    cprint(f"⏱️  Total time: {elapsed_time:.2f}s\n", "white")

    # Print errors if any
    if stats["errors"]:
        cprint("Failed tasks:", "red", attrs=["bold"])
        for task_name, error_msg in stats["errors"]:
            cprint(f"  - {task_name}: {error_msg}", "red")
        cprint("")

    # Final status
    if stats["failed"] == 0:
        cprint("🎉 All tasks downloaded successfully!", "green", attrs=["bold"])
        cprint("📓 Notebooks will now use local data files.\n", "green")
    else:
        cprint("⚠️  Some tasks failed to download.", "yellow", attrs=["bold"])
        cprint("📓 Notebooks will fall back to HuggingFace for failed tasks.\n", "yellow")

    return stats


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Download all LegalBench task data from HuggingFace",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download all tasks (skip existing files)
  python scripts/download_legalbench_data.py

  # Overwrite existing files
  python scripts/download_legalbench_data.py --overwrite

This will download all 162 tasks from HuggingFace and save them to:
  tasks/{task_name}/train.tsv
  tasks/{task_name}/test.tsv

Estimated time: 3-5 minutes
Required disk space: ~500MB-1GB
        """
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files (default: skip existing)"
    )

    args = parser.parse_args()

    try:
        stats = download_all_tasks(overwrite=args.overwrite)

        # Exit with error code if any failures
        if stats["failed"] > 0:
            sys.exit(1)

    except KeyboardInterrupt:
        cprint("\n\n⚠️  Download interrupted by user", "yellow", attrs=["bold"])
        sys.exit(130)
    except Exception as e:
        cprint(f"\n\n❌ Fatal error: {str(e)}", "red", attrs=["bold"])
        sys.exit(1)


if __name__ == "__main__":
    main()
