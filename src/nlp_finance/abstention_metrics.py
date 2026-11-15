# Regras de abstenção e métricas com convenções do protocolo O6–O7.

from __future__ import annotations

import math
from collections.abc import Sequence


# Confere se as pontuações e os indicadores de acerto são compatíveis.
def _validate(scores: Sequence[float], correct: Sequence[bool]) -> None:
    if not scores or len(scores) != len(correct):
        raise ValueError("Scores e acertos devem ter o mesmo tamanho não vazio")
    if any(not math.isfinite(value) for value in scores):
        raise ValueError("Scores devem ser finitos")


# Escolhe o limiar de confiança para alcançar ao menos a cobertura desejada.
def threshold_for_coverage(scores: Sequence[float], coverage: float) -> float:
    if not scores or not 0 < coverage <= 1 or any(not math.isfinite(x) for x in scores):
        raise ValueError("Informe scores finitos e cobertura no intervalo (0, 1]")
    scores_from_highest = sorted(scores, reverse=True)
    desired_count = math.ceil(coverage * len(scores))
    return scores_from_highest[desired_count - 1]


# Calcula cobertura e erro dos exemplos aceitos pelo limiar.
def selective_result(scores: Sequence[float], correct: Sequence[bool], threshold: float) -> dict:
    _validate(scores, correct)
    if not math.isfinite(threshold):
        raise ValueError("Limiar deve ser finito")
    accepted = [ok for score, ok in zip(scores, correct) if score >= threshold]
    accepted_count = len(accepted)
    error_count = sum(not ok for ok in accepted)
    error_rate = error_count / accepted_count if accepted else None
    return {
        "coverage": accepted_count / len(scores),
        "accepted": accepted_count,
        "error": error_rate,
    }


# Resume o risco em diferentes coberturas, considerando empates nas pontuações.
def aurc(scores: Sequence[float], correct: Sequence[bool]) -> float:
    _validate(scores, correct)
    ordered = sorted(zip(scores, correct), key=lambda pair: pair[0], reverse=True)
    total_risk = 0.0
    preceding = 0
    errors_before = 0
    while preceding < len(ordered):
        end = preceding + 1
        while end < len(ordered) and ordered[end][0] == ordered[preceding][0]:
            end += 1
        size = end - preceding
        errors = sum(not ok for _, ok in ordered[preceding:end])
        # Para cada posição do empate, usa a quantidade esperada de erros.
        for position in range(1, size + 1):
            expected_errors = errors_before + position * errors / size
            examples_seen = preceding + position
            total_risk += expected_errors / examples_seen
        preceding = end
        errors_before += errors
    return total_risk / len(ordered)


# Compara a confiança média com a frequência de acertos em cada faixa.
def ece(confidence: Sequence[float], correct: Sequence[bool], bins: int = 15) -> dict:
    _validate(confidence, correct)
    if bins <= 0 or any(value < 0 or value > 1 for value in confidence):
        raise ValueError("Confianças devem estar entre 0 e 1 e o número de faixas deve ser positivo")
    groups: list[list[tuple[float, bool]]] = [[] for _ in range(bins)]
    for value, ok in zip(confidence, correct):
        groups[min(int(value * bins), bins - 1)].append((value, ok))
    result = []
    error = 0.0
    for group in groups:
        if group:
            mean_confidence = sum(value for value, _ in group) / len(group)
            accuracy = sum(ok for _, ok in group) / len(group)
            error += len(group) / len(confidence) * abs(mean_confidence - accuracy)
            result.append({"count": len(group), "confidence": mean_confidence, "accuracy": accuracy})
        else:
            result.append({"count": 0, "confidence": None, "accuracy": None})
    return {"ece": error, "bins": result}
