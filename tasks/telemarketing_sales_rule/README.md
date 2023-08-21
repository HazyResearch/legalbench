# telemarketing_sales_rule

### Determine how 16 C.F.R. § 310.3(a)(1) and 16 C.F.R. § 310.3(a)(2) (governing deceptive practices) apply to different fact patterns.
---


**Source**: Jonathan H. Choi

**License**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 52

**Legal reasoning type**: Application/conclusion

**Task type**: Binary classification

## Task description

The Telemarketing Sales Rule (16 C.F.R. Part 310) is a set of regulations promulgated by the Federal Trade Commission to implement the Telemarketing and Consumer Fraud and Abuse Prevention Act. Its purpose is to protect consumers from specified deceptive and abusive telemarketing practices. This task focuses on 16 C.F.R. § 310.3(a)(1) and 16 C.F.R. § 310.3(a)(2), which outline a series of specific telemarketing practices prohibited as "deceptive." 16 C.F.R. § 310.3(a)(1) lists information that must be disclosed to a consumer before a sale is made, and 16 C.F.R. § 310.3(a)(2) lists categories of information that a telemarketer is prohibited from misrepresenting. 16 C.F.R. § 310.2 provides definitions relevant to both of these subsections. 


## Task construction

This dataset is designed to test a model's ability to apply 16 C.F.R. § 310.3(a)(1) and 16 C.F.R. § 310.3(a)(2) of the Telemarketing Sales Rule to a simple fact pattern with a clear outcome. The dataset was created by hand, by creating simple fact patterns tied to a specific violation, or non-violation, of 16 C.F.R. § 310.3(a)(1) or 16 C.F.R. § 310.3(a)(2). Each fact pattern ends with the question: "Is this a violation of the Telemarketing Sales Rule?" Each fact pattern is paired with the answer "Yes" or the answer "No." Fact patterns are listed in the column "text," and answers are listed in the column "label."


## Data column names
 
 - `answer`: whether the telemarketing sales rule is violated
 - `text`: fact pattern