# personal_jurisdiction 

### Given a fact pattern describing the set of contacts between a plaintiff, defendant, and forum, determine if a court in that forum could excercise personal jurisdiction over the defendant.
---


**Source**: Neel Guha

**License**: [CC by 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 50

**Legal reasoning type**: Rule-application/Rule-conclusion

**Task type**: Binary classification

## Task description

Personal jurisdiction refers to the ability of a particular court (e.g. a court in the Northern District of California) to preside over a dispute between a specific plaintiff and defendant~\todocite. A court (sitting in a particular forum) has personal jurisdiction over a defendant only when that defendant has a relationship with the forum. We focus on a simplified version of the rule for federal personal jurisdiction, using the rule:

```text
There is personal jurisdiction over a defendant in the state where the defendant is domiciled, or when (1) the defendant has sufficient contacts with the state, such that they have availed themselves of the privileges of the state and (2) the claim arises out of the nexus of the defendant's contacts with the state.
```

Under this rule, there are two paths for a court have jurisdiction over a defendant: through domicile or through contacts.

- **Domicile**: A defendant is domiciled in a state if they are a citizen of the state (i.e. they live in the state). Changing residency affects a change in citizenship.
- **Contacts**:  Alternatively, a court may exercise jurisdiction over a defendant when that defendant has *sufficient contacts* with the court's forum, and the legal claims asserted arise from the \textit{nexus} of the defendant's contacts with the state. In evaluating whether a set of contacts are sufficient, lawyers look at the extent to which the defendant interacted with the forum, and availed themselves of the benefits and privileges of the state's laws. Behavior which usually indicates sufficient contacts include: marketing in the forum or selling/shipping products into the forum. In assessing nexus, lawyers ask if the claims brought against the defendant arise from their contacts with the forum. In short: is the conduct being litigated involve the forum or its citizens in some capacity?

## Dataset Construction

We manually construct a dataset to test application of the personal jurisdiction rule, drawing inspiration from exercises found online and in legal casebooks. Each sample in our dataset describes a ``fact pattern," and asks if a court located in particular state (**A**) can exercise personal jurisdiction over an individual (**B**) named in the fact pattern. In designing the dataset, we use 5 base fact patterns, and create 4 slices, where each slice evaluates a different aspect of the personal jurisdiction rule:

- Domicile: Fact patterns where **B** is domiciled in **A**. Hence, personal jurisdiction exists.
- No contacts: Fact patterns where **B** has insufficient contacts with **A**. Hence there is no personal jurisdiction.
- Yes contacts, no nexus: Fact patterns where **B** has sufficient contacts with **A**, but the claims against **B** do not arise from those contacts. Hence, personal jurisdiction does not exist.
- Yes contacts, yes nexus: Fact patterns where **B** has sufficient contacts with **A**, and the claims against **B** arise from those contacts. Hence, there is personal jurisdiction.

**Caveat**. Personal jurisdiction is a rich and complex doctrine. Our dataset focuses on a narrow class of fact patterns, related to jurisdiction over individuals. We don't consider, for instance, more complex questions related to adjudicating citizenship (e.g. the *Hertz* test) or the classic stream-of-commerce problems. We leave this to future work.

## Data column names

- `label`: whether personal jurisdiction over the defendant exists ("Yes") or doesn't ("No")
- `text`: a fact pattern describing a plaintiff and defendant's relationship to each other and a particular set of forums
- `slice`: the slice for the fact pattern