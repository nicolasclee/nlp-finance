# Seleção na validação, sem consultar previsões do teste.

from __future__ import annotations

import math
from collections.abc import Sequence
from fractions import Fraction


# Escolhe a época pela acurácia, Macro-F1 e, em último empate, pela mais antiga.
def select_epoch(epochs: Sequence[dict]) -> dict:
    if not epochs:
        raise ValueError("Nenhuma época disponível para seleção")
    for epoch in epochs:
        valid_counts = epoch["total"] > 0 and 0 <= epoch["correct"] <= epoch["total"]
        if not valid_counts or not math.isfinite(epoch["macro_f1"]):
            raise ValueError("Métricas de validação devem ser finitas")

    def ranking(epoch: dict) -> tuple:
        accuracy = Fraction(epoch["correct"], epoch["total"])
        # Uma época menor vence quando acurácia e Macro-F1 empatam.
        return accuracy, epoch["macro_f1"], -epoch["epoch"]

    return max(epochs, key=ranking)


# Escolhe a taxa pelas médias das três execuções de validação.
def select_rate(runs_by_rate: dict[float, Sequence[dict]]) -> float:
    if len(runs_by_rate) != 2:
        raise ValueError("São necessárias as duas taxas previstas")
    if set(runs_by_rate) != {2e-5, 5e-5}:
        raise ValueError("As taxas devem ser 2e-5 e 5e-5")
    for rate, runs in runs_by_rate.items():
        if len(runs) != 3 or {run["seed"] for run in runs} != {13, 37, 73}:
            raise ValueError(f"Taxa {rate}: são necessárias as três sementes previstas")
        for run in runs:
            valid_counts = run["total"] > 0 and 0 <= run["correct"] <= run["total"]
            if not valid_counts or not math.isfinite(run["macro_f1"]):
                raise ValueError(f"Taxa {rate}: métricas devem ser finitas")

    def ranking(rate: float) -> tuple:
        runs = runs_by_rate[rate]
        accuracies = [Fraction(run["correct"], run["total"]) for run in runs]
        average_accuracy = sum(accuracies) / len(runs)
        average_f1 = sum(run["macro_f1"] for run in runs) / len(runs)
        # Taxa menor vence se as duas médias empatarem.
        return average_accuracy, average_f1, -rate

    return max(runs_by_rate, key=ranking)
