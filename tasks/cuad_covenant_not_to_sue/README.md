# cuad_covenant_not_to_sue

### Classify if the clause specifies that a party is restricted from contesting the validity of the counterparty’s ownership of intellectual property or otherwise bringing a claim against the counterparty for matters unrelated to the contract.
---



**Source**: [Atticus Project](https://www.atticusprojectai.org/cuad>)

**License**: [CC By 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 314

**Legal reasoning type**: Interpretation

**Task type**: Binary classification

## Task description

This is a binary classification task in which the model must determine if a contractual clause falls under the category of "Covenant Not To Sue".

## Task construction

This task was constructed from the [CUAD dataset](https://www.atticusprojectai.org/cuad), which annotated clauses in 500 contracts according to 41 types. Positive samples for this task correspond to clauses for which annotators answered the following question in the affirmative:

```text
Is a party restricted from contesting the validity of the counterparty’s ownership of intellectual property or otherwise bringing a claim against the counterparty for matters unrelated to the contract?
```

Negative samples are randomly selected from other clauses.

## Citation information
If you use this dataset, we ask that you also cite to the source of the data as well.

```bib
@article{hendrycks2021cuad,
  title={Cuad: An expert-annotated nlp dataset for legal contract review},
  author={Hendrycks, Dan and Burns, Collin and Chen, Anya and Ball, Spencer},
  journal={arXiv preprint arXiv:2103.06268},
  year={2021}
}
```

## Data column names

- `answer`: whether the clause is an instance of the type ("Yes") or not ("No")
- `text`: text of contractual clause
- 'document_name`: name of document in original dataset containing clause