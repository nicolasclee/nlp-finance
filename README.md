# nlp-finance
Trabalho de PLN da UFRGS: classificação de intenções bancárias no BANKING77, comparando checkpoints BERT e FinBERT e duas regras de abstenção.

## Passo a passo até o diagnóstico

O fluxo **ainda não foi validado com PyTorch, GPU ou dados reais**. Os comandos abaixo foram preparados para Linux; se algum falhar, investigar antes de continuar. Não é necessário arquivo `.env` para usar os arquivos locais.

**Downloads e espaço:** os pesos dos dois modelos somam cerca de **882 MB**. A instalação de Python e das bibliotecas pode ultrapassar 50 MB e consumir vários gigabytes, dependendo da versão de PyTorch/CUDA. Reserve espaço também para caches e checkpoints. Baixar arquivos não insere seu conteúdo automaticamente no contexto da conversa.

### 1. Entrar no projeto e verificar a GPU

```sh
cd ~/ufrgs/pln/nlp-finance
nvidia-smi
```

O comando deve mostrar a GPU e a versão do driver. Se falhar, resolver o acesso à GPU antes de executar o diagnóstico. Na última verificação deste ambiente, o driver não respondeu; isso não prova que a GPU esteja indisponível no terminal do autor.

### 2. Instalar `uv` e Python 3.11

Se o `uv` ainda não estiver instalado, usar o instalador documentado em [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/):

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Abrir um novo terminal, voltar à pasta do projeto e conferir a instalação:

```sh
cd ~/ufrgs/pln/nlp-finance
uv --version
```

```sh
uv python install 3.11
```

O tamanho do download de Python depende da distribuição e pode ultrapassar 50 MB.

### 3. Instalar as bibliotecas

```sh
uv sync
```

Esta etapa pode baixar vários gigabytes, especialmente para PyTorch/CUDA; o tamanho depende das versões resolvidas. Verificar se o PyTorch consegue acessar a GPU:

```sh
uv run python -c "import torch; print('PyTorch:', torch.__version__); print('CUDA disponível:', torch.cuda.is_available()); print('CUDA do PyTorch:', torch.version.cuda)"
```

É necessário aparecer `CUDA disponível: True`. Se aparecer `False`, conferir a compatibilidade entre driver e variante de PyTorch antes de continuar. O `uv sync` não garante, por si só, a escolha da variante CUDA adequada; ver [guia uv/PyTorch](https://docs.astral.sh/uv/guides/integration/pytorch/).

### 4. Baixar e preparar o BANKING77

Os CSVs oficiais somam aproximadamente **1,1 MB**. Os comandos abaixo usam uma revisão imutável do repositório oficial. Execute-os apenas se `train.csv` e `test.csv` ainda não existirem nessa pasta: `curl -o` sobrescreve arquivos existentes.

```sh
mkdir -p data/banking77
```

```sh
curl -fL https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/9d081458ff52e53cf7e848f414e6e9344e4e6696/banking_data/train.csv -o data/banking77/train.csv
```

```sh
curl -fL https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/9d081458ff52e53cf7e848f414e6e9344e4e6696/banking_data/test.csv -o data/banking77/test.csv
```

Preparar os dados; `resultados/preparacao` deve ser uma pasta nova:

```sh
uv run python -m nlp_finance prepare \
  --train data/banking77/train.csv \
  --test data/banking77/test.csv \
  --revision 9d081458ff52e53cf7e848f414e6e9344e4e6696 \
  --output resultados/preparacao
```

`splits.json` registra os IDs, `manifest.json` guarda hashes e configurações, e `audit.json` apresenta possíveis problemas. A validação vem de aproximadamente 10% do treino oficial; o teste oficial permanece separado.

Inspecionar `audit.json` antes de continuar. Se houver sobreposição entre divisões, rótulos conflitantes ou textos vazios, discutir os achados antes de alterar qualquer dado. O código exige registrar a decisão em `audit_review.json`, com `audit_sha256` e `author_decision`, quando encontra esses problemas.

### 5. Baixar modelos e tokenizers

**Aviso de download:** aproximadamente **440 MB para BERT e 442 MB para FinBERT**, além dos arquivos pequenos dos tokenizers. Os arquivos vão para o cache do Hugging Face; reserve espaço extra para arquivos temporários. Fontes: [BERT](https://huggingface.co/google-bert/bert-base-uncased/blob/main/model.safetensors) e [FinBERT](https://huggingface.co/yiyanghkust/finbert-pretrain/blob/main/pytorch_model.bin).

O comando resolve as revisões dos dois repositórios, baixa somente os arquivos indicados e as registra em `revisoes.json`. O arquivo de saída deve ser novo:

```sh
uv run python - <<'PY'
import json
from pathlib import Path

from huggingface_hub import HfApi, snapshot_download

if Path("revisoes.json").exists():
    raise FileExistsError("revisoes.json já existe; revise-o antes de continuar")

modelos = {
    "google-bert/bert-base-uncased": "model.safetensors",
    "yiyanghkust/finbert-pretrain": "pytorch_model.bin",
}

revisoes = {}
api = HfApi()

for nome, pesos in modelos.items():
    revisao = api.model_info(nome).sha
    print(f"Baixando {nome}, revisão {revisao}...")
    snapshot_download(
        repo_id=nome,
        revision=revisao,
        allow_patterns=[
            pesos,
            "config.json",
            "tokenizer.json",
            "tokenizer_config.json",
            "special_tokens_map.json",
            "vocab.txt",
        ],
    )
    revisoes[nome] = revisao

with Path("revisoes.json").open("x", encoding="utf-8") as arquivo:
    json.dump(revisoes, arquivo, indent=2)

print("Revisões registradas em revisoes.json")
PY
```

### 6. Executar o diagnóstico

Depois de verificar a auditoria, executar em uma pasta de saída nova:

```sh
CUBLAS_WORKSPACE_CONFIG=:4096:8 uv run python -m nlp_finance diagnose \
  --preparation resultados/preparacao \
  --revisions revisoes.json \
  --output resultados/diagnostico
```

O diagnóstico usa a GPU em treinamentos curtos para medir memória, velocidade e estabilidade. Sua duração ainda é desconhecida; ele não inicia os 12 treinamentos científicos. O resultado principal é `resultados/diagnostico/diagnostic.json`. Se o status for `needs_review`, revisar os achados antes de continuar.

## Organização do código

- `data.py`: leitura, divisão e auditoria dos dados.
- `model_selection.py`: escolha de épocas e taxas usando a validação.
- `abstention_metrics.py`: limiares e métricas de abstenção.
- `tokenization.py`: conversão de mensagens em tokens, sem cortes.
- `model.py`: encoder BERT, pooler e saída para 77 intenções.
- `training.py` e `trainer_training.py`: diagnóstico numérico, treinamento com `Trainer` e registro de uma tentativa.
- `dataset.py`: reconstrução das divisões e montagem dos lotes.
- `hardware_diagnostic/`: medições de recursos antes dos treinamentos completos.
- `experiment/`: coordenação do treinamento, seleção, avaliação final e relatório.
- `constants.py`: constantes compartilhadas, como o número de intenções.
- `predictions.py` e `evaluation.py`: previsões e métricas compartilhadas pelos fluxos.
- `__main__.py`: comando de preparação executado pelo terminal.

## Depois do diagnóstico

Transformers 4.57.1 e Accelerate 1.10.1 estão especificados para a integração com o Trainer; o ambiente e o lockfile ainda precisam ser resolvidos. Antes das execuções científicas, validar o carregamento dos modelos e uma execução curta do fluxo completo.

1. As 12 configurações estão em `configuracoes/`, com seeds 13, 37 e 73 e taxas 0.00002 e 0.00005 para cada modelo. Os campos de recursos correspondem ao diagnóstico atual. Cada tentativa precisa de uma pasta nova; por exemplo:

   ```sh
   CUBLAS_WORKSPACE_CONFIG=:4096:8 python -m nlp_finance train --preparation resultados/preparacao --diagnostic resultados/diagnostico/diagnostic.json --config configuracoes/bert_2e-5_seed13.json --output resultados/bert_2e-5_seed13
   ```

2. Congelar a seleção na validação, passando as 12 pastas em `--runs`; depois executar `evaluate` com o arquivo congelado. Finalmente, `report` gera tabelas, curvas e exemplos. Consulte `python -m nlp_finance --help` e o `--help` de cada comando para os argumentos.

Uma falha interrompe a tentativa e é registrada. Para tentar novamente, usar uma pasta nova com a mesma configuração e seed; não retomar pesos de uma execução incompleta. A validação serve à seleção; o teste só é usado depois do congelamento.
