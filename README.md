# 📜 LegalBench

<div align="center">

The LegalBench project is an ongoing open science effort to collaboratively curate tasks for evaluating legal reasoning in English large language models (LLMs). The benchmark currently consists of 162 tasks gathered from 40 contributors.

[**Website**](https://hazyresearch.stanford.edu/legalbench/)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[**Data**](https://huggingface.co/datasets/nguha/legalbench)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[**Paper**](https://arxiv.org/abs/2308.11462)
</div>


## What is LegalBench?

LegalBench is a benchmark consisting of different legal reasoning *tasks*. Each task has an associated *dataset*, consisting of input-output pairs. Examples of tasks include:

- The [hearsay](./tasks/hearsay/README.md) task, for which the input is a description of some evidence and the output is whether or not that evidence would be considered hearsay (i.e., "Yes" or "No").
- The [definition extraction](./tasks/definition_extraction/README.md) task, for which the input is a sentence (from a Supreme Court opinion) which defines a term, and the output is the term.
- The [Rule QA](./tasks/rule_qa/README.md) task, for which the input is a question about the substance of a law, and the output is the correct answer to the question.

Task datasets can be used to evaluate LLMs by providing the LLM with the input, and evaluating how frequently it generates the corresponding output. LegalBench tasks cover a wide range of textual types, task structures, legal domains, and difficulty levels. Descriptions of each task are available [here](https://hazyresearch.stanford.edu/legalbench/tasks/).

Notably, LegalBench tasks have been assembled through a unique crowd-sourcing effort within the legal community. [Individuals and organizations](https://hazyresearch.stanford.edu/legalbench/#contributors) from a broad range of legal backgrounds---lawyers, computational legal practitioners, law professors, and legal impact labs---have contributed tasks they see as "interesting" or "useful." Interesting tasks are those that require a type of reasoning that the contributor deemed to be worth measuring. For instance, the task might correspond to one that law students are frequently expected to perform as part of assessments. Useful tasks correspond to processes that legal professionals currently engage in (either manually or through other means), and thus represent potential practical applications for LLMs.

**LegalBench is ongoing and we are always looking to incorporate more tasks. See [here](https://hazyresearch.stanford.edu/legalbench/contribute/) for more information on how to get involved!**


## Who are we?

We're an [interdisciplinary team]([#contributors](https://hazyresearch.stanford.edu/legalbench/#contributors)) of computer scientists and lawyers spanning academia and industry, interested in understanding the types of legal tasks that modern language models are capable of solving. To do so, we've been accumulating and constructing a diverse collection of legal NLP tasks---all of which are [available]([/legalbench/tasks/](https://hazyresearch.stanford.edu/legalbench/tasks/)) in this repository. We have two goals for this project:

1. First, we'd like to use these datasets to continually evaluate large language models for tasks involving legal reasoning and legal text. In particular, we're excited by the idea that the unique challenges posed by legal text may inspire new algorithmic innovations.
2. Second, we'd like to use these datasets to guide legal practitioners and academics as they seek to understand to the safety and reliability implications of these models in their daily workflows.

Our approach to building LegalBench is inspired by contemporaneous open-science efforts for democratizing participation in machine learning development (e.g [HELM](https://crfm.stanford.edu/helm/latest/), [BigBench](https://github.com/google/BIG-bench)).


## Contributing a task

Please see [here](https://hazyresearch.stanford.edu/legalbench/contribute/) for more details.


## Evaluating on LegalBench tasks

Please see [here](https://hazyresearch.stanford.edu/legalbench/getting-started/) for more details.


## Licenses

LegalBench is a mix of created and transformed datasets. We ask that you follow the license of the dataset creator. Please see the [task page](https://github.com/HazyResearch/legalbench/tree/main/tasks) for a list of tasks and licenses.

Please see the [notebook](https://github.com/HazyResearch/legalbench/blob/main/UsingLegalBench.ipynb) for an example of how to select tasks based on license information.

## Recent work involving LegalBench

We'd like to highlight community efforts building on LegalBench. If you've worked with LegalBench and would like us to add a pointer to your work here, please get in touch! 

Projects/evaluation frameworks:
- [vals.ai](https://www.vals.ai/)
- Stanford Center for Foundation Model Research's [HELM Lite Benchmark](https://crfm.stanford.edu/helm/lite/latest/)
- [Reexpress AI: Uncertainty-aware Legal Reasoning](https://github.com/ReexpressAI/Example_Data/blob/main/tutorials/tutorial8_legalbench/README.md)

Research:
- Nihal V. Nayak, Yiyang Nan, Avi Trost, & Stephen H. Bach. [Learning to Generate Instruction Tuning Datasets for Zero-Shot Task Adaptation](https://arxiv.org/abs/2402.18334) (2024)
- Sergio Servantez, Joe Barrow, Kristian Hammond, & Rajiv Jain. [Chain of Logic: Rule-Based Reasoning with Large Language Models](https://arxiv.org/abs/2402.10400) (2024).

## Citing this work

Please include all citations below, which credit all sources LegalBench draws on.

```text
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

## Contact

For questions, concerns, or comments, please reach out to Neel (nguha@stanford.edu).
