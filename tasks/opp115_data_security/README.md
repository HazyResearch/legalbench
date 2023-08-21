# opp115_data_security

### Given a clause from a privacy policy, classify if the clause describes how user information is protected.
---



**Source**: [OPP-115](https://usableprivacy.org/data)

**License**: Creative Commons Attribution-NonCommercial License

**Size (samples)**: 1342

**Legal reasoning type**: Interpretation

**Task type**: Binary classification

## Task description

This is a binary classification task in which the LLM must answer the following annotation intent for clauses in privacy policies.

```text
Does the clause describe how user information is protected?
```

## Task construction

This task was constructed from the [OPP-115 dataset](https://usableprivacy.org/data). Please see the [original paper](https://usableprivacy.org/static/files/swilson_acl_2016.pdf) for more details on construction. This dataset is class balanced.

## Citation information
If you use this dataset, we ask that you also cite to the source of the data as well.

```bib
@inproceedings{wilson2016creation,
  title={The creation and analysis of a website privacy policy corpus},
  author={Wilson, Shomir and Schaub, Florian and Dara, Aswarth Abhilash and Liu, Frederick and Cherivirala, Sushain and Leon, Pedro Giovanni and Andersen, Mads Schaarup and Zimmeck, Sebastian and Sathyendra, Kanthashree Mysore and Russell, N Cameron and others},
  booktitle={Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  pages={1330--1340},
  year={2016}
}
```

## Data column names
- `text`: clause from privacy policy
- `answer`: answer the annotation intent above as applied to the clause (Yes/No)