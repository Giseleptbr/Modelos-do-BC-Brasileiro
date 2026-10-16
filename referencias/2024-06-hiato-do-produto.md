# Medidas de hiato do produto no Brasil

**Fonte.** Banco Central do Brasil, *Relatório de Inflação*, junho de 2024,
boxe 10.
<https://www.bcb.gov.br/content/ri/relatorioinflacao/202406/ri202406b10p.pdf>

**Entra em:** Módulo 4, aulas 17 ("O que não se observa") e 19 ("As medidas que
o BCB publica").

> ⚠️ Transcrição automática. Números de tabela conferidos na extração;
> equações não aparecem neste boxe, que é descritivo.

## O que o documento afirma

O BCB não tem *uma* medida de hiato do produto: calcula **doze**, em dois grupos.

**Univariadas (7)** — só usam o PIB:
tendência quadrática com quebras (Bai e Perron, 2003), tendência não
paramétrica, Hodrick-Prescott, filtro de tendência ℓ₁ (Kim et al., 2009), HP
modificado (Andrle, 2013), filtro band-pass (Christiano e Fitzgerald, 2003) e
Beveridge-Nelson na variante de Kamber, Morley e Wong (2018).

**Multivariadas (5)** — usam mais informação:
função de produção por combinação simples, função de produção com Areosa (2008),
função de produção no estilo do CBO americano (Shackleton, 2018), modelo
bayesiano de fatores dinâmicos (Jarocinski e Lenza, 2018) e componentes
principais.

## O número que sustenta a aula

Para **2024T1**, as doze estimativas vão de **−0,28% a 2,37%**. Média 0,63%,
mediana 0,40%, quartis −0,08% e 1,13%.

Ou seja: a mesma economia, no mesmo trimestre, medida pelos métodos que o
próprio Banco Central usa, pode estar com o produto abaixo ou bem acima do
potencial. **Esse intervalo é a aula 17 inteira.**

Dispersão histórica (2003T2–2024T1): distância média entre as medidas extremas
de **4,25 p.p.**; entre o primeiro e o terceiro quartil, **1,31 p.p.**

Para comparação, o Questionário Pré-Copom de junho de 2024 trazia mediana de
0,3% para 2024T1, com quartis −0,1% e 0,7% — isto é, o mercado concentra-se mais
do que o leque de métodos do próprio BCB.

## O problema de fim de amostra, com evidência

A Tabela 1 compara as estimativas calculadas com dados observados contra as
calculadas estendendo a série com a mediana do Focus. Para 2024T1:

- tendência não paramétrica: de **3,67% para −0,04%**;
- filtro ℓ₁: de **1,75% para 0,47%**;
- HP, band-pass e Beveridge-Nelson: praticamente não se movem.

Acrescentar previsões futuras ao fim da série muda o hiato do *presente* em
quase 4 pontos percentuais em um dos métodos. É a demonstração mais limpa
possível de por que o filtro estatístico é frágil justamente onde a política
monetária precisa de precisão — e o argumento para tratar o hiato como variável
latente dentro do modelo, como fazem os semiestruturais.

## Amostra

- Univariadas: PIB trimestral de 1996T1 a 2024T1. Extensão até 2028T4 com a
  mediana do Focus de 14/06/2024, interpolada a partir de 2026T2.
- Multivariadas: 2001T1–2024T1 (Gráfico 2); 2003T2–2024T1 (Gráfico 3, Tabela 2).

## Referências que o curso vai usar

Da lista de 21 do boxe, estas entram diretamente nas aulas:

- Orphanides, A.; van Norden, S. (2002). The Unreliability of Output-Gap
  Estimates in Real Time. *Review of Economics and Statistics*, 84(4).
  — o artigo que fundamenta a aula 17.
- Hamilton, J. (2018). Why You Should Never Use the Hodrick-Prescott Filter.
  *Review of Economics and Statistics*, 100(5).
  — contraponto direto ao `util.hiato_hp` do repositório.
- Kamber, G.; Morley, J.; Wong, B. (2018). Intuitive and reliable estimates of
  the output gap from a Beveridge-Nelson filter. *Review of Economics and
  Statistics*, 100(3).
- Cusinato, R. T.; Minella, A.; Pôrto Júnior, S. (2013). Output gap in Brazil: a
  real-time data analysis. *Empirical Economics*, 44(3).
  — o caso brasileiro do problema de tempo real.
- Jarocinski, M.; Lenza, M. (2018). An inflation-predicting measure of the output
  gap in the euro area. *Journal of Money, Credit and Banking*, 50(6).
- Areosa, M. (2008). Combining Hodrick-Prescott Filtering with a Production
  Function Approach to Estimate Output Gap. BCB, Trabalho para Discussão 172.
- Fasolo, A. M.; Araújo, E.; Valli Jorge, M.; Kornelius, A.; Marinho, L. S. G.
  (2023). Brazilian Macroeconomic Dynamics Redux. BCB, Trabalho para Discussão 578.
  — útil também no Módulo 5.

## Exercício que nasce daqui

Reproduzir três das medidas univariadas (HP, band-pass e ℓ₁) com o PIB do IBGE e
comparar a dispersão com a reportada pelo BCB. Depois refazer com a série
estendida pelo Focus e medir quanto o hiato do último trimestre se move. É a
Aula 22, e o resultado esperado já está publicado — dá para verificar se a
implementação está certa.
