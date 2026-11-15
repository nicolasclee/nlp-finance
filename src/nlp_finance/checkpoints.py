# Identificação dos arquivos de um checkpoint armazenado localmente.

from pathlib import Path

from huggingface_hub import snapshot_download

from .data import sha256


# Calcula os hashes dos arquivos relevantes no cache, sem acessar a rede.
def checkpoint_files(model_name: str, revision: str) -> dict:
    snapshot = Path(snapshot_download(model_name, revision=revision, local_files_only=True))
    names = {"config.json", "tokenizer.json", "tokenizer_config.json", "special_tokens_map.json", "vocab.txt"}
    files = {}
    for path in sorted(snapshot.rglob("*")):
        if path.is_file() and (path.name in names or path.suffix in (".bin", ".safetensors")):
            files[str(path.relative_to(snapshot))] = sha256(path)
    if "config.json" not in files or not any(name.endswith((".bin", ".safetensors")) for name in files):
        raise ValueError(f"Arquivos de configuração ou pesos ausentes no cache de {model_name}")
    return files
