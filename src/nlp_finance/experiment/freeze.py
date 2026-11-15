# Congela escolhas feitas na validação antes da avaliação final.

import json
from pathlib import Path

from ..data import sha256
from ..dataset import load_prepared_data
from ..evaluation import classification_metrics, prediction_scores, select_thresholds
from ..model_selection import select_epoch, select_rate
from ..predictions import load_predictions


MODELS = ("google-bert/bert-base-uncased", "yiyanghkust/finbert-pretrain")
RATES = (2e-5, 5e-5)
SEEDS = (13, 37, 73)


# Lê uma tentativa concluída e confere seus dados de validação e checkpoint.
def read_completed_run(directory: Path, validation: list[dict], preparation_hash: str) -> dict:
    config = json.loads((directory / "config.json").read_text(encoding="utf-8"))
    status = json.loads((directory / "result.json").read_text(encoding="utf-8"))
    history = json.loads((directory / "epochs.json").read_text(encoding="utf-8"))
    if status["status"] != "completed" or [item["epoch"] for item in history] != [1, 2, 3, 4, 5]:
        raise ValueError(f"A tentativa {directory} não possui cinco épocas completas")
    if config.get("preparation_hash") != preparation_hash:
        raise ValueError(f"A tentativa {directory} usou outra preparação")

    best = select_epoch(history)
    if best["epoch"] != status["best_epoch"]:
        raise ValueError(f"O checkpoint selecionado de {directory} não corresponde ao histórico")
    prediction_file = directory / "validation_predictions.npz"
    predictions = load_predictions(prediction_file)
    if predictions["ids"].tolist() != [item["id"] for item in validation]:
        raise ValueError(f"As previsões de {directory} não usam os IDs esperados de validação")
    if predictions["labels"].tolist() != [item["label_id"] for item in validation]:
        raise ValueError(f"Os rótulos de {directory} não correspondem aos dados de validação")

    scores = prediction_scores(predictions)
    metrics = classification_metrics(predictions["labels"], scores["predicted"])
    if abs(metrics["accuracy"] - best["accuracy"]) > 1e-12 or abs(metrics["macro_f1"] - best["macro_f1"]) > 1e-12:
        raise ValueError(f"As métricas salvas e as previsões de {directory} não correspondem")

    return {
        "model": config["model_name"], "rate": config["learning_rate"], "seed": config["seed"],
        "config": config, "best": best, "checkpoint": str(directory / "best_model.pt"),
        "checkpoint_sha256": sha256(directory / "best_model.pt"),
        "validation_predictions": str(prediction_file),
        "validation_predictions_sha256": sha256(prediction_file),
    }


# Confere as 12 execuções, seleciona uma taxa por modelo e salva as escolhas.
def freeze_protocol(preparation: Path, run_directories: list[Path], output: Path) -> dict:
    if len(run_directories) != 12:
        raise ValueError("O congelamento requer as 12 execuções completas planejadas")
    manifest_file = preparation / "manifest.json"
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    splits, _ = load_prepared_data(preparation)
    preparation_hash = sha256(manifest_file)
    runs = [read_completed_run(path, splits["validation"], preparation_hash) for path in run_directories]

    expected = {(model, rate, seed) for model in MODELS for rate in RATES for seed in SEEDS}
    observed = {(run["model"], run["rate"], run["seed"]) for run in runs}
    if observed != expected or len(observed) != len(runs):
        raise ValueError("As execuções não correspondem aos dois modelos, duas taxas e três seeds")

    for key in ("batch_size", "max_length", "precision", "diagnostic_hash"):
        values = {run["config"].get(key) for run in runs}
        if None in values or len(values) != 1:
            raise ValueError(f"As execuções precisam compartilhar {key}")
    for model in MODELS:
        revisions = {run["config"].get("revision") for run in runs if run["model"] == model}
        if None in revisions or len(revisions) != 1:
            raise ValueError(f"As execuções de {model} precisam compartilhar a revisão")

    chosen = {}
    for model in MODELS:
        runs_by_rate = {}
        for rate in RATES:
            runs_by_rate[rate] = [
                {"seed": run["seed"], **run["best"]}
                for run in runs if run["model"] == model and run["rate"] == rate
            ]
        selected_rate = select_rate(runs_by_rate)
        selected_runs = [run for run in runs if run["model"] == model and run["rate"] == selected_rate]
        for run in selected_runs:
            validation_predictions = load_predictions(Path(run["validation_predictions"]))
            run["thresholds"] = select_thresholds(validation_predictions)
        chosen[model] = {"rate": selected_rate, "runs": selected_runs}

    result = {
        "preparation_hash": preparation_hash,
        "split_sha256": manifest["split_sha256"],
        "selected": chosen,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
        file.write("\n")
    return result
