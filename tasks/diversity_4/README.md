# diversity_4 

### Given a set of facts about the citizenships of plaintiffs and defendants and the amounts associated with claims, determine if the criteria for diversity jurisdiction have been met (variant 4).
---



**Source**: Neel Guha

**License**: [CC By 4.0](https://creativecommons.org/licenses/by/4.0/)

**Legal reasoning type**: Rule-application/Rule-conclusion

**Task type**: Binary classification

## Task description

Diversity jurisdiction is one way in which a federal court may have jurisdiction over claims arising from state law. Diversity jurisdiction exists when there is (1) complete diversity between plaintiffs and defendants, and (2) the amount-in-controversy (AiC) is greater than \$75k.
"Complete diversity" requires that there is no pair of plaintiff and defendant that are citizens of the same state. However, it is acceptable for multiple plaintiffs to be from the same state, or for multiple defendants to be from the same state. AiC is the amount of damages being sued for. The AiC requirement allows for certain forms of aggregation. Specifically, if plaintiff A asserts two independent claims against defendant B, the value of the claims may be added together when considering if the AiC requirement is met. However, a plaintiff may not aggregate the value of claims against two separate defendants, and two plaintiffs may not aggregate claims against the same defendant.

In variant 4, there are two plaintiffs, one defendant, and one claim per plaintiff-defendant pair.


## Dataset construction

We constructed a dataset to evaluate diversity jurisdiction by creating synthetic fact patterns describing individual(s), their citizenships, and the amounts being sued for. Each diversity task corresponds to a different type of fact pattern. In this version, we test fact patterns consisting of two plaintiffs asserting one claim each against one defendant. Fact patterns are generated with random amounts, citizenships, claim types, and party names. For each sample, we additionally provide whether or not the AiC is met (`aic_is_met`) and whether or not the parties are diverse (`parties_are_diverse`).

## Data column names

- `text`: fact pattern describing the parties citizenship and claims
- `answer`: whether there is diversity jurisdiction (Yes) or not (No)
- `parties_are_diverse`: whether the parties are diverse (True/False) 
- `aic_is_met`: whether the amount-in-controversy is met (True/False)