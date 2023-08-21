---
layout: default
title: sara_entailment
parent: Tasks
---
# sara_entailment

### Given a statute, a fact pattern, and an assertion, determine if the assertion is "entailed" by the fact pattern and statute.
---



**Source**: <https://nlp.jhu.edu/law/>

**License**: MIT

**Size (samples)**: 277

**Legal reasoning type**: Interpretation

**Task type**: Binary classification

## Task description

The StAtutory Reasoning Assessment (SARA) dataset tests the ability to reason about summaries of facts and statutes, in the context of US federal tax law. SARA contains a set of statutes, and summaries of facts (cases) paired with an entailment prompt. An entailment prompt asks about a specific section of the SARA statutes. 

## Task construction

For information on task construction, see the [original paper](https://ceur-ws.org/Vol-2645/paper5.pdf). This task is built off of the [second version of the dataset](https://nlp.jhu.edu/law/#SARA_v2).

Note: The original dataset contains both entailment prompts, and numerical questions which require computing the amount of tax owed. This task contains just the entailment instances, and the `sara_numeric` task contains the numerical questions. 

## Citation information
If you use this dataset, we ask that you also cite to the source of the data as well.

```bib
@article{holzenberger2021factoring,
  title={Factoring statutory reasoning as language understanding challenges},
  author={Holzenberger, Nils and Van Durme, Benjamin},
  journal={arXiv preprint arXiv:2105.07903},
  year={2021}
}
```

