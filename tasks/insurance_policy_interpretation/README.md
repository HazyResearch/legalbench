# insurance_policy_interpretation

### Given an insurance claim and policy, determine whether the claim is covered by the policy.
---

**Contributors**: Brandon Waldon (bwaldon@stanford.edu), Zehua Li (zehuali@stanford.edu), Megan Ma (meganma@law.stanford.edu)

**Source**: [Vague Contracts](https://github.com/madiganbrodsky/vague_contracts)

**License**: [CC By 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 138

**Legal reasoning type**: Interpretation

**Task type**: 3-way classification

## Task description

This is a multiple-choice task in which the model must answer whether an insurance claim is covered under a certain policy, or if the coverage is ambiguous.

## Task construction

This task was constructed from the list of insurance policy-claim pairs constructed by Madigan Brodsky (madiganb@stanford.edu). [Prolific](https://www.prolific.co) workers are recruited to review the policy-claim pairs and respond whether they believe a claim is covered under a given policy.

To convert the numbers of Yes/No/Can’t Decide responses to discrete labels, we first calculate the 95% multinomial confidence interval of the proportion of each response. We then choose the label for which the confidence interval lower bound is greater than or equal to .5. If no label has a lower bound ≥ .5, we classify the policy-claim pair as “It’s ambiguous.” This conversion process ensures that individual crowdsource workers do not arbitrarily sway the labels.

The task is formatted as a series of multiple-choice questions, where given an insurance policy and an insurance claim, the model is to choose whether an insurance claim is covered under a certain policy, or if the coverage is ambiguous.

```text
Read the insurance policy and the insurance claim. Answer whether the claim is covered under the policy with [A: Yes; B: No; C: It’s ambiguous]
```

## Data column names

- `policy`: insurance policy
- `claim`: insurnace claim
- `answer`: answer key to the question
