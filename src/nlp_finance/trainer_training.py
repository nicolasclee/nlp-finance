# Treinamento com o Trainer do Transformers, como no laboratório.

import json
import math
import os
import random
from contextlib import contextmanager
from importlib.metadata import version
from pathlib import Path

import numpy as np
import torch
from transformers import Trainer, TrainerCallback, TrainingArguments

from .evaluation import classification_metrics
from .constants import AMP_INITIAL_SCALE
from .model_selection import select_epoch
from .training import AmpMonitor, validation_logits


# Durante avaliação, evita o autocast que o Accelerate aplica ao forward do modelo.
@contextmanager
def fp32_forward(model, device, amp_enabled: bool):
    original = getattr(model, "_original_forward", None)
    if amp_enabled and original is None:
        raise RuntimeError("Não foi possível garantir a validação em FP32 com AMP")

    wrapped_forward = model.forward
    if original is not None:
        model.forward = original
    try:
        with torch.autocast(device_type=device.type, enabled=False):
            yield
    finally:
        model.forward = wrapped_forward


# O Trainer cuida do treino; esta adaptação mantém a validação em FP32.
class FP32ValidationTrainer(Trainer):
    def prediction_step(self, model, inputs, prediction_loss_only, ignore_keys=None):
        device = next(model.parameters()).device
        with fp32_forward(model, device, self.args.fp16):
            return super().prediction_step(model, inputs, prediction_loss_only, ignore_keys)


# Registra os saltos e aplica a regra de estabilidade aprovada para AMP.
class StabilityCallback(TrainerCallback):
    def __init__(self, monitor, output: Path, amp_enabled: bool):
        self.monitor = monitor
        self.output = output
        self.amp_enabled = amp_enabled
        self.last_loss = None

    def on_train_begin(self, args, state, control, model=None, optimizer=None, **kwargs):
        if any(group["weight_decay"] not in (0, 0.01) for group in optimizer.param_groups):
            raise RuntimeError("O weight decay do Trainer difere do valor previsto")
        names = {id(parameter): name for name, parameter in model.named_parameters()}
        layer_norm_ids = set()
        for module in model.modules():
            if isinstance(module, torch.nn.LayerNorm):
                layer_norm_ids.update(id(parameter) for parameter in module.parameters(recurse=False))

        expected_no_decay = {
            name for name, parameter in model.named_parameters()
            if parameter.requires_grad and (name.rsplit(".", 1)[-1] == "bias" or id(parameter) in layer_norm_ids)
        }
        actual_no_decay = {
            names[id(parameter)]
            for group in optimizer.param_groups if group["weight_decay"] == 0
            for parameter in group["params"]
        }
        if actual_no_decay != expected_no_decay:
            raise RuntimeError("Os grupos de weight decay do Trainer diferem do protocolo")

        groups = []
        for group in optimizer.param_groups:
            groups.append({
                "weight_decay": group["weight_decay"],
                "parameters": [names[id(parameter)] for parameter in group["params"]],
            })
        (self.output / "optimizer_groups.json").write_text(
            json.dumps(groups, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    def on_optimizer_step(self, args, state, control, model=None, optimizer=None, **kwargs):
        if self.amp_enabled and not hasattr(optimizer, "step_was_skipped"):
            raise RuntimeError("Não foi possível verificar se o AMP pulou a atualização")
        skipped = bool(optimizer.step_was_skipped) if self.amp_enabled else False
        scaler = getattr(optimizer, "scaler", None)
        if self.amp_enabled and scaler is None:
            raise RuntimeError("Não foi possível acessar a escala do AMP")

        checks = [torch.isfinite(parameter).all() for parameter in model.parameters()]
        if not torch.stack(checks).all().item():
            raise RuntimeError("Parâmetro não finito após atualização")

        event = {
            "attempt": self.monitor.attempts + 1,
            "loss": self.last_loss,
            "skipped": skipped,
            "scale": scaler.get_scale() if scaler is not None else None,
            "learning_rate": optimizer.param_groups[0]["lr"],
        }
        with (self.output / "updates.jsonl").open("a", encoding="utf-8") as file:
            file.write(json.dumps(event) + "\n")
        self.monitor.record(skipped)


# Mede a classificação na validação; a acurácia escolhe o checkpoint.
def compute_metrics(prediction) -> dict:
    labels = prediction.label_ids
    predicted = np.argmax(prediction.predictions, axis=-1)
    metrics = classification_metrics(labels, predicted)
    return {
        "accuracy": metrics["accuracy"],
        "macro_f1": metrics["macro_f1"],
        "correct": int(np.sum(labels == predicted)),
        "total": len(labels),
    }


# Interrompe a tentativa se a perda ou a saída do modelo não for finita.
def check_model_output(module, inputs, output):
    if not torch.isfinite(output.logits).all().item():
        raise RuntimeError("Logits não finitos durante o treinamento ou validação")
    if output.loss is not None and not torch.isfinite(output.loss).item():
        raise RuntimeError("Perda não finita durante o treinamento ou validação")


# Executa uma tentativa completa sem retomar checkpoints parciais.
def run_with_trainer(model_factory, train_batches_factory, validation_batches_factory, config: dict, output: Path):
    expected_versions = {"transformers": "4.57.1", "accelerate": "1.10.1"}
    for package, expected in expected_versions.items():
        installed = version(package)
        if installed != expected:
            raise RuntimeError(f"{package} {installed} difere da versão verificada {expected}")

    seed = config["seed"]
    rate = config["learning_rate"]
    precision = config["precision"]
    device = torch.device(config["device"])
    if seed not in (13, 37, 73) or rate not in (2e-5, 5e-5):
        raise ValueError("Use uma das seeds e taxas previstas no protocolo")
    if precision not in ("fp32", "amp_fp16"):
        raise ValueError("A precisão precisa ser fp32 ou amp_fp16")
    if device.type not in ("cpu", "cuda"):
        raise ValueError("O dispositivo precisa ser CPU ou CUDA")
    if device.type == "cuda" and not torch.cuda.is_available():
        raise ValueError("CUDA não está disponível neste ambiente")
    if device.type == "cuda" and torch.cuda.device_count() != 1:
        raise ValueError("O experimento requer exatamente uma GPU visível")
    if precision == "amp_fp16" and device.type != "cuda":
        raise ValueError("AMP FP16 requer CUDA neste experimento")
    if device.type == "cuda" and device.index not in (None, 0):
        raise ValueError("Use cuda ou cuda:0; o experimento prevê uma GPU")
    if device.type == "cuda" and os.environ.get("CUBLAS_WORKSPACE_CONFIG") not in (":4096:8", ":16:8"):
        raise ValueError("Configure CUBLAS_WORKSPACE_CONFIG=:4096:8 antes de iniciar o Python")

    output.mkdir(parents=True, exist_ok=False)
    (output / "config.json").write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    monitor = AmpMonitor()

    try:
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.benchmark = False
        torch.use_deterministic_algorithms(True)

        model = model_factory()
        stability_callback = StabilityCallback(monitor, output, precision == "amp_fp16")

        def observe_output(module, inputs, model_output):
            check_model_output(module, inputs, model_output)
            if module.training and model_output.loss is not None:
                stability_callback.last_loss = model_output.loss.item()

        model.register_forward_hook(observe_output)
        (output / "loading_info.json").write_text(
            json.dumps(model.loading_info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        train_batches = train_batches_factory()
        validation_batches = validation_batches_factory()
        planned_updates = len(train_batches) * 5
        warmup_updates = math.ceil(planned_updates * 0.10)

        args = TrainingArguments(
            output_dir=str(output / "trainer_checkpoints"),
            num_train_epochs=5,
            per_device_train_batch_size=config["batch_size"],
            per_device_eval_batch_size=config["batch_size"],
            learning_rate=rate,
            optim="adamw_torch",
            adam_beta1=0.9,
            adam_beta2=0.999,
            adam_epsilon=1e-8,
            weight_decay=0.01,
            lr_scheduler_type="linear",
            warmup_steps=warmup_updates,
            max_grad_norm=1.0,
            gradient_accumulation_steps=1,
            fp16=precision == "amp_fp16",
            fp16_full_eval=False,
            eval_strategy="epoch",
            save_strategy="epoch",
            save_total_limit=1,
            save_only_model=True,
            load_best_model_at_end=True,
            metric_for_best_model="accuracy",
            greater_is_better=True,
            dataloader_drop_last=False,
            dataloader_num_workers=0,
            remove_unused_columns=False,
            logging_nan_inf_filter=False,
            seed=seed,
            data_seed=seed,
            use_cpu=device.type == "cpu",
            report_to="none",
        )

        trainer = FP32ValidationTrainer(
            model=model,
            args=args,
            train_dataset=train_batches.dataset,
            eval_dataset=validation_batches.dataset,
            data_collator=train_batches.collate_fn,
            compute_metrics=compute_metrics,
            callbacks=[stability_callback],
        )
        if precision == "amp_fp16":
            # Usa a mesma escala medida no diagnóstico antes de preparar o otimizador.
            trainer.accelerator.scaler = torch.amp.GradScaler("cuda", init_scale=AMP_INITIAL_SCALE)
        trainer.train()

        history = []
        for event in trainer.state.log_history:
            if "eval_accuracy" in event:
                history.append({
                    "epoch": int(round(event["epoch"])),
                    "accuracy": event["eval_accuracy"],
                    "macro_f1": event["eval_macro_f1"],
                    "correct": event["eval_correct"],
                    "total": event["eval_total"],
                    "step": event["step"],
                })
        if [item["epoch"] for item in history] != [1, 2, 3, 4, 5]:
            raise RuntimeError("O Trainer não registrou as cinco avaliações previstas")
        if monitor.attempts != planned_updates:
            raise RuntimeError("O Trainer executou quantidade diferente de atualizações planejadas")

        selected = select_epoch(history)
        if (
            trainer.state.best_model_checkpoint is None
            or trainer.state.best_metric != selected["accuracy"]
            or trainer.state.best_global_step != selected["step"]
        ):
            raise RuntimeError("O checkpoint selecionado pelo Trainer não corresponde à validação")
        (output / "epochs.json").write_text(
            json.dumps(history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        torch.save(model.state_dict(), output / "best_model.pt")
        with fp32_forward(model, device, precision == "amp_fp16"):
            logits = validation_logits(model, validation_batches, device)
        torch.save(logits, output / "validation_logits.pt")

        result = {
            "status": "completed",
            "best_epoch": selected["epoch"],
            "planned_updates": planned_updates,
            "warmup_updates": warmup_updates,
            "updates": monitor.summary(),
            "final_learning_rate": trainer.lr_scheduler.get_last_lr()[0],
        }
    except BaseException as error:
        result = {
            "status": "failed", "error_type": type(error).__name__,
            "error": str(error), "updates": monitor.summary(),
        }
        (output / "result.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        raise

    (output / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return result
