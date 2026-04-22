import weave
from weave import Scorer
from typing import Any
from evaluation import (
    normalize,
    EXACT_MATCH_BALANCED_ACC_TASKS,
    MANUAL_EVAL_TASKS,
)
from leaderboard.scorer.row_level_metrics import (
    evaluate_exact_match,
    evaluate_sara_within_10pt,
    evaluate_successor_liability_f1_single_example,
    evaluate_citation_open_single_example,
    evaluate_definition_extraction_single_row,
    evaluate_ssla_row
)
from leaderboard.scorer.task_level_metrics import (
    plain_accuracy,
    arithmetic_mean,
    balanced_accuracy,
    micro_f1
    
)

class LegalBenchScorer(Scorer):
    task: str

    @weave.op()
    async def score(self, output: dict | None, answer: str) -> Any:
        """Scores the correctness of the predictions on a per-example basis.
        Selects the correct (row-level) metric depending on the task.
        Args:
            - """
        
        if output is None:
            raise ValueError("No model output to score")
        
        generation = output.get("generation")
        if generation is None:
            raise KeyError("Expected 'prediction' key in output dict")

        task = self.task

        if task in EXACT_MATCH_BALANCED_ACC_TASKS:
            normalized_answer_em = normalize(answer, stem=False)
            normalized_generation_em = normalize(generation, stem=False)
            # adding normalized answer and generation separately to calculate balanced accuracy on class level in summarize() later
            return {"exact_match": evaluate_exact_match(normalized_generation_em, normalized_answer_em), "normalized_answer": normalized_answer_em, "normalized_generation": normalized_generation_em, "task_level_metric": "balanced_accuracy"}
        elif task == "sara_numeric":
            return {"within_10pt": evaluate_sara_within_10pt(generation, answer), "task_level_metric": "arithmetic_mean"}
        elif task == "successor_liability":
            tp, fp, fn = evaluate_successor_liability_f1_single_example(generation, answer)
            return {"tp": tp, "fp": fp, "fn": fn, "f1": 2 * tp / (2 * tp + fp + fn), "task_level_metric": "f1"}
        elif task == "citation_prediction_open":
            return {"correct": evaluate_citation_open_single_example(generation, answer), "task_level_metric": "plain_accuracy"}
        elif task == "definition_extraction":
            return {"correct": evaluate_definition_extraction_single_row(generation, answer), "task_level_metric": "plain_accuracy"}
        elif task.startswith("ssla"):
            tp, fp, fn = evaluate_ssla_row(generation, answer)
            return {"tp": tp, "fp": fp, "fn": fn, "f1": 2 * tp / (2 * tp + fp + fn), "task_level_metric": "f1"}
        elif task in MANUAL_EVAL_TASKS:
            raise Exception("This task needs to be manually evaluated:", task)
        else:
            raise Exception(f"Unknown task: {task}")
        
    @weave.op()
    def summarize(self, score_rows: list) -> dict | None:
        """
        Aggregate per-example score dicts into a single task-level result 
        based on the correct task-level metric.

        • plain_accuracy      → rows have "correct": 0/1
        • balanced_accuracy   → rows have "exact_match": bool
        • arithmetic_mean     → rows have "within_10pt": 0/1
        • f1                  → rows have tp / fp / fn
        """

        if not score_rows:
            return None

        # Every row of a run has the same task_level_metric,
        # so just read it off the first one.
        metric_type = score_rows[0].get("task_level_metric")
        if metric_type is None:
            raise ValueError("No task_level_metric found in score rows")

        # plain accuracy
        if metric_type == "plain_accuracy":
            return {"plain_accuracy": plain_accuracy(score_rows)}

        # arithmetic mean
        elif metric_type == "arithmetic_mean":
            return {"arithmetic_mean": arithmetic_mean(score_rows)}

        # balanced accuracy
        elif metric_type == "balanced_accuracy":
            return {"balanced_accuracy": balanced_accuracy(score_rows)}

        # micro-F1
        elif metric_type == "f1":
            tp_total, fp_total, fn_total, micro_f1_total = micro_f1(score_rows)
            return {"tp": tp_total, "fp": fp_total, "fn": fn_total, "f1": micro_f1_total}

        # unknown metric
        else:
            raise ValueError(f"Unrecognised task_level_metric: {metric_type}")
