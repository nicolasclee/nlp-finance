git puhs# Registro de pesquisa

Registro retrospectivo das consultas desta sessão, consolidado em 2026-11-14. Não substitui decisões do PLAN.md. Datas individuais das consultas anteriores não foram registradas.

## Convenções

- **Verificado:** trecho relevante consultado; não implica leitura integral ou reprodução dos experimentos.
- **Triagem:** fonte localizada por busca ou resumo; exige leitura antes de fundamentar decisões.
- Para novas pesquisas, registrar data, pergunta, fonte, trecho/seção, achado, limites e relação com decisões. Manter sugestões distintas de decisões confirmadas.
- Referências abaixo são fontes primárias. Resultados de busca, blogs e repositórios de terceiros vistos na triagem não foram adotados como evidência acadêmica.

## Perguntas pesquisadas

1. Como trabalhos sobre BANKING77 separam treino, validação e teste?
2. Existe fundamento publicado para abstenção pela maior saída softmax?
3. Como escolher e avaliar limiares sem usar o teste para ajustá-los?
4. Há referência diretamente compatível com a diferença entre as duas maiores probabilidades?

Buscas incluíram BANKING77 com termos validation/split/BERT; selective classification com confidence/threshold/risk/coverage; e top-two margin/softmax. Não foi feita revisão sistemática ou exaustiva.

## R1 — BANKING77 e classificação de intenções

- **Fonte:** Casanueva et al. (2020), *Efficient Intent Detection with Dual Sentence Encoders*.
- **Links:** [publicação](https://aclanthology.org/2020.nlp4convai-1.5/), [PDF](https://aclanthology.org/2020.nlp4convai-1.5.pdf).
- **Status:** verificado em trechos do artigo, incluindo introdução e discussão de invariância a hiperparâmetros.
- **Achado:** apresenta BANKING77 com 13.083 exemplos e 77 intenções. Discute o custo de reservar dados escassos para validação, especialmente em few-shot.
- **Limite:** não fundamenta a sugestão de reservar 20% para nossa validação nem valida ferramentas financeiras corporativas.
- **Relação:** D1 e D4; contextualiza o dataset, sem resolver o protocolo de abstenção.

## R2 — Abstenção por Softmax Response

- **Fonte:** Geifman e El-Yaniv (2017), *Selective Classification for Deep Neural Networks*, NeurIPS.
- **Links:** [publicação](https://proceedings.neurips.cc/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html), [PDF](https://proceedings.neurips.cc/paper/2017/file/4a8423d5e91fda00bb7e46540e2b0cf1-Paper.pdf).
- **Status:** verificado em introdução, formulação e §5.1.
- **Achado:** usa a maior saída softmax como sinal para rejeição de previsões de uma rede já treinada; avalia risco versus cobertura. Propõe SGR para selecionar limiares com controle probabilístico de risco sob suas condições.
- **Protocolo observado:** em CIFAR-10, separa o conjunto usado para ajustar SGR daquele usado para testar os limites de risco (§5.1).
- **Limite:** experimentos de visão; não estabelece proporção ideal para BANKING77. Um limiar arbitrário ou simplesmente ajustado pelo erro empírico não herda as garantias de SGR.
- **Relação:** fundamento para D2 e critério de maior pontuação em D3. Implementar SGR não foi decidido.

## R3 — Precedente de aproximadamente 10% de validação no BANKING77

- **Fonte:** Botzer et al. (2023), *TK-KNN: A Balanced Distance-Based Pseudo Labeling Approach for Semi-Supervised Intent Classification*, Findings of EMNLP.
- **Link:** [PDF](https://aclanthology.org/2023.findings-emnlp.429.pdf).
- **Status:** verificado em §4.1, tabela 1 e §4.3.
- **Achado:** cria validação a partir do treino original: 9.002 treino, 1.001 validação e 3.080 teste. Usa BERT-base e validação para early stopping.
- **Limite:** tarefa semissupervisionada; não demonstra que aproximadamente 1.000 exemplos bastam para ajustar nossos critérios de abstenção. Esses números não equivalem a uma verificação de estratificação.
- **Relação:** precedente para D4; percentual ainda não aprovado.

## R4 — Outro precedente de divisão 90/10

- **Fonte:** Gulati et al. (2024), *Out-of-Distribution Detection through Soft Clustering with Non-Negative Kernel Regression*, Findings of EMNLP.
- **Link:** [PDF](https://aclanthology.org/2024.findings-emnlp.758.pdf).
- **Status:** verificado no apêndice B, parágrafo BANKING77.
- **Achado:** relata 10.003 exemplos oficiais de treino e 3.080 de teste; divide o treino em 90/10 para treino/validação.
- **Limite:** investigação de detecção fora da distribuição com seleção de classes; não é o mesmo problema de abstenção em classificação fechada das 77 intenções.
- **Relação:** D4; precedente de proporção, não prova de suficiência ou de optimalidade.

## R5 — Separação de calibração e validação

- **Fonte:** *Deep Neural Network Benchmarks for Selective Classification*, arXiv:2401.12708, versão v2 consultada.
- **Links:** [registro](https://arxiv.org/abs/2401.12708), [texto consultado](https://arxiv.org/html/2401.12708v2).
- **Status:** verificado em §5.1 e discussão das limitações.
- **Achado:** usa treino/calibração/validação/teste em 60/10/10/20%; compara erro seletivo e cobertura, com bootstrap no teste. Separa ajuste dos hiperparâmetros e calibração da função de confiança.
- **Limite:** benchmark de imagens e dados tabulares. Não devemos transportar automaticamente proporções ou garantias para NLP. Calibração nesse protocolo não significa necessariamente temperature scaling.
- **Relação:** evidencia alternativa à reutilização de uma única validação em D4. Quarto subconjunto e bootstrap não foram aprovados.

## R6 — Seleção a partir dos scores de classificação

- **Fonte:** *Towards Better Selective Classification*, arXiv:2206.09034.
- **Links:** [registro](https://arxiv.org/abs/2206.09034), [PDF localizado](https://openreview.net/pdf?id=5gDz_yTcst).
- **Status:** trechos do texto HTML verificados em 2026-11-14: discussão do mecanismo, apêndices D.3 e D.7. [Texto consultado](https://arxiv.org/html/2206.09034). PDF no OpenReview bloqueado por verificação de navegador.
- **Achado:** compara entropia e Softmax Response no mesmo classificador convencional (tabelas 8–9) e apresenta curvas risco-cobertura. A seleção por Softmax Response pode ser aplicada sem retreinar.
- **Limite:** resultados de visão; não sustenta limiar universal, superioridade no BANKING77 ou margem entre probabilidades. O artigo também inclui métodos que alteram treinamento, distintos da seleção pós-treinamento.

## R7 — Possível análise de qualidade dos rótulos

- **Fonte:** *Label Errors in BANKING77* (2022).
- **Links:** [publicação](https://aclanthology.org/2022.insights-1.19/), [PDF](https://aclanthology.org/2022.insights-1.19.pdf).
- **Status:** triagem por resumo.
- **Indicação:** investiga possíveis erros de anotação e seus impactos na classificação de intenções.
- **Pendente:** examinar metodologia antes de usar na discussão de erros. Alterar rótulos ou dataset não foi proposto nem aprovado.

## R8 — Referência diretamente compatível com a margem de probabilidades

- **Consulta:** 2026-11-14. Buscas: selective classification com top two probabilities e softmax margin.
- **Fonte:** Cattelan e Silva (2024), *How to Fix a Broken Confidence Estimator: Evaluating Post-hoc Methods for Selective Classification with Deep Neural Networks*, UAI, PMLR 244.
- **Links:** [publicação](https://proceedings.mlr.press/v244/cattelan24a.html), [texto v4 consultado](https://arxiv.org/html/2305.15508v4).
- **Status:** verificado em §3.2, equações 3–6, §4.2, §5 e tabelas 1–2.
- **Achado:** define MSP como maior probabilidade e SoftmaxMargin como diferença entre as duas maiores probabilidades; distingue margem de logits. Compara os critérios após treinamento em ImageNet. Usa curvas risco-cobertura e métricas de área; discute influência da qualidade do classificador na comparação. Separa ajuste pós-treinamento e avaliação.
- **Limite:** fundamenta os critérios de D3, sem demonstrar superioridade no BANKING77 ou determinar limiares numéricos.
- **Acesso:** PDF da PMLR não processado pelo navegador; verificação feita no HTML do arXiv v4 e metadados da publicação.

## Síntese e pendências

- **Fundamentado em precedente:** rejeição pela maior saída softmax em um classificador já treinado (R2); divisão de validação a partir do treino oficial do BANKING77 (R3–R4).
- **Lacuna resolvida em 2026-11-14:** R8 define e compara exatamente a diferença entre as duas maiores probabilidades escolhida em D3. Isso resolve o precedente metodológico, não sua eficácia no BANKING77. Margens sobre logits ou distâncias não são automaticamente equivalentes.
- **Ainda aberto:** objetivo para selecionar limiares, avaliação de incerteza, proporção de validação e possível separação adicional de dados para limiares.
- **Correção da sugestão inicial:** 20% foi heurística da IA, sem justificativa específica encontrada para este estudo; 10% possui precedentes, mas não está aprovado e não é uma proporção comprovadamente ótima.
- **Distinção central:** no desenho pós-treinamento discutido, limiares não alteram pesos nem acurácia sobre todos os exemplos; alteram cobertura e erro entre os aceitos.
- **Próximo trabalho:** concluir revisão direcionada de critérios e seleção de limiares, distinguindo avaliação empírica de garantias estatísticas; depois retomar decisões com o autor.

## Encaminhamento da revisão — 2026-11-14

- A comparação pós-treinamento de MSP e SoftmaxMargin tem precedente; não exige inventar uma arquitetura ou modificar pesos.
- Proposta para discussão, ainda não decisão: primeiro avaliar curvas risco-cobertura, sem fixar um único limiar arbitrário; depois definir procedimento de escolha de pontos operacionais na validação e avaliar os limiares congelados no teste.
- Distinguir duas perguntas: qualidade do sinal ao longo das coberturas versus desempenho de uma regra operacional fixada antes do teste. Uma curva descritiva de teste não deve ser usada para escolher o limiar operacional.
- R2 é referência para controle estatístico de risco; comparar curvas empiricamente não equivale a implementar esse controle. Não prometer limite de erro garantido sem adotar e verificar o método correspondente.
- Proporção de validação e eventual subconjunto separado para limiares continuam sem decisão. R3–R4 sustentam precedente de aproximadamente 10%, não uma proporção ótima.
- Nenhuma nova métrica, divisão ou variante de treinamento foi aprovada com esta pesquisa.
