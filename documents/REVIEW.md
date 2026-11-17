O desenho científico é defensável, mas O2–O4 e O8–O9 precisam de ajustes antes de serem tratados como protocolo executável fechado. Não encontrei vazamento inevitável, erro na fórmula de O7 ou motivo suficiente para reabrir D1–D43. Nenhum arquivo foi alterado.

1. Alta — risco condicional: recuperação de falhas pode alterar as repetições.
   Local: O2 (PLAN.md:455), O3 e O9 (PLAN.md:531).
   Problema: salvar o melhor checkpoint não define como retomar uma execução interrompida. Faltam estado do otimizador, scheduler, GradScaler, geradores aleatórios e posição no treinamento — ou uma regra explícita de reinício integral. Também não está delimitado quais execuções devem ser refeitas quando uma correção muda o treinamento.
   Consequência: uma “continuação” pode seguir outra trajetória; corrigir apenas execuções que falharam pode produzir condições diferentes entre modelos/seeds.
   Correção: escolher previamente entre reinício integral com mesma configuração/seed ou retomada completa verificável; preservar tentativas e artefatos anteriores. Correções que mudem resultados devem invalidar todas as execuções afetadas. Não substituir seeds problemáticas nem tratar baixo desempenho, sozinho, como falha técnica.
2. Média — incompatibilidade demonstrável quando AMP pula passos: scheduler versus cinco épocas.
   Local: O3, linha 469 (PLAN.md:469), D24/D26.
   Problema: o horizonte usa atualizações planejadas, mas o scheduler avança somente nas efetivas. Com passos pulados, cinco épocas terminam antes desse horizonte; portanto, o decaimento não chega necessariamente a zero. Isso decorre diretamente das regras propostas; o salto de atualizações é comportamento documentado do GradScaler (https://docs.pytorch.org/docs/2.15/notes/amp_examples.html).
   Consequência: modelos podem terminar com quantidades de atualizações e taxas finais diferentes, embora o texto prometa o mesmo esquema completo.
   Correção: explicitar essa exceção e registrar passos efetivos/taxa final, ou definir outra política antes do treino. Não acrescentar passos automaticamente para compensar: isso alteraria o orçamento de D24. Incluir um check com atualização pulada.
3. Média — problema demonstrável no diagnóstico; efeito sobre a escolha é condicional.
   Local: O4, linhas 479–485 (PLAN.md:479).
   Problema: vinte lotes medidos processam 160, 320 ou 640 exemplos conforme o batch. Em uma sequência fixa de 512 mensagens, os candidatos medem trechos e repetições diferentes. Além disso, reservar 128 posições às mensagens mais longas torna a amostra deliberadamente diferente do treino completo.
   Consequência: diferenças de comprimento podem ser confundidas com ganho de throughput; a projeção de duração não é necessariamente representativa.
   Correção: medir passagens completas sobre os mesmos exemplos após aquecimento separado; distinguir benchmark de seleção, stress e estimativa de duração. Fixar também seed, taxa, scheduler e escala inicial usados no diagnóstico, atualmente não especificados. Preserva D27.
4. Média — risco condicional: três passos pulados não bastam para caracterizar estabilidade numérica.
   Local: O3, linhas 470–472 (PLAN.md:470).
   Problema: a regra interrompe três saltos consecutivos, mas permite muitos saltos intercalados. Também não distingue ajuste inicial da escala de instabilidade persistente. A documentação explica como AMP detecta gradientes inválidos e pula atualizações; não sustenta esse limite de três como diagnóstico suficiente. Fonte: PyTorch (https://docs.pytorch.org/docs/2.15/notes/amp_examples.html).
   Consequência: rejeitar uma configuração recuperável ou aceitar treinamento com muitas atualizações perdidas.
   Correção: separar fase inicial e janela medida; registrar fração total de saltos, escala e quantidade de atualizações válidas. Fechar o critério de aceitação antes dos treinamentos científicos, sem escolher pela acurácia.
5. Média — lacuna de verificação: superar a classe majoritária é um controle fraco.
   Local: O8, linhas 522–524 (PLAN.md:522).
   Problema: esse baseline detecta colapso grosseiro, mas um pipeline parcialmente quebrado pode superá-lo. Os checks previstos não explicitam identidade do mapeamento rótulo↔ID entre splits/modelos nem equivalência das previsões antes/depois de recarregar o checkpoint.
   Consequência: obter números plausíveis sem garantir avaliação correta ou reprodução dos resultados salvos.
   Correção: manter o baseline e acrescentar essas verificações focadas, além de um pequeno teste de aprendizado no treino durante o diagnóstico. Investigações motivadas por desempenho devem ocorrer no desenvolvimento; o teste final não pode virar critério para “consertar” resultados desfavoráveis.
6. Média para a entrega — divergência documental, sem invalidar o experimento.
   Local: D1/D10, O9 (PLAN.md:527), proposta.md (proposta.md:1).
   Problema: a proposta ainda promete compreensão financeira corporativa e comparação de “arquiteturas”; o plano avalia checkpoints em intenções bancárias. O9 também não explicita formato SBC e exclusão das referências da contagem de páginas.
   Consequência: artigo ou apresentação podem prometer mais que os dados demonstram ou descumprir requisitos formais.
   Correção: alinhar a descrição final a D1/D10, verificar o status da aprovação docente e incluir no encerramento: SBC, 8–10 páginas sem referências, código reproduzível e apresentação de exatamente 15 minutos. São requisitos de spec.md (spec.md:51), não novas decisões experimentais.

Pontos conferidos que não considero falhas:

- Treino/validação/teste: D18 reutiliza validação, mas O5/O6 preservam avaliação independente do procedimento congelado. Isso permite sobreajuste à validação, não demonstra vazamento ao teste. Não recomendo criar outra divisão por obrigação; resultados de validação devem permanecer diagnósticos. Cawley e Talbot (https://jmlr.org/papers/v11/cawley10a.html).
- Checkpoints e três repetições: seleção por época, taxa pela média e reporte das três seeds são coerentes. A dispersão descreve variação do treinamento naquele split, não toda a incerteza experimental. D41 já impede transformar isso em significância.
- Comparabilidade: D10 limita corretamente as conclusões ao sistema completo. O artigo FinBERT distingue variantes continuadas e treinadas do zero; tamanho de vocabulário não comprova sozinho toda a procedência do checkpoint. A auditoria prevista continua necessária, sem justificar troca de modelo. Yang et al., §4 (https://arxiv.org/html/2006.08097).
- O7 está matematicamente correto: em um bloco empatado, o número esperado de erros nos primeiros j elementos é j·e/m; o denominador é fixo. No exemplo, as duas AURCs são 1/9 e 5/18, cuja média é 7/36. Trata-se de ranking esperado, não de limiar operacional — distinção já presente no plano.
- Limiares, AURC e ECE: O6 trata corretamente igualdade e cobertura efetiva. AURC não isola qualidade da confiança entre classificadores; ECE não mede qualidade do ranking. As ressalvas estão adequadas às fontes: Cattelan e Silva (https://arxiv.org/html/2305.15508v4) e Guo et al. (https://proceedings.mlr.press/v70/guo17a/guo17a.pdf). Não encontrei alegação central mais forte que essas fontes.

Antes de implementar: fechar recuperação de falhas, semântica do scheduler e protocolo comparável do diagnóstico; incorporar os checks faltantes e aprovar O1–O9.

Durante o diagnóstico: resolver versões, pooler, comprimentos, duplicatas/sobreposição, memória, precisão e duração. Esses são riscos condicionais já reconhecidos, não defeitos demonstrados nos dados. Excedentes no teste continuam sujeitos à parada e revisão previstas em D31/D42; não autorizam truncamento ou ajuste silencioso.