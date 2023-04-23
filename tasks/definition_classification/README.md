# definition_classification 
 **Contributor**: Kevin Tobia
 
 **Source**: Kevin Tobia
 
 **License**: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
 
 **Task summary**: Extract the term being defined in sentences from Supreme Court opinions.
 
 **Size (samples)**: 1346
 
 ## Task Description
 
 Courts frequently define terms in the course of interpreting and applying laws. For instance, the following sentence provides a definition of the term "confidential":
 
 ```text
 The term “confidential” meant then, as it does now, “private” or “secret.” Webster's Seventh New Collegiate Dictionary 174 (1963). And here is a sentence defining “brought”: But a natural reading of § 27's text does not extend so far. “Brought” in this context means “commenced,” Black's Law Dictionary 254 (3d ed. 1933).
 ```
 
 The goal of this task is to identify if a sentence contains a definition. For example, the following sentence defines "vacation":
 
 ```text
 A vacation is defined by Bouvier to be the period of time between the end of one term and the beginning of another.
 ```
 
 ## Task Construction
 
 This task was constructed by hand-coding sentences from Supreme Court opinions.
 
 ## Column names
 
 - `text`: a sentence from an opinion
 - `label`: whether the sentence defines a term (`Yes`) or not (`No`)