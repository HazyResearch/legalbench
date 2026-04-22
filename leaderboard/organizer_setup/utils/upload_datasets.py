import textwrap
import weave
from weave import Dataset
from datasets import load_dataset, load_dataset_builder

# ------------------------------------------------------------------
HUGGINGFACE_DATASET = "nguha/legalbench"
# sample selection, for real leaderboard one could simply import all task names from evaluation.py
TASKS = [
    "abercrombie",
    "sara_numeric",
    "successor_liability",
    "citation_prediction_open",
    "definition_extraction",
    "ssla_company_defendants",
]
WEAVE_TEAM    = "fuels"
WEAVE_PROJECT = "legalbench-leaderboard4"
SPLIT         = "test"
# ------------------------------------------------------------------

def build_description(info, split):
    """Return a markdown string for Weave's `description` field."""

    return textwrap.dedent(f"""\
        Task Name: {info.config_name}

        Split: {split}
        
        Description: {info.description}

        License: {info.license}

        Citation: {info.citation}
    """)

def upload_dataset(hf_dataset: str, task: str):
    # use builder to access metadata
    builder = load_dataset_builder(hf_dataset, task)
    # load data
    ds = load_dataset(HUGGINGFACE_DATASET, task, split=SPLIT)

    info = builder.info
    df   = ds.to_pandas()
    desc = build_description(info, SPLIT)

    weave_ds = Dataset(
        name        = f"{task}_{SPLIT}",
        rows        = df,
        description = desc,
    )

    return weave.publish(weave_ds, name=weave_ds.name)
