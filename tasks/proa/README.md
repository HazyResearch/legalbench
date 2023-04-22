# proa 
 **Contributor**: Neel Guha (nguha@stanford.edu)
 
 **Source**: Neel Guha
 
 **License**: [CC by 4.0](https://creativecommons.org/licenses/by/4.0/)
 
 **Task summary**: Classify if a statute contains a private right of action.
 
 **Size (samples)**: 100
 
 ## Task Description
 
 A private right of action (PROA) exists when a statute empowers an ordinary individual (i.e., a private person) to legally enforce their rights by bringing an action in court. In short, a PROA creates the ability for an individual to sue someone in order to recover damages or halt some offending conduct. PROAs are ubiquitous in antitrust law (in which individuals harmed by anti-competitive behavior can sue offending firms for compensation) and environmental law (in which individuals can sue entities which release hazardous substances for damages).  
 
 ## Dataset construction
 
 We construct a dataset of PROAs by hand, drawing inspiration from clauses found in different state codes. We construct 50 clauses which do contain a PROA, and 50 clauses which don't. 5 randomly sampled clauses constitute the training set, and the remaining 95 form the test set.
 
 ## Column names
 
 - `text`: a statutory clause
 - `label`: whether the clause contains a private right ("Yes") or not ("No")