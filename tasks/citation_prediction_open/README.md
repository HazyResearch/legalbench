# citation_prediction_open

### Given a legal statement, predict the name of the case which best supports the statement.
---



**Source**: Michael Livermore, Daniel N. Rockmore

**License**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 55

**Legal reasoning type**: Rule-recall

**Task type**: Open generation

## Task description

This task evaluates the extent to which a LLM can provide the "best" case which supports a sentence as a citation. Here, "best" is defined as the citation a federal court elected to use for the associated sentence.

## Task construction

We gathered a sample of circuit court opinions published after January 1, 2023. From each opinion, we identified sentences where the following criteria were mere:

1. The sentence was followed by a citation to a single judicial opinion. We ignored instances where a single case was offered as support, but a parenthetical indicated the case was citing or quoting another.
2. The sentence was entirely or contained part of quotation.

We selected these sentences in order to minimize the chance of selecting sentences for which a court could have pointed towards a broad range of cases as authoratively supportive. When collecting sentences, we also recorded the federal circuit for the opinion, as courts prefer to cite within their own circuit.

**Note**: we expect this task to be less informative for models trained on text data for 2023. However, the process of creating this task data is straightforward, so we believe it can be replicated on newly released opinions for newer models.

## Files

- `train.tsv`: contains samples to be used as in-context demonstrations
- `test.tsv`: contains the evaluation set
- `base_prompt.txt`: a few-shot prompt that can be used to perform this task

## Data column names

In `train.tsv` and `test.tsv`, column names correspond to the following:

- `index`: sample identifier
- `text`: sentence from a judicial opinion
- `circuit`: the circuit from which the opinion was taken
- `answer`: the case name which supports the sentence
