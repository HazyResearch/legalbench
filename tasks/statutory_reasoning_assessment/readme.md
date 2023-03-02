# StAtutory Reasoning Assessment (SARA) dataset

**Contributor**: Nilz Holzenberg

**Source**: <https://nlp.jhu.edu/law/>

**License**:

## Task Description

The StAtutory Reasoning Assessment (SARA) dataset tests the ability to reason about summaries of facts and statutes, in the context of US federal tax law. SARA contains a set of statutes, and summaries of facts (cases) paired with a question or an entailment prompt. An entailment prompt asks about a specific section of the SARA statutes. A question asks how much tax one of the protagonists in the case owes.

## Task Construction

For information on task construction, see the [original paper](https://ceur-ws.org/Vol-2645/paper5.pdf).

## Description of Headers

- **case id**: A unique string identifier for the case.
- **statute**: The snippet from the statutes that is the most relevant to the question. For numerical cases, that's the entirety of the statutes.
- **description**:  The summary of facts from the case description.
- **question**: The question or entailment prompt.
- **text**:  The concatenation of statute, description and question. This is meant as the input to the LM, as per the LegalBench format. In some cases, this might exceed the context window of the LM, in which case I would recommend truncating from the left.
- **label**: The answer to the question or entailment problem. Answers to questions are dollar amounts, answers to entailment problems are either "Entailment" or "Contradiction".
