# jcrew_blocker 

### Classify if a clause in a loan agreement is a J.Crew blocker provision.
---


**Source**: Enam Hoque

**License**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 60

**Legal reasoning type**: Interpretation

**Task type**: Binary classification

## Task description

The J.Crew Blocker, also known as the J.Crew Protection, is a provision included in leveraged loan documents to prevent companies from removing security by transferring intellectual property (IP) into new subsidiaries and raising additional debt. This provision was created after the company J.Crew used a "back-door" provision in its credit facility in 2016 to transfer highly valuable IP to an unrestricted subsidiary with the intent of using that IP as collateral for new debt.

The J.Crew Blocker typically includes the following provisions:

- A prohibition on the borrower from transferring IP to an unrestricted subsidiary.
- A requirement that the borrower obtains the consent of its agent/lenders before transferring IP to any subsidiary.

The J.Crew Blocker is designed to protect lenders from being blindsided by a borrower's attempt to remove material assets from the collateral pool.

The J.Crew Blocker has been widely adopted by lenders in the leveraged loan market. It is an important tool for protecting lenders from borrowers who may try to game the system. 

## Task construction

The data set consists of 50+ real-life text examples of J.Crew Blocker provisions extracted from various publicly-sourced loan documents and curated by legal experts.


## Data column names

The data set is organized into two columns:

- `text`: Contains the text of a provision found in the loan document.
- `answer`: Indicates whether the provision meets the criteria of a J.Crew Blocker provision (Yes/No).
