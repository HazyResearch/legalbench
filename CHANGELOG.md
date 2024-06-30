# Changelog

This file tracks all changes and updates to LegalBench data.

## June 30, 2024

- We have removed the `train.tsv` files for `scalr` and `rule_qa`. Both these tasks were intended to be zero-shot and hence have no samples in their `train.tsv` files. We have removed these files to avoid any confusion.
- We noticed an error in `unfair_tos` whereby labels were not correctly assigned for some samples. We have fixed this issue and uploaded a new version of the data with corrected labels.
