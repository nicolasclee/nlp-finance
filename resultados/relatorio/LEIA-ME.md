# Resultados do experimento

As seis versões avaliadas foram escolhidas pela validação e aplicadas ao teste com limiares congelados. As médias abaixo usam três seeds por modelo; o desvio-padrão é amostral. Não são testes de significância.

## Classificação e calibração

| Modelo | Acurácia média | Desvio da acurácia | Macro-F1 médio | ECE médio |
|---|---:|---:|---:|---:|
| BERT | 92,61% | 0,78 ponto percentual | 92,61% | 4,36% |
| FinBERT | 92,40% | 0,18 ponto percentual | 92,41% | 1,59% |

A acurácia mede os acertos sem abstenção. O Macro-F1 resume o desempenho das 77 intenções, dando o mesmo peso a cada uma. A ECE resume a diferença entre confiança e frequência de acerto em 15 faixas; menor sugere melhor calibração nessa medição, mas o valor depende das faixas usadas.

## Abstenção

MSP usa a maior probabilidade; margem usa a diferença entre as duas maiores. Um modelo se abstém quando seu score fica abaixo do limiar escolhido na validação. O erro seletivo considera apenas as mensagens respondidas.

Exemplo com MSP e meta de 90% na validação, médias das três seeds:

| Modelo | Cobertura efetiva no teste | Erro entre respostas aceitas | Erro sem abstenção |
|---|---:|---:|---:|
| BERT | 89,91% | 3,49% | 7,39% |
| FinBERT | 89,49% | 3,01% | 7,60% |

As coberturas efetivas não são idênticas: essa tabela ilustra cada operação, mas não é comparação em cobertura exatamente igual. Nas curvas descritivas em 90% de cobertura, o erro médio com MSP foi 3,50% para BERT e 3,24% para FinBERT. Essa leitura das curvas é descritiva e não recalibra os limiares congelados.

A AURC resume o risco ao longo das coberturas; menor é melhor nessa convenção. As médias foram 0,0130 para BERT e 0,0110 para FinBERT com MSP; com margem, 0,0129 e 0,0109. Não há garantia estatística de risco associada a esses valores.

## Análise qualitativa

Os dois modelos confundiram com frequência as intenções `verify_my_identity` e `why_verify_identity`, ligadas à verificação de identidade. Foram 27 erros somados nas três execuções do BERT e 32 nas do FinBERT. Essas contagens incluem repetições do mesmo exemplo entre seeds; não representam 27 ou 32 pessoas diferentes.

Um exemplo do teste é “What is the need to verify my identity?”. O rótulo registrado é `why_verify_identity`, mas as seis versões preveram `verify_my_identity`. Com os limiares definidos para 90% de cobertura na validação, as duas regras aceitaram essa resposta equivocada em todas as seis versões. Nesse caso, a abstenção não identificou o erro.

Outro par recorrente foi `card_arrival` e `card_delivery_estimate`, sobre chegada ou prazo de entrega do cartão. Esses exemplos são selecionados para inspeção: não representam a distribuição completa de erros nem comprovam que os rótulos estejam incorretos.

## Limites e verificações

- Sete exemplos do teste têm correspondentes no treino que, embora diferentes em espaços, geram os mesmos tokens nos dois modelos. Os dados oficiais foram mantidos; o efeito sobre as métricas não foi medido.
- Três seeds usam a mesma divisão de dados. Elas não representam toda a incerteza e não sustentam, por si só, uma conclusão de significância.
- As métricas das seis execuções foram recalculadas a partir das previsões salvas e coincidiram com os arquivos da avaliação. O conjunto de teste não foi usado para ajustar os limiares.
- Os pesos treinados estão no disco local, fora do Git, e devem ser preservados com as configurações e os registros para reproduzir a avaliação.

## Arquivos

- `classification.csv` e `aggregate.json`: métricas individuais e médias com desvio.
- `abstention.csv`: cobertura, erro e AURC por modelo, seed, regra e meta.
- Arquivos `*_risk.svg`: curvas risco–cobertura por seed.
- Arquivos `*_reliability.svg`: diagramas de confiança por seed.
- `confusions.json` e `examples.json`: confusões e exemplos para leitura qualitativa; não são amostras representativas.
