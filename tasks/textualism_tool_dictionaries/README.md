# textualism_tool_dictionaries

### Determine if a paragraph from a judicial opinion is applying a form textualism that relies on the dictionary meaning of terms.
---



**Source**: Austin Peters

**License**: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

**Size (samples)**: 111

**Legal reasoning type**: Rhetorical-analysis

**Task type**: Binary classification

## Task description

This is a binary classification task in which the LLM must determine if a paragraph interpreting a statute uses a dictionary, such as Websters Dictionary or Black Law’s Legal Dictionary. In order to recieve a positive label (``Yes''), the paragraph must: 

1. Reference reliance on the use of a dictionary in interpreting the statute. This includes explicit reference or referencing the tools logic. 
2. Provide evidence that the opinion used a dictionary. This includes a) citing it as a general rule of decision guiding the outcome or b) applying it to the facts.

## Task construction

The contributes collected a sample of 1,000 random Court of Appeals paragraphs where a verb + noun combination occurs in a sentence suggests the paragraph involves statutory interpretation. For example, the combination of “interpret” + “statute”. These paragraphs where then manually coded as to whether they meet the criteria above. 

## Data column names
 
 - `answer`: whether the excerpt evidences dictionary-based textualism
 - `text`: judicial excerpt