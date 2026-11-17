# Plano arquitetural e experimental

## Rastreabilidade da pesquisa

As pesquisas e referências são mantidas em [RESEARCH.md](RESEARCH.md), com achados, seções consultadas, limites e pendências. O autor autorizou o registro contínuo das pesquisas. Evidências novas não alteram decisões automaticamente: mudanças neste plano continuam dependendo de confirmação.

## Decisões confirmadas

### D1 — Escopo experimental: BANKING77

- **Decisão:** adotar a opção A: classificação das 77 intenções do BANKING77, com comparação entre BERT e FinBERT.
- **Motivo:** manter coerência entre dados anotados, avaliação e conclusões, com escopo viável para o trabalho.
- **Limite:** os resultados nesse dataset sustentam conclusões sobre suas intenções bancárias; não validam intenções corporativas como fluxo de caixa, estimativas tributárias ou calendário de pagamentos.
- **Motivação apresentada pelo autor:** um agente de produto financeiro precisa interpretar pedidos em linguagem natural para direcionar ferramentas ou respostas. A contribuição principal está definida em D2; a forma de representar esse contexto no experimento ainda será detalhada.

### D2 — Contribuição principal: classificação com abstenção

- **Decisão:** investigar abstenção como contribuição principal da comparação entre BERT e FinBERT.
- **Motivo:** conectar a classificação de intenções à decisão prática de encaminhar um pedido automaticamente ou não, aprofundando a avaliação além do desempenho agregado.
- **Questão orientadora:** como os modelos se comparam na relação entre proporção de pedidos aceitos e erros entre os pedidos aceitos?
- **Limite:** abstenção continua sendo classificação de intenções; esta decisão não inclui question answering, implementação de diálogo ou execução de ferramentas.
- **Situação consolidada:** critérios em D3, separação e proporção dos dados em D4/D18/D19, métricas em D15–D17. Procedimento operacional de seleção dos limiares permanece aberto. Robustez e hierarquia não integram o escopo aprovado.

### D3 — Comparar dois critérios de abstenção separadamente

- **Decisão:** comparar, em cada modelo, uma regra baseada na maior pontuação entre as intenções e outra baseada na diferença entre as duas maiores pontuações. Usar as previsões do mesmo classificador para avaliar cada regra, com referência sem abstenção.
- **Regras:** na primeira, abster quando a maior pontuação ficar abaixo de um limiar; na segunda, quando a diferença entre as duas primeiras ficar abaixo de um limiar.
- **Motivo:** investigar empiricamente os dois sinais sugeridos pelo autor, distinguindo apoio à intenção escolhida de competição entre alternativas, sem acrescentar outra arquitetura de treinamento.
- **Comparação:** examinar erros entre pedidos aceitos em níveis comparáveis de cobertura (proporção de pedidos aceitos). Objetivo e metas confirmados em D37–D38; detalhes operacionais propostos em O6 aguardam aprovação final.
- **Escopo:** avaliar os critérios separadamente. Sua combinação não integra o experimento principal aprovado e não precisa ser acrescentada para concluir o plano.
- **Cuidado conceitual:** as pontuações não garantem probabilidades reais de acerto; ambos os sinais derivam da mesma distribuição de saída.

### D4 — Separação entre treino, validação e teste

- **Decisão:** preservar a divisão oficial de treino/teste do BANKING77 e separar do treino uma validação estratificada por intenção, com proporção definida em D19.
- **Responsabilidades:** treino ajusta os pesos; validação orienta a seleção do modelo e dos limiares; teste avalia o procedimento final após congelar essas escolhas.
- **Motivo:** preservar aproximadamente a distribuição das intenções na divisão de treino/validação e evitar adaptar escolhas aos resultados do teste final.
- **Limite:** estratificação preserva proporções entre classes, não exige conjuntos do mesmo tamanho. O teste oficial será preservado, sem redistribuí-lo para equilibrar classes.
- **Situação consolidada:** divisão oficial e proporção documentadas em D19; faltam índices, semente e política de tratamento de problemas de dados. Arquivos concretos ainda não foram auditados.

### D5 — Fundamentação bibliográfica e revisão final das decisões

- **Decisão:** realizar agora uma revisão curta dos protocolos de validação em trabalhos sobre BANKING77 com Transformers e classificação com abstenção, antes de escolher a proporção de validação.
- **Decisão:** após completar a sequência de decisões do plano, realizar uma segunda iteração para revisar o embasamento de todas as decisões arquiteturais e experimentais e buscar referências acadêmicas pertinentes.
- **Motivo:** toda escolha deve ter uma razão explícita; recomendações heurísticas não devem ser apresentadas como conclusões sustentadas pela literatura.
- **Resultado esperado:** para cada decisão, explicitar justificativa, referências aplicáveis, limites da evidência e eventuais lacunas. Distinguir fundamentação publicada de escolhas práticas ou hipóteses que precisam de verificação experimental.
- **Revisões:** alterações de decisões resultantes dessa auditoria dependem de nova confirmação do autor antes de atualizar este plano.
- **Situação atual:** proporção de aproximadamente 10% confirmada em D19 após revisão bibliográfica. A sugestão anterior de 20% foi superada e não integra o protocolo.

### D6 — Comparar erro em vários níveis de cobertura antes de escolher limiares definitivos

- **Decisão:** avaliar os dois critérios de D3 em vários níveis de cobertura, incluindo a referência sem abstenção, e apresentar a relação entre erro e cobertura em tabela e curva.
- **Medidas:** cobertura é a proporção de pedidos aceitos; erro seletivo é a proporção de classificações incorretas entre os pedidos aceitos. Comparar os critérios em níveis equivalentes de cobertura.
- **Motivo:** investigar qual sinal identifica melhor as previsões arriscadas e explicitar o custo da redução de erros em termos de pedidos recusados, evitando iniciar a análise com um limiar arbitrário.
- **Etapas:** estudar o comportamento dos critérios; depois escolher limiares operacionais usando a validação, conforme D4, e avaliar as regras congeladas no teste. Curvas descritivas de teste não autorizam ajustar limiares a partir dele.
- **Fundamentação:** RESEARCH.md, R2, R6 e R8 documentam precedentes para seleção pós-treinamento e avaliação por erro versus cobertura; seus resultados não garantem melhoria no BANKING77.
- **Limites:** os critérios são aplicados após o treinamento e não alteram os pesos ou a acurácia do modelo sobre todos os exemplos. Redução de erro entre os aceitos é uma hipótese a avaliar, não uma garantia de segurança.
- **Atualização:** coberturas confirmadas em D38 e objetivo em D37. Empates e seleção operacional detalhados na proposta O6; percentuais anteriores a D38 eram ilustrativos.

### D7 — Recursos e diagnóstico antes dos treinamentos completos

- **Decisão:** usar o notebook próprio como ambiente principal e Colab como alternativa caso haja limitações de memória ou tempo.
- **Recursos informados pelo autor:** ROG Zephyrus M16, RTX 3070 Ti e processador i9. VRAM disponível e ambiente de execução ainda não foram verificados. Servidor em nuvem não está disponível atualmente e não integra o plano principal.
- **Prazo informado:** aproximadamente uma semana para experimentos, dentro de cerca de uma semana e meia até a entrega do artigo; estimativa do autor, não orçamento integral obrigatório para treinamento.
- **Decisão:** prever uma execução curta de diagnóstico antes dos treinamentos completos, para verificar funcionamento, consumo de memória e estimar duração, sem usar resultados do teste para escolher configurações.
- **Motivo:** reduzir tentativas caras e dimensionar um experimento compacto conforme recursos e prazo reais.
- **Reaproveitamento:** salvar previsões dos modelos treinados para avaliar os dois critérios, coberturas e limiares sem retreinar a cada alteração da regra de abstenção.
- **Situação consolidada:** modelos em D12; orçamento e repetições em D22; taxas em D23; duração planejada em D24; batch por diagnóstico em D27. A viabilidade será medida antes das execuções completas. Nesta etapa, apenas o planejamento está autorizado; a execução ocorrerá após aprovação do desenho e autorização de implementação.

### D8 — Pergunta principal e pergunta adicional

- **Decisão:** manter como comparação principal a investigação de BERT genérico versus FinBERT na classificação das 77 intenções do BANKING77: a especialização financeira está associada a melhor desempenho nessa tarefa?
- **Pergunta adicional:** para cada modelo, qual dos dois critérios de abstenção de D3 permite reduzir mais os erros entre os pedidos aceitos em níveis equivalentes de cobertura?
- **Motivo:** aprofundar a análise da comparação original por meio das mesmas previsões, mantendo o experimento compacto e alinhado à proposta.
- **Limite:** investigar limiares e cobertura não implica buscar um limiar universal ideal. A comparação dos checkpoints não demonstrará, isoladamente, causalidade do domínio de pré-treinamento caso existam outras diferenças entre eles.
- **Situação consolidada:** checkpoints selecionados em D12, com diferenças e limites documentados. Faltam revisões exatas dos arquivos e verificação operacional; seleção dos nomes dos modelos não está mais aberta.

### D9 — Limites da comparação e consulta ao professor

- **Orientação confirmada pelo autor:** aceitar, neste momento, a comparação de modelos disponíveis com documentação explícita das diferenças de pré-treinamento e de seus limites de interpretação, mantendo a busca por alternativas mais comparáveis.
- **Motivo:** preservar viabilidade sem atribuir automaticamente ao domínio financeiro diferenças que também podem decorrer de outros fatores do histórico dos modelos.
- **Limite:** essa orientação não escolhe um checkpoint específico, não garante equivalência entre modelos e não autoriza trocar dataset ou domínio, adicionar modelos ou executar pré-treinamento próprio.
- **Acompanhamento:** manter dúvidas em [QUESTIONS_FOR_PROFESSOR.md](QUESTIONS_FOR_PROFESSOR.md) para a conversa que o autor pretende ter com o professor. Registrar respostas posteriormente; mudanças de desenho exigem confirmação.
- **Pesquisa autorizada:** investigar alternativas com histórico mais comparável e registrar evidências e limitações em RESEARCH.md antes de propor substituições.

### D10 — Comparação empírica de checkpoints com execução controlada

- **Decisão:** comparar checkpoints disponíveis de BERT e FinBERT, buscando uma execução justa e documentando os fatores controlados e as limitações que permanecem.
- **Objetivo:** identificar qual checkpoint apresenta melhor desempenho na classificação e como se comporta com os critérios de abstenção, sob o protocolo definido para BANKING77. Esta decisão operacionaliza D8 e consolida a orientação de D9.
- **Motivo:** a comparação responde à pergunta prática do trabalho e é viável no prazo; investigar isoladamente todas as causas das diferenças de pré-treinamento exigiria outro desenho experimental.
- **Controle pretendido:** manter dados e avaliação comuns e estabelecer oportunidades comparáveis de ajuste dos modelos. Orçamento e taxas definidos em D22–D23; agregação confirmada em D39; complementos operacionais propostos em O5. Justiça não implica impor automaticamente valores idênticos de hiperparâmetros finais.
- **Interpretação:** diferenças observadas serão atribuídas aos checkpoints e ao protocolo completos, sem afirmar que foram causadas exclusivamente pelo domínio financeiro ou identificar causalmente diferenças específicas dos pesos.
- **Ressalva:** controles e ablações podem isolar fatores específicos. A limitação deste estudo não implica que controle causal seja impossível na pesquisa em geral.
- **Fundamentação:** RESEARCH.md, R10–R12: comparação de variantes financeiras, controles de adaptação de domínio e influência do orçamento de ajuste.
- **Escopo:** não acrescentar treinamento próprio de linguagem ou controles adicionais de pré-treinamento sem nova decisão. Checkpoints selecionados em D12 e repetições em D22; os detalhes ainda abertos estão reunidos na seção Próximo Passo.

### D11 — Isolar a regra de abstenção com classificador fixo

- **Decisão:** destacar como parte central controlada do estudo a comparação dos dois critérios de D3 sobre exatamente as mesmas previsões de um classificador treinado.
- **Controle:** para cada checkpoint e execução, preservar pesos, exemplos, rótulos e pontuações; variar apenas o critério de seleção. Comparar erro entre pedidos aceitos em coberturas equivalentes, conforme D6.
- **Motivo:** identificar diferenças decorrentes da seleção feita pelas regras sem confundi-las com mudanças no treinamento, nos dados ou nos pesos. Essa análise reutiliza previsões e não exige treinamentos adicionais por regra.
- **Aplicação:** realizar a comparação dentro de cada modelo. A comparação entre BERT e FinBERT continua sujeita às limitações de D10.
- **Interpretação:** diferenças de erro nessa comparação descrevem o efeito das regras sobre aquele conjunto de previsões; generalização para outros exemplos, checkpoints e execuções precisa ser avaliada, não presumida.
- **Fundamentação:** RESEARCH.md, R8: comparação de estimadores de confiança em classificadores fixos.
- **Situação consolidada:** três repetições por configuração em D22; coberturas confirmadas em D38; tratamento de empates proposto em O6–O7. Não confundir esses empates com o desempate entre checkpoints de D21.

### D12 — Checkpoints selecionados

- **Decisão:** comparar `google-bert/bert-base-uncased` e `yiyanghkust/finbert-pretrain` no BANKING77.
- **Motivo:** preservar a comparação entre modelo genérico e financeiro com estruturas de porte semelhante, usando o checkpoint financeiro indicado no repositório dos autores. A procedência documental mais direta foi preferida à cópia comunitária BaseVocab examinada.
- **Comparabilidade verificada:** configurações com 12 camadas, dimensão interna 768 e 12 cabeças de atenção. Vocabulários diferentes: 30.522 e 30.873 tokens, respectivamente; cada modelo deverá usar seu próprio tokenizer.
- **Limites:** aceitar e documentar diferenças de vocabulário e histórico de pré-treinamento, conforme D10. Textos financeiros de pré-treinamento não equivalem às mensagens bancárias do BANKING77; melhoria é hipótese experimental.
- **Adaptação de tarefa:** ambos precisarão de uma saída para 77 intenções; regime completo confirmado em D13. Demais detalhes do fine-tuning ainda serão decididos.
- **Verificação operacional:** configuração e documentação foram consultadas; carregamento dos pesos e consumo de memória serão verificados no diagnóstico de D7. A ausência de Transformers no ambiente inspecionado não é evidência de incompatibilidade do modelo.
- **Rastreabilidade:** RESEARCH.md, R9 e R13. Revisões exatas dos dois repositórios ainda serão fixadas para reprodução. Downloads acima de 50 MB exigem aviso prévio, conforme AGENTS.md.

### D13 — Fine-tuning completo nos dois modelos

- **Decisão:** ajustar os pesos do encoder e da nova saída de classificação em ambos os checkpoints, usando exemplos anotados de intenções. Não adicionar um regime de encoder congelado ao experimento principal.
- **Motivo:** avaliar os checkpoints após adaptação supervisionada às 77 intenções, alinhando o experimento à proposta original e ao precedente direto encontrado no BANKING77.
- **Controle preservado:** salvar os modelos derivados sem sobrescrever os checkpoints de origem; após selecionar a versão treinada, fixar pesos e previsões para comparar as regras de abstenção conforme D11. Os limiares não participam do backpropagation.
- **Fundamentação:** RESEARCH.md, R14–R16. Casanueva et al. (2020), §4 e tabela 3, reportam BERT-FIXED 87,19% versus BERT-TUNED 93,66% no BANKING77 completo.
- **Limite da referência:** o artigo usa BERT-large cased e configurações de pooling/cabeça diferentes. Seus resultados fundamentam a escolha e podem contextualizar a discussão posterior; não demonstram que nosso ajuste superou congelamento, pois não realizaremos essa comparação, nem antecipam nossos resultados de BERT-base/FinBERT.
- **Viabilidade:** consumo de memória e duração serão verificados no diagnóstico de D7. Taxas em D23, épocas em D24, AdamW/decay em D25, scheduler em D26 e repetições em D22 já confirmados. Batch final será escolhido pelo procedimento de D27.

### D14 — Representação CLS e classificador linear multiclasse

- **Decisão:** usar uma representação baseada em CLS como entrada de uma camada linear de 77 classes em ambos os modelos. Produzir logits e obter probabilidades estimadas por softmax; treinar com entropia cruzada multiclasse.
- **Dimensões:** representação de 768 valores; saída com 77 logits, um por intenção. Uma camada linear com viés possui 59.213 parâmetros (768 × 77 + 77).
- **Motivo:** adotar uma saída simples, com precedente acadêmico direto, mantendo a mesma forma de classificação nos dois modelos sem acrescentar outra arquitetura à comparação.
- **Treinamento:** encoder e saída são ajustados conjuntamente conforme D13. A implementação da entropia cruzada deverá receber logits, evitando aplicar softmax duas vezes; probabilidades serão usadas na previsão e nas regras de abstenção.
- **Interpretação:** pesos da cabeça pontuam cada classe por combinação linear da representação; não é busca de intenção mais próxima por cosseno. Softmax não garante calibração.
- **Fundamentação:** RESEARCH.md, R17 (Devlin et al., 2019, §3.2 e §4.1), e R15 (BERT-TUNED no BANKING77). Explicação técnica em LEARNING_NOTES.md.
- **Limites e pendências:** não demonstramos superioridade sobre outras cabeças. Representação transformada pelo pooler confirmada em D32; dropout confirmado em D33. Não tratar CLS direto e pooler como idênticos. Alternativas de R18 não integram o experimento.

### D15 — Métricas de classificação sem abstenção

- **Decisão:** comparar acurácia e Macro-F1 nas previsões sem abstenção; usar precisão, recall e F1 por intenção e análise das principais confusões para diagnóstico.
- **Motivo:** acurácia mede acerto global; Macro-F1 combina precisão e recall dando o mesmo peso a cada intenção. Diagnóstico por classe revela falhas ocultas pelas médias.
- **Fundamentação acadêmica:** Casanueva et al. (2020) usam acurácia no BANKING77 (RESEARCH.md, R15); Peng et al. (2021) reportam Macro-F1 e Micro-F1 em comparações BERT/FinBERT em tarefas financeiras (R10). Definições e agregações verificadas na documentação do scikit-learn (R19).
- **Métricas não priorizadas:** Micro-F1 equivale à acurácia na classificação de rótulo único incluindo todas as classes; não tratá-lo como evidência independente. ROUGE avalia sobreposição textual, não o acerto dos rótulos de intenções (R19).
- **Abstenção:** cobertura e erro entre os aceitos permanecem conforme D6. Não substituir essas medidas pela acurácia calculada somente nos aceitos, omitindo a cobertura.
- **Limites:** Macro-F1 não incorpora automaticamente custos distintos de encaminhamento e não substitui inspeção por intenção. Seleção pela validação definida em D20–D21; política de divisões por zero e detalhes da análise de confusões ainda abertos. Novas métricas não entram no plano sem confirmação.

### D16 — AURC como resumo da avaliação de abstenção

- **Decisão:** reportar AURC (área sob a curva de erro seletivo versus cobertura), acompanhando as curvas e tabelas de D6. Menor área indica menor erro seletivo agregado ao longo das coberturas avaliadas.
- **Motivo:** sintetizar o comportamento de cada critério em vários níveis de aceitação, sem depender apenas de um limiar isolado. Reutiliza as mesmas previsões; não requer treinamento adicional.
- **Fundamentação:** Xin et al. (2021), [The Art of Abstention](https://aclanthology.org/2021.acl-long.84.pdf), §3.1, usa área sob curva risco-cobertura em classificação NLP; Kamath et al. (2020), [Selective Question Answering under Domain Shift](https://aclanthology.org/2020.acl-main.503.pdf), §3.1, usa essa área em outra tarefa de NLP com abstenção. RESEARCH.md, R20 documenta pertinência e limites.
- **Interpretação:** dentro de um classificador fixo, comparar seleção feita pelos critérios; entre checkpoints, reconhecer que a área também reflete a qualidade inicial da classificação. Cattelan e Silva (2024), [§4.2](https://arxiv.org/html/2305.15508v4), discute essa dependência (RESEARCH.md, R8). Não confundir AURC com AUROC nem substituir curvas por um único número.
- **Pendências:** fixar convenção discreta de cálculo, escala, tratamento de empates e cobertura zero antes de implementar. ECE foi aprovado como diagnóstico secundário em D17; RPP não integra o escopo aprovado.

### D17 — ECE como diagnóstico secundário

- **Decisão:** incluir Expected Calibration Error (ECE) em segundo plano, como diagnóstico complementar das probabilidades dos dois modelos; preservar classificação e abstenção como foco principal.
- **Motivo:** investigar se a confiança declarada corresponde à frequência observada de acertos, complementando a avaliação de seleção por confiança feita pelas curvas e AURC.
- **Aplicação:** usar a probabilidade da classe prevista e o indicador de acerto, reaproveitando as previsões salvas. Não interpretar a margem entre probabilidades como probabilidade de acerto para esse cálculo.
- **Escopo:** medir calibração; não acrescentar temperature scaling, outra técnica corretiva, novo modelo ou treinamento adicional. Gráfico de confiabilidade e detalhes de apresentação ainda serão definidos.
- **Fundamentação:** Guo et al. (2017), [On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a/guo17a.pdf), descreve ECE como agregação das diferenças entre confiança e acurácia por faixas; RESEARCH.md, R20.
- **Limites:** ECE depende do agrupamento e da amostra; não garante segurança nem substitui métricas de abstenção. Número e tipo de faixas e conjunto avaliado ainda serão fixados. RPP permanece fora do escopo aprovado.

### D18 — Validação compartilhada para selecionar modelo e limiares

- **Decisão:** usar o mesmo conjunto de validação para selecionar a versão treinada de cada modelo e escolher seus limiares de abstenção. Preservar o teste exclusivamente para avaliação final após congelar essas escolhas.
- **Motivo:** aproveitar os exemplos disponíveis sem fragmentar a validação em conjuntos menores, mantendo o protocolo viável no escopo e prazo definidos.
- **Compromisso:** a reutilização pode adaptar escolhas excessivamente à validação. Planejar busca limitada e documentada; limites concretos ainda serão definidos. O teste independente avalia generalização, mas não elimina esse risco nem confere garantia estatística de erro.
- **Escopo:** não acrescentar subconjunto separado de calibração ou método de certificação de risco. Proporção confirmada em D19; procedimento exato de seleção continua aberto.
- **Fundamentação e limites:** R3 registra uso de validação para seleção em BANKING77; R5 documenta alternativa com calibração separada, e R12 fundamenta transparência do orçamento de busca. Nenhuma dessas referências demonstra superioridade da validação compartilhada neste experimento; esta é uma escolha prática explicitada pelo autor.

### D19 — Aproximadamente 10% do treino oficial para validação

- **Decisão:** reservar aproximadamente 10% dos 10.003 exemplos do treino oficial do BANKING77 como validação estratificada por intenção, compartilhada conforme D18. Manter os 3.080 exemplos do teste oficial para avaliação final.
- **Tamanhos esperados:** aproximadamente 9.000 exemplos para ajustar pesos e 1.000 para validação. Contagem exata dependerá do arredondamento e da verificação de dados; não redistribuir exemplos do teste para atingir proporções.
- **Motivo:** seguir precedentes publicados no próprio dataset e evitar fragmentar uma amostra de validação já limitada entre seleção de modelo e ajuste de limiares.
- **Fundamentação:** Botzer et al. (2023), [TK-KNN, §4.1 e tabela 1](https://aclanthology.org/2023.findings-emnlp.429.pdf), usam 9.002 treino, 1.001 validação e 3.080 teste. Gulati et al. (2024), [Soft Clustering, apêndice B](https://aclanthology.org/2024.findings-emnlp.758.pdf), dividem o treino oficial em 90/10. RESEARCH.md, R3, R4 e R22.
- **Limites da evidência:** são precedentes de tamanho, não prova de proporção ótima ou da suficiência dessa validação para nossos limiares. Acurácia global, erros raros, resultados por intenção e baixas coberturas têm precisões diferentes. Busca de configurações deverá ser limitada e documentada; não prometer garantia estatística de erro.
- **Pendências:** semente e índices reproduzíveis da divisão, diagnóstico de duplicatas/conflitos e regras de seleção dos modelos e limiares ainda serão definidos. Mudanças motivadas por esse diagnóstico exigem confirmação se alterarem o desenho aprovado.

### D20 — Selecionar versão treinada pela acurácia de validação

- **Decisão revisada e confirmada:** selecionar a versão treinada de cada modelo pela maior acurácia no conjunto de validação, calculada sem abstenção. Substitui a escolha inicial de Macro-F1 após a comparação crítica documentada em RESEARCH.md, R24. Macro-F1 continua no reporte e diagnóstico conforme D15.
- **Motivo:** maximizar a proporção de intenções corretas com custo unitário por erro, alinhando seleção à comparação prática de encaminhamentos e à definição de erro seletivo. Estabelecer a regra antes dos resultados evita alternar retrospectivamente entre métricas.
- **Fundamentação:** Casanueva et al. (2020), [BANKING77, tabela 3](https://aclanthology.org/2020.nlp4convai-1.5.pdf), usam acurácia para avaliação; Loukas et al. (2023), [nota 1 e tabela 4](https://stogiannidis.github.io/files/LLMPenny.pdf), confirmam teste balanceado e reportam Micro-F1/Macro-F1; Opitz (2024), [§4.1 e §4.4](https://aclanthology.org/2024.tacl-1.46.pdf), analisa propriedades e necessidade de justificar a escolha. Essas fontes sustentam a adequação do critério, sem provar que selecionar por acurácia supera selecionar por Macro-F1 neste projeto.
- **Etapas:** escolher a versão com esse critério; fixá-la para comparar regras e selecionar limiares conforme D18. Macro-F1, AURC e ECE não escolhem a versão; Macro-F1 permanece no reporte. Teste permanece fora da seleção.
- **Limites:** acurácia maior não garante Macro-F1 maior ou AURC menor. Balanceamento do teste não implica validação perfeitamente balanceada. Avaliação por época e ausência inicial de early stopping confirmadas em D24; orçamento em D22. Não importar outros detalhes dos artigos automaticamente.

### D21 — Desempate na seleção de versões

- **Decisão revisada:** escolher a maior acurácia de validação; em empate exato, manter a versão salva mais antiga na mesma execução. O autor aceitou a troca condicionada a precedente em estudo; a busca posterior encontrou esse precedente, com os limites abaixo.
- **Motivo:** resolver empates de forma explícita e determinística, com o comportamento da classe Trainer consultada, simplificando a implementação. Macro-F1 continua sendo reportado e não desempata épocas.
- **Fundamento e limite:** Zhang e Virtanen (2026), [§4](https://arxiv.org/html/2610.35329v1), usam maior acurácia macro e, em empate, checkpoint mais antigo em classificação de áudio; é precedente de uso, não comparação que prove superioridade do desempate neste projeto. RESEARCH.md, R50–R51. Pode selecionar uma época diferente da regra anterior, que priorizava Macro-F1 em empate.
- **Precisão:** comparar contagem de acertos e métricas não arredondadas; não definir empates pelos percentuais exibidos na tela.
- **Limite:** esta regra não seleciona a melhor seed para omitir outras repetições. Agregação confirmada em D39; desempate entre configurações proposto em O5.

### D22 — Orçamento inicial: duas configurações e três repetições por modelo

- **Decisão:** planejar duas configurações por checkpoint e três repetições com sementes aleatórias distintas para cada configuração: 2 modelos × 2 configurações × 3 repetições = 12 treinamentos completos planejados.
- **Condição:** verificar duração e memória no diagnóstico de D7 antes de iniciar as execuções completas. Se inviável, revisar o orçamento com o autor antes de alterá-lo. Diagnóstico não está incluído nas 12 execuções científicas.
- **Motivo:** limitar busca e custo e observar variação entre treinamentos, oferecendo aos dois modelos o mesmo número planejado de configurações e repetições. Regras de abstenção reutilizam as previsões.
- **Fundamentação:** Yin et al. (2021), [BatchMixup, tabela 1](https://aclanthology.org/2021.findings-acl.434.pdf), reporta médias de três seeds no BANKING77; Botzer et al. (2023), [TK-KNN, §4.1](https://aclanthology.org/2023.findings-emnlp.429.pdf), usa cinco. RESEARCH.md, R25, compara esses precedentes; R12 fundamenta explicitar orçamento de busca.
- **Limites:** três repetições são compromisso prático com precedente, não garantia de estabilidade ou significância. Duas configurações constituem busca restrita escolhida pelo custo, não número ótimo estabelecido por artigo. Não omitir execuções desfavoráveis ou selecionar apenas a seed vencedora.
- **Pendências:** taxas das duas configurações já definidas em D23; agregação/reporte confirmados em D39; valores de seeds e detalhes complementares propostos em O1/O5. Seleção da versão em cada execução segue D20–D21.

### D23 — Configurações variando a taxa de aprendizado

- **Decisão:** testar taxas de aprendizado de referência `2e-5` e `5e-5` em ambos os modelos, com três repetições por taxa conforme D22. Manter os demais hiperparâmetros iguais entre as configurações A e B, a definir.
- **Motivo:** permitir ajuste limitado de cada checkpoint dentro do mesmo orçamento, variando um hiperparâmetro com precedente direto no fine-tuning de BERT.
- **Fundamentação:** Devlin et al. (2019), [§4.1 e apêndice A.3](https://aclanthology.org/N19-1423.pdf), exploram taxas que incluem os dois valores; Liu e Wang (2021), [tabela 1 e §5.1](https://aclanthology.org/2021.acl-long.178.pdf), investigam espaços de busca incluindo taxa de aprendizado e sua restrição. RESEARCH.md, R26.
- **Limites:** dois pontos são uma busca restrita pelo custo, não garantia de taxa ótima no BANKING77/FinBERT. Otimizador, duração e scheduler definidos em D24–D26; batch final depende de D27. As taxas são picos do scheduler, não valores constantes durante todo o treino.
- **Seleção:** checkpoints de cada execução seguem D20–D21. Escolha da configuração pela média das três validações confirmada em D39; não escolher taxa pelo teste ou apenas pela seed mais favorável.

### D24 — Cinco épocas, avaliação por época e melhor checkpoint

- **Decisão:** planejar cinco épocas por treinamento completo, sem early stopping inicialmente; avaliar na validação ao final de cada época e reter a melhor versão conforme D20–D21. Não usar automaticamente a versão da última época.
- **Motivo:** orçamento de duração explícito e comum entre configurações, com oportunidade de selecionar uma versão anterior caso o desempenho se degrade.
- **Fundamentação:** Casanueva et al. (2020), [§4](https://aclanthology.org/2020.nlp4convai-1.5.pdf), usa cinco épocas em BERT-TUNED no regime de treino completo do BANKING77; Devlin et al. (2019), [apêndice A.3](https://aclanthology.org/N19-1423.pdf), explora 2–4 épocas e ressalta dependência da tarefa. RESEARCH.md, R27, separa precedente da escolha operacional de avaliar por época.
- **Condição:** duração e memória devem passar pelo diagnóstico de D7 antes das 12 execuções de D22. Ajustes de orçamento exigem nova confirmação.
- **Custo a verificar:** o autor considera duas horas adicionais um custo relevante. Comparar no diagnóstico as projeções de três e cinco épocas para as 12 execuções, incluindo avaliação e custos fixos. Mantidas as demais condições, cinco épocas envolvem aproximadamente 67% mais passos de treino que três, mas não necessariamente 67% mais tempo total. A diferença de duas horas discutida foi um exemplo hipotético, não uma medição ou limite rígido aprovado. Cinco épocas permanecem planejadas; eventual redução para três depende da projeção e de confirmação do autor.
- **Limites:** referência BANKING77 usa modelo e taxa diferentes, e nosso treino reserva validação. Cinco épocas não garantem convergência ou ausência de overfitting. Melhor checkpoint no limite com validação crescente será limitação a documentar, sem extensão automática ou uso do teste para decidir.

### D25 — AdamW e weight decay de 0,01

- **Decisão:** usar AdamW com coeficiente de weight decay `0,01` nos dois modelos, fixo entre as configurações; variar as taxas conforme D23.
- **Motivo:** adotar otimização e regularização com precedentes publicados, mantendo o esforço experimental na comparação dos checkpoints e critérios de abstenção.
- **Fundamentação:** Loshchilov e Hutter (2019), [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101), fundamenta AdamW; Botzer et al. (2023), [TK-KNN, §4.3](https://aclanthology.org/2023.findings-emnlp.429.pdf), usa AdamW com BERT-base em intenções, incluindo BANKING77. Devlin et al. (2019), [apêndices A.2–A.3](https://aclanthology.org/N19-1423.pdf), oferece precedente para coeficiente 0,01. RESEARCH.md, R28.
- **Limites:** precedente não demonstra que o coeficiente seja ótimo nem garante ausência de overfitting. Em AdamW, weight decay é desacoplado da atualização adaptativa; não equivale automaticamente a penalização L2 em Adam. `0,01` não significa reduzir diretamente cada peso em 1% por passo.
- **Pendências:** parâmetros beta/epsilon e grupos de pesos sujeitos ao decay (incluindo política para bias/LayerNorm) ainda serão explicitados. Scheduler e warmup já confirmados em D26.

### D26 — Warmup de 10% e decaimento linear

- **Decisão:** usar warmup linear nos primeiros 10% dos passos de atualização, seguido por redução linear até zero no restante do treinamento. Aplicar a mesma regra aos dois modelos e taxas.
- **Taxas:** `2e-5` e `5e-5` de D23 passam a ser explicitamente os valores de pico, não taxas constantes durante todas as épocas.
- **Motivo:** começar com atualizações menores e reduzir sua escala ao final, adotando um esquema com precedente de classificação BERT sem acrescentar configurações à busca.
- **Fundamentação:** código oficial de BERT, [run_classifier.py](https://github.com/google-research/bert/blob/master/run_classifier.py), define warmup_proportion=0,1; [optimization.py](https://github.com/google-research/bert/blob/master/optimization.py) implementa aquecimento e redução lineares. RESEARCH.md, R29, registra diferenças para implementação moderna.
- **Limites:** não é garantia de estabilidade nem reprodução numérica exata do código histórico. Definir total de passos e arredondamento após fixar batch size/acumulação. Se a duração de D24 for revisada, recalcular scheduler antes das execuções, reconhecendo que muda a trajetória das taxas.

### D27 — Escolher batch size no diagnóstico de hardware

- **Decisão:** comparar batches 8, 16 e 32 no diagnóstico de D7, após definir comprimento de sequência e precisão numérica. Medir memória máxima e exemplos por segundo nos dois modelos, incluindo forward, backward e atualização AdamW.
- **Motivo:** GPU e VRAM nominal não determinam um batch ideal; capacidade e velocidade dependem da configuração completa. Evitar fixar batch 16 por suposição.
- **Critério técnico:** buscar um batch comum aos dois modelos que caiba com margem de memória e tenha bom throughput. Limite quantitativo de margem, amostra e duração da medição ainda serão especificados antes de executar o diagnóstico.
- **Limites:** essa seleção é técnica, não busca por melhor acurácia. Não usar o teste nem resultados de qualidade para escolher batch nesse procedimento. Fixar a configuração antes dos 12 treinamentos científicos; ajustar contagem de passos e scheduler de D26.
- **Fundamentação:** RESEARCH.md, R30, com especificações ASUS e documentação oficial de memória e eficiência de treinamento. Não há benchmark verificado do nosso par no notebook.

### D28 — Medir antes de escolher entre 64 e 128 tokens

- **Decisão:** considerar limites de 64 e 128 tokens e escolher após medir, nos dados de desenvolvimento, os comprimentos e cortes com o tokenizer próprio de cada modelo. Integrar essa escolha ao diagnóstico de hardware, junto ao batch size e às projeções de duração por número de épocas.
- **Motivo:** avaliar a informação removida pelo truncamento junto ao consumo de memória e tempo, antes de fixar a entrada dos treinamentos científicos. Não usar o teste para escolher o limite.
- **Limites:** nenhum dos dois valores está escolhido. Padding dinâmico confirmado em D29; diagnóstico em D30 e critério de preservação integral confirmado em D31. Não escolher um lado de corte que remova conteúdo do desenvolvimento para contornar esse critério. Esta decisão não autoriza execução nem amplia as configurações científicas de D22.
- **Fundamentação verificada:** RESEARCH.md, R31. Botzer et al. (2023), [TK-KNN, §4.3](https://aclanthology.org/2023.findings-emnlp.429.pdf), usam 64 tokens com BERT-base em experimentos incluindo BANKING77, em regime semissupervisionado. Devlin et al. (2019), [BERT, A.2](https://aclanthology.org/N19-1423.pdf), usam 128 em 90% dos passos de pré-treinamento; o [código oficial de classificação](https://raw.githubusercontent.com/google-research/bert/master/run_classifier.py) também define 128 como padrão. Yehudai e Bandel (2024), [FastFit, §4.3](https://aclanthology.org/2024.naacl-demo.18.pdf), usam 128 em avaliação few-shot incluindo BANKING77. São precedentes dos candidatos, não prova de optimalidade, equivalência ou ausência de cortes com nossos tokenizers. A escolha por medição permanece conforme a decisão confirmada.

### D29 — Padding dinâmico nos dois modelos

- **Decisão:** preencher cada lote até o comprimento da maior sequência daquele lote, após aplicar o limite de entrada escolhido conforme D28. Aplicar a mesma política aos dois modelos, usando o marcador de padding do tokenizer correspondente e máscara de atenção para distinguir conteúdo de preenchimento.
- **Motivo:** evitar preenchimento desnecessário sem remover texto adicional. O limite de truncamento permanece uma escolha separada entre 64 e 128 tokens, condicionada à medição.
- **Fundamentação:** RESEARCH.md, R32. A documentação oficial [Padding and truncation](https://huggingface.co/docs/transformers/v4.57.1/en/pad_truncation) apresenta preenchimento até a maior sequência do lote como abordagem geralmente adequada; [DataCollatorWithPadding](https://huggingface.co/docs/transformers/en/main_classes/data_collator) documenta o mecanismo. Trata-se de orientação técnica de eficiência, não demonstração de melhoria de acurácia no BANKING77.
- **Limites:** medir memória e tempo no diagnóstico; menos posições de preenchimento não garantem redução proporcional desses custos. Padding à direita confirmado em D34; política de truncamento permanece pendente. Não adicionar arredondamento para múltiplos ou outras otimizações sem confirmação. Nenhuma execução ou implementação autorizada.

### D30 — Estatísticas de entrada antes da GPU e lado do corte após inspeção

- **Decisão:** aproveitar as estatísticas publicadas do BANKING77 como referência inicial e, antes das medições de GPU, planejar a contagem de tokens dos dados de desenvolvimento com cada tokenizer de D12, sem truncamento e incluindo marcadores especiais. Registrar comprimento máximo e quantidade/proporção de mensagens acima de 64 e 128 tokens.
- **Decisão:** condicionar a escolha do lado do truncamento à inspeção das mensagens de desenvolvimento que excederem os limites candidatos. Examinar o conteúdo que seria removido antes de confirmar qual trecho preservar; não adotar automaticamente o lado usado pelo código BERT nem adicionar treinamentos para comparar políticas.
- **Atualização confirmada em D31:** priorizar preservação integral, em vez de aceitar cortes após inspeção. A inspeção pode explicar excedentes, mas não autoriza descartá-los ou cortar seu conteúdo para escolher um candidato. Se 128 não preservar tudo no desenvolvimento, revisar com o autor antes de prosseguir.
- **Referência inicial:** RESEARCH.md, R34. A ficha do dataset informa média de 59,5 caracteres por mensagem no treino; Loukas et al. (2023), tabela 2, reportam média de 11,9 palavras. O visualizador consultado exibe faixa de 13–433 caracteres no treino, ainda não reproduzida como mínimo/máximo da revisão que será usada. Essas unidades não equivalem a tokens e não substituem a contagem com os dois tokenizers.
- **Uso nas outras decisões:** usar o diagnóstico de entrada para orientar a escolha de 64/128 e dimensionar as medições de batch, memória e velocidade. Usar o custo efetivamente medido para projetar duração de três/cinco épocas e das 12 execuções conforme D7/D24/D27, preservando os critérios e confirmações exigidos. Estatísticas de caracteres ou tokens, isoladamente, não determinam batch, precisão numérica ou número de épocas.
- **Fundamentação do corte:** RESEARCH.md, R33. Nos trabalhos próximos consultados, os limites de comprimento não estabelecem um lado superior no BANKING77; comparações de início/final/ambos em documentos longos têm transferência limitada.
- **Limites:** contagem de tokens e inspeção de cortes não exigem treinamento. Se não houver excedentes no desenvolvimento com o limite escolhido, o lado não altera essas entradas observadas; isso não garante ausência de cortes em teste ou uso futuro. Não consultar o teste para escolher limite ou lado. Amostragem da inspeção e critérios quantitativos ainda serão definidos. Esta decisão apenas planeja o diagnóstico; nenhuma execução, implementação ou nova configuração científica está autorizada.

### D31 — Preservação integral como critério do limite de entrada

- **Decisão:** exigir preservação integral das mensagens de desenvolvimento com ambos os tokenizers, incluindo os marcadores especiais na contagem. Adotar 64 se todas couberem nesse limite; caso contrário, adotar 128 se todas couberem nele. Se houver mensagem acima de 128 em qualquer tokenizer, nenhum candidato atende ao critério: apresentar os excedentes e revisar a escolha com o autor antes dos treinamentos científicos, sem cortes ou exclusões automáticos.
- **Motivo:** preservar a informação disponível para distinguir intenções e estabelecer uma regra objetiva, sem tolerância arbitrária de cortes. Entre candidatos que preservam tudo, escolher o menor; memória e velocidade continuam sujeitas ao diagnóstico.
- **Relação com D28–D30:** manter candidatos, padding dinâmico e contagem antes da GPU. Esta decisão substitui a possibilidade discutida de aceitar cortes considerados toleráveis após inspeção. O lado do truncamento não afeta as entradas de desenvolvimento que couberem integralmente; sua política operacional para entradas futuras ou maiores ainda será explicitada.
- **Fundamentação e limites:** RESEARCH.md, R31–R34. Estatísticas publicadas em caracteres/palavras não substituem a contagem por tokenizer. Preservar conteúdo é um requisito confirmado do projeto, não demonstração publicada de maior acurácia. A regra se baseia somente no desenvolvimento; não garante ausência de excedentes no teste ou em uso futuro e não autoriza consultar o teste para ajustar o limite.
- **Orientação de continuidade:** após repetição da discussão, o autor pediu inferir a conduta a partir das decisões anteriores. Priorizar preservação integral, sem cortes ou exclusões automáticas, também diante de eventuais entradas de teste/futuras excedentes. Tratar excedentes reais como exceções a apresentar e discutir conforme D42, sem alterar automaticamente o limite nem usar o teste para escolher outra configuração. Não reabrir preventivamente a escolha entre cortar início/final; a proposta de truncamento automático não foi aprovada.
- **Escopo:** nenhuma implementação, medição ou execução autorizada nesta etapa. Critérios técnicos de viabilidade permanecem para consolidação operacional; exceções concretas seguem o princípio de revisão com o autor.

### D32 — Saída do pooler como representação para classificação

- **Decisão:** usar, nos dois modelos, o vetor final de CLS transformado pelo pooler BERT como entrada da camada linear de 77 classes de D14. O pooler aplica transformação linear 768→768 e tanh; não calcula média dos tokens. Encoder, pooler e classificador participam do fine-tuning completo de D13.
- **Motivo:** adotar o mesmo caminho de representação nos dois modelos, alinhado à implementação de classificação BERT e ao exemplo oficial de fine-tuning do FinBERT. Não acrescentar uma comparação experimental com CLS direto às configurações de D22.
- **Fundamentação técnica:** RESEARCH.md, R35. [BertPooler e BertForSequenceClassification, Transformers v4.57.1](https://raw.githubusercontent.com/huggingface/transformers/v4.57.1/src/transformers/models/bert/modeling_bert.py) documentam a transformação e seu uso na classificação; o [notebook oficial FinBERT](https://raw.githubusercontent.com/yya518/FinBERT/master/finetune.ipynb) usa essa classe a partir de yiyanghkust/finbert-pretrain. A versão de código consultada fundamenta o mecanismo, sem fixar as versões de ferramentas do projeto.
- **Precedente acadêmico e limites:** [Benayas et al. (2021), §III](https://repository.essex.ac.uk/32137/1/Unified_Transformer_Multi-Task_Learning_for_Intent_Classification_With_Entity_Recognition.pdf), explicita pooler em classificação de intenções em ATIS/SNIPS, com arquitetura conjunta distinta. Não foi localizada comparação controlada CLS direto versus pooler no BANKING77; Casanueva et al. (2020) não distingue inequivocamente as duas representações no trecho consultado. A decisão tem precedente de uso, não evidência de superioridade em acurácia, calibração ou abstenção.
- **Verificação futura:** no diagnóstico de carregamento, registrar pesos usados, ausentes e novos, incluindo pooler. O log histórico do notebook FinBERT lista apenas a camada classificadora como nova, mas não substitui a auditoria da revisão que será usada. Eventuais diferenças de inicialização devem ser explicitadas e discutidas, sem presumir equivalência.
- **Atualização:** dropout da cabeça confirmado separadamente em D33; nenhuma implementação ou execução autorizada.

### D33 — Dropout de 0,1 na cabeça dos dois modelos

- **Decisão:** aplicar dropout com p=0,1 após o pooler e antes do classificador linear de 77 classes, nos dois modelos. Ativar somente no treino; desativar na validação, no teste e na geração de previsões para abstenção. Manter o dropout interno dos encoders conforme os checkpoints.
- **Controle:** manter o valor fixo nas duas configurações de taxa de aprendizado, sem ampliar a busca de D22.
- **Motivo e fundamento:** regularizar a representação recebida pelo classificador, reduzindo dependência de características específicas. RESEARCH.md, R36, registra precedente explícito de dropout 0,1 no fine-tuning BERT e sua aplicação antes do classificador no código original. É escolha com precedente, não demonstração de melhoria ou valor ótimo no BANKING77.
- **Semântica:** cada elemento tem probabilidade 0,1 de ser zerado a cada passagem de treino, com reescala dos elementos mantidos; não remover pesos permanentemente nem exigir exatamente 10% de elementos zerados em cada passagem.
- **Escopo:** confirmação apenas do desenho; nenhuma implementação ou execução autorizada.

### D34 — Padding à direita nos dois modelos

- **Decisão:** aplicar padding à direita nos dois modelos, usando o marcador do tokenizer correspondente e a máscara de atenção de D29. Preservar o padding dinâmico por lote.
- **Motivo:** manter CLS na primeira posição utilizada pelo pooler e preservar as posições do conteúdo ao acrescentar preenchimento.
- **Fundamentação:** RESEARCH.md, R43, registra a recomendação de padding à direita na documentação BERT, relacionada às posições absolutas. A decisão trata somente de preenchimento; não define lado de truncamento nem política para excedentes.
- **Escopo:** confirmação do desenho, sem autorizar implementação, medição ou execução.

### D35 — Avaliar precisão mista no diagnóstico

- **Orientação do autor:** autoriza registrar adesão às recomendações com bom embasamento. Nesta decisão, a adesão cobre avaliar precisão mista no diagnóstico; não significa confirmação automática de outras propostas pendentes.
- **Decisão:** incluir avaliação de precisão mista automática (AMP) no diagnóstico dos dois modelos, como candidata preferencial para reduzir memória e tempo, com FP32 como referência. A precisão final dos treinamentos científicos permanece condicionada às medições e à definição prévia dos critérios de estabilidade e viabilidade.
- **Fundamento:** RESEARCH.md, R37: trabalho de precisão mista e documentação PyTorch sobre autocast/GradScaler. Há fundamento para a técnica, sem evidência local de ganho ou estabilidade para os checkpoints escolhidos. Não presumir suporte a BF16 nem converter integralmente os modelos para FP16.
- **Controle e pendências:** planejar uma política comum aos dois modelos; dtype candidato definido em D36; fixar procedimento de comparação, registro de não finitos/passos pulados e conduta diante de instabilidade antes de executar. Não trocar precisão silenciosamente nem escolher pelo teste. Acumulação de gradientes continua decisão separada.
- **Escopo:** planejamento do diagnóstico; não autoriza execução, implementação ou adoção definitiva de AMP sem as verificações pendentes.

### D36 — AMP com FP16 e GradScaler como candidata do diagnóstico

- **Decisão:** avaliar AMP com autocast em FP16 e GradScaler nos dois modelos, mantendo FP32 como referência conforme D35. Não converter integralmente pesos e operações para FP16. Usar a mesma abordagem nos dois modelos, após verificar compatibilidade do ambiente real.
- **Fundamentação:** RESEARCH.md, R37, documenta o mecanismo de precisão mista, escalonamento da perda e tratamento de gradientes não finitos no PyTorch; também registra precedente de FP16 em BANKING77 com método distinto. A escolha delimita uma candidata fundamentada, sem demonstrar superioridade sobre BF16 ou estabilidade local.
- **Motivo:** limitar o diagnóstico a uma candidata de precisão mista com procedimento documentado, buscando reduzir memória e tempo sem ampliar a comparação para diferentes formatos de AMP. BF16 não integra este diagnóstico; eventual inclusão exige nova decisão.
- **Pendências:** definir registro de passos pulados, critérios de estabilidade, conduta diante de falhas e procedimento de medição antes da execução. GradScaler pode ajustar sua escala e pular atualizações com gradientes não finitos; isso precisa ser registrado, não interpretado automaticamente como falha fatal. A precisão científica final continua condicionada ao diagnóstico.
- **Autorização e escopo:** adesão à recomendação fundamentada conforme orientação do autor; apenas planejamento, sem implementação ou execução.

### D37 — Selecionar limiares por coberturas-alvo na validação

- **Decisão:** selecionar os limiares operacionais por coberturas-alvo na validação. Congelar os limiares antes do teste e reportar cobertura e erro seletivo efetivamente observados nele; não reajustar os limiares no teste para forçar as metas.
- **Avaliação preservada:** manter curvas completas e AURC de D6/D16, permitindo examinar a relação erro–cobertura além dos pontos operacionais. Não acrescentar seleção separada por erro-alvo ao protocolo principal.
- **Motivo:** alinhar os pontos operacionais à comparação em níveis semelhantes de atendimento, sem pressupor um requisito externo de erro máximo que o projeto não possui. Cobertura-alvo e erro-alvo são abordagens válidas; a preferência é adequação ao desenho, não superioridade universal.
- **Fundamentação e limites:** RESEARCH.md, R2/R8/R42, distingue controle de risco, curvas risco–cobertura e avaliação de confiança. O ajuste empírico de limiares não herda garantias probabilísticas de métodos como SGR. Cobertura na validação não garante cobertura idêntica no teste.
- **Pendências:** valores confirmados em D38; granularidade dos limiares por modelo/regra/execução e convenções operacionais de empates/igualdade continuam abertas. Nenhuma implementação ou execução autorizada.

### D38 — Coberturas-alvo de 95%, 90% e 80%

- **Decisão:** usar coberturas-alvo de 95%, 90% e 80% na validação para selecionar os limiares operacionais de D37, com referência sem abstenção de 100%. Aplicar as mesmas metas aos dois modelos e critérios; conservar curvas completas e AURC.
- **Justificativa prática:** representar encaminhamento de aproximadamente 5%, 10% e 20% das mensagens para esclarecimento e tornar explícita a troca entre atendimento automático e erro seletivo. Fixar esses pontos antes de observar resultados.
- **Fundamentação e limite:** RESEARCH.md, R44, registra busca breve em dois trabalhos de PLN: há apoio à avaliação por risco–cobertura, mas os trechos consultados não justificam especificamente o trio 80/90/95. Os números são escolha prática do projeto, aceita pelo autor; não constituem padrão acadêmico obrigatório nem valores ótimos demonstrados. A busca limitada não prova ausência de justificativas em toda a literatura.
- **Teste:** preservar os limiares selecionados na validação e reportar cobertura efetiva e erro observados; as metas não garantem cobertura idêntica no teste. Empates podem impedir metas exatas e ainda exigem convenção operacional.
- **Escopo:** planejamento e documentação; nenhuma implementação ou execução autorizada.

### D39 — Selecionar taxa pela média das três validações

- **Decisão:** para cada modelo, selecionar a taxa de aprendizado pela maior média das três acurácias de validação, usando em cada repetição o checkpoint selecionado por D20–D21. Avaliar e reportar as três execuções da taxa escolhida, sem selecionar uma seed vencedora.
- **Reporte:** apresentar resultados individuais, média e dispersão entre as três execuções. Não combinar pesos ou probabilidades em ensemble. O estimador específico de dispersão continua pendente; alcance inferencial definido em D41.
- **Motivo:** representar desempenho agregado das repetições em vez de favorecer uma execução excepcional. R25/R40 fundamentam a necessidade de considerar variação; a aplicação da média à seleção é escolha de protocolo coerente com esse princípio, não prova de superioridade sobre outros agregadores.
- **Limites discutidos:** médias iguais podem ocultar estabilidade diferente; três repetições oferecem evidência limitada e são sensíveis a extremos. Pequenas diferenças de média permitem ordenar configurações, mas não demonstram por si só superioridade consistente. A mediana foi discutida e não adotada como critério principal. Não adicionar penalização de instabilidade ao critério.
- **Pendências e escopo:** desempate entre taxas ainda aberto; inferência tratada em D41. Não extrapolar D21 automaticamente para empates entre configurações. Apenas planejamento e documentação; nenhuma implementação ou execução autorizada.

### D40 — Analisar confusões recorrentes e erros aceitos após abstenção

- **Decisão:** focar a análise qualitativa nas confusões recorrentes entre intenções e nos erros que continuam aceitos após aplicar as regras de abstenção. Comparar BERT e FinBERT e examinar como os dois critérios de confiança tratam os casos analisados.
- **Motivo:** conectar os padrões de classificação à contribuição de abstenção, complementando métricas agregadas com mensagens concretas. Priorizar recorrência como princípio de seleção em vez de escolher somente exemplos interessantes.
- **Separação das etapas:** a análise final do teste interpreta os resultados, sem autorizar retreinamento, ajuste de limiares ou outras mudanças motivadas pelo teste. Preservar a distinção entre exploração do desenvolvimento e análise final.
- **Pendências:** ranking dos pares, quantidade de casos, seleção entre repetições e tratamento das mensagens rejeitadas/aceitas serão especificados no protocolo operacional, de forma reproduzível e coerente com o foco aprovado. Não presumir que uma discordância com o modelo seja erro do rótulo oficial.
- **Escopo:** planejamento e documentação; nenhuma implementação, inspeção de dados ou execução autorizada.

### D41 — Comparação descritiva principal e inferência como extensão planejada

- **Decisão:** manter análise descritiva como protocolo principal: resultados individuais, médias, dispersão, curvas e análise de erros. Inferência estatística é extensão opcional, cujo procedimento deve ser planejado antes da avaliação final e cuja inclusão não depende de a diferença observada parecer grande ou pequena.
- **Interpretação:** descrever magnitude e consistência das diferenças nas execuções observadas, sem alegar significância estatística a partir somente de médias ou dispersão. Não tratar diferença de 0,3 ponto percentual como automaticamente irrelevante nem diferença grande como automaticamente consistente; importância prática depende do contexto e dos erros.
- **Motivo:** adequar o alcance das conclusões ao protocolo e ao orçamento, separando importância prática de evidência estatística. Três repetições limitam a evidência, mas não tornam todo procedimento inferencial automaticamente inválido.
- **Extensão:** não foi aprovado teste, intervalo, hipótese, nível de significância ou procedimento inferencial específico. Caso a extensão seja incluída, definir e justificar esses elementos antes da avaliação final; não escolher o teste conforme os resultados do teste oficial.
- **Escopo:** planejamento e documentação; nenhuma implementação ou execução autorizada.

### D42 — Auditar dados antes do treino e revisar alterações com o autor

- **Decisão:** planejar auditoria de dados antes do treino, verificando textos vazios, duplicatas, rótulos conflitantes e sobreposição entre conjuntos. Preservar o teste oficial e documentar ambiguidades; não corrigir rótulos apenas porque um modelo discorda deles.
- **Tratamento:** diante de problemas que possam comprometer a comparação, apresentar diagnóstico e proposta de correção ao autor antes de alterar os dados. Alterações com efeito no experimento dependem de decisão explícita; não limpar, excluir ou corrigir automaticamente.
- **Fundamento:** RESEARCH.md, R7/R43, registra pesquisa sobre problemas de anotação no BANKING77 e a necessidade de distinguir ambiguidade/erro de rótulo de erro do modelo. Isso motiva a auditoria; não prova a presença de qualquer problema nos arquivos concretos, ainda não auditados.
- **Limites:** política geral confirmada; ações específicas dependem dos achados, sem presumir problemas ou suas soluções. Manter comparação rastreável, mesmos conjuntos entre modelos e separação entre desenvolvimento e teste conforme decisões anteriores.
- **Escopo:** planejamento da auditoria; nenhuma inspeção de dados, implementação ou execução autorizada nesta etapa.

### D43 — Meta de implementar e iniciar experimentos em 14–15/11

- **Decisão do autor:** tentar realizar a implementação entre hoje (14/11/2026) e amanhã (15/11/2026), já iniciando os experimentos assim que o pipeline estiver verificado e o diagnóstico permitir. Esta meta substitui o cronograma proposto de implementar em 16–17/11 e experimentar em 18–20/11, que não foi aprovado.
- **Sequência:** consolidar detalhes técnicos delegados e concluir a revisão/aprovação do desenho; implementar com verificações incrementais; executar auditoria e diagnóstico; iniciar treinamentos completos quando as condições do protocolo forem atendidas. Não dispensar verificações para cumprir a meta.
- **Orçamento preservado:** manter as 12 execuções e cinco épocas de D22/D24; estimar duração real no diagnóstico. A meta é iniciar os experimentos em 14–15/11, não garantir conclusão de todas as execuções nesse intervalo. Mudanças em épocas, configurações ou repetições exigem revisão com o autor.
- **Entrega:** spec.md registra artigo/código em 26/11 e apresentação em 24 ou 26/11; autor ainda não sabe sua data de apresentação. Planejar preparação para a primeira data possível, respeitando artigo de 8–10 páginas e apresentação de exatamente 15 minutos. Datas intermediárias de análise/escrita/slides ainda não foram aprovadas.
- **Escopo:** registrar a meta de execução antecipada; concluir a revisão e aprovação do desenho de D5 antes da implementação. Nenhum código ou experimento foi executado nesta etapa.

## Diagnóstico de hardware e configurações condicionadas

Esta seção reúne decisões dependentes de medição; não autoriza implementação ou início do diagnóstico nesta fase de planejamento.

| Item | Planejado | Verificação necessária | Como revisar |
|---|---|---|---|
| Ambiente (D7) | Notebook principal; Colab como alternativa | GPU/VRAM disponíveis, carregamento, funcionamento e memória | Documentar ambiente efetivamente usado; não presumir que o hardware disponível corresponde ao nominal |
| Entrada (D28–D31) | 64 se preservar todo o desenvolvimento em ambos os tokenizers; senão 128 se preservar tudo; padding dinâmico | Antes da GPU: máximo e quantidade/proporção acima de cada limite por tokenizer, incluindo marcadores especiais. Depois: medir memória e tempo em conjunto com batch | Se algum exemplo exceder 128, revisar com o autor; não cortar ou excluir automaticamente nem usar o teste para escolher |
| Batch size (D27) | Candidatos 8, 16 e 32 | Memória máxima e exemplos/s com a mesma sequência e precisão nos dois modelos | Escolher conforme critério técnico previamente fechado e registrar valor comum; se nenhum candidato for viável, discutir alternativa |
| Épocas (D24) | Cinco, com avaliação por época | Projetar tempo para três e cinco épocas nas 12 execuções, incluindo validação e salvamento | Redução para três depende de confirmação do autor; duas horas adicionais foram consideradas relevantes, não um limite rígido |
| Orçamento (D22) | 12 treinamentos completos | Estimar duração total a partir dos dois modelos | Revisar com o autor antes de alterar configurações ou repetições |
| Scheduler (D26) | Warmup de 10% e redução linear | Calcular passos a partir de batch e épocas finais | Recalcular após fixar configuração; mudança de épocas altera a trajetória de taxas |

Avaliação de AMP no diagnóstico aprovada em D35, com FP32 como referência; precisão final e eventual acumulação de gradientes continuam abertas e não são adaptações automáticas para contornar limitações. Os candidatos de comprimento de sequência estão definidos em D28, mas o valor final depende de medição. O diagnóstico não será usado para escolher modelos ou hiperparâmetros com base no desempenho do teste. Registrar medidas e configuração final antes dos experimentos completos, preservando as condições comparáveis entre modelos.

Somente decisões confirmadas pelo autor serão incorporadas a este plano. Nenhuma implementação está autorizada nesta etapa.

## Retomada em nova sessão — 2026-11-14

- **Modo:** brainstorming com Vibe-Wise; explicar uma ideia por vez, apresentar fundamento e limites e fazer apenas uma pergunta arquitetural por turno. D1–D43 estão confirmadas e travadas. Não confundir aceitação de proposta com domínio conceitual demonstrado.
- **Escopo autorizado:** planejamento e documentação. Nenhum código, treinamento, diagnóstico ou download de pesos/dataset foi iniciado ou autorizado. Registrar novas decisões no plano somente após confirmação individual.
- **Ponto atualizado de retomada:** D37 confirma seleção por coberturas-alvo na validação, congelando limiares antes do teste. D38 confirma metas de 95%, 90% e 80%, com referência de 100%. D39 confirma seleção da taxa pela média das três acurácias de validação e reporte das três execuções com média/dispersão. D40 confirma foco em confusões recorrentes e erros aceitos após abstenção. D41 confirma comparação descritiva principal e inferência opcional planejada antes da avaliação final, sem condicionar inclusão ao tamanho da diferença. D42 confirma auditoria antes do treino, preservação do teste oficial e revisão de alterações com o autor. Autor pediu inferir a política de excedentes pelas decisões anteriores: preservar conteúdo, sem cortes/exclusões automáticos, e discutir exceções somente se observadas, conforme esclarecimento em D31/D42. Não repetir a decisão sobre lado de corte. D43 confirma a meta de implementar e iniciar experimentos em 14–15/11, com diagnóstico anterior às execuções completas. Consolidação concluída como proposta O1–O9; revisão documental D5 registrada em R45. Próximo passo: aprovação conjunta do desenho e dos acréscimos operacionais, antes de implementar. Autor pediu abstrair detalhes operacionais e concentrar a conversa em escolhas que afetam validade e interpretação; profundidade sobre AMP não é a próxima discussão de aprendizado. Detalhes técnicos propostos em O1–O9 aguardam aprovação conjunta do desenho; implementação ainda não iniciada.
- **Decisões desta continuação:** D28 restringe comprimento a 64/128 após medição; D29 aprova padding dinâmico; D30 organiza estatísticas de entrada antes da GPU; D31 exige preservação integral do desenvolvimento nos dois tokenizers, com 64 se suficiente, senão 128 e revisão se houver excedentes; D32 aprova pooler treinável seguido do classificador linear. D31 atualiza a discussão anterior de tolerar cortes após inspeção; não reabrir essa tolerância como pendência.
- **Entrada ainda por medir:** o limite final não foi escolhido. Os 13–433 do visualizador são caracteres, não tokens; não resolvem o máximo nos tokenizers. Contar incluindo marcadores especiais. Padding à direita confirmado em D34; excedentes reais seguem preservação e revisão de exceções conforme D31/D42.
- **Pesquisa já disponível:** consultar os blocos pertinentes de RESEARCH.md pela tabela abaixo antes de repetir buscas. A autorização autônoma de pesquisa terminou às 22h49; novas pesquisas voltam a exigir pedido prévio, salvo nova autorização do autor.

| Pendência do Próximo Passo | Pesquisa disponível | O que já ajuda a decidir e o que permanece aberto |
|---|---|---|
| 1 — Entrada/tokenização | R31–R34, R43 | 64/128 têm precedentes; caracteres não equivalem a tokens; documentação recomenda padding à direita para BERT. Padding à direita em D34; preservação e revisão de excedentes reais esclarecidas em D31/D42 |
| 2 — Dropout da cabeça | R35–R36 | Pooler já aprovado; p=0,1 tem precedente explícito no fine-tuning/cabeça BERT. O 0,75 do artigo BANKING77 pertence a outro regime. Dropout 0,1 confirmado em D33 |
| 3 — Precisão e otimização | R37–R38 | AMP/GradScaler, acumulação e ordem de clipping documentados; betas, epsilon histórico/moderno e exclusões de decay comparados. D35–D36 definem candidata AMP FP16/GradScaler versus referência FP32; estabilidade, precisão final, acumulação, betas/epsilon, grupos e clipping continuam abertos |
| 4 — Diagnóstico | R30, R34, R37, R39 | Fundamentação de tempo sincronizado, memória alocada/reservada e lotes representativos. Duração, amostra, margem e regra final de batch ainda não definidas; não há medições locais |
| 5 — Dados/reprodução | R7, R34, R40, R43 | Controle de aleatoriedade e limites de reprodução; fundamento para auditoria de dados. Seeds, revisões/índices e tratamento de problemas continuam abertos |
| 6 — Configurações/repetições | R25, R40 | Seleção/reporte em D39, alcance inferencial em D41 e complementos propostos em O5 |
| 7 — Limiares/cobertura | R2, R6, R8, R42 | Distinguir ranking descritivo e regra congelada; empates impedem certas coberturas exatas e cobertura de validação não é garantida no teste. Objetivo em D37 e metas 95/90/80 em D38; convenções ainda abertas |
| 8 — Convenções de métricas | R19–R20, R41–R42 | ECE com 15 faixas tem precedente, mas depende de binning/amostra; zero_division e AURC discreta exigem convenções. Faixas, conjunto, integração, escala, empates e cobertura zero ainda não aprovados |
| 9–12 — Análise, execução, checks e entrega | R40, R43 como apoio parcial; spec.md e itens abaixo | Foco qualitativo em D40, meta em D43; O2/O8/O9 consolidam execução/artefatos/checks/entrega; revisão D5 registrada em R45 |

As propostas da pesquisa não são decisões automaticamente: D33–D43 registram as confirmações posteriores. Os detalhes operacionais delegados estão consolidados no apêndice abaixo para revisão final; números práticos não devem ser apresentados como valores ótimos demonstrados pela literatura.

## Próximo Passo

Esta lista preserva o histórico das pendências; O1–O9 consolidam os detalhes operacionais e as correções de REVIEW.md. Permanecem abertas as medições do diagnóstico; o critério quantitativo de estabilidade do AMP foi decidido depois em D44. As decisões D1–D43 permanecem válidas.

1. **Entrada e tokenização:** candidatos **64 e 128 tokens**, padding dinâmico e diagnóstico antes da GPU confirmados em D28–D30. D31 fecha o critério: preservação integral no desenvolvimento em ambos os tokenizers, escolhendo 64 se suficiente, senão 128; excedentes de 128 exigem revisão com o autor. Padding à direita confirmado em D34. Para eventuais excedentes, seguir o princípio de preservação de D31 e revisão de exceções reais de D42, sem cortes/exclusões automáticos nem adaptação do limite ao teste. Não repetir a discussão preventiva de lado do corte. Uso do tokenizer próprio de cada modelo já está confirmado em D12.

2. **Regularização da cabeça — concluída:** pooler em D32 e dropout p=0,1 em D33, somente no treino, nos dois modelos, mantendo dropout interno dos checkpoints. CLS com camada linear, 77 classes, softmax e cross-entropy já estão confirmados; não reabrir a escolha de arquitetura inteira.

3. **Precisão e detalhes da otimização:** avaliação de AMP no diagnóstico com referência FP32 confirmada em D35; candidata FP16/GradScaler definida em D36; definir precisão final, critérios de estabilidade e comportamento diante de instabilidade numérica, beta/epsilon do AdamW, exclusão ou inclusão de bias/LayerNorm no weight decay e eventual clipping de gradientes. Decidir se acumulação de gradientes será usada; ela não está autorizada como adaptação automática. AdamW, decay 0,01 e scheduler de D25–D26 já estão fechados.

4. **Protocolo executável do diagnóstico:** fixar amostra de desenvolvimento, duração/aquecimento da medição, margem de VRAM, regra de escolha entre batches 8/16/32 e conduta se nenhum for viável nos dois modelos. Definir como estimar tempo incluindo validação e salvamento. A decisão de medir batches e comparar projeções de três/cinco épocas já foi tomada; resultados numéricos só existirão após execução autorizada. Cinco épocas e 12 treinamentos continuam planejados, sujeitos à revisão confirmada pelo autor.

5. **Dados e reprodução:** definir semente da divisão, três seeds de treinamento e quais fontes de aleatoriedade variarão; garantir mesmos exemplos de treino/validação entre modelos. D42 confirma auditoria de duplicatas, rótulos conflitantes, textos vazios e sobreposição; documentar achados e submeter alterações com efeito no experimento ao autor, preservando o teste oficial. Escolher revisões do dataset, modelos e tokenizers e registrar índices dos splits. A proporção de validação e o teste oficial já estão fechados em D19.

6. **Escolha da configuração e reporte das repetições:** D39 confirma seleção da taxa pela média das três acurácias de validação, preservando as três execuções da taxa escolhida na avaliação final e apresentando resultados individuais, média e dispersão. Definir desempate entre taxas e estimador de dispersão. D41 estabelece comparação descritiva principal; eventual inferência exige planejamento anterior à avaliação final, independentemente do tamanho da diferença observada. Interpretar diferenças pequenas com cautela; não escolher a melhor seed e descartar as demais. Seleção por época dentro de cada execução já está fechada em D20–D21.

7. **Limiar operacional e comparação de cobertura:** objetivo por coberturas-alvo na validação confirmado em D37; metas 95/90/80 e referência 100 em D38. Definir se haverá um limiar por modelo/regra/execução. Fixar regra de aceitação na igualdade, tratamento de empates nas pontuações, coberturas a apresentar e como lidar com cobertura efetiva diferente da desejada no teste. As metas de D38 são escolhas práticas confirmadas; nenhum erro-alvo foi aprovado. Comparar apenas os dois critérios separados e a referência sem abstenção já está confirmado.

8. **Convenções de avaliação:** definir cálculo discreto e escala da AURC, empates, cobertura zero e alinhamento das curvas entre repetições; definir divisões por zero nas métricas por intenção. Para ECE secundária, escolher número/tipo de faixas, conjunto avaliado e forma de apresentação. Acurácia, Macro-F1, AURC e ECE já foram aprovadas; RPP e correção de calibração permanecem fora do escopo.

9. **Análise de erros:** foco confirmado em D40: confusões recorrentes e erros aceitos após abstenção, comparando os dois modelos e critérios. Especificar ranking, número e seleção reproduzível de exemplos/repetições no protocolo operacional. Separar desenvolvimento da análise final do teste, sem usar esta última para retunar o sistema.

10. **Arquitetura de execução e artefatos:** fechar ferramentas, versões, organização de módulos/comandos, configuração dos experimentos e sequência dados → treinamento → seleção → previsões → abstenção → relatório. Especificar o conteúdo salvo para reprodução: configuração, seeds, logs, checkpoints selecionados, rótulos/pontuações por exemplo, limiares e resultados. O reaproveitamento de previsões já está aprovado; o formato e a estrutura ainda não.

11. **Verificações e critérios de conclusão:** definir checks focados antes da implementação para divisão sem vazamento, 77 classes, probabilidades válidas, seleção de checkpoints, limiares, AURC e ECE. Estabelecer baseline e comparação automatizada pertinente, sem pressupor melhoria garantida de FinBERT ou de abstenção. Seguir o ciclo de uma verificação falhando antes da implementação correspondente, conforme as instruções da sessão.

12. **Entrega e revisão final:** D43 confirma meta de implementar e iniciar experimentos em 14–15/11, sujeita a verificações e diagnóstico. Fechar cronograma restante de análise/artigo, tabelas/figuras e critérios para encerrar a busca; conciliar com artigo de 8–10 páginas e apresentação de 15 minutos exigidos em spec.md. Realizar a segunda iteração bibliográfica de D5, incorporar respostas do professor quando disponíveis, declarar uso de IA conforme a especificação e submeter o desenho consolidado à aprovação antes de implementar. Revisões do que já foi decidido continuam dependendo de confirmação.

## Consolidação operacional — revisão final pendente

Este apêndice atende à delegação dos detalhes técnicos e ao pedido de concluir o desenho. D1–D43 continuam confirmadas; os detalhes adicionais abaixo são propostas para aprovação conjunta do desenho final, não decisões científicas retroativamente atribuídas ao autor. A lista anterior passa a servir de índice de rastreabilidade: suas pendências operacionais são tratadas aqui. Nenhuma implementação, instalação, download ou medição foi realizada nesta consolidação.

### O1 — Dados, sementes e versões

- Usar o BANKING77 oficial referenciado em R1, sem substituir por variante corrigida. Resolver a origem e registrar revisão imutável, nomes dos arquivos e SHA-256 dos dados antes de treinar. Conferir 77 rótulos e as contagens esperadas em D19; divergência exige diagnóstico, não ajuste silencioso.
- Criar uma única divisão estratificada do treino oficial com proporção 0,10 e seed **42**. Persistir IDs/índices, rótulos e hash do split; reutilizá-los em todos os modelos e execuções. IDs vinculam-se à origem, revisão, split e posição original, sem depender do texto.
- Usar seeds de treino **13, 37 e 73**, reiniciando Python, NumPy, PyTorch, CUDA e ordem dos lotes a cada execução. A mesma seed numérica entre modelos não significa estados aleatórios idênticos. Números das seeds são escolhas práticas, não valores indicados por artigo.
- Registrar versões e política de determinismo; desativar escolha automática de algoritmos por benchmarking e solicitar operações determinísticas. Se houver operação incompatível, registrar e revisar explicitamente antes da execução científica; não esconder a ocorrência. Inicialmente, DataLoader com zero workers para simplificar reprodução.
- Auditar igualdade exata e, como diagnóstico adicional, igualdade após aparar espaços externos e compactar espaços internos; não modificar os textos originais. Registrar vazios, duplicatas, conflitos e sobreposição, distinguindo os dois critérios de igualdade. Achados que afetem validade seguem D42; nenhuma limpeza automática.
- Fixar commits dos dois checkpoints e tokenizers e registrar arquivos, hashes e logs de carregamento. Usar o tokenizer próprio, sem truncamento, nas contagens de desenvolvimento; incluir marcadores especiais. Revisões concretas serão resolvidas durante preparação autorizada, antes de congelar o manifesto científico.
- **Base:** R1, R3–R4, R9/R13, R34, R40/R43. Garantia de identidade de exemplos vem dos índices persistidos; seed sozinha não é suficiente.

### O2 — Ambiente e organização da implementação

- Usar Python 3.11, ambiente de projeto com **uv**, PyTorch, Transformers, Datasets, NumPy, scikit-learn, Matplotlib e pytest. Organização em pacote `src/nlp_finance/`, testes em `tests/`, parâmetros em JSON e comandos por módulo Python. A escolha das ferramentas é operacional, sem alegação de superioridade científica.
- Separar responsabilidades em dados/auditoria, tokenização, modelo, treino/seleção, diagnóstico, previsões, abstenção/métricas e relatório. Comandos correspondentes: preparar, diagnosticar, treinar, selecionar, prever e relatar. Nenhum comando de treinamento deve iniciar avaliação final do teste implicitamente.
- Resolver versões compatíveis e gerar lockfile após conferir o ambiente disponível. Registrar Python, sistema, GPU, driver, CUDA, versões efetivas e configurações. Não instalar uma combinação presumida nem confundir versões das referências documentais com versões já aprovadas/instaladas.
- Salvar em diretórios por modelo/taxa/seed: configuração, IDs dos dados, log de épocas, melhor checkpoint, metadados de seleção e previsões. Salvar logits FP32, probabilidades calculadas em FP64 a partir desses logits, rótulos e IDs em NPZ sem objetos; metadados/limiares/métricas em JSON, tabelas em CSV e figuras em SVG/PNG.
- Em interrupção ou falha técnica, reiniciar a execução completa com a mesma configuração e seed, sem retomar do melhor checkpoint. Preservar logs e artefatos de cada tentativa com identificador próprio; somente uma execução completa e válida conta como repetição. Desempenho baixo, isoladamente, não é falha técnica e não justifica trocar seed.
- Registrar a causa e o alcance de cada correção. Se alterar treinamento ou resultados, invalidar e refazer todas as execuções afetadas, inclusive as já concluídas; mudanças de desenho seguem revisão com o autor. Preservar resultados anteriores para auditoria e não usar o desempenho no teste para orientar correções.
- Preservar checkpoints originais. Permitir apenas a nova cabeça de classificação como inicialização esperada; auditar separadamente pesos de encoder/pooler ausentes e pesos de pré-treinamento descartados. Ausência inesperada de encoder/pooler segue D32 e exige revisão.
- Antes de downloads maiores que 50 MB, avisar tamanho estimado, finalidade e consumo de rede/disco conforme AGENTS.md. Nenhum download está sendo realizado nesta etapa.

### O3 — Otimização e comportamento numérico

- Manter AdamW/decay, taxas, cinco épocas e scheduler de D23–D26. Complementar com **betas (0,9; 0,999), epsilon 1e-8, exclusão de bias e parâmetros de LayerNorm do decay e clipping global de norma 1,0**. Registrar grupos por nome e tipo de parâmetro, evitando exclusões por substring genérica.
- Betas têm precedente comum entre implementação BERT e AdamW moderno; epsilon é escolha do AdamW moderno, não reprodução do otimizador histórico. Exclusões e clipping têm precedente operacional BERT. R38 não demonstra optimalidade desse conjunto para nosso par.
- Planejar **sem acumulação de gradientes**: cada lote gera uma atualização quando seus gradientes são válidos. Se nenhum batch aprovado couber, interromper e discutir alternativa; não acrescentar acumulação silenciosamente.
- Warmup com `ceil(0,10 × total de atualizações planejadas)`, limitado ao total; decaimento linear até zero no horizonte planejado. Usar todos os exemplos, inclusive último lote incompleto; registrar total previsto, atualizações efetivas, saltos e taxa final. Scheduler avança somente quando o otimizador efetivamente atualiza os pesos. Se AMP pular passos, cinco épocas podem terminar antes de a taxa chegar a zero; não acrescentar passos para compensar. Verificar em teste focado que um passo pulado não avança o scheduler.
- Avaliar AMP FP16/GradScaler e referência FP32 conforme D35–D36. Em AMP, desfazer escala antes de clipping. Registrar escala e atualizações puladas. Não tratar um passo pulado isolado como falha fatal.
- **Atualização posterior em D44:** perda ou parâmetros não finitos interrompem imediatamente; o limite de três saltos consecutivos aplica-se após as primeiras 20 tentativas. Registrar escala, total e fração de saltos e atualizações válidas, e aplicar também o critério de janela de D44. Não trocar precisão nem reiniciar silenciosamente.
- AMP só será admitida para os treinamentos se for compatível, estável e viável nos dois modelos, e apresentar economia de memória ou aumento de throughput observado em ambos contra FP32 em um mesmo batch comparável. Se não houver comparação viável em FP32 ou esse critério não for atendido, apresentar as medições antes de fixar outra política; não converter ausência de referência em ganho comprovado.
- Validação e geração final de previsões em **FP32 e modo de avaliação**, para manter a mesma precisão de avaliação entre execuções e desativar dropout. Não aplicar softmax antes da cross-entropy no treinamento.
- **Base:** R17/R28–R29 e R37–R38; os limites e critérios quantitativos adicionais são escolhas práticas transparentes.

### O4 — Diagnóstico antes dos treinamentos científicos

- Primeiro contar tokens de todo o desenvolvimento, com ambos os tokenizers e sem cortes. Aplicar D31: 64 se preservar tudo; senão 128 se preservar tudo; qualquer excedente de 128 retorna ao autor. Não consultar teste para selecionar comprimento.
- Para comparar throughput, usar amostra fixa de **512 mensagens estratificadas do treino**, seed 42, persistindo IDs e ordem. A amostra não é uma garantia de representatividade; registrar distribuição de comprimentos e compará-la à do treino. Nenhum uso de qualidade do teste.
- Em cada modelo/precisão/batch 8, 16 e 32, aquecer por cinco atualizações em janela separada e medir uma passagem completa pelos mesmos 512 exemplos, na mesma ordem, incluindo último lote incompleto. Reinicializar modelo e otimizador entre candidatos; não aproveitar pesos do diagnóstico como início das execuções científicas. Fixar seed 13, a menor taxa de D23, scheduler de D26 com horizonte de cinco épocas do treino completo e escala inicial do GradScaler explicitamente registrada e igual entre candidatos AMP; registrar também os valores efetivos.
- Medir atualizações completas, incluindo AdamW; sincronizar CUDA nos limites da janela, reiniciar contadores de pico após aquecimento e registrar exemplos/s, memória alocada/reservada e VRAM livre. Não somar memória alocada e reservada. Registrar uso externo da GPU e executar um candidato por vez.
- Fazer também teste de memória com lote composto de repetições da mensagem de treino mais longa para cada tokenizer. Este lote é somente stress de recursos; não altera o dataset científico nem entra no throughput representativo ou nas métricas.
- Exigir, após stress, **ao menos 1 GiB livre**, além de registrar os picos e ausência de OOM. Trata-se de margem prática que não garante ausência de OOM em toda condição; execução com outros consumidores relevantes de GPU exige nova verificação.
- Entre batches viáveis nos dois modelos, escolher o que maximiza o menor throughput entre os dois. Se a diferença for de até 5%, preferir o menor batch, poupando memória; esse desempate é prático. Usar uma única precisão de treino e um batch comum nas 12 execuções.
- Medir uma validação completa e um salvamento de checkpoint por modelo separadamente. Projetar custo de três/cinco épocas nas 12 execuções usando throughput da amostra estratificada, incluindo avaliação e cinco salvamentos por execução como estimativa conservadora; declarar que diferenças de comprimento, aquecimento e variação de execução limitam a projeção. O stress de comprimento não entra nessa estimativa. Reportar custo de carregamento e geração de previsões à parte; liberar checkpoints temporários do diagnóstico.
- Publicar relatório de diagnóstico e manifesto com configuração final antes das execuções completas. Se memória, estabilidade ou duração inviabilizarem o orçamento, revisar com o autor conforme D7/D22/D24; não reduzir épocas/repetições automaticamente.
- **Base:** R30/R34/R37/R39. Amostra, duração, margem e regra de desempate não são valores ótimos estabelecidos por publicação.

### O5 — Seleção das configurações e congelamento do protocolo

- Dentro de cada execução, seguir D20–D21 sem alterar o desempate. Entre taxas, usar a média das três acurácias de validação conforme D39; em empate exato, maior média de Macro-F1; persistindo empate, menor taxa de aprendizado. Esse desempate entre taxas é proposta operacional explícita, não extensão tácita de D21.
- Comparar métricas sem arredondamento de exibição; para acurácia, usar contagens de acertos, pois todas as validações têm os mesmos exemplos. Não escolher seed pelo teste.
- Reportar valores individuais, média e **desvio-padrão amostral** entre as três execuções escolhidas. É estimador de dispersão, não intervalo de confiança nem evidência de significância. D41 rege qualquer extensão inferencial.
- Antes de gerar previsões finais do teste, persistir manifesto com hashes de dados/configuração, commits, seeds, tamanho de entrada, batch, precisão, taxas selecionadas, checkpoints e limiares. Mudanças após congelamento ficam registradas e não podem ser guiadas por desempenho no teste.
- A auditoria de integridade do teste de D42 não é ajuste por qualidade preditiva. Excedentes de entrada continuam exceções explícitas de D31; o manifesto não autoriza truncar, excluir ou acrescentar uma regra de abstenção por comprimento.
- **Base:** D20–D21/D39/D41 e R25/R40. Desempate e estimador de dispersão são convenções declaradas.

### O6 — Limiares e comparação das regras

- Para cada modelo, execução selecionada, regra e meta 95/90/80, escolher um limiar próprio na validação. Isso acomoda distribuições de confiança diferentes; mesmo valor numérico de limiar não representa necessariamente a mesma cobertura.
- Aceitar quando **score ≥ limiar**. Para meta c com n exemplos, tomar o score do exemplo na posição `ceil(c × n)` em ordem decrescente. Aceitar todos os empates nessa posição: a cobertura realizada será a menor cobertura atingível por essa regra que seja pelo menos a meta. Registrar meta, cobertura realizada e quantidade de empates; não separar empates usando rótulos.
- Usar os mesmos logits/probabilidades e previsões para MSP e margem entre as duas maiores probabilidades, conforme D3/D11; empate no argmax entre classes usa menor ID de rótulo, deterministicamente.
- Aplicar os limiares congelados ao teste. Reportar erro e cobertura efetivos, sem recalibrar para atingir o alvo. Tabelas com a mesma meta de validação não autorizam dizer que as coberturas de teste são idênticas; usar curvas descritivas para comparação em cobertura comum.
- Manter referência sem abstenção de 100%. Cobertura zero tem erro seletivo indefinido, representado como `null`, nunca como zero. Sem novos treinamentos por regra/meta.
- **Base:** R2/R8/R42 e D37–D38. Igualdade, quantil e aceitação em blocos empatados são convenções operacionais justificadas, sem garantia estatística de risco.

### O7 — Convenções das métricas

- Acurácia/Macro-F1 e precisão/recall/F1 por intenção incluem explicitamente os 77 rótulos. Usar `zero_division=0`, registrando os casos indefinidos separadamente. Não retirar classes silenciosamente da média.
- AURC descritiva na escala **0–1**: ordenar scores decrescentes e calcular a média dos riscos dos prefixos de tamanho 1 até n. Não adicionar ponto artificial de risco zero na cobertura zero nem misturar integração trapezoidal com essa convenção.
- Para scores exatamente empatados, calcular o valor esperado dessa AURC sob todas as ordens uniformes dentro do bloco, analiticamente, sem aleatoriedade adicional. Se antes do bloco há a exemplos e E erros, e o bloco contém m exemplos e e erros, o risco esperado no prefixo que inclui j elementos do bloco é `(E + j × e/m)/(a + j)`. A AURC é a média desses valores para todos os prefixos.
- Essa fórmula de empates é uma **dedução matemática operacional**, não resultado atribuído aos artigos revisados. Sem empates, coincide com a média usual dos riscos dos prefixos. Exemplo de verificação: um acerto de maior score, seguido de um acerto e um erro empatados, produz AURC esperada **7/36**; o teste deverá conferir a média das duas ordenações possíveis. Curvas operacionais por limiar só contêm finais dos blocos; prefixos internos são descritivos e não correspondem a limiares executáveis.
- Plotar as três curvas por execução de cada modelo/regra, sem interpolar riscos entre seeds para fingir coberturas operacionais iguais. Reportar média/desvio da AURC por execução e os pontos operacionais com suas coberturas efetivas.
- ECE secundária nas previsões sem abstenção: **15 faixas de largura igual**, confiança da classe prevista e acerto, ponderação pela quantidade de exemplos. Faixas fechadas à esquerda e abertas à direita, exceto a última, que inclui 1. Faixas vazias contribuem peso zero; salvar contagens, confiança média e acurácia. Reportar validação como diagnóstico e teste como resultado final, sem corrigir calibração.
- **Base:** R19–R20/R41–R42. Quinze faixas têm precedente em Guo et al.; não são número ótimo demonstrado. Relatar baixa ocupação e dependência da estimativa em relação às faixas/amostra.

### O8 — Análise de erros, baseline e verificações incrementais

- Na análise final, ordenar pares não direcionados de intenções pela contagem total de confusões entre as três execuções de cada modelo; preservar também contagens direcionadas. Empates por IDs de rótulos. Usar a união dos **cinco primeiros pares de cada modelo**, no máximo dez pares.
- Selecionar até **dois exemplos por par**: priorizar erro recorrente entre seeds que continue aceito na meta de 90%, depois caso rejeitado do mesmo par quando disponível; desempatar por ID de exemplo. Mostrar previsão, rótulo, pontuações e decisões dos dois modelos/regras, sem omitir discordâncias. A meta de 90% aqui organiza exemplos, não substitui avaliação nos demais níveis.
- Ranking, limite de casos e prioridade qualitativa são escolhas práticas para caber no artigo. Contagens agregadas de execuções não são observações independentes; não confundir até 20 exemplos selecionados com amostra representativa de todas as falhas.
- Registrar baseline trivial de **classe majoritária do treino** antes dos treinamentos, com desempate por menor ID; medir na validação e congelar antes do teste. Comparar modelos treinados a essa referência e à referência sem abstenção. O baseline trivial não substitui BERT como comparação principal nem acrescenta treinamento.
- Verificações serão implementadas **uma por vez**, confirmando falha antes do código correspondente: divisão/IDs sem vazamento; saída de 77 classes e gradientes nos componentes ajustáveis; checkpoint por D20–D21; seleção da taxa por D39/O5; probabilidades finitas e normalizadas; limiares calculados só na validação, incluindo empates; AURC com caso manual e empates; ECE com caso manual e bordas de faixas; serialização/releitura das previsões.
- Acrescentar verificações focadas de identidade do mapeamento bidirecional rótulo↔ID entre splits e modelos e de equivalência das previsões em FP32 antes e depois de salvar/recarregar o checkpoint, com tolerância numérica explícita. No diagnóstico, exigir pequeno teste de aprendizado em exemplos de treino, registrando perda inicial e final; investigar falha antes das execuções completas, sem usar o teste final para orientar correções.
- Antes das execuções completas, exigir smoke test de atualização de pesos, validação e salvamento/recarregamento, sem resultados do teste. Comparar automaticamente resultados treinados ao baseline e registrar magnitude/sinal; se não houver aprendizado sobre a referência trivial, investigar pipeline antes de encerrar a execução como verificada. Não exigir que FinBERT supere BERT nem que cada regra reduza erro em toda cobertura para considerar o resultado científico válido.
- Nenhum teste foi escrito ou executado nesta fase documental. Exemplos manuais são especificações dos checks, não evidência de que a implementação passa.

### O9 — Resultados e encerramento

- Tabela principal: acurácia, Macro-F1 e ECE por execução e média/desvio dos dois modelos. Tabela de abstenção: modelo/regra/meta, cobertura e erro efetivos, com referência sem abstenção; tabela de AURC por execução e resumo. Curvas risco–cobertura e diagramas de confiabilidade acompanham a interpretação.
- Apresentar limites do par de checkpoints, diferença de vocabulários, validação compartilhada, três seeds, erros de anotação quando documentados e ausência de garantias de risco. Declaração de IA conforme spec.md. Respostas do professor só entram mediante relato efetivo; nenhuma aprovação docente foi presumida.
- Alinhar proposta, artigo e apresentação ao escopo de intenções bancárias e comparação de checkpoints; não prometer compreensão financeira corporativa nem atribuir diferenças apenas à arquitetura. Verificar e registrar o status da consulta e aprovação docente sem presumir resposta. Entregar artigo em formato SBC, com 8–10 páginas excluindo referências, código reproduzível e apresentação de exatamente 15 minutos, conforme spec.md.
- Encerrar a busca ao concluir duas taxas × três seeds × dois modelos com os checks aprovados, artefatos íntegros e resultados analisados. Resultados desfavoráveis não autorizam ampliar a busca. Falhas técnicas são registradas e corrigidas sem contar tentativas incompletas como repetições científicas; mudanças de desenho voltam ao autor.
- D43 mantém a meta de implementar e iniciar experimentos em 14–15/11. Preparar metodologia e referências em paralelo; após as execuções, dedicar os dois dias seguintes a análise/artigo e reservar 23/11 para slides e ensaio, visando prontidão para 24/11 e entrega em 26/11. São metas condicionadas à duração real, não promessa de término nem obrigação de consumir os dias completos.
- Sem novos modelos, testes de significância, correções de calibração, ablações ou pré-treinamento próprio nesta versão. Extensões seguem as decisões confirmadas e nova revisão de escopo.

### D44 — Critério operacional de estabilidade do AMP

- **Decisão delegada pelo autor em 15/11/2026:** no diagnóstico de cada modelo com o batch candidato à configuração final, registrar separadamente as primeiras 20 tentativas de atualização e uma janela seguinte de 100 tentativas. Na janela, aceitar a triagem numérica somente com pelo menos 99 atualizações efetivas e no máximo um salto; interromper e investigar três saltos consecutivos após a fase inicial, perda não finita ou parâmetros não finitos. Registrar escala, saltos iniciais e posteriores, atualizações válidas e não finitos. Se necessário, repetir exemplos de treino para completar a janela, sem contar essas atualizações como treino científico.
- **Acompanhamento das execuções científicas:** registrar os mesmos eventos desde o início; após as primeiras 20 tentativas, interromper e investigar se qualquer janela móvel completa de 100 tentativas tiver mais de um salto ou se ocorrerem três saltos consecutivos. Registrar também a fração total pós-inicial e qualquer trecho final incompleto. Uma interrupção segue a recuperação de O2 quando aprovada; não trocar precisão automaticamente.
- **Limites:** 20, 100, 1% e três são convenções práticas escolhidas para triagem, não limiares validados pela literatura nem garantia de convergência. As fontes e a justificativa estão em RESEARCH.md, R46. O diagnóstico precisa avaliar os dois modelos; passar nesse critério não prova economia de recursos ou desempenho equivalente em todas as seeds e taxas. A escolha final da precisão permanece condicionada ao diagnóstico e aos demais critérios operacionais aprovados.
- **Relação com O3:** esta decisão substitui a pendência do limite quantitativo e aplica o limite de três saltos após a fase inicial, que é registrada separadamente. O restante de O1–O9 continua pendente de confirmação conjunta.

### D45 — Escala inicial do AMP após investigação

- Após a interrupção registrada em R62 e a investigação em R63–R64, o autor autorizou investigar e ajustar a escala preservando os checkpoints originais. Usar escala inicial 16.384 para os dois modelos, tanto no diagnóstico quanto no treinamento, mantendo o critério D44.
- A escala pode alterar as atualizações do fine-tuning; não modifica os pesos pré-treinados armazenados. A mudança é uma escolha operacional baseada nas medições locais, sem garantia de estabilidade em todas as configurações.

## Resultado da revisão final do embasamento

A segunda iteração de D5 foi feita sobre o registro já revisado, sem nova busca externa nesta consolidação. RESEARCH.md, R45, mapeia D1–D43 às fontes e distingue justificativas acadêmicas de escolhas práticas. Não foi encontrada contradição que exija reabrir as escolhas científicas confirmadas. A revisão não certifica o código, não resolve empiricamente hardware/compatibilidade e não transforma evidência parcial em leitura integral dos artigos.

Lacunas preservadas e tratadas como limites: ausência de ablação direta CLS/pooler e de política de truncamento vencedora no BANKING77; procedência detalhada dos pesos atuais ainda por auditar; valores exatos de batch/precisão/tempo ainda por medir; convenção de empates da AURC proposta por dedução, sem atribuí-la a código de referência não auditado. Nenhuma dessas lacunas autoriza trocar decisões ou ampliar escopo automaticamente.

**Próximo passo efetivo:** critério quantitativo de AMP decidido em D44; obter aprovação final de O1–O9 e autorização de implementação, então começar pelo primeiro check em RED. D1–D43 permanecem válidas. Não iniciar downloads ou experimentos apenas por ter atualizado o documento.
