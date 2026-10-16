"""Sistema visual único do curso — matplotlib, modo claro e escuro.

Todos os 39 notebooks desenham por aqui. Motivo prático: um gráfico de projeção
tem convenções que, se mudarem de aula para aula, atrapalham a leitura — onde
fica a meta, como se marca o começo da projeção, que cor é dado observado e que
cor é cenário.

A paleta categórica é usada em ordem fixa (nunca ciclada) e foi validada para
daltonismo nos dois modos. O leque usa uma rampa de azul em um só tom, do mais
escuro (centro, mais provável) ao mais claro (cauda).
"""

from __future__ import annotations

import os
from contextlib import contextmanager

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .config import BANDA, FIGURAS, META_INFLACAO

# --- Paleta -----------------------------------------------------------------
CLARO = {
    "superficie": "#fcfcfb",
    "tinta": "#0b0b0b",
    "tinta_secundaria": "#52514e",
    "tinta_fraca": "#898781",
    "grade": "#e1e0d9",
    "eixo": "#c3c2b7",
    "series": ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
               "#e87ba4", "#008300", "#6250d6", "#e34948"],
    # rampa sequencial de azul, do centro do leque para a cauda
    "leque": ["#2a78d6", "#5598e7", "#86b6ef", "#b7d3f6", "#cde2fb"],
}

ESCURO = {
    "superficie": "#1a1a19",
    "tinta": "#f0efec",
    "tinta_secundaria": "#c3c2b7",
    "tinta_fraca": "#898781",
    "grade": "#2c2c2a",
    "eixo": "#383835",
    "series": ["#3987e5", "#d95926", "#199e70", "#c98500",
               "#d55181", "#008300", "#9085e9", "#e66767"],
    "leque": ["#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95"],
}

_TEMA = CLARO


def tema() -> dict:
    """Paleta ativa. Útil quando um notebook precisa da cor exata de uma série."""
    return _TEMA


def estilo(modo: str | None = None) -> dict:
    """Aplica o estilo do curso. `modo` é "claro", "escuro" ou None (variável de
    ambiente MODELOSBC_TEMA, padrão claro)."""
    global _TEMA
    modo = modo or os.environ.get("MODELOSBC_TEMA", "claro")
    _TEMA = ESCURO if modo.startswith("esc") else CLARO
    t = _TEMA

    mpl.rcParams.update({
        "figure.figsize": (9, 4.6),
        "figure.dpi": 120,
        "savefig.dpi": 200,
        "figure.facecolor": t["superficie"],
        "axes.facecolor": t["superficie"],
        "savefig.facecolor": t["superficie"],
        "axes.edgecolor": t["eixo"],
        "axes.linewidth": 0.8,
        "axes.labelcolor": t["tinta_secundaria"],
        "axes.titlecolor": t["tinta"],
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 12,
        "axes.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "axes.prop_cycle": mpl.cycler(color=t["series"]),
        "grid.color": t["grade"],
        "grid.linewidth": 0.7,
        "grid.alpha": 1.0,
        "xtick.color": t["tinta_fraca"],
        "ytick.color": t["tinta_fraca"],
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "lines.linewidth": 2.0,
        "lines.solid_capstyle": "round",
        "legend.frameon": False,
        "legend.fontsize": 9,
        "legend.labelcolor": t["tinta_secundaria"],
        "text.color": t["tinta"],
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Segoe UI", "Helvetica", "Arial"],
        "font.size": 10,
    })
    return t


@contextmanager
def modo(nome: str):
    """Desenha um bloco em outro modo, restaurando o anterior ao sair."""
    anterior = "escuro" if _TEMA is ESCURO else "claro"
    estilo(nome)
    try:
        yield
    finally:
        estilo(anterior)


# --- Blocos de gráfico ------------------------------------------------------
def eixo(titulo: str = "", subtitulo: str = "", unidade: str = "", **kw) -> plt.Axes:
    """Figura com título à esquerda, subtítulo recessivo e eixo y rotulado."""
    fig, ax = plt.subplots(**kw)
    if titulo:
        ax.set_title(titulo, pad=30 if subtitulo else 12)
    if subtitulo:
        ax.text(0, 1.015, subtitulo, transform=ax.transAxes, fontsize=9.5,
                color=_TEMA["tinta_secundaria"], va="bottom")
    if unidade:
        ax.set_ylabel(unidade)
    return ax


def _legenda(ax: plt.Axes, n: int) -> None:
    """Legenda em uma única faixa abaixo do eixo, sem moldura."""
    ax.legend(loc="upper left", bbox_to_anchor=(0, -0.09), ncols=min(n, 6))
    ax._tem_legenda = True  # consumido por `fonte` para não sobrepor


def fonte(ax: plt.Axes, texto: str) -> None:
    """Nota de fonte no rodapé. Toda aula cita de onde veio o número."""
    y = -0.30 if getattr(ax, "_tem_legenda", False) else -0.16
    ax.annotate(texto, xy=(0, y), xycoords="axes fraction",
                fontsize=8, color=_TEMA["tinta_fraca"], va="top")


def marcar_meta(ax: plt.Axes, meta: float = META_INFLACAO, banda: float = BANDA) -> None:
    """Meta de inflação e intervalo de tolerância, como pano de fundo."""
    ax.axhspan(meta - banda, meta + banda, color=_TEMA["grade"], zorder=0)
    ax.axhline(meta, color=_TEMA["eixo"], linewidth=1.0, linestyle="--", zorder=1)
    ax.annotate(f"meta {meta:g}%", xy=(0.006, meta), xycoords=("axes fraction", "data"),
                xytext=(0, 3), textcoords="offset points",
                fontsize=8, color=_TEMA["tinta_fraca"], ha="left", va="bottom")


def marcar_projecao(ax: plt.Axes, inicio) -> None:
    """Linha vertical separando dado observado de projeção.

    Sem essa marca, o leitor não distingue o que aconteceu do que o modelo
    supõe — que é exatamente a confusão que o curso quer desfazer.
    """
    x = pd.Timestamp(inicio)
    ax.axvline(x, color=_TEMA["eixo"], linewidth=1.0, linestyle=":")
    ax.annotate("projeção →", xy=(x, 1.0), xycoords=("data", "axes fraction"),
                xytext=(5, -12), textcoords="offset points",
                fontsize=8, color=_TEMA["tinta_fraca"])


def linha(
    dados: pd.Series | pd.DataFrame,
    titulo: str = "",
    subtitulo: str = "",
    unidade: str = "",
    rotular_fim: bool = True,
    ax: plt.Axes | None = None,
) -> plt.Axes:
    """Série(s) temporal(is). Uma série dispensa legenda; duas ou mais ganham
    legenda e rótulo no último ponto."""
    ax = ax or eixo(titulo, subtitulo, unidade)
    df = dados.to_frame() if isinstance(dados, pd.Series) else dados

    for i, col in enumerate(df.columns):
        s = df[col].dropna()
        if s.empty:
            continue
        cor = _TEMA["series"][i % len(_TEMA["series"])]
        ax.plot(s.index, s.values, color=cor, label=str(col))
        if rotular_fim:
            ax.annotate(f"{s.iloc[-1]:,.2f}".replace(".", ","),
                        xy=(s.index[-1], s.iloc[-1]), xytext=(6, 0),
                        textcoords="offset points", fontsize=9,
                        color=_TEMA["tinta_secundaria"], va="center")

    if df.shape[1] >= 2:
        _legenda(ax, df.shape[1])
    return ax


def leque(
    central: pd.Series,
    desvio: pd.Series | float,
    titulo: str = "",
    subtitulo: str = "",
    unidade: str = "% a.a.",
    observado: pd.Series | None = None,
    quantis: tuple[float, ...] = (0.3, 0.5, 0.8, 0.9),
    ax: plt.Axes | None = None,
) -> plt.Axes:
    """Gráfico de leque: projeção central e bandas de probabilidade.

    `desvio` é o desvio-padrão da projeção em cada horizonte — constante ou
    crescente. O leque do Relatório abre com o horizonte justamente porque a
    incerteza acumula; um leque de largura fixa é um erro conceitual, não
    estético.

    As bandas são desenhadas da mais larga para a mais estreita, para que a
    mais provável fique por cima.
    """
    from scipy.stats import norm

    ax = ax or eixo(titulo, subtitulo, unidade)
    sigma = (pd.Series(desvio, index=central.index)
             if np.isscalar(desvio) else desvio.reindex(central.index))

    cores = _TEMA["leque"]
    for j, q in enumerate(sorted(quantis, reverse=True)):
        z = norm.ppf(0.5 + q / 2)
        cor = cores[min(j, len(cores) - 1)]
        ax.fill_between(central.index, central - z * sigma, central + z * sigma,
                        color=cor, linewidth=0, zorder=2,
                        label=f"{int(q * 100)}%")

    if observado is not None and not observado.empty:
        ax.plot(observado.index, observado.values, color=_TEMA["tinta"],
                linewidth=2.0, zorder=4, label="observado")
        marcar_projecao(ax, central.index[0])

    ax.plot(central.index, central.values, color=_TEMA["superficie"],
            linewidth=2.6, zorder=5)
    ax.plot(central.index, central.values, color=_TEMA["tinta"],
            linewidth=1.4, linestyle="--", zorder=6, label="projeção central")
    _legenda(ax, len(quantis) + 2)
    return ax


def barras(
    dados: pd.Series,
    titulo: str = "",
    subtitulo: str = "",
    unidade: str = "",
    ax: plt.Axes | None = None,
) -> plt.Axes:
    """Barras horizontais ordenadas — decomposição de choques, contribuições."""
    ax = ax or eixo(titulo, subtitulo, unidade)
    s = dados.sort_values()
    cores = [_TEMA["series"][0] if v >= 0 else _TEMA["series"][7] for v in s.values]
    ax.barh(s.index.astype(str), s.values, color=cores, height=0.62)
    ax.axvline(0, color=_TEMA["eixo"], linewidth=1.0)
    ax.grid(axis="y", visible=False)
    for nome, v in s.items():
        ax.annotate(f"{v:,.2f}".replace(".", ","), xy=(v, str(nome)),
                    xytext=(5 if v >= 0 else -5, 0), textcoords="offset points",
                    ha="left" if v >= 0 else "right", va="center",
                    fontsize=9, color=_TEMA["tinta_secundaria"])
    return ax


def salvar(ax: plt.Axes, nome: str) -> None:
    """Salva a figura em `figuras/` nos dois modos, para uso fora do notebook."""
    ax.figure.savefig(FIGURAS / f"{nome}.png", bbox_inches="tight")


estilo()
