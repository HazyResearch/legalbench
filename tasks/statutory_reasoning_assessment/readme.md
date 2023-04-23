# statutory_reasoning_assessment 
 **Contributor**: Nils Holzenberger
 
 **Source**: <https://nlp.jhu.edu/law/>
 
 **License**: MIT
 
 ## Task Description
 
 The StAtutory Reasoning Assessment (SARA) dataset tests the ability to reason about summaries of facts and statutes, in the context of US federal tax law. SARA contains a set of statutes, and summaries of facts (cases) paired with a question or an entailment prompt. An entailment prompt asks about a specific section of the SARA statutes. A question asks how much tax one of the protagonists in the case owes.
 
 ## Task Construction
 
 For information on task construction, see the [original paper](https://ceur-ws.org/Vol-2645/paper5.pdf). This task is built off of the [second version of the dataset](https://nlp.jhu.edu/law/#SARA_v2).
 
 
 ## Column names
 
 ### {train, test}.csv
 - **case id**: A unique string identifier for the case.
 - **statute**: The snippet from the statutes that is the most relevant to the question. For numerical cases, that's the entirety of the statutes.
 - **description**:  The summary of facts from the case description.
 - **question**: The question or entailment prompt.
 - **text**:  The concatenation of statute, description and question. This is meant as the input to the LM, as per the LegalBench format. In some cases, this might exceed the context window of the LM, in which case I would recommend truncating from the left.
 - **label**: The answer to the question or entailment problem. Answers to questions are dollar amounts, answers to entailment problems are either "Entailment" or "Contradiction".
 
 ### few-shot-choices.csv
 
 This file contains, for each test case, the 4 closest cases from the training set. The distance is measured in terms of the part of the statutes they test for.
 
 - **test case**: The **case id** of the test case.
 - **train case {1,2,3,4}**: The **case id** of the n-th training case closest to the **test case**.
