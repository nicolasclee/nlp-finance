# Modelo de classificação com encoder BERT, pooler e saída para 77 intenções.

from torch import nn
from transformers import BertModel


# Carrega os pesos originais e acrescenta uma cabeça de classificação treinável.
class IntentClassifier(nn.Module):
    def __init__(self, model_name: str, revision: str):
        super().__init__()
        if not revision.strip():
            raise ValueError("Informe a revisão imutável do checkpoint")

        self.encoder, loading_info = BertModel.from_pretrained(
            model_name,
            revision=revision,
            output_loading_info=True,
            local_files_only=True,
        )

        # Pesos ausentes no encoder ou pooler não podem ser inicializados silenciosamente.
        missing = loading_info.get("missing_keys", [])
        mismatched = loading_info.get("mismatched_keys", [])
        errors = loading_info.get("error_msgs", [])
        if missing or mismatched or errors:
            raise RuntimeError(
                f"Falha ao carregar encoder/pooler: ausentes={missing}, "
                f"incompatíveis={mismatched}, erros={errors}"
            )
        if self.encoder.config.hidden_size != 768:
            raise ValueError("O encoder precisa produzir vetores de 768 posições")
        if self.encoder.pooler is None:
            raise ValueError("O checkpoint precisa fornecer um pooler")

        self.loading_info = loading_info
        self.dropout = nn.Dropout(0.1)
        self.classifier = nn.Linear(768, 77)

    # Retorna logits: a função de perda aplica a transformação necessária no treino.
    def forward(self, input_ids, attention_mask, token_type_ids=None):
        output = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
        )
        representation = self.dropout(output.pooler_output)
        return self.classifier(representation)
