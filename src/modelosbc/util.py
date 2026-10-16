"""Transformações que aparecem em todo o curso.

Nada aqui é esotérico, mas todas são decisões de modelagem que costumam ficar
implícitas. Explicitá-las em funções nomeadas evita que o mesmo conceito apareça
de três jeitos diferentes em três notebooks.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

TRIM_POR_ANO = 4
MESES_POR_ANO = 12


def acumular_12m(mensal: pd.Series) -> pd.Series:
    """Acumula uma variação mensal em % para a variação em 12 meses.

    Composto, não soma: (1+π₁)(1+π₂)…(1+π₁₂) − 1. A soma simples erra pouco com
    inflação baixa e erra feio com inflação alta — e o curso passa por 2002 e
    2015.
    """
    fator = 1 + mensal / 100
    return (fator.rolling(MESES_POR_ANO).apply(np.prod, raw=True) - 1) * 100


def anualizar(mensal: pd.Series) -> pd.Series:
    """Converte variação mensal em % para taxa anualizada em %."""
    return ((1 + mensal / 100) ** MESES_POR_ANO - 1) * 100


def desanualizar(anual: pd.Series | float) -> pd.Series | float:
    """Inverso de `anualizar`: taxa anual em % para equivalente mensal em %."""
    return ((1 + np.asarray(anual) / 100) ** (1 / MESES_POR_ANO) - 1) * 100


def para_trimestral(s: pd.Series, como: str = "media") -> pd.Series:
    """Agrega série mensal ou diária em trimestral.

    `como="media"` para taxas e índices de nível; `como="composto"` para
    variações percentuais, que precisam ser compostas e não promediadas.
    O modelo semiestrutural do BCB trabalha em frequência trimestral — é esta
    função que leva os dados até lá.
    """
    g = s.resample("QE")
    if como == "media":
        return g.mean()
    if como == "fim":
        return g.last()
    if como == "composto":
        return (g.apply(lambda x: np.prod(1 + x / 100)) - 1) * 100
    raise ValueError("`como` deve ser 'media', 'fim' ou 'composto'.")


def juro_real_ex_ante(selic_nominal: pd.Series, expectativa_12m: pd.Series) -> pd.Series:
    """Juro real ex-ante pela relação de Fisher, em % a.a.

    Ex-ante usa a inflação *esperada*, não a observada. Essa escolha não é
    detalhe: é o juro real ex-ante que entra na curva IS, porque é ele que o
    agente enxerga quando decide consumir ou investir hoje.
    """
    alinhado = pd.concat([selic_nominal, expectativa_12m], axis=1).dropna()
    i, pi = alinhado.iloc[:, 0], alinhado.iloc[:, 1]
    return ((1 + i / 100) / (1 + pi / 100) - 1) * 100


def hiato_hp(log_pib: pd.Series, lamb: float = 1600) -> pd.DataFrame:
    """Hiato do produto pelo filtro HP — a referência ingênua do curso.

    Existe aqui para ser comparado, não para ser usado como verdade. O HP sofre
    de viés de fim de amostra justamente onde a política monetária precisa de
    precisão (o presente), e esse defeito é o ponto de partida do Módulo 4,
    onde o hiato vira variável latente estimada dentro do modelo.

    λ=1600 é a convenção para dados trimestrais.
    """
    from statsmodels.tsa.filters.hp_filter import hpfilter

    ciclo, tendencia = hpfilter(log_pib.dropna(), lamb=lamb)
    return pd.DataFrame({"tendencia": tendencia, "hiato": ciclo * 100})


def defasar(df: pd.DataFrame, colunas: list[str], defasagens: int = 1) -> pd.DataFrame:
    """Acrescenta defasagens nomeadas (`x_l1`, `x_l2`) a um DataFrame."""
    saida = df.copy()
    for col in colunas:
        for k in range(1, defasagens + 1):
            saida[f"{col}_l{k}"] = saida[col].shift(k)
    return saida


def erro_quadratico_medio(observado: pd.Series, previsto: pd.Series) -> float:
    """RMSE entre duas séries, alinhadas pela interseção das datas."""
    par = pd.concat([observado, previsto], axis=1).dropna()
    return float(np.sqrt(((par.iloc[:, 0] - par.iloc[:, 1]) ** 2).mean()))
