# definition_extraction 

### Given a sentence from a Supreme Court opinion offering a definition of a term, extract the term being defined.
---



**Source**: Kevin Tobia

**License**: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

**Task summary**: Extract the term being defined in sentences from Supreme Court opinions.

**Size (samples)**: 696

**Legal reasoning type**: Rhetorical-analysis

**Task type**: Extraction
 
## Task description

Courts frequently define terms in the course of interpreting and applying laws. For instance, the following sentence provides a definition of the term "confidential":

```text
The term “confidential” meant then, as it does now, “private” or “secret.” Webster's Seventh New Collegiate Dictionary 174 (1963). And here is a sentence defining “brought”: But a natural reading of § 27's text does not extend so far. “Brought” in this context means “commenced,” Black's Law Dictionary 254 (3d ed. 1933).
```

The goal of this task is to identify, from a sentence defining a term, the term that is being defined. A challenge is that defining sentences may not explicitly use quotations to denote the term being defined. For example, the following sentence defines "vacation":

```text
A vacation is defined by Bouvier to be the period of time between the end of one term and the beginning of another.
```

## Task construction

This task was constructed by hand-coding sentences from Supreme Court opinions.

## Data column names

- `text`: A sentence from an opinion
- `answer`: The term defined in the sentence. Because a sentence may define multiple terms, or there are multiple ways of referring to the term defined in a sentence, potential correct answers here are separated by a comma. 
