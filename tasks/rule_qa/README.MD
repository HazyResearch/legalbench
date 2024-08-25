# rule_qa 

### Answer questions about federal and state law.
---
**Contributor**: Neel Guha

**Source**: Neel Guha

**License**: [CC by 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 50

**Legal reasoning type**: Rule-recall

**Task type**: Generation

## Task Description

Rule QA is a question-answer task in which the model is asked about laws. Questions span asking the model to state the formulations for different legal rules (e.g., the rule for hearsay), identify where laws are codified, and general questions about doctrine.

## Dataset construction

We constructed this dataset by hand. For each sample, we provide the area of law it relates to (e.g. Civil Procedure).

**Note**: This task is intended to be evaluated in a zero-shot setting. As a result, `train.tsv` is intentionally blank.

## Data column names

- `text`: a question pertaining to a part of the law
- `answer`: an acceptable answer to the question
- `doctrine`: the area of law the question pertains to
