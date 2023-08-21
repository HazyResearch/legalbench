# supply_chain_disclosure_best_practice_accountability

### Given a supply chain disclosure, determine if the statement discloses whether the retail seller or manufacturer maintains internal compliance procedures on company standards regarding human trafficking and slavery.
---



**Source**: Adam Chilton & Galit Sarfaty

**License**: [CC by 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 387

**Legal reasoning type**: Interpretation

**Task type**: Binary classification

## Task description

This is a binary classification task in which the LLM must determine if a supply chain disclosure meets the following coding criteria.

```text
Does the above statement disclose whether the retail seller or manufacturer maintains internal compliance procedures on company standards regarding human trafficking and slavery? This includes any type of internal accountability mechanism. Requiring independently of the supply to comply with laws does not qualify or asking for documentary evidence of compliance does not count either. 
```

## Task construction

This task was constructed by manually coding supply chain disclosures.

## Data column names
 
- `answer`: answer to coding
- `text`: supply disclosure