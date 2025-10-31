"""
Phase 2B: Integration Validation Tests

Validates that eval_maite components work correctly with canonical LegalBench functions.

Test Strategy:
- Use mock data (no HuggingFace dependency for Phase 2B)
- Test canonical workflow: generate_prompts → evaluate
- Verify all imports work
- Simple smoke tests to validate integration
"""

import pandas as pd
import pytest
from termcolor import cprint

# Canonical LegalBench functions (from root modules)
from evaluation import evaluate
from tasks import TASKS
from utils import generate_prompts

# eval_maite modules
from eval_maite.models import AgentConfig, EvaluationRun, TaskResult, TaskTrace


def test_task_exists():
    """Verify hearsay task exists in TASKS list."""
    cprint(f"\n✓ Testing task existence...", "cyan")
    assert "hearsay" in TASKS, "Task 'hearsay' not found in TASKS list"
    cprint(f"   ✓ Task 'hearsay' found in TASKS ({len(TASKS)} total tasks)", "green")


def test_imports_work():
    """
    Verify all critical imports work without errors.

    Tests:
    - Canonical functions from root modules
    - eval_maite modules
    - No circular import errors
    """
    cprint(f"\n✓ Testing imports...", "cyan")

    # Test canonical function imports
    try:
        from evaluation import evaluate
        from utils import generate_prompts
        from tasks import TASKS, ISSUE_TASKS, RULE_TASKS
        cprint(f"   ✓ Canonical functions imported", "green")
    except ImportError as e:
        pytest.fail(f"Failed to import canonical functions: {e}")

    # Test eval_maite module imports
    try:
        from eval_maite.task_loader import (
            get_task_category,
            load_prompt_template,
        )
        from eval_maite.models import AgentConfig, EvaluationRun, TaskResult, TaskTrace
        from eval_maite.agent_wrapper import MaiteAgentWrapper
        from eval_maite.agent_config import discover_workbench_path, get_eval_config
        from eval_maite.agent_utils import (
            build_error_trace,
            check_correctness,
            retry_with_backoff,
        )
        cprint(f"   ✓ eval_maite modules imported", "green")
    except ImportError as e:
        pytest.fail(f"Failed to import eval_maite modules: {e}")

    # Test pandas and datasets
    try:
        import pandas as pd
        import datasets
        cprint(f"   ✓ External dependencies imported", "green")
    except ImportError as e:
        pytest.fail(f"Failed to import external dependencies: {e}")


def test_generate_prompts_integration():
    """
    Test canonical generate_prompts function with mock data.

    Validates:
    - DataFrame → prompts generation
    - {{placeholder}} substitution works
    - List lengths match
    """
    cprint(f"\n✓ Testing generate_prompts integration...", "cyan")

    # Create mock DataFrame
    mock_df = pd.DataFrame({
        "text": [
            "The witness saw the crime happen.",
            "The witness heard about the crime from someone else.",
            "The witness read about the crime in a newspaper.",
        ],
        "answer": ["No", "Yes", "Yes"],
    })

    # Create simple template
    template = "Q: {{text}}\nA:"

    # Generate prompts using canonical function
    prompts = generate_prompts(prompt_template=template, data_df=mock_df)

    # Verify results
    assert len(prompts) == len(mock_df), f"Expected {len(mock_df)} prompts, got {len(prompts)}"
    assert all("Q:" in p for p in prompts), "Prompts missing expected format"
    cprint(f"   ✓ Generated {len(prompts)} prompts successfully", "green")
    cprint(f"   ✓ Sample prompt: {prompts[0][:50]}...", "white")


def test_evaluate_integration():
    """
    Test canonical evaluate function with mock data.

    Validates:
    - evaluate() computes scores correctly
    - Perfect/zero/partial accuracy works
    """
    cprint(f"\n✓ Testing evaluate integration...", "cyan")

    task_name = "hearsay"
    ground_truth = ["Yes", "No", "Yes", "No", "Yes"]

    # Test perfect accuracy
    perfect_generations = ["Yes", "No", "Yes", "No", "Yes"]
    perfect_score = evaluate(task_name, perfect_generations, ground_truth)
    assert perfect_score == 1.0, f"Expected perfect score 1.0, got {perfect_score}"
    cprint(f"   ✓ Perfect accuracy: {perfect_score}", "green")

    # Test zero accuracy
    zero_generations = ["No", "Yes", "No", "Yes", "No"]
    zero_score = evaluate(task_name, zero_generations, ground_truth)
    assert zero_score == 0.0, f"Expected zero score 0.0, got {zero_score}"
    cprint(f"   ✓ Zero accuracy: {zero_score}", "green")

    # Test partial accuracy
    partial_generations = ["Yes", "No", "No", "Yes", "Yes"]  # 2/5 correct
    partial_score = evaluate(task_name, partial_generations, ground_truth)
    assert 0.0 < partial_score < 1.0, f"Expected intermediate score, got {partial_score}"
    cprint(f"   ✓ Partial accuracy: {partial_score}", "green")


def test_canonical_workflow_end_to_end():
    """
    Test complete canonical workflow with mock data.

    Workflow:
    1. Create mock DataFrame (simulating loaded task)
    2. Generate prompts (using canonical generate_prompts)
    3. Mock agent responses
    4. Evaluate (using canonical evaluate)
    5. Verify scores match expectations
    """
    cprint(f"\n✓ Testing canonical workflow end-to-end...", "cyan")

    # Step 1: Create mock task data
    mock_df = pd.DataFrame({
        "text": [
            "Direct eyewitness testimony about what was seen.",
            "Testimony about what someone else said.",
            "A written statement from someone not present.",
        ],
        "answer": ["No", "Yes", "Yes"],
    })
    cprint(f"   Step 1: Created mock DataFrame ({len(mock_df)} samples)", "white")

    # Step 2: Generate prompts
    template = "Q: Is this hearsay? {{text}}\nA:"
    prompts = generate_prompts(prompt_template=template, data_df=mock_df)
    assert len(prompts) == len(mock_df), "Prompt count mismatch"
    cprint(f"   Step 2: Generated {len(prompts)} prompts", "white")

    # Step 3: Mock agent responses (perfect accuracy)
    mock_generations = mock_df["answer"].tolist()
    cprint(f"   Step 3: Mocked agent responses: {mock_generations}", "white")

    # Step 4: Evaluate
    ground_truth = mock_df["answer"].tolist()
    score = evaluate("hearsay", mock_generations, ground_truth)
    cprint(f"   Step 4: Evaluated score: {score}", "white")

    # Step 5: Verify
    assert score == 1.0, f"Expected perfect score with matching answers, got {score}"
    cprint(f"   ✓ Canonical workflow validated (score: {score})", "green")


def test_model_validation():
    """Test that Pydantic models validate correctly."""
    cprint(f"\n✓ Testing Pydantic model validation...", "cyan")

    # Test AgentConfig
    config = AgentConfig(
        name="test_agent",
        timeout=30,
        max_retries=3,
    )
    assert config.name == "test_agent"
    assert config.timeout == 30
    cprint(f"   ✓ AgentConfig validates", "green")

    # Test TaskTrace
    trace = TaskTrace(
        sample_id="test_001",
        input_text="Test prompt",
        expected_output="Yes",
        actual_output="Yes",
        is_correct=True,
        execution_time=1.5,
        tokens={"input": 10, "output": 5, "total": 15},
    )
    assert trace.is_correct is True
    assert trace.execution_time == 1.5
    cprint(f"   ✓ TaskTrace validates", "green")

    # Test TaskResult
    result = TaskResult(
        task_name="hearsay",
        category="CONCLUSION_TASKS",
        samples_evaluated=20,
        metric="balanced_accuracy",
        score=0.85,
        avg_execution_time=2.3,
        avg_tokens=150.0,
    )
    assert result.score == 0.85
    assert result.samples_evaluated == 20
    assert result.category == "CONCLUSION_TASKS"
    cprint(f"   ✓ TaskResult validates", "green")

    # Test EvaluationRun
    run = EvaluationRun(
        run_id="test_run_001",
        agent_config=config,
        tasks=["hearsay"],
        samples_per_task=20,
        results=[result],
    )
    assert run.run_id == "test_run_001"
    assert len(run.results) == 1
    assert len(run.tasks) == 1
    assert run.samples_per_task == 20
    cprint(f"   ✓ EvaluationRun validates", "green")


def test_dataframe_format_requirements():
    """
    Verify DataFrame format requirements for canonical workflow.

    Requirements:
    - Must have 'answer' column for ground truth
    - Prompts list must match DataFrame length
    """
    cprint(f"\n✓ Testing DataFrame format requirements...", "cyan")

    # Valid DataFrame
    valid_df = pd.DataFrame({"text": ["Sample"], "answer": ["Yes"]})
    assert "answer" in valid_df.columns, "Missing 'answer' column"
    cprint(f"   ✓ Valid DataFrame has 'answer' column", "green")

    # Test prompt generation length matching
    template = "Q: {{text}}\nA:"
    prompts = generate_prompts(template, valid_df)
    assert len(prompts) == len(valid_df), "Prompt/DataFrame length mismatch"
    cprint(f"   ✓ Prompts list length matches DataFrame", "green")

    # Test evaluation length matching
    answers = valid_df["answer"].tolist()
    generations = ["Yes"]  # Same length as answers
    score = evaluate("hearsay", generations, answers)
    assert isinstance(score, float), "Score should be float"
    assert 0.0 <= score <= 1.0, "Score should be between 0 and 1"
    cprint(f"   ✓ Evaluation accepts matching-length lists", "green")


if __name__ == "__main__":
    """Run tests directly with pytest."""
    cprint("\n" + "=" * 80, "cyan", attrs=["bold"])
    cprint("Phase 2B: Integration Validation Tests (Mock-Based)", "cyan", attrs=["bold"])
    cprint("=" * 80 + "\n", "cyan", attrs=["bold"])

    pytest.main([__file__, "-v", "-s"])
