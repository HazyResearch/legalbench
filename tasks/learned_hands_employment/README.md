# learned_hands_employment

### Classify if a user post implicates legal isssues related to employment.
---



**Source**: [Learned Hands](https://spot.suffolklitlab.org/data/#learnedhands)

**License**: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

**Size (samples)**: 716

**Legal reasoning type**: Issue-spotting

**Task type**: Binary classification

## Task description

This is a binary classification task in which the model must determine if a user's post discusses issues related to working at a job, including discrimination and harassment, worker's compensation, workers rights, unions, getting paid, pensions, being fired, and more.

## Task construction

This task was constructed from the [LearnedHands](https://suffolklitlab.org/) dataset. Please see their website for more information on annotation. Our task consists of a binarized version of the original dataset, with "negatives" randomly sampled from posts with other topics. This dataset is class balanced.

## Data column names

- `text`: user post
- `answer`: class label (Yes/No)