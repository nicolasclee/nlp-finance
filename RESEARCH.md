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

## R9 — Versões concretas de BERT e FinBERT

- **Consulta:** 2026-11-14; seleção de checkpoints comparáveis para D8.
- **Fontes:** [BERT-base-uncased](https://huggingface.co/google-bert/bert-base-uncased), [configuração BERT](https://huggingface.co/google-bert/bert-base-uncased/raw/main/config.json), [FinBERT pré-treinado HKUST](https://huggingface.co/yiyanghkust/finbert-pretrain), [configuração FinBERT](https://huggingface.co/yiyanghkust/finbert-pretrain/raw/main/config.json), [ProsusAI/finbert](https://huggingface.co/ProsusAI/finbert).
- **Verificado:** configurações dos dois candidatos MLM têm 12 camadas, dimensão 768 e 12 cabeças; vocabulários diferentes: 30.522 no BERT e 30.873 no checkpoint HKUST. Tamanhos semelhantes não isolam o efeito do corpus.
- **Verificado:** ProsusAI/finbert já inclui ajuste para sentimento com três saídas. Usá-lo incluiria histórico de ajuste supervisionado, mesmo substituindo a cabeça para intenções. Não foi selecionado.
- **Fonte acadêmica:** Yang, Uy e Huang (2020), [FinBERT: A Pretrained Language Model for Financial Communications](https://arxiv.org/html/2006.08097), §4.
- **Achado:** artigo distingue BaseVocab, continuado do BERT original por 250 mil passos, e FinVocab, treinado do zero por 1 milhão de passos. Logo, essas variantes diferem em mais que domínio. A ficha do checkpoint HKUST relata 4,9 bilhões de tokens financeiros; seu vocabulário tem tamanho compatível com FinVocab uncased, mas a correspondência completa de origem ainda exige confirmação.
- **Pendência:** localizar e verificar disponibilidade de checkpoint financeiro pré-treinado, sem ajuste de sentimento, com vocabulário e inicialização comparáveis ao BERT. Nenhum checkpoint exato foi aprovado.
- **Inferência para discussão:** priorizar continuação do BERT com vocabulário original reduz diferenças de comparação; não garante isolamento causal, pois quantidade e procedimento de pré-treinamento também podem variar.
- **Continuação da consulta (2026-11-14):** o [README oficial dos autores](https://raw.githubusercontent.com/yya518/FinBERT/master/README.md), seção de lançamento de 16/06/2020, lista quatro variantes, incluindo FinBERT-BaseVocab-Uncased, e aponta para downloads no SharePoint. O navegador de pesquisa não conseguiu acessar a pasta dessa variante; isso não prova que o download esteja indisponível. Os pesos não foram baixados nem inspecionados.
- **Fonte operacional:** [pasta oficial BaseVocab-Uncased](https://gohkust-my.sharepoint.com/:f:/g/personal/imyiyang_ust_hk/ErcYR77ZaxBAnQsmjIJF5joBapAf0HDaH0vWr_WXnoF1sA?e=oBTsSk). Formato, integridade e compatibilidade com Transformers permanecem pendentes; podem exigir conversão, a verificar antes de qualquer treinamento.
- **Proposta, não decisão:** BERT-base-uncased versus FinBERT-BaseVocab-Uncased dos autores, condicionada à validação técnica dos arquivos. Se não viável, discutir outra variante antes de mudar o desenho. Não acrescentar terceiro modelo ou pré-treinamento próprio automaticamente.

## R10 — Precedentes de comparação e alternativas de adaptação

- **Consulta:** 2026-11-14; busca direcionada por modelos comparáveis e estudos de BERT/FinBERT. Não exaustiva.
- **Fonte principal:** Peng, Chersoni, Hsu e Huang (2021), [Is Domain Adaptation Worth Your Investment? Comparing BERT and FinBERT on Financial Tasks](https://aclanthology.org/2021.econlp-1.5/), [PDF](https://aclanthology.org/2021.econlp-1.5.pdf).
- **Verificado:** resumo e introdução comparam BERT e variantes FinBERT em tarefas financeiras, incluindo sentimento, causalidade e compreensão de numerais. Relatam melhores resultados para continuação do BERT com vocabulário geral do que para a variante treinada do zero com vocabulário financeiro.
- **Limite:** resultados dessas tarefas não demonstram superioridade em BANKING77 nem fornecem controle com igual quantidade de treinamento geral adicional. Protocolo completo ainda deve ser examinado antes de adaptar hiperparâmetros.
- **Alternativa financeira localizada:** [SALT-NLP/FLANG-BERT](https://huggingface.co/SALT-NLP/FLANG-BERT), ficha dos autores verificada. Continua BERT em finanças com mascaramento preferencial de termos e expressões financeiros. Portanto, introduz mudança de estratégia de pré-treinamento além do corpus; não resolve automaticamente isolamento causal. Não selecionado; artigo e compatibilidade exata ainda pendentes.
- **Outro domínio, apenas triagem:** [BioBERT, Lee et al.](https://arxiv.org/abs/1901.08746), resumo verificado: adaptação biomédica de BERT. Trocar de domínio não elimina a questão do treinamento adicional e exigiria repensar dados e proposta; não é recomendação de substituição.
- **Conclusão da busca limitada:** não foi verificado um par público com controle financeiro versus geral de orçamento equivalente de pré-treinamento. Isso não significa que inexista. BaseVocab continua candidato mais próximo entre os já examinados, sujeito à verificação de acesso aos pesos em R9.
- **Recomendação para discussão:** manter finanças e comparar checkpoints com limitações explícitas; usar o precedente de Peng et al. para motivar a escolha das variantes, sem transformar comparação empírica em prova causal.
- **Acompanhamento:** dúvidas docentes em QUESTIONS_FOR_PROFESSOR.md; orientação atual em PLAN.md, D9. Nenhuma troca de modelo aprovada nesta pesquisa.

## R11 — Como controlar fatores na adaptação de domínio

- **Consulta:** 2026-11-14; pergunta do autor sobre comparação empírica versus explicação causal.
- **Fonte:** Gururangan et al. (2020), [Don’t Stop Pretraining: Adapt Language Models to Domains and Tasks](https://aclanthology.org/2020.acl-main.740/), [PDF](https://aclanthology.org/2020.acl-main.740.pdf).
- **Verificado:** §3.3 e tabela 3 comparam RoBERTa, adaptação no domínio relevante e adaptação em domínio irrelevante; reportam média e desvio em cinco seeds. O controle adicional investiga se os ganhos vêm apenas de continuar treinando. Isso vai além de listar limitações.
- **Limite:** não assumir igualdade exata de tokens e orçamento em todas as condições sem auditar apêndices. Não é experimento financeiro e não resolve fatores de nossos checkpoints disponíveis.

## R12 — Orçamento de busca como fator de comparação

- **Consulta:** 2026-11-14.
- **Fonte:** Dodge et al. (2019), [Show Your Work: Improved Reporting of Experimental Results](https://aclanthology.org/D19-1224/), [PDF](https://aclanthology.org/D19-1224.pdf).
- **Verificado:** resumo e formulação da avaliação por orçamento: conclusões sobre modelos podem mudar com o investimento em busca de hiperparâmetros. Propõe reportar desempenho de validação em função do orçamento computacional, além do teste.
- **Aplicação proposta:** definir e registrar orçamento de busca comparável, critério de seleção e tentativas realizadas; mesmos valores de hiperparâmetros não significam automaticamente comparação justa.
- **Limite:** não remove diferenças históricas de pré-treinamento. Orçamento e busca deste projeto ainda não foram definidos.

## R10 — Complemento de leitura metodológica

- **Consulta adicional:** 2026-11-14, Peng et al. (2021), §3.2 e parágrafo anterior a §4.
- **Verificado:** compara checkpoints BERT/FinBERT com mesma forma de cabeça linear, softmax e cross-entropy. Relata médias de dez execuções, além de validação cruzada em datasets sem split oficial. Distingue históricos das variantes.
- **Limite:** esse protocolo permite comparação de sistemas; não constitui controle isolado de corpus, quantidade de pré-treinamento e vocabulário.

## Síntese metodológica para discussão — 2026-11-14

- Comparação de sistemas pergunta qual combinação de checkpoint e procedimento funciona melhor na tarefa. Controle de dados e avaliação reduz fontes evitáveis de diferença sem apagar os históricos dos checkpoints.
- Investigação de causas exige intervenções e controles dirigidos: partir de um checkpoint comum, manter fatores definidos e variar o aspecto estudado; incluir controle de treinamento adicional fora do domínio ajuda a separar efeito de mais treinamento de relevância do domínio (R11).
- Ablação remove ou troca um componente para estudar sua contribuição sob aquelas condições. Vários componentes que interagem podem exigir combinações adicionais; uma única troca não explica tudo.
- Repetições e intervalos quantificam variação amostral/aleatória; não eliminam confundimento de vocabulário ou corpus. Normalizar métricas também não elimina esse confundimento.
- Treinar do zero não é requisito universal nem solução automática: é preciso controlar corpus, tokens, objetivos e demais condições, e repetições continuam relevantes.
- Recomendações, ainda não decisões: comparar checkpoints com protocolo de fine-tuning explícito e orçamento comparável, medir variação e limitar conclusões ao efeito do sistema completo. Adicionar controles de pré-treinamento somente se a pergunta causal justificar o custo e o autor aprovar.
- Nenhuma mudança de escopo, seed, orçamento ou treinamento próprio foi aprovada com esta revisão.

## R13 — Verificação operacional do BaseVocab-Uncased

- **Consulta:** 2026-11-14, solicitada pelo autor para resolver a escolha de checkpoints com fatos. Inspeção de arquivos; nenhum treinamento ou implementação do projeto.
- **Oficial:** requisição HTTP ao link SharePoint de R9, fora da restrição de rede, redirecionou à pasta nominal BaseVocab-Uncased e retornou diagnóstico de acesso negado/exigência de autenticação. Não concluir que os arquivos foram apagados; não foi possível obter os pesos oficiais anonimamente nesta consulta.
- **Cópia localizada:** [radmada/FinBERT-BaseVocab-Uncased](https://huggingface.co/radmada/FinBERT-BaseVocab-Uncased), mantida por terceiro, não pelos autores originais. [API consultada](https://huggingface.co/api/models/radmada/FinBERT-BaseVocab-Uncased).
- **Revisão examinada:** `74c4976d78040f07ed8e987f2588f4a63990b629`. API informa repositório público, sem gate. Arquivos: README.md, config.json, vocab.txt e pytorch_model.bin.
- **Configuração lida:** 12 camadas, dimensão 768, 12 cabeças, vocabulário 30.522. Não contém model_type ou architectures; carregamento por classes automáticas não foi comprovado. Possível necessidade de usar classe BERT explícita ou adaptar configuração, a verificar.
- **Vocabulário verificado byte a byte:** idêntico ao vocab.txt de google-bert/bert-base-uncased consultado. SHA-256 dos dois: `07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3`. Isso verifica tokenização no nível do catálogo, não todos os parâmetros do tokenizer.
- **Pesos baixados integralmente em /tmp:** 440.472.039 bytes. SHA-256 `5f88f5cd36ae1256392d23ceabd667ce831419e141da4db4c3c61db7e7245ae3`, igual ao LFS oid informado pela API do repositório. Garante correspondência ao arquivo hospedado, não aos pesos originais dos autores.
- **Inspeção estática:** serialização PyTorch/pickle legada; opcodes examinados com pickletools, sem desserializar ou executar o objeto. Encontrados nomes de embeddings, encoder até camada 11, pooler, cls.predictions e cls.seq_relationship; não foram encontrados nomes classifier.* nessa estrutura. Estrutura compatível com pré-treinamento BERT; não prova histórico de treinamento ou qualidade dos tensores.
- **Origem não comprovada:** README cita Yang et al., mas o exemplo de uso aponta para outro modelo, yiyanghkust/finbert-tone. Não documenta conversão ou fornece hash verificável do original. Nenhum confronto com pesos oficiais foi possível.
- **Limite de teste:** torch, transformers e numpy não estão instalados no ambiente consultado. Não foi realizado carregamento funcional nem forward pass; integridade criptográfica e inspeção de estrutura não equivalem a teste de execução.
- **Conclusão factual:** existe uma cópia descarregável, com configuração e vocabulário compatíveis com BaseVocab-Uncased; procedência e carregamento funcional não ficaram comprovados. Não registrar o par como tecnicamente validado de ponta a ponta.
- **Alternativa já documentada:** yiyanghkust/finbert-pretrain é apontado pelo repositório dos autores (R9), oferecendo origem documental mais direta, porém com vocabulário diferente e menor isolamento das causas. Nenhuma troca foi aprovada.

## R14 — Representações congeladas versus ajuste completo

- **Consulta:** 2026-11-14; autor pediu explicação técnica e questão ao professor, sem autorizar implementação.
- **Fonte acadêmica:** Devlin et al. (2019), [BERT](https://aclanthology.org/N19-1423.pdf), §3 e §5.3. Verificado: distingue atualização de todos os parâmetros de uso de representações fixas; estuda ambas em NER. Seus resultados não demonstram qual será melhor em BANKING77 nem que qualquer saída sobre CLS seja a melhor opção congelada.
- **Fonte técnica:** [PyTorch, Autograd mechanics](https://docs.pytorch.org/docs/2.15/notes/autograd.html), seções Setting requires_grad e Evaluation Mode. Verificado: requires_grad controla cálculo de gradientes; eval controla comportamento de módulos como dropout e não congela pesos por si só.
- **Interpretação para o desenho:** D11 congela o classificador ao comparar regras após treinamento, não exige encoder congelado durante treinamento. Original do checkpoint pode ser preservado em ambos os regimes. Estratégia ainda em discussão; detalhes em QUESTIONS_FOR_PROFESSOR.md, Q4.
- **Cálculo próprio:** saída linear 768 → 77 com viés tem 768 × 77 + 77 = 59.213 parâmetros. Pooling, cabeça e regime ainda não confirmados.

## R15 — Comparação direta de regimes no BANKING77

- **Consulta:** 2026-11-14; complemento de R1, Casanueva et al. (2020), [PDF](https://aclanthology.org/2020.nlp4convai-1.5.pdf), §4 e tabela 3.
- **Verificado:** avalia BERT-FIXED e BERT-TUNED; BANKING77 completo: 87,19% e 93,66% de acurácia. Usa BERT-large cased; FIXED emprega média dos vetores de tokens, TUNED usa CLS e adapta toda a rede.
- **Limite:** compara configurações completas, não apenas congelamento; pooling e cabeça diferem. Não transportar números ao nosso BERT-base/FinBERT ou à abstenção.
- **Inferência prática:** ambas têm precedente direto; ajuste completo tem evidência favorável nesse protocolo. Não é levantamento de prevalência na literatura nem garantia de superioridade no projeto.

## R16 — Tradeoffs de extração fixa e fine-tuning

- **Consulta:** 2026-11-14.
- **Fonte:** Peters, Ruder e Smith (2019), [To Tune or Not to Tune? Adapting Pretrained Representations to Diverse Tasks](https://aclanthology.org/W19-4302/), [PDF](https://aclanthology.org/W19-4302.pdf).
- **Verificado:** resumo, introdução e orientações discutem extração congelada e ajuste completo com BERT/ELMo em sete tarefas. Resultados dependem da relação entre pré-treinamento e tarefa; extração permite pré-computar representações, enquanto ajuste adapta a representação. Não há vencedor universal.
- **Limite:** não é BANKING77 nem estudo de FinBERT. Não mede prevalência atual das estratégias. Escolha de pooling/cabeça importa para a abordagem congelada.
- **Recomendação para discussão:** considerar fine-tuning completo como regime principal pela proximidade com proposta e precedente BANKING77, condicionado ao diagnóstico de recursos. Congelamento continua alternativa válida para estudar representações prontas; não acrescentar ambos automaticamente.
- **Atualização posterior:** autor confirmou fine-tuning completo em PLAN.md, D13. Q4 preservada como histórico; não incluir encoder congelado como condição experimental sem nova aprovação.

## Síntese e pendências (gerais, após comparação dos regimes)

- **Fundamentado em precedente:** rejeição pela maior saída softmax em um classificador já treinado (R2); divisão de validação a partir do treino oficial do BANKING77 (R3–R4).
- **Lacuna resolvida em 2026-11-14:** R8 define e compara exatamente a diferença entre as duas maiores probabilidades escolhida em D3. Isso resolve o precedente metodológico, não sua eficácia no BANKING77. Margens sobre logits ou distâncias não são automaticamente equivalentes.
- **Ainda aberto:** objetivo para selecionar limiares, avaliação de incerteza, proporção de validação e possível separação adicional de dados para limiares.
- **Correção da sugestão inicial:** 20% foi heurística da IA, sem justificativa específica encontrada para este estudo; 10% possui precedentes, mas não está aprovado e não é uma proporção comprovadamente ótima.
- **Distinção central:** no desenho pós-treinamento discutido, limiares não alteram pesos nem acurácia sobre todos os exemplos; alteram cobertura e erro entre os aceitos.
- **Próximo trabalho:** concluir revisão direcionada de critérios e seleção de limiares, distinguindo avaliação empírica de garantias estatísticas; depois retomar decisões com o autor.

## R17 — CLS e saída para classificação

- **Consulta:** 2026-11-14; explicação solicitada pelo autor, com referência para futura metodologia do artigo.
- **Fonte:** Devlin et al. (2019), [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://aclanthology.org/N19-1423/), [PDF](https://aclanthology.org/N19-1423.pdf), §3.2 e §4.1.
- **Verificado:** usa representação final de CLS como entrada da saída classificadora, ajustando parâmetros de ponta a ponta; saída com dimensão correspondente ao número de rótulos. Precedente metodológico, não prova de melhor pooling no BANKING77.
- **Explicação para o projeto:** tokens são processados pelo encoder; a representação contextual de CLS pode alimentar a saída para 77 intenções. Logits tornam-se pontuações softmax para previsão e abstenção. No ajuste completo, erro supervisionado atualiza saída e encoder.
- **Cuidado:** CLS não constitui um resumo semanticamente perfeito por definição. Sua utilidade para a tarefa é aprendida; vetores finais de CLS e pooler_output não devem ser tratados como idênticos.
- **Atualização:** após as explicações, o autor confirmou CLS e camada linear, softmax e entropia cruzada em PLAN.md, D14. Pooler e dropout permanecem abertos. Nenhuma implementação autorizada.

## R18 — Alternativas à cabeça linear e notas técnicas

- **Consulta:** 2026-11-14; curiosidade do autor sobre alternativas acadêmicas, sem pedido de ampliar o experimento.
- **Fonte:** Mehri e Eric (2021), [Example-Driven Intent Prediction with Observers](https://aclanthology.org/2021.naacl-main.237/), [PDF](https://aclanthology.org/2021.naacl-main.237.pdf). Resumo verificado: classifica por comparação com exemplos e propõe observers como alternativa representacional; avalia BANKING77, CLINC150 e HWU64. Não assumir que o método seja simplesmente vizinho mais próximo por cosseno sem examinar detalhes.
- **Fonte:** Reimers e Gurevych (2019), [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://aclanthology.org/D19-1410/). Resumo verificado: aprende embeddings de sentenças para comparação por cosseno. É precedente para similaridade, não resultado direto para nosso par no BANKING77.
- **Explicações técnicas:** salvas em LEARNING_NOTES.md: logits, softmax, cabeça linear, dimensões e diferença em relação à busca por similaridade.
- **Interpretação:** cabeça linear tem precedente direto no BERT (R17) e BERT-TUNED/BANKING77 (R15); existem alternativas publicadas, sem necessidade de incluir novas condições no estudo. Não foi feito levantamento quantitativo de prevalência.
- **Atualização:** cabeça linear confirmada em D14; alternativas discutidas apenas por curiosidade não foram incluídas. Nenhuma implementação.

## R19 — Métricas para classificação e geração

- **Consulta:** 2026-11-14; autor pediu revisão e justificativa de acurácia/Macro-F1 versus recall, F1 e ROUGE.
- **Fontes técnicas verificadas:** [scikit-learn, avaliação](https://scikit-learn.org/stable/modules/model_evaluation.html), [precision_recall_fscore_support](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html), [classification_report](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html). Distinguem métricas por classe, médias macro/micro/ponderada e acurácia. Precisão e recall podem ser mantidos para diagnóstico por intenção, sem tornar cada agregado uma métrica principal.
- **Fonte acadêmica:** Lin (2004), [ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/), [PDF](https://aclanthology.org/W04-1013.pdf), resumo e §1 verificados: comparação de textos por sobreposição de unidades. Não mede diretamente acerto de rótulos discretos.
- **Justificativa proposta:** acurácia para acerto global e comparabilidade com R15; Macro-F1 para combinar precisão/recall dando peso igual às intenções. F1 micro é redundante com acurácia quando todas as classes são incluídas na classificação multiclasse de rótulo único, sem abstenção.
- **Limites:** Macro-F1 não substitui diagnóstico por classe nem considera custos financeiros diferentes. Métricas de classificação sem abstenção não substituem cobertura e erro seletivo de D6. Casos sem predições por classe e zero_division ainda precisarão de convenção explícita.
- **Atualização:** autor confirmou acurácia, Macro-F1 e diagnóstico por intenção em PLAN.md, D15. Métricas adicionais exigem decisão separada.

## R20 — Métricas adicionais em tarefas próximas

- **Consulta:** 2026-11-14; pesquisa complementar autorizada após D15. Foco: classificação NLP com rejeição, QA seletivo e calibração; não foi encontrada nesta busca uma comparação acadêmica exatamente igual ao nosso par no BANKING77.
- **Xin et al. (2021):** [The Art of Abstention: Selective Prediction and Error Regularization for Natural Language Processing](https://aclanthology.org/2021.acl-long.84.pdf), §3.1 e tabelas 3–4 verificados. Compara Transformers em classificação textual usando área sob curva risco-cobertura (denominada AUC no artigo) e RPP, proporção de pares com ordenação confiança/erro invertida. Menor é melhor. Não confundir essa AUC com AUROC.
- **Kamath, Jia e Liang (2020):** [Selective Question Answering under Domain Shift](https://aclanthology.org/2020.acl-main.503.pdf), §3.1 verificado. Usa área risco-cobertura e cobertura máxima em determinado nível de risco. É precedente para avaliação seletiva, não proposta de acrescentar QA ou mudança de domínio ao nosso experimento. Fronteira descritiva não equivale ao desempenho de limiar escolhido na validação e congelado no teste.
- **Guo et al. (2017):** [On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a/guo17a.pdf), seção de calibração verificada. Usa diagramas de confiabilidade e ECE, diferença agregada entre confiança e acurácia por faixas; também discute NLL e MCE. Calibração não equivale a qualidade da ordenação para abstenção. Margem softmax não deve ser tratada automaticamente como probabilidade de acerto ao calcular ECE.
- **Traub et al. (2024), triagem:** [Overcoming Common Flaws in the Evaluation of Selective Classification Systems](https://arxiv.org/abs/2407.01032). Trabalho localizado sobre limitações de métricas e AUGRC; leitura do método ainda pendente. Não adotar essa métrica por resumo.
- **Complemento já consultado:** R8 discute AURC e formas normalizadas. Área bruta pode refletir diferenças de qualidade dos classificadores além do sinal de confiança; não atribuir toda diferença de área ao critério de abstenção.
- **Atualização:** autor confirmou AURC em PLAN.md, D16, junto às curvas já aprovadas, e ECE como diagnóstico secundário em D17, sem técnica corretiva de calibração. Definições de cálculo serão fixadas antes da implementação. RPP e outras áreas não integram o escopo aprovado.

## R21 — Reutilização de validação e viés de seleção

- **Consulta:** 2026-11-14; autor questionou se D18 equivale a favorecer artificialmente o modelo.
- **Fonte acadêmica:** Cawley e Talbot (2010), [On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation](https://jmlr.org/papers/v11/cawley10a.html), [PDF](https://jmlr.org/papers/volume11/cawley10a/cawley10a.pdf). Resumo e introdução verificados: o critério de seleção também pode sofrer overfitting; avaliar e selecionar usando os mesmos resultados produz viés. Discute avaliação mais rigorosa, inclusive validação cruzada aninhada.
- **Fonte operacional:** [scikit-learn, cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html), introdução verificada: validação orienta escolhas e teste separado avalia o resultado; CV pode aproveitar dados com custo computacional maior.
- **Distinção para D18:** selecionar versão e limiares na mesma validação faz parte do desenvolvimento de um pipeline; resultados dessa validação não são avaliação independente. Avaliar o pipeline congelado em teste intocado é diferente de anunciar a melhor validação como resultado final.
- **Limite:** teste separado não torna as escolhas imunes a overfitting nem certifica erro máximo. Reutilizar teste para alterar configurações, escolher seeds ou ajustar regras o transforma em informação de desenvolvimento.
- **Possíveis controles, ainda não novos compromissos:** definir busca e critérios antes de executar; registrar tentativas; limitar adaptação manual; usar teste apenas após congelar o protocolo. Alternativas mais custosas incluem divisão adicional para limiares ou CV aninhada.
- **Situação:** D18 permanece registrada; autor pediu esclarecimento, não revogou a escolha. Não atribuir à literatura prova de superioridade da validação compartilhada. Orçamento e critério de seleção precisam ser fechados antes da execução.

## R22 — Reavaliação da divisão conforme tamanho e protocolos publicados

- **Consulta:** 2026-11-14, a pedido do autor; rechecagem de R3–R5 e R8.
- **BANKING77:** TK-KNN, [§4.1 e tabela 1](https://aclanthology.org/2023.findings-emnlp.429.pdf), confirma 9.002 treino, 1.001 validação, 3.080 teste; artigo de [Soft Clustering, apêndice B](https://aclanthology.org/2024.findings-emnlp.758.pdf), confirma treino oficial dividido em 90/10. Precedentes para tamanho de validação, não prova de adequação da mesma validação à seleção de nossos limiares.
- **Classificação seletiva:** [benchmark, §5.1](https://arxiv.org/html/2401.12708v2) usa treino/calibração/validação/teste 60/10/10/20 em imagens e tabelas; documenta que separar funções é alternativa publicada, sem estabelecer superioridade aqui.
- **Eficiência de dados:** [Cattelan e Silva, apêndice E](https://arxiv.org/html/2305.15508v4) avalia ajuste pós-treinamento em amostras menores e discute maior vulnerabilidade ao overfitting com mais ajustes e menos dados. Não transportar suficiência de amostras ImageNet para BANKING77.
- **Cálculo ilustrativo próprio:** 1.000 exemplos correspondem a cerca de 13 por intenção em média; dividir igualmente em dois grupos dá cerca de 6,5 por intenção em cada. Distribuição real deve ser verificada. Esses tamanhos não garantem erro estável por classe.
- **Cálculo ilustrativo próprio:** com cobertura de 80% numa amostra de 1.000, há 800 aceitos; cada erro altera a taxa em 0,125 ponto percentual. Com 500 exemplos, restam 400 aceitos e cada erro altera em 0,25 ponto. Taxa hipotética de 1% corresponde a 8 ou 4 erros, respectivamente. Não é previsão de desempenho nem intervalo de confiança.
- **Avaliação:** tamanho é plausível para comparação global exploratória com busca pequena, mas não permite garantir estabilidade de limiares, detectar ganhos mínimos ou certificar erros raros. Curvas de cobertura muito baixa, ECE com faixas pequenas e análises por classe são especialmente sensíveis.
- **Recomendação:** manter D18 e considerar validação estratificada de aproximadamente 10% do treino oficial, com base em precedente e limitação de fragmentação. Percentual ainda não aprovado; não afirmar que risco de seleção é insignificante sem resultados. Preservar teste oficial e discutir incerteza/repetições no protocolo.
- **Atualização posterior:** autor confirmou aproximadamente 10% do treino oficial para validação estratificada compartilhada, preservando teste oficial (PLAN.md, D19). Precedente de proporção não implica garantia de estabilidade de limiares.

## R23 — Macro-F1 como critério de seleção na validação

- **Consulta:** 2026-11-14; autor condicionou aprovação à fundamentação acadêmica. Buscou-se uso na seleção/parada, não apenas reporte final.
- **Precedente explícito:** Sadat e Caragea (2024), [MSCINLI: A Diverse Benchmark for Scientific Natural Language Inference](https://aclanthology.org/2024.naacl-long.90.pdf), apêndice sobre configuração, especialmente p. 1629. Usa Macro-F1 do desenvolvimento como critério de early stopping no fine-tuning das tarefas posteriores, incluindo classificação de intenção de citação (ACL-ARC). Não é intenção bancária nem demonstra optimalidade no BANKING77.
- **Precedente complementar:** Ghosal et al. (2021), [Exploring the Role of Context in Utterance-level Emotion, Act and Intent Classification in Conversations](https://aclanthology.org/2021.findings-acl.124.pdf), legendas das tabelas 2 e 10. Reporta teste no ponto de melhor F1 de validação; agrega por macro ou por frequência conforme tarefa. Sustenta selecionar por F1 de validação, mas não chamar o F1 de MultiWOZ de Macro-F1: ali é ponderado.
- **Justificativa própria:** maior Macro-F1 na validação alinha seleção ao peso igual das 77 intenções definido em D15; evita alternar retrospectivamente entre métricas para escolher vencedores.
- **Limite:** não foi verificado nesta busca precedente exato do mesmo par no BANKING77 selecionado por Macro-F1. R15 usa acurácia como medida principal. Evidência encontrada fundamenta a prática, não obriga a métrica ou garante que maximiza AURC.
- **Situação:** aprovação condicional do autor aplicada ao critério em D20 com esses limites explícitos. Frequência de avaliação, early stopping, paciência e desempate ainda não definidos.

## R24 — Comparação crítica de Macro-F1 versus acurácia

- **Consulta:** 2026-11-14. Autor solicitou comparar fundamentos, pois R23 demonstra precedente de uso, não preferência justificada sobre acurácia.
- **Referência de acurácia no dataset:** Casanueva et al. (2020), [§4 e tabela 3](https://aclanthology.org/2020.nlp4convai-1.5.pdf), reportam acurácia nas comparações BANKING77. Isso é precedente de avaliação, não comprovação de seleção por acurácia na validação.
- **Distribuição e comparação prática:** Loukas et al. (2023), [Making LLMs Worth Every Penny](https://stogiannidis.github.io/files/LLMPenny.pdf), nota 1 e tabelas 3–4, confirma teste com 40 exemplos por rótulo e reporta Micro-F1/Macro-F1. Exemplos publicados: MPNet completo 94,1/94,1 e SetFit 20-shot 91,2/91,3. Mostra possível proximidade, sem garantir mesma ordenação entre nossos checkpoints ou superioridade de uma métrica na seleção.
- **Análise conceitual:** Opitz (2024), [A Closer Look at Classification Evaluation Metrics and a Critical Reflection of Common Evaluation Practice](https://aclanthology.org/2024.tacl-1.46.pdf), §4.1 e §4.4 verificados. Acurácia conta predições corretas; Macro-F1 combina precisão/recall por classe. Média igual dos F1 não torna a métrica invariável à distribuição dos rótulos. Motivação de escolha deve ir além de frequência de uso.
- **Definição de Macro-F1:** Opitz e Burst (2021, revisão de nota de 2019), [Macro F1 and Macro F1](https://arxiv.org/html/1911.03347v3), §1 verificado. Distingue média dos F1 por classe de F1 das médias de precisão/recall; fórmulas podem mudar rankings. Neste projeto, Macro-F1 discutido significa média aritmética dos F1 por intenção, conforme D15 e explicação prévia.
- **Limite de acesso:** Sokolova e Lapalme (2009), artigo de análise de métricas, localizado em busca; PDF no site dos autores bloqueado por proteção de acesso. Não usar trechos não verificados para conclusões novas.
- **Derivação própria:** com mesmo número de exemplos verdadeiros por classe, acurácia equivale ao recall médio por classe. Logo, no teste balanceado, já agrega recuperação com peso igual das intenções. Isso não torna acurácia igual a Macro-F1, pois a precisão depende de como as previsões se distribuem. A validação estratificada conserva aproximadamente proporções do treino, não necessariamente 40 exemplos ou igualdade por classe.
- **Exemplo matemático próprio:** duas classes com dez exemplos cada. Confusões [[8,2],[2,8]] e [[10,0],[4,6]] têm ambas acurácia 80%, mas Macro-F1 80% e aproximadamente 79,17%. Mesmo balanceamento não torna métricas idênticas.
- **Conclusão da revisão:** evidência não estabelece superioridade universal de Macro-F1 para seleção. R23 sustenta legitimidade, não optimalidade. Acurácia responde diretamente a acerto de encaminhamento com custos iguais, aproxima o objetivo de erro 0/1 de D6 e facilita comparação com R15; Macro-F1 complementa o diagnóstico de precisão/recall entre intenções.
- **Recomendação atual, não decisão:** considerar acurácia como critério de seleção e manter Macro-F1 no reporte e diagnóstico. Alternativamente, manter D20 se o autor priorizar explicitamente o equilíbrio precisão/recall por classe. Não testar critérios no teste final para escolher o vencedor.
- **Atualização posterior:** autor confirmou trocar a seleção para acurácia; D20 revisada. D15 (reportar ambas) continua válida. Combinação de métricas ou desempate por Macro-F1 não foram aprovados.

## R25 — Orçamento de duas configurações e três repetições

- **Consulta:** 2026-11-14; autor aprovou orçamento proposto, pedindo verificação acadêmica antes do registro definitivo.
- **Precedente de três seeds no mesmo dataset:** Yin et al. (2021), [BatchMixup: Improving Training by Interpolating Hidden States of the Entire Mini-batch](https://aclanthology.org/2021.findings-acl.434.pdf), §5 e legenda da tabela 1 verificados: resultados de BANKING77 e outras tarefas são médias de três sementes aleatórias. Modelo e objetivo diferem; não adotar mixup ou RoBERTa por essa referência.
- **Comparação de rigor:** Botzer et al. (2023), [TK-KNN, §4.1](https://aclanthology.org/2023.findings-emnlp.429.pdf), usa cinco seeds; R10 documenta dez execuções em comparação BERT/FinBERT. Não há um número universal ideal demonstrado para nosso projeto.
- **Por que repetir:** Dodge et al. (2020), [Fine-Tuning Pretrained Language Models: Weight Initializations, Data Orders, and Early Stopping](https://arxiv.org/abs/2002.06305), resumo verificado: seeds afetam inicialização e ordem de dados, podendo produzir diferenças importantes. Não prova suficiência de três repetições.
- **Busca de configurações:** R12 fundamenta transparência e comparação por orçamento. Duas configurações são um limite prático compatível com o prazo, não uma quantidade comprovadamente suficiente para encontrar o melhor hiperparâmetro. A busca será restrita e não exaustiva, sem alegação de optimalidade.
- **Conclusão:** três repetições têm precedente direto em BANKING77 e permitem observar alguma variação, mas oferecem estimativa de variabilidade limitada e não garantem poder para diferenças pequenas. O total de 12 execuções é orçamento planejado, cuja duração depende de D7.
- **Pendências:** valores das configurações/seeds, agregação para escolher configuração, reporte da dispersão e critérios de viabilidade do diagnóstico. Não selecionar apenas a melhor seed.

## R26 — Variar taxa de aprendizado no fine-tuning

- **Consulta:** 2026-11-14; autor pediu verificar se variar taxa é prática acadêmica adequada antes de confirmar os valores.
- **Precedente BERT:** Devlin et al. (2019), [§4.1 e apêndice A.3](https://aclanthology.org/N19-1423.pdf), verificados. Seleciona taxa pela validação; §4.1 testa 2e-5, 3e-5, 4e-5, 5e-5; A.3 recomenda explorar 2e-5, 3e-5, 5e-5 e informa dependência da tarefa. Dá fundamento aos candidatos 2e-5/5e-5, não à suficiência de apenas dois pontos no BANKING77/FinBERT.
- **Estudo de HPO:** Liu e Wang (2021), [An Empirical Study on Hyperparameter Optimization for Fine-Tuning Pre-trained Language Models](https://aclanthology.org/2021.acl-long.178.pdf), tabela 1 e §5.1 verificados. Inclui taxa nos espaços de busca de ELECTRA/RoBERTa e considera restringir exploração a taxa, ou taxa e batch size. Demonstra precedente para busca limitada, sem provar optimalidade da nossa grade.
- **Precedente adicional para D20:** o mesmo estudo, §3, seleciona checkpoint de melhor acurácia de validação; evidencia uso efetivo na seleção, além do reporte de acurácia já registrado em R24.
- **Triagem de estabilidade:** Mosbach et al. (2021), On the Stability of Fine-Tuning BERT, localizado; PDF OpenReview bloqueado por verificação. Não usar conclusões detalhadas não verificadas para definir nossa faixa.
- **Comparação financeira:** Peng et al. (R10) foi reconsultado; não foi localizado um espaço explícito de busca de taxas no trecho inspecionado. Não atribuir a ele nossa grade.
- **Interpretação:** variar taxa é ajuste de hiperparâmetro, não nova contribuição central. Mesmos dois candidatos e orçamento por modelo permitem ajuste limitado; demais fatores fixos entre A/B tornam essa busca mais interpretável. Taxa pode interagir com scheduler, batch size, otimizador e épocas, ainda não definidos.
- **Atualização:** autor confirmou 2e-5 e 5e-5 em PLAN.md, D23. Demais configurações permanecem abertas.

## R27 — Cinco épocas e seleção por época

- **Consulta:** 2026-11-14; autor aprovou protocolo condicionado à sustentação na literatura.
- **Precedente direto:** Casanueva et al. (2020), [§4](https://aclanthology.org/2020.nlp4convai-1.5.pdf), especifica 50, 18 e 5 épocas para BERT-TUNED em 10 exemplos/classe, 30 exemplos/classe e treino completo. Usa BERT-large cased e taxa 4e-4; não transferir sua alegação de convergência automaticamente aos nossos checkpoints, taxas e subconjunto de treino.
- **Contexto:** Devlin et al. (2019), [apêndice A.3](https://aclanthology.org/N19-1423.pdf), explora 2–4 épocas e indica dependência da tarefa. Isso sustenta durações curtas como candidatas, não consenso de que exatamente cinco seja ótimo.
- **Escolhas do projeto:** avaliar ao final de cada época e reter o melhor checkpoint usa D20–D21, controlando a avaliação final sem obrigar uso do último estado. Executar cinco épocas sem early stopping é orçamento fixo, não garantia contra overfitting ou não convergência. Frequência por época é decisão operacional, não exigência do artigo BANKING77.
- **Diagnóstico:** inspecionar duração, memória e curvas de treino/validação. Se o melhor ponto ficar no limite e a validação ainda melhorar, documentar limitação de duração; não prolongar automaticamente ou consultar teste para decidir.
- **Conclusão:** há precedente próximo para cinco épocas, suficiente para justificar um orçamento inicial condicionado ao diagnóstico, não para afirmar optimalidade ou estabilidade garantidas.

## R28 — Otimizador e regularização

- **Consulta:** 2026-11-14; definição da configuração comum de otimização.
- **Fonte metodológica:** Loshchilov e Hutter (2019), [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101), resumo verificado. AdamW desacopla weight decay da atualização adaptativa de Adam. Não afirmar equivalência automática a penalização L2 em Adam.
- **Precedente de tarefa:** Botzer et al. (2023), [TK-KNN, §4.3](https://aclanthology.org/2023.findings-emnlp.429.pdf), usa AdamW com BERT-base em classificação de intenções incluindo BANKING77. Não importar batch size, ciclos semissupervisionados ou taxa do artigo automaticamente.
- **Valor de regularização:** Devlin et al. (2019), [apêndices A.2–A.3](https://aclanthology.org/N19-1423.pdf), documenta weight decay 0,01 no pré-treinamento e manutenção da maioria dos hiperparâmetros no ajuste. É precedente de valor, não prova de optimalidade para nossos checkpoints.
- **Atualização:** autor confirmou AdamW e weight_decay=0,01 como configuração fixa comum em PLAN.md, D25, após explicação introdutória. Valores de beta/epsilon, política de bias/LayerNorm, scheduler e warmup ainda não definidos.

## R29 — Warmup e redução linear da taxa

- **Consulta:** 2026-11-14; próximo ponto proposto após D25.
- **Fontes primárias:** [run_classifier.py oficial do BERT](https://raw.githubusercontent.com/google-research/bert/master/run_classifier.py), flags learning_rate e warmup_proportion; [optimization.py](https://raw.githubusercontent.com/google-research/bert/master/optimization.py), create_optimizer. Trechos verificados: padrão de warmup_proportion=0,1 e mecanismo de aquecimento linear e redução linear da taxa até zero.
- **Limite:** código TensorFlow histórico serve de precedente, não será copiado literalmente. Seu decay é parametrizado pelo total de passos; uma implementação moderna com decaimento após warmup não é reprodução numérica exata desse código. Não importar otimizador sem correção de viés ou epsilon silenciosamente.
- **Proposta:** warmup linear nos primeiros 10% dos passos de atualização, seguido por decaimento linear até zero no restante. D23 define o pico da taxa, não uma taxa constante. Mesma regra nos dois modelos/configurações.
- **Motivo prático:** iniciar com atualizações menores e reduzi-las ao fim; não garante estabilidade ou melhor desempenho. Não adiciona execuções ao orçamento.
- **Atualização:** autor confirmou o esquema em PLAN.md, D26. Arredondamento do número de passos e relação com batch size/acumulação ainda pendentes. Mudança de cinco para três épocas também altera duração do scheduler e não é simples corte de um treinamento idêntico.

## R30 — Batch size e RTX 3070 Ti de notebook

- **Consulta:** 2026-11-14; autor pediu investigar batch ideal para seu hardware antes de aprovar batch 16.
- **Hardware, fonte primária:** [ASUS, Zephyrus M16 2022](https://rog.asus.com/us/laptops/rog-zephyrus/rog-zephyrus-m16-2022-series/spec/) lista variante RTX 3070 Ti Laptop com 8 GB GDDR6. Identificação da variante e memória livre do notebook do autor ainda não verificadas localmente.
- **Treinamento, fonte oficial:** [Hugging Face, treinamento em uma GPU](https://huggingface.co/docs/transformers/v4.42.4/perf_train_gpu_one) e [anatomia de memória](https://huggingface.co/docs/transformers/v5.7.0/en/model_memory_anatomy) descrevem dependência de batch size, ativações, sequência e precisão. Não foi verificado benchmark reproduzível do nosso par, com mesma sequência/precisão, nesse notebook.
- **Distinção:** maior batch que cabe na memória, batch com maior throughput e batch com melhor generalização são objetivos diferentes. Modelo de GPU sozinho não determina os três.
- **Proposta aberta:** no diagnóstico, comparar poucos batches candidatos (por exemplo 8, 16, 32), com mesma sequência e precisão, medindo memória máxima e exemplos/s com forward, backward e atualização AdamW. Escolher regra técnica comum aos dois modelos, com margem de memória, antes dos treinamentos completos. Valores e regra ainda não aprovados; não ampliar automaticamente a busca científica de D22.
- **Limites:** inferência não estima memória completa de treinamento; precisão mista não garante economia em toda configuração; maior batch não é automaticamente mais rápido. Batch altera número de atualizações por época e scheduler, exigindo definição antes da execução científica.
- **Atualização:** autor confirmou escolher batch pelo diagnóstico comparando 8, 16 e 32 (PLAN.md, D27), e pediu agrupar com épocas e outros itens dependentes de hardware. Seção de diagnóstico adicionada ao plano. Batch final não escolhido; nenhuma medição ou novo download de pesos realizado nesta consulta.

## R31 — Limites de 64 e 128 tokens: precedentes e limites de transferência

- **Consulta:** 2026-11-14. Autor autorizou verificar os precedentes mencionados anteriormente e acrescentar fundamentação à decisão D28, já confirmada: medir antes de escolher entre 64 e 128 tokens, em conjunto com o diagnóstico.
- **Pergunta:** quais fontes primárias documentam esses valores e em que etapa experimental são usados? Pesquisa dirigida, não revisão sistemática; somente documentação e artigos, sem download de pesos ou datasets.
- **64 no BANKING77 — verificado:** Botzer et al. (2023), [TK-KNN: A Balanced Distance-Based Pseudo Labeling Approach for Semi-Supervised Intent Classification, §4.3, p. 6477](https://aclanthology.org/2023.findings-emnlp.429.pdf), especificam BERT-base com cabeça de classificação e limite de 64 tokens nos experimentos, incluindo BANKING77. É precedente próximo de arquitetura/dataset, mas em regime semissupervisionado com auto-treinamento e poucas amostras rotuladas. Não demonstra equivalência entre 64 e 128, ausência de cortes ou adequação ao nosso FinBERT.
- **128 no artigo BERT — verificado:** Devlin et al. (2019), [BERT, apêndice A.2, p. 4183](https://aclanthology.org/N19-1423.pdf), usam sequências de 128 em 90% dos passos de pré-treinamento e 512 nos 10% restantes. Isso contextualiza custo computacional, mas não é recomendação específica de 128 para fine-tuning no BANKING77.
- **128 na classificação BERT — verificado:** [código oficial run_classifier.py](https://raw.githubusercontent.com/google-research/bert/master/run_classifier.py), definição de `max_seq_length` (linhas 58–62), usa padrão 128. Em `convert_single_example`, uma entrada simples reserva duas posições para CLS/SEP e recebe padding até o limite. É precedente operacional de classificação; não fundamenta padding dinâmico nem prova valor ótimo. Código consultado na branch master, sem commit fixado nesta consulta.
- **128 também em trabalho com BANKING77 — verificado:** Yehudai e Bandel (2024), [FastFit: Fast and Effective Few-Shot Text Classification with a Multitude of Classes, §4.3, p. 176](https://aclanthology.org/2024.naacl-demo.18.pdf), usam máximo de 128 tokens no FastFit em avaliação few-shot que inclui BANKING77. Objetivo e modelos diferem do nosso classificador BERT/FinBERT; não transferir os demais hiperparâmetros nem interpretar como comparação controlada contra 64.
- **Conclusão para D28:** ambos os candidatos possuem precedentes publicados; nenhuma fonte acima estabelece qual preserva melhor a informação com nossos dois tokenizers ou qual oferece melhor custo no notebook. A escolha após medir cortes nos dados de desenvolvimento e recursos continua sendo uma decisão metodológica do projeto, não resultado provado pelos artigos.
- **Pendências preservadas:** política de padding, lado do truncamento, inclusão explícita de tokens especiais na convenção do projeto, métricas de cortes e critérios quantitativos de escolha. Não executar diagnóstico nem consultar o teste para escolher o limite; não adicionar configurações científicas às 12 execuções de D22.

## R32 — Padding fixo versus dinâmico

- **Consulta:** 2026-11-14. Autor declarou desconhecer padding e pediu explicação e recomendação fundamentada. Pesquisa autorizada nesta pergunta; nenhuma decisão nova confirmada.
- **Conceito e orientação técnica — verificados:** documentação oficial [Padding and truncation, Transformers v4.57.1](https://huggingface.co/docs/transformers/v4.57.1/en/pad_truncation), explica que lotes de sequências variáveis precisam de dimensões compatíveis. Padding adiciona posições especiais; truncamento remove tokens acima do limite. Recomenda, como abordagem geral, preencher até a maior sequência do lote, mantendo um limite de truncamento. Isso é orientação técnica, não comparação experimental publicada de BERT/FinBERT no BANKING77.
- **Mecanismo — verificado:** [DataCollatorWithPadding](https://huggingface.co/docs/transformers/en/main_classes/data_collator), parâmetros `padding` e `max_length`: `longest` preenche até o maior comprimento do lote; `max_length` preenche até o limite especificado. A página consultada descreve o mecanismo; não fixa versões de ferramentas do projeto.
- **Máscara:** o [código oficial BERT](https://raw.githubusercontent.com/google-research/bert/master/run_classifier.py), já consultado em R31, constrói `input_mask` com 1 nas posições reais e 0 no preenchimento. Mascarar padding impede sua atenção como conteúdo, mas não implica eliminar automaticamente o trabalho sobre todas as posições em processamento denso.
- **Exemplo hipotético:** três entradas de 10, 20 e 40 tokens, contando marcadores especiais, com limite 64. Padding fixo produz 192 posições (3 × 64); dinâmico produz 120 (3 × 40), preservando os mesmos 70 tokens reais. A redução de posições não é uma previsão proporcional de tempo ou VRAM.
- **Recomendação proposta:** padding dinâmico nos dois modelos, com atenção mascarada e mesmo limite final escolhido por D28. Fundamentação: evitar preenchimento desnecessário sem remover texto adicional; não prometer aumento de acurácia ou ganho fixo de velocidade. Tempo e memória serão medidos no diagnóstico autorizado posteriormente. Padding fixo do código histórico não invalida essa alternativa, mas impede alegar reprodução exata dele.
- **Situação atualizada:** autor confirmou padding dinâmico nos dois modelos após a explicação e fundamentação; registrado em PLAN.md, D29. Lado do padding e do truncamento continuam abertos. Preenchimento até múltiplos para otimização de hardware não foi aprovado.

## R33 — Lado do truncamento e alternativas próximas à classificação de intenções

- **Consulta:** 2026-11-14. Autor pediu pesquisa adicional, além do código original BERT, priorizando trabalhos próximos ao nosso caso antes de decidir o lado do corte. PLAN.md não alterado: nenhuma política nova confirmada.
- **Escopo:** busca dirigida por BANKING77/intent classification com truncation, left/right e head/tail; leitura das seções pertinentes de TK-KNN, ConvFiT, FastFit e comparação de estratégias em classificação de textos. Não é revisão sistemática; ausência de evidência localizada não demonstra inexistência de trabalhos.
- **Precedente próximo, sem comparação de lados:** [Botzer et al. (2023), TK-KNN, §4.3](https://aclanthology.org/2023.findings-emnlp.429.pdf), usa BERT-base e limite de 64 em experimentos incluindo BANKING77, conforme R31. O trecho não explicita o lado nem compara preservar início/final. A [página oficial do repositório](https://github.com/ServiceNow/tk-knn) foi acessada, mas tentativas de ler arquivos e diretório src pela ferramenta web retornaram cache miss; não foi possível auditar o truncamento no código. Não inferir o lado a partir do padrão presumido do tokenizer.
- **Outra abordagem de intenções — verificada:** [Vulić et al. (2021), ConvFiT, §3, p. 1155](https://aclanthology.org/2021.emnlp-main.88.pdf), usa comprimento máximo 48 na segunda etapa, avaliando BANKING77, CLINC150 e HWU64, com BERT/RoBERTa/DistilRoBERTa e objetivos de representação conversacional. O trecho de configuração foi lido; a busca textual por trunc não retornou ocorrências no PDF. Isso documenta um limite curto em tarefa próxima, sem estabelecer lado preferível ou ausência de perda. Não propor 48 como novo candidato nem incorporar seu regime de treinamento ao desenho travado.
- **Outra abordagem próxima, limite sem ablação de lados:** [Yehudai e Bandel (2024), FastFit, §4.3](https://aclanthology.org/2024.naacl-demo.18.pdf), já verificado em R31, usa 128 em classificação few-shot incluindo BANKING77. O trecho fundamenta comprimento, não superioridade de um lado de truncamento.
- **Comparação explícita de alternativas — verificada:** [Sun et al. (2019), How to Fine-Tune BERT for Text Classification?, §5.3.1 e tabela 2](https://arxiv.org/pdf/1905.05583), compara preservar primeiros 510 tokens, últimos 510 ou primeiros 128 + últimos 382. Erros de teste, respectivamente: IMDb 5,63%, 5,44%, 5,42%; Sogou 2,58%, 3,17%, 2,43%. Início+final teve menor erro reportado nesses dois datasets; final sozinho não superou início em ambos. O trabalho também compara agregação hierárquica de segmentos. São documentos longos e tarefas distintas; os resultados não demonstram superioridade em intenções bancárias de entrada limitada a 64/128. Não copiar proporções, afirmar significância ou alterar a arquitetura do projeto a partir disso.
- **Alternativas e riscos:** preservar início corta a cauda; preservar final corta a apresentação; início+final descarta o meio e junta trechos antes separados. Métodos de segmentos com agregação mudam o processamento e extrapolam a escolha simples do lado; não fazem parte do plano confirmado.
- **Síntese:** nesta consulta não foi localizada comparação controlada de lados no BANKING77 que permita recomendar uma política como vencedora. Os precedentes de comprimento não resolvem essa escolha. Preservar início tem precedente operacional BERT (R31), sem prova de superioridade para este projeto.
- **Recomendação metodológica proposta:** aproveitar D28 para quantificar quais mensagens de desenvolvimento excedem 64/128 em cada tokenizer e inspecionar seus trechos antes de confirmar o lado do corte. Comprimentos independem do lado; conteúdo perdido depende dele. Se não houver cortes no desenvolvimento com o limite escolhido, o lado não altera essas entradas observadas, mas isso não garante ausência de cortes em teste ou uso futuro. Não selecionar pela qualidade no teste nem acrescentar treinamentos para comparar políticas sem nova decisão.
- **Pendência:** autor decidirá se condiciona também o lado do corte à inspeção de desenvolvimento. Amostragem e critérios dessa inspeção continuam por definir; nenhuma execução autorizada.

## R34 — Estatísticas de comprimento já publicadas pelo dataset

- **Consulta:** 2026-11-14. Autor perguntou se o BANKING77 já disponibiliza máximos e outras estatísticas para orientar a entrada. Consulta de metadados e documentação, sem baixar dataset/tokenizers ou executar diagnóstico.
- **Ficha oficial — verificada:** [PolyAI/banking77, README, Data Splits](https://huggingface.co/datasets/PolyAI/banking77/blob/main/README.md), informa média de 59,5 caracteres no treino oficial (e 54,2 no teste). Não foi localizada nessa tabela uma medida de máximo ou comprimento com os tokenizers escolhidos. Para orientar decisões do projeto, usar o treino/desenvolvimento; o valor publicado do teste não orienta a escolha de limite.
- **Visualizador — verificado:** [página do dataset](https://huggingface.co/datasets/PolyAI/banking77), com split train selecionado, exibe `text string lengths 13 433`. Registrar como faixa exibida pela interface consultada, não como máximo global reproduzido na revisão de dados que adotaremos. Nenhuma contagem local foi executada.
- **Unidade e API — verificadas:** [documentação do Dataset Viewer, estatísticas, seção string_text](https://huggingface.co/docs/dataset-viewer/statistics), informa que os comprimentos de strings são calculados em caracteres e disponibiliza mínimo, máximo e outras medidas pelo endpoint /statistics. O campo `partial` indica estatística parcial. A tentativa de acessar a resposta específica do BANKING77 pela ferramenta web não foi bem-sucedida; não afirmar que o JSON desse dataset ou o campo partial foram verificados.
- **Publicação complementar — verificada:** [Loukas et al. (2023), Making LLMs Worth Every Penny, tabela 2](https://stogiannidis.github.io/files/LLMPenny.pdf), reporta no treino média de 59,5 ± 40,9 caracteres e 11,9 ± 7,9 palavras. Médias e desvios não determinam máximos ou proporções acima de 64/128 tokens; não converter palavras/caracteres em tokens com razão fixa.
- **Implicação:** aproveitar estatísticas públicas evita ignorar informações prontas, mas não substitui medir comprimentos com cada tokenizer de D12, incluindo marcadores especiais. A distribuição de tokens, o máximo e a proporção acima dos candidatos podem ser calculados sem treinamento e antes dos benchmarks de GPU. Isso especifica medições de D28, não autoriza sua execução nem altera os candidatos ou o protocolo de teste.
- **Estado atualizado:** após o esclarecimento, autor confirmou registrar as estatísticas como apoio às outras decisões e o procedimento de decisão. PLAN.md, D30, registra contagem de tokens antes da GPU e escolha do lado do corte após inspeção do desenvolvimento, com limites de interpretação e sem autorizar execução.

## R35 — CLS direto versus pooler: mecanismo, intenções e checkpoints

- **Consulta:** 2026-11-14. Autor autorizou pesquisar precedentes e diferenças antes de escolher qual representação de CLS alimentará a camada linear de D14. Pesquisa documental; sem download de pesos ou execução. PLAN.md preservado.
- **Pergunta:** CLS final e pooler são equivalentes? Qual caminho possui precedente próximo e apoio operacional nos checkpoints escolhidos? Busca dirigida por intent classification/BANKING77 com pooler/CLS e consulta às implementações oficiais; não revisão sistemática.
- **Mecanismo — verificado:** [Transformers v4.57.1, modeling_bert.py, BertPooler e BertForSequenceClassification](https://raw.githubusercontent.com/huggingface/transformers/v4.57.1/src/transformers/models/bert/modeling_bert.py). BertPooler aplica camada linear 768→768 e tanh ao vetor do primeiro token. BertForSequenceClassification usa essa saída, seguida de dropout e classificador linear. CLS direto pula o pooler. Ambos representam a entrada com 768 valores; o pooler não calcula média dos tokens. A versão consultada é referência de código, não versão de ferramentas aprovada para o projeto.
- **Origem — verificada:** [documentação BERT v4.57.1, pooler_output](https://huggingface.co/docs/transformers/v4.57.1/en/model_doc/bert), descreve a transformação linear+tanh do primeiro token e seu vínculo com o objetivo de previsão da próxima sentença no pré-treinamento. Isso não garante que a saída seja melhor para intenções. No fine-tuning completo, se o pooler integrar o caminho, seus pesos também serão ajustados; não confundir com uso congelado de embeddings para similaridade.
- **BANKING77 — verificado, com ambiguidade preservada:** [Casanueva et al. (2020), Efficient Intent Detection with Dual Sentence Encoders, §4, p. 41](https://aclanthology.org/2020.nlp4convai-1.5.pdf), descreve BERT-TUNED como ajuste completo e softmax sobre a saída de CLS. O trecho não esclarece inequivocamente CLS cru versus pooler; não atribuir a ele uma ablação ou uma preferência entre os dois. A comparação FIXED/TUNED também varia regime de treinamento e representação, não isola o pooler.
- **Precedente em intenções — verificado:** [Benayas et al. (2021), Unified Transformer Multi-Task Learning for Intent Classification With Entity Recognition, §III, p. 147310](https://repository.essex.ac.uk/32137/1/Unified_Transformer_Multi-Task_Learning_for_Intent_Classification_With_Entity_Recognition.pdf), explicita pooler na representação de classificação de intenções. Experimentos em ATIS/SNIPS usam modelo conjunto com reconhecimento de entidades e camada adicional de 256 unidades. É precedente de uso, não comparação CLS/pooler no BANKING77; não incorporar sua cabeça ou treinamento multitarefa.
- **FinBERT — verificado em exemplo oficial:** [yya518/FinBERT, finetune.ipynb](https://raw.githubusercontent.com/yya518/FinBERT/master/finetune.ipynb), instancia BertForSequenceClassification a partir de yiyanghkust/finbert-pretrain para três classes. O log histórico salvo no notebook (Transformers 4.18.0) lista somente classifier.weight/bias como novos pesos, sem listar pooler. Isso é evidência histórica compatível com carregamento do pooler; não constitui auditoria dos pesos da revisão atual. O exemplo não é BANKING77 nem comparação entre representações.
- **Configurações — verificadas:** [BERT selecionado](https://huggingface.co/google-bert/bert-base-uncased/raw/main/config.json) e [FinBERT selecionado](https://huggingface.co/yiyanghkust/finbert-pretrain/raw/main/config.json) informam hidden_size=768 e architectures=BertForMaskedLM. Essa etiqueta não determina sozinha quais tensores estão no arquivo: não inferir ausência/presença de pooler apenas dela. Na futura verificação de carregamento, registrar pesos usados, ausentes e novos, incluindo pooler, sem interpretar o log histórico como verificação local.
- **Síntese:** não foi localizada comparação controlada CLS cru versus pooler no BANKING77 nas fontes desta consulta. Existe apoio operacional explícito para pooler na classe de classificação BERT e no exemplo oficial do FinBERT; isso sustenta uma escolha de protocolo, não alegação de superioridade em acurácia, calibração ou AURC.
- **Proposta:** usar pooler nos dois modelos, seguido da camada linear de 77 classes aprovada em D14, pela proximidade com o caminho oficial de classificação e com o exemplo FinBERT. Alternativa: CLS direto, que remove a transformação intermediária, mas exige explicitar esse desvio do caminho padrão. Manter uma só escolha comum, sem criar uma comparação adicional entre cabeças. Dropout permanece decisão separada, mesmo que a implementação consultada já tenha um padrão.
- **Situação atualizada:** após explicação do mecanismo e dos limites das referências, autor confirmou pooler nos dois modelos; registrado em PLAN.md, D32, com fundamentação. Dropout continua pendente, sem autorizar implementação ou execução. Se houver pesos ausentes no carregamento futuro, documentar e discutir implicações em vez de pressupor equivalência de inicialização.

## R36 — Dropout da cabeça: fundamento e candidato de 0,1

- **Consulta:** 2026-11-14, pesquisa autônoma autorizada até 22h49 de São Paulo. Relógio consultado às 22h46; “10:49” interpretado como 22h49 da mesma noite, informado ao autor. Autor autorizou pesquisar pendências sem novas perguntas, não aprovar decisões nem implementar.
- **Fundamento — verificado:** [Srivastava et al. (2014), Dropout: A Simple Way to Prevent Neural Networks from Overfitting, resumo](https://jmlr.org/papers/v15/srivastava14a.html), fundamenta desligamento aleatório de unidades para reduzir coadaptação e overfitting. É princípio geral, não prova de intensidade ótima para BANKING77.
- **Semântica — verificada:** [PyTorch, Dropout](https://docs.pytorch.org/docs/2.15/generated/torch.nn.Dropout.html), define p como probabilidade de zerar cada elemento, com reescala por 1/(1-p) no treino e identidade na avaliação. p=0,1 não significa zerar exatamente 10% dos elementos em toda passagem nem remover pesos permanentemente.
- **Precedente direto BERT — verificado:** [Devlin et al. (2019), A.3](https://aclanthology.org/N19-1423.pdf), mantém dropout 0,1 no fine-tuning. O [run_classifier.py oficial, create_model](https://raw.githubusercontent.com/google-research/bert/master/run_classifier.py) aplica keep_prob=0,9 à representação antes da camada classificadora, apenas no treino. Isso distingue o dropout da cabeça do dropout interno do encoder.
- **Caminho dos checkpoints — verificado anteriormente em R35:** [BertForSequenceClassification v4.57.1](https://raw.githubusercontent.com/huggingface/transformers/v4.57.1/src/transformers/models/bert/modeling_bert.py) aplica dropout após pooler, antes do classificador; usa classifier_dropout quando definido, senão hidden_dropout_prob. As configurações consultadas de BERT e FinBERT têm hidden_dropout_prob=0,1. Isso apoia declarar explicitamente 0,1 na cabeça, sem depender de defaults ou alterar o encoder.
- **Cuidado com referência do BANKING77:** [Casanueva et al. (2020), §4 e discussão de hiperparâmetros](https://aclanthology.org/2020.nlp4convai-1.5.pdf), usa dropout agressivo 0,75 em MLPs sobre representações de sentenças, com regime distinto. Não transferir esse valor para nossa cabeça linear com fine-tuning completo.
- **Proposta para discussão:** dropout p=0,1 entre pooler e classificador em ambos os modelos; ativo no treino, desativado na validação/teste e geração de previsões para abstenção. Manter fixo nas duas taxas, sem ampliar a busca de D22 e sem alterar dropout interno dos checkpoints. É escolha com precedente, não garantia de melhoria ou optimalidade. Aguardar confirmação antes de PLAN.md.

## R37 — Precisão mista e acumulação: mecanismo e limites

- **Consulta:** 2026-11-14, mesma autorização de R36. Fontes documentais; nenhum benchmark ou teste executado.
- **Fundamento acadêmico — verificado:** [Micikevicius et al., Mixed Precision Training, resumo](https://arxiv.org/abs/1710.03740), descreve limitações de faixa numérica de meia precisão, manutenção de cópia de pesos em precisão simples e escalonamento da perda. Não garante estabilidade ou ganho específico em nossos modelos/hardware.
- **Implementação moderna — verificada:** [PyTorch, Automatic Mixed Precision examples](https://docs.pytorch.org/docs/2.15/notes/amp_examples.html), documenta autocast/GradScaler, detecção de gradientes não finitos e possível salto de atualização. Acumulação requer escala constante dentro do batch efetivo; unscale e atualização de escala devem respeitar o passo do otimizador. Clipping com escala exige desfazer a escala antes de limitar os gradientes.
- **Acumulação:** batch efetivo = batch por passagem × número de acumulações em uma GPU. Altera frequência de atualizações e deve entrar na contagem do scheduler. Não equivale automaticamente, bit a bit, a um batch físico maior e não é adaptação automática autorizada no plano.
- **Precedente próximo já verificado:** FastFit (R31) usa FP16 em BANKING77 com método diferente; é precedente de uso, não validação de BERT/FinBERT na RTX do autor.
- **Pendências/propostas:** discutir FP32 versus AMP no diagnóstico comum aos modelos, registrando dtype, comportamento numérico e custo. Não aprovar BF16 por presumir suporte da GPU nominal; verificar hardware e stack efetivos. Não converter todo o modelo para FP16 por inferência desta pesquisa. Definir antes das execuções como registrar não finitos/passos pulados e como interromper/revisar instabilidade persistente, sem fallback silencioso ou troca automática de precisão. Nenhuma opção confirmada.

## R38 — AdamW: beta/epsilon, grupos de decay e clipping

- **Consulta:** 2026-11-14, mesma autorização de R36. Refinar detalhes abertos de D25 sem reabrir AdamW, decay ou scheduler.
- **Defaults modernos — verificados:** [PyTorch AdamW](https://docs.pytorch.org/docs/2.15/generated/torch.optim.AdamW.html), assinatura usa betas=(0,9; 0,999), eps=1e-8, weight_decay=0,01. Defaults são especificação da ferramenta, não demonstração de adequação ótima.
- **Precedente BERT — verificado:** [optimization.py oficial](https://raw.githubusercontent.com/google-research/bert/master/optimization.py), create_optimizer define betas 0,9/0,999, epsilon 1e-6, exclui nomes LayerNorm/layer_norm/bias do decay e limita norma global dos gradientes a 1,0. O otimizador histórico não deve ser tratado como numericamente idêntico ao AdamW moderno; não atribuir automaticamente seu epsilon à implementação atual.
- **Leitura:** beta controla médias móveis do otimizador; epsilon é estabilizador numérico, não taxa de aprendizado. Excluir bias/LayerNorm muda grupos sujeitos ao decay; clipping limita a norma conjunta dos gradientes antes do passo e não limita diretamente pesos ou probabilidades. São decisões distintas, não um pacote já aprovado.
- **Propostas para discussão separada:** betas 0,9/0,999 têm suporte comum entre código histórico e moderno; considerar excluir bias e parâmetros de LayerNorm e clipping global 1,0 por precedente explícito. Para epsilon, apresentar 1e-8 moderno versus 1e-6 histórico com diferenças de implementação e precisão, sem alegar vencedor. Com AMP, seguir ordem unscale→clipping→step conforme R37. Não escolher valores por resultados do teste nem ampliar silenciosamente a busca científica.

## R39 — Diagnóstico de hardware: medir tempo e memória de forma interpretável

- **Consulta:** 2026-11-14, autorização de R36. Não há benchmark local nesta pesquisa.
- **Tempo — verificado:** [PyTorch, CUDA semantics](https://docs.pytorch.org/docs/2.15/notes/cuda.html), informa que execução CUDA é assíncrona; medições sem sincronização podem ser inexatas. Usar sincronização nos limites do trecho ou eventos CUDA conforme a finalidade. Isso fundamenta o mecanismo, não duração ótima de aquecimento/amostragem.
- **Memória — verificado:** [max_memory_allocated](https://docs.pytorch.org/docs/2.15/generated/torch.cuda.memory.max_memory_allocated.html) mede pico ocupado por tensores; [max_memory_reserved](https://docs.pytorch.org/docs/2.15/generated/torch.cuda.memory.max_memory_reserved.html) mede pico gerenciado pelo alocador com cache; [reset_peak_memory_stats](https://docs.pytorch.org/docs/stable/generated/torch.cuda.memory.reset_peak_memory_stats.html) reinicia contadores de pico. São medidas diferentes; não somá-las como se fossem parcelas independentes nem tratá-las como VRAM total do dispositivo.
- **Proposta metodológica:** fazer aquecimento e atualizações completas antes da janela medida, reiniciar picos por candidato, incluir forward/backward/AdamW e medir exemplos realmente processados por segundo. Com padding dinâmico, registrar a composição/comprimentos dos lotes; um lote só de mensagens curtas não sustenta ausência de OOM para o limite escolhido. Conservar exemplos e política comuns aos dois modelos. Validar duração/salvamento separadamente e incluí-los na projeção total.
- **Pendências:** duração de aquecimento e medição, composição da amostra, margem quantitativa de VRAM e desempate entre batches continuam escolhas práticas. Não foi localizado um percentual de margem universal validado para nosso par no notebook; não inventar limite como consenso acadêmico. Não ampliar batches além de 8/16/32 nem adotar precisão/acumulação sem confirmação.

## R40 — Seeds, reprodução e agregação das repetições

- **Consulta:** 2026-11-14, autorização de R36. Preservar três repetições e orçamento já aprovado.
- **Reprodução — verificado:** [PyTorch, Reproducibility](https://docs.pytorch.org/docs/2.15/notes/randomness.html), alerta que resultados não são garantidamente idênticos entre versões/plataformas ou CPU/GPU, mesmo com seeds iguais. Discute controle de fontes aleatórias e DataLoader. Registrar seed não substitui registrar ambiente, versões e política de determinismo.
- **Evidência acadêmica — verificada:** [Popović et al. (2023), Exploring Variation of Results from Different Experimental Conditions, resumo e conclusão](https://aclanthology.org/2023.findings-acl.172.pdf), estuda simplificação de textos variando seeds, ambientes e dependências; recomenda médias e coeficiente de variação em lugar de máximo. Sustenta reporte de variação, sem provar número suficiente de seeds para BANKING77.
- **Proposta de seleção, ainda não aprovada:** para cada checkpoint e taxa, agregar a acurácia de validação dos melhores checkpoints de cada uma das três execuções (selecionados por D20–D21); escolher taxa pela média dessas três acurácias. Avaliar/reportar as três execuções da taxa escolhida, sem escolher uma seed vencedora. Média e desvio-padrão amostral, com valores individuais disponíveis, são uma proposta compacta de reporte; a fonte acima não exige especificamente esse par.
- **Limites:** uma divisão de dados fixa e três seeds de treinamento observam variação de treinamento, não variação de possíveis divisões. Desvio entre seeds não é intervalo de confiança da população de mensagens. Mesma seed numérica entre modelos não produz pesos/dropout idênticos; não afirmar controle aleatório perfeito. Teste estatístico, desempate entre taxas, seeds exatas e política de determinismo permanecem por confirmar.

## R41 — ECE e métricas por intenção: convenções que precisam ficar explícitas

- **Consulta:** 2026-11-14, autorização de R36. Não adicionar métricas nem correção de calibração.
- **ECE — verificado:** [Guo et al. (2017), §2 e tabela 1](https://proceedings.mlr.press/v70/guo17a/guo17a.pdf), descreve agregação das diferenças entre acurácia e confiança por faixas e usa M=15 na tabela de ECE. É precedente para 15 faixas, não prova de número ótimo no nosso dataset.
- **Limites da estimativa — verificado:** [Roelofs et al. (2022), Mitigating Bias in Calibration Error Estimation, resumo](https://proceedings.mlr.press/v151/roelofs22a.html), encontra menor viés em estimadores com faixas de massa igual do que largura igual nos estudos apresentados. Não implica substituir automaticamente a convenção de Guo, adicionar novo estimador ou garantir essa ordenação em nossa amostra. Fixar tipo e número antes de comparar modelos; faixas definidas por quantis podem ter limites diferentes entre modelos.
- **Proposta para discussão:** ECE secundária nas previsões sem abstenção de cada execução, com uma convenção comum, confiança máxima softmax e indicador de acerto. Considerar 15 faixas de largura igual por precedente, reconhecendo baixa ocupação em algumas faixas; reportar contagens e confiança/acurácia por faixa. Escolha final de faixas e conjunto de reporte continua aberta. Não interpretar margem como probabilidade de acerto nem decidir temperature scaling por essa pesquisa.
- **Divisões por zero — verificado:** [scikit-learn, precision_recall_fscore_support](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html), documenta zero_division e casos indefinidos de precisão, recall e F1. Proposta: explicitar todas as 77 classes e usar zero_division=0 com diagnóstico de casos indefinidos. Não permitir que classes ausentes sejam removidas silenciosamente da média. Essa convenção ainda exige confirmação; versões citadas são documentação consultada, não stack aprovada.

## R42 — Cobertura, limiares e AURC: separar ranking descritivo de regra operacional

- **Consulta:** 2026-11-14, autorização de R36. Complemento a R8/R20; não alterar métricas ou critérios aprovados.
- **Fonte primária — reconsultada:** [Cattelan e Silva (2024), §3.1 e §4.2](https://arxiv.org/html/2305.15508v4), define aceitação por confiança acima de limiar, cobertura empírica e risco seletivo; discute dependência da AURC da qualidade do classificador. Convenções de empates não foram verificadas no código nesta consulta. Não importar NAURC ou métodos corretivos ao escopo aprovado.
- **Dedução operacional, não resultado novo da literatura:** aceitar todos os exemplos com score ≥ limiar pode impedir atingir exatamente uma cobertura-alvo quando vários exemplos empatam. Cortar uma lista ordenada em k exemplos consegue cobertura k/n, mas pode dividir empates e deixar de representar uma regra baseada somente no limiar. Precisamos distinguir a curva por ranking da curva/pontos obtidos por limiares que aceitam blocos inteiros empatados.
- **AURC discreta — proposta a validar:** sem empates, ordenar confiança decrescente, calcular a fração acumulada de erros entre os primeiros k para k=1…n e tirar média desses riscos. Isso corresponde a uma convenção por degraus de largura 1/n, não é automaticamente igual à integração trapezoidal. Cobertura zero não tem erro seletivo definido; não adicionar ponto artificial sem especificar seu efeito na integração. Escala 0–1 versus percentual deve estar explícita. Com empates, a fórmula exige política própria ainda por decidir.
- **Limiar versus teste:** um limiar escolhido para cobertura de validação não garante a mesma cobertura efetiva no teste. Conservar o limiar e reportar cobertura observada; não recalibrar no teste para atingir a meta. Curvas descritivas por ranking podem ser calculadas depois, com finalidade separada e sem retunar o procedimento final.
- **Pendências:** objetivo operacional, valores de cobertura/erro, igualdade, empates, integração, escala e alinhamento entre seeds continuam abertos. Proposta de procedimento não é decisão aprovada nem garantia estatística de erro.

## R43 — Lado do padding e auditoria dos dados

- **Consulta:** 2026-11-14, autorização de R36. Pendências de entrada/reprodução; nenhuma política aprovada nesta pesquisa.
- **Padding à direita — verificado:** [documentação BERT v4.57.1, Notes](https://huggingface.co/docs/transformers/v4.57.1/en/model_doc/bert), recomenda preencher à direita porque BERT usa posições absolutas. Trata-se do lado do preenchimento, não do lado do truncamento. Com pooler que extrai a primeira posição, não deslocar CLS para depois de pads ao simplesmente ativar padding à esquerda. Proposta: explicitar padding à direita nos dois modelos da família BERT, mantendo a política dinâmica de D29; aguardar confirmação.
- **Rótulos — fonte primária reconsultada:** [Ying e Thomas (2022), Label Errors in BANKING77](https://aclanthology.org/2022.insights-1.19.pdf), investiga possíveis erros de rótulos e efeitos sobre classificação. É fundamento para auditoria e para discutir ambiguidades; não prova que toda discordância do nosso modelo seja erro de anotação nem autoriza corrigir/remover exemplos do teste oficial.
- **Proposta de auditoria:** registrar textos vazios, duplicatas exatas, pares texto/rótulo conflitantes e sobreposição entre conjuntos antes de treinar; definir a ação sobre cada categoria antes de executar. Métodos de detecção, normalização e tratamento devem ser explícitos. Duplicatas com mesmo rótulo e com rótulos diferentes não são o mesmo problema; não remover tudo silenciosamente. Eventual ajuste que altere a divisão oficial ou o desenho depende de discussão com o autor.
- **Limites:** nenhum arquivo concreto de dados foi auditado e nenhum índice/seed foi escolhido nesta rodada. Metadados e literatura fornecem riscos e mecanismos, não resultados de qualidade dos nossos splits.

## Síntese da pesquisa autônoma de 22h46–22h49 — 2026-11-14

- R36–R43 antecipam fundamentação para as pendências do plano: dropout, precisão/acumulação, AdamW/clipping, medição de hardware, seeds/agregação, ECE/divisões por zero, limiares/AURC e padding/auditoria de dados.
- Próxima decisão proposta: dropout da cabeça p=0,1 nos dois modelos, fixo entre configurações e desligado na avaliação, por precedente BERT. Não confirmado.
- As fontes não estabelecem intensidade ótima, margem universal de VRAM, tamanho mínimo suficiente de três seeds ou garantia de erro dos limiares. Propostas operacionais foram identificadas como propostas; decisões D1–D32 permanecem travadas.
- Nenhuma implementação, treinamento, benchmark ou download de pesos/dataset foi realizado. PLAN.md não foi editado durante esta rodada de pesquisa. Continuar decisões arquiteturais uma por turno, com aprovação antes do registro no plano.

## Encaminhamento da revisão — 2026-11-14

- A comparação pós-treinamento de MSP e SoftmaxMargin tem precedente; não exige inventar uma arquitetura ou modificar pesos.
- Confirmado posteriormente pelo autor (PLAN.md, D6): primeiro avaliar curvas risco-cobertura, sem fixar um único limiar arbitrário; depois definir procedimento de escolha de pontos operacionais na validação e avaliar os limiares congelados no teste.
- Distinguir duas perguntas: qualidade do sinal ao longo das coberturas versus desempenho de uma regra operacional fixada antes do teste. Uma curva descritiva de teste não deve ser usada para escolher o limiar operacional.
- R2 é referência para controle estatístico de risco; comparar curvas empiricamente não equivale a implementar esse controle. Não prometer limite de erro garantido sem adotar e verificar o método correspondente.
- Proporção de validação e eventual subconjunto separado para limiares continuam sem decisão. R3–R4 sustentam precedente de aproximadamente 10%, não uma proporção ótima.
- A pesquisa isolada não aprovou escolhas. Posteriormente, o autor confirmou a avaliação erro versus cobertura em D6; divisões, variantes de treinamento e métricas adicionais continuam sem aprovação.


## R44 — Busca curta sobre os níveis de cobertura em PLN

- **Autorização:** autor autorizou pesquisa breve e pediu evitar gasto excessivo de tempo. Escopo limitado a dois trabalhos de PLN já citados; não é revisão sistemática.
- **Xin et al. (2021):** [The Art of Abstention](https://aclanthology.org/2021.acl-long.84.pdf), §3.1 e §5.1/tabela 1, consultados novamente. Define risco em cobertura dada, usa curvas risco–cobertura e sua área para avaliar classificadores. Os trechos examinados não justificam uma grade operacional específica de 80%, 90% e 95%. Percentuais presentes em outras partes, como a divisão 20/80 da regularização, não são metas de cobertura e não devem ser usados como tal.
- **Kamath et al. (2020):** [Selective Question Answering under Domain Shift](https://aclanthology.org/2020.acl-main.503.pdf), §3.1 e tabela 1/apêndice A.5, consultados via busca indexada do PDF. Avalia área sob curva e cobertura em níveis de acurácia de 80%/90%; esses valores são acurácia, não cobertura. Não justificam a grade proposta por transferência direta.
- **Conclusão limitada:** os dois trabalhos sustentam avaliar a relação risco–cobertura; esta busca não encontrou justificativa específica para o trio de coberturas 80/90/95. Não inferir ausência de precedentes em toda a literatura.
- **Recomendação prática, ainda pendente:** manter 100% como referência e metas 95/90/80 para representar abstenção de 5/10/20%, escolhidas antes dos resultados por interpretabilidade; declarar explicitamente que os números são escolha do projeto. Curva completa e AURC mantêm a avaliação geral. PLAN.md não alterado; adesão anterior estava condicionada a embasamento dos percentuais e não confirma esta escolha prática.

- **Atualização de R44:** autor aceitou a grade como escolha prática após apresentação dos limites da busca; registrada em PLAN.md, D38. Nenhuma implementação autorizada.

- **Atualização sobre R40:** protocolo de seleção pela média das três acurácias de validação e reporte das três execuções da taxa escolhida confirmado em PLAN.md, D39. Estimador de dispersão, desempate entre taxas e inferência estatística continuam pendentes.

## R45 — Segunda iteração do embasamento e consolidação operacional

- **Escopo:** atendimento a D5 e ao pedido do autor de consolidar o desenho antes de implementar. Revisão documental do registro existente; nenhuma nova busca externa, download, inspeção do dataset ou execução. Não é revisão sistemática, releitura integral de todos os artigos ou verificação de software.
- **Critério:** distinguir fundamento do mecanismo, precedente de uso, escolha prática e afirmações que os dados futuros ainda precisam sustentar. Fontes/links e trechos efetivamente consultados permanecem nos blocos indicados.

| Decisões | Evidência já registrada | Conclusão e limite da revisão |
|---|---|---|
| D1 | R1 | Dataset de intenções bancárias; não valida intenções financeiras corporativas fora dos rótulos |
| D2–D3 | R2/R6/R8 | Classificação seletiva, MSP e margem de probabilidades fundamentados; superioridade futura é hipótese |
| D4 | R3–R5/R21–R22 | Separação e estratificação são coerentes com seleção e avaliação independentes; integridade dos arquivos ainda por auditar |
| D5 | Requisito do autor | Revisão e justificativa são exigências do processo; esta seção é a segunda iteração sobre evidência existente |
| D6 | R2/R6/R8/R20/R42 | Curvas/área permitem avaliar vários níveis; limiar empírico não herda garantia de controle de risco |
| D7 | R30/R39 | Diagnóstico prévio é escolha de engenharia motivada pelo custo; hardware e tempos não foram medidos |
| D8–D10 | R9–R12 | Comparação empírica dos checkpoints é viável como escopo; diferenças não isolam causalmente o domínio |
| D11 | R8 | Aplicar duas regras às mesmas previsões controla o classificador, sem provar generalização para outras execuções |
| D12 | R9/R13/R35 | Origem documental mais direta para o par selecionado; revisões/tensores atuais e carregamento ainda por conferir |
| D13 | R14–R16 | Fine-tuning tem precedente no BANKING77; comparação publicada usa outro porte/regime e não garante o ganho local |
| D14 | R17–R18 | Cabeça linear/CLS e cross-entropy fundamentadas; pooler tratado separadamente, sem alegar representação perfeita |
| D15 | R19/R24 | Métricas compatíveis com rótulo único; diagnósticos por intenção complementam agregação |
| D16–D17 | R20/R41–R42 | AURC e ECE têm precedentes; dependem respectivamente do ranking/classificador e da convenção de estimação |
| D18–D19 | R3–R5/R21–R22 | Validação compartilhada de aproximadamente 10% tem justificativa prática e precedentes; não elimina viés de seleção |
| D20–D21 | R24/R26 | Acurácia é critério coerente com erro unitário; desempates são convenções do protocolo, não valores prescritos por artigo |
| D22–D24 | R25–R27 | Três seeds, taxas e cinco épocas têm precedentes; orçamento reduzido não garante ótimo ou poder estatístico |
| D25–D27 | R28–R30 | AdamW/decay/scheduler têm fundamentos e precedentes; batch final é medição técnica, não conclusão bibliográfica |
| D28–D31 | R31–R34 | 64/128 têm precedentes; preservação integral é requisito do autor, ainda depende das contagens por tokenizer |
| D32–D34 | R35–R36/R43 | Pooler/dropout/padding à direita têm apoio técnico; não foi localizada ablação controlada de pooler no BANKING77 |
| D35–D36 | R37 | AMP FP16/GradScaler é candidata documentada; viabilidade e ganho local permanecem por medir |
| D37–D38 | R42/R44 | Objetivo de cobertura e avaliação geral coerentes; grade 95/90/80 é escolha prática explicitamente aceita |
| D39 | R25/R40 | Repetir e reportar variação é fundamentado; média para selecionar taxa é aplicação escolhida pelo autor |
| D40 | D15/R7/R43 | Foco qualitativo é escolha alinhada à pergunta; exemplos não demonstram causalidade nem erro de anotação por si sós |
| D41 | R40 e escopo do autor | Descrição principal e inferência opcional são escolhas de escopo; tamanho aparente da diferença não decide significância |
| D42 | R7/R43 | Há motivação para auditoria, sem achados locais presumidos ou autorização de corrigir benchmark automaticamente |
| D43 | spec.md e prazo do autor | Cronograma é meta de projeto; nenhuma referência acadêmica determina duração real das execuções |

- **Lacunas mantidas:** procedência detalhada dos tensores atuais; compatibilidade das versões/ambiente; medidas de recursos; suficiência de três seeds para diferenças pequenas; ausência de comparação direta de pooler/truncamento no BANKING77 nas fontes examinadas. Nenhuma aprovação do professor foi presumida. Não há base para prometer FinBERT superior, redução de erro monotônica ou garantia de segurança.
- **Consolidação proposta:** PLAN.md, O1–O9, especifica seeds, AdamW/clipping, diagnóstico, desempates, limiares, métricas, artefatos e verificações. As escolhas práticas (por exemplo, seeds 42/13/37/73, duração de diagnóstico, margem de memória, estimador de dispersão e limite de exemplos qualitativos) são identificadas como tais, não como consenso acadêmico.
- **AURC com empates:** O7 propõe média esperada dos riscos de prefixos sob permutações uniformes dentro de blocos. É dedução operacional que deve ser verificada por enumeração de caso pequeno na implementação; não atribuí-la aos autores de R42 nem afirmar reprodução de código não consultado. Mantém separação entre ranking descritivo e limiares que aceitam blocos inteiros.
- **Situação:** D1–D43 preservadas; O1–O9 e cronograma complementar aguardam aprovação conjunta do desenho final. Revisões de status no plano corrigem notas antigas que ainda marcavam escolhas confirmadas como pendentes. Nenhum código, teste ou benchmark foi executado nesta revisão.
