---
layout: default
title: Tasks
nav_order: 3
has_children: true
---

## Task organization
LegalBench tasks are organized into six categories based on the type of legal reasoning the task requires. These are: 

- Issue-spotting: tasks in which an LLM must determine if a set of facts raise a particular set of legal questions, implicate an area of the law, or are relevant to a specific party.
- Rule-recall: tasks which require the LLM to generate the correct legal rule on an issue in a jurisdiction (e.g., the rule for hearsay in US federal court), or answer a question about what the law in a jurisdiction does/does not permit.
- Rule-application: tasks which evaluate whether an LLM can explain reasoning in a manner which exhibits the correct legal inferences.
- Rule-conclusion: tasks which require an LLM to determine the legal outcome of a set of facts under a specified rule.
- Interpretation: tasks which require the LLM to parse and understand a legal text (e.g., classifying contractual clauses).
- Rhetorical-understanding: tasks which require an LLM to reason about legal argumentation and analysis (e.g., identifying textualist arguments).

A richer description of tasks can be found in the most recent paper. The purpose of organizing tasks is to enable higher-level observations about the types of tasks which different LLMs can perform, using a vocabulary familiar to lawyers.


## Train/test splits

Each LegalBench task has a "train split" which contains a handful of labeled samples. These samples can be used as in-context demonstrations in prompts. However, benchmark users are also welcome to resample the train/test splits in order to create larger train sets, or pursue other research goals.

## Licenses

LegalBench tasks are subject to different licenses. License information can be found on task pages.


## Prompts

Prompts for tasks are available on the [Github repository](https://github.com/HazyResearch/legalbench/).


## Evaluation 

Evaluation code for all non-open generation tasks can be found on the [Github repository](https://github.com/HazyResearch/legalbench/).

LegalBench contains several open-generation tasks. These include [rule_qa](./rule_qa.markdown) and the rule-application tasks. For these tasks, we provide a [manual gradebook]() to guide evaluation.

