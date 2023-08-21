# supply_chain_disclosure_disclosed_verification

### Given a supply chain disclosure, determine if the statement discloses whether the retail seller or manufacturer engages in verification of product supply chains to evaluate and address risks of human trafficking and slavery.
---



**Source**: Adam Chilton & Galit Sarfaty

**License**: [CC by 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 387

**Legal reasoning type**: Interpretation

**Task type**: Binary classification

## Task description

This is a binary classification task in which the LLM must determine if a supply chain disclosure meets the following coding criteria.

```text
Does the above statement disclose to what extent, if any, that the retail seller or manufacturer engages in verification of product supply chains to evaluate and address risks of human trafficking and slavery? If the company conducts verification], the disclosure shall specify if the verification was not conducted by a third party.
```

## Task construction

This task was constructed by manually coding supply chain disclosures.

## Data column names
 
 - `answer`: answer to coding
 - `text`: supply disclosure