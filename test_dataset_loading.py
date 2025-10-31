#!/usr/bin/env python3
"""
Test script to verify that datasets library can load LegalBench from HuggingFace.
"""
from termcolor import cprint
import datasets

def main():
    cprint("Testing HuggingFace dataset loading...", "cyan", attrs=["bold"])

    try:
        # Suppress progress bars for cleaner output
        datasets.utils.logging.set_verbosity_error()

        cprint("\n[1/3] Loading abercrombie dataset from HuggingFace...", "cyan")
        data = datasets.load_dataset("nguha/legalbench", "abercrombie")

        cprint(f"[SUCCESS] Loaded dataset with splits: {list(data.keys())}", "green", attrs=["bold"])

        cprint(f"\n[2/3] Checking train split...", "cyan")
        train_data = data["train"]
        cprint(f"[SUCCESS] Train split has {len(train_data)} samples", "green", attrs=["bold"])

        cprint(f"\n[3/3] Checking test split...", "cyan")
        test_data = data["test"]
        cprint(f"[SUCCESS] Test split has {len(test_data)} samples", "green", attrs=["bold"])

        cprint("\n" + "="*60, "green")
        cprint("ALL TESTS PASSED!", "green", attrs=["bold"])
        cprint("="*60, "green")
        cprint(f"\nDatasets library version: {datasets.__version__}", "yellow")
        cprint(f"Dataset splits available: {list(data.keys())}", "yellow")
        cprint(f"Train samples: {len(train_data)}", "yellow")
        cprint(f"Test samples: {len(test_data)}", "yellow")

        return True

    except Exception as e:
        cprint("\n" + "="*60, "red")
        cprint("TEST FAILED!", "red", attrs=["bold"])
        cprint("="*60, "red")
        cprint(f"\nError: {str(e)}", "red")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
