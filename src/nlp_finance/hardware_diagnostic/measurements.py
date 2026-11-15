# Medições usadas para escolher comprimento e avaliar recursos antes do treino.

import math
import platform
import subprocess
import time
from importlib import metadata
from itertools import islice

import torch
from sklearn.model_selection import train_test_split

from ..tokenization import token_lengths
from ..training import AmpMonitor, create_optimizer, create_scheduler, train_batch


# Compara o comprimento das mensagens de desenvolvimento nos dois tokenizers.
def inspect_lengths(examples, tokenizers: dict) -> dict:
    if len(tokenizers) != 2:
        raise ValueError("O diagnóstico exige os dois tokenizers")
    if not examples:
        raise ValueError("Não há mensagens de desenvolvimento para medir")

    texts = [example["text"] for example in examples]
    report = {}
    for name, tokenizer in tokenizers.items():
        lengths = token_lengths(tokenizer, texts)
        report[name] = {
            "maximum": max(lengths),
            "above_64": sum(length > 64 for length in lengths),
            "above_128": sum(length > 128 for length in lengths),
            "count": len(lengths),
        }

    if all(item["above_64"] == 0 for item in report.values()):
        chosen_limit = 64
    elif all(item["above_128"] == 0 for item in report.values()):
        chosen_limit = 128
    else:
        chosen_limit = None
    return {"models": report, "chosen_limit": chosen_limit}


# Registra o ambiente realmente disponível; não presume que exista GPU.
def hardware_info() -> dict:
    info = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "torch": torch.__version__,
        "cuda_version": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "gpus": [],
    }
    info["packages"] = {}
    for name in ("numpy", "transformers", "accelerate", "datasets", "scikit-learn", "matplotlib"):
        try:
            info["packages"][name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            info["packages"][name] = None
    if info["cuda_available"]:
        for index in range(torch.cuda.device_count()):
            properties = torch.cuda.get_device_properties(index)
            info["gpus"].append({
                "index": index, "name": properties.name, "total_memory": properties.total_memory
            })
        try:
            driver = subprocess.run(
                ["nvidia-smi", "--query-gpu=driver_version,memory.used", "--format=csv,noheader"],
                capture_output=True, text=True, check=True, timeout=10,
            )
            info["driver_and_memory_used"] = driver.stdout.strip()
        except (OSError, subprocess.SubprocessError) as error:
            info["driver_query_error"] = str(error)
    return info


# Escolhe 512 mensagens estratificadas do treino e mantém seus IDs e ordem.
def diagnostic_sample(examples, seed: int = 42) -> list[dict]:
    if len(examples) < 512:
        raise ValueError("A amostra do diagnóstico precisa de 512 mensagens de treino")
    if len(examples) == 512:
        return list(examples)

    labels = [example["label"] for example in examples]
    _, sample = train_test_split(examples, test_size=512, stratify=labels, random_state=seed)
    selected_ids = {example["id"] for example in sample}
    return [example for example in examples if example["id"] in selected_ids]


# Mede um candidato com aquecimento separado e a mesma amostra completa de treino.
def benchmark_candidate(model, warmup_batches, measured_batches, full_train_batches: int, device, use_amp: bool):
    if device.type != "cuda":
        raise ValueError("O benchmark de GPU requer CUDA")
    if len(warmup_batches) < 5:
        raise ValueError("O aquecimento requer ao menos cinco lotes")

    model.to(device)
    model.train()
    optimizer, _ = create_optimizer(model, 2e-5)
    scheduler, _ = create_scheduler(optimizer, full_train_batches * 5)
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)
    initial_scale = scaler.get_scale()

    for batch in islice(warmup_batches, 5):
        train_batch(model, batch, optimizer, scheduler, scaler, device, use_amp)

    torch.cuda.synchronize(device)
    torch.cuda.reset_peak_memory_stats(device)
    started = time.perf_counter()
    examples = 0
    skipped = 0
    for batch in measured_batches:
        result = train_batch(model, batch, optimizer, scheduler, scaler, device, use_amp)
        examples += len(batch["labels"])
        skipped += int(result["skipped"])
    torch.cuda.synchronize(device)
    elapsed = time.perf_counter() - started
    free, total = torch.cuda.mem_get_info(device)

    if not examples or elapsed <= 0:
        raise ValueError("A amostra medida não contém exemplos")
    return {
        "examples": examples, "seconds": elapsed, "examples_per_second": examples / elapsed,
        "peak_allocated": torch.cuda.max_memory_allocated(device),
        "peak_reserved": torch.cuda.max_memory_reserved(device),
        "free_memory": free, "total_memory": total, "skipped": skipped,
        "initial_scale": initial_scale, "final_scale": scaler.get_scale(),
    }


# Mede a janela de estabilidade separada do benchmark de throughput.
def measure_amp_stability(model, batches, full_train_batches: int, device):
    if device.type != "cuda":
        raise ValueError("O diagnóstico de AMP requer CUDA")
    model.to(device)
    model.train()
    optimizer, _ = create_optimizer(model, 2e-5)
    scheduler, _ = create_scheduler(optimizer, full_train_batches * 5)
    scaler = torch.amp.GradScaler("cuda", enabled=True)
    monitor = AmpMonitor()
    events = []

    # O chamador fornece ao menos 120 lotes, podendo repetir exemplos de treino.
    for batch in batches:
        event = train_batch(model, batch, optimizer, scheduler, scaler, device, True)
        events.append(event)
        monitor.record(event["skipped"])
        if len(events) == 120:
            break
    if len(events) != 120:
        raise ValueError("O diagnóstico requer 20 tentativas iniciais e 100 medidas")
    return {"summary": monitor.summary(), "events": events}


# Faz uma atualização com mensagens mais longas e mede a memória livre após o pico.
def stress_memory(model, batch, full_train_batches: int, device, use_amp: bool) -> dict:
    model.to(device)
    model.train()
    optimizer, _ = create_optimizer(model, 2e-5)
    scheduler, _ = create_scheduler(optimizer, full_train_batches * 5)
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)
    torch.cuda.reset_peak_memory_stats(device)
    train_batch(model, batch, optimizer, scheduler, scaler, device, use_amp)
    torch.cuda.synchronize(device)
    free, total = torch.cuda.mem_get_info(device)
    return {
        "free_memory_after_stress": free,
        "stress_total_memory": total,
        "stress_peak_allocated": torch.cuda.max_memory_allocated(device),
        "stress_peak_reserved": torch.cuda.max_memory_reserved(device),
        "oom": False,
    }


# Escolhe o batch comum pelo menor throughput entre os dois modelos.
def choose_batch(results: dict) -> int:
    candidates = []
    for batch_size, models in results.items():
        if batch_size not in (8, 16, 32) or len(models) != 2:
            raise ValueError("Informe batches 8, 16 ou 32 e resultados dos dois modelos")
        viable = all(item["free_memory_after_stress"] >= 1024 ** 3 and not item["oom"] for item in models.values())
        if viable:
            speed = min(item["examples_per_second"] for item in models.values())
            if not math.isfinite(speed) or speed <= 0:
                raise ValueError("Throughput deve ser finito e positivo")
            candidates.append((batch_size, speed))
    if not candidates:
        raise ValueError("Nenhum batch foi viável nos dois modelos")
    best_speed = max(speed for _, speed in candidates)
    return min(batch for batch, speed in candidates if speed >= best_speed * 0.95)
