# Atualização dos modelos semiestruturais de pequeno porte

**Fonte.** Banco Central do Brasil, *Relatório de Inflação*, junho de 2024,
boxe 12, p. 97–107.
<https://www.bcb.gov.br/content/ri/relatorioinflacao/202406/ri202406b12p.pdf>

**Entra em:** Módulo 2 (modelo agregado) e Módulo 3 (modelo desagregado).

> ⚠️ **Transcrição automática.** As tabelas de coeficientes abaixo vieram
> limpas da extração. As **equações, não**: a notação matemática se perdeu na
> conversão do PDF. Antes de escrever a Aula 06 e a Aula 10, as equações
> precisam ser lidas no PDF original e transcritas à mão.

## O que o documento afirma

O BCB mantém **duas versões** do modelo semiestrutural de pequeno porte, que
compartilham quase todas as equações e diferem apenas no bloco de inflação de
preços livres:

- **agregado** — uma curva de Phillips para o conjunto dos preços livres;
- **desagregado** — três curvas de Phillips: bens industriais, alimentação no
  domicílio e serviços.

O boxe documenta a revisão de 2024 das duas versões.

## Estrutura

| Bloco | O que determina | Principais regressores |
|---|---|---|
| Curva de Phillips | inflação de preços livres | inércia, expectativas, inflação importada de *commodities*, câmbio, hiato do produto, anomalias climáticas (El Niño/La Niña) |
| Curva IS | hiato do produto | defasagens do próprio hiato, hiato de juro real (Selic Focus menos inflação Focus 12 meses), resultado primário ajustado ao ciclo, hiato do produto mundial, choque AR(1) |
| Regra de Taylor | Selic | defasagens da própria Selic e desvio da inflação esperada em relação à meta — **sem o hiato do produto** |
| Paridade descoberta (UIP) | câmbio | diferencial de juros contra *Fed Funds*, prêmio de risco pelo CDS de 5 anos, termo de longo prazo pela PPC (depreciação de longo prazo = meta doméstica menos 2%) |
| Expectativas | expectativa 4 trimestres à frente | expectativa defasada, inflação passada e termo consistente com o modelo |
| Hiato como variável latente | — | quatro indicadores carregam em um componente cíclico comum: PIB, Nuci, desemprego e empregos formais do Novo Caged, com erro de medida σₕ |

Três coisas aqui merecem destaque em aula:

1. **A regra de Taylor não tem hiato.** O BCB a especifica reagindo só ao desvio
   da inflação esperada. Isso contraria o livro-texto e é um bom gancho para a
   Aula 07.
2. **O hiato não é um dado, é um estado estimado** dentro do modelo, a partir de
   quatro indicadores observados. É a virada que o Módulo 4 destrincha.
3. **O câmbio de longo prazo vem da PPC**, não de previsão de mercado — por isso
   o cenário do Relatório não é "o que o mercado acha que o dólar vai fazer".

## O que mudou em 2024

- Phillips agregada: defasagem do câmbio caiu de dois trimestres para um.
- Phillips de bens industriais (desagregado): entrou o Índice de Pressão nas
  Cadeias de Suprimentos Brasileiras, restrito a 2020T4–2022T3.
- Phillips de alimentação (desagregado): entrou um termo de erro MA(1), com
  coeficiente estimado negativo, capturando reversão mais rápida dos choques de
  alimentos.
- Curva IS: saiu o índice de incerteza econômica; o choque da IS ganhou
  persistência AR; entraram termos de erro com variância calibrada alta para
  2008T4–2009T4 e 2020T1–2020T4.
- Juro real de equilíbrio: passou a ser decomposto em um componente muito
  persistente e uma tendência HP do juro real do Focus — e a regra de Taylor usa
  um componente persistente próprio, distinto do da IS.
- Caiu a ligação entre IS e regra de Taylor que existia nas versões de 2021.

## Estimação

- **Método:** bayesiano, com *priors* majoritariamente não informativos
  (uniformes; beta para o termo fiscal).
- **Amostra:** trimestral, 2003T4 a 2023T4.
- **Pandemia:** variâncias de erro calibradas mais altas nas curvas de Phillips
  entre 2020T2 e 2022T4, seguindo Lenza e Primiceri (2022).
- **Reportado:** moda a posteriori e intervalo de credibilidade de 90%. Não há
  erro-padrão.

## Coeficientes — modelo agregado (Tabela 1)

Moda [intervalo de credibilidade de 90%]:

| Bloco | Parâmetro | Moda | IC 90% |
|---|---|---|---|
| Phillips | α1L | 0,24 | [0,02; 0,38] |
| Phillips | α1I | 0,38 | [0,13; 0,69] |
| Phillips | α2 | 0,023 | [0,006; 0,039] |
| Phillips | α3 | 0,011 | [0; 0,025] |
| Phillips | α4 | 0,120 | [0,072; 0,198] |
| IS | β1 | 0,85 | [0,70; 0,95] |
| IS | β2 | 0,44 | [0,21; 0,66] |
| IS | β3 | 0,030 | [0,027; 0,032] |
| IS | β4 | 0,054 | [0; 0,23] |
| IS | β5 | 0,84 | [0,59; 0,99] |
| Taylor | θ1 | 1,48 | [1,41; 1,54] |
| Taylor | θ2 | −0,58 | [−0,63; −0,52] |
| Taylor | θ3 | 2,03 | [1,47; 2,64] |
| Expectativas | φ1 | 0,75 | [0,68; 0,82] |
| Expectativas | φ2 | 0,11 | [0,06; 0,13] |
| Expectativas | φ3 | 0,021 | [0; 0,049] |
| Outros | δ | 1,90 | [0,77; 3,22] |
| Outros | γNuci | 1,87 | [1,65; 2,12] |
| Outros | γemp | 1,10 | [0,96; 1,25] |
| Outros | γCaged | 0,69 | [0,61; 0,79] |
| Outros | σₕ | 1,09 | [0,98; 1,21] |

**Pendente:** associar cada letra grega à sua posição na equação. A extração
perdeu as fórmulas, então o mapeamento parâmetro ↔ regressor precisa sair do
PDF antes da calibração.

## Coeficientes — modelo desagregado (Tabela 2)

| Curva | Parâmetro | Moda | IC 90% |
|---|---|---|---|
| Bens industriais | α1 (inércia) | 0,43 | [0,252; 0,598] |
| Bens industriais | α6 (hiato) | 0,079 | [0,017; 0,15] |
| Bens industriais | α5 (cadeias de suprimentos) | 0,23 | [0; 0,45] |
| Alimentação no domicílio | α1 (inércia) | 0,53 | [0,12; 0,63] |
| Alimentação no domicílio | α4 (hiato) | 0,073 | [0; 0,22] |
| Alimentação no domicílio | α7 (MA(1)) | −0,50 | [−0,62; −0,01] |
| Serviços | α1 (inércia do IPCA) | 0,37 | [0,19; 0,55] |
| Serviços | α2 (inércia setorial) | 0,30 | [0,104; 0,497] |
| Serviços | α3 (hiato) | 0,13 | [0,095; 0,173] |
| IS | β1 | 0,86 | [0,70; 0,96] |
| IS | β2 | 0,44 | [0,14; 0,69] |
| IS | β3 | 0,030 | [0,027; 0,033] |
| IS | β4 | 0,053 | [0; 0,22] |
| IS | β5 | 0,83 | [0,56; 1] |
| Taylor | θ1 | 1,48 | [1,41; 1,53] |
| Taylor | θ2 | −0,58 | [−0,63; −0,53] |
| Taylor | θ3 | 2,07 | [1,55; 2,70] |
| Expectativas | φ1 | 0,74 | [0,66; 0,79] |
| Expectativas | φ2 | 0,12 | [0,08; 0,15] |
| Expectativas | φ3 | 0,026 | [0,004; 0,056] |
| Outros | δ | 1,95 | [0,73; 3,19] |
| Outros | γNuci | 1,86 | [1,65; 2,12] |
| Outros | γemp | 1,09 | [0,97; 1,25] |
| Outros | γCaged | 0,70 | [0,62; 0,79] |
| Outros | σₕ | 1,10 | [0,98; 1,21] |

Note que os coeficientes de IS, Taylor e expectativas são praticamente idênticos
entre as duas versões — coerente com o que o boxe afirma: só o bloco de preços
livres muda. Isso é um bom teste de sanidade para a reimplementação.

**Aula 15 ("Quando agregado e desagregado divergem") ganha aqui o seu ponto:**
dois modelos com o mesmo motor macro divergem porque a inflação setorial responde
ao hiato com intensidades diferentes — 0,13 em serviços contra 0,073 em
alimentação. Serviços é quase o dobro.

## Referência citada que importa

Lenza, M.; Primiceri, G. E. (2022). How to estimate a vector autoregression
after March 2020. *Journal of Applied Econometrics*, 37(4), 688–699.

## Boxes anteriores citados (a fichar)

- Sistema de análise e projeções do BC — RI mar/2023
- Novo modelo desagregado de pequeno porte — RI mar/2021
- Revisão do modelo agregado de pequeno porte — RI dez/2021
- Reformulação dos modelos de projeção de médio prazo dos preços administrados — RI set/2017
- Modelo agregado de pequeno porte 2017 — RI jun/2017
- Índice de pressão nas cadeias de suprimentos brasileiras — RI set/2022
- Condicionantes de câmbio nas projeções do BCB e a paridade do poder de compra — RI set/2020
- Atualização de medidas de taxa de juros real neutra no Brasil — RI jun/2024
