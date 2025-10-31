"""
Pydantic data models for Maite evaluation system.

These models define the structure for evaluation runs, task results, and traces.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict, field_serializer


class AgentConfig(BaseModel):
    """Configuration for the Maite AI agent."""

    name: str = Field(default="maite", description="Agent name")
    version: str = Field(default="0.1.0", description="Agent version")
    model: str = Field(default="claude-sonnet-4", description="Model identifier")
    temperature: float = Field(default=0.0, ge=0.0, le=2.0, description="Model temperature")
    tools: List[str] = Field(default_factory=list, description="Available tools")
    timeout: int = Field(default=60, gt=0, description="Timeout in seconds per sample")
    max_retries: int = Field(default=3, ge=0, description="Maximum retry attempts")


class TaskTrace(BaseModel):
    """Execution trace for a single task sample."""

    sample_id: str = Field(..., description="Unique sample identifier (task_name_split_index)")
    input_text: str = Field(..., description="Input prompt sent to agent")
    expected_output: str = Field(..., description="Ground truth answer")
    actual_output: str = Field(..., description="Agent's generated output")
    is_correct: bool = Field(..., description="Whether output matches expected")
    execution_time: float = Field(..., ge=0.0, description="Execution time in seconds")
    tokens: Optional[Dict[str, int]] = Field(
        default=None, description="Token counts (input, output, total)"
    )
    tool_calls: List[Dict[str, Any]] = Field(
        default_factory=list, description="List of tool calls made during execution"
    )
    chain_steps: List[str] = Field(
        default_factory=list, description="Reasoning chain steps"
    )
    error: Optional[str] = Field(default=None, description="Error message if execution failed")


class TaskResult(BaseModel):
    """Aggregated results for a single task."""

    task_name: str = Field(..., description="Task name (e.g., 'hearsay')")
    category: str = Field(..., description="Task category (ISSUE_TASKS, RULE_TASKS, etc.)")
    samples_evaluated: int = Field(..., ge=0, description="Number of samples evaluated")
    metric: str = Field(..., description="Evaluation metric used (e.g., 'balanced_accuracy')")
    score: float = Field(..., ge=0.0, le=1.0, description="Evaluation score")
    avg_execution_time: float = Field(..., ge=0.0, description="Average execution time in seconds")
    avg_tokens: Optional[float] = Field(
        default=None, ge=0.0, description="Average total tokens per sample"
    )
    avg_tool_calls: Optional[float] = Field(
        default=None, ge=0.0, description="Average tool calls per sample"
    )
    errors: int = Field(default=0, ge=0, description="Number of errors encountered")
    traces: Optional[List[TaskTrace]] = Field(
        default=None, description="Detailed execution traces (optional)"
    )


class EvaluationRun(BaseModel):
    """Complete evaluation run with metadata and results."""

    run_id: str = Field(..., description="Unique run identifier (e.g., 'run_20251028_153000')")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Run start timestamp"
    )
    agent_config: AgentConfig = Field(..., description="Agent configuration used")
    tasks: List[str] = Field(..., description="List of task names evaluated")
    samples_per_task: int = Field(..., gt=0, description="Number of samples per task")
    results: List[TaskResult] = Field(default_factory=list, description="Task-level results")
    summary: Optional[Dict[str, Any]] = Field(
        default=None, description="Summary statistics for the run"
    )

    def add_result(self, result: TaskResult) -> None:
        """Add a task result to the run."""
        self.results.append(result)

    def compute_summary(self) -> Dict[str, Any]:
        """Compute summary statistics across all tasks."""
        if not self.results:
            return {
                "total_samples": 0,
                "total_time": 0.0,
                "avg_accuracy": 0.0,
                "tasks_completed": 0,
                "total_errors": 0,
            }

        total_samples = sum(r.samples_evaluated for r in self.results)
        total_time = sum(r.avg_execution_time * r.samples_evaluated for r in self.results)
        total_errors = sum(r.errors for r in self.results)

        # Calculate weighted average accuracy
        weighted_scores = sum(r.score * r.samples_evaluated for r in self.results)
        avg_accuracy = weighted_scores / total_samples if total_samples > 0 else 0.0

        # Calculate token usage if available
        total_tokens = 0
        token_count = 0
        for r in self.results:
            if r.avg_tokens is not None:
                total_tokens += r.avg_tokens * r.samples_evaluated
                token_count += r.samples_evaluated

        avg_tokens = total_tokens / token_count if token_count > 0 else None

        summary = {
            "total_samples": total_samples,
            "total_time": round(total_time, 2),
            "avg_accuracy": round(avg_accuracy, 4),
            "tasks_completed": len(self.results),
            "total_errors": total_errors,
        }

        if avg_tokens is not None:
            summary["avg_tokens"] = round(avg_tokens, 1)

        self.summary = summary
        return summary

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()}
    )

    @field_serializer('timestamp')
    def serialize_timestamp(self, value: datetime) -> str:
        """Serialize datetime to ISO format."""
        return value.isoformat()
