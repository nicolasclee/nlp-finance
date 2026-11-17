# Classificação de intenções bancárias com BERT e FinBERT: uma análise de abstenção e calibração

**Nicolas Chin Lee · João Vítor Munhoz**  
Instituto de Informática — Universidade Federal do Rio Grande do Sul

> **Primeiro esboço para revisão dos autores.** O texto ainda deve ser diagramado no modelo SBC, revisado integralmente e conferido quanto ao limite de 8 a 10 páginas sem referências. A declaração de uso de IA ao final precisa ser completada e validada pelos autores.

## Resumo

A classificação de intenções permite encaminhar mensagens de clientes a fluxos de atendimento, mas previsões incorretas podem direcionar solicitações ao fluxo inadequado. Este trabalho compara BERT e FinBERT na identificação de 77 intenções bancárias do conjunto BANKING77, investigando também o efeito da abstenção em previsões de menor confiança. Os modelos foram ajustados sob o mesmo protocolo, com três sementes por configuração selecionada. Duas regras de aceitação foram avaliadas: a maior probabilidade prevista e a diferença entre as duas maiores probabilidades. Limiares foram escolhidos na validação para metas de cobertura de 80%, 90% e 95%, e aplicados sem reajuste ao teste. BERT e FinBERT alcançaram, respectivamente, acurácias médias de 92,61% e 92,40%. Com a maior probabilidade e meta de 90%, os erros entre previsões aceitas foram 3,49% e 3,01%, com coberturas efetivas próximas de 90%. FinBERT apresentou menor erro de calibração estimado e menor área sob a curva risco–cobertura. Os resultados são descritivos e não estabelecem significância estatística ou causalidade.

**Palavras-chave:** classificação de intenções; BANKING77; BERT; FinBERT; classificação seletiva; calibração.

## 1. Introdução

Sistemas de atendimento precisam interpretar mensagens expressas de maneiras diferentes para encaminhar solicitações aos serviços apropriados. No domínio bancário, um pedido sobre a chegada de um cartão pode ser semanticamente próximo de uma pergunta sobre a previsão de entrega, embora cada um pertença a uma intenção distinta. A classificação de intenções procura associar cada mensagem a uma categoria previamente definida. Mesmo em um conjunto restrito a um domínio, a proximidade entre categorias torna a tarefa desafiadora [Casanueva et al. 2020].

Modelos baseados em Transformers fornecem representações contextuais que podem ser ajustadas a tarefas supervisionadas [Devlin et al. 2019]. Uma alternativa ao uso de modelos gerais é empregar versões pré-treinadas com textos de um domínio específico. Em finanças, variantes de FinBERT foram propostas para incorporar linguagem financeira ao pré-treinamento [Yang et al. 2020]. A comparação entre modelos gerais e financeiros, contudo, depende das tarefas, das variantes e das condições de treinamento consideradas [Peng et al. 2021].

Além de escolher uma intenção, um sistema pode decidir não aceitar uma previsão quando seu sinal de confiança é baixo. Essa decisão, chamada abstenção ou classificação seletiva, troca cobertura — a fração de mensagens aceitas — pelo risco de erro entre as respostas aceitas [Xin et al. 2021]. Por exemplo, encaminhar automaticamente menos pedidos pode reduzir erros nos pedidos efetivamente encaminhados, mas transfere os demais para algum procedimento alternativo. Este trabalho não implementa atendimento humano nem mede o custo dessa transferência.

A questão principal é: **como BERT e FinBERT se comparam na classificação das 77 intenções do BANKING77 e na relação entre cobertura e erro quando é permitida a abstenção?** Como questão complementar, investigamos como dois critérios calculados a partir das mesmas previsões — maior probabilidade e margem entre as duas maiores probabilidades — se comportam nessa relação.

A contribuição consiste em comparar os dois checkpoints sob um protocolo comum de ajuste, aplicar as duas regras de abstenção sem novo treinamento e analisar classificação, calibração e erros recorrentes. O estudo também descreve uma auditoria dos dados e explicita os limites da comparação, em particular a diferença entre checkpoints e a presença de exemplos de teste que geram entradas tokenizadas iguais às de treino.

## 2. Referencial teórico

### 2.1. Classificação de intenções e Transformers

Na classificação de intenções, uma mensagem recebe um rótulo entre um conjunto conhecido. Em BANKING77, a entrada é uma mensagem em inglês e a saída é uma das 77 intenções bancárias. O problema é multiclasse e de rótulo único: cada exemplo avaliado possui uma classe de referência. Dessa forma, a tarefa não consiste em gerar uma resposta textual, identificar entidades ou realizar uma operação financeira.

O BERT utiliza uma arquitetura Transformer pré-treinada para produzir representações contextualizadas de texto [Devlin et al. 2019]. Para adaptá-lo à classificação supervisionada, seus pesos podem ser ajustados com exemplos rotulados da tarefa. Uma camada de classificação transforma a representação da entrada em pontuações para as classes, que são convertidas em probabilidades por softmax na etapa de previsão.

Neste estudo, BERT-base-uncased representa o modelo geral, enquanto `yiyanghkust/finbert-pretrain` representa um modelo pré-treinado com dados financeiros [Yang et al. 2020]. O ajuste supervisionado é aplicado aos dois modelos no BANKING77. Como os checkpoints diferem em seu pré-treinamento e em seus tokenizers, uma diferença de resultado não pode ser atribuída exclusivamente ao domínio dos textos utilizados no pré-treinamento.

### 2.2. Abstenção e estimativas de confiança

Na classificação convencional, o sistema sempre devolve a classe de maior pontuação. Na classificação seletiva, uma regra adicional decide se a previsão será aceita. O sistema pode, assim, abster-se nos casos em que o sinal utilizado indique menor confiança. A cobertura é a proporção de exemplos aceitos; o risco, ou erro seletivo, é a proporção de erros entre esses exemplos [Xin et al. 2021].

Este trabalho usa dois sinais calculados após o ajuste dos pesos. A **maior probabilidade softmax** — *maximum softmax probability* (MSP) — é o valor da classe de maior probabilidade. A **margem softmax** é a diferença entre as duas maiores probabilidades. Uma margem pequena indica que as duas classes mais prováveis receberam valores próximos. Cattelan e Silva [2024] analisam esses e outros sinais de confiança em classificação seletiva; seus experimentos envolvem classificadores de imagens, e não demonstram qual critério será melhor para BANKING77.

Para cada regra, uma previsão é aceita quando o sinal atinge ou supera um limiar. Um limiar mais restritivo tende a reduzir a cobertura. Os sinais servem para ordenar e selecionar previsões, mas não garantem individualmente que uma resposta aceita esteja correta.

### 2.3. Métricas de avaliação

A **acurácia** mede a proporção de previsões corretas entre todas as mensagens. O **Macro-F1** é a média aritmética do F1 calculado separadamente para cada intenção, dando o mesmo peso às 77 classes. As métricas respondem a perguntas diferentes: a primeira resume acertos gerais; a segunda combina precisão e recall por classe.

Para avaliar a abstenção, é necessário informar cobertura e erro seletivo em conjunto. Uma redução de erro deve ser interpretada levando em conta a fração de mensagens não atendidas automaticamente. A área sob a curva risco–cobertura, ou **AURC**, resume o erro seletivo ao longo de níveis de cobertura; valores menores indicam menor área segundo a convenção utilizada. A área também depende da qualidade inicial do classificador, portanto não deve ser atribuída exclusivamente à regra de confiança [Cattelan e Silva 2024].

A calibração pergunta se a confiança atribuída às previsões corresponde à frequência observada de acerto. Por exemplo, entre previsões com confiança próxima de 80%, uma frequência de acerto próxima de 80% indica correspondência naquela faixa. O **erro de calibração esperado** (*expected calibration error*, ECE) agrega as diferenças entre confiança média e frequência de acerto em faixas, ponderadas por sua quantidade de exemplos [Guo et al. 2017]. Neste trabalho, a ECE é um diagnóstico secundário; calibração e capacidade de ordenar erros para abstenção não são propriedades equivalentes.

## 3. Trabalhos relacionados

Casanueva et al. [2020] apresentam o BANKING77 no estudo de detecção de intenções com representações de sentenças. O conjunto reúne 13.083 mensagens e 77 intenções em um único domínio, tornando possível avaliar distinções finas entre pedidos bancários. Os autores também relatam resultados com BERT ajustado à tarefa. Seu experimento fornece contexto para nosso trabalho, mas diferenças de variante e protocolo impedem uma comparação controlada dos números.

Peng et al. [2021] comparam BERT e variantes de FinBERT em tarefas financeiras, incluindo análise de sentimento, identificação de relações causais e compreensão de numerais. Os autores relatam que diferenças na forma de pré-treinamento e no vocabulário afetam os resultados. Essas tarefas não são equivalentes ao BANKING77: o estudo motiva a investigação de modelos gerais e especializados, mas não determina qual checkpoint deve prevalecer em classificação de intenções bancárias.

Xin et al. [2021] investigam classificação seletiva em processamento de linguagem natural e comparam modelos e estimadores de confiança. Seu trabalho usa a relação entre risco e cobertura para avaliar o comportamento das previsões aceitas. Nossa análise aplica essa perspectiva a dois modelos e duas regras calculadas sobre as mesmas previsões em BANKING77, sem reproduzir o método adicional de regularização proposto pelos autores.

Cattelan e Silva [2024] estudam estimadores de confiança aplicados após o treinamento de classificadores, sem modificar seus pesos. O trabalho fundamenta a distinção entre maior probabilidade e margem de probabilidades e destaca que a avaliação seletiva depende tanto do classificador quanto do sinal usado para ordenar previsões. Como seus experimentos utilizam classificadores ImageNet, a relação com nosso estudo é metodológica, não uma comparação direta de resultados.

Guo et al. [2017] analisam a calibração de redes neurais e empregam a ECE como medida agregada. Utilizamos a métrica para descrever a correspondência entre confiança e acerto, sem aplicar uma técnica de correção de calibração. Por fim, Huang et al. [2024] relatam 92,61% de acurácia média para BERT-base no BANKING77 em seu protocolo. Esse valor contextualiza a ordem de grandeza observada, mas os autores utilizam cinco sementes, taxa inicial e tamanho de lote diferentes; a identidade exata do checkpoint e dos arquivos de divisão não foi confirmada nesta revisão.

## 4. Metodologia

### 4.1. Conjunto de dados e divisão

Utilizamos os dados oficiais do BANKING77, que contêm mensagens em inglês anotadas com 77 intenções [Casanueva et al. 2020]. Preservamos o conjunto oficial de teste, com 3.080 mensagens e 40 exemplos por intenção. O conjunto oficial de treino foi dividido de forma estratificada, com semente 42, em 9.002 exemplos para treino e 1.001 para validação. A mesma divisão foi utilizada em todos os experimentos. Botzer et al. [2023] relatam quantidades equivalentes, o que constitui um precedente para a divisão, não uma demonstração de que essa proporção seja ótima para a seleção de limiares.

A Tabela 1 apresenta a função de cada parte. O treino ajusta os parâmetros; a validação orienta escolhas de épocas, taxas e limiares; o teste é reservado à avaliação final após o congelamento dessas escolhas. O uso da mesma validação para várias decisões pode levar a alguma adaptação às particularidades desse conjunto, embora o teste permaneça separado.

**Tabela 1. Divisão dos dados.**

| Conjunto | Mensagens | Uso |
|---|---:|---|
| Treino | 9.002 | Ajuste dos pesos dos modelos |
| Validação | 1.001 | Seleção de épocas, taxas e limiares |
| Teste | 3.080 | Avaliação final com escolhas congeladas |
| Total | 13.083 | 77 intenções |

A auditoria encontrou sete mensagens do teste com correspondentes no treino que, apesar de diferenças de espaços, geram sequências idênticas de IDs de tokens nos dois modelos. Mantivemos os textos e a divisão oficial. O impacto dessas sobreposições nas métricas não foi medido e deve ser considerado ao interpretar os resultados.

### 4.2. Modelos e treinamento

Os checkpoints empregados foram `google-bert/bert-base-uncased` e `yiyanghkust/finbert-pretrain`, cada um com seu tokenizer. Em ambos os casos, realizamos fine-tuning completo para classificação das 77 intenções, com representação do pooler e camada linear multiclasse. A função de perda foi entropia cruzada; o treinamento atualizou os parâmetros do encoder e do classificador. Utilizamos dropout de 0,1 na cabeça de classificação.

Foram testadas as taxas de aprendizado de 2 × 10⁻⁵ e 5 × 10⁻⁵, com três sementes de treinamento — 13, 37 e 73 — por modelo e taxa. Cada execução teve até cinco épocas, avaliadas ao final de cada época. Usamos AdamW, lote de 32 exemplos, comprimento máximo de 128 tokens, padding dinâmico e precisão mista FP16 no treinamento. A avaliação e a geração das previsões foram realizadas em FP32. O diagnóstico foi executado em uma GPU NVIDIA RTX 3070 Ti Laptop de 8 GB.

A melhor época de cada execução foi selecionada pela acurácia na validação; a taxa foi escolhida pela média das três acurácias de validação. A taxa 5 × 10⁻⁵ foi selecionada para ambos os modelos. Os resultados das seis execuções correspondentes, três por modelo, foram então avaliados no teste. As sementes repetem o treinamento na mesma divisão; elas não constituem diferentes partições independentes dos dados.

### 4.3. Regras de abstenção e protocolo de avaliação

Após o treinamento e a seleção, calculamos as probabilidades das 77 classes para cada mensagem. Aplicamos MSP e margem separadamente sobre as mesmas previsões, sem alterar os pesos. Para cada modelo, semente, regra e meta de cobertura, selecionamos na validação um limiar que aceitasse pelo menos a proporção desejada: 80%, 90% ou 95%. Foram aceitos exemplos com score maior ou igual ao limiar, incluindo empates no valor escolhido.

Os limiares foram congelados antes da avaliação no teste. A cobertura efetiva pode diferir da meta, porque a distribuição dos scores no teste não é necessariamente igual à da validação. A comparação de pontos com a mesma meta deve, portanto, informar suas coberturas efetivas; uma comparação em cobertura comum exige leitura descritiva das curvas, sem reajustar os limiares no teste.

Reportamos acurácia e Macro-F1 sem abstenção, cobertura e erro seletivo nos pontos operacionais, AURC para MSP e margem e ECE nas previsões sem abstenção. A ECE utiliza 15 faixas de largura igual, a confiança da classe prevista e a proporção de acertos. A AURC é calculada na escala de 0 a 1 como a média dos riscos dos prefixos ordenados por score, com tratamento de empates documentado no protocolo do projeto. Os resultados são médias de três execuções; os desvios de acurácia apresentados são desvios-padrão amostrais, não intervalos de confiança.

## 5. Experimentos e resultados

### 5.1. Escolha das taxas na validação

A Tabela 2 resume a média das acurácias da melhor época de cada execução na validação. Em ambos os modelos, 5 × 10⁻⁵ obteve a maior média entre as duas taxas testadas. O resultado sustenta a escolha dentro da grade utilizada, sem demonstrar que seja a melhor taxa entre todas as possíveis.

**Tabela 2. Acurácia média de validação por taxa, em porcentagem.**

| Modelo | 2 × 10⁻⁵ | 5 × 10⁻⁵ |
|---|---:|---:|
| BERT | 88,45 | **93,04** |
| FinBERT | 90,01 | **91,98** |

### 5.2. Classificação e calibração no teste

A Tabela 3 apresenta os resultados sem abstenção. BERT obteve acurácia média de 92,61%, e FinBERT, 92,40%, uma diferença descritiva de 0,21 ponto percentual. O Macro-F1 foi semelhante à acurácia para ambos. As médias não demonstram que uma diferença pequena seja estatisticamente significativa. Os desvios entre sementes indicam variação dos treinamentos na divisão utilizada, mas três sementes não caracterizam toda a incerteza do experimento.

**Tabela 3. Classificação e calibração no teste; médias de três sementes.**

| Modelo | Acurácia | Desvio da acurácia | Macro-F1 | ECE |
|---|---:|---:|---:|---:|
| BERT | 92,61% | 0,78 p.p. | 92,61% | 4,36% |
| FinBERT | 92,40% | 0,18 p.p. | 92,41% | 1,59% |

A ECE menor de FinBERT sugere melhor correspondência agregada entre confiança e frequência de acerto nesta medição. Ela não implica que toda previsão do modelo seja confiável, nem que o modelo ordene os erros de forma superior em qualquer nível de cobertura. A métrica depende das faixas e da amostra. Também não podemos atribuir a diferença observada exclusivamente ao pré-treinamento financeiro, pois os checkpoints diferem em outros aspectos.

A acurácia média de BERT coincide, após arredondamento, com os 92,61% relatados por Huang et al. [2024] para BERT-base em BANKING77. Os protocolos, no entanto, diferem: aquele trabalho usa cinco sementes, lote 24, taxa inicial 2 × 10⁻⁵ e parada antecipada. A coincidência numérica contextualiza a escala, mas não constitui replicação nem validação independente de nossos resultados.

### 5.3. Abstenção: metas, cobertura e erro

A Tabela 4 apresenta a regra MSP nas três metas de validação. Para BERT, o erro entre mensagens aceitas foi de 1,77%, 3,49% e 4,85%, respectivamente, enquanto a cobertura efetiva aumentou. Para FinBERT, os erros foram de 1,65%, 3,01% e 4,92%. Nesse conjunto de pontos, aceitar mais mensagens veio acompanhado de maior erro entre as aceitas. Esses valores não garantem o mesmo comportamento em dados externos ou para qualquer limiar.

**Tabela 4. MSP no teste: cobertura efetiva e erro seletivo médios. A meta foi definida na validação.**

| Meta de validação | BERT: cobertura | BERT: erro aceito | FinBERT: cobertura | FinBERT: erro aceito |
|---|---:|---:|---:|---:|
| 80% | 78,20% | 1,77% | 78,86% | 1,65% |
| 90% | 89,91% | 3,49% | 89,49% | 3,01% |
| 95% | 95,26% | 4,85% | 94,94% | 4,92% |

Sem abstenção, os erros médios foram 7,39% para BERT e 7,60% para FinBERT. Na meta de 90% com MSP, esses valores passaram a 3,49% e 3,01% entre as mensagens aceitas, com coberturas efetivas de 89,91% e 89,49%. A comparação entre os pontos de cada modelo não ocorre em cobertura exatamente igual. Nas curvas descritivas a 90% de cobertura, os erros médios com MSP foram 3,50% para BERT e 3,24% para FinBERT; essa leitura não corresponde a reajustar os limiares no teste.

A Tabela 5 apresenta os resultados da margem. As duas regras usam as mesmas previsões, mas produzem ordenações e limiares distintos. Em uma mesma meta, a cobertura efetiva pode diferir tanto entre modelos quanto entre regras. Portanto, valores de erro nessas linhas descrevem seus respectivos pontos operacionais e não isolam a superioridade de uma regra a cobertura idêntica.

**Tabela 5. Margem no teste: cobertura efetiva e erro seletivo médios.**

| Meta de validação | BERT: cobertura | BERT: erro aceito | FinBERT: cobertura | FinBERT: erro aceito |
|---|---:|---:|---:|---:|
| 80% | 78,48% | 1,79% | 78,81% | 1,54% |
| 90% | 90,65% | 3,47% | 89,48% | 3,11% |
| 95% | 95,02% | 4,86% | 94,99% | 4,87% |

A AURC média com MSP foi 0,0130 para BERT e 0,0110 para FinBERT; com margem, foi 0,0129 e 0,0109, respectivamente. A proximidade entre as regras sugere diferenças pequenas nessa medida agregada, mas as médias não demonstram equivalência nem superioridade estatística. A AURC de FinBERT foi menor para ambas as regras, embora ela reflita também características do classificador inicial.

### 5.4. Análise de erros

Uma confusão recorrente ocorreu entre `verify_my_identity` e `why_verify_identity`. Considerando as três sementes, houve 27 confusões somadas nas execuções de BERT e 32 nas de FinBERT. Como um mesmo exemplo pode aparecer como erro em várias sementes, essas contagens não representam quantidades de mensagens distintas.

A mensagem “What is the need to verify my identity?” possui o rótulo `why_verify_identity`, mas as seis versões previram `verify_my_identity`. Nas metas de 90%, ambas as regras aceitaram essa previsão equivocada em todas as versões. O caso ilustra que uma regra de abstenção pode reduzir o erro agregado sem identificar todos os erros individuais.

Uma hipótese é que a proximidade lexical e temática entre as intenções dificulte sua distinção; o experimento não testa essa explicação causalmente. Outro par recorrente foi `card_arrival` e `card_delivery_estimate`, relacionado à chegada e ao prazo de entrega de cartões. Os exemplos foram selecionados para inspeção qualitativa e não constituem uma amostra representativa de todas as falhas.

### 5.5. Limitações e reprodutibilidade

Os resultados se restringem ao BANKING77 em inglês e a uma divisão de treino e validação. Não avaliamos mensagens fora das 77 intenções, mudança de distribuição ou um fluxo de atendimento real. Três sementes capturam parte da variação do ajuste, mas não fornecem, por si só, significância estatística. Também não há comparação controlada que isole o efeito causal do pré-treinamento financeiro.

As sete sobreposições tokenizadas entre treino e teste são uma limitação adicional. Não foi medido como sua remoção afetaria o desempenho, e a preservação do teste oficial facilita a referência ao benchmark sem eliminar esse problema. A validação compartilhada para escolha da época, taxa e limiares também pode concentrar escolhas nas particularidades daquela amostra.

Para apoiar a reprodução, o projeto registra configurações, seeds, divisão, revisões, previsões e métricas. Os limiares foram congelados antes do teste, e o recálculo das métricas a partir das previsões salvas reproduziu os arquivos de avaliação. Os pesos treinados permanecem em disco local fora do Git; sua disponibilidade deve ser verificada antes da entrega.

## 6. Conclusão

Este trabalho comparou BERT e FinBERT em classificação de intenções bancárias e avaliou duas regras de abstenção após o treinamento. No BANKING77, os modelos atingiram acurácias médias próximas: 92,61% e 92,40%. FinBERT apresentou ECE e AURC médias menores na avaliação realizada, enquanto BERT apresentou acurácia média ligeiramente maior. Essas diferenças são descritivas e não estabelecem significância estatística ou uma relação causal com o pré-treinamento financeiro.

Nos pontos examinados com MSP, a aceitação de mais mensagens veio acompanhada de maior erro entre as respostas aceitas. As regras reduziram o erro agregado em relação à ausência de abstenção nos pontos reportados, ao custo de deixar parte das mensagens sem classificação aceita. A análise qualitativa mostra, contudo, que previsões incorretas ainda podem ser aceitas.

Trabalhos futuros podem avaliar outras divisões e dados externos, medir o efeito das sobreposições tokenizadas e investigar classes semanticamente próximas. Também seria útil comparar as regras em coberturas comuns e estudar custos concretos de erro e de encaminhamento para revisão. Essas extensões ajudariam a avaliar a generalização do resultado e a adequação de uma política de abstenção a um contexto operacional.

## Declaração de uso de inteligência artificial generativa

Uma ferramenta de inteligência artificial generativa da OpenAI (ChatGPT/Codex) foi utilizada como apoio à organização e revisão do material, à elaboração deste esboço e à pesquisa e desenvolvimento do projeto. **Declaração provisória:** os autores devem conferir e completar as ferramentas, etapas e finalidades efetivamente utilizadas, incluindo eventual auxílio em código e análise. Todo o texto, código, resultados e referências devem ser integralmente revisados e assumidos pelos autores antes da entrega, conforme a especificação da disciplina.

## Referências

Botzer, N., Vazquez, D., Weninger, T. e Laradji, I. (2023). TK-KNN: A Balanced Distance-Based Pseudo Labeling Approach for Semi-Supervised Intent Classification. *Findings of the Association for Computational Linguistics: EMNLP 2023*. https://aclanthology.org/2023.findings-emnlp.429/

Casanueva, I., Temčinas, T., Gerz, D., Henderson, M. e Vulić, I. (2020). Efficient Intent Detection with Dual Sentence Encoders. *Proceedings of the 2nd Workshop on Natural Language Processing for Conversational AI*, p. 38–45. https://aclanthology.org/2020.nlp4convai-1.5/

Cattelan, L. F. e Silva, D. (2024). How to Fix a Broken Confidence Estimator: Evaluating Post-hoc Methods for Selective Classification with Deep Neural Networks. *Proceedings of the Fortieth Conference on Uncertainty in Artificial Intelligence*, PMLR 244, p. 547–584. https://proceedings.mlr.press/v244/cattelan24a.html

Devlin, J., Chang, M.-W., Lee, K. e Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. *Proceedings of NAACL-HLT 2019*, p. 4171–4186. https://aclanthology.org/N19-1423/

Guo, C., Pleiss, G., Sun, Y. e Weinberger, K. Q. (2017). On Calibration of Modern Neural Networks. *Proceedings of the 34th International Conference on Machine Learning*, PMLR 70, p. 1321–1330. https://proceedings.mlr.press/v70/guo17a.html

Huang, P., Huang, J., Xu, Y., Li, W. e Xiao, X. (2024). Logits Reranking via Semantic Labels for Hard Samples in Text Classification. *Findings of the Association for Computational Linguistics: EMNLP 2024*. https://aclanthology.org/2024.findings-emnlp.657/

Peng, B., Chersoni, E., Hsu, Y.-Y. e Huang, C.-R. (2021). Is Domain Adaptation Worth Your Investment? Comparing BERT and FinBERT on Financial Tasks. *Proceedings of the Third Workshop on Economics and Natural Language Processing*, p. 37–44. https://aclanthology.org/2021.econlp-1.5/

Xin, J., Tang, R., Yu, Y. e Lin, J. (2021). The Art of Abstention: Selective Prediction and Error Regularization for Natural Language Processing. *Proceedings of ACL-IJCNLP 2021*, p. 1040–1051. https://aclanthology.org/2021.acl-long.84/

Yang, Y., Uy, M. C. S. e Huang, A. (2020). FinBERT: A Pretrained Language Model for Financial Communications. *arXiv preprint arXiv:2006.08097*. https://arxiv.org/abs/2006.08097
