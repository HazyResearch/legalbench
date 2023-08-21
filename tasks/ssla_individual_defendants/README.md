# ssla_plaintiff

### Extract the identities of individual defendants from excerpts of securities class action complaints.
---


**Source**: [SSLA](https://sla.law.stanford.edu/)

**License**: [CC by 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 1016

**Legal reasoning type**: Interpretation

**Task type**: Extraction

## Task description 

This task requires the LLM to extract the identities of individual defendants from excerpts of securities class action complaints.

LLM outputs should be evaluated by comparing the extracted names to the ground truth. We recommend using `fuzz.partial_ratio` from the [fuzz](https://github.com/seatgeek/thefuzz) library, with a similarity score >= 80 constituting a correct answer (if a plaintiff is mentioned).


## Dataset construction

This task was constructed by hand, using the process described on the SSLA website.

## Data column names

- `answer`: individual defendants
- `text`: excerpt from complaint