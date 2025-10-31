"""
Maite AI Agent Evaluation System for LegalBench

This package provides infrastructure for evaluating the Maite AI agent
on LegalBench tasks following canonical patterns.
"""

__version__ = "0.1.0"

from eval_maite.models import AgentConfig, EvaluationRun, TaskResult, TaskTrace
from eval_maite.task_loader import (
    get_task_category,
    get_test_df,
    get_train_df,
    load_prompt_template,
    load_task_data,
)
from eval_maite.utils import generate_run_id, load_results, save_results

from eval_maite.agent_wrapper import MaiteAgentWrapper

__all__ = [
    "AgentConfig",
    "EvaluationRun",
    "TaskResult",
    "TaskTrace",
    "get_task_category",
    "get_test_df",
    "get_train_df",
    "load_prompt_template",
    "load_task_data",
    "generate_run_id",
    "load_results",
    "save_results",
    "MaiteAgentWrapper",
]
