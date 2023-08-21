# supply_chain_disclosure_best_practice_training

### Given a supply chain disclosure, determine if the statement discloses whether the retail seller or manufacturer  provides training to employees on human trafficking and slavery.
---



**Source**: Adam Chilton & Galit Sarfaty

**License**: [CC by 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 387

**Legal reasoning type**: Interpretation

**Task type**: Binary classification

## Task description

This is a binary classification task in which the LLM must determine if a supply chain disclosure meets the following coding criteria.

```text
Does the above statement disclose whether the retail seller or manufacturer  provides training to employees on human trafficking and slavery? Broad policies such as ongoing dialogue on mitigating risks of human trafficking and slavery or increasing managers and purchasers knowledge about health, safety and labor practices qualify as training. Providing training to contractors who failed to comply with human trafficking laws counts as training. 
```

## Task construction

This task was constructed by manually coding supply chain disclosures.

## Data column names
 
 - `answer`: answer to coding
 - `text`: supply disclosure