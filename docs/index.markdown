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

- [Read the paper.](https://arxiv.org/abs/2308.11462)
- [Download the dataset from Huggingface.](https://huggingface.co/datasets/nguha/legalbench)
- [See prompts for different tasks.](https://github.com/HazyResearch/legalbench/)

## What is LegalBench?

LegalBench is a benchmark consisting of different legal reasoning *tasks*. Each task has an associated *dataset*, consisting of input-output pairs. Examples of tasks include:

- The [hearsay](tasks/hearsay.html) task, for which the input is a description of some evidence and the output is whether or not that evidence would be considered hearsay (i.e., "Yes" or "No").
- The [proa](tasks/proa.html) task, for which the input is a statute, and the output is whether or not that statute contains a private right of action.
- The [Rule QA](tasks/rule_qa.html) task, for which the input is a question about the substance of a law, and the output is the correct answer to the question.

Task datasets can be used to evaluate LLMs by providing the LLM with the input, and evaluating how frequently it generates the desired output. LegalBench tasks cover a wide range of textual types, task structures, legal domains, and difficulty levels. Descriptions of each task are available [here](./tasks/index.markdown).


## Where do tasks come from?
Notably, LegalBench tasks have been assembled through a unique crowd-sourcing effort within the legal community. [Individuals and organizations](#contributors) from a broad range of legal backgrounds---lawyers, computational legal practitioners, law professors, and legal impact labs---have contributed tasks they see as "interesting" or "useful." Interesting tasks are those that require a type of reasoning that the contributor deemed to be worth measuring. For instance, the task might correspond to one that law students are frequently expected to perform as part of assessments. Useful tasks correspond to realistic potential applications of LLMs (e.g., contractual analysis). LegalBench has also been augmented with tasks derived from existing legal benchmarks (e.g., CUAD), thus providing a single platform for evaluating a wide range of legal tasks.

**LegalBench is ongoing and we are always looking to incorporate more tasks. See [here](./contribute.markdown) for more information on how to get involved!**

## How can LegalBench be used?

**For AI researchers**: LegalBench provides a collection of interesting and hard tasks. Researchers have long recognized the distinct technical challenges posed by legal tasks: complex jargon, longer contexts, sophisticated multi-step reasoning, intricate structure, and minimal labeled data. LegalBench offers AI researchers a new and relevant setting in which to evaluate existing LLMs.

**For the legal community**: LegalBench provides a means of assessing the performance of different LLMs for law-relevant tasks. As the legal community increasingly explores the potential applications and uses for LLMs, empirical assessments of LLM performance on domain-relevant tasks grow in importance. LegalBench provides legal professionals with guidance on the types of tasks for which current LLMs/prompting methods are proficient, and the types where significant technical improvements are necessary.

## Citation information

Please include all citations below, which credit all sources LegalBench draws on.

```bib
@misc{guha2023legalbench,
      title={LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models}, 
      author={Neel Guha and Julian Nyarko and Daniel E. Ho and Christopher Ré and Adam Chilton and Aditya Narayana and Alex Chohlas-Wood and Austin Peters and Brandon Waldon and Daniel N. Rockmore and Diego Zambrano and Dmitry Talisman and Enam Hoque and Faiz Surani and Frank Fagan and Galit Sarfaty and Gregory M. Dickinson and Haggai Porat and Jason Hegland and Jessica Wu and Joe Nudell and Joel Niklaus and John Nay and Jonathan H. Choi and Kevin Tobia and Margaret Hagan and Megan Ma and Michael Livermore and Nikon Rasumov-Rahe and Nils Holzenberger and Noam Kolt and Peter Henderson and Sean Rehaag and Sharad Goel and Shang Gao and Spencer Williams and Sunny Gandhi and Tom Zur and Varun Iyer and Zehua Li},
      year={2023},
      eprint={2308.11462},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
@article{koreeda2021contractnli,
  title={ContractNLI: A dataset for document-level natural language inference for contracts},
  author={Koreeda, Yuta and Manning, Christopher D},
  journal={arXiv preprint arXiv:2110.01799},
  year={2021}
}
@article{hendrycks2021cuad,
  title={Cuad: An expert-annotated nlp dataset for legal contract review},
  author={Hendrycks, Dan and Burns, Collin and Chen, Anya and Ball, Spencer},
  journal={arXiv preprint arXiv:2103.06268},
  year={2021}
}
@article{wang2023maud,
  title={MAUD: An Expert-Annotated Legal NLP Dataset for Merger Agreement Understanding},
  author={Wang, Steven H and Scardigli, Antoine and Tang, Leonard and Chen, Wei and Levkin, Dimitry and Chen, Anya and Ball, Spencer and Woodside, Thomas and Zhang, Oliver and Hendrycks, Dan},
  journal={arXiv preprint arXiv:2301.00876},
  year={2023}
}
@inproceedings{wilson2016creation,
  title={The creation and analysis of a website privacy policy corpus},
  author={Wilson, Shomir and Schaub, Florian and Dara, Aswarth Abhilash and Liu, Frederick and Cherivirala, Sushain and Leon, Pedro Giovanni and Andersen, Mads Schaarup and Zimmeck, Sebastian and Sathyendra, Kanthashree Mysore and Russell, N Cameron and others},
  booktitle={Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  pages={1330--1340},
  year={2016}
}
@inproceedings{zheng2021does,
  title={When does pretraining help? assessing self-supervised learning for law and the casehold dataset of 53,000+ legal holdings},
  author={Zheng, Lucia and Guha, Neel and Anderson, Brandon R and Henderson, Peter and Ho, Daniel E},
  booktitle={Proceedings of the eighteenth international conference on artificial intelligence and law},
  pages={159--168},
  year={2021}
}
@article{zimmeck2019maps,
  title={Maps: Scaling privacy compliance analysis to a million apps},
  author={Zimmeck, Sebastian and Story, Peter and Smullen, Daniel and Ravichander, Abhilasha and Wang, Ziqi and Reidenberg, Joel R and Russell, N Cameron and Sadeh, Norman},
  journal={Proc. Priv. Enhancing Tech.},
  volume={2019},
  pages={66},
  year={2019}
}
@article{ravichander2019question,
  title={Question answering for privacy policies: Combining computational and legal perspectives},
  author={Ravichander, Abhilasha and Black, Alan W and Wilson, Shomir and Norton, Thomas and Sadeh, Norman},
  journal={arXiv preprint arXiv:1911.00841},
  year={2019}
}
@article{holzenberger2021factoring,
  title={Factoring statutory reasoning as language understanding challenges},
  author={Holzenberger, Nils and Van Durme, Benjamin},
  journal={arXiv preprint arXiv:2105.07903},
  year={2021}
}
@article{lippi2019claudette,
  title={CLAUDETTE: an automated detector of potentially unfair clauses in online terms of service},
  author={Lippi, Marco and Pa{\l}ka, Przemys{\l}aw and Contissa, Giuseppe and Lagioia, Francesca and Micklitz, Hans-Wolfgang and Sartor, Giovanni and Torroni, Paolo},
  journal={Artificial Intelligence and Law},
  volume={27},
  pages={117--139},
  year={2019},
  publisher={Springer}
}
```

## Contributors

The following individuals/groups have contributed to LegalBench:

- [Neel Guha](https://neelguha.github.io/)
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
