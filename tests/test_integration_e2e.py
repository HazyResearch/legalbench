"""
End-to-end integration smoke test.

Tests the complete data pipeline with real LegalBench data (minimal mocking).

NOTE: These tests require the tasks/ directory with local TSV files.
If tasks are not available locally, tests will be skipped.
"""

import pandas as pd
import pytest
from pathlib import Path

from evaluation import evaluate
from utils import generate_prompts


# Check if tasks directory exists
TASKS_DIR = Path("tasks")
TASKS_AVAILABLE = TASKS_DIR.exists() and (TASKS_DIR / "hearsay").exists()

skip_if_no_tasks = pytest.mark.skipif(
    not TASKS_AVAILABLE,
    reason="Tasks directory not available locally (requires task data files)"
)


@skip_if_no_tasks
def test_canonical_workflow_hearsay():
    """
    End-to-end test with real LegalBench data (no mocks).

    Tests the canonical workflow:
    1. Load real task data from tasks/hearsay/
    2. Load real prompt template
    3. Generate prompts using canonical generate_prompts()
    4. Evaluate using canonical evaluate()

    Uses ground truth as "generated" output to verify perfect score.
    """
    task_name = "hearsay"

    # Load real task data from local TSV (2 samples only for speed)
    # Note: Using train.tsv as test.tsv may not be in local clone
    task_path = Path("tasks") / task_name
    test_df = pd.read_csv(task_path / "train.tsv", sep="\t", encoding="utf-8").iloc[:2]
    assert len(test_df) == 2, "Should load exactly 2 test samples"

    # Load real prompt template from local file
    template_path = task_path / "base_prompt.txt"
    template = template_path.read_text(encoding="utf-8")
    assert len(template) > 0, "Prompt template should not be empty"
    assert "{{text}}" in template, "Template should contain {{text}} placeholder"

    # Generate prompts using canonical function
    prompts = generate_prompts(template, test_df)
    assert len(prompts) == 2, "Should generate 2 prompts"
    assert all(isinstance(p, str) for p in prompts), "All prompts should be strings"
    assert all(len(p) > 0 for p in prompts), "All prompts should be non-empty"

    # Use ground truth as mock generations (simulates perfect agent)
    generations = test_df["answer"].tolist()
    answers = test_df["answer"].tolist()

    # Test canonical evaluate function
    score = evaluate(task_name, generations, answers)

    # With perfect match, score should be 1.0
    assert score == 1.0, f"Perfect match should score 1.0, got {score}"


@skip_if_no_tasks
def test_canonical_workflow_contract_qa():
    """
    End-to-end test with contract_qa task (interpretation category).

    Verifies the workflow works across different task types.
    """
    task_name = "contract_qa"

    # Load real task data from local TSV
    task_path = Path("tasks") / task_name
    test_df = pd.read_csv(task_path / "train.tsv", sep="\t", encoding="utf-8").iloc[:2]
    assert len(test_df) == 2

    # Load and verify template from local file
    template = (task_path / "base_prompt.txt").read_text(encoding="utf-8")
    assert "{{text}}" in template

    # Generate prompts
    prompts = generate_prompts(template, test_df)
    assert len(prompts) == 2

    # Perfect match scenario
    generations = test_df["answer"].tolist()
    answers = test_df["answer"].tolist()

    score = evaluate(task_name, generations, answers)
    assert score == 1.0


@skip_if_no_tasks
def test_task_data_integrity():
    """
    Verify task data has required columns and structure.
    """
    task_name = "hearsay"

    # Load data from local TSV
    task_path = Path("tasks") / task_name
    test_df = pd.read_csv(task_path / "train.tsv", sep="\t", encoding="utf-8")

    # Check required columns
    assert "answer" in test_df.columns, "Test data should have 'answer' column"
    assert "text" in test_df.columns, "Test data should have 'text' column"
    assert "index" in test_df.columns, "Test data should have 'index' column"

    # Check data integrity
    assert len(test_df) > 0, "Test data should not be empty"
    assert test_df["answer"].notna().all(), "All answers should be non-null"
    assert test_df["text"].notna().all(), "All texts should be non-null"


@skip_if_no_tasks
def test_prompt_template_placeholders():
    """
    Verify prompt templates contain expected placeholders.
    """
    # Test a few different tasks
    tasks_to_test = ["hearsay", "contract_qa", "learned_hands_torts"]

    for task_name in tasks_to_test:
        task_path = Path("tasks") / task_name
        template = (task_path / "base_prompt.txt").read_text(encoding="utf-8")

        # All templates should have at least {{text}} placeholder
        assert "{{text}}" in template, f"{task_name} template should contain {{{{text}}}}"

        # Template should be non-empty
        assert len(template) > 100, f"{task_name} template seems too short"


@skip_if_no_tasks
def test_evaluate_with_incorrect_predictions():
    """
    Test canonical evaluate() with intentionally wrong predictions.

    Verifies that the evaluation function correctly identifies errors.
    """
    task_name = "hearsay"

    # Load real data from local TSV
    task_path = Path("tasks") / task_name
    test_df = pd.read_csv(task_path / "train.tsv", sep="\t", encoding="utf-8").iloc[:2]
    answers = test_df["answer"].tolist()

    # Create intentionally wrong predictions (flip answers)
    if answers[0] == "Yes":
        wrong_generations = ["No", "No"]
    else:
        wrong_generations = ["Yes", "Yes"]

    # Score should be less than 1.0
    score = evaluate(task_name, wrong_generations, answers)
    assert score < 1.0, "Wrong predictions should score less than 1.0"
    assert score >= 0.0, "Score should be non-negative"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
