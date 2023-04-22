# contract_nli_limited_use 
 **Contributor**: Neel Guha
 
 **Source**: [ContractNLI](https://stanfordnlp.github.io/contract-nli/)
 
 **License**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
 
 **Task summary**: Identify if the clause provides that the Receiving Party shall not use any Confidential Information for any purpose other than the purposes stated in Agreement.
 
 **Size (samples)**: 220
 
 ## Task Description
 
 This task is a subset of ContractNLI, and consists of determinining whether a clause from an NDA has a particular legal effect.
 
 ## Task Construction
 
 This task was constructed from the ContractNLI dataset, which originally annotated clauses from NDAs based on whether they entailed, contradicted, or neglgected to mention a hypothesis. We binarized this dataset, treating contradictions and failures to mention as the negative label. We used the hypothesis provided as the prompt. Please see the original paper for more information on construction. All samples are drawn from the test set.