# cuad_price_restrictions 
 **Contributor**: Neel Guha (nguha@stanford.edu)
 
 **Source**: [Atticus Project](https://www.atticusprojectai.org/cuad>)
 
 **License**: [CC By 4.0](https://creativecommons.org/licenses/by/4.0/)
 
 **Task summary**: Does the clause place a restriction on the ability of a party to raise or reduce prices of technology, goods, or services provided?
 
 **Size (samples)**: 52
 
 ## Task Description
 
 This is a binary classification task in which the model must determine if a contractual clause falls under the category of "Price Restrictions".
 
 ## Task Construction
 
 This task was constructed from the [CUAD dataset](https://www.atticusprojectai.org/cuad), which annotated clauses in 500 contracts according to 41 types. Positive samples for this task correspond to clauses for which annotators answered the following question in the affirmative:
 
 ```text
 Does the clause place a restriction on the ability of a party to raise or reduce prices of technology, goods, or services provided?
 ```
 
 Negative samples are randomly selected from other clauses.
 
 ## Column names
 
 - `label`: whether the clause is an instance of the type ("Yes") or not ("No")
 - `text`: text of contractual clause