# nys_judicial_ethics 

### Answer questions on judicial ethics from the New York State Unified Court System Advisory Committee.
---



**Source**: Peter Henderson

**License**: MIT

**Size (samples)**: 300

**Legal reasoning type**: Rule-recall

**Task type**: Binary classification

## Task description

The New York State Unified Court System Advisory Committee posts rulings on real ethical scenarios. These have been reformulated into Yes/No questions for judicial ethics to understand whether models understand ethical rules and how they might apply to different judicial situations.

## Dataset construction

We collect digest statements from the New York State Unified Court System Advisory Committee on Judicial Ethics (<https://www.nycourts.gov/legacyhtm/ip/judicialethics/opinions/>). We collect samples from 2010, 2021, 2022, and 2023 and then use ChatGPT to reformulate the statements into yes or no questions. To ensure that data is not used for training OpenAI models, we opt out of data use for accounts used for task creation. We leave 2010 and 2021 data for understanding scope of data leakage from opinions being online. 2022 and 2023 data should not have been seen by most models that were trained prior to these years.

## Data column names

- `question`: question
- `answer`: Yes/No answer
- `year`: year of exam 