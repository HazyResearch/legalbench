# corporate_lobbying 

### Predict if a proposed bill is relevant to a company given information about the bill and the company.
---



**Source**: John Nay

**License**: [CC By 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 500

**Legal reasoning type**: Issue-spotting

**Task type**: Binary classification
 
## Task description
 
The Corporate Lobbying task requires an LLM to determine whether a proposed Congressional bill may be relevant to a company based on a company’s self-description in its SEC 10K filing. The following information about a bill and a company are available:

- The title of the bill.
- A summary of the bill.
- The name of the company.
- A description of the company.

We refer readers to [prior work](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0176999) for additional background on this type of task.

## Task construction

This data was manually labeled.

## Files

- `train.tsv`: contains samples to be used as in-context demonstrations
- `test.tsv`: contains the evaluation set
- `base_prompt.txt`: a few-shot prompt that can be used to perform this task

## Data column names

In `train.tsv` and `test.tsv`, column names correspond to the following:
- `index`: sample identifier
 - `bill_title`: title of bill
 - `bill_summary`: summary of bill
 - `company_name`: name of company
 - `company_description`: description of company
 - `label`: whether the bill is relevant ("Yes") or not ("No")
