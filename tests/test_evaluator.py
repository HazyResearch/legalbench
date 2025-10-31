"""
Phase 3: Evaluator Tests

Tests for LegalBenchEvaluator class using mock agent responses.

Test Strategy:
- Mock agent execution (no real Maite agent required)
- Test evaluate_task() and evaluate_multiple()
- Verify canonical workflow integration
- Test error handling and aggregation
"""

import pandas as pd
import pytest
from termcolor import cprint
from unittest.mock import Mock, patch, MagicMock

# eval_maite modules
from eval_maite.evaluator import LegalBenchEvaluator
from eval_maite.models import AgentConfig, TaskTrace
from eval_maite.utils import get_metric_name


# Mock data fixtures
@pytest.fixture
def mock_test_df():
    """Create mock test DataFrame."""
    return pd.DataFrame({
        "text": [
            "Direct eyewitness testimony.",
            "Testimony about what someone else said.",
            "Written statement from absent person."
        ],
        "answer": ["No", "Yes", "Yes"]
    })


@pytest.fixture
def mock_task_loading(mock_test_df):
    """Mock task loading functions to avoid HuggingFace dependency."""
    with patch("eval_maite.evaluator.get_test_df") as mock_get_test:
        with patch("eval_maite.evaluator.load_prompt_template") as mock_load_template:
            with patch("eval_maite.evaluator.get_task_category") as mock_category:
                # Setup return values
                mock_get_test.return_value = mock_test_df
                mock_load_template.return_value = "Q: {{text}}\nA:"
                mock_category.return_value = "CONCLUSION_TASKS"

                yield {
                    "get_test_df": mock_get_test,
                    "load_prompt_template": mock_load_template,
                    "get_task_category": mock_category
                }


class MockAgentWrapper:
    """Mock agent wrapper for testing."""

    def __init__(self, response_mode="perfect"):
        """
        Initialize mock agent.

        Args:
            response_mode: "perfect" | "zero" | "error" | "partial"
        """
        self.response_mode = response_mode
        self.call_count = 0

    def execute(self, prompt: str, expected_output: str, sample_id: str) -> TaskTrace:
        """Mock execute method."""
        self.call_count += 1

        if self.response_mode == "perfect":
            # Return expected output
            return TaskTrace(
                sample_id=sample_id,
                input_text=prompt,
                expected_output=expected_output,
                actual_output=expected_output,  # Perfect match
                is_correct=True,
                execution_time=1.0,
                tokens={"input": 100, "output": 10, "total": 110},
                tool_calls=[],
                chain_steps=[],
                error=None,
            )
        elif self.response_mode == "zero":
            # Return wrong output
            wrong = "No" if expected_output == "Yes" else "Yes"
            return TaskTrace(
                sample_id=sample_id,
                input_text=prompt,
                expected_output=expected_output,
                actual_output=wrong,  # Wrong answer
                is_correct=False,
                execution_time=1.0,
                tokens={"input": 100, "output": 10, "total": 110},
                tool_calls=[],
                chain_steps=[],
                error=None,
            )
        elif self.response_mode == "error":
            # Return error trace
            return TaskTrace(
                sample_id=sample_id,
                input_text=prompt,
                expected_output=expected_output,
                actual_output="",  # Empty on error
                is_correct=False,
                execution_time=0.0,
                tokens=None,
                tool_calls=[],
                chain_steps=[],
                error="Mock error",
            )
        elif self.response_mode == "partial":
            # Return correct for even indices, wrong for odd
            is_correct = self.call_count % 2 == 1
            actual = expected_output if is_correct else (
                "No" if expected_output == "Yes" else "Yes"
            )
            return TaskTrace(
                sample_id=sample_id,
                input_text=prompt,
                expected_output=expected_output,
                actual_output=actual,
                is_correct=is_correct,
                execution_time=1.0,
                tokens={"input": 100, "output": 10, "total": 110},
                tool_calls=[],
                chain_steps=[],
                error=None,
            )


def test_evaluator_initialization():
    """Test evaluator can be initialized with mock agent."""
    cprint("\n✓ Testing evaluator initialization...", "cyan")

    mock_agent = MockAgentWrapper()
    evaluator = LegalBenchEvaluator(mock_agent)

    assert evaluator.agent_wrapper is mock_agent
    cprint("   ✓ Evaluator initialized successfully", "green")


def test_get_metric_name():
    """Test metric name determination for various tasks."""
    cprint("\n✓ Testing metric name determination...", "cyan")

    # Test known tasks
    assert get_metric_name("hearsay") == "balanced_accuracy"
    assert get_metric_name("sara_numeric") == "numeric_tolerance"
    assert get_metric_name("successor_liability") == "f1_score"
    assert get_metric_name("citation_prediction_open") == "contains_match"
    assert get_metric_name("definition_extraction") == "balanced_accuracy_stemmed"
    assert get_metric_name("ssla_plaintiff") == "f1_score"
    assert get_metric_name("rule_qa") == "manual_evaluation"

    # Test unknown task (should default to balanced_accuracy)
    assert get_metric_name("unknown_task") == "balanced_accuracy"

    cprint("   ✓ Metric names determined correctly", "green")


def test_evaluate_task_perfect_accuracy(mock_task_loading):
    """Test evaluate_task with perfect accuracy mock."""
    cprint("\n✓ Testing evaluate_task (perfect accuracy)...", "cyan")

    mock_agent = MockAgentWrapper(response_mode="perfect")
    evaluator = LegalBenchEvaluator(mock_agent)

    # Evaluate with small sample size
    result = evaluator.evaluate_task("hearsay", sample_size=3)

    # Verify result
    assert result.task_name == "hearsay"
    assert result.category == "CONCLUSION_TASKS"
    assert result.samples_evaluated == 3
    assert result.metric == "balanced_accuracy"
    assert result.score == 1.0  # Perfect accuracy
    assert result.avg_execution_time > 0
    assert result.avg_tokens > 0
    assert result.errors == 0

    cprint(f"   ✓ Perfect accuracy result: {result.score:.4f}", "green")


def test_evaluate_task_zero_accuracy(mock_task_loading):
    """Test evaluate_task with zero accuracy mock."""
    cprint("\n✓ Testing evaluate_task (zero accuracy)...", "cyan")

    mock_agent = MockAgentWrapper(response_mode="zero")
    evaluator = LegalBenchEvaluator(mock_agent)

    # Evaluate with small sample size
    result = evaluator.evaluate_task("hearsay", sample_size=3)

    # Verify result
    assert result.task_name == "hearsay"
    assert result.samples_evaluated == 3
    assert result.score == 0.0  # Zero accuracy
    assert result.errors == 0  # No errors, just wrong answers

    cprint(f"   ✓ Zero accuracy result: {result.score:.4f}", "green")


def test_evaluate_task_with_errors(mock_task_loading):
    """Test evaluate_task with error traces."""
    cprint("\n✓ Testing evaluate_task (with errors)...", "cyan")

    mock_agent = MockAgentWrapper(response_mode="error")
    evaluator = LegalBenchEvaluator(mock_agent)

    # Evaluate with small sample size
    result = evaluator.evaluate_task("hearsay", sample_size=3)

    # Verify result
    assert result.task_name == "hearsay"
    assert result.samples_evaluated == 3
    assert result.score == 0.0  # All errors = zero score
    assert result.errors == 3  # All samples errored
    assert result.avg_tokens is None  # No tokens on error

    cprint(f"   ✓ Error handling result: {result.errors} errors", "green")


def test_evaluate_task_sample_size(mock_task_loading):
    """Test evaluate_task respects sample_size parameter."""
    cprint("\n✓ Testing sample size limiting...", "cyan")

    mock_agent = MockAgentWrapper(response_mode="perfect")
    evaluator = LegalBenchEvaluator(mock_agent)

    # Test with sample_size=3 (matches our mock data)
    result = evaluator.evaluate_task("hearsay", sample_size=3)

    assert result.samples_evaluated == 3
    assert mock_agent.call_count == 3

    cprint(f"   ✓ Sample size respected: {result.samples_evaluated} samples", "green")


def test_evaluate_task_include_traces(mock_task_loading):
    """Test evaluate_task with include_traces=True."""
    cprint("\n✓ Testing trace inclusion...", "cyan")

    mock_agent = MockAgentWrapper(response_mode="perfect")
    evaluator = LegalBenchEvaluator(mock_agent)

    # With traces
    result_with_traces = evaluator.evaluate_task("hearsay", sample_size=3, include_traces=True)
    assert result_with_traces.traces is not None
    assert len(result_with_traces.traces) == 3
    cprint(f"   ✓ Traces included: {len(result_with_traces.traces)} traces", "green")

    # Without traces
    mock_agent2 = MockAgentWrapper(response_mode="perfect")
    evaluator2 = LegalBenchEvaluator(mock_agent2)
    result_without_traces = evaluator2.evaluate_task("hearsay", sample_size=3, include_traces=False)
    assert result_without_traces.traces is None
    cprint(f"   ✓ Traces excluded when requested", "green")


def test_evaluate_multiple_tasks(mock_task_loading):
    """Test evaluate_multiple with multiple tasks."""
    cprint("\n✓ Testing evaluate_multiple...", "cyan")

    mock_agent = MockAgentWrapper(response_mode="perfect")
    evaluator = LegalBenchEvaluator(mock_agent)

    # Evaluate multiple tasks
    task_names = ["hearsay", "contract_qa"]
    results = evaluator.evaluate_multiple(task_names, sample_size=3)

    # Verify results
    assert len(results) == 2
    assert results[0].task_name == "hearsay"
    assert results[1].task_name == "contract_qa"
    assert all(r.samples_evaluated == 3 for r in results)
    assert all(r.score == 1.0 for r in results)  # Perfect accuracy

    cprint(f"   ✓ Multiple tasks evaluated: {len(results)} tasks", "green")


def test_evaluate_multiple_with_failure(mock_task_loading):
    """Test evaluate_multiple continues when one task fails."""
    cprint("\n✓ Testing evaluate_multiple with failures...", "cyan")

    # Mock that will fail for invalid_task_xyz
    with patch("eval_maite.evaluator.get_test_df") as mock_get_test:
        def side_effect(task_name):
            if task_name == "invalid_task_xyz":
                raise ValueError("Invalid task")
            return mock_task_loading["get_test_df"].return_value

        mock_get_test.side_effect = side_effect

        mock_agent = MockAgentWrapper(response_mode="perfect")
        evaluator = LegalBenchEvaluator(mock_agent)

        # Use invalid task name to trigger failure
        task_names = ["hearsay", "invalid_task_xyz", "contract_qa"]

        # Should continue despite invalid task
        results = evaluator.evaluate_multiple(task_names, sample_size=2)

    # Should have 2 results (hearsay and contract_qa), invalid_task_xyz fails
    assert len(results) == 2
    assert results[0].task_name == "hearsay"
    assert results[1].task_name == "contract_qa"

    cprint(f"   ✓ Handled failure gracefully: {len(results)}/3 tasks succeeded", "green")


def test_build_task_result():
    """Test _build_task_result aggregation."""
    cprint("\n✓ Testing task result aggregation...", "cyan")

    # Create mock traces
    traces = [
        TaskTrace(
            sample_id="test_0",
            input_text="Prompt 1",
            expected_output="Yes",
            actual_output="Yes",
            is_correct=True,
            execution_time=1.5,
            tokens={"input": 100, "output": 10, "total": 110},
            tool_calls=[],
            chain_steps=[],
            error=None,
        ),
        TaskTrace(
            sample_id="test_1",
            input_text="Prompt 2",
            expected_output="No",
            actual_output="No",
            is_correct=True,
            execution_time=2.5,
            tokens={"input": 120, "output": 15, "total": 135},
            tool_calls=[],
            chain_steps=[],
            error=None,
        ),
        TaskTrace(
            sample_id="test_2",
            input_text="Prompt 3",
            expected_output="Yes",
            actual_output="",
            is_correct=False,
            execution_time=0.0,
            tokens=None,  # No tokens on error
            tool_calls=[],
            chain_steps=[],
            error="Mock error",
        ),
    ]

    mock_agent = MockAgentWrapper()
    evaluator = LegalBenchEvaluator(mock_agent)

    result = evaluator._build_task_result(
        task_name="hearsay",
        category="CONCLUSION_TASKS",
        traces=traces,
        score=0.667,
        metric_name="balanced_accuracy",
        include_traces=False,
    )

    # Verify aggregation
    assert result.samples_evaluated == 3
    assert result.errors == 1
    assert result.avg_execution_time == (1.5 + 2.5 + 0.0) / 3
    assert result.avg_tokens == (110 + 135) / 2  # Only 2 traces have tokens
    assert result.traces is None  # include_traces=False

    cprint("   ✓ Task result aggregated correctly", "green")


if __name__ == "__main__":
    """Run tests directly with pytest."""
    cprint("\n" + "=" * 80, "cyan", attrs=["bold"])
    cprint("Phase 3: Evaluator Tests", "cyan", attrs=["bold"])
    cprint("=" * 80 + "\n", "cyan", attrs=["bold"])

    pytest.main([__file__, "-v", "-s"])
