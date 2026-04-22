import re
from evaluation import (
    normalize
)

def evaluate_exact_match(output: dict, answer: str):
    """
    [Evaluates single example, implementation borrowed from evaluation.py]
    Evaluates exact match.
    """

    return answer == output

def evaluate_sara_within_10pt(output: str, answer: str) -> int:
    """
    [Evaluates single example, implementation borrowed from evaluation.py]
    Return 1 if the first number in *output* is within ±10 % of *answer*, else 0.
    """

    sentence = str(output).replace(",", "").replace(".", "")
    m = re.search(r"\d+", sentence)

    prediction: float = float(m.group()) if m else 0.0
    target: float = float(answer.replace("$", ""))

    correct = abs(prediction / (target + 1e-1) - 1.0) < 0.1
    return int(correct)

def evaluate_successor_liability_f1_single_example(output: str, answer: str):
    """
    [Evaluates single example, implementation borrowed from evaluation.py]
    For successor liability, we measure F1 over the predicted exceptions.
    """
    CLASSES = [
        "express agreement",
        "fraudulent conveyance",
        "de facto merger",
        "mere continuation",
    ]
    tp, fp, fn = 0, 0, 0
    predictions = [c for c in CLASSES if c in str(output)]
    sample_answers = str(answer).split(",")

    for j in range(len(predictions)):
        if predictions[j] in sample_answers:
            index = sample_answers.index(predictions[j])
            del sample_answers[index]
            tp += 1
        else:
            fp += 1
    fn += len(sample_answers)
    return tp, fp, fn # return raw results for calculating micro-f1 both per row and later for entire task

def evaluate_citation_open_single_example(output: str, answer: str):
    """
    Example-level correctness for the open-citation task.
    Returns 1.0 if the (normalized) gold case name appears anywhere
    in the (normalized) generation; else 0.0.
    """

    normalized_answer = normalize(answer, stem=False)
    normalized_output = normalize(output, stem=False)
    
    return 1.0 if normalized_answer in normalized_output else 0.0

def evaluate_definition_extraction_single_row(output: str, answer: str):
    """
    desc
    """

    answers_list = answer.split(",")
    generations_list = output.split(",")
    normalized_answers = [normalize(a, stem=True) for a in answers_list]
    normalized_outputs = [normalize(g, stem=True) for g in generations_list]

    for gen in normalized_outputs:
        if gen in normalized_answers:
            return 1.0
    return 0.0

def evaluate_ssla_row(output: str, answer: str):
    """
    Row-level TP / FP / FN for the SSLA tasks.
    Mirrors the benchmark’s logic exactly, just scoped to one example.
    """

    answers_split = answer.split(",")
    outputs_split = str(output).split(",")

    normalized_answers = [normalize(a, stem=False) for a in answers_split]
    normalized_outputs = [normalize(g, stem=False) for g in outputs_split]

    tp = fp = fn = 0

    for a in normalized_answers:
        found = False
        for j, g in enumerate(normalized_outputs):
            if a in g:
                tp += 1
                found = True
                break
        if found:
            del normalized_outputs[j]
        else:
            fn += 1

    fp += len(normalized_outputs)
    return tp, fp, fn