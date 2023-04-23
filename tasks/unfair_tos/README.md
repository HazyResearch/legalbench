# unfair_tos 
 **Contributor**: Joel Niklaus
 
 **Source**: [Claudette](https://arxiv.org/abs/1805.01217)
 
 **License**: [CC by 4.0](https://creativecommons.org/licenses/by/4.0/)
 
 **Task summary**: Classify if a terms-of-service clause is unfair.
 
 **Size (samples)**: 3850.
 
 ## Task Description
 
 The purpose of this task is classifying clauses in Terms of Service agreements. Clauses have been annotated by into nine categories: `['Arbitration', 'Unilateral change', 'Content removal', 'Jurisdiction', 'Choice of law', 'Limitation of liability', 'Unilateral termination', 'Contract by using', 'Other']`. The first eight categories correspond to clauses that would potentially be deemed *potentially unfair*. The last category (`Other`) corresponds to clauses in agreements which don't fit into these categories. A description of the precise annotation guidelines can be found in the original paper.
 
 ## Task Construction
 
 Our data is composed of clauses from the validation and test split of [LexGlue](https://arxiv.org/abs/2110.00976) version of this task. We removed all clauses for which multiple annotations were available.
 
 ## Column names
 
 - `text`: a contractual clause
 - `label`: clause category