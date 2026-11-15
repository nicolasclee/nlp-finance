# Preparação reproduzível e auditoria dos arquivos CSV do BANKING77.

from __future__ import annotations

import csv
import hashlib
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path


# Calcula a impressão digital de um arquivo sem carregá-lo inteiro.
def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        chunk = source.read(1024 * 1024)
        while chunk:
            digest.update(chunk)
            chunk = source.read(1024 * 1024)
    return digest.hexdigest()


# Lê o CSV oficial e associa cada linha à sua posição original.
def read_examples(path: Path, split: str) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames or not {"text", "category"}.issubset(reader.fieldnames):
            raise ValueError(f"{path}: CSV precisa das colunas text e category")
        examples = []
        for index, row in enumerate(reader):
            if row.get("text") is None or row.get("category") is None:
                raise ValueError(f"{path}: linha {index + 2} incompleta")
            examples.append({
                "id": f"{split}:{index}",
                "text": row["text"],
                "label": row["category"],
            })

    if not examples:
        raise ValueError(f"{path}: nenhum exemplo encontrado")
    return examples


# Separa aproximadamente 10% para validação, mantendo exemplos de cada classe.
def stratified_split(
    examples: list[dict[str, str]], seed: int = 42
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for example in examples:
        groups[example["label"]].append(example)

    if any(len(group) < 2 for group in groups.values()):
        raise ValueError("Cada classe precisa de pelo menos dois exemplos para a divisão")

    rng = random.Random(seed)
    labels = sorted(groups)
    target = math.ceil(len(examples) * 0.10)
    if target < len(labels) or len(examples) - target < len(labels):
        raise ValueError("A proporção de validação não permite representar todas as classes")

    # Cada classe precisa aparecer tanto no treino quanto na validação.
    quotas = {}
    for label in labels:
        class_size = len(groups[label])
        desired_count = math.floor(class_size * 0.10)
        quotas[label] = max(1, min(class_size - 1, desired_count))

    # Ajusta as cotas para que o total corresponda a 10% dos exemplos.
    while sum(quotas.values()) < target:
        eligible = [label for label in labels if quotas[label] < len(groups[label]) - 1]
        label = max(eligible, key=lambda item: (len(groups[item]) * 0.10 - quotas[item], item))
        quotas[label] += 1

    while sum(quotas.values()) > target:
        eligible = [label for label in labels if quotas[label] > 1]
        label = min(eligible, key=lambda item: (len(groups[item]) * 0.10 - quotas[item], item))
        quotas[label] -= 1

    validation_ids: set[str] = set()
    for label in labels:
        class_examples = list(groups[label])
        rng.shuffle(class_examples)
        for example in class_examples[:quotas[label]]:
            validation_ids.add(example["id"])

    train = [item for item in examples if item["id"] not in validation_ids]
    validation = [item for item in examples if item["id"] in validation_ids]
    return train, validation


# Registra vazios, duplicatas e rótulos conflitantes sem alterar os dados.
def audit(splits: dict[str, list[dict[str, str]]]) -> dict:
    result: dict = {"counts": {}, "empty_text_ids": [], "empty_label_ids": [], "comparisons": {}}
    all_ids = [item["id"] for items in splits.values() for item in items]
    if len(all_ids) != len(set(all_ids)):
        raise ValueError("IDs repetidos entre ou dentro das divisões")

    for name, items in splits.items():
        counts_by_label = Counter(item["label"] for item in items)
        result["counts"][name] = {
            "total": len(items),
            "by_label": dict(sorted(counts_by_label.items())),
        }
        result["empty_text_ids"].extend(item["id"] for item in items if not item["text"].strip())
        result["empty_label_ids"].extend(item["id"] for item in items if not item["label"].strip())

    # Compara os textos originais e, separadamente, ignorando diferenças de espaços.
    for mode in ("exact", "whitespace"):
        grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
        for name, items in splits.items():
            for item in items:
                text = item["text"]
                if mode == "whitespace":
                    text = " ".join(text.split())
                grouped[text].append({"id": item["id"], "label": item["label"], "split": name})

        duplicates = []
        for text, occurrences in sorted(grouped.items()):
            if len(occurrences) > 1:
                split_names = {item["split"] for item in occurrences}
                labels = {item["label"] for item in occurrences}
                duplicates.append({
                    "text": text,
                    "occurrences": occurrences,
                    "cross_split": len(split_names) > 1,
                    "conflicting_labels": len(labels) > 1,
                })
        result["comparisons"][mode] = duplicates
    return result


# Prepara os dados oficiais e salva divisão, auditoria e manifesto.
def prepare(train_path: Path, test_path: Path, output: Path, revision: str) -> dict:
    if not revision.strip():
        raise ValueError("Informe a revisão imutável da origem dos dados")

    official_train = read_examples(train_path, "official_train")
    official_test = read_examples(test_path, "official_test")
    labels = sorted({item["label"] for item in official_train})
    if len(labels) != 77 or len(official_train) != 10003 or len(official_test) != 3080:
        raise ValueError(
            f"Contagens inesperadas: treino={len(official_train)}, "
            f"teste={len(official_test)}, rótulos={len(labels)}; investigar a origem"
        )
    if {item["label"] for item in official_test} != set(labels):
        raise ValueError("Rótulos do teste oficial diferem dos rótulos do treino")

    train, validation = stratified_split(official_train)
    splits = {"train": train, "validation": validation, "test": official_test}
    report = audit(splits)
    if report["empty_label_ids"]:
        raise ValueError("Há rótulos vazios; investigar antes da preparação")

    label_to_id = {label: index for index, label in enumerate(labels)}
    train_counts = Counter(item["label"] for item in train)
    # Em empate, os rótulos em ordem alfabética já têm os menores IDs.
    majority = min(labels, key=lambda label: (-train_counts[label], label_to_id[label]))
    correct = sum(item["label"] == majority for item in validation)

    split_indices = {name: [item["id"] for item in items] for name, items in splits.items()}
    split_json = json.dumps(
        split_indices, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    )
    split_hash = hashlib.sha256(split_json.encode("utf-8")).hexdigest()

    manifest = {
        "source_revision": revision,
        "sources": {
            "train": {"path": str(train_path), "sha256": sha256(train_path)},
            "test": {"path": str(test_path), "sha256": sha256(test_path)},
        },
        "split_seed": 42,
        "validation_fraction": 0.10,
        "split_sha256": split_hash,
        "training_seeds": [13, 37, 73],
        "label_to_id": label_to_id,
        "majority_baseline_validation": {
            "label": majority,
            "correct": correct,
            "total": len(validation),
            "accuracy": correct / len(validation),
        },
    }
    output.mkdir(parents=True, exist_ok=False)
    files = {
        "manifest.json": manifest,
        "splits.json": split_indices,
        "audit.json": report,
    }
    for name, value in files.items():
        content = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
        (output / name).write_text(content, encoding="utf-8")

    return {
        "output": str(output),
        "counts": {name: len(items) for name, items in splits.items()},
        "empty_texts": len(report["empty_text_ids"]),
        "cross_split_duplicates": {
            mode: sum(item["cross_split"] for item in items)
            for mode, items in report["comparisons"].items()
        },
        "conflicting_groups": {
            mode: sum(item["conflicting_labels"] for item in items)
            for mode, items in report["comparisons"].items()
        },
    }
