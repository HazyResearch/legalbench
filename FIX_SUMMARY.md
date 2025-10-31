# LegalBench Dataset Loading Fix - Summary

## Problem
The notebook `/Users/laurentwiesel/Dev/S-C/legalbench/UsingLegalBench.ipynb` was unable to load LegalBench datasets from HuggingFace due to incompatibility with the `datasets` library version 4.3.0, which no longer supports dataset loading scripts (`.py` files).

## Solution Implemented

### 1. Downgraded `datasets` Library
- **From:** `datasets==4.3.0` (incompatible)
- **To:** `datasets==2.19.0` (supports loading scripts)
- **Command used:** `uv pip install "datasets==2.19.0"`

### 2. Updated `pyproject.toml`
- Changed dependency from `datasets>=2.14.0` to `datasets>=2.19.0,<3.0.0`
- This ensures the correct version range is used in future installations

### 3. Reverted Notebook Cells
All notebook cells were reverted to use `datasets.load_dataset()` from HuggingFace:

#### Cell 0 (Markdown)
- **Before:** Warning about local files only
- **After:** Clean introduction without warnings

#### Cell 5 (Markdown)
- **Before:** Instructions to use local TSV files
- **After:** Instructions to load from HuggingFace with proper documentation links

#### Cell 6 (Code)
- **Before:**
  ```python
  import pandas as pd
  train_df = pd.read_csv("tasks/abercrombie/train.tsv", sep="\t", encoding="utf-8")
  test_df = pd.read_csv("tasks/abercrombie/test.tsv", sep="\t", encoding="utf-8")
  ```
- **After:**
  ```python
  data = datasets.load_dataset("nguha/legalbench", "abercrombie")
  data
  ```

#### Cell 10 (Code)
- Added line to convert dataset to pandas: `test_df = data["test"].to_pandas()`
- This ensures compatibility with the rest of the notebook

#### Cell 14 (Code)
- **Before:** Loading from local README files to check licenses
- **After:**
  ```python
  import json

  # Download the CC-BY 4.0 licensed tasks
  tasks_with_cc_by_license = []
  for task in tqdm(TASKS):
      data = datasets.load_dataset("nguha/legalbench", task, split="train")
      if data.info.license == "CC BY 4.0":
          tasks_with_cc_by_license.append(task)

  print()
  print(tasks_with_cc_by_license)
  ```

## Verification

### Test 1: Basic Dataset Loading
Created and executed `/Users/laurentwiesel/Dev/S-C/legalbench/test_dataset_loading.py`
- Successfully loaded `abercrombie` dataset from HuggingFace
- Verified both train (5 samples) and test (95 samples) splits

### Test 2: Complete Notebook Workflow
Created and executed `/Users/laurentwiesel/Dev/S-C/legalbench/test_notebook_workflow.py`
- Verified task organization (162 total tasks, 17 issue tasks)
- Verified dataset loading from HuggingFace
- Verified prompt generation (95 prompts)
- Verified evaluation functionality
- Verified correct datasets version (2.19.0)

**All tests passed successfully!**

## Current Environment
- **Working directory:** `/Users/laurentwiesel/Dev/S-C/legalbench`
- **Virtual environment:** `/Users/laurentwiesel/Dev/S-C/legalbench/.venv`
- **Package manager:** `uv`
- **datasets version:** 2.19.0
- **pyarrow version:** 22.0.0 (compatible with datasets 2.19.0)

## Files Modified
1. `/Users/laurentwiesel/Dev/S-C/legalbench/UsingLegalBench.ipynb`
2. `/Users/laurentwiesel/Dev/S-C/legalbench/pyproject.toml`

## Files Created (for testing)
1. `/Users/laurentwiesel/Dev/S-C/legalbench/test_dataset_loading.py`
2. `/Users/laurentwiesel/Dev/S-C/legalbench/test_notebook_workflow.py`

## Next Steps
The notebook is now fully functional and can be used to:
1. Load any LegalBench task from HuggingFace
2. Generate prompts using task-specific templates
3. Evaluate model predictions
4. Filter tasks by license

## Note
When running the notebook, you may see a `FutureWarning` about `trust_remote_code=True`. This is expected for datasets with custom loading scripts and does not affect functionality. In future versions of the datasets library (3.x+), you'll need to add `trust_remote_code=True` to the `load_dataset()` calls.
