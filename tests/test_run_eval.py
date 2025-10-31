"""
Phase 4: CLI Interface Tests

Tests for run_eval.py CLI script.

Test Strategy:
- Test argument parsing with various combinations
- Test task selection logic (--tasks, --category, --quick)
- Test validation for invalid task names
- Mock-based integration tests
- Verify JSON output creation
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest
from termcolor import cprint

# Add scripts to path for import
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import run_eval


def test_parse_arguments_tasks():
    """Test argument parsing with --tasks."""
    cprint("\n✓ Testing argument parsing with --tasks...", "cyan")

    with patch("sys.argv", ["run_eval.py", "--tasks", "hearsay,contract_qa"]):
        args = run_eval.parse_arguments()

        assert args.tasks == "hearsay,contract_qa"
        assert args.category is None
        assert args.quick is False
        assert args.samples == 20  # Default
        assert args.model == "claude-sonnet-4"  # Default

    cprint("   ✓ --tasks argument parsed correctly", "green")


def test_parse_arguments_category():
    """Test argument parsing with --category."""
    cprint("\n✓ Testing argument parsing with --category...", "cyan")

    with patch("sys.argv", ["run_eval.py", "--category", "CONCLUSION_TASKS", "--samples", "10"]):
        args = run_eval.parse_arguments()

        assert args.category == "CONCLUSION_TASKS"
        assert args.tasks is None
        assert args.quick is False
        assert args.samples == 10

    cprint("   ✓ --category argument parsed correctly", "green")


def test_parse_arguments_quick():
    """Test argument parsing with --quick."""
    cprint("\n✓ Testing argument parsing with --quick...", "cyan")

    with patch("sys.argv", ["run_eval.py", "--quick"]):
        args = run_eval.parse_arguments()

        assert args.quick is True
        assert args.tasks is None
        assert args.category is None

    cprint("   ✓ --quick argument parsed correctly", "green")


def test_parse_arguments_custom_output():
    """Test argument parsing with --output."""
    cprint("\n✓ Testing argument parsing with --output...", "cyan")

    with patch("sys.argv", ["run_eval.py", "--tasks", "hearsay", "--output", "custom.json"]):
        args = run_eval.parse_arguments()

        assert args.output == "custom.json"

    cprint("   ✓ --output argument parsed correctly", "green")


def test_parse_arguments_agent_config():
    """Test argument parsing with agent configuration."""
    cprint("\n✓ Testing argument parsing with agent config...", "cyan")

    with patch(
        "sys.argv",
        [
            "run_eval.py",
            "--tasks",
            "hearsay",
            "--model",
            "claude-opus-4",
            "--temperature",
            "0.5",
            "--timeout",
            "120",
        ],
    ):
        args = run_eval.parse_arguments()

        assert args.model == "claude-opus-4"
        assert args.temperature == 0.5
        assert args.timeout == 120

    cprint("   ✓ Agent configuration arguments parsed correctly", "green")


def test_get_task_list_from_tasks():
    """Test get_task_list with --tasks argument."""
    cprint("\n✓ Testing get_task_list from --tasks...", "cyan")

    # Create mock args
    args = MagicMock()
    args.tasks = "hearsay, contract_qa, personal_jurisdiction"
    args.category = None
    args.quick = False

    tasks = run_eval.get_task_list(args)

    assert tasks == ["hearsay", "contract_qa", "personal_jurisdiction"]
    cprint(f"   ✓ Extracted {len(tasks)} tasks from comma-separated string", "green")


def test_get_task_list_from_category():
    """Test get_task_list with --category argument."""
    cprint("\n✓ Testing get_task_list from --category...", "cyan")

    args = MagicMock()
    args.tasks = None
    args.category = "CONCLUSION_TASKS"
    args.quick = False

    tasks = run_eval.get_task_list(args)

    # Should return all conclusion tasks
    assert len(tasks) > 0
    assert isinstance(tasks, list)
    cprint(f"   ✓ Extracted {len(tasks)} tasks from CONCLUSION_TASKS category", "green")


def test_get_task_list_from_quick():
    """Test get_task_list with --quick argument."""
    cprint("\n✓ Testing get_task_list from --quick...", "cyan")

    args = MagicMock()
    args.tasks = None
    args.category = None
    args.quick = True

    tasks = run_eval.get_task_list(args)

    # Should return 5 quick test tasks
    assert len(tasks) == 5
    assert tasks == run_eval.QUICK_TEST_TASKS
    cprint(f"   ✓ Extracted {len(tasks)} quick test tasks", "green")


def test_validate_tasks_valid():
    """Test validate_tasks with valid task names."""
    cprint("\n✓ Testing validate_tasks with valid tasks...", "cyan")

    valid_tasks = ["hearsay", "contract_qa", "personal_jurisdiction"]

    # Should not raise
    try:
        run_eval.validate_tasks(valid_tasks)
        cprint("   ✓ Valid tasks passed validation", "green")
    except ValueError:
        pytest.fail("validate_tasks raised ValueError for valid tasks")


def test_validate_tasks_invalid():
    """Test validate_tasks with invalid task names."""
    cprint("\n✓ Testing validate_tasks with invalid tasks...", "cyan")

    invalid_tasks = ["hearsay", "fake_task_123", "another_fake_task"]

    with pytest.raises(ValueError) as excinfo:
        run_eval.validate_tasks(invalid_tasks)

    assert "Invalid task names" in str(excinfo.value)
    assert "fake_task_123" in str(excinfo.value)
    cprint("   ✓ Invalid tasks correctly rejected", "green")


def test_validate_tasks_all_invalid():
    """Test validate_tasks with all invalid task names."""
    cprint("\n✓ Testing validate_tasks with all invalid tasks...", "cyan")

    all_invalid = ["fake1", "fake2", "fake3"]

    with pytest.raises(ValueError) as excinfo:
        run_eval.validate_tasks(all_invalid)

    error_msg = str(excinfo.value)
    assert "fake1" in error_msg
    assert "fake2" in error_msg
    assert "fake3" in error_msg
    cprint("   ✓ All invalid tasks correctly rejected", "green")


def test_print_summary_basic():
    """Test print_summary with mock EvaluationRun."""
    cprint("\n✓ Testing print_summary...", "cyan")

    # Import models
    from eval_maite.models import AgentConfig, EvaluationRun, TaskResult

    # Create mock evaluation run
    config = AgentConfig(name="test_agent", model="claude-sonnet-4")

    run = EvaluationRun(
        run_id="test_run_001",
        agent_config=config,
        tasks=["hearsay", "contract_qa"],
        samples_per_task=10,
        results=[],
    )

    # Add mock results
    result1 = TaskResult(
        task_name="hearsay",
        category="CONCLUSION_TASKS",
        samples_evaluated=10,
        metric="balanced_accuracy",
        score=0.85,
        avg_execution_time=2.0,
        avg_tokens=150.0,
    )

    result2 = TaskResult(
        task_name="contract_qa",
        category="INTERPRETATION_TASKS",
        samples_evaluated=10,
        metric="balanced_accuracy",
        score=0.75,
        avg_execution_time=1.5,
        avg_tokens=120.0,
    )

    run.add_result(result1)
    run.add_result(result2)

    # Should not raise
    try:
        run_eval.print_summary(run)
        cprint("   ✓ Summary printed successfully", "green")
    except Exception as e:
        pytest.fail(f"print_summary raised exception: {e}")


@patch("run_eval.LegalBenchEvaluator")
@patch("run_eval.MaiteAgentWrapper")
@patch("run_eval.save_results")
def test_main_basic_execution(mock_save, mock_agent, mock_evaluator):
    """Test main() with mocked dependencies."""
    cprint("\n✓ Testing main() with mocked dependencies...", "cyan")

    # Import models
    from eval_maite.models import AgentConfig, TaskResult

    # Setup mocks
    mock_agent_instance = Mock()
    mock_agent.return_value = mock_agent_instance

    mock_evaluator_instance = Mock()
    mock_evaluator.return_value = mock_evaluator_instance

    # Mock evaluate_multiple to return results
    mock_result = TaskResult(
        task_name="hearsay",
        category="CONCLUSION_TASKS",
        samples_evaluated=5,
        metric="balanced_accuracy",
        score=0.85,
        avg_execution_time=2.0,
        avg_tokens=150.0,
    )
    mock_evaluator_instance.evaluate_multiple.return_value = [mock_result]

    # Mock save_results to return a path
    mock_save.return_value = Path("results/test_run.json")

    # Run main with mocked argv
    with patch("sys.argv", ["run_eval.py", "--tasks", "hearsay", "--samples", "5"]):
        exit_code = run_eval.main()

    # Verify success
    assert exit_code == 0
    cprint("   ✓ main() executed successfully with exit code 0", "green")

    # Verify agent was initialized
    mock_agent.assert_called_once()
    cprint("   ✓ Agent wrapper initialized", "green")

    # Verify evaluator was initialized
    mock_evaluator.assert_called_once()
    cprint("   ✓ Evaluator initialized", "green")

    # Verify evaluate_multiple was called
    mock_evaluator_instance.evaluate_multiple.assert_called_once()
    cprint("   ✓ evaluate_multiple called", "green")

    # Verify results were saved
    mock_save.assert_called_once()
    cprint("   ✓ Results saved", "green")


@patch("run_eval.LegalBenchEvaluator")
@patch("run_eval.MaiteAgentWrapper")
def test_main_handles_invalid_tasks(mock_agent, mock_evaluator):
    """Test main() handles invalid task names gracefully."""
    cprint("\n✓ Testing main() with invalid tasks...", "cyan")

    # Run main with invalid task
    with patch("sys.argv", ["run_eval.py", "--tasks", "fake_task_does_not_exist"]):
        exit_code = run_eval.main()

    # Should fail with exit code 1
    assert exit_code == 1
    cprint("   ✓ main() returned exit code 1 for invalid tasks", "green")

    # Evaluator should not be called
    mock_evaluator.assert_not_called()
    cprint("   ✓ Evaluator was not called (validation failed early)", "green")


@patch("run_eval.LegalBenchEvaluator")
@patch("run_eval.MaiteAgentWrapper")
def test_main_handles_keyboard_interrupt(mock_agent, mock_evaluator):
    """Test main() handles KeyboardInterrupt gracefully."""
    cprint("\n✓ Testing main() with KeyboardInterrupt...", "cyan")

    # Setup evaluator to raise KeyboardInterrupt
    mock_evaluator_instance = Mock()
    mock_evaluator.return_value = mock_evaluator_instance
    mock_evaluator_instance.evaluate_multiple.side_effect = KeyboardInterrupt()

    # Run main
    with patch("sys.argv", ["run_eval.py", "--tasks", "hearsay", "--samples", "5"]):
        exit_code = run_eval.main()

    # Should fail with exit code 1
    assert exit_code == 1
    cprint("   ✓ main() returned exit code 1 for KeyboardInterrupt", "green")


@patch("run_eval.LegalBenchEvaluator")
@patch("run_eval.MaiteAgentWrapper")
@patch("run_eval.save_results")
def test_main_category_selection(mock_save, mock_agent, mock_evaluator):
    """Test main() with --category argument."""
    cprint("\n✓ Testing main() with --category...", "cyan")

    # Import models
    from eval_maite.models import TaskResult

    # Setup mocks
    mock_agent_instance = Mock()
    mock_agent.return_value = mock_agent_instance

    mock_evaluator_instance = Mock()
    mock_evaluator.return_value = mock_evaluator_instance

    # Mock results
    mock_result = TaskResult(
        task_name="hearsay",
        category="CONCLUSION_TASKS",
        samples_evaluated=5,
        metric="balanced_accuracy",
        score=0.85,
        avg_execution_time=2.0,
        avg_tokens=150.0,
    )
    mock_evaluator_instance.evaluate_multiple.return_value = [mock_result]
    mock_save.return_value = Path("results/test_run.json")

    # Run with category
    with patch("sys.argv", ["run_eval.py", "--category", "CONCLUSION_TASKS", "--samples", "3"]):
        exit_code = run_eval.main()

    # Verify success
    assert exit_code == 0
    cprint("   ✓ main() executed successfully with --category", "green")

    # Verify evaluate_multiple was called with task list
    call_args = mock_evaluator_instance.evaluate_multiple.call_args
    task_names = call_args.kwargs["task_names"]
    assert len(task_names) > 0  # Should have tasks from category
    cprint(f"   ✓ evaluate_multiple called with {len(task_names)} tasks from category", "green")


@patch("run_eval.LegalBenchEvaluator")
@patch("run_eval.MaiteAgentWrapper")
@patch("run_eval.save_results")
def test_main_quick_mode(mock_save, mock_agent, mock_evaluator):
    """Test main() with --quick argument."""
    cprint("\n✓ Testing main() with --quick...", "cyan")

    # Import models
    from eval_maite.models import TaskResult

    # Setup mocks
    mock_agent_instance = Mock()
    mock_agent.return_value = mock_agent_instance

    mock_evaluator_instance = Mock()
    mock_evaluator.return_value = mock_evaluator_instance

    # Mock results
    mock_results = [
        TaskResult(
            task_name=task,
            category="TEST",
            samples_evaluated=5,
            metric="balanced_accuracy",
            score=0.85,
            avg_execution_time=2.0,
            avg_tokens=150.0,
        )
        for task in run_eval.QUICK_TEST_TASKS
    ]
    mock_evaluator_instance.evaluate_multiple.return_value = mock_results
    mock_save.return_value = Path("results/test_run.json")

    # Run quick mode
    with patch("sys.argv", ["run_eval.py", "--quick"]):
        exit_code = run_eval.main()

    # Verify success
    assert exit_code == 0
    cprint("   ✓ main() executed successfully with --quick", "green")

    # Verify evaluate_multiple was called with 5 tasks
    call_args = mock_evaluator_instance.evaluate_multiple.call_args
    task_names = call_args.kwargs["task_names"]
    assert len(task_names) == 5
    assert task_names == run_eval.QUICK_TEST_TASKS
    cprint(f"   ✓ evaluate_multiple called with {len(task_names)} quick test tasks", "green")

    # Verify sample size is 5
    sample_size = call_args.kwargs["sample_size"]
    assert sample_size == 5
    cprint("   ✓ Quick mode uses 5 samples per task", "green")


if __name__ == "__main__":
    """Run tests directly with pytest."""
    cprint("\n" + "=" * 80, "cyan", attrs=["bold"])
    cprint("Phase 4: CLI Interface Tests", "cyan", attrs=["bold"])
    cprint("=" * 80 + "\n", "cyan", attrs=["bold"])

    pytest.main([__file__, "-v", "-s"])
