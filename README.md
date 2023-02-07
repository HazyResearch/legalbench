# LegalBench

## About

LegalBench is an open science effort to benchmark legal reasoning in [foundation models](https://arxiv.org/abs/2108.07258). For more information, please see our [call for submissions on ArXiv](https://arxiv.org/abs/2209.06120), which outlines our vision for this project.

The goals for this project are twofold:

1. First, we'd like to develop a diverse collection of tasks which can test different aspects of legal reasoning in foundation models. We ground our approach in the IRAC framework, which is a common approach to "legal reasoning" in American law.

2. Second, we'd like to understand how different foundation models perform on these tasks, and what types of methods (e.g. prompt types) improve performance.

We've seeded LegalBench with an initial collection of 43 tasks, which can be found in this Github. However, we're excited to expand beyond these tasks. To that end, we welcome any individuals/groups with relevant domain expertise to submit their own tasks and prompts. Our ultimate goal is to collaboratively write a paper with all contributors detailing our findings (we're inspired by the [Deep Review effort](https://github.com/cgreene/deep-review) and [BigBench](https://github.com/google/BIG-bench/)). This repository contains more information on how to submit tasks and get involved!

If you have any questions, please don't hesitate to reach out to Neel Guha (nguha@stanford.edu).

## Collaboration approach

As we've discussed above, LegalBench is inspired by Open Science initiatives, and we hope it can be a community wide effort in which relevant stakeholders participate in. We envision the following model of collaboration:

1. Any individual or group with relevant domain expertise may contribute one more tasks to LegalBench via our website. Tasks should ideally fall into the IRAC framework, and consist of at least 50 samples for inference. More information on task requirements is detailed below.
2. When new FMs are released, we will run them on LegalBench tasks and release results.
3. After LegalBench has grown to encompass a sufficient number of tasks, we hope to---together with all task contributors to LegalBench---collaboratively write a paper detailing the different tasks and discussing our findings.

## What are foundation models?

Foundation models are extremely large pretrained models that have been trained on vast amounts of corpora. These models are typically *autoregressive*-given the beginning of a text fragment, they're usually capable of generating a cogent and fluent completion for the fragment. Prior research has shown that, by carefully designing [prompts](https://thegradient.pub/prompting/), these models can be used to perform more general purpose language classification tasks. 

At a high level, designing prompts entails constructing an ``input'' text that consists of a description of the task, several demonstrations of the task, and the sample to predict. We provide more information on how to design prompts for legal tasks [here](./prompts/README.md).

## Contributing task data

### Task requirements

For examples of submitted tasks, please see the tasks submitted under `tasks/`. Tasks should contain at least 50 test samples, and between 2-5 train samples. Tasks should fall into one of following categories:

**Issue tasks**: For these tasks, the model must identify a relevant legal issue in an input text.

**Rule tasks**: For these tasks, the model is asked to restate a particular legal rule, or identify a quality of a legal rule.

**Application and conclusion tasks**: For these tasks, the model is provided with a rule and a set of facts, and must determine what the outcome of the rule applied to those facts is. Examples: hearsay, diversity jurisdiction, etc.

**Classification tasks**: These correspond to other legally relevant applications that require a model to classify a piece of text into a category. Examples: contract clause classification, citation prediction, etc.

### Submitting tasks

There are three ways to contribute tasks.

**Contributing via Github**. Please submit a merge request with the following changes.

1. Create a directory under `tasks/` with the name of the task.
2. Create `test.tsv` in this directory with the test data. Make sure the file has the columns "label" and "text."
3. [OPTIONAL] If you have created training data as well, put that in a file called `train.tsv`.
4. [OPTIONAL] If you would like to contribute a chain-of-thought style prompt, then write chain-of-thought style explanations for the provided train samples in a file called `train_explanations.txt`. See the hearsay task for an explanation.


**Contributing via Google forms**. Please submit the task using this [form](https://forms.gle/HjgH8Vd3b2143cu29).


**Contributing via email**. Please create the above files and email Neel Guha (nguha@stanford.edu)! He will manually add them to this repository.

## Prompts

To submit prompt, see [here](./prompts/README.md) for more information about our prompt schema, and how to submit prompts.

## Current tasks
See [here](https://docs.google.com/spreadsheets/d/1DiY4ktP5zYi-uC6OgGUf8E05WX9Ea8IiZsuZicL8kHg/edit?usp=sharing) for a description of current tasks. We shall update this as more tasks are added.

## Licenses
LegalBench is a mix of created and transformed datasets. We ask that you follow the license of the dataset creator. 


| Task                        | License                                                   | 
| --------------------------- | --------------------------------------------------------- | 
| CUAD                        | [CC by 4.0](https://creativecommons.org/licenses/by/4.0/) | 
| Abercrombie                 | [CC by 4.0](https://creativecommons.org/licenses/by/4.0/) |  
| Diversity                   | [CC by 4.0](https://creativecommons.org/licenses/by/4.0/) | 
| Hearsay                     | [CC by 4.0](https://creativecommons.org/licenses/by/4.0/) | 
| Personal Jurisdiction       | [CC by 4.0](https://creativecommons.org/licenses/by/4.0/) | 
| PROA                        | [CC by 4.0](https://creativecommons.org/licenses/by/4.0/) | 
| Rule QA                     | [CC by 4.0](https://creativecommons.org/licenses/by/4.0/) | 
| Intra-rule distinguishing   | [CC by 4.0](https://creativecommons.org/licenses/by/4.0/) | 

## Citing this work

Please cite to our ArXiv paper!

```
@misc{https://doi.org/10.48550/arxiv.2209.06120, 
  doi = {10.48550/ARXIV.2209.06120}, 
  url = {https://arxiv.org/abs/2209.06120}, 
  author = {Guha, Neel and Ho, Daniel E. and Nyarko, Julian and Ré, Christopher}, 
  keywords = {Artificial Intelligence (cs.AI), FOS: Computer and information sciences, FOS: Computer and information sciences}, 
  title = {LegalBench: Prototyping a Collaborative Benchmark for Legal Reasoning}, 
  publisher = {arXiv}, 
  year = {2022}, 
  copyright = {arXiv.org perpetual, non-exclusive license}
}
```

