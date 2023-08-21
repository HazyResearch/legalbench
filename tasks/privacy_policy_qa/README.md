# privacy_policy_qa

### Given a question and a clause from a privacy policy, determine if the clause contains enough information to answer the question.
---


**Source**: [Privacy Q&A Corpus](https://github.com/AbhilashaRavichander/PrivacyQA_EMNLP)

**License**: [MIT](https://github.com/AbhilashaRavichander/PrivacyQA_EMNLP/blob/master/LICENSE)

**Size (samples)**: 10992

**Legal reasoning type**: Interpretation

**Task type**: Binary classification

## Task description

This is a binary classification task in which the LLM is provided with a question (e.g., "do you publish my data") and a clause from a privacy policy. The LLM must determine if the clause contains an answer to the question, and classify the question-clause pair as `Relevant` or `Irrelevant`.  

## Task construction

This task was constructed from the test split of the [PrivacyQA](https://github.com/AbhilashaRavichander/PrivacyQA_EMNLP) dataset. Please see the [original paper](https://arxiv.org/abs/1911.00841) for more details.

## Citation information
If you use this dataset, we ask that you also cite to the source of the data as well.

```bib
@article{ravichander2019question,
  title={Question answering for privacy policies: Combining computational and legal perspectives},
  author={Ravichander, Abhilasha and Black, Alan W and Wilson, Shomir and Norton, Thomas and Sadeh, Norman},
  journal={arXiv preprint arXiv:1911.00841},
  year={2019}
}
```

## Data column names

- `question`: question
- `text`: clause
- `answer`: whether or not the clause is relevant