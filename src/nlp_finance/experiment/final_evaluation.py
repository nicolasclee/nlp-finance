# Aplica ao teste somente checkpoints e limiares congelados na validação.

import json
from pathlib import Path

import numpy as np
import torch

from ..data import sha256
from ..dataset import load_prepared_data
from ..evaluation import classification_metrics, evaluate_predictions
from ..model import load_model
from ..predictions import load_predictions, predict, save_predictions
from ..tokenization import load_tokenizer, token_lengths


# Confere a preparação e gera resultados para as seis execuções selecionadas.
def evaluate_frozen(preparation: Path, frozen_path: Path, output: Path, device_name: str) -> None:
    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    if sha256(preparation / "manifest.json") != frozen["preparation_hash"]:
        raise ValueError("A preparação atual difere daquela congelada")
    splits, manifest = load_prepared_data(preparation)
    if manifest["split_sha256"] != frozen["split_sha256"]:
        raise ValueError("As divisões atuais diferem daquelas congeladas")

    device = torch.device(device_name)
    checked_lengths = set()

    # Confere todas as seis execuções antes de gerar qualquer previsão do teste.
    for model_name, selection in frozen["selected"].items():
        for run in selection["runs"]:
            if sha256(Path(run["checkpoint"])) != run["checkpoint_sha256"]:
                raise ValueError("O checkpoint difere daquele congelado")
            if sha256(Path(run["validation_predictions"])) != run["validation_predictions_sha256"]:
                raise ValueError("As previsões de validação diferem daquelas congeladas")

            config = run["config"]
            tokenizer = load_tokenizer(model_name, config["revision"])
            if model_name not in checked_lengths:
                test_lengths = token_lengths(tokenizer, [item["text"] for item in splits["test"]])
                exceeded = [
                    item["id"] for item, length in zip(splits["test"], test_lengths)
                    if length > config["max_length"]
                ]
                if exceeded:
                    raise ValueError(f"Entradas de teste acima do limite em {model_name}: {exceeded}")
                checked_lengths.add(model_name)
            model = load_model(model_name, config["revision"])
            state = torch.load(run["checkpoint"], map_location="cpu", weights_only=True)
            model.load_state_dict(state, strict=True)
            model.to(device)

            # Reproduzir a validação verifica a releitura antes de consultar o teste.
            validation = predict(
                model, splits["validation"], tokenizer, config["max_length"], config["batch_size"], device
            )
            original = load_predictions(Path(run["validation_predictions"]))
            if not np.array_equal(validation["ids"], original["ids"]):
                raise ValueError("Os IDs da validação mudaram após recarregar o checkpoint")
            if not np.allclose(validation["logits"], original["logits"], rtol=1e-5, atol=1e-6):
                raise ValueError("Os logits da validação mudaram após recarregar o checkpoint")

            del model

    output.mkdir(parents=True, exist_ok=False)
    summary = {}

    # A classe majoritária foi escolhida no treino e é mantida fixa no teste.
    baseline_label = manifest["majority_baseline_validation"]["label"]
    baseline_id = manifest["label_to_id"][baseline_label]
    test_labels = np.asarray([item["label_id"] for item in splits["test"]])
    baseline_predictions = np.full(len(test_labels), baseline_id)
    baseline = classification_metrics(test_labels, baseline_predictions)
    baseline["label"] = baseline_label
    (output / "baseline.json").write_text(
        json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    for model_name, selection in frozen["selected"].items():
        summary[model_name] = []
        for run in selection["runs"]:
            config = run["config"]
            tokenizer = load_tokenizer(model_name, config["revision"])
            model = load_model(model_name, config["revision"])
            state = torch.load(run["checkpoint"], map_location="cpu", weights_only=True)
            model.load_state_dict(state, strict=True)
            model.to(device)
            test = predict(model, splits["test"], tokenizer, config["max_length"], config["batch_size"], device)
            name = f"{model_name.replace('/', '_')}_seed_{run['seed']}"
            save_predictions(output / f"{name}.npz", test)
            metrics = evaluate_predictions(test, run["thresholds"])
            metrics_path = output / f"{name}.json"
            metrics_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            summary[model_name].append({"seed": run["seed"], "metrics": str(metrics_path)})
            del model

    (output / "summary.json").write_text(
        json.dumps({"frozen_sha256": sha256(frozen_path), "runs": summary, "baseline": "baseline.json"},
                   ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
