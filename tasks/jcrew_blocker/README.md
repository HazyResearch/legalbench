# jcrew_blocker 

 **Contributor**: Enam Hoque
 
 **Source**: Enam Hoque
 
 **License**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
 
 **Task summary**: Classify if a clause in a loan agreement is a JCrew blocker provision.
 
 **Size (samples)**: 60
 
 ## Task Description
 
The JCrew Blocker, also known as the JCrew Protection, is a provision included in leveraged loan documents to prevent companies from removing security by transferring intellectual property (IP) into new subsidiaries and raising additional debt. This provision was created after the company J.Crew used a "back-door" provision in its credit facility in 2016 to transfer highly valuable IP to an unrestricted subsidiary with the intent of using that IP as collateral for new debt.

The JCrew Blocker typically includes the following provisions:

- A prohibition on the borrower from transferring IP to an unrestricted subsidiary.
- A requirement that the borrower obtains the consent of its agent/lenders before transferring IP to any subsidiary.

The JCrew Blocker is designed to protect lenders from being blindsided by a borrower's attempt to remove material assets from the collateral pool.

The JCrew Blocker has been widely adopted by lenders in the leveraged loan market. It is an important tool for protecting lenders from borrowers who may try to game the system. 

 ## Task Construction
 
The data set consists of 50+ real-life text examples of JCrew Blocker provisions extracted from various publicly-sourced loan documents and curated by legal experts.

The data set is organized into two columns:

- `Text`: Contains the text of the "JCrew Blocker" provision found in the loan document.
- `Label`: Indicates whether the provision meets the criteria of a JCrew Blocker provision (Yes/No).
