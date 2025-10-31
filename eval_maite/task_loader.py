"""
Task loader for LegalBench tasks following canonical patterns.

Loads tasks from HuggingFace datasets and local files.
"""

import os
from pathlib import Path
from typing import Dict, Optional

import datasets
import pandas as pd
from termcolor import cprint

# Import task lists from LegalBench
from tasks import (
    CONCLUSION_TASKS,
    INTERPRETATION_TASKS,
    ISSUE_TASKS,
    RHETORIC_TASKS,
    RULE_TASKS,
    TASKS,
)

# Suppress HuggingFace progress bars (canonical pattern)
datasets.utils.logging.set_verbosity_error()

# Task directory base path
TASK_DIR = Path(__file__).parent.parent / "tasks"


def load_task_data(task_name: str, cache_dir: Optional[str] = None) -> datasets.DatasetDict:
    """
    Load task data from HuggingFace (canonical pattern).

    Args:
        task_name: Name of the task (e.g., 'hearsay')
        cache_dir: Optional cache directory for datasets

    Returns:
        DatasetDict with 'train' and 'test' splits

    Raises:
        ValueError: If task_name is not valid
    """
    if task_name not in TASKS:
        cprint(f"❌ Invalid task name: {task_name}", "red")
        cprint(f"   Valid tasks: {len(TASKS)} tasks available", "yellow")
        raise ValueError(f"Task '{task_name}' not found in TASKS list")

    cprint(f"📥 Loading task '{task_name}' from HuggingFace...", "cyan")

    try:
        dataset = datasets.load_dataset("nguha/legalbench", task_name, cache_dir=cache_dir)
        cprint(
            f"✅ Loaded {len(dataset['train'])} train, {len(dataset['test'])} test samples",
            "green",
        )
        return dataset
    except Exception as e:
        cprint(f"❌ Failed to load task '{task_name}': {e}", "red")
        raise


def get_test_df(task_name: str, cache_dir: Optional[str] = None) -> pd.DataFrame:
    """
    Get test split as pandas DataFrame (canonical pattern).

    Args:
        task_name: Name of the task
        cache_dir: Optional cache directory

    Returns:
        DataFrame with test samples
    """
    dataset = load_task_data(task_name, cache_dir)
    df = dataset["test"].to_pandas()
    cprint(f"📊 Test DataFrame: {len(df)} rows, {len(df.columns)} columns", "cyan")
    return df


def get_train_df(task_name: str, cache_dir: Optional[str] = None) -> pd.DataFrame:
    """
    Get train split as pandas DataFrame (for few-shot examples).

    Args:
        task_name: Name of the task
        cache_dir: Optional cache directory

    Returns:
        DataFrame with training samples
    """
    dataset = load_task_data(task_name, cache_dir)
    df = dataset["train"].to_pandas()
    cprint(f"📊 Train DataFrame: {len(df)} rows (few-shot examples)", "cyan")
    return df


def load_prompt_template(task_name: str, variant: str = "base") -> str:
    """
    Load prompt template from local task directory.

    Args:
        task_name: Name of the task
        variant: Template variant ('base', 'claude', 'application', 'rule_description')

    Returns:
        Prompt template string with {{placeholders}}

    Raises:
        FileNotFoundError: If template file doesn't exist
        ValueError: If task_name is invalid
    """
    if task_name not in TASKS:
        cprint(f"❌ Invalid task name: {task_name}", "red")
        raise ValueError(f"Task '{task_name}' not found in TASKS list")

    # Map variant to filename
    variant_map = {
        "base": "base_prompt.txt",
        "claude": "claude_prompt.txt",
        "application": "application_prompt.txt",
        "claude_application": "claude_application_prompt.txt",
        "rule_description": "rule_description_prompt.txt",
        "rule_reference": "rule_reference_prompt.txt",
    }

    if variant not in variant_map:
        cprint(f"⚠️  Unknown variant '{variant}', defaulting to 'base'", "yellow")
        variant = "base"

    template_file = TASK_DIR / task_name / variant_map[variant]

    if not template_file.exists():
        cprint(f"❌ Template file not found: {template_file}", "red")
        raise FileNotFoundError(f"Template '{variant}' not found for task '{task_name}'")

    cprint(f"📄 Loading template: {variant_map[variant]}", "cyan")
    with open(template_file, "r", encoding="utf-8") as f:
        template = f.read()

    # Validate template has placeholders
    if "{{" not in template:
        cprint(f"⚠️  Warning: Template has no {{placeholders}}", "yellow")

    return template


def get_task_category(task_name: str) -> str:
    """
    Determine the category of a task.

    Args:
        task_name: Name of the task

    Returns:
        Category name (ISSUE_TASKS, RULE_TASKS, CONCLUSION_TASKS, etc.)

    Raises:
        ValueError: If task_name is not found in any category
    """
    if task_name not in TASKS:
        cprint(f"❌ Invalid task name: {task_name}", "red")
        raise ValueError(f"Task '{task_name}' not found in TASKS list")

    # Check each category
    category_map = {
        "ISSUE_TASKS": ISSUE_TASKS,
        "RULE_TASKS": RULE_TASKS,
        "CONCLUSION_TASKS": CONCLUSION_TASKS,
        "INTERPRETATION_TASKS": INTERPRETATION_TASKS,
        "RHETORIC_TASKS": RHETORIC_TASKS,
    }

    for category_name, task_list in category_map.items():
        if task_name in task_list:
            cprint(f"📂 Task category: {category_name}", "cyan")
            return category_name

    cprint(f"⚠️  Task '{task_name}' not found in any category", "yellow")
    raise ValueError(f"Task '{task_name}' not categorized")


def get_task_info(task_name: str) -> Dict[str, any]:
    """
    Get comprehensive information about a task.

    Args:
        task_name: Name of the task

    Returns:
        Dictionary with task metadata
    """
    if task_name not in TASKS:
        raise ValueError(f"Task '{task_name}' not found in TASKS list")

    # Get category
    category = get_task_category(task_name)

    # Load datasets to get counts
    dataset = load_task_data(task_name)
    train_count = len(dataset["train"])
    test_count = len(dataset["test"])

    # Check available prompt variants
    task_path = TASK_DIR / task_name
    available_prompts = []
    for variant_file in [
        "base_prompt.txt",
        "claude_prompt.txt",
        "application_prompt.txt",
        "rule_description_prompt.txt",
    ]:
        if (task_path / variant_file).exists():
            available_prompts.append(variant_file.replace("_prompt.txt", ""))

    info = {
        "task_name": task_name,
        "category": category,
        "train_samples": train_count,
        "test_samples": test_count,
        "total_samples": train_count + test_count,
        "available_prompts": available_prompts,
    }

    cprint(f"\n📋 Task Info: {task_name}", "cyan", attrs=["bold"])
    cprint(f"   Category: {category}", "white")
    cprint(f"   Train samples: {train_count}", "white")
    cprint(f"   Test samples: {test_count}", "white")
    cprint(f"   Available prompts: {', '.join(available_prompts)}", "white")

    return info
