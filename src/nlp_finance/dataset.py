# Reconstitui as divisões registradas e cria lotes para os modelos.

import hashlib
import torch
from torch.utils.data import DataLoader
import json
from pathlib import Path

from .constants import NUM_LABELS
from .data import read_examples, sha256
from .tokenization import tokenize_batch


# Confere arquivos e índices antes de reconstruir treino, validação e teste.
def load_prepared_data(preparation: Path) -> tuple[dict, dict]:
    manifest = json.loads((preparation / "manifest.json").read_text(encoding="utf-8"))
    split_ids = json.loads((preparation / "splits.json").read_text(encoding="utf-8"))
    split_json = json.dumps(split_ids, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    actual_hash = hashlib.sha256(split_json.encode("utf-8")).hexdigest()
    if actual_hash != manifest["split_sha256"]:
        raise ValueError("O hash das divisões não corresponde ao manifesto")

    originals = {}
    for source_name, original_split in (("train", "official_train"), ("test", "official_test")):
        source = manifest["sources"][source_name]
        path = Path(source["path"])
        if sha256(path) != source["sha256"]:
            raise ValueError(f"O arquivo de {source_name} não corresponde ao manifesto")
        for example in read_examples(path, original_split):
            originals[example["id"]] = example

    labels = manifest["label_to_id"]
    if len(labels) != NUM_LABELS or set(labels.values()) != set(range(NUM_LABELS)):
        raise ValueError(f"O manifesto precisa mapear {NUM_LABELS} rótulos para IDs únicos de 0 a {NUM_LABELS - 1}")

    all_ids = [example_id for ids in split_ids.values() for example_id in ids]
    if len(all_ids) != len(set(all_ids)) or set(all_ids) != set(originals):
        raise ValueError("Os IDs das divisões não correspondem aos exemplos originais")
    if set(split_ids) != {"train", "validation", "test"}:
        raise ValueError("As divisões precisam ser train, validation e test")
    if any(not item.startswith("official_train:") for key in ("train", "validation") for item in split_ids[key]):
        raise ValueError("Treino e validação devem vir do treino oficial")
    if any(not item.startswith("official_test:") for item in split_ids["test"]):
        raise ValueError("O teste precisa preservar a divisão oficial")

    splits = {}
    for name, ids in split_ids.items():
        splits[name] = []
        for example_id in ids:
            example = originals[example_id]
            if example["label"] not in labels:
                raise ValueError(f"Rótulo desconhecido no exemplo {example_id}")
            splits[name].append({**example, "label_id": labels[example["label"]]})
    return splits, manifest


# Impede que achados relevantes passem despercebidos antes do diagnóstico ou treino.
def check_audit_review(preparation: Path) -> None:
    audit = json.loads((preparation / "audit.json").read_text(encoding="utf-8"))
    concerning = bool(audit["empty_text_ids"] or audit["empty_label_ids"])
    for duplicates in audit["comparisons"].values():
        concerning |= any(item["cross_split"] or item["conflicting_labels"] for item in duplicates)
    if not concerning:
        return

    review_path = preparation / "audit_review.json"
    if not review_path.exists():
        raise ValueError("A auditoria identificou problemas; apresente os achados ao autor antes de prosseguir")
    review = json.loads(review_path.read_text(encoding="utf-8"))
    if review.get("audit_sha256") != sha256(preparation / "audit.json") or not review.get("author_decision"):
        raise ValueError("A revisão da auditoria precisa registrar a decisão do autor e o hash do relatório")
    
# Cria lotes com padding dinâmico; não carrega o teste implicitamente.
def make_dataloader(examples, tokenizer, max_length: int, batch_size: int, shuffle: bool):
    if batch_size not in (8, 16, 32):
        raise ValueError("O batch deve ser um dos candidatos 8, 16 ou 32")
    if not examples:
        raise ValueError("A divisão não contém exemplos")

    def collate(items):
        encoded = tokenize_batch(tokenizer, [item["text"] for item in items], max_length)
        encoded["labels"] = torch.tensor([item["label_id"] for item in items], dtype=torch.long)
        return encoded

    return DataLoader(examples, batch_size=batch_size, shuffle=shuffle, num_workers=0, collate_fn=collate)
