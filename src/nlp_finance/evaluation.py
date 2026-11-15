# Avalia previsões e seleciona limiares apenas na validação.

import math

import numpy as np
from sklearn.metrics import precision_recall_fscore_support

from .constants import NUM_LABELS
from .abstention_metrics import aurc, ece, selective_result, threshold_for_coverage


# Calcula scores MSP e margem a partir das mesmas probabilidades.
def prediction_scores(predictions: dict) -> dict:
    probabilities = predictions["probabilities"]
    predicted = np.argmax(probabilities, axis=1)
    correct = predicted == predictions["labels"]
    sorted_probabilities = np.sort(probabilities, axis=1)
    highest = sorted_probabilities[:, -1]
    margin = highest - sorted_probabilities[:, -2]
    return {"predicted": predicted, "correct": correct, "msp": highest, "margin": margin}


# Obtém um limiar por regra e meta, usando exclusivamente previsões de validação.
def select_thresholds(validation_predictions: dict) -> dict:
    scores = prediction_scores(validation_predictions)
    thresholds = {}
    for rule in ("msp", "margin"):
        values = scores[rule].tolist()
        thresholds[rule] = {}
        for target in (0.95, 0.90, 0.80):
            threshold = threshold_for_coverage(values, target)
            result = selective_result(values, scores["correct"].tolist(), threshold)
            thresholds[rule][str(target)] = {
                "threshold": threshold,
                "target": target,
                "validation_coverage": result["coverage"],
                "ties_at_threshold": sum(value == threshold for value in values),
            }
    return thresholds


# Resume a classificação, incluindo as 77 intenções mesmo sem exemplos previstos.
def classification_metrics(labels, predicted) -> dict:
    if len(labels) == 0 or len(labels) != len(predicted):
        raise ValueError("Rótulos e previsões devem ter o mesmo tamanho não vazio")

    precisions, recalls, f1_scores, supports = precision_recall_fscore_support(
        labels, predicted, labels=list(range(NUM_LABELS)), zero_division=0
    )
    predicted_counts = np.bincount(predicted, minlength=NUM_LABELS)
    per_class = []
    for label in range(NUM_LABELS):
        actual = int(supports[label])
        predicted_count = int(predicted_counts[label])
        per_class.append({
            "label_id": label, "support": actual, "predicted": predicted_count,
            "precision": float(precisions[label]), "recall": float(recalls[label]),
            "f1": float(f1_scores[label]),
            "undefined_precision": predicted_count == 0,
            "undefined_recall": actual == 0,
            "undefined_f1": actual + predicted_count == 0,
        })
    return {
        "accuracy": float(np.mean(labels == predicted)),
        "macro_f1": sum(item["f1"] for item in per_class) / NUM_LABELS,
        "per_class": per_class,
    }


# Produz pontos apenas ao final de cada grupo de pontuações empatadas.
def risk_coverage_curve(scores, correct) -> list[dict]:
    if len(scores) == 0 or len(scores) != len(correct):
        raise ValueError("Scores e acertos devem ter o mesmo tamanho não vazio")
    if not all(math.isfinite(float(score)) for score in scores):
        raise ValueError("Scores precisam ser finitos")

    ordered = sorted(zip(scores, correct), key=lambda pair: pair[0], reverse=True)
    points = []
    errors = 0
    for index, (score, is_correct) in enumerate(ordered):
        errors += not is_correct
        last_in_group = index == len(ordered) - 1 or ordered[index + 1][0] != score
        if last_in_group:
            accepted = index + 1
            points.append({"coverage": accepted / len(ordered), "error": errors / accepted})
    return points


# Avalia as regras usando limiares já escolhidos; não reajusta a cobertura.
def evaluate_predictions(predictions: dict, thresholds: dict) -> dict:
    scores = prediction_scores(predictions)
    correct = scores["correct"].tolist()
    result = classification_metrics(predictions["labels"], scores["predicted"])
    result["ece"] = ece(scores["msp"].tolist(), correct)
    result["rules"] = {}
    for rule in ("msp", "margin"):
        values = scores[rule].tolist()
        rule_result = {
            "aurc": aurc(values, correct),
            "curve": risk_coverage_curve(values, correct),
            "targets": {},
        }
        for target, details in thresholds[rule].items():
            rule_result["targets"][target] = selective_result(values, correct, details["threshold"])
        result["rules"][rule] = rule_result
    return result
