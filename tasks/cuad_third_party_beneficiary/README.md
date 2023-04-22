# cuad_third_party_beneficiary 
 **Contributor**: Neel Guha (nguha@stanford.edu)
 
 **Source**: [Atticus Project](https://www.atticusprojectai.org/cuad>)
 
 **License**: [CC By 4.0](https://creativecommons.org/licenses/by/4.0/)
 
 **Task summary**: Does the clause specify that that there a non-contracting party who is a beneficiary to some or all of the clauses in the contract and therefore can enforce its rights against a contracting party?
 
 **Size (samples)**: 76
 
 ## Task Description
 
 This is a binary classification task in which the model must determine if a contractual clause falls under the category of "Third Party Beneficiary".
 
 ## Task Construction
 
 This task was constructed from the [CUAD dataset](https://www.atticusprojectai.org/cuad), which annotated clauses in 500 contracts according to 41 types. Positive samples for this task correspond to clauses for which annotators answered the following question in the affirmative:
 
 ```text
 Does the clause specify that that there a non-contracting party who is a beneficiary to some or all of the clauses in the contract and therefore can enforce its rights against a contracting party?
 ```
 
 Negative samples are randomly selected from other clauses.
 
 ## Column names
 
 - `label`: whether the clause is an instance of the type ("Yes") or not ("No")
 - `text`: text of contractual clause