import weave
from weave import Dataset, Evaluation
from weave.flow import leaderboard
from weave.trace.ref_util import get_ref
from leaderboard.scorer.legalbench_scorer import LegalBenchScorer
from leaderboard.organizer_setup.utils.upload_datasets import upload_dataset
from leaderboard.organizer_setup.utils.get_task_metric import get_task_metric
from leaderboard.organizer_setup.utils.preprocessing import preprocess_example
import argparse

# setup
HUGGINGFACE_DATASET = "nguha/legalbench"
# sample selection of tasks, for real leaderboard one could simply import all task names from evaluation.py
TASKS = [
    "abercrombie",
    "sara_numeric",
    "successor_liability",
    "citation_prediction_open",
    "definition_extraction",
    "ssla_company_defendants",
]

def main():
    parser = argparse.ArgumentParser(description='Setup LegalBench leaderboard')
    parser.add_argument('--team', type=str, help='Weave team name')
    parser.add_argument('--project', type=str, help='Weave project name')
    
    args = parser.parse_args()
    
    WEAVE_TEAM = args.team
    WEAVE_PROJECT = args.project
    SPLIT = "test"

    client = weave.init(f"{WEAVE_TEAM}/{WEAVE_PROJECT}")

    for task in TASKS:
        dataset = upload_dataset(HUGGINGFACE_DATASET, task)
        evaluation = Evaluation(
            name=f"{task}_evaluation", 
            dataset=dataset, 
            scorers=[LegalBenchScorer(task=task)],
            preprocess_model_input=preprocess_example
        )
        weave.publish(evaluation, f"{task}_evaluation")
        leaderboard_spec = leaderboard.Leaderboard(
            name=f"{task}",
            description=f"""
This leaderboard compares the performance of models on the LegalBench {task} task.""",
            columns=[
                leaderboard.LeaderboardColumn(
                    evaluation_object_ref=get_ref(evaluation).uri(),
                    scorer_name="LegalBenchScorer",
                    summary_metric_path=get_task_metric(task),
                )
            ],
        )
        
        # Publish the leaderboard
        weave.publish(leaderboard_spec, f"{task}_leaderboard")

if __name__ == "__main__":
    main()

# invoke via python -m leaderboard.organizer_setup.setup --team <name of weave team> --project <name of weave project>