# intra_rule_distinguishing 
 **Contributor**: Neel Guha (nguha@stanford.edu)
 
 **Source**: Neel Guha
 
 **License**: [CC by 4.0](https://creativecommons.org/licenses/by/4.0/)
 
 **Task summary**: Determine which LegalBench issue is implicated in a certain fact pattern (meta-task).
 
 **Size (samples)**: 60
 
 ## Task Description
 
 Intra-rule distinguishing evaluates whether a LLM can identify the legal rule implicated by a fact pattern. 
 
 ## Task Construction
 
 We selected fact patterns from the personal jurisdiction, hearsay, and abercrombie tasks. For each sample, the name of the original task is treated as the label to predict.
 
 
 ## Column names
 
 - `label`: the type of legal question implicated
 - `text`: a fact pattern from a LegalBench task