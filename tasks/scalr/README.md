# scalr

### Given a legal question, identify the holding statement (amongst a set of candidates) that best answers a particular legal question.
---



**Source**: [SCALR](https://github.com/lexeme-dev/scalr)

**License**: [CC by 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 571

**Legal reasoning type**: Rhetorical-analysis

**Task type**: 5-way classification

## Description

The SCALR benchmark is a collection of 571 multiple choice questions designed to assess the legal reasoning and reading comprehension ability of large language models. It is intended, to the extent possible, to measure understanding of legal language, rather than the ability to memorize specific legal knowledge.

Each question gives the question presented for review in a particular Supreme Court case. The solver must then determine which "holding" statement best corresponds to the question (i.e. which "holding" statement is a description of the Court's holding in the case for which the question was presented). Here's an example:

> Question: Whether the Federal Arbitration Act preempts States from conditioning the enforcement of an arbitration agreement on the availability of particular procedures--here, class-wide arbitration--when those procedures are not necessary to ensure that the parties to the arbitration agreement are able to vindicate their claims.
>
>A: holding that when the parties in court proceedings include claims that are subject to an arbitration agreement, the FAA requires that agreement to be enforced even if a state statute or common-law rule would otherwise exclude that claim from arbitration
>
>B: holding that the Arbitration Act "leaves no place for the exercise of discretion by a district court, but instead mandates that district courts shall direct the parties to proceed to arbitration on issues as to which an arbitration agreement has been signed"
>
>C: holding that class arbitration "changes the nature of arbitration to such a degree that it cannot be presumed the parties consented to it by simply agreeing to submit
their disputes to an arbitrator"
>
>**D: holding that a California law requiring classwide arbitration was preempted by the FAA because it "stands as an obstacle to the accomplishment and execution of the full purposes and objectives of Congress," which is to promote arbitration and enforce arbitration agreements according to their terms**
>
>E: holding that under the Federal Arbitration Act, a challenge to an arbitration provision is for the courts to decide, while a challenge to an entire contract which includes an arbitration provision is an issue for the arbitrator

Because questions presented for review in Supreme Court cases are not easily available prior to 2001, the benchmark is limited to questions from cases decided in the 2001 Term and later.

## Results

Our test set is composed of 30% of the full dataset (172 questions), chosen at random. We report the performance of a number of different solvers below:

| Solver                                   | % Correct |
|------------------------------------------|-----------|
| Human*                                   | 86.0      |
| gpt-4-0314†                              | 81.4      |
| gpt-3.5-turbo-0301†                      | 64.0      |
| all-mpnet-base-v2 (CaseHOLD fine-tuned)‡ | 50.0      |
| all-mpnet-base-v2‡                       | 46.5      |
| all-distilroberta-v1‡                    | 44.2      |
| TF-IDF Bag-of-Words                      | 27.9      |

*Performance measured for a subset of 50 questions of the test set. Performance for models on this subset is within 2% of the reported performance on the full test set.

†One-shot prompting with temperature 0.0.

‡Results for these models are computed via embedding dot-product similarity:
the choice with an embedding most similar to the question embedding is selected.

## Dataset construction

The data used to create this task comes from the following sources:

- Questions presented were gathered from the Supreme Court of the United States' website, which hosts PDFs of questions granted for review in each case dating back to the 2001 Term.
- Holding statements that comprise the "choices" for each question were compiled from (a) [CourtListener's collection](https://free.law/2022/03/17/summarizing-important-cases/) of parenthetical descriptions of cases written by judges in other cases citing the case in question and (b) extraction of parenthetical descriptions from Courtlistener's and the Caselaw Access Project's collections of court decisions using [Eyecite](https://github.com/freelawproject/eyecite).

To ensure that "holding" statements would address the particular question presented, we limited the set of cases to those in which exactly one question was granted for review. We also perform some manual curation to exclude questions which are not answerable without specific knowledge of a case, e.g.:
>Whether this Court's decision in Harris v. United States, 536 U.S. 545 (2002), should be overruled.

### Choice Selection

To create choices for each question presented, we first filter our set of parenthetical descriptions
as follows:

- We limited our parenthetical descriptions to only those that begin with "holding that...", as these are most  likely to describe the core holding of the case, rather than some peripheral issue.
- We use only parentheticals that describe Supreme Court cases. This avoids the creation
of impossible questions that ask the solver to distinguish between "holding" statements dealing with exactly the same issue at different stages of appellate review.
- We then select for each case the longest parenthetical meeting the above criteria. We use the longest parenthetical because it is likely to be descriptive enough to make the question answerable.

We then create a task for each case which has both a question presented and a "holding" statement meeting the above requirements. (While question-correct holding pairs are only for cases decided after 2001, we allow the use of parentheticals describing any Supreme Court case as incorrect answer choices.) We then need to select the four alternative answer choices for each question in a manner that makes the task challenging. To select choices that are at least facially plausible, we find the four "holding" statements from the remaining pool that are most TF-IDF similar to the question presented.

## Data column names

The dataset TSV file contains the following columns:

- "docket_number": The docket number of the Supreme Court case. Not intended to be passed to models, just for identification purposes.
- "question": The question presented
- "choice_0", "choice_1", "choice_2", "choice_3", "choice_4": The five candidate answers
- "correct_choice_index": A number corresponding to the correct choice (possible values: 0,1,2,3,4)