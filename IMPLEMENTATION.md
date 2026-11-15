# Roteiro de implementação e execução

## Situação e modo de trabalho

Este roteiro organiza [PLAN.md](PLAN.md), D1–D44, e a revisão em [REVIEW.md](REVIEW.md). O autor aprovou O1–O9 e autorizou a implementação; as medições e decisões que dependem de resultados continuam pendentes. [RESEARCH.md](RESEARCH.md) registra fontes e limites; notas históricas com status antigo não revogam decisões posteriores.

O autor acompanha as decisões que afetam validade e interpretação; a implementação avança em partes pequenas, com explicação curta do fluxo e revisão do código pelo autor. O2 usa módulos Python, comandos reproduzíveis e configurações salvas, sem depender da ordem de células de notebook.

**Modo de trabalho:** implementar diretamente cada etapa em um bloco compreensível, explicar o fluxo e apresentar o código ao autor. Por decisão explícita do autor, não exigir TDD, red–green–refactor ou testes unitários para cada função; essa orientação substitui a regra de ciclo obrigatório da seção 7 de AGENTS.md para este trabalho. Manter verificações proporcionais aos riscos científicos: auditorias de dados, conferência de métricas com exemplos conhecidos, integridade dos checkpoints e diagnóstico de treinamento. Registrar os resultados dessas verificações; não alterar ou enfraquecer testes existentes para ocultar falhas. Os testes já criados podem continuar disponíveis, sem definir o ritmo da implementação.

**Situação:** critério quantitativo de AMP decidido em D44; O1–O9 aprovados e implementação iniciada. Decisões científicas adicionais ou alterações de desenho voltam ao autor; detalhes técnicos já delegados podem ser resolvidos dentro do protocolo confirmado.

## 0. Protocolo, ambiente e rastreabilidade

- **Objetivo / resultado:** ter um protocolo executável e um manifesto de versões, comandos e artefatos; conferir aprovação do tópico pelos professores, sem presumir resposta.
- **Dependências / artefatos:** D1–D44 e O1–O9; pacote `src/nlp_finance/`, configurações JSON, ambiente e lockfile conforme O2. Fixar revisões e hashes de dados, checkpoints e tokenizers quando disponíveis. Registrar hardware e versões reais.
- **Verificações / conclusão:** conferir que cada execução identifica dados, configuração, modelo, seed e tentativa; comando de treino não executa teste final implicitamente. Antes de cada download acima de 50 MB, avisar tamanho estimado, finalidade e consumo de rede/disco; se o tamanho for desconhecido e puder exceder esse limite, obter metadados ou avisar. Downloads não inserem binários automaticamente no contexto; saídas volumosas exigem aviso separado.
- **Pendências:** versões e revisões concretas após inspeção; status da aprovação docente.

## 1. Dados e divisão

- **Objetivo / resultado:** preservar o teste oficial e criar uma divisão reproduzível do treino oficial, com cerca de 10% para validação estratificada. Treino ajusta pesos; validação orienta escolhas; teste fica reservado à avaliação final (D4, D18–D19).
- **Dependências / artefatos:** protocolo e origem autorizados; manifesto de origem/revisão/hash, mapeamento dos 77 rótulos, IDs e índices persistidos de treino/validação/teste e relatório de auditoria. O1 fixa seed 42 para divisão e seeds 13, 37 e 73 para treino.
- **Verificações / conclusão:** primeiro testar ausência de IDs compartilhados entre treino e validação; depois verificar separação dos splits, identidade bidirecional rótulo↔ID entre splits e modelos, contagens e 77 rótulos. Auditar vazios, duplicatas, conflitos e sobreposição, inclusive igualdade após normalização de espaços, sem alterar textos. Registrar baseline da classe majoritária do treino na validação, conforme O8.
- **Pendências:** divergências, sobreposições ou correções com efeito experimental exigem apresentar achados ao autor, sem limpeza automática (D42).

## 2. Modelo e entrada

- **Objetivo / resultado:** converter texto em 77 logits e permitir que encoder, pooler e classificador aprendam juntos. Usar `google-bert/bert-base-uncased` e `yiyanghkust/finbert-pretrain`, cada um com seu tokenizer; pooler treinável, dropout 0,1 na cabeça e camada linear (D12–D14, D32–D34).
- **Dependências / artefatos:** divisão e revisões fixadas; componentes de tokenização e modelo, configurações e registro dos pesos carregados, ausentes, descartados e novos. Preservar checkpoints originais.
- **Verificações / conclusão:** checks separados para saída de 77 classes, gradientes no encoder/pooler/cabeça, padding dinâmico à direita e probabilidades finitas e normalizadas; entropia cruzada recebe logits. Em avaliação, dropout desligado. Auditar pooler e encoder: ausência inesperada exige revisão.
- **Pendências:** fixar revisões concretas. Contar tokens com marcadores especiais no desenvolvimento, sem corte: usar 64 se ambos os tokenizers preservarem tudo, senão 128 se ambos preservarem tudo. Acima de 128, parar e discutir; não cortar ou excluir automaticamente (D31).

## 3. Uma execução e recuperação

- **Objetivo / resultado:** executar uma tentativa de treinamento dos pesos com o `Trainer` do Transformers, validação por época e salvamento verificável; a validação escolhe a versão de cada execução pela maior acurácia e, em empate, a versão mais antiga (D20–D21). A integração com AMP e validação em FP32 ainda precisa ser validada no ambiente real.
- **Dependências / artefatos:** dados e modelo verificados; configuração, logs por época, checkpoint selecionado, histórico de tentativas e metadados de seleção. Planejar cinco épocas, AdamW com decay 0,01, warmup de 10% e decaimento linear; taxas de pico 2e-5 e 5e-5 (D23–D26).
- **Verificações / conclusão:** checks separados para atualização de pesos, desempates de checkpoint, scheduler e equivalência das previsões em FP32 antes/depois de salvar e recarregar, com tolerância explícita. Testar que passo pulado não avança o scheduler. Um smoke test integra treino, validação e salvamento sem usar teste final.
- **Recuperação conforme O2:** em falha ou interrupção, reiniciar a execução inteira com mesma configuração e seed, preservando todas as tentativas; só uma execução completa válida conta. Baixo desempenho isolado não é falha técnica. Correções que alterem treinamento ou resultados invalidam todas as execuções afetadas; mudanças de desenho exigem revisão com o autor.
- **Pendências:** medir viabilidade. Com passos AMP pulados, o scheduler pode não chegar a zero em cinco épocas: registrar atualizações previstas/efetivas, saltos e taxa final, sem compensar com passos extras.

## 4. Diagnóstico e configurações finais

- **Objetivo / resultado:** medir viabilidade e custo antes dos treinamentos completos, sem escolher por acurácia ou teste. Comparar FP32 com AMP FP16/GradScaler nos dois modelos e batches 8, 16 e 32 (D7, D27, D35–D36).
- **Dependências / artefatos:** etapas 1–3 verificadas; relatório de hardware, comprimentos, memória, velocidade, estabilidade e estimativas de três/cinco épocas e 12 execuções; manifesto da configuração comum escolhida. O4 propõe aquecimento separado, mesma amostra de 512 exemplos e passagem completa por candidato; stress com entradas longas separado do throughput e da projeção.
- **Verificações / conclusão:** verificar GPU/stack reais, compatibilidade, memória e throughput com atualização completa em ambos os modelos; medir também validação e salvamento. Realizar pequeno diagnóstico de aprendizado no treino, registrando perdas inicial e final; investigar falha antes dos experimentos. Aplicar a margem de 1 GiB, o desempate de batch e a seleção por throughput de O4, escolhas práticas aprovadas. Fixar comprimento, batch e precisão comuns antes das execuções científicas.
- **Pendências:** medir compatibilidade, memória e duração. Se nenhum candidato for viável, se AMP não atender ao critério ou se o prazo for inviável, apresentar medições ao autor; não trocar precisão, adicionar acumulação ou reduzir épocas/seeds silenciosamente.

### Estabilidade quantitativa do AMP — decisão D44

Separar as primeiras 20 tentativas de adaptação da escala e medir as 100 seguintes por modelo no batch candidato final, repetindo exemplos de treino se necessário em diagnóstico separado do benchmark. Exigir pelo menos 99 atualizações válidas e no máximo um salto; após a fase inicial, interromper diante de três saltos consecutivos. Registrar escala, perdas, parâmetros e gradientes não finitos; parar diante de perda ou parâmetros não finitos. Estas atualizações não contam como épocas científicas.

Durante cada treinamento científico, após as primeiras 20 tentativas, interromper e investigar se qualquer janela móvel completa de 100 tentativas tiver mais de um salto ou se houver três saltos consecutivos; registrar totais e trecho final incompleto. Os números são convenções práticas, não limites validados pela literatura nem garantia de estabilidade futura ([RESEARCH.md, R46](RESEARCH.md)). Compatibilidade e estabilidade não provam ganho: O3 exige economia de memória ou maior throughput em ambos os modelos contra FP32 em batch comparável. Se não houver referência comparável, apresentar o resultado para decisão, sem afirmar ganho.

## 5. Treinamentos científicos e seleção na validação

- **Objetivo / resultado:** executar as condições planejadas e escolher uma taxa por modelo sem escolher a seed vencedora. São **2 modelos × 2 taxas × 3 seeds = 12 treinamentos completos**, cinco épocas cada, sujeitos ao diagnóstico (D22–D24, D39).
- **Dependências / artefatos:** manifesto e diagnóstico concluídos, mesmas divisões e condições fixas; logs e checkpoints por modelo/taxa/seed/tentativa; previsões de validação, métricas por época e registro de recursos/falhas.
- **Verificações / conclusão:** cada execução segue D20–D21; selecionar a taxa por maior média das três acurácias de validação. Preservar as três repetições da taxa escolhida e reportar resultados individuais, média e dispersão; não omitir resultados desfavoráveis. Investigar falhas do pipeline durante desenvolvimento, inclusive comparação com baseline, sem exigir que FinBERT supere BERT.
- **Pendências:** resolver falhas conforme etapa 3. Aplicar o desempate entre taxas e o desvio amostral de O5. Inferência estatística é opcional e deve ser planejada antes do teste, não decidida pelo tamanho da diferença (D41).

## 6. Regras de abstenção e congelamento

- **Objetivo / resultado:** com pesos e previsões fixos, selecionar na validação limiares separados para maior probabilidade e margem entre as duas maiores probabilidades; metas 95%, 90% e 80%, com referência de 100% (D3, D11, D37–D38). Limiares não treinam pesos.
- **Dependências / artefatos:** três checkpoints da taxa escolhida por modelo e previsões de validação; limiares, coberturas alcançadas e manifesto congelado com hashes, modelos, seeds, checkpoints e configurações.
- **Verificações / conclusão:** testar que limiares usam somente validação, igualdade e empates; verificar serialização/releitura de previsões e cálculo das métricas com casos manuais, incluindo empates na AURC e bordas da ECE. O6 determina aceitar scores iguais ao limiar e blocos inteiros de empate; O7 define AURC discreta e ECE em 15 faixas. Congelar todas as escolhas antes de gerar previsões finais do teste.
- **Pendências:** conferir a aplicação das convenções aprovadas em O5–O7. Validação compartilhada pode sobreajustar escolhas; não acrescentar automaticamente divisão de calibração nem garantia de risco.

## 7. Avaliação final no teste

- **Objetivo / resultado:** aplicar o procedimento congelado ao teste oficial, medir classificação e abstenção e interpretar resultados sem reajustar escolhas.
- **Dependências / artefatos:** manifesto congelado; previsões por ID e rótulo, scores, limiares, métricas, tabelas e curvas para as três repetições selecionadas de cada modelo. Reutilizar previsões para ambas as regras.
- **Verificações / conclusão:** reportar acurácia, Macro-F1, diagnóstico por intenção, ECE secundária, curvas risco–cobertura, AURC e cobertura/erro efetivos por meta, com referência sem abstenção. Comparar em coberturas efetivas, sem forçar metas no teste. Auditar integridade do teste sem usar desempenho para seleção; se houver entrada excedente, parar e discutir, sem truncar ou excluir (D31/D42).
- **Pendências:** quaisquer falhas descobertas após congelamento exigem registro e revisão do alcance, sem orientar correções por resultados desfavoráveis. Três seeds descrevem variação dos treinamentos no split fixo, não significância ou toda a incerteza.

## 8. Análise e entrega

- **Objetivo / resultado:** explicar confusões recorrentes e erros aceitos, relacionando resultados à pergunta sobre checkpoints e regras; produzir código reproduzível, artigo e apresentação.
- **Dependências / artefatos:** avaliação final e registros completos; tabelas, figuras, análise qualitativa, instruções de reprodução, artigo SBC de 8–10 páginas excluindo referências e apresentação de exatamente 15 minutos ([spec.md](spec.md)). Declarar uso de IA e revisar conteúdo e código; referenciar código reutilizado.
- **Verificações / conclusão:** conferir integridade dos artefatos e execução reproduzível; conferir escopo, formato e tempo. Alinhar proposta, artigo e apresentação a intenções bancárias e comparação de checkpoints; relatar diferenças de vocabulário e pré-treinamento, validação compartilhada, limites das seeds e ausência de garantia de risco. Não atribuir causalidade exclusiva ao domínio financeiro. O8 define seleção reproduzível e limitada de exemplos; não tratá-los como amostra representativa.
- **Pendências:** verificar a situação da aprovação docente e a data de apresentação. A meta de D43 para 14–15/11 depende do diagnóstico; datas intermediárias são metas condicionadas, não garantia de execução. Não ampliar busca por resultados desfavoráveis.
