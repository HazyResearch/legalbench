#!/usr/bin/env python3
"""
Comprehensive test to verify the notebook workflow works end-to-end.
Tests all the main operations from the UsingLegalBench.ipynb notebook.
"""
from termcolor import cprint
import datasets
from tasks import TASKS, ISSUE_TASKS
from utils import generate_prompts
from evaluation import evaluate
import numpy as np

def main():
    cprint("="*70, "cyan", attrs=["bold"])
    cprint("  Testing LegalBench Notebook Workflow", "cyan", attrs=["bold"])
    cprint("="*70, "cyan", attrs=["bold"])

    # Suppress progress bars
    datasets.utils.logging.set_verbosity_error()

    try:
        # Test 1: Task organization
        cprint("\n[Test 1/5] Testing task organization...", "cyan")
        cprint(f"  - Total tasks: {len(TASKS)}", "white")
        cprint(f"  - Issue tasks: {len(ISSUE_TASKS)}", "white")
        assert len(TASKS) == 162, "Expected 162 tasks"
        assert len(ISSUE_TASKS) == 17, "Expected 17 issue tasks"
        cprint("[SUCCESS] Task organization verified", "green", attrs=["bold"])

        # Test 2: Loading dataset from HuggingFace
        cprint("\n[Test 2/5] Loading dataset from HuggingFace...", "cyan")
        data = datasets.load_dataset("nguha/legalbench", "abercrombie")
        cprint(f"  - Splits available: {list(data.keys())}", "white")
        cprint(f"  - Train samples: {len(data['train'])}", "white")
        cprint(f"  - Test samples: {len(data['test'])}", "white")
        assert "train" in data, "Train split not found"
        assert "test" in data, "Test split not found"
        cprint("[SUCCESS] Dataset loaded successfully", "green", attrs=["bold"])

        # Test 3: Loading and applying prompts
        cprint("\n[Test 3/5] Testing prompt generation...", "cyan")
        with open("tasks/abercrombie/base_prompt.txt", encoding="utf-8") as f:
            prompt_template = f.read()

        test_df = data["test"].to_pandas()
        prompts = generate_prompts(prompt_template=prompt_template, data_df=test_df)
        cprint(f"  - Generated {len(prompts)} prompts", "white")
        cprint(f"  - First prompt length: {len(prompts[0])} characters", "white")
        assert len(prompts) == len(test_df), "Prompt count mismatch"
        assert len(prompts[0]) > 0, "Empty prompt generated"
        cprint("[SUCCESS] Prompts generated successfully", "green", attrs=["bold"])

        # Test 4: Evaluation
        cprint("\n[Test 4/5] Testing evaluation...", "cyan")
        classes = ["generic", "descriptive", "suggestive", "arbitrary", "fanciful"]
        generations = np.random.choice(classes, len(test_df))
        score = evaluate("abercrombie", generations, test_df["answer"].tolist())
        cprint(f"  - Evaluation score (random): {score:.4f}", "white")
        assert 0.0 <= score <= 1.0, "Score out of range"
        cprint("[SUCCESS] Evaluation completed", "green", attrs=["bold"])

        # Test 5: Dataset version check
        cprint("\n[Test 5/5] Verifying datasets library version...", "cyan")
        version = datasets.__version__
        cprint(f"  - Datasets version: {version}", "white")
        major, minor, patch = map(int, version.split('.'))
        assert major == 2, f"Expected major version 2, got {major}"
        assert minor >= 19, f"Expected minor version >= 19, got {minor}"
        cprint("[SUCCESS] Correct datasets version", "green", attrs=["bold"])

        # All tests passed
        cprint("\n" + "="*70, "green")
        cprint("  ALL TESTS PASSED!", "green", attrs=["bold"])
        cprint("="*70, "green")
        cprint("\nSummary:", "yellow", attrs=["bold"])
        cprint(f"  - Datasets version: {datasets.__version__}", "yellow")
        cprint(f"  - Total LegalBench tasks: {len(TASKS)}", "yellow")
        cprint(f"  - Test dataset loaded: abercrombie ({len(test_df)} samples)", "yellow")
        cprint(f"  - Prompts generated: {len(prompts)}", "yellow")
        cprint(f"  - Evaluation functional: Yes", "yellow")
        cprint("\nThe notebook should now work correctly!", "green", attrs=["bold"])

        return True

    except Exception as e:
        cprint("\n" + "="*70, "red")
        cprint("  TEST FAILED!", "red", attrs=["bold"])
        cprint("="*70, "red")
        cprint(f"\nError: {str(e)}", "red")
        import traceback
        cprint(f"\nTraceback:", "red")
        cprint(traceback.format_exc(), "red")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
