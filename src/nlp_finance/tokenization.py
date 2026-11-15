# Tokenização sem cortes e com preenchimento à direita.

from collections.abc import Sequence


# Carrega o tokenizer específico do checkpoint a partir do cache local.
def load_tokenizer(model_name: str, revision: str):
    from transformers import AutoTokenizer

    if not revision.strip():
        raise ValueError("Informe a revisão imutável do tokenizer")

    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        revision=revision,
        local_files_only=True,
    )
    tokenizer.padding_side = "right"
    if tokenizer.pad_token_id is None:
        raise ValueError("O tokenizer não possui marcador de padding")
    return tokenizer


# Conta tokens com marcadores especiais, sem remover trechos das mensagens.
def token_lengths(tokenizer, texts: Sequence[str]) -> list[int]:
    if not texts:
        raise ValueError("Informe pelo menos uma mensagem")

    encoded = tokenizer(list(texts), add_special_tokens=True, truncation=False)
    return [len(token_ids) for token_ids in encoded["input_ids"]]


# Preenche o lote até a maior mensagem; excedentes interrompem a execução.
def tokenize_batch(tokenizer, texts: Sequence[str], max_length: int):
    if max_length not in (64, 128):
        raise ValueError("O limite de entrada precisa ser 64 ou 128 tokens")
    if tokenizer.padding_side != "right":
        raise ValueError("O padding precisa ser feito à direita")
    if not texts:
        raise ValueError("Informe pelo menos uma mensagem")

    encoded = tokenizer(
        list(texts),
        add_special_tokens=True,
        truncation=False,
        padding=False,
        return_attention_mask=True,
    )
    lengths = [len(token_ids) for token_ids in encoded["input_ids"]]
    too_long = [(index, length) for index, length in enumerate(lengths) if length > max_length]
    if too_long:
        raise ValueError(f"Mensagens acima de {max_length} tokens: {too_long}")

    return tokenizer.pad(encoded, padding=True, return_tensors="pt")
