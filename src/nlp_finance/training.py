# Componentes de treino e validação. A execução científica ainda depende do diagnóstico.

import math
from collections import deque

import numpy as np
import torch
from torch import nn
from torch.optim import AdamW
from transformers import get_linear_schedule_with_warmup

from .constants import NUM_LABELS
from .evaluation import classification_metrics


# Divide os parâmetros entre aqueles que recebem ou não weight decay.
def create_optimizer(model, learning_rate: float):
    no_decay_ids = set()
    for module in model.modules():
        if isinstance(module, nn.LayerNorm):
            no_decay_ids.update(id(parameter) for parameter in module.parameters(recurse=False))

    decay = []
    no_decay = []
    groups = {"decay": [], "no_decay": []}

    for name, parameter in model.named_parameters():
        if not parameter.requires_grad:
            continue
        if name.rsplit(".", 1)[-1] == "bias" or id(parameter) in no_decay_ids:
            no_decay.append(parameter)
            groups["no_decay"].append(name)
        else:
            decay.append(parameter)
            groups["decay"].append(name)

    optimizer = AdamW(
        [
            {"params": decay, "weight_decay": 0.01},
            {"params": no_decay, "weight_decay": 0.0},
        ],
        lr=learning_rate,
        betas=(0.9, 0.999),
        eps=1e-8,
    )
    return optimizer, groups


# Define 10% de aquecimento e redução linear no horizonte de atualizações planejadas.
def create_scheduler(optimizer, planned_updates: int):
    if planned_updates <= 0:
        raise ValueError("O número de atualizações planejadas precisa ser positivo")

    warmup_updates = math.ceil(planned_updates * 0.10)

    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=warmup_updates,
        num_training_steps=planned_updates,
    )
    return scheduler, warmup_updates


# Acompanha os passos pulados pelo AMP conforme o critério D44.
class AmpMonitor:
    def __init__(self):
        self.attempts = 0
        self.skipped = 0
        self.initial_skips = 0
        self.consecutive_skips = 0
        self.window = deque(maxlen=100)

    def record(self, skipped: bool) -> None:
        self.attempts += 1
        self.skipped += int(skipped)

        if self.attempts <= 20:
            self.initial_skips += int(skipped)
            return

        self.window.append(skipped)
        self.consecutive_skips = self.consecutive_skips + 1 if skipped else 0

        if self.consecutive_skips >= 3:
            raise RuntimeError("AMP pulou três atualizações consecutivas após a fase inicial")
        if len(self.window) == 100 and sum(self.window) > 1:
            raise RuntimeError("AMP pulou mais de uma atualização em uma janela de 100")

    def summary(self) -> dict:
        measured_attempts = max(0, self.attempts - 20)
        measured_skips = self.skipped - self.initial_skips
        return {
            "attempts": self.attempts,
            "effective_updates": self.attempts - self.skipped,
            "skipped": self.skipped,
            "initial_skips": self.initial_skips,
            "measured_skips": measured_skips,
            "measured_skip_fraction": measured_skips / measured_attempts if measured_attempts else None,
            "last_window_attempts": len(self.window),
            "last_window_skips": sum(self.window),
        }


# Atualiza os pesos uma vez e informa se o GradScaler pulou a atualização.
def train_batch(model, batch, optimizer, scheduler, scaler, device, use_amp: bool) -> dict:
    optimizer.zero_grad(set_to_none=True)
    inputs = {key: value.to(device) for key, value in batch.items() if key != "labels"}
    labels = batch["labels"].to(device)

    with torch.autocast(device_type=device.type, dtype=torch.float16, enabled=use_amp):
        logits = model(**inputs).logits
        loss = nn.functional.cross_entropy(logits, labels)

    if not torch.isfinite(loss).item():
        raise RuntimeError("Perda não finita durante o treinamento")

    scaler.scale(loss).backward()
    scaler.unscale_(optimizer)
    gradient_checks = [
        torch.isfinite(parameter.grad).all()
        for parameter in model.parameters()
        if parameter.grad is not None
    ]
    if not gradient_checks:
        raise RuntimeError("Nenhum gradiente foi produzido no treinamento")
    gradients_finite = torch.stack(gradient_checks).all().item()

    if gradients_finite:
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0, error_if_nonfinite=True)
    elif not use_amp:
        raise RuntimeError("Gradientes não finitos durante treinamento em FP32")

    old_scale = scaler.get_scale()
    scaler.step(optimizer)
    scaler.update()
    new_scale = scaler.get_scale()
    skipped = use_amp and new_scale < old_scale

    if not skipped:
        scheduler.step()

    parameter_checks = [torch.isfinite(parameter).all() for parameter in model.parameters()]
    if not torch.stack(parameter_checks).all().item():
        raise RuntimeError("Parâmetro não finito após atualização")

    return {
        "loss": loss.item(),
        "skipped": skipped,
        "scale": new_scale,
        "learning_rate": optimizer.param_groups[0]["lr"],
    }


# Mede acurácia e Macro-F1 nas 77 classes, sem abstenção e em FP32.
def evaluate_validation(model, batches, device) -> dict:
    model.eval()
    all_labels = []
    all_predictions = []

    with torch.no_grad():
        for batch in batches:
            inputs = {key: value.to(device) for key, value in batch.items() if key != "labels"}
            labels = batch["labels"].to(device)
            logits = model(**inputs).logits
            if logits.ndim != 2 or logits.shape[1] != NUM_LABELS or not torch.isfinite(logits).all().item():
                raise RuntimeError(f"A validação precisa produzir {NUM_LABELS} logits finitos por exemplo")

            predictions = logits.argmax(dim=1)
            all_labels.extend(labels.tolist())
            all_predictions.extend(predictions.tolist())

    if not all_labels:
        raise ValueError("A validação não contém exemplos")
    if any(not 0 <= label < NUM_LABELS for label in all_labels):
        raise ValueError("A validação contém ID de rótulo fora do intervalo")

    labels_array = np.asarray(all_labels)
    predictions_array = np.asarray(all_predictions)
    metrics = classification_metrics(labels_array, predictions_array)
    correct = int(np.sum(labels_array == predictions_array))

    return {
        "correct": correct,
        "total": len(all_labels),
        "accuracy": metrics["accuracy"],
        "macro_f1": metrics["macro_f1"],
    }


# Guarda os logits para conferir a equivalência após recarregar o checkpoint.
def validation_logits(model, batches, device):
    model.eval()
    logits = []
    with torch.no_grad():
        for batch in batches:
            inputs = {key: value.to(device) for key, value in batch.items() if key != "labels"}
            logits.append(model(**inputs).logits.float().cpu())
    return torch.cat(logits)


# O Trainer executa a tentativa; os componentes acima também servem ao diagnóstico.
def run_training(model_factory, train_batches_factory, validation_batches_factory, config: dict, output):
    from .trainer_training import run_with_trainer

    return run_with_trainer(model_factory, train_batches_factory, validation_batches_factory, config, output)
