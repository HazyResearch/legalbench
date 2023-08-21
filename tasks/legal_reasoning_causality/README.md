# legal_reasoning_causality

### Given an excerpt from a district court opinion, classify if it relies on statistical evidence in its reasoning.
---



**Source**: Haggai Porat, Tom Zur

**License**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 59

**Legal reasoning type**: Rhetorical-analysis

**Task type**: Binary classification

## Task description

Large datasets of court opinions are typically limited to identifying and coding technical information, such as the names of the parties and the judge(s), and sometimes the outcome and the legal topics of the case. However, the most important part of any judicial opinion, the legal reasoning, is typically treated as a black box in empirical legal scholarship. This task begins to address this shortcoming. It focuses on the way that judges provide legal reasoning for the finding of causality (specifically, in labor discrimination cases), and labels the text based on the question of whether the judge/s, in their written reasoning, relied on statistical evidence (e.g., regression analysis) or direct evidence (e.g., witnesses' testimonies) when determining the legal question of whether there was a causal link between the plaintiff's characteristics (e.g., gender, race) and the contested decision (to hire them, set a certain wage, etc.).

## Task construction

We read fifty nine (59) court opinions issued in cases of labor market discrimination by judges from the US Federal District Courts, and we identified and extracted the passages that provide legal reasoning for finding of causality ("text" column). In the second stage, we labeled ("label" column) the text as either relying on statistical evidence (e.g., regression analysis) (labeled as "Yes") or by direct evidence (e.g., witnesses) (labeled as "No").

# Data column names
- `text`: excerpt from judicial decision
- `answer`: whether the excerpt relies on causality or not