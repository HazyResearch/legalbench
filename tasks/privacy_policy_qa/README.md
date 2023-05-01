# privacy_policy_qa 
 **Contributor**: Neel Guha
 
 **Source**: [Privacy Q&A Corpus](https://github.com/AbhilashaRavichander/PrivacyQA_EMNLP)
 
 **License**: [MIT](https://github.com/AbhilashaRavichander/PrivacyQA_EMNLP/blob/master/LICENSE)
 
 **Task summary**: Determine if a clause in a privacy policy contains the answer to a given question.
 
 **Size (samples)**: 10992
 
 ## Task Description
 
 This is a binary classification task in which the LLM is provided with a question (e.g., "do you publish my data") and a clause from a privacy policy. The LLM must determine if the clause contains an answer to the question, and classify the question-clause pair as `Relevant` or `Irrelevant`.  
 
 ## Task Construction
 
 This task was constructed from the test split of the [PrivacyQA](https://github.com/AbhilashaRavichander/PrivacyQA_EMNLP) dataset. Please see the [original paper](https://arxiv.org/abs/1911.00841) for more details.