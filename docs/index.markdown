---
layout: default
title: Home
nav_order: 1
description: "A collaborative benchmark for evaluating legal reasoning in large language models"
permalink: /
---

# A collaboratively built large language model benchmark for legal reasoning

{: .fs-9}

---

The LegalBench project is an ongoing open science effort to collaboratively curate tasks for evaluating legal reasoning in English large language models (LLMs). The benchmark currently consists of **162** tasks gathered from **40** contributors.

- [Read the paper.](https://arxiv.org/abs/2209.06120)
- [Download the dataset from Huggingface.]()
- [See prompts for different tasks.](https://github.com/HazyResearch/legalbench/)

## What is LegalBench?

LegalBench is a benchmark consisting of different legal reasoning *tasks*. Each task has an associated *dataset*, consisting of input-output pairs. Examples of tasks include:

- The [hearsay](/tasks/hearsay.html) task, for which the input is a description of some evidence and the output is whether or not that evidence would be considered hearsay (i.e., "Yes" or "No").
- The [definition extraction](tasks/definition_extraction.html) task, for which the input is a sentence (from a Supreme Court opinion) which defines a term, and the output is the term.
- The [Rule QA](/tasks/rule_qa.html) task, for which the input is a question about the substance of a law, and the output is the correct answer to the question.

Task datasets can be used to evaluate LLMs by providing the LLM with the input, and evaluating how frequently it generates the corresponding output. LegalBench tasks cover a wide range of textual types, task structures, legal domains, and difficulty levels. Descriptions of each task are available [here](./tasks/index.markdown).

Notably, LegalBench tasks have been assembled through a unique crowd-sourcing effort within the legal community. [Individuals and organizations](#contributors) from a broad range of legal backgrounds---lawyers, computational legal practitioners, law professors, and legal impact labs---have contributed tasks they see as "interesting" or "useful." Interesting tasks are those that require a type of reasoning that the contributor deemed to be worth measuring. For instance, the task might correspond to one that law students are frequently expected to perform as part of assessments. Useful tasks correspond to processes that legal professionals currently engage in (either manually or through other means), and thus represent potential practical applications for LLMs.

**LegalBench is ongoing and we are always looking to incorporate more tasks. See [here](./contribute.markdown) for more information on how to get involved!**

## How can LegalBench be used?

**For AI researchers**: LegalBench provides a collection of interesting and hard tasks. Researchers have long recognized the distinct technical challenges posed by legal tasks: complex jargon, longer contexts, sophisticated multi-step reasoning, intricate structure, and minimal labeled data. LegalBench offers AI researchers a new and relevant setting in which to evaluate existing LLMs.

**For the legal community**: LegalBench provides a means of assessing the performance of different LLMs for law-relevant tasks. As the legal community increasingly explores the potential applications and uses for LLMs, empirical assessments of LLM performance on domain-relevant tasks grow in importance. LegalBench provides legal professionals with guidance on the types of tasks where current LLMs/prompting methods are proficient, and the types where significant technical improvements are necessary.

## Citation information

If you intend to reference LegalBench broadly, please use the citation below. If you are working with a particular task, please use the citation below **in addition** to the task specific citation (which can be found on the task page).

```bib
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

## Contributors

The following individuals/groups have contributed to LegalBench:

- [Neel Guha](https://www.neelguha.com/)
- Julian Nyarko
- Daniel E. Ho
- Christopher Ré
- Adam Chilton
- Aditya Narayana
- Alex Chohlas-Wood
- Austin Peters
- [Brandon Waldon](https://bwaldon.github.io/)
- Daniel N. Rockmore
- Diego Zambrano
- Dmitry Talisman
- Enam Hoque
- [Faiz Surani](https://faizsurani.com)
- [Frank Fagan](https://www.stcl.edu/about-us/faculty/frank-fagan/)
- Galit Sarfaty
- [Gregory M. Dickinson](https://www.stu.edu/law/faculty-staff/faculty/gregorydickinson/)
- [Haggai Porat](https://hls.harvard.edu/haggai-porat/)
- Jason Hegland
- Jessica Wu
- Joe Nudell
- [Joel Niklaus](https://niklaus.ai)
- [John Nay](http://johnjnay.com/)
- Jonathan H. Choi
- [Kevin Tobia](https://www.law.georgetown.edu/faculty/kevin-tobia/)
- Margaret Hagan
- Megan Ma
- [Michael Livermore](https://www.law.virginia.edu/faculty/profile/mal5un/2457619)
- [Nikon Rasumov-Rahe](https://maxime.tools/)
- [Nils Holzenberger](https://perso.telecom-paristech.fr/holzenberger/)
- [Noam Kolt](http://noamkolt.com/)
- [Peter Henderson](https://www.peterhenderson.co/)
- [Sean Rehaag](https://www.osgoode.yorku.ca/faculty-and-staff/rehaag-sean/)
- Sharad Goel
- Shang Gao
- [Spencer Williams](https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=2882090)
- Sunny Gandhi
- Tom Zur
- Varun Iyer
- Zehua Li
