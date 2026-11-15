# Consolida os resultados individuais, tabelas e figuras do experimento.

import csv
import json
import statistics
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

from .data import sha256
from .dataset import load_prepared_data
from .evaluation import prediction_scores
from .predictions import load_predictions


# Escreve uma tabela preservando a ordem explícita das colunas.
def write_table(path: Path, rows: list[dict], columns: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


# Resume uma métrica entre as três seeds sem interpretar dispersão como significância.
def summarize(values) -> dict:
    return {"mean": statistics.mean(values), "sample_std": statistics.stdev(values)}


# Extrai os pares de intenções mais confundidos, preservando a direção dos erros.
def confusion_pairs(runs: list[dict]) -> tuple[list[tuple], dict]:
    counts = Counter()
    directions = Counter()
    for run in runs:
        labels = run["predictions"]["labels"]
        predicted = run["scores"]["predicted"]
        for label, prediction in zip(labels.tolist(), predicted.tolist()):
            if label != prediction:
                pair = tuple(sorted((label, prediction)))
                counts[pair] += 1
                directions[(label, prediction)] += 1
    ranked = sorted(counts, key=lambda pair: (-counts[pair], pair))[:5]
    details = {
        f"{a}-{b}": {
            "total": counts[(a, b)],
            "a_to_b": directions[(a, b)],
            "b_to_a": directions[(b, a)],
        }
        for a, b in ranked
    }
    return ranked, details


# Seleciona exemplos para leitura humana sem tratá-los como amostra representativa.
def qualitative_examples(examples, all_runs: dict, pairs: list[tuple]) -> list[dict]:
    selected = []
    for pair in pairs:
        candidates = []
        for index, example in enumerate(examples):
            decisions = {}
            recurring_accepted = False
            rejected = False
            for model, runs in all_runs.items():
                decisions[model] = []
                matching_errors = 0
                accepted_error = False
                for run in runs:
                    prediction = int(run["scores"]["predicted"][index])
                    label = int(example["label_id"])
                    same_pair_error = label != prediction and tuple(sorted((label, prediction))) == pair
                    matching_errors += int(same_pair_error)
                    rule_details = {}
                    for rule in ("msp", "margin"):
                        score = float(run["scores"][rule][index])
                        threshold = run["frozen"]["thresholds"][rule]["0.9"]["threshold"]
                        rule_details[rule] = {"score": score, "accepted": score >= threshold}
                    if same_pair_error:
                        accepted_error |= any(value["accepted"] for value in rule_details.values())
                        rejected |= any(not value["accepted"] for value in rule_details.values())
                    decisions[model].append({"seed": run["frozen"]["seed"], "prediction": prediction, **rule_details})
                recurring_accepted |= matching_errors >= 2 and accepted_error
            if recurring_accepted or rejected:
                priority = 0 if recurring_accepted else 1
                candidates.append((priority, example["id"], example, decisions))
        for _, _, example, decisions in sorted(candidates, key=lambda item: (item[0], item[1]))[:2]:
            selected.append({"pair": list(pair), "id": example["id"], "text": example["text"],
                             "label_id": example["label_id"], "decisions": decisions})
    return selected


# Gera tabelas, curvas por seed, diagramas de confiança e exemplos de erro.
def create_report(preparation: Path, frozen_path: Path, evaluation_dir: Path, output: Path) -> None:
    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    if sha256(preparation / "manifest.json") != frozen["preparation_hash"]:
        raise ValueError("A preparação não corresponde ao protocolo congelado")
    summary_file = evaluation_dir / "summary.json"
    summary = json.loads(summary_file.read_text(encoding="utf-8"))
    if summary["frozen_sha256"] != sha256(frozen_path):
        raise ValueError("A avaliação não corresponde ao protocolo congelado")
    splits, _ = load_prepared_data(preparation)
    test_examples = splits["test"]
    output.mkdir(parents=True, exist_ok=False)
    all_runs = {}
    classification_rows = []
    selective_rows = []
    aggregate = {}
    pairs_by_model = {}
    baseline = json.loads((evaluation_dir / summary["baseline"]).read_text(encoding="utf-8"))
    classification_rows.append({
        "model": "majority_baseline", "seed": "", "accuracy": baseline["accuracy"],
        "macro_f1": baseline["macro_f1"], "ece": "",
    })

    for model, selection in frozen["selected"].items():
        all_runs[model] = []
        for run in selection["runs"]:
            name = f"{model.replace('/', '_')}_seed_{run['seed']}"
            predictions = load_predictions(evaluation_dir / f"{name}.npz")
            if predictions["ids"].tolist() != [item["id"] for item in test_examples]:
                raise ValueError(f"IDs de teste inesperados em {name}")
            if predictions["labels"].tolist() != [item["label_id"] for item in test_examples]:
                raise ValueError(f"Rótulos de teste inesperados em {name}")
            metrics = json.loads((evaluation_dir / f"{name}.json").read_text(encoding="utf-8"))
            scores = prediction_scores(predictions)
            all_runs[model].append({"frozen": run, "predictions": predictions, "scores": scores, "metrics": metrics})
            classification_rows.append({
                "model": model, "seed": run["seed"], "accuracy": metrics["accuracy"],
                "macro_f1": metrics["macro_f1"], "ece": metrics["ece"]["ece"],
            })
            selective_rows.append({
                "model": model, "seed": run["seed"], "rule": "no_abstention", "target": "1.0",
                "coverage": 1.0, "error": 1 - metrics["accuracy"], "aurc": None,
            })
            for rule, details in metrics["rules"].items():
                for target, values in details["targets"].items():
                    selective_rows.append({"model": model, "seed": run["seed"], "rule": rule,
                                           "target": target, "coverage": values["coverage"],
                                           "error": values["error"], "aurc": details["aurc"]})

        metrics = [run["metrics"] for run in all_runs[model]]
        aggregate[model] = {
            "accuracy": summarize([item["accuracy"] for item in metrics]),
            "macro_f1": summarize([item["macro_f1"] for item in metrics]),
            "ece": summarize([item["ece"]["ece"] for item in metrics]),
            "aurc": {rule: summarize([item["rules"][rule]["aurc"] for item in metrics])
                     for rule in ("msp", "margin")},
        }
        aggregate[model]["operating_points"] = {}
        for rule in ("msp", "margin"):
            aggregate[model]["operating_points"][rule] = {}
            for target in ("0.95", "0.9", "0.8"):
                points = [item["rules"][rule]["targets"][target] for item in metrics]
                errors = [point["error"] for point in points]
                aggregate[model]["operating_points"][rule][target] = {
                    "coverage": summarize([point["coverage"] for point in points]),
                    "error": summarize(errors) if all(error is not None for error in errors) else None,
                    "undefined_error_runs": sum(error is None for error in errors),
                }
        ranked, details = confusion_pairs(all_runs[model])
        pairs_by_model[model] = {"ranked": ranked, "details": details}

        for rule in ("msp", "margin"):
            fig, axis = plt.subplots()
            for run in all_runs[model]:
                points = run["metrics"]["rules"][rule]["curve"]
                axis.plot([point["coverage"] for point in points], [point["error"] for point in points],
                          label=f"seed {run['frozen']['seed']}")
            axis.set(xlabel="Cobertura", ylabel="Erro seletivo", title=f"{model}: {rule}")
            axis.legend()
            fig.tight_layout()
            fig.savefig(output / f"{model.replace('/', '_')}_{rule}_risk.svg")
            plt.close(fig)

        fig, axis = plt.subplots()
        for run in all_runs[model]:
            bins = [item for item in run["metrics"]["ece"]["bins"] if item["count"]]
            axis.plot([item["confidence"] for item in bins], [item["accuracy"] for item in bins],
                      marker="o", label=f"seed {run['frozen']['seed']}")
        axis.plot([0, 1], [0, 1], linestyle="--", color="gray")
        axis.set(xlabel="Confiança média", ylabel="Acurácia", title=model, xlim=(0, 1), ylim=(0, 1))
        axis.legend()
        fig.tight_layout()
        fig.savefig(output / f"{model.replace('/', '_')}_reliability.svg")
        plt.close(fig)

    pairs = sorted({pair for item in pairs_by_model.values() for pair in item["ranked"]})
    qualitative = qualitative_examples(test_examples, all_runs, pairs)
    write_table(output / "classification.csv", classification_rows, ["model", "seed", "accuracy", "macro_f1", "ece"])
    write_table(output / "abstention.csv", selective_rows, ["model", "seed", "rule", "target", "coverage", "error", "aurc"])
    for name, content in (("aggregate.json", aggregate), ("confusions.json", pairs_by_model),
                          ("examples.json", qualitative)):
        (output / name).write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
