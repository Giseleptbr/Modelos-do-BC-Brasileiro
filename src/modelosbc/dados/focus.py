"""Cliente da API de Expectativas de Mercado (pesquisa Focus), via Olinda/OData.

Base:
    https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/

Recursos usados no curso:
    ExpectativasMercadoAnuais          — mediana por ano-calendário de referência
    ExpectativaMercadoMensais          — mediana por mês de referência
    ExpectativasMercadoInflacao12Meses — inflação esperada para os 12 meses à frente
    ExpectativasMercadoTop5Anuais      — os cinco respondentes mais acurados

Por que isso importa no curso: a expectativa do Focus não é enfeite, é insumo.
Ela entra na curva de Phillips do modelo semiestrutural e no cenário de
referência do Relatório. Quando a projeção do BCB muda sem que a Selic mude, a
explicação costuma estar aqui.

Atenção a `baseCalculo`: 0 usa as respostas dos últimos 30 dias, 1 usa as dos
últimos 5 dias úteis. O Relatório trabalha com a mediana suavizada; o padrão
deste módulo é 0, e a diferença entre as duas é assunto da Aula 29.
"""

from __future__ import annotations

import pandas as pd

from ._http import baixar_json, com_cache

BASE = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/{recurso}"
_PAGINA = 10_000


def _consultar(recurso: str, filtro: str, campos: list[str], ordenar: str) -> pd.DataFrame:
    """Paginação OData com $skip/$top até a API parar de devolver linhas."""
    linhas, pulo = [], 0
    while True:
        payload = baixar_json(
            BASE.format(recurso=recurso),
            params={
                "$format": "json",
                "$filter": filtro,
                "$select": ",".join(campos),
                "$orderby": ordenar,
                "$top": _PAGINA,
                "$skip": pulo,
            },
        )
        lote = payload.get("value", []) if isinstance(payload, dict) else []
        linhas.extend(lote)
        if len(lote) < _PAGINA:
            break
        pulo += _PAGINA

    df = pd.DataFrame(linhas)
    if not df.empty:
        df["Data"] = pd.to_datetime(df["Data"])
    return df


def anuais(
    indicador: str = "IPCA",
    inicio: str = "2010-01-01",
    base_calculo: int = 0,
    forcar: bool = False,
) -> pd.DataFrame:
    """Expectativas por ano-calendário de referência.

    Colunas: Data (dia da coleta), DataReferencia (ano), Mediana, Media,
    DesvioPadrao, numeroRespondentes.
    """
    filtro = (
        f"Indicador eq '{indicador}' and Data ge '{inicio}' "
        f"and baseCalculo eq {base_calculo}"
    )
    campos = ["Indicador", "Data", "DataReferencia", "Media", "Mediana",
              "DesvioPadrao", "numeroRespondentes"]
    return com_cache(
        nome=f"focus_anuais_{indicador.lower()}_{base_calculo}",
        params={"indicador": indicador, "inicio": inicio, "base": base_calculo},
        construtor=lambda: _consultar(
            "ExpectativasMercadoAnuais", filtro, campos, "Data asc,DataReferencia asc"
        ),
        forcar=forcar,
    )


def inflacao_12_meses(
    suavizada: str = "S",
    inicio: str = "2010-01-01",
    base_calculo: int = 0,
    forcar: bool = False,
) -> pd.DataFrame:
    """Expectativa de IPCA para os 12 meses à frente.

    `suavizada="S"` é a série que o BCB usa na comunicação — ela interpola entre
    anos-calendário em vez de pular no virar do ano. É também a que entra como
    proxy de expectativa nas estimações do curso.
    """
    filtro = (
        f"Indicador eq 'IPCA' and Suavizada eq '{suavizada}' "
        f"and Data ge '{inicio}' and baseCalculo eq {base_calculo}"
    )
    campos = ["Indicador", "Data", "Suavizada", "Media", "Mediana",
              "DesvioPadrao", "numeroRespondentes"]
    return com_cache(
        nome=f"focus_12m_{suavizada}_{base_calculo}",
        params={"suav": suavizada, "inicio": inicio, "base": base_calculo},
        construtor=lambda: _consultar(
            "ExpectativasMercadoInflacao12Meses", filtro, campos, "Data asc"
        ),
        forcar=forcar,
    )


def mediana_por_referencia(df: pd.DataFrame, data_coleta: str | None = None) -> pd.Series:
    """Fotografia das expectativas em uma data: mediana por ano de referência.

    É assim que se monta o cenário de mercado de um Relatório específico —
    usando a coleta mais próxima da data de corte do documento, não a de hoje.
    """
    if df.empty:
        return pd.Series(dtype=float)
    alvo = pd.Timestamp(data_coleta) if data_coleta else df["Data"].max()
    disponiveis = df.loc[df["Data"] <= alvo, "Data"]
    if disponiveis.empty:
        raise ValueError(f"Não há coleta do Focus em ou antes de {alvo.date()}.")
    corte = disponiveis.max()
    foto = df[df["Data"] == corte]
    return foto.set_index("DataReferencia")["Mediana"].sort_index()
