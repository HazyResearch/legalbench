# ucc_v_common_law 
 **Contributor**: Spencer Williams
 
 **Source**: Spencer Williams
 
 **License**: [CC By 4.0](https://creativecommons.org/licenses/by/4.0/)
 
 **Task summary**: Determine if a contract is governed by the Uniform Commercial Code (UCC) or the common law of contracts.
 
 **Size (samples)**: 100
 
 ## Task Description
 
 The purpose of this task is to determine whether a contract is governed by the Uniform Commercial Code (UCC) or the common law of contracts. The UCC (through Article 2) governs the sale of goods, which are defined as moveable tangible things (cars, apples, books, etc.), whereas the common law governs contracts for real estate and services.
 
 Some contracts contain both goods and services, such as a contract for the purchase of a car which also includes a year of free maintenance. For simplicity, this task ignores the existence of these "mixed purpose" contracts.
 
 ## Dataset construction
 
 The dataset consists of 100 descriptions of simple contracts such as "Bob agrees to mow Alice's lawn for $20." Each contract description ends with the following question: "Is this contract governed by the UCC or the common law?" For each contract description, the dataset lists whether the contract is governed by the "UCC" or the "Common Law." The dataset was constructed by hand.