# Classificação de intenções bancárias com BERT e FinBERT

Projeto da disciplina de Processamento de Linguagem Natural da UFRGS. O estudo compara BERT e FinBERT na classificação das 77 intenções do BANKING77 e investiga se regras de abstenção reduzem os erros entre as previsões aceitas.

## Experimento

O conjunto contém 13.083 mensagens em inglês. A divisão usada tem 9.002 exemplos de treinamento, 1.001 de validação e 3.080 de teste. O teste oficial foi preservado.

Os modelos `google-bert/bert-base-uncased` e `yiyanghkust/finbert-pretrain` passaram por fine-tuning com duas taxas de aprendizado e três sementes por configuração. A taxa selecionada na validação para ambos foi 5 × 10⁻⁵. Após o treinamento, foram avaliadas duas regras de confiança: maior probabilidade softmax (MSP) e margem entre as duas maiores probabilidades. Os limiares foram escolhidos na validação para metas de cobertura de 80%, 90% e 95% e aplicados ao teste sem reajuste.

## Resultados

Médias de três sementes no teste, sem abstenção:

| Modelo | Acurácia | Macro-F1 | ECE |
| --- | ---: | ---: | ---: |
| BERT | 92,61% | 92,61% | 4,36% |
| FinBERT | 92,40% | 92,41% | 1,59% |

Com MSP e meta de 90% de cobertura na validação, o BERT atingiu 89,91% de cobertura efetiva e 3,49% de erro seletivo no teste; o FinBERT atingiu 89,49% e 3,01%, respectivamente. As coberturas diferem, portanto os pontos não representam uma comparação com cobertura exatamente igual.

Os resultados são descritivos: três sementes na mesma divisão não estabelecem significância estatística nem permitem atribuir diferenças ao pré-treinamento financeiro. Sete mensagens de teste têm correspondentes no treino que geram sequências de tokens idênticas; o efeito sobre as métricas não foi medido. A abstenção também não identifica todos os erros de alta confiança.

A análise completa está no [artigo](documents/artigo.tex) e no [relatório de resultados](resultados/relatorio/LEIA-ME.md). A [apresentação](documents/nlp_finance_apresentacao.html) pode ser aberta no navegador.

## Estrutura

- `src/nlp_finance/`: preparação dos dados, treinamento, seleção, avaliação e relatórios.
- `data/banking77/`: arquivos oficiais de treino e teste.
- `configuracoes/`: configurações dos experimentos.
- `resultados/`: divisões, auditoria, métricas, previsões e relatórios.
- `documents/`: artigo, apresentação e registros de pesquisa e planejamento.
- `revisoes.json`: revisões dos modelos utilizados.

## Execução

O projeto usa Python 3.11 e [uv](https://docs.astral.sh/uv/). Na raiz do projeto, instale as dependências e consulte os comandos disponíveis:

```sh
uv sync
uv run python -m nlp_finance --help
```

O fluxo segue as etapas `prepare`, `diagnose`, `train`, `freeze`, `evaluate` e `report`. Para preparar novamente os dados locais, use um diretório de saída novo:

```sh
uv run python -m nlp_finance prepare \
  --train data/banking77/train.csv \
  --test data/banking77/test.csv \
  --revision 9d081458ff52e53cf7e848f414e6e9344e4e6696 \
  --output resultados/preparacao_nova
```

A preparação registra a divisão e a auditoria; examine a auditoria antes de treinar. As 12 configurações em `configuracoes/` combinam as taxas 2 × 10⁻⁵ e 5 × 10⁻⁵ com as sementes 13, 37 e 73 para cada modelo. As escolhas finais e os limiares estão em `resultados/selecao/protocolo.json`, e a avaliação final está em `resultados/avaliacao_final/`.

Para consultar as opções de uma etapa, execute, por exemplo:

```sh
uv run python -m nlp_finance train --help
```

Treinamento e avaliação dos modelos exigem os checkpoints correspondentes e, na configuração utilizada, uma GPU compatível com CUDA. A instalação das dependências e o download dos modelos podem consumir vários gigabytes. Os pesos treinados não estão versionados; os artefatos em `resultados/` permitem consultar as métricas e previsões já produzidas. As etapas de geração exigem diretórios de saída novos: preserve os resultados existentes ao repetir o experimento.

## Licença

[MIT](LICENSE).
