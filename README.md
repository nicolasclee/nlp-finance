# nlp-finance
[UFRGS NLP Final Project] Intent classification for corporate financial chatbots/agents: fine-tuning and evaluating BERT vs. FinBERT on BANKING77.

## Preparação dos dados

O primeiro bloco aceita os CSVs oficiais já disponíveis localmente, com colunas `text` e `category`. Ele não faz downloads nem modifica os arquivos de origem:

```sh
PYTHONPATH=src python -m nlp_finance prepare --train caminho/train.csv --test caminho/test.csv --revision COMMIT_IMUTAVEL --output resultados/preparacao
```

O diretório de saída deve ser novo. `manifest.json` registra hashes dos arquivos, sementes, mapeamento de rótulos e baseline da classe majoritária na validação; `splits.json` guarda os IDs originais de cada divisão; `audit.json` registra textos vazios, duplicatas e conflitos, tanto exatos como após normalização de espaços para comparação. A divisão separa aproximadamente 10% do treino oficial de forma estratificada e reproduzível; não altera o teste oficial.

Antes de treinar, inspecione a auditoria e discuta problemas que afetem a validade do experimento. O resultado da comparação de textos não autoriza remover exemplos nem alterar rótulos. A revisão informada identifica a origem; confira que ela corresponde aos arquivos, cujos hashes também são registrados.

## Organização do código

- `data.py`: leitura, divisão e auditoria dos dados.
- `model_selection.py`: escolha de épocas e taxas usando a validação.
- `abstention_metrics.py`: limiares e métricas de abstenção.
- `tokenization.py`: conversão de mensagens em tokens, sem cortes.
- `model.py`: encoder BERT, pooler e saída para 77 intenções.
- `__main__.py`: comando de preparação executado pelo terminal.

O treinamento dos modelos e a ligação entre essas etapas ainda não foram implementados. O carregamento do modelo e do tokenizer usa apenas arquivos locais: os checkpoints, as dependências e suas revisões precisam estar disponíveis antes do diagnóstico.
