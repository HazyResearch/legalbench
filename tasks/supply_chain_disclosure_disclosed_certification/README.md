# supply_chain_disclosure_disclosed_certification

### Given a supply chain disclosure, determine if the statement discloses to what extent, if any, that the retail seller or manufacturer requires direct suppliers to certify that materials incorporated into the product comply with the laws regarding slavery and human trafficking of the country or countries in which they are doing business.
---



**Source**: Adam Chilton & Galit Sarfaty

**License**: [CC by 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 386

**Legal reasoning type**: Interpretation

**Task type**: Binary classification

## Task description

This is a binary classification task in which the LLM must determine if a supply chain disclosure meets the following coding criteria.

```text
Does the above statement disclose to what extent, if any, that the retail seller or manufacturer requires direct suppliers to certify that materials incorporated into the product comply with the laws regarding slavery and human trafficking of the country or countries in which they are doing business?
```

## Task construction

This task was constructed by manually coding supply chain disclosures.

## Data column names
 
 - `answer`: answer to coding
 - `text`: supply disclosure