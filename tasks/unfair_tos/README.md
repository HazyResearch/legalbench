# unfair_tos

### Given a clause from a terms-of-service contract, determine the category the clause belongs to.
---



**Source**: [Claudette](https://arxiv.org/abs/1805.01217)

**License**: [CC by 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 3850

**Legal reasoning type**: Interpretation

**Task type**: 8-way classification

## Task description

The purpose of this task is classifying clauses in Terms of Service agreements. Clauses have been annotated by into nine categories: `['Arbitration', 'Unilateral change', 'Content removal', 'Jurisdiction', 'Choice of law', 'Limitation of liability', 'Unilateral termination', 'Contract by using', 'Other']`. The first eight categories correspond to clauses that would potentially be deemed *potentially unfair*. The last category (`Other`) corresponds to clauses in agreements which don't fit into these categories. A description of the precise annotation guidelines can be found in the original paper.

## Task construction

Our data is composed of clauses from the validation and test split of [LexGlue](https://arxiv.org/abs/2110.00976) version of this task. We removed all clauses for which multiple annotations were available.

## Citation information
If you use this dataset, we ask that you also cite to the source of the data as well.

```bib
@article{lippi2019claudette,
  title={CLAUDETTE: an automated detector of potentially unfair clauses in online terms of service},
  author={Lippi, Marco and Pa{\l}ka, Przemys{\l}aw and Contissa, Giuseppe and Lagioia, Francesca and Micklitz, Hans-Wolfgang and Sartor, Giovanni and Torroni, Paolo},
  journal={Artificial Intelligence and Law},
  volume={27},
  pages={117--139},
  year={2019},
  publisher={Springer}
}
```

## Data column names

- `text`: a contractual clause
- `label`: clause category