# function_of_decision_section 

### Classify the function of different sections of legal written opinions.
---



**Source**: Gregory M. Dickinson

**License**: [CC By 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 374

**Legal reasoning type**: Rhetorical-analysis

**Task type**: 7-way classification

## Task description

Lawyers reading prior court decisions must be able to identify the function that each section of the written decision serves within the context of the whole. Beginning lawyers in law school are taught to do so intentionally and explicitly as they read cases. As lawyers become more experienced over time, the process becomes second nature. This task is to classify a paragraph extracted from a written decision into one of seven possible categories: Facts, Procedural History, Issue, Rule, Analysis, Conclusion, or Decree.

1. Facts - The paragraph describes the faction background that led up to the present lawsuit.
2. Procedural History - The paragraph describes the course of litigation that led to the current proceeding before the court.
3. Issue - The paragraph describes the legal or factual issue that must be resolved by the court.
4. Rule - The paragraph describes a rule of law relevant to resolving the issue.
5. Analysis - The paragraph analyzes the legal issue by applying the relevant legal principles to the facts of the present dispute.
6. Conclusion - The paragraph presents a conclusion of the court.
7. Decree - The paragraph constitutes a decree resolving the dispute.

## Dataset construction

Beginning at the start of the Fourth Federal Reporter series (1 F.4th 1) paragraphs of text were extracted from decisions of the U.S. Federal Courts of Appeals and classified into one of the seven function categories. To achieve some degree of randomness, cases were chosen sequentially by appearance in the Federal Reporter to avoid a series of decisions decided by the same judge or court or on the same topic.


## Data column names

- `Citation`: the citation for the case from which the text was excerpted with
- `Paragraph`: excerpt from judicial decision
- `answer`: the purpose the excerpt serves. Options: Facts, Procedural History, Issue, Rule, Analysis, Conclusion, Decree