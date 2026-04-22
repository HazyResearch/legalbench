from sklearn.metrics import balanced_accuracy_score

def plain_accuracy(score_rows):
    correct = [row["correct"] for row in score_rows if "correct" in row]
    plain_accuracy = sum(correct) / len(correct) if correct else 0.0
    return plain_accuracy

def arithmetic_mean(score_rows):
    within = [row["within_10pt"] for row in score_rows if "within_10pt" in row]
    arithmetic_mean = sum(within) / len(within) if within else 0.0
    return arithmetic_mean

def balanced_accuracy(score_rows):
    gold = [row["normalized_answer"]     for row in score_rows]
    pred = [row["normalized_generation"] for row in score_rows]
    return balanced_accuracy_score(gold, pred)

def micro_f1(score_rows):
    tp_total = sum(row.get("tp", 0) for row in score_rows)
    fp_total = sum(row.get("fp", 0) for row in score_rows)
    fn_total = sum(row.get("fn", 0) for row in score_rows)
    denom = 2 * tp_total + fp_total + fn_total
    micro_f1 = (2 * tp_total / denom) if denom else 0.0
    return tp_total, fp_total, fn_total, micro_f1