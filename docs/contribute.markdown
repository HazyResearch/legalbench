---
layout: page
title: Contribute
permalink: /contribute/
nav_order: 4
---

# Contributing to LegalBench

We continue to solicit more contributions to LegalBench. If you are interested in developing a task, know of an existing legal reasoning/legal text analysis dataset, or possess data that is relevant to legal reasoning, then we would love to explore adding your task/dataset to LegalBench. Please see below for more details on how to contribute a task.

Task contributors will be invited to join future papers describing newly added tasks, in the style of the most recent LegalBench paper.

## What is the process for contributing?

If you have a task or dataset in mind, we ask that you first reach out to us (contact Neel at [nguha@cs.stanford.edu](nguha@cs.stanford.edu)) with a description of the task and the dataset. Task contributions undergo a review process for both legal correctness and task robustness. We will then work with you to incorporate the dataset into LegalBench.

## Task ideas

Below is an incomplete list of potential task ideas:

- We are especially interested in hand-coded data generated as part of empirical legal scholarship!
- Tasks which require a model to apply specific legal rule(s) to a hypothetical pattern of facts. For instance:
  - E.g., asking the model to determine from a set of facts describing a contractual relationship which party would be liable for breaching the contract.
- Tasks which require a model to answer questions about the law in different jurisdiction.
  - E.g., asking the model to explain differences in law between two jurisdictions.
- Tasks which require a model to classify legal texts.
  - E.g., asking the model to classify if a piece of statutory text performs a certain function (e.g., creates a private right, discusses notice requirements, allows for fee-shifting, etc.)
- Tasks which require the model to perform types of reasoning common or unique to legal practice.
  - Asking the model to determine the Bluebook signal that should preface a particular parenthetical.
  - Asking the model to evaluate which premise most strongly supports a legal argument.
- A number of LegalBench tasks are quite small, with only 50-100 samples. We welcome contributions which make an existing task larger.

## FAQ

**What jurisdictions are allowed?**

Any jurisdiction is acceptable, provided the task text is in English.

**How do licenses work?**

When you submit a task you may specify the license that applies.

**How large do tasks need to be?**

Tasks should be at least 50 samples.

**How long can task samples be?**

There is no limit--task samples can be document-length.

**Does the LSAT count as legal reasoning?**

No. The LSAT is a generalist exam for logical reasoning and reading comprehension. Though it's an essential part of American law school applications, it doesn't actually require legal reasoning. If you're curious about performance on the LSAT, we encourage you check out the [HELM effort](https://crfm.stanford.edu/helm/latest/?group=lsat_qa)!
