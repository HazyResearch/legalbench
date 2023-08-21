# oral_argument_question_purpose

### Given a question asked during oral argument, classify the purpose of the question.
---


 
**Source**: Gregory M. Dickinson

**License**: [CC by 4.0](https://creativecommons.org/licenses/by/4.0/)

**Size (samples)**: 319

**Legal reasoning type**: Rhetorical-analysis

**Task type**: 7-way classification

## Task description

This task classifies questions asked by Supreme Court justices at oral argument into seven categories:

1. Background - questions seeking factual or procedural information that is missing or not clear in the briefing
2. Clarification - questions seeking to get an advocate to clarify her position or the scope of the rule being advocated for
3. Implications - questions about the limits of a rule or its implications for future cases
4. Support - questions offering support for the advocate's position
5. Criticism - questions criticizing an advocate's position
6. Communicate - question designed primarily to communicate with other justices
7. Humor - questions designed to interject humor into the argument and relieve tension

## Task construction

Starting with oral arguments from the most recent term, and proceeding chronologically backwards, oral argument questions (utterances, really, not always actually questions) were classified manually into one of seven categories based on their apparent primary purpose. Human coders both read the written arguments and listened to audio recordings of the proceedings to improve coding accuracy.

The seven categories are drawn from Lawrence S. Wrightsman, Oral Arguments Before the Supreme Court (2008), which I also found useful in my own prior study of Supreme Court oral argument, A Computational Analysis of Oral Argument in the Supreme Court, 28 Cornell J.L. & Pub. Pol'y 449 (2019).

## Data column names
- `Docket No`: docket number for oral argument
- `question`: oral argument question
- `answer`: type for question