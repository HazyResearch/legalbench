# supply_chain_disclosure_best_practice_verification

### Given a supply chain disclosure, determine if the statement discloses whether the retail seller or manufacturer engages in verification and auditing as one practice, expresses that it may conduct an audit, or expressess that it is assessing supplier risks through a review of the US Dept. of Labor's List.
---



**Source**: Adam Chilton & Galit Sarfaty

**License**: [CC by 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 387

**Legal reasoning type**: Interpretation

**Task type**: Binary classification

## Task description

This is a binary classification task in which the LLM must determine if a supply chain disclosure meets the following coding criteria.

```text
Does the above statement disclose whether the retail seller or manufacturer engages in verification and auditing as one practice, expresses that it may conduct an audit, or expressess that it is assessing supplier risks through a review of the US Dept. of Labor's List?
```

## Task construction

This task was constructed by manually coding supply chain disclosures.

## Data column names
 
 - `answer`: answer to coding
 - `text`: supply disclosure