# Conecta preparação, diagnóstico aprovado e uma tentativa de treinamento.

import json
from pathlib import Path

import numpy as np
import torch

from ..data import sha256
from ..constants import AMP_INITIAL_SCALE
from ..dataset import check_audit_review, load_prepared_data, make_dataloader
from ..checkpoints import checkpoint_files
from ..evaluation import classification_metrics, prediction_scores
from ..model import load_model
from ..predictions import predict, save_predictions
from ..tokenization import load_tokenizer
from ..training import run_training


# Treina uma configuração e salva suas previsões de validação, sem executar o teste.
def train_one(preparation: Path, diagnostic: Path, config: dict, output: Path) -> dict:
    report = json.loads(diagnostic.read_text(encoding="utf-8"))
    preparation_hash = sha256(preparation / "manifest.json")
    if report.get("status") != "ready" or report.get("preparation_hash") != preparation_hash:
        raise ValueError("É necessário um diagnóstico concluído para esta preparação")

    for key in ("batch_size", "max_length", "precision"):
        if config.get(key) != report.get(key):
            raise ValueError(f"A configuração de {key} difere do diagnóstico")
    if report.get("amp_initial_scale") != AMP_INITIAL_SCALE:
        raise ValueError("A escala inicial do AMP difere do diagnóstico; refaça a medição")
    model_name = config["model_name"]
    if report.get("revisions", {}).get(model_name) != config["revision"]:
        raise ValueError("A revisão do modelo difere da usada no diagnóstico")
    for filename in (
        "model.py", "training.py", "trainer_training.py", "tokenization.py", "dataset.py", "data.py",
        "evaluation.py", "predictions.py", "constants.py", "checkpoints.py",
    ):
        current_file = Path(__file__).parent.parent / filename
        if report.get("code_files", {}).get(filename) != sha256(current_file):
            raise ValueError(f"O código {filename} mudou após o diagnóstico; revisar antes de prosseguir")
    if checkpoint_files(model_name, config["revision"]) != report["checkpoint_files"][model_name]:
        raise ValueError("Os arquivos do checkpoint mudaram após o diagnóstico")

    check_audit_review(preparation)
    splits, manifest = load_prepared_data(preparation)
    tokenizer = load_tokenizer(model_name, config["revision"])
    config = {**config, "amp_initial_scale": AMP_INITIAL_SCALE,
              "preparation_hash": preparation_hash, "diagnostic_hash": sha256(diagnostic)}

    def model_factory():
        return load_model(model_name, config["revision"])

    def train_batches():
        return make_dataloader(
            splits["train"], tokenizer, config["max_length"], config["batch_size"], shuffle=True
        )

    def validation_batches():
        return make_dataloader(
            splits["validation"], tokenizer, config["max_length"], config["batch_size"], shuffle=False
        )

    result = run_training(model_factory, train_batches, validation_batches, config, output)

    # Recarrega os pesos e confere as métricas antes de salvar as previsões.
    try:
        device = torch.device(config["device"])
        model = model_factory()
        state = torch.load(output / "best_model.pt", map_location="cpu", weights_only=True)
        model.load_state_dict(state, strict=True)
        model.to(device)
        validation = predict(
            model, splits["validation"], tokenizer, config["max_length"], config["batch_size"], device
        )
        previous_logits = torch.load(output / "validation_logits.pt", map_location="cpu", weights_only=True)
        if not np.allclose(validation["logits"], previous_logits.numpy(), rtol=1e-5, atol=1e-6):
            raise ValueError("Os logits mudaram após recarregar o checkpoint")
        scores = prediction_scores(validation)
        metrics = classification_metrics(validation["labels"], scores["predicted"])
        history = json.loads((output / "epochs.json").read_text(encoding="utf-8"))
        expected = next(epoch for epoch in history if epoch["epoch"] == result["best_epoch"])
        if not np.isclose(metrics["accuracy"], expected["accuracy"], rtol=0, atol=1e-12):
            raise ValueError("A acurácia mudou após recarregar o checkpoint")
        if not np.isclose(metrics["macro_f1"], expected["macro_f1"], rtol=0, atol=1e-12):
            raise ValueError("O Macro-F1 mudou após recarregar o checkpoint")
        save_predictions(output / "validation_predictions.npz", validation)
    except BaseException as error:
        result["status"] = "failed"
        result["error_type"] = type(error).__name__
        result["error"] = str(error)
        (output / "result.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        raise

    baseline = manifest["majority_baseline_validation"]
    if expected["accuracy"] <= baseline["accuracy"]:
        result["status"] = "needs_review"
        result["reason"] = "A validação não superou o baseline majoritário; investigar o pipeline"
        (output / "result.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return result
