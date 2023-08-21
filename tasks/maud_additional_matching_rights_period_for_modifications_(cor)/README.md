# maud_additional_matching_rights_period_for_modifications_(cor)

### Read an excerpt from a merger agreement and answer: how long is the additional matching rights period for modifications in case the board changes its recommendation?
---

(zehuali@stanford.edu)

**Source**: [Atticus Project](https://www.atticusprojectai.org/maud)

**License**: [CC By 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 159

**Legal reasoning type**: Interpretation

**Task type**: 6-way classification

## Task description

This is a multiple-choice task in which the model must select the answer that best characterizes the merger agreement.

## Task construction

This task was constructed from the [MAUD dataset](https://www.atticusprojectai.org/maud), which consists of over 47,000 labels across 152 merger agreements annotated to identify 92 questions in each agreement used by the 2021 American Bar Association (ABA) [Public Target Deal Points Study](https://www.americanbar.org/groups/business_law/committees/ma/deal_points/). The task is formatted as a series of multiple-choice questions, where given a segment of the merger agreement and a Deal Point question, the model is to choose the answer that best characterizes the agreement as response.

```text
Question: Read an excerpt from a merger agreement and answer: how long is the additional matching rights period for modifications in case the board changes its recommendation?
```

```text
Options:
A: 2 business days or less
B: 3 business days
C: 3 days
D: 4 business days
E: 5 business days
F: > 5 business days
G: None
```

## Citation information
If you use this dataset, we ask that you also cite to the source of the data as well.

```bib
@article{wang2023maud,
  title={MAUD: An Expert-Annotated Legal NLP Dataset for Merger Agreement Understanding},
  author={Wang, Steven H and Scardigli, Antoine and Tang, Leonard and Chen, Wei and Levkin, Dimitry and Chen, Anya and Ball, Spencer and Woodside, Thomas and Zhang, Oliver and Hendrycks, Dan},
  journal={arXiv preprint arXiv:2301.00876},
  year={2023}
}
```

## Data column names

- `label`: answer key to the question
- `text`: segment of the merger agreement
