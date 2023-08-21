# hearsay 

### Classify if a particular piece of evidence qualifies as hearsay.
---



**Source**: Neel Guha

**License**: [CC By 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 100

**Legal reasoning type**: Rule-application/Rule-conclusion

**Task type**: Binary classification

## Task description
The Federal Rules of Evidence dictate that hearsay evidence is inadmissible at trial. Hearsay is defined as an "out-of-court statement introduced to prove the truth of the matter asserted." In determining whether a piece of evidence meets the definition of hearsay, lawyers ask three questions: 

1. Was there a statement?
2. Was it made outside of court?
3. Is it being introduced to prove the truth of the matter asserted?

**Was there a statement?** The definition of statement is broad, and includes oral assertions, written assertions, and non-verbal conduct intended to communicate (i.e. \textit{assert}) a message. Thus, for the purposes of the hearsay rule, letters, verbal statements, and pointing all count as statements. 

**Was it made outside of court?** Statements not made during the trial or hearing in question count as being out-of-court. 

**Is it being introduced to prove the truth of the matter asserted?** A statement is introduced to prove the truth of the matter asserted if its truthfulness is essential to the purpose of its introduction. Suppose that at trial, the parties were litigating whether Alex was a soccer fan. Evidence that Alex told his brother "I like soccer," would be objectionable on hearsay grounds, as (1) the statement itself asserts that Alex likes soccer, and (2) the purpose of introducing this statement is to prove/disprove that Alex likes soccer. In short, the truthfulness of the statement's assertion is central to the issue being litigated. However, consider if one of the parties wished to introduce evidence that Alex told his brother, "Real Madrid is the greatest soccer team in the world." This statement would **not** be hearsay. Its assertion---that Real Madrid is the greatest soccer team in the world---is unrelated to the issue being litigated. Here, one party is introducing the statement not to prove what the statement says, but to instead show that a particular party (i.e. Alex) was the speaker of the statement.

In practice, many pieces of evidence which are hearsay are nonetheless still admissible under one of the many hearsay exception rules. We ignore these exceptions for our purposes, and leave the construction of benchmarks corresponding to these exceptions for future work.

## Dataset construction
We create a dataset to test a model's ability to apply the hearsay rule. Each sample in the dataset describes (1) an issue being litigated or an assertion a party wishes to prove, and (2) a piece of evidence a party wishes to introduce. The goal is to determine if---as it relates to the issue---the evidence would be considered hearsay under the definition provided above. 

We create the hearsay dataset by hand, drawing inspiration from similar exercises available in legal casebooks and online resources. The dataset consists of 5 types of questions, where each slice tests a different aspect of the hearsay rule. We randomly select 1 sample from each slice to be in the train set. The remainder of the slice constitutes the test set (for a total of 95 samples). The slices (with test set counts) are: 

- Statement made in court: Fact patterns where the statement in question is made during the course of testimony at trial. Thus, the statement is not hearsay.
- Non-assertive conduct: Fact patterns where the evidence does not correspond to a statement. Hence, the hearsay rule is inapplicable.
- Standard hearsay : Fact patterns where there is an oral statement, it is said out of court, and it is introduced to prove the truth of the matter asserted. Thus, these fact patterns correspond to hearsay.
- Non-verbal hearsay: Fact patterns where the statement is hearsay, but made in writing or through assertive conduct (e.g. pointing).
- Not introduced to prove truth : Fact patterns where an out-of-court statement is introduced to prove something other than what it asserts.


## Data column names

- `answer`: whether the evidence in the fact pattern is hearsay ("Yes") or not ("No")
- `text`: a fact pattern describing a piece of evidence and a particular issue
- `slice`: denotes the slice of the fact pattern