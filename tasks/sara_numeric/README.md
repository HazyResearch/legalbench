# statutory_reasoning_assessment

### Given a statute and a set of facts, determine how much tax an individual owes.
---



**Source**: <https://nlp.jhu.edu/law/>

**License**: MIT

**Size (samples)**: 100

**Legal reasoning type**: Interpretation

**Task type**: Binary classification

## Task description

The StAtutory Reasoning Assessment (SARA) dataset tests the ability to reason about summaries of facts and statutes, in the context of US federal tax law. SARA contains a set of statutes, and summaries of facts (cases) paired with a numerical question. These questions asks how much tax one of the protagonists in the case owes.

## Task construction

For information on task construction, see the [original paper](https://ceur-ws.org/Vol-2645/paper5.pdf). This task is built off of the [second version of the dataset](https://nlp.jhu.edu/law/#SARA_v2).

Note: The original dataset contains both entailment prompts, and numerical questions which require computing the amount of tax owed. This task contains just the numerical questions, and the `sara_entailment` task contains the entailment prompts. 

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

## Data column names

- **case id**: A unique string identifier for the case.
- **statute**: The snippet from the statutes that is the most relevant to the question. For numerical cases, that's the entirety of the statutes.
- **description**:  The summary of facts from the case description.
- **question**: The question or entailment prompt.
- **text**:  The concatenation of statute, description and question. This is meant as the input to the LM, as per the LegalBench format. In some cases, this might exceed the context window of the LM, in which case I would recommend truncating from the left.
- **label**: The answer to the question or entailment problem. Answers to questions are dollar amounts, answers to entailment problems are either "Entailment" or "Contradiction".

