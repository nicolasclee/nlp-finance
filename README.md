# nlp-finance
Trabalho de PLN da UFRGS: classificação de intenções bancárias no BANKING77, comparando checkpoints BERT e FinBERT e duas regras de abstenção.

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
- `training.py` e `trainer_training.py`: diagnóstico numérico, treinamento com `Trainer` e registro de uma tentativa.
- `dataset.py`: reconstrução das divisões e montagem dos lotes.
- `hardware_diagnostic/`: medições de recursos antes dos treinamentos completos.
- `constants.py`: constantes compartilhadas, como o número de intenções.
- `predictions.py`, `freeze.py` e `evaluation.py`: previsões, congelamento e métricas.
- `final_evaluation.py` e `report.py`: avaliação final e consolidação dos resultados.
- `__main__.py`: comando de preparação executado pelo terminal.

## Fluxo planejado de execução

O código abaixo **ainda não foi validado com PyTorch ou dados reais**. Antes de executar experimentos, revisar o código e validar o ambiente e o fluxo com um diagnóstico curto. O projeto prevê Python 3.11 e `uv`; Transformers 4.57.1 e Accelerate 1.10.1 estão especificados para a integração com o Trainer, mas o ambiente e o lockfile ainda precisam ser resolvidos. A instalação de PyTorch/CUDA e o download dos checkpoints podem consumir vários gigabytes; verificar os tamanhos e avisar antes de iniciar. Não é necessário arquivo `.env` para as operações locais.

1. Preparar os CSVs com o comando acima e inspecionar `audit.json`. Se houver sobreposição, rótulos conflitantes ou textos vazios, discutir os achados com o autor. A decisão deve ser registrada em `audit_review.json`, com `audit_sha256` e `author_decision`, sem alterar os dados automaticamente.
2. Ter os checkpoints e tokenizers no cache local. Criar um JSON de revisões com os nomes `google-bert/bert-base-uncased` e `yiyanghkust/finbert-pretrain` como chaves e seus hashes completos de commit como valores. O código usa somente arquivos locais e não baixa pesos.
3. Medir recursos antes de treinar:

   ```sh
   CUBLAS_WORKSPACE_CONFIG=:4096:8 python -m nlp_finance diagnose --preparation resultados/preparacao --revisions revisoes.json --output resultados/diagnostico
   ```

   O relatório `diagnostic.json` registra as medições. O status `needs_review` exige revisão dos achados; o código não escolhe outro protocolo automaticamente.

4. Para cada uma das 12 configurações, criar um JSON com `model_name`, `revision`, `seed`, `learning_rate`, `precision`, `batch_size`, `max_length` e `device`. Os três campos de recursos devem coincidir com o diagnóstico. Usar as seeds 13, 37 e 73 e as taxas 0.00002 e 0.00005 para cada modelo. Cada tentativa precisa de uma pasta nova:

   ```sh
   CUBLAS_WORKSPACE_CONFIG=:4096:8 python -m nlp_finance train --preparation resultados/preparacao --diagnostic resultados/diagnostico/diagnostic.json --config configuracao.json --output resultados/tentativa
   ```

5. Congelar a seleção na validação, passando as 12 pastas em `--runs`; depois executar `evaluate` com o arquivo congelado. Finalmente, `report` gera tabelas, curvas e exemplos. Consulte `python -m nlp_finance --help` e o `--help` de cada comando para os argumentos.

Uma falha interrompe a tentativa e é registrada. Para tentar novamente, usar uma pasta nova com a mesma configuração e seed; não retomar pesos de uma execução incompleta. A validação serve à seleção; o teste só é usado depois do congelamento.
