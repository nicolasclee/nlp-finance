# Gera e salva previsões em FP32, com probabilidades calculadas em FP64.

from pathlib import Path

import numpy as np
import torch

from .constants import NUM_LABELS
from .dataset import make_dataloader


# Gera previsões na ordem dos exemplos, sem misturar ou reajustar pesos.
def predict(model, examples, tokenizer, max_length: int, batch_size: int, device):
    batches = make_dataloader(examples, tokenizer, max_length, batch_size, shuffle=False)
    model.eval()
    logits_parts = []

    with torch.no_grad():
        for batch in batches:
            inputs = {key: value.to(device) for key, value in batch.items() if key != "labels"}
            logits = model(**inputs).logits.float()
            if logits.ndim != 2 or logits.shape[1] != NUM_LABELS or not torch.isfinite(logits).all().item():
                raise ValueError(f"O modelo precisa gerar {NUM_LABELS} logits finitos por exemplo")
            logits_parts.append(logits.cpu())

    logits = torch.cat(logits_parts)
    probabilities = torch.softmax(logits, dim=1, dtype=torch.float64)

    return {
        "ids": np.asarray([item["id"] for item in examples], dtype=str),
        "labels": np.asarray([item["label_id"] for item in examples], dtype=np.int64),
        "logits": logits.numpy(),
        "probabilities": probabilities.numpy(),
    }


# Salva arrays sem objetos e impede substituir resultados de outra execução.
def save_predictions(path: Path, predictions: dict) -> None:
    if path.suffix != ".npz":
        raise ValueError("O arquivo de previsões precisa ter extensão .npz")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as output:
        np.savez_compressed(output, **predictions)


# Reabre os arrays sem permitir objetos serializados.
def load_predictions(path: Path) -> dict:
    with np.load(path, allow_pickle=False) as archive:
        required = {"ids", "labels", "logits", "probabilities"}
        if set(archive.files) != required:
            raise ValueError("O arquivo de previsões não contém os campos esperados")
        result = {name: archive[name] for name in required}

    count = len(result["ids"])
    if result["labels"].shape != (count,) or result["logits"].shape != (count, NUM_LABELS):
        raise ValueError("IDs, rótulos e logits têm formatos incompatíveis")
    if result["probabilities"].shape != (count, NUM_LABELS):
        raise ValueError(f"As probabilidades precisam ter {NUM_LABELS} colunas")
    if len(set(result["ids"].tolist())) != count:
        raise ValueError("Há IDs repetidos nas previsões")
    if not np.isfinite(result["logits"]).all() or not np.isfinite(result["probabilities"]).all():
        raise ValueError("As previsões contêm valores não finitos")
    if np.any(result["probabilities"] < 0) or not np.allclose(result["probabilities"].sum(axis=1), 1):
        raise ValueError("As probabilidades precisam ser não negativas e somar 1")
    if np.any(result["labels"] < 0) or np.any(result["labels"] >= NUM_LABELS):
        raise ValueError(f"Os rótulos precisam estar entre 0 e {NUM_LABELS - 1}")
    return result
