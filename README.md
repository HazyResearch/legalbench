# LegalBench

LegalBench is a **collaborative** benchmark intended to evaluate English large language models on legal reasoning and legal text-based tasks. LegalBench currently consists of more than 40 tasks, which are described in detail [here](https://github.com/HazyResearch/legalbench/tree/main/tasks). A paper describing the organization of an initial seed set of tasks is available as a preprint [here](https://arxiv.org/abs/2209.06120). This paper will be updated with the most recent task submissions by May 2023, with task submitters included as authors.

We are currently soliciting submissions. Tasks will be reviewed and merged into this repository on a rolling basis.

- [About us](#about-us)
- [Contributing a task](#contributing-a-task)
  - [Task train data](#task-train-data)
  - [Task test data](#task-test-data)
  - [Base prompt](#base-prompt)
  - [Task description](#task-description)
  - [Submission via Github](#submission-via-github)
  - [Submission via Google Forms](#submission-via-google-forms)
  - [Misc](#misc)
- [Contributors](#contributors)
- [Citing this work](#citing-this-work)
- [Contact](#contact)

## About us

We're an [interdisciplinary team](#contributors) of computer scientists and lawyers spanning academia and industry, interested in understanding the types of legal tasks that modern language models are capable of solving. To do so, we've been accumulating and constructing a diverse collection of legal NLP tasks---all of which are [available](/legalbench/tasks/) in this repository. We have two goals for this project:

1. First, we'd like to use these datasets to continually evaluate large language models for tasks involving legal reasoning and legal text. In particular, we're excited by the idea that the unique challenges posed by legal text may inspire new algorithmic innovations.
2. Second, we'd like to use these datasets to guide legal practitioners and academics as they seek to understand to the safety and reliability implications of these models in their daily workflows.

Our approach to building LegalBench is inspired by contemporaneous open-science efforts for democratizing participation in machine learning development (e.g [HELM](https://crfm.stanford.edu/helm/latest/), [BigBench](https://github.com/google/BIG-bench)).

If you have any questions, please don't hesitate to reach out to Neel Guha (nguha@stanford.edu).

## Contributing a task

We are currently in the process of adding more tasks to LegalBench. If you are interested in developing a task, know of an existing legal reasoning/legal text analysis dataset, or possess data that is relevant to legal reasoning, then we would be delighted to add your task/dataset to LegalBench. Our view of what constitutes "legal reasoning" is very broad---any task involving legal text, laws of any jurisdiction, or reasoning skill relevant to the law can be added. Examples of tasks that could be added to LegalBench include:

- Tasks which require a model to apply specific legal rule(s) to a hypothetical pattern of facts. For instance:
  - Asking the model to determine if a particular set of contacts give rise to personal jurisdiction?
  - Asking the model to determine from a set of facts describing a contractual relationship which party would be liable for breaching the contract.
  - Asking the model to determine whether a proposed federal statute would be a permissible exercise of power under the Commerce Clause.
- Tasks which require a model to answer questions about the law in different jurisdiction.
  - Asking the model to provide the holding statements for different cases.
  - Asking the model to explain different common law tests.
  - Asking the model to explain differences in law between two jurisdictions.
  - Asking the model to identify the legal authority for different laws.
- Tasks which require a model to classify legal texts.
  - Asking the model to classify whether or not a contractual provision creates some type of right between the parties.
  - Asking the model to classify whether a provision in a legal agreement would be oppressive and unenforceable under the laws of a jurisdiction.
  - Asking the model to classify if a piece of statutory text performs a certain function (e.g., creates a private right, discusses notice requirements, allows for fee-shifting, etc.)
- Tasks which require the model to perform types of reasoning common or unique to legal practice.
  - Asking the model to determine the Bluebook signal that should preface a particular parenthetical.
  - Asking the model to evaluate which premise most strongly supports a legal argument.

A task submission consists of the following: (1) a task train data file, (2) a task test data file, (3) a base prompt, (3) a task description. We accept new tasks via Github or via Google Forms. Instructions on both methods of submission are provided below.

### Task train data

Task train data should be formatted as TSV (tab separated value) file. The first row of the TSV file should contain a header for each column of data. Most tasks will have only two columns, corresponding to the task input and the correct task output (e.g., [Unfair TOS](/tasks/unfair_tos/)). However, a task may have more than one column (e.g., [Statutory Reasoning Assessment](/legalbench/tasks/statutory_reasoning_assessment)). Each remaining row in the file should correspond to a sample. Task training data should consist of between 5-7 samples. The file should be named `train.tsv`.

If you wish to add metadata for each sample---to categorize subgroups in the dataset which implicate similar challenges---then add that as a column. For instance, [Hearsay](https://github.com/HazyResearch/legalbench/tree/main/tasks/hearsay) consists of a `slice` column, which describes the element of the hearsay rule being tested for each sample.

### Task test data

The test data file should be formatted identically to the train data file. Test data should consist of at least 50 samples. The file should be named `test.tsv`.

### Base prompt

The base prompt file contains a prompt that can be used to solve the task. Below is an example of a prompt for the [Hearsay](https://github.com/HazyResearch/legalbench/tree/main/tasks/hearsay) task.

```text
Hearsay is an out-of-court statement introduced to prove the truth of the matter asserted.


Q: On the issue of whether David is fast, the fact that David set a high school track record. Is there hearsay?
A: No

Q: On the issue of whether Rebecca was ill, the fact that Rebecca told Ronald that she was unwell. Is there hearsay?
A: Yes

Q: To prove that Tim was a soccer fan, the fact that Tim told Jimmy that "Real Madrid was the best soccer team in the world." Is there hearsay?
A: No

Q: When asked by the attorney on cross-examination, Alice testified that she had "never seen the plaintiff before, and had no idea who she was. Is there hearsay?
A: No

Q: On the issue of whether Martin punched James, the fact that Martin smiled and nodded when asked if he did so by an officer on the scene. Is there hearsay?
A: Yes

Q: {text} Is there hearsay?
A:
```

Text enclosed in brackets should correspond to column names in the task data files.

### Task description

Lastly, tasks should be accompanied by a description, which includes the following:

- What the task is.
- What types of legal reasoning the task evaluates.
- How the data was collected or created. If the task was adapted from an existing benchmark, then a reference to that paper should be included.

### Submission via Github

### Submission via Google Forms

Tasks may be submitted via Google Forms at [this link](https://forms.gle/6wRB4ety1a7D1GQF8). Task data can be uploaded as TSV files.

### Misc

- Tasks that have been previously published as parts of other works or benchmarks may be added to LegalBench. If you are doing so, please be sure to follow the licensing requirements imposed by the original publishers, and to include a citation to the original work (see more below).
- Task datasets should consist of at least 50 samples. However, if this is a barrier, please contact us and we can work with you to scale the dataset.
- Due to the length limitations of most large language models, we prefer tasks which operate on sequences of text that are less than 2000 words. For tasks involving longer documents---like contract clause extraction---we encourage you to reframe the task as a classification task, by chunking the long document into subparts.

# Evaluating on LegalBench tasks

We encourage you to use LegalBench. See this [notebook](https://github.com/HazyResearch/legalbench/blob/main/UsingLegalBench.ipynb) for a guide on how to load task data and prompts.

LegalBench tasks will be made available via Huggingface in June 2023.

## Contributors

The following individuals have contributed to LegalBench:

- Neel Guha
- Joel Niklaus
- Nils Holzenberger
- John Nay
- Julian Nyarko
- Daniel E. Ho
- Christopher Ré

## Licenses
LegalBench is a mix of created and transformed datasets. We ask that you follow the license of the dataset creator. Please see the [task page](https://github.com/HazyResearch/legalbench/tree/main/tasks) for a list of tasks and licenses.

## Citing this work

For now, please cite to the ArXiv paper. This will be updated in May 2023 when a paper with task contributors is released. 

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

## Contact

For questions, concerns, or comments, please reach out to Neel (nguha@stanford.edu).
