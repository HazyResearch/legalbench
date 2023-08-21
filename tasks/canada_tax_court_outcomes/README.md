# canada_tax_court_outcomes

### Classify whether an excerpt from a Canada Tax Court decision includes the outcome of the appeal, and if so, specify whether the appeal was allowed or dismissed.
---



**Source**: Sean Rehaag

**License**: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

**Size (samples)**: 250

**Legal reasoning type**: Rhetorical-analysis

**Task type**: 3-way classification

## Task description

The input is an excerpt of text from Tax Court of Canada decisions involving appeals of tax related matters. The task is to classify whether the excerpt includes the outcome of the appeal, and if so, to specify whether the appeal was allowed or dismissed. Partial success (e.g. appeal granted on one tax year but dismissed on another) counts as allowed (with the exception of costs orders which are disregarded). Where the excerpt does not clearly articulate an outcome, the system should indicate other as the outcome. Categorizing case outcomes is a common task that legal researchers complete in order to gather datasets involving outcomes in legal processes for the purposes of quantitative empirical legal research.

## Task construction

Decisions were scraped from the Tax Court of Canada website (subject to a non-commercial use with attribution license): <https://decision.tcc-cci.gc.ca/tcc-cci/en/nav.do> The decisions were then parsed to get brief excerpts that are likely to include the outcome. TCC decisions frequently include a header that summarizes the decision. Where that was available in a decision, that was selected as the excerpt. Where that was not available, the first 2500 characters and last 2500 characters in the decision were selected, as outcomes are typically included in those sections. The desired outputs for each case in the selection were manually gathered and verified. Note that while a proposed prompt is below, further prompt engineering and experimentation may be worthwhile depending on what type of model is used for this task (especially for zero shot).

## Files

- `train.tsv`: contains samples to be used as in-context demonstrations
- `test.tsv`: contains the evaluation set
- `base_prompt.txt`: a few-shot prompt that can be used to perform this task

## Data column names

In `train.tsv` and `test.tsv`, column names correspond to the following:

- `index`: sample identifier
- `answer`: the outcome for the case. There are three options: allowed, dismissed, other
- `text`: excerpt from the case
