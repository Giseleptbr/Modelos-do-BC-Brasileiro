# Plano de produção

Estado de cada aula e as decisões que valem para o curso inteiro. Este arquivo é
a memória do projeto: quem retomar o trabalho — pessoa ou agente — lê daqui.

Legenda: `[ ]` a fazer · `[~]` em produção · `[x]` pronto e executado de ponta a ponta

## Decisões firmadas

1. **Calibrar no Módulo 2, estimar no Módulo 4.** O semiestrutural agregado usa
   coeficientes publicados pelo BCB nos boxes do Relatório. Assim a projeção
   reproduzida pode ser comparada ao número oficial, e o notebook roda em
   segundos. Estimação entra no Módulo 4, onde é o próprio assunto.
2. **Samba é reimplementado, não copiado.** Não há código oficial público. O
   Módulo 5 constrói um DSGE novo-keynesiano pequeno com calibração brasileira,
   em Python puro (sem Dynare), e explicita o que o Samba real tem a mais:
   economia aberta, dois setores produtivos, famílias ricardianas e não
   ricardianas, bens administrados.
3. **Frequência trimestral no núcleo.** O sistema de projeções do BCB trabalha
   em trimestre. Séries mensais e diárias são agregadas explicitamente em
   `util.para_trimestral`, nunca dentro do carregador.
4. **Toda aula cita a fonte.** Equação, coeficiente ou número que venha do BCB
   entra com referência ao documento e à data. Ficha de leitura em
   `referencias/`.
5. **Nenhum notebook chama API nem define cor.** Dados por `modelosbc.dados`,
   gráficos por `modelosbc.viz`.

## Fase 0 — Fundação

- [x] Estrutura do repositório e `pyproject.toml`
- [x] `config.py` — caminhos, cache, parâmetros de rede
- [x] `dados/_http.py` — rede com retentativa e cache em parquet
- [x] `dados/catalogo.py` — séries com rótulo, unidade e procedência
- [x] `dados/sgs.py` — cliente do SGS, com fatiamento por período
- [x] `dados/focus.py` — cliente da API de Expectativas (Olinda)
- [x] `dados/sidra.py` — IPCA por grupo (IBGE)
- [x] `util.py` — acumulação, anualização, juro real ex-ante, hiato HP
- [x] `viz.py` — sistema visual, claro e escuro, com leque
- [x] `scripts/verificar_series.py` — confere códigos contra o BCB
- [ ] Rodar `verificar_series.py` e marcar `verificado=True` no catálogo
- [ ] `dados/seed/` — amostras versionadas para execução offline
- [ ] CI que executa os notebooks a cada push

## Fase 1 — Fontes primárias

Índice e estado em `referencias/FONTES.md`.

- [x] RPM set/2026 — projeções do cenário de referência e lista de boxes (parcial: falta a seção de perspectivas e o apêndice metodológico)
- [x] Atualização dos modelos semiestruturais de pequeno porte — RI jun/2024, boxe 12. **Especificação vigente, com os coeficientes estimados.**
- [x] Medidas de hiato do produto no Brasil — RI jun/2024, boxe 10
- [ ] Conferir as equações do boxe 12 no PDF original — a extração automática perdeu a notação
- [ ] Samba — Trabalho para Discussão 239
- [ ] Repasse cambial sob a ótica de um modelo semiestrutural — Estudos Especiais
- [ ] Juro real neutro — RI jun/2024
- [ ] Sistema de análise e projeções do BC — RI mar/2023
- [ ] Modelo desagregado — RI mar/2021; modelo agregado — RI dez/2021
- [ ] Preços administrados — RI set/2017

## Módulo 1 — O sistema de projeções do Banco Central

- [ ] Aula 01 — Por que um sistema de modelos
- [ ] Aula 02 — Anatomia do Relatório de Política Monetária
- [ ] Aula 03 — Da premissa ao número publicado
- [ ] Aula 04 — (implementação) Ambiente e coleta de séries do SGS e da Focus

## Módulo 2 — O modelo semiestrutural agregado

- [ ] Aula 05 — A ideia do semiestrutural
- [ ] Aula 06 — As três equações e o que cada uma afirma
- [ ] Aula 07 — Como se lê um coeficiente
- [ ] Aula 08 — Cenário condicional: congelar a Selic
- [ ] Aula 09 — Por que um leque, e não uma linha
- [ ] Aula 10 — (implementação) O modelo rodando
- [ ] Aula 11 — (implementação) Mexer nas premissas

## Módulo 3 — O modelo desagregado e o repasse cambial

- [ ] Aula 12 — Livres, administrados, comercializáveis e não comercializáveis
- [ ] Aula 13 — Serviços, alimentação e industriais
- [ ] Aula 14 — O repasse cambial por setor
- [ ] Aula 15 — Quando agregado e desagregado divergem
- [ ] Aula 16 — (implementação) A versão setorial fechando com o IPCA

## Módulo 4 — Variáveis latentes: a virada de 2020

- [ ] Aula 17 — O que não se observa
- [ ] Aula 18 — Filtro de Kalman, pela intuição
- [ ] Aula 19 — As medidas que o BCB publica
- [ ] Aula 20 — Estimação bayesiana: o que é um prior
- [ ] Aula 21 — O que muda na projeção
- [ ] Aula 22 — (implementação) Estimar hiato e juro neutro

## Módulo 5 — Samba: o DSGE do Banco Central

- [ ] Aula 23 — Por que um DSGE ao lado do semiestrutural
- [ ] Aula 24 — A estrutura do Samba
- [ ] Aula 25 — A decomposição histórica da inflação
- [ ] Aula 26 — O que se ganha e o que se perde
- [ ] Aula 27 — (implementação) Respostas a impulso e decomposição

## Módulo 6 — Preços administrados, expectativas e VARs

- [ ] Aula 28 — Preços administrados
- [ ] Aula 29 — Expectativas e ancoragem
- [ ] Aula 30 — VARs no curto prazo
- [ ] Aula 31 — VAR com ancoragem de longo prazo
- [ ] Aula 32 — Quando os modelos discordam
- [ ] Aula 33 — (implementação) Painel de modelos concorrentes

## Módulo 7 — Operar a máquina com inteligência artificial

- [ ] Aula 34 — Skill, MCP e agente
- [ ] Aula 35 — O modelo como ferramenta
- [ ] Aula 36 — Alucinação e versionamento de modelo
- [ ] Aula 37 — (implementação) Um MCP para o modelo do Módulo 2
- [ ] Aula 38 — (implementação) O agente auditor dos boxes
- [ ] Aula 39 — (implementação) A cadeia completa

## Padrão de produção por módulo

1. Levantar as fontes primárias e registrar a ficha em `referencias/`.
2. Escrever as aulas conceituais, com figura gerada por código — nada de parede
   de texto, nada de imagem avulsa.
3. Escrever as aulas de implementação sobre a camada de dados já pronta.
4. De um a três exercícios por aula, com gabarito em `solucoes/`.
5. Executar o módulo inteiro em ambiente limpo antes de fechar.
