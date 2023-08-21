# privacy_policy_entailment

### Given a privacy policy clause and a description of the clause, determine if the description is correct.
---


**Source**: [APP-350 Corpus](https://github.com/AbhilashaRavichander/PrivacyQA_EMNLP)

**License**: [CC BY-NC 3.0](https://creativecommons.org/licenses/by-nc/3.0/)

**Size (samples)**: 4385

**Legal reasoning type**: Interpretation

**Task type**: Binary classification

## Task description

This is a binary classification task in which the LLM is provided with a clause from a privacy policy, and a description of that clause (e.g., "The policy describes collection of the user's HTTP cookies, flash cookies, pixel tags, or similar identifiers by a party to the contract."). The LLM must determine if description of the clause is `Correct` or `Incorrect`.

## Task construction

This task was constructed from the test split of the [APP-350](https://usableprivacy.org/static/files/popets-2019-maps.pdf) dataset. Please see the original paper for more details.

## Citation information
If you use this dataset, we ask that you also cite to the source of the data as well.

```bib
@article{zimmeck2019maps,
  title={Maps: Scaling privacy compliance analysis to a million apps},
  author={Zimmeck, Sebastian and Story, Peter and Smullen, Daniel and Ravichander, Abhilasha and Wang, Ziqi and Reidenberg, Joel R and Russell, N Cameron and Sadeh, Norman},
  journal={Proc. Priv. Enhancing Tech.},
  volume={2019},
  pages={66},
  year={2019}
}
```

## Data column names

- `text`: privacy policy clause
- `description`: description of the clause
- `answer`: whether the description correctly summarizes the clause