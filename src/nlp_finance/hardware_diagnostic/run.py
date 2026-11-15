# Orquestra as medições de recursos sem consultar previsões do teste.

import itertools
import json
import math
import os
import random
import re
import tempfile
import time
from pathlib import Path

import numpy as np
import torch
from ..checkpoints import checkpoint_files
from ..data import sha256
from ..dataset import check_audit_review, load_prepared_data, make_dataloader
from .measurements import (
    benchmark_candidate, choose_batch, diagnostic_sample, hardware_info,
    inspect_lengths, measure_amp_stability, stress_memory,
)
from ..model import load_model
from ..predictions import predict
from ..tokenization import load_tokenizer, token_lengths
from ..training import evaluate_validation


MODELS = ("google-bert/bert-base-uncased", "yiyanghkust/finbert-pretrain")


# Reinicia os geradores para que candidatos partam da mesma seed de diagnóstico.
def seed_diagnostic() -> None:
    random.seed(13)
    np.random.seed(13)
    torch.manual_seed(13)
    torch.cuda.manual_seed_all(13)
    torch.backends.cudnn.benchmark = False
    torch.use_deterministic_algorithms(True)


# Executa diagnóstico com os dois modelos e os mesmos exemplos de treino.
def run_diagnostic(preparation: Path, revisions: dict, output: Path, device_name: str = "cuda") -> dict:
    if set(revisions) != set(MODELS) or any(
        not re.fullmatch(r"[0-9a-fA-F]{40}", value) for value in revisions.values()
    ):
        raise ValueError("Informe o hash completo de commit dos dois modelos previstos")
    device = torch.device(device_name)
    if device.type != "cuda" or not torch.cuda.is_available():
        raise ValueError("O diagnóstico requer uma GPU CUDA disponível")
    if os.environ.get("CUBLAS_WORKSPACE_CONFIG") not in (":4096:8", ":16:8"):
        raise ValueError("Configure CUBLAS_WORKSPACE_CONFIG=:4096:8 antes de iniciar o Python")

    check_audit_review(preparation)
    splits, _ = load_prepared_data(preparation)
    development = splits["train"] + splits["validation"]
    tokenizers = {name: load_tokenizer(name, revisions[name]) for name in MODELS}
    lengths = inspect_lengths(development, tokenizers)
    output.mkdir(parents=True, exist_ok=False)
    report = {
        "status": "needs_review", "preparation_hash": sha256(preparation / "manifest.json"),
        "revisions": revisions, "hardware": hardware_info(), "lengths": lengths,
        "checkpoint_files": {name: checkpoint_files(name, revisions[name]) for name in MODELS},
        "code_files": {path.name: sha256(path) for path in sorted(Path(__file__).parent.parent.glob("*.py"))},
    }

    if lengths["chosen_limit"] is None:
        report["reason"] = "Há mensagens de desenvolvimento acima de 128 tokens"
        (output / "diagnostic.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        return report

    max_length = lengths["chosen_limit"]
    sample = diagnostic_sample(splits["train"])
    report["sample_ids"] = [item["id"] for item in sample]
    report["length_distributions"] = {}
    for name in MODELS:
        report["length_distributions"][name] = {}
        for group_name, examples in (("train", splits["train"]), ("sample", sample)):
            values = sorted(token_lengths(tokenizers[name], [item["text"] for item in examples]))
            report["length_distributions"][name][group_name] = {
                "count": len(values), "mean": sum(values) / len(values),
                "p90": values[math.ceil(0.90 * len(values)) - 1], "maximum": values[-1],
            }
    results = {precision: {} for precision in ("fp32", "amp_fp16")}

    for precision in results:
        for batch_size in (8, 16, 32):
            results[precision][batch_size] = {}
            for name in MODELS:
                seed_diagnostic()
                model = load_model(name, revisions[name])
                tokenizer = tokenizers[name]
                sample_batches = make_dataloader(sample, tokenizer, max_length, batch_size, shuffle=False)
                full_train_batches = math.ceil(len(splits["train"]) / batch_size)
                try:
                    measured = benchmark_candidate(
                        model, sample_batches, sample_batches, full_train_batches, device, precision == "amp_fp16"
                    )
                    del model
                    model = None
                    torch.cuda.empty_cache()
                    seed_diagnostic()
                    model = load_model(name, revisions[name])
                    train_lengths = token_lengths(tokenizer, [item["text"] for item in splits["train"]])
                    longest = splits["train"][max(range(len(train_lengths)), key=train_lengths.__getitem__)]
                    stress_batches = make_dataloader(
                        [longest] * batch_size, tokenizer, max_length, batch_size, shuffle=False
                    )
                    stress = stress_memory(model, next(iter(stress_batches)), full_train_batches, device, precision == "amp_fp16")
                    results[precision][batch_size][name] = {**measured, **stress}
                except torch.cuda.OutOfMemoryError as error:
                    results[precision][batch_size][name] = {
                        "oom": True, "free_memory_after_stress": 0, "error": str(error)
                    }
                finally:
                    del model
                    torch.cuda.empty_cache()

    report["benchmarks"] = results
    try:
        batch_size = choose_batch(results["amp_fp16"])
    except ValueError as error:
        report["reason"] = str(error)
        (output / "diagnostic.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        return report

    # AMP precisa de comparação possível com FP32 no mesmo batch e ganho nos dois modelos.
    for name in MODELS:
        amp = results["amp_fp16"][batch_size][name]
        fp32 = results["fp32"][batch_size][name]
        if fp32["oom"] or not (
            amp["peak_allocated"] < fp32["peak_allocated"]
            or amp["examples_per_second"] > fp32["examples_per_second"]
        ):
            report["reason"] = f"AMP sem ganho comparável em ambos os modelos; revisar {name}"
            (output / "diagnostic.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
            return report

    report["stability"] = {}
    report["validation_and_save_seconds"] = {}
    report["load_and_prediction_seconds"] = {}
    for name in MODELS:
        seed_diagnostic()
        started = time.perf_counter()
        model = load_model(name, revisions[name])
        model.to(device)
        torch.cuda.synchronize(device)
        load_seconds = time.perf_counter() - started
        batches = make_dataloader(sample, tokenizers[name], max_length, batch_size, shuffle=False)
        full_train_batches = math.ceil(len(splits["train"]) / batch_size)
        try:
            report["stability"][name] = measure_amp_stability(model, itertools.cycle(batches), full_train_batches, device)
            validation_batches = make_dataloader(
                splits["validation"], tokenizers[name], max_length, batch_size, shuffle=False
            )
            model.to(device)
            torch.cuda.synchronize(device)
            started = time.perf_counter()
            evaluate_validation(model, validation_batches, device)
            torch.cuda.synchronize(device)
            validation_seconds = time.perf_counter() - started
            with tempfile.TemporaryDirectory() as temporary:
                started = time.perf_counter()
                torch.save(model.state_dict(), Path(temporary) / "checkpoint.pt")
                save_seconds = time.perf_counter() - started
            report["validation_and_save_seconds"][name] = {
                "validation": validation_seconds, "save": save_seconds,
            }
            started = time.perf_counter()
            predict(model, splits["validation"], tokenizers[name], max_length, batch_size, device)
            torch.cuda.synchronize(device)
            report["load_and_prediction_seconds"][name] = {
                "load": load_seconds, "validation_predictions": time.perf_counter() - started,
            }
        except (RuntimeError, ValueError) as error:
            report["reason"] = f"Estabilidade ou medição de {name} requer revisão: {error}"
            (output / "diagnostic.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
            return report
        finally:
            del model
            torch.cuda.empty_cache()

    # Inclui validação e salvamento a cada época nas projeções de 12 execuções.
    projections = {}
    for epochs in (3, 5):
        seconds = 0.0
        for name in MODELS:
            throughput = results["amp_fp16"][batch_size][name]["examples_per_second"]
            costs = report["validation_and_save_seconds"][name]
            # A validação adicional cobre a conferência dos logits ao salvar checkpoint.
            per_epoch = len(splits["train"]) / throughput + 2 * costs["validation"] + costs["save"]
            seconds += 6 * epochs * per_epoch
        projections[str(epochs)] = seconds

    report.update({
        "status": "ready", "batch_size": batch_size, "max_length": max_length,
        "precision": "amp_fp16", "estimated_seconds": projections,
        "projection_limits": "Amostra de 512 mensagens; custos de carregamento e previsões não incluídos.",
    })
    (output / "diagnostic.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report
