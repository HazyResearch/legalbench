from evaluation import EXACT_MATCH_BALANCED_ACC_TASKS, MANUAL_EVAL_TASKS

def get_task_metric(task: str) -> str:
    """
    Automatically determine the summary metric for any LegalBench task.
    This mirrors the logic in LegalBenchScorer.summarize().
    """
    if task in EXACT_MATCH_BALANCED_ACC_TASKS:
        return "balanced_accuracy"
    elif task == "sara_numeric":
        return "arithmetic_mean"
    elif task == "successor_liability" or task.startswith("ssla"):
        return "f1"
    elif task in ["citation_prediction_open", "definition_extraction"]:
        return "plain_accuracy"
    elif task in MANUAL_EVAL_TASKS:
        raise ValueError(f"Task {task} requires manual evaluation")
    else:
        raise ValueError(f"Task unknown")