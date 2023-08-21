# supply_chain_disclosure_disclosed_audits

### Given a disclosure, determine whether the statement discloses to what extent, if any, that the retail seller or manufacturer conducts audits of suppliers to evaluate supplier compliance with company standards for trafficking and slavery in supply chains.
---



**Source**: Adam Chilton & Galit Sarfaty

**License**: [CC by 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 387

**Legal reasoning type**: Interpretation

**Task type**: Binary classification

## Task description

This is a binary classification task in which the LLM must determine if a supply chain disclosure meets the following coding criteria.

```text
Does the above statement disclose to what extent, if any, that the retail seller or manufacturer conducts audits of suppliers to evaluate supplier compliance with company standards for trafficking and slavery in supply chains? The disclosure shall specify if the verification was not an independent, unannounced audit.
```

## Task construction

This task was constructed by manually coding supply chain disclosures.

## Data column names
 
 - `answer`: answer to coding
 - `text`: supply disclosure