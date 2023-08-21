# overruling 

### Classify whether a sentence from a judicial opinion overrules a previous case.
---


**Source**: [CaseHOLD](https://github.com/reglab/casehold)

**License**: [CC By 4.0](https://creativecommons.org/licenses/by/4.0/)

**Task summary**: Classify whether a sentence overrules a previous case.

**Size (samples)**: 2400

**Legal reasoning type**: Rhetorical-analysis

**Task type**: Binary classification

## Task description

This task consists of classifying whether or not a particular sentence of case law overturns the decision of a previous case.

## Dataset construction

This dataset consists of sentences derived from US caselaw and manually annotated as to whether they overrule a previous case. See the original [CaseHOLD](https://arxiv.org/abs/2104.08671) paper for more information.

## Citation information
If you use this dataset, we ask that you also cite to the source of the data as well.

```bib
@inproceedings{zheng2021does,
  title={When does pretraining help? assessing self-supervised learning for law and the casehold dataset of 53,000+ legal holdings},
  author={Zheng, Lucia and Guha, Neel and Anderson, Brandon R and Henderson, Peter and Ho, Daniel E},
  booktitle={Proceedings of the eighteenth international conference on artificial intelligence and law},
  pages={159--168},
  year={2021}
}
```

## Data column names

- `label`: whether or not the sentence overrules a previous decision
- `text`: a sentence from a judicial opinion