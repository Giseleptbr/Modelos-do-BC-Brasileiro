# Modelos do Banco Central

Curso em notebooks sobre o sistema de projeções que sustenta o **Relatório de
Política Monetária** do Banco Central do Brasil.

O Relatório traz uma projeção de inflação e um leque em volta dela. Por trás do
número trabalha uma pilha de modelos que se checam. Este repositório abre essa
pilha peça por peça — e reimplementa cada peça em Python, com dados reais do
BCB e do IBGE, até reproduzir a lógica de uma projeção condicional completa.

> **Aviso.** Projeto educacional e independente. Não é o modelo oficial do BCB,
> não reproduz os coeficientes proprietários da instituição e não tem relação
> com o Banco Central do Brasil. É uma reconstrução didática a partir da
> documentação pública — Relatórios de Política Monetária, boxes metodológicos
> e Trabalhos para Discussão —, cujas fontes estão citadas aula por aula.

## O que se aprende

- **Modelo semiestrutural**: curvas IS e de Phillips, expectativas e regra de Taylor.
- **Modelo desagregado**: preços livres, administrados e o repasse cambial por setor.
- **Hiato do produto e juro neutro**: a virada metodológica de 2020, pela intuição.
- **Samba, o DSGE do Banco Central**: de que choques vem a inflação.
- **Satélites e VARs**: as peças que completam o sistema.
- **Operar modelos com IA**: a diferença entre skill, MCP e agente.

## Programa

| Módulo | Tema | Aulas |
|---|---|---|
| 1 | O sistema de projeções do Banco Central | 01–04 |
| 2 | O modelo semiestrutural agregado | 05–11 |
| 3 | O modelo desagregado e o repasse cambial | 12–16 |
| 4 | Variáveis latentes: a virada de 2020 | 17–22 |
| 5 | Samba: o DSGE do Banco Central | 23–27 |
| 6 | Preços administrados, expectativas e VARs | 28–33 |
| 7 | Operar a máquina com inteligência artificial | 34–39 |

São 39 aulas: 24 conceituais e 15 de implementação. `PLANO.md` traz o conteúdo
de cada uma e o estado de execução.

## Instalação

```bash
git clone https://github.com/Giseleptbr/Modelos-do-BC-Brasileiro.git
cd Modelos-do-BC-Brasileiro

python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[notebooks]"

python scripts/verificar_series.py    # confere os códigos de série contra o BCB
jupyter lab
```

Para os módulos 4 e 5, que estimam variáveis latentes: `pip install -e ".[bayes]"`.

## Como o repositório está organizado

```
src/modelosbc/        pacote do curso — importado por todos os notebooks
  config.py           caminhos, cache, parâmetros de rede, meta de inflação
  dados/
    catalogo.py       o que é cada série, com unidade e procedência
    sgs.py            Sistema Gerenciador de Séries Temporais (BCB)
    focus.py          expectativas de mercado (API Olinda)
    sidra.py          aberturas do IPCA por grupo (IBGE)
    _http.py          rede com retentativa e cache em parquet
  modelos/            os modelos de cada módulo (semiestrutural, DSGE, VAR)
  util.py             acumulação em 12 meses, anualização, hiato, defasagens
  viz.py              sistema visual único: linhas, leque, barras, claro/escuro
modulos/NN-nome/      notebooks numerados por aula
solucoes/             gabaritos dos exercícios
referencias/          fichas de leitura das fontes do BCB
scripts/              utilitários de manutenção
dados/cache/          baixado das APIs — não versionado
dados/seed/           amostras versionadas, para o curso rodar offline
```

Duas regras sustentam o resto:

1. **Nenhum notebook chama API diretamente.** Todo acesso passa por
   `modelosbc.dados`, que guarda parquet em `dados/cache/`. A primeira execução
   baixa; as seguintes leem do disco. O curso continua rodando com a API do BCB
   fora do ar.
2. **Nenhum notebook define cor ou estilo.** Todo gráfico sai de `modelosbc.viz`,
   para que a convenção visual — onde fica a meta, onde começa a projeção — seja
   a mesma nas 39 aulas.

## Uso

```python
from modelosbc import dados, util, viz

ipca = dados.sgs.serie("ipca_mensal", inicio="2015-01-01")
ax = viz.linha(util.acumular_12m(ipca), "IPCA em 12 meses", unidade="% a.a.")
viz.marcar_meta(ax)
viz.fonte(ax, "Fonte: BCB/SGS, série 433. Elaboração própria.")
```

## Fontes de dados

| Fonte | O que fornece | Endpoint |
|---|---|---|
| BCB/SGS | IPCA, Selic, câmbio, IBC-Br | `api.bcb.gov.br/dados/serie/...` |
| BCB/Olinda | expectativas da pesquisa Focus | `olinda.bcb.gov.br/olinda/servico/Expectativas/...` |
| IBGE/SIDRA | IPCA por grupo, subgrupo e item | `apisidra.ibge.gov.br/values/...` |

## Licença

Código sob MIT. Textos, notebooks e figuras sob
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pt-br).
Os dados pertencem ao Banco Central do Brasil e ao IBGE, nos termos de cada
instituição.
