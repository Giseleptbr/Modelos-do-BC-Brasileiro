"""Cliente do SGS — Sistema Gerenciador de Séries Temporais do Banco Central.

Endpoint:
    https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json

Três detalhes que quebram quem usa o SGS pela primeira vez:

1. Datas vão e voltam em dd/MM/yyyy, não ISO.
2. Valores vêm como string, com ponto decimal, e faltantes vêm como "" — ler
   sem tratar produz uma coluna de texto que parece número.
3. Séries diárias estouram um limite de ~10 anos por requisição e respondem
   com erro. Este módulo fatia o período automaticamente e remonta.
"""

from __future__ import annotations

import pandas as pd

from ..config import INICIO_PADRAO
from . import catalogo
from ._http import baixar_json, com_cache

BASE = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
_ANOS_POR_FATIA = 9  # margem sob o limite de 10 anos das séries diárias


def _formatar(d: pd.Timestamp) -> str:
    return d.strftime("%d/%m/%Y")


def _fatias(inicio: pd.Timestamp, fim: pd.Timestamp) -> list[tuple[pd.Timestamp, pd.Timestamp]]:
    blocos, atual = [], inicio
    while atual <= fim:
        termino = min(atual + pd.DateOffset(years=_ANOS_POR_FATIA), fim)
        blocos.append((atual, termino))
        atual = termino + pd.Timedelta(days=1)
    return blocos


def _baixar_bruto(codigo: int, inicio: pd.Timestamp, fim: pd.Timestamp) -> pd.DataFrame:
    partes = []
    for ini, fi in _fatias(inicio, fim):
        dados = baixar_json(
            BASE.format(codigo=codigo),
            params={"formato": "json", "dataInicial": _formatar(ini), "dataFinal": _formatar(fi)},
        )
        if dados:
            partes.append(pd.DataFrame(dados))
    if not partes:
        return pd.DataFrame(columns=["data", "valor"])

    df = pd.concat(partes, ignore_index=True)
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df["valor"] = pd.to_numeric(df["valor"].replace("", None), errors="coerce")
    return df.dropna(subset=["valor"]).drop_duplicates("data").sort_values("data")


def serie(
    chave: str,
    inicio: str = INICIO_PADRAO,
    fim: str | None = None,
    forcar: bool = False,
) -> pd.Series:
    """Baixa uma série do catálogo e devolve uma `pd.Series` indexada por data.

    O nome da Series é a chave do catálogo, e `.attrs` carrega código, rótulo e
    unidade — assim o gráfico sabe rotular o eixo sem você repetir a unidade.

    >>> ipca = serie("ipca_mensal", inicio="2015-01-01")
    >>> ipca.attrs["unidade"]
    '% a.m.'
    """
    meta = catalogo.buscar(chave)
    ini = pd.Timestamp(inicio)
    fi = pd.Timestamp(fim) if fim else pd.Timestamp.today().normalize()

    df = com_cache(
        nome=f"sgs_{chave}",
        params={"codigo": meta.codigo, "inicio": str(ini.date()), "fim": str(fi.date())},
        construtor=lambda: _baixar_bruto(meta.codigo, ini, fi),
        forcar=forcar,
    )

    s = df.set_index("data")["valor"].rename(chave)
    s.attrs.update(
        codigo=meta.codigo, rotulo=meta.rotulo, unidade=meta.unidade,
        frequencia=meta.frequencia, fonte="BCB/SGS",
    )
    return s


def painel(chaves: list[str], inicio: str = INICIO_PADRAO, fim: str | None = None) -> pd.DataFrame:
    """Várias séries em um DataFrame, alinhadas pela data.

    Não reamostra nada: séries de frequências diferentes ficam com buracos, e
    isso é intencional — agregar diário em mensal é decisão de modelagem, feita
    explicitamente em `modelosbc.util`, não escondida no carregador.
    """
    return pd.concat([serie(c, inicio, fim) for c in chaves], axis=1)
