# citation_prediction_classification

### Given a legal statement and a case citation, determine if the citation is supportive of the legal statement.
---



**Source**: Michael Livermore, Daniel N. Rockmore

**License**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 110

**Legal reasoning type**: Rule-recall

**Task type**: Binary classification

## Task description

This task evaluates the extent to which a LLM can determine if a case is supportive of a particular sentence.

## Task construction

We gathered a sample of circuit court opinions published after January 1, 2023. From each opinion, we identified sentences where the following criteria were mere:

1. The sentence was followed by a citation to a single judicial opinion. We ignored instances where a single case was offered as support, but a parenthetical indicated the case was citing or quoting another.
2. The sentence was entirely or contained part of quotation.

We selected these sentences in order to minimize the chance of selecting sentences for which a court could have pointed towards a broad range of cases as authoratively supportive. After collecting (sentence, citation) pairs, we constructed negative samples by pairing sentences with citations associated with other sentences.

**Note**: we expect this task to be less informative for models trained on text data for 2023. However, the process of creating this task data is straightforward, so we believe it can be replicated on newly released opinions for newer models.

## Files

- `train.tsv`: contains samples to be used as in-context demonstrations
- `test.tsv`: contains the evaluation set
- `base_prompt.txt`: a few-shot prompt that can be used to perform this task

## Data column names

In `train.tsv` and `test.tsv`, column names correspond to the following:

- `index`: sample identifier
- `text`: sentence from a judicial opinion
- `citation`: the citation for a case (case name only)
- `answer`: whether or not the citation is actually supportive of the sentence. Options: Yes, No.
