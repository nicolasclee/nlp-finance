# Notas conceituais para estudo e apresentação

Explicações discutidas na sessão; não substituem decisões do PLAN.md. Texto de apoio, a revisar e adaptar com palavras próprias no artigo.

## Classificação de intenções com encoder e camada linear

- **Tokenizer:** divide texto em tokens, inclui marcadores e gera IDs/máscaras. Não produz sozinho a representação semântica contextual da mensagem.
- **Encoder Transformer:** transforma entradas em representações contextuais por token. A representação final de CLS pode alimentar a classificação; sua utilidade para a tarefa é aprendida no ajuste supervisionado, não um resumo perfeito garantido.
- **Proposta discutida:** vetor de mensagem com 768 valores → camada linear de 77 classes → logits → softmax. CLS, pooling/pooler e detalhes da cabeça ainda dependem de confirmação.

### Nomes e cálculo

- Nome: **classificador linear multiclasse com softmax**, ou cabeça de classificação linear (*linear classification head*).
- Sobre representações fixas, essa saída corresponde à regressão logística multinomial. Com fine-tuning completo, o sistema inteiro é uma rede não linear; apenas a cabeça é linear em relação à representação que recebe.
- Operação: `z = W h + b`.
- `h`: vetor da mensagem, 768 valores.
- `W`: matriz de pesos com 77 linhas e 768 colunas; uma linha por intenção.
- `b`: vetor com 77 vieses.
- `z`: vetor com 77 **logits**, números reais sem restrição a [0,1]. Cada logit é um escalar.
- Softmax transforma todos os logits em 77 probabilidades estimadas que somam 1; isso não garante calibração.
- Treinamento por entropia cruzada compara logits e rótulo verdadeiro. Gradientes e otimizador ajustam cabeça e encoder no regime completo confirmado em D13.

### Intuição geométrica

Cada vetor de pesos atua como detector aprendido. Produto escalar e viés pontuam quanto a representação favorece cada classe. Não se trata de procurar automaticamente o exemplo de intenção mais próximo por cosseno. Em relação a h, empates entre pares de logits definem fronteiras lineares; a transformação do texto em h é não linear.

Exemplo fictício em duas dimensões, omitindo vieses: h=[2,1], pesos da classe A=[1,0] e da B=[0,1] produzem logits [2,1]. Softmax resulta em aproximadamente [0,731;0,269]. A dimensionalidade reduzida é apenas didática.

### Frase técnica para apresentação

“A arquitetura proposta usa a representação contextual de CLS como entrada de uma camada linear para 77 intenções, com softmax na obtenção das probabilidades e entropia cruzada no treinamento.”

Fonte: Devlin et al. (2019), [BERT, §3.2 e §4.1](https://aclanthology.org/N19-1423.pdf); RESEARCH.md, R17. Essa referência fundamenta o mecanismo, não comprova que seja o melhor para nossa tarefa.

## Alternativa: classificar por exemplos semelhantes

Outra estratégia representa a mensagem e exemplos rotulados em vetores e usa suas similaridades para inferir a intenção. Essa é a família mais próxima da intuição de comparar mensagens no espaço vetorial. Não equivale a aplicar cosseno indiscriminadamente ao CLS de qualquer checkpoint.

Sentence-BERT é referência para aprender embeddings de sentenças comparáveis por cosseno. Mehri e Eric (2021) propõem predição de intenções orientada por exemplos, avaliada inclusive em BANKING77. Fontes e limites em RESEARCH.md, R18.

Alternativas discutidas por curiosidade não são condições adicionais do experimento.
