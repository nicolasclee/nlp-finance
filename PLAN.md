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
- **Pendências:** valores dos limiares, proporções dos conjuntos e métricas ainda dependem de confirmação. Os critérios de abstenção estão definidos em D3 e a separação dos dados em D4. Robustez e hierarquia não foram aprovadas como contribuições adicionais.

### D3 — Comparar dois critérios de abstenção separadamente

- **Decisão:** comparar, em cada modelo, uma regra baseada na maior pontuação entre as intenções e outra baseada na diferença entre as duas maiores pontuações. Usar as previsões do mesmo classificador para avaliar cada regra, com referência sem abstenção.
- **Regras:** na primeira, abster quando a maior pontuação ficar abaixo de um limiar; na segunda, quando a diferença entre as duas primeiras ficar abaixo de um limiar.
- **Motivo:** investigar empiricamente os dois sinais sugeridos pelo autor, distinguindo apoio à intenção escolhida de competição entre alternativas, sem acrescentar outra arquitetura de treinamento.
- **Comparação:** examinar erros entre pedidos aceitos em níveis comparáveis de cobertura (proporção de pedidos aceitos). Valores e procedimento de seleção dos limiares permanecem abertos.
- **Escopo:** avaliar os critérios separadamente primeiro. Sua combinação permanece pendente, sem inclusão confirmada no experimento principal.
- **Cuidado conceitual:** as pontuações não garantem probabilidades reais de acerto; ambos os sinais derivam da mesma distribuição de saída.

### D4 — Separação entre treino, validação e teste

- **Decisão:** preservar a divisão oficial de treino/teste, caso exista, e separar do treino uma validação estratificada por intenção.
- **Responsabilidades:** treino ajusta os pesos; validação orienta a seleção do modelo e dos limiares; teste avalia o procedimento final após congelar essas escolhas.
- **Motivo:** preservar aproximadamente a distribuição das intenções na divisão de treino/validação e evitar adaptar escolhas aos resultados do teste final.
- **Limite:** estratificação preserva proporções entre classes, não exige conjuntos do mesmo tamanho. O teste oficial será preservado, sem redistribuí-lo para equilibrar classes.
- **Pendências:** proporção de validação e detalhes reprodutíveis da divisão ainda serão definidos; estrutura oficial do dataset ainda será verificada.

### D5 — Fundamentação bibliográfica e revisão final das decisões

- **Decisão:** realizar agora uma revisão curta dos protocolos de validação em trabalhos sobre BANKING77 com Transformers e classificação com abstenção, antes de escolher a proporção de validação.
- **Decisão:** após completar a sequência de decisões do plano, realizar uma segunda iteração para revisar o embasamento de todas as decisões arquiteturais e experimentais e buscar referências acadêmicas pertinentes.
- **Motivo:** toda escolha deve ter uma razão explícita; recomendações heurísticas não devem ser apresentadas como conclusões sustentadas pela literatura.
- **Resultado esperado:** para cada decisão, explicitar justificativa, referências aplicáveis, limites da evidência e eventuais lacunas. Distinguir fundamentação publicada de escolhas práticas ou hipóteses que precisam de verificação experimental.
- **Revisões:** alterações de decisões resultantes dessa auditoria dependem de nova confirmação do autor antes de atualizar este plano.
- **Situação atual:** a reserva de 20% do treino para validação foi apenas sugerida pela IA; não foi aprovada nem fundamentada especificamente para este experimento.

Somente decisões confirmadas pelo autor serão incorporadas a este plano. Nenhuma implementação está autorizada nesta etapa.
