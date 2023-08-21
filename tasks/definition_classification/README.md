# definition_classification 

### Given a sentence from a Supreme Court opinion, classify whether or not that sentence offers a definition of a term.
---



**Source**: Kevin Tobia

**License**: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

**Size (samples)**: 1346

**Legal reasoning type**: Rhetorical-analysis

**Task type**: Binary classification
 
## Task description
 
Courts frequently define terms in the course of interpreting and applying laws. For instance, the following sentence provides a definition of the term "confidential":

```text
The term “confidential” meant then, as it does now, “private” or “secret.” Webster's Seventh New Collegiate Dictionary 174 (1963). And here is a sentence defining “brought”: But a natural reading of § 27's text does not extend so far. “Brought” in this context means “commenced,” Black's Law Dictionary 254 (3d ed. 1933).
```

The goal of this task is to identify if a sentence contains a definition. For example, the following sentence defines "vacation":

```text
A vacation is defined by Bouvier to be the period of time between the end of one term and the beginning of another.
```
 
## Task construction
 
This task was constructed by hand-coding sentences from Supreme Court opinions.
 
## Data column names
 
- `text`: a sentence from an opinion
- `label`: whether the sentence defines a term (`Yes`) or not (`No`)
