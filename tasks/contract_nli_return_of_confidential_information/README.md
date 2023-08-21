# contract_nli_return_of_confidential_information

### Identify if the clause provides that the Receiving Party shall destroy or return some Confidential Information upon the termination of Agreement.
---



**Source**: [ContractNLI](https://stanfordnlp.github.io/contract-nli/)

**License**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 74

**Legal reasoning type**: Interpretation

**Task type**: Binary classification

## Task description

This task is a subset of ContractNLI, and consists of determinining whether a clause from an NDA has a particular legal effect.

## Task construction

This task was constructed from the ContractNLI dataset, which originally annotated clauses from NDAs based on whether they entailed, contradicted, or neglgected to mention a hypothesis. We binarized this dataset, treating contradictions and failures to mention as the negative label. We used the hypothesis provided as the prompt. Please see the original paper for more information on construction. All samples are drawn from the test set.

## Citation information

If you use this dataset, we ask that you also cite to the source of the data as well.

```bib
@article{koreeda2021contractnli,
  title={ContractNLI: A dataset for document-level natural language inference for contracts},
  author={Koreeda, Yuta and Manning, Christopher D},
  journal={arXiv preprint arXiv:2110.01799},
  year={2021}
}
```

## Files

- `train.tsv`: contains samples to be used as in-context demonstrations
- `test.tsv`: contains the evaluation set
- `base_prompt.txt`: a few-shot prompt that can be used to perform this task

## Data column names

In `train.tsv` and `test.tsv`, column names correspond to the following:
- `index`: sample identifier
- `document_name`: name of document in original dataset
- `text`: excerpt from a contract
- `answer`: `Yes` if the clause provides that the Receiving Party shall destroy or return some Confidential Information upon the termination of Agreement, and `No` otherwise.