# privacy_policy_entailment 
 **Contributor**: Neel Guha
 
 **Source**: [APP-350 Corpus](https://github.com/AbhilashaRavichander/PrivacyQA_EMNLP)
 
 **License**: [CC BY-NC 3.0](https://creativecommons.org/licenses/by-nc/3.0/)
 
 **Task summary**: Determine if a description of a privacy policy clause is correct given that clause.
 
 **Size (samples)**: 4385
 
 ## Task Description
 
 This is a binary classification task in which the LLM is provided with a clause from a privacy policy, and a description of that clause (e.g., "The policy describes collection of the user's HTTP cookies, flash cookies, pixel tags, or similar identifiers by a party to the contract."). The LLM must determine if description of the clause is `Correct` or `Incorrect`.
 
 ## Task Construction
 
 This task was constructed from the test split of the [APP-350](https://usableprivacy.org/static/files/popets-2019-maps.pdf) dataset. Please see the original paper for more details.