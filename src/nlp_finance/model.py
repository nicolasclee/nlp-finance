# Carregamento do classificador BERT pronto, como no laboratório.

from transformers import BertForSequenceClassification

from .constants import NUM_LABELS


# Carrega o checkpoint e configura a saída para as intenções do BANKING77.
def load_model(model_name: str, revision: str):
    if not revision.strip():
        raise ValueError("Informe a revisão imutável do checkpoint")

    model, loading_info = BertForSequenceClassification.from_pretrained(
        model_name,
        revision=revision,
        num_labels=NUM_LABELS,
        classifier_dropout=0.1,
        return_dict=True,
        output_loading_info=True,
        local_files_only=True,
    )

    # A cabeça é nova; pesos ausentes no encoder ou pooler exigem revisão.
    expected_new_weights = {"classifier.weight", "classifier.bias"}
    missing = set(loading_info.get("missing_keys", []))
    unexpected_missing = sorted(missing - expected_new_weights)
    mismatched = loading_info.get("mismatched_keys", [])
    errors = loading_info.get("error_msgs", [])
    if unexpected_missing or mismatched or errors:
        raise RuntimeError(
            f"Falha ao carregar encoder/pooler: ausentes={unexpected_missing}, "
            f"incompatíveis={mismatched}, erros={errors}"
        )
    if model.config.hidden_size != 768 or model.bert.pooler is None:
        raise ValueError("O checkpoint precisa ter encoder de 768 posições e pooler")

    model.loading_info = loading_info
    return model
