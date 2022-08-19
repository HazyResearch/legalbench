# LegalBench

## About

LegalBench is an open science effort to benchmark legal reasoning in foundation models. For more information, please see our call for submissions on ArXiv, which outlines our vision for this project.

The goals for this project are twofold: 

1. First, we'd like to develop a diverse collection of tasks which can test different aspects of legal reasoning in foundation models. We ground our approach in the IRAC framework, which is common approach to "legal reasoning" in American law.

2. Second, we'd like to understand how different foundation models perform on these tasks, and what types of methods (e.g. prompt types) improve performance.

We've seeded LegalBench with an initial collection of 43 tasks, which can be found in this Github. However, we're excited to expand beyond these tasks. To that end, we welcome any individuals/groups with relevant domain expertise to submit their own tasks and prompts. Our ultimate goal is to collaboratively write a paper with all contributors detailing our findings (we're inspired by the [Deep Review effort](https://github.com/cgreene/deep-review)). This repository contains more information on how to submit tasks and get involved!

If you have any questions, please don't hesitate to reach out to Neel Guha (nguha@stanford.edu).

## Collaboration model

As we've discussed above, LegalBench is inspired by Open Science initiatives, and hope it can be a community wide effort in which relevant stakeholders participate in. We envision the following model of collaboration: 

1. Any individual or group with relevant domain expertise may contribute one more tasks to LegalBench via our website. Tasks should ideally fall into the IRAC framework, and consist of at least 50 samples for inference. More information on task requirements is detailed below.
2. When new FMs are released, we will run them on LegalBench tasks and release results.
3. After LegalBench has grown to encompass a sufficient number of tasks, we hope to---together with all task contributors to LegalBench---collaboratively write a paper detailing the different tasks and discussing our findings.

## Contributing task data

**Task requirements**. For examples of submitted tasks, please see the tasks submitted under `tasks/`. Tasks should contain at least 50 test samples, and between 2-5 train samples. Tasks should fall into one of three categories: 

- Issue tasks, which require a model to identify a relevant legal issue in an input text. 
- Rule tasks, which require a model to restate a particular legal rule, or identify a quality of a legal rule.
- Application/conclusion tasks, in which the model is provided with a rule and a set of facts, and must determine what the outcome of the rule applied to those facts is.

If you submit an application/conclusion task, we ask that you also submit the rule being used (see [below](#contributing-prompts) for more details). 

There are two ways to contribute tasks–via Github and via email. We prefer submission via Github, but understand if email is easier.

**Contributing via Github**. Please submit a merge request with the following changes.

1. Create a directory under `tasks/` with the name of the task.
2. Create `test.tsv` in this directory with the test data. Make sure the file has the columns "label" and "text." 
3. [OPTIONAL] If you have created training data as well, put that in a file called `train.tsv`.

See [LINK HERE]() for an example merge request.

**Contributing via email**. Please create the above files and email Neel Guha (nguha@stanford.edu)! He will manually add them to this repository.

## Prompts
To submit prompt, see [here](./prompts/README.md) for more information about our prompt schema, and how to submit prompts.


## Current tasks

## Citing this work