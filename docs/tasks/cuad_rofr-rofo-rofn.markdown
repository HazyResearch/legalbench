---
layout: default
title: cuad_rofr-rofo-rofn
parent: Tasks
---
# cuad_rofr-rofo-rofn

### Classify if the clause grant one party a right of first refusal, right of first offer or right of first negotiation to purchase, license, market, or distribute equity interest, technology, assets, products or services.
---



**Source**: [Atticus Project](https://www.atticusprojectai.org/cuad>)

**License**: [CC By 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 696

**Legal reasoning type**: Interpretation

**Task type**: Binary classification

## Task description

This is a binary classification task in which the model must determine if a contractual clause falls under the category of "Rofr/Rofo/Rofn".

## Task construction

This task was constructed from the [CUAD dataset](https://www.atticusprojectai.org/cuad), which annotated clauses in 500 contracts according to 41 types. Positive samples for this task correspond to clauses for which annotators answered the following question in the affirmative:

```text
Does the clause grant one party a right of first refusal, right of first offer or right of first negotiation to purchase, license, market, or distribute equity interest, technology, assets, products or services?
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

