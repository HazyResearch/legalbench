# contract_qa

### Answer yes/no questions about whether contractual clauses discuss particular issues.
---

-Rahe, Aditya Narayana, and Dmitry Talisman

**Source**: Nikon Rasumov-Rahe, Aditya Narayana, and Dmitry Talisman

**License**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 88

**Legal reasoning type**: Interpretation

**Task type**: Binary classification

## Task description

This is a binary classification task where the LLM must determine if language from a contract contains a particular type of content. Unlike other contractual clause classification tasks in LegalBench, this task covers multiple distinct types of contant. As the prompt only provides examples of some clauses, the LLM is required to identify clause types for which it in-context demonstrations have not been provided. This task encompasses the following questions:

- Does the clause describe confidentiality requirements?
- Does the clause discuss BIPA consent?
- Does the clause discuss CIPA policy?
- Does the clause discuss PII data breaches?
- Does the clause discuss arbitration?
- Does the clause discuss breach of contract?
- Does the clause discuss choice of law governing the contract?
- Does the clause discuss compliance with California consumer privacy law?
- Does the clause discuss compromised user credentials?
- Does the clause discuss dispute resolution?
- Does the clause discuss how disputes may be escalated?
- Does the clause discuss inadvertent disclosures of personal information?
- Does the clause discuss personal indemnification?
- Does the clause discuss the American with Disabilities Act (ADA) compliance?
- Does the clause waive confidentiality?
- Does the clause waive damages?
- Is this a Force Majeure clause?
- Is this a non-compete clause?
- Is this a severability clause?
- Is this a termination clause?

## Task construction

This task was constructed by manual annotating a sample of contracts.

## Files

- `train.tsv`: contains samples to be used as in-context demonstrations
- `test.tsv`: contains the evaluation set
- `base_prompt.txt`: a few-shot prompt that can be used to perform this task

## Data column names

In `train.tsv` and `test.tsv`, column names correspond to the following:
- `index`: sample identifier
- `text`: excerpt from a contract
- `question`: a question about the content of the excerpt
- `answer`: the answer to the question. The choices are `Yes` or `No`.