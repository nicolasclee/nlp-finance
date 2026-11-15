# Dúvidas para o professor

Perguntas abertas para discussão; não representam respostas ou aprovação docente. Criado em 2026-11-14. Não houve contato com o professor pela IA.

## Q1 — Comparação de checkpoints versus isolamento causal

- **Contexto:** pergunta principal compara BERT genérico e FinBERT em BANKING77. Pré-treinamento adicional, corpus, vocabulário e histórico supervisionado podem variar entre candidatos.
- **Pergunta:** é adequado comparar checkpoints disponíveis, controlar o fine-tuning e explicitar que diferenças de desempenho não isolam causalmente o efeito do domínio financeiro?
- **Posição atual do autor:** considera pertinente aceitar e documentar essa limitação, enquanto investigamos alternativas mais comparáveis.
- **Referências para levar:** RESEARCH.md, R9 e R10; PLAN.md, D8–D9.
- **Resposta do professor:** pendente.

- **Subsídio metodológico pesquisado:** RESEARCH.md, R11–R12: estudos podem usar controles de adaptação a outro domínio, repetição de execuções e comparação por orçamento. Discutir se o objetivo do trabalho deve permanecer comparação de checkpoints ou exigir controles adicionais de pré-treinamento, considerando o prazo.

## Q2 — Contribuição adicional com abstenção

- **Contexto:** comparar maior probabilidade e margem entre as duas maiores probabilidades sobre as mesmas previsões, apresentando erro versus cobertura.
- **Pergunta:** essa análise, junto da comparação BERT/FinBERT e discussão de erros, oferece profundidade suficiente dentro do tópico aprovado de chatbots?
- **Referências para levar:** RESEARCH.md, R2, R6 e R8; PLAN.md, D2, D3 e D6.
- **Resposta do professor:** pendente.

## Q3 — Organização dos dados para selecionar modelo e limiares

- **Contexto:** teste oficial preservado; validação retirada do treino. Percentual e possível separação entre seleção do modelo e ajuste dos limiares ainda abertos.
- **Atualização:** autor confirmou validação compartilhada em PLAN.md, D18; percentual segue aberto. Manter pergunta para eventual revisão com o professor, sem presumir aprovação docente.
- **Esclarecimento pesquisado:** RESEARCH.md, R21 distingue seleção na validação de avaliação independente no teste e registra risco de overfitting do critério de seleção; discutir se o controle planejado é suficiente para este escopo.
- **Pergunta:** uma validação compartilhada, com procedimento explícito e teste final independente, é adequada ao escopo, ou devemos reservar subconjuntos separados para essas duas escolhas?
- **Referências para levar:** RESEARCH.md, R3–R5; PLAN.md, D4.
- **Resposta do professor:** pendente.

## Q4 — Encoder congelado ou fine-tuning completo?

- **Contexto:** par confirmado: google-bert/bert-base-uncased e yiyanghkust/finbert-pretrain. Inicialmente foi discutido treinar apenas a saída; após examinar precedentes, o autor confirmou fine-tuning completo (PLAN.md, D13).
- **Situação:** dúvida de escopo sobre congelamento superada pela decisão do autor; manter como histórico e referência para explicar a escolha ao professor. Não há exigência docente de ajuste completo registrada.
- **Pergunta:** usar Transformers como extratores congelados e treinar um classificador de 77 intenções atende ao escopo aprovado, cuja proposta menciona fine-tuning? Ou é esperado ajustar também os pesos do encoder?
- **Distinção central:** o controle de D11 exige pesos fixos ao comparar regras de abstenção, depois do treinamento. Permite tanto encoder congelado quanto fine-tuning completo antes dessa etapa. Fine-tuning completo não altera o checkpoint original armazenado; produz um modelo derivado.

### Explicação técnica para apresentar

1. Cada tokenizer transforma o texto em IDs e máscara de atenção. O encoder gera um vetor de 768 valores por token. É preciso escolher como representar a mensagem inteira (por exemplo, vetor do token CLS); essa escolha ainda não foi aprovada.
2. Com uma representação de 768 valores, uma saída linear de 77 classes possui 59.213 parâmetros (768 × 77 pesos + 77 vieses). Ela gera logits; softmax permite obter as pontuações usadas na abstenção. A cross-entropy compara os logits com a intenção anotada.
3. **Encoder congelado:** impedir gradientes nos parâmetros do encoder e otimizar somente a saída. Uma variante simples mantém encoder em avaliação, desativando seu dropout, enquanto treina a saída; isso é uma escolha explícita, não consequência automática de congelar pesos. Pode pré-calcular representações para economizar computação, desde que extração seja determinística e tratamento dos splits permaneça correto.
4. **Fine-tuning completo:** permitir gradientes no encoder e na saída; backpropagation calcula como o erro depende desses pesos, e o otimizador os atualiza. Há maior custo de memória para gradientes, ativações e estado do otimizador. Continua partindo de pesos aprendidos; não é treinar do zero.
5. **Avaliação em ambos:** terminar treinamento, selecionar versão na validação e fixar o classificador; gerar previsões em modo de avaliação; comparar as duas regras sobre as mesmas pontuações, sem atualização dos pesos.

- **Perguntas científicas diferentes:** encoder congelado avalia utilidade das representações prontas sob o classificador escolhido; ajuste completo avalia desempenho após adaptação supervisionada à tarefa. Nenhuma estratégia elimina diferenças históricas entre checkpoints.
- **Precedente direto encontrado:** Casanueva et al. (2020), tabela 3, comparam BERT congelado e ajustado no BANKING77, favorecendo o ajustado no protocolo deles; usam BERT-large e pooling/cabeças diferentes. Peters et al. (2019) mostram dependência de tarefa na comparação geral. Ver RESEARCH.md, R15–R16; não presumir equivalência com nossos modelos nem necessidade de executar ambos.
- **Cuidado de escopo:** não adicionar automaticamente os dois regimes como experimento; isso ampliaria o número de condições e treinamentos.
- **Referências:** RESEARCH.md, R14; proposta.md e PLAN.md, D11–D12.
- **Resposta do professor:** pendente. A especificação exige Transformers, mas não determina explicitamente atualização de todos os pesos; a aceitação do desvio em relação à redação da proposta deve ser confirmada.

## Como manter este registro

Adicionar perguntas com contexto, decisão relacionada e referências. Após a conversa, registrar a resposta e sua data a partir do relato do autor, distinguindo recomendação docente de interpretação. Mudanças no PLAN.md continuam dependendo de confirmação do autor.
