"""
Tests for compare_runs.py script.

Tests all core functionality: argument parsing, comparison logic, delta calculation,
output formatting, and JSON export.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock

from scripts.compare_runs import (
    calculate_delta,
    format_delta_string,
    build_task_comparison_map,
    detect_configuration_differences,
    load_runs,
    parse_arguments,
)
from eval_maite.models import AgentConfig, EvaluationRun, TaskResult


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def sample_config1():
    """Sample agent configuration 1."""
    return AgentConfig(
        name="maite",
        version="0.1.0",
        model="claude-sonnet-4",
        temperature=0.0,
        tools=[],
        timeout=60,
        max_retries=3,
    )


@pytest.fixture
def sample_config2():
    """Sample agent configuration 2 (different settings)."""
    return AgentConfig(
        name="maite",
        version="0.1.0",
        model="claude-opus-4",
        temperature=0.7,
        tools=[],
        timeout=90,
        max_retries=5,
    )


@pytest.fixture
def sample_result1():
    """Sample task result 1."""
    return TaskResult(
        task_name="hearsay",
        category="CONCLUSION_TASKS",
        samples_evaluated=20,
        metric="balanced_accuracy",
        score=0.85,
        avg_execution_time=2.3,
        avg_tokens=450.0,
        errors=0,
    )


@pytest.fixture
def sample_result2():
    """Sample task result 2 (improved score)."""
    return TaskResult(
        task_name="hearsay",
        category="CONCLUSION_TASKS",
        samples_evaluated=20,
        metric="balanced_accuracy",
        score=0.87,
        avg_execution_time=2.2,
        avg_tokens=455.0,
        errors=0,
    )


@pytest.fixture
def sample_result3():
    """Sample task result 3 (different task)."""
    return TaskResult(
        task_name="contract_qa",
        category="INTERPRETATION_TASKS",
        samples_evaluated=20,
        metric="balanced_accuracy",
        score=0.92,
        avg_execution_time=2.5,
        avg_tokens=480.0,
        errors=0,
    )


@pytest.fixture
def sample_run1(sample_config1, sample_result1):
    """Sample evaluation run 1."""
    return EvaluationRun(
        run_id="run_001",
        agent_config=sample_config1,
        tasks=["hearsay"],
        samples_per_task=20,
        results=[sample_result1],
    )


@pytest.fixture
def sample_run2(sample_config1, sample_result2):
    """Sample evaluation run 2 (improved results)."""
    return EvaluationRun(
        run_id="run_002",
        agent_config=sample_config1,
        tasks=["hearsay"],
        samples_per_task=20,
        results=[sample_result2],
    )


@pytest.fixture
def sample_run_different_config(sample_config2, sample_result2):
    """Sample evaluation run with different configuration."""
    return EvaluationRun(
        run_id="run_003",
        agent_config=sample_config2,
        tasks=["hearsay"],
        samples_per_task=30,
        results=[sample_result2],
    )


# ============================================================================
# Argument Parsing Tests
# ============================================================================


def test_parse_arguments_basic(monkeypatch):
    """Test basic argument parsing with two paths."""
    monkeypatch.setattr(
        "sys.argv",
        ["compare_runs.py", "run1.json", "run2.json"],
    )

    args = parse_arguments()

    assert args.run1_path == "run1.json"
    assert args.run2_path == "run2.json"
    assert args.format == "table"  # Default
    assert args.threshold == 0.01  # Default
    assert args.output is None  # Default


def test_parse_arguments_with_options(monkeypatch):
    """Test argument parsing with all options."""
    monkeypatch.setattr(
        "sys.argv",
        [
            "compare_runs.py",
            "run1.json",
            "run2.json",
            "--format",
            "json",
            "--threshold",
            "0.05",
            "--output",
            "comparison.json",
        ],
    )

    args = parse_arguments()

    assert args.run1_path == "run1.json"
    assert args.run2_path == "run2.json"
    assert args.format == "json"
    assert args.threshold == 0.05
    assert args.output == "comparison.json"


def test_parse_arguments_format_choices(monkeypatch):
    """Test that format argument only accepts valid choices."""
    # Valid format
    monkeypatch.setattr(
        "sys.argv",
        ["compare_runs.py", "run1.json", "run2.json", "--format", "markdown"],
    )
    args = parse_arguments()
    assert args.format == "markdown"

    # Invalid format should raise SystemExit (argparse error)
    monkeypatch.setattr(
        "sys.argv",
        ["compare_runs.py", "run1.json", "run2.json", "--format", "invalid"],
    )
    with pytest.raises(SystemExit):
        parse_arguments()


# ============================================================================
# Delta Calculation Tests
# ============================================================================


def test_calculate_delta_improvement():
    """Test delta calculation for improvement."""
    delta = calculate_delta(0.80, 0.85, threshold=0.01)

    assert delta["absolute"] == pytest.approx(0.05, abs=1e-6)
    assert delta["percentage"] == pytest.approx(6.25, abs=1e-2)
    assert delta["direction"] == "improvement"
    assert delta["indicator"] == "↑"


def test_calculate_delta_regression():
    """Test delta calculation for regression."""
    delta = calculate_delta(0.85, 0.80, threshold=0.01)

    assert delta["absolute"] == pytest.approx(-0.05, abs=1e-6)
    assert delta["percentage"] == pytest.approx(-5.88, abs=1e-1)
    assert delta["direction"] == "regression"
    assert delta["indicator"] == "↓"


def test_calculate_delta_unchanged():
    """Test delta calculation for unchanged (within threshold)."""
    delta = calculate_delta(0.80, 0.805, threshold=0.01)

    assert delta["absolute"] == pytest.approx(0.005, abs=1e-6)
    assert delta["direction"] == "unchanged"
    assert delta["indicator"] == "→"


def test_calculate_delta_zero_score():
    """Test delta calculation when first score is zero (edge case)."""
    delta = calculate_delta(0.0, 0.5, threshold=0.01)

    assert delta["absolute"] == 0.5
    assert delta["percentage"] == 0.0  # Avoid division by zero
    assert delta["direction"] == "improvement"


def test_calculate_delta_custom_threshold():
    """Test delta calculation with custom threshold."""
    # 0.04 difference with 0.05 threshold = unchanged
    delta = calculate_delta(0.80, 0.84, threshold=0.05)

    assert delta["absolute"] == pytest.approx(0.04, abs=1e-6)
    assert delta["direction"] == "unchanged"
    assert delta["indicator"] == "→"

    # 0.06 difference with 0.05 threshold = improvement
    delta = calculate_delta(0.80, 0.86, threshold=0.05)

    assert delta["absolute"] == pytest.approx(0.06, abs=1e-6)
    assert delta["direction"] == "improvement"
    assert delta["indicator"] == "↑"


# ============================================================================
# Delta Formatting Tests
# ============================================================================


def test_format_delta_string_improvement():
    """Test formatting delta string for improvement (green)."""
    delta = {"absolute": 0.05, "percentage": 6.25, "direction": "improvement", "indicator": "↑"}
    result = format_delta_string(delta)

    # Should contain the delta value and indicator
    assert "+0.0500" in result
    assert "↑" in result


def test_format_delta_string_regression():
    """Test formatting delta string for regression (red)."""
    delta = {"absolute": -0.05, "percentage": -5.88, "direction": "regression", "indicator": "↓"}
    result = format_delta_string(delta)

    # Should contain the delta value and indicator
    assert "-0.0500" in result
    assert "↓" in result


def test_format_delta_string_unchanged():
    """Test formatting delta string for unchanged (yellow)."""
    delta = {"absolute": 0.005, "percentage": 0.625, "direction": "unchanged", "indicator": "→"}
    result = format_delta_string(delta)

    # Should contain the delta value and indicator
    assert "0.0050" in result
    assert "→" in result


# ============================================================================
# Task Comparison Map Tests
# ============================================================================


def test_build_task_comparison_map_identical(sample_run1, sample_run2):
    """Test building comparison map when both runs have same tasks."""
    comparison_map = build_task_comparison_map(sample_run1, sample_run2)

    assert len(comparison_map) == 1
    assert "hearsay" in comparison_map

    hearsay_comp = comparison_map["hearsay"]
    assert hearsay_comp["status"] == "both"
    assert hearsay_comp["run1_result"] is not None
    assert hearsay_comp["run2_result"] is not None
    assert hearsay_comp["run1_result"].score == 0.85
    assert hearsay_comp["run2_result"].score == 0.87


def test_build_task_comparison_map_missing_tasks(sample_config1, sample_result1, sample_result3):
    """Test building comparison map with missing tasks."""
    run1 = EvaluationRun(
        run_id="run_001",
        agent_config=sample_config1,
        tasks=["hearsay"],
        samples_per_task=20,
        results=[sample_result1],
    )

    run2 = EvaluationRun(
        run_id="run_002",
        agent_config=sample_config1,
        tasks=["contract_qa"],
        samples_per_task=20,
        results=[sample_result3],
    )

    comparison_map = build_task_comparison_map(run1, run2)

    assert len(comparison_map) == 2
    assert "hearsay" in comparison_map
    assert "contract_qa" in comparison_map

    # hearsay only in run1
    assert comparison_map["hearsay"]["status"] == "run1_only"
    assert comparison_map["hearsay"]["run1_result"] is not None
    assert comparison_map["hearsay"]["run2_result"] is None

    # contract_qa only in run2
    assert comparison_map["contract_qa"]["status"] == "run2_only"
    assert comparison_map["contract_qa"]["run1_result"] is None
    assert comparison_map["contract_qa"]["run2_result"] is not None


def test_build_task_comparison_map_overlapping(sample_config1, sample_result1, sample_result2, sample_result3):
    """Test building comparison map with some overlapping tasks."""
    run1 = EvaluationRun(
        run_id="run_001",
        agent_config=sample_config1,
        tasks=["hearsay", "contract_qa"],
        samples_per_task=20,
        results=[sample_result1, sample_result3],
    )

    # Create a new contract_qa result for run2
    contract_qa_run2 = TaskResult(
        task_name="contract_qa",
        category="INTERPRETATION_TASKS",
        samples_evaluated=20,
        metric="balanced_accuracy",
        score=0.95,
        avg_execution_time=2.4,
        avg_tokens=475.0,
        errors=0,
    )

    run2 = EvaluationRun(
        run_id="run_002",
        agent_config=sample_config1,
        tasks=["hearsay", "contract_qa"],
        samples_per_task=20,
        results=[sample_result2, contract_qa_run2],
    )

    comparison_map = build_task_comparison_map(run1, run2)

    assert len(comparison_map) == 2

    # Both tasks should be in both runs
    assert comparison_map["hearsay"]["status"] == "both"
    assert comparison_map["contract_qa"]["status"] == "both"


# ============================================================================
# Configuration Difference Tests
# ============================================================================


def test_detect_configuration_differences_none(sample_run1, sample_run2):
    """Test detecting configuration differences when there are none."""
    warnings = detect_configuration_differences(sample_run1, sample_run2)

    assert len(warnings) == 0


def test_detect_configuration_differences_model(sample_run1, sample_run_different_config):
    """Test detecting model differences."""
    warnings = detect_configuration_differences(sample_run1, sample_run_different_config)

    assert len(warnings) >= 1
    assert any("model" in w.lower() for w in warnings)
    assert any("claude-sonnet-4" in w and "claude-opus-4" in w for w in warnings)


def test_detect_configuration_differences_temperature(sample_run1, sample_run_different_config):
    """Test detecting temperature differences."""
    warnings = detect_configuration_differences(sample_run1, sample_run_different_config)

    assert any("temperature" in w.lower() for w in warnings)
    assert any("0.0" in w and "0.7" in w for w in warnings)


def test_detect_configuration_differences_timeout(sample_run1, sample_run_different_config):
    """Test detecting timeout differences."""
    warnings = detect_configuration_differences(sample_run1, sample_run_different_config)

    assert any("timeout" in w.lower() for w in warnings)
    assert any("60" in w and "90" in w for w in warnings)


def test_detect_configuration_differences_sample_size(sample_run1, sample_run_different_config):
    """Test detecting sample size differences."""
    warnings = detect_configuration_differences(sample_run1, sample_run_different_config)

    assert any("sample" in w.lower() for w in warnings)
    assert any("20" in w and "30" in w for w in warnings)


def test_detect_configuration_differences_max_retries(sample_run1, sample_run_different_config):
    """Test detecting max retries differences."""
    warnings = detect_configuration_differences(sample_run1, sample_run_different_config)

    assert any("retries" in w.lower() for w in warnings)
    assert any("3" in w and "5" in w for w in warnings)


# ============================================================================
# File Loading Tests
# ============================================================================


def test_load_runs_valid(tmp_path, sample_run1, sample_run2):
    """Test loading two valid evaluation runs."""
    # Create temporary JSON files
    path1 = tmp_path / "run1.json"
    path2 = tmp_path / "run2.json"

    # Write run data
    with open(path1, "w", encoding="utf-8") as f:
        json.dump(sample_run1.model_dump(mode="json"), f)

    with open(path2, "w", encoding="utf-8") as f:
        json.dump(sample_run2.model_dump(mode="json"), f)

    # Load runs
    run1, run2 = load_runs(path1, path2)

    assert run1.run_id == "run_001"
    assert run2.run_id == "run_002"
    assert len(run1.results) == 1
    assert len(run2.results) == 1


def test_load_runs_file_not_found(tmp_path):
    """Test loading runs when file doesn't exist."""
    path1 = tmp_path / "nonexistent1.json"
    path2 = tmp_path / "nonexistent2.json"

    with pytest.raises(FileNotFoundError):
        load_runs(path1, path2)


def test_load_runs_invalid_json(tmp_path):
    """Test loading runs with invalid JSON."""
    path1 = tmp_path / "invalid1.json"
    path2 = tmp_path / "invalid2.json"

    # Write invalid JSON
    with open(path1, "w", encoding="utf-8") as f:
        f.write("{ invalid json }")

    with open(path2, "w", encoding="utf-8") as f:
        f.write("{ also invalid }")

    with pytest.raises(Exception):  # Could be JSONDecodeError or ValueError
        load_runs(path1, path2)


# ============================================================================
# Output Function Tests (using capsys to capture stdout)
# ============================================================================


def test_print_comparison_table_basic(capsys, sample_run1, sample_run2):
    """Test printing comparison table with basic data."""
    from scripts.compare_runs import print_comparison_table

    comparison_map = build_task_comparison_map(sample_run1, sample_run2)
    print_comparison_table(comparison_map, threshold=0.01)

    captured = capsys.readouterr()
    output = captured.out

    # Check for table structure
    assert "Task Name" in output
    assert "Run 1" in output
    assert "Run 2" in output
    assert "Delta" in output
    assert "hearsay" in output
    assert "0.8500" in output
    assert "0.8700" in output


def test_print_summary_comparison(capsys, sample_run1, sample_run2):
    """Test printing summary comparison."""
    from scripts.compare_runs import print_summary_comparison

    print_summary_comparison(sample_run1, sample_run2)

    captured = capsys.readouterr()
    output = captured.out

    # Check for summary statistics
    assert "Overall Statistics" in output
    assert "Total Samples" in output
    assert "Average Score" in output
    assert "Total Time" in output


def test_print_metadata_comparison(capsys, sample_run1, sample_run2):
    """Test printing metadata comparison."""
    from scripts.compare_runs import print_metadata_comparison

    print_metadata_comparison(sample_run1, sample_run2)

    captured = capsys.readouterr()
    output = captured.out

    # Check for metadata
    assert "Run Metadata" in output
    assert "run_001" in output
    assert "run_002" in output
    assert "Agent:" in output
    assert "Model:" in output


# ============================================================================
# JSON Export Tests
# ============================================================================


def test_export_comparison_json(tmp_path, sample_run1, sample_run2):
    """Test exporting comparison to JSON file."""
    from scripts.compare_runs import export_comparison_json

    comparison_map = build_task_comparison_map(sample_run1, sample_run2)
    output_path = tmp_path / "comparison.json"

    export_comparison_json(comparison_map, sample_run1, sample_run2, output_path)

    # Verify file exists
    assert output_path.exists()

    # Load and verify contents
    with open(output_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "run1" in data
    assert "run2" in data
    assert "task_comparisons" in data
    assert "config_differences" in data

    assert data["run1"]["run_id"] == "run_001"
    assert data["run2"]["run_id"] == "run_002"
    assert len(data["task_comparisons"]) == 1


def test_export_comparison_json_creates_directory(tmp_path, sample_run1, sample_run2):
    """Test that export creates parent directories if needed."""
    from scripts.compare_runs import export_comparison_json

    comparison_map = build_task_comparison_map(sample_run1, sample_run2)
    output_path = tmp_path / "subdir" / "comparison.json"

    export_comparison_json(comparison_map, sample_run1, sample_run2, output_path)

    # Verify file exists in created directory
    assert output_path.exists()
    assert output_path.parent.exists()


# ============================================================================
# Integration Tests
# ============================================================================


def test_main_success(tmp_path, monkeypatch, capsys, sample_run1, sample_run2):
    """Test main() function with successful comparison."""
    from scripts.compare_runs import main

    # Create temporary JSON files
    path1 = tmp_path / "run1.json"
    path2 = tmp_path / "run2.json"

    with open(path1, "w", encoding="utf-8") as f:
        json.dump(sample_run1.model_dump(mode="json"), f)

    with open(path2, "w", encoding="utf-8") as f:
        json.dump(sample_run2.model_dump(mode="json"), f)

    # Mock sys.argv
    monkeypatch.setattr(
        "sys.argv",
        ["compare_runs.py", str(path1), str(path2)],
    )

    # Run main
    exit_code = main()

    assert exit_code == 0

    # Verify output
    captured = capsys.readouterr()
    assert "Comparison complete" in captured.out


def test_main_file_not_found(tmp_path, monkeypatch, capsys):
    """Test main() function with non-existent file."""
    from scripts.compare_runs import main

    path1 = tmp_path / "nonexistent1.json"
    path2 = tmp_path / "nonexistent2.json"

    monkeypatch.setattr(
        "sys.argv",
        ["compare_runs.py", str(path1), str(path2)],
    )

    exit_code = main()

    assert exit_code == 1

    captured = capsys.readouterr()
    assert "ERROR" in captured.out or "error" in captured.out.lower()


def test_main_with_json_export(tmp_path, monkeypatch, sample_run1, sample_run2):
    """Test main() function with JSON export option."""
    from scripts.compare_runs import main

    # Create temporary JSON files
    path1 = tmp_path / "run1.json"
    path2 = tmp_path / "run2.json"
    output_path = tmp_path / "comparison.json"

    with open(path1, "w", encoding="utf-8") as f:
        json.dump(sample_run1.model_dump(mode="json"), f)

    with open(path2, "w", encoding="utf-8") as f:
        json.dump(sample_run2.model_dump(mode="json"), f)

    # Mock sys.argv
    monkeypatch.setattr(
        "sys.argv",
        ["compare_runs.py", str(path1), str(path2), "--output", str(output_path)],
    )

    # Run main
    exit_code = main()

    assert exit_code == 0
    assert output_path.exists()

    # Verify exported JSON
    with open(output_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "task_comparisons" in data


def test_print_comparison_markdown(capsys, sample_run1, sample_run2):
    """Test printing comparison in markdown format."""
    from scripts.compare_runs import print_comparison_markdown

    comparison_map = build_task_comparison_map(sample_run1, sample_run2, verbose=False)
    print_comparison_markdown(comparison_map, threshold=0.01)

    captured = capsys.readouterr()
    output = captured.out

    # Check for markdown table structure
    assert "## Task-by-Task Comparison" in output
    assert "| Task Name | Run 1 | Run 2 | Delta | Metric |" in output
    assert "|-----------|-------|-------|-------|--------|" in output
    assert "| hearsay |" in output
    assert "0.8500" in output
    assert "0.8700" in output


def test_print_comparison_json(capsys, sample_run1, sample_run2):
    """Test printing comparison in JSON format."""
    from scripts.compare_runs import print_comparison_json

    comparison_map = build_task_comparison_map(sample_run1, sample_run2, verbose=False)
    print_comparison_json(comparison_map, sample_run1, sample_run2, threshold=0.01)

    captured = capsys.readouterr()
    output = captured.out

    # Should be valid JSON
    import json
    data = json.loads(output)

    # Check structure
    assert "comparison_timestamp" in data
    assert "run1" in data
    assert "run2" in data
    assert "task_comparisons" in data
    assert "config_differences" in data

    # Check task comparisons
    assert len(data["task_comparisons"]) == 1
    assert data["task_comparisons"][0]["task_name"] == "hearsay"
    assert data["task_comparisons"][0]["status"] == "both"


def test_main_with_markdown_format(tmp_path, monkeypatch, capsys, sample_run1, sample_run2):
    """Test main() function with markdown format."""
    from scripts.compare_runs import main

    # Create temporary JSON files
    path1 = tmp_path / "run1.json"
    path2 = tmp_path / "run2.json"

    with open(path1, "w", encoding="utf-8") as f:
        json.dump(sample_run1.model_dump(mode="json"), f)

    with open(path2, "w", encoding="utf-8") as f:
        json.dump(sample_run2.model_dump(mode="json"), f)

    # Mock sys.argv
    monkeypatch.setattr(
        "sys.argv",
        ["compare_runs.py", str(path1), str(path2), "--format", "markdown"],
    )

    # Run main
    exit_code = main()

    assert exit_code == 0

    # Verify markdown output
    captured = capsys.readouterr()
    assert "## Task-by-Task Comparison" in captured.out
    assert "|" in captured.out  # Markdown table pipes


def test_main_with_json_format(tmp_path, monkeypatch, capsys, sample_run1, sample_run2):
    """Test main() function with JSON format."""
    from scripts.compare_runs import main

    # Create temporary JSON files
    path1 = tmp_path / "run1.json"
    path2 = tmp_path / "run2.json"

    with open(path1, "w", encoding="utf-8") as f:
        json.dump(sample_run1.model_dump(mode="json"), f)

    with open(path2, "w", encoding="utf-8") as f:
        json.dump(sample_run2.model_dump(mode="json"), f)

    # Mock sys.argv
    monkeypatch.setattr(
        "sys.argv",
        ["compare_runs.py", str(path1), str(path2), "--format", "json"],
    )

    # Run main
    exit_code = main()

    assert exit_code == 0

    # Verify JSON output is parseable (skip any status messages from load_results)
    captured = capsys.readouterr()
    output_lines = captured.out.strip().split("\n")

    # Find JSON start (first line with {)
    json_start = None
    for i, line in enumerate(output_lines):
        if line.strip().startswith("{"):
            json_start = i
            break

    assert json_start is not None
    json_text = "\n".join(output_lines[json_start:])
    data = json.loads(json_text)

    assert "task_comparisons" in data
    assert "run1" in data
    assert "run2" in data


def test_sorted_tasks_stable_order(sample_config1):
    """Test that tasks with equal delta magnitudes are sorted by name."""
    from scripts.compare_runs import _get_sorted_tasks

    # Create three tasks with same scores (zero delta, equal magnitude)
    result_a = TaskResult(
        task_name="task_a",
        category="CONCLUSION_TASKS",
        samples_evaluated=20,
        metric="balanced_accuracy",
        score=0.80,
        avg_execution_time=2.0,
        avg_tokens=400.0,
        errors=0,
    )

    result_b = TaskResult(
        task_name="task_b",
        category="CONCLUSION_TASKS",
        samples_evaluated=20,
        metric="balanced_accuracy",
        score=0.80,
        avg_execution_time=2.0,
        avg_tokens=400.0,
        errors=0,
    )

    result_z = TaskResult(
        task_name="task_z",
        category="CONCLUSION_TASKS",
        samples_evaluated=20,
        metric="balanced_accuracy",
        score=0.80,
        avg_execution_time=2.0,
        avg_tokens=400.0,
        errors=0,
    )

    run1 = EvaluationRun(
        run_id="run_001",
        agent_config=sample_config1,
        tasks=["task_z", "task_a", "task_b"],  # Not alphabetical
        samples_per_task=20,
        results=[result_z, result_a, result_b],
    )

    run2 = EvaluationRun(
        run_id="run_002",
        agent_config=sample_config1,
        tasks=["task_b", "task_z", "task_a"],  # Different order
        samples_per_task=20,
        results=[result_b, result_z, result_a],  # Same scores = same delta magnitude
    )

    comparison_map = build_task_comparison_map(run1, run2, verbose=False)
    sorted_tasks = _get_sorted_tasks(comparison_map, threshold=0.01)

    # Tasks with equal magnitudes should be sorted alphabetically (stable sort)
    task_names = [name for name, _ in sorted_tasks]
    assert task_names == ["task_a", "task_b", "task_z"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
