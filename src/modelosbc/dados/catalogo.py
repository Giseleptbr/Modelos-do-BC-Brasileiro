"""Catálogo de séries usadas no curso.

Por que um catálogo em vez de códigos soltos nos notebooks: o número de uma
série do SGS não diz nada sobre o que ela é. Espalhado pelo código, `433` vira
magia. Aqui cada série tem rótulo, unidade, frequência e procedência — e o
notebook pede `sgs.serie("ipca_mensal")`, não `433`.

O campo `verificado` registra se o código já foi conferido contra o nome
oficial publicado pelo BCB em dadosabertos.bcb.gov.br. Rode
`python scripts/verificar_series.py` para conferir todas e preencher as que
estão pendentes. Nunca use em aula uma série com `verificado=False` sem rodar
o script antes: trocar monitorados por livres não dá erro, dá resultado errado.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Serie:
    chave: str
    codigo: int
    rotulo: str
    unidade: str
    frequencia: str  # "D", "M" ou "T"
    verificado: bool = False
    nota: str = ""


_SERIES: tuple[Serie, ...] = (
    # --- Inflação -----------------------------------------------------------
    Serie("ipca_mensal", 433, "IPCA", "% a.m.", "M", True),
    Serie("ipca_12m", 13522, "IPCA acumulado em 12 meses", "% a.a.", "M", True),
    Serie("ipca_livres", 11428, "IPCA — itens livres", "% a.m.", "M", True),
    Serie("ipca_monitorados", 4449, "IPCA — itens monitorados", "% a.m.", "M", False,
          "Conferir rótulo oficial antes do Módulo 3."),
    Serie("ipca_comercializaveis", 11427, "IPCA — comercializáveis", "% a.m.", "M", False,
          "Conferir: 11427 e 11428 formam um par na base; o par precisa fechar com o IPCA cheio."),
    Serie("ipca_nucleo_ma", 4466, "IPCA — núcleo por médias aparadas com suavização",
          "% a.m.", "M", False),

    # --- Juros --------------------------------------------------------------
    Serie("selic_meta", 432, "Meta Selic definida pelo Copom", "% a.a.", "D", True,
          "Série se estende até a próxima reunião, logo tem datas futuras."),
    Serie("selic_mes", 4189, "Selic acumulada no mês, anualizada (base 252)", "% a.a.", "M", True),
    Serie("selic_diaria", 1178, "Selic anualizada (base 252)", "% a.a.", "D", False),

    # --- Câmbio -------------------------------------------------------------
    Serie("cambio_venda", 1, "Taxa de câmbio livre — dólar americano (venda)",
          "R$/US$", "D", True),

    # --- Atividade ----------------------------------------------------------
    Serie("ibcbr_dessaz", 24364, "IBC-Br dessazonalizado", "índice", "M", True),
    Serie("ibcbr", 24363, "IBC-Br", "índice", "M", False),

    # --- Expectativas (contexto; o grosso vem da API Focus, não do SGS) ------
    Serie("ipca_expectativa_12m", 4394, "Expectativa de inflação — 12 meses à frente",
          "% a.a.", "M", False,
          "Só para conferência cruzada; a fonte canônica de expectativas é a API Olinda."),
)

POR_CHAVE: dict[str, Serie] = {s.chave: s for s in _SERIES}
POR_CODIGO: dict[int, Serie] = {s.codigo: s for s in _SERIES}


def buscar(chave: str) -> Serie:
    """Devolve a série pela chave, com mensagem útil quando a chave não existe."""
    if chave not in POR_CHAVE:
        proximas = sorted(k for k in POR_CHAVE if chave.split("_")[0] in k)
        dica = f" Talvez: {', '.join(proximas)}." if proximas else ""
        raise KeyError(f"Série '{chave}' não está no catálogo.{dica}")
    return POR_CHAVE[chave]


def listar(verificadas: bool | None = None) -> list[Serie]:
    """Lista as séries do catálogo, opcionalmente filtrando por `verificado`."""
    if verificadas is None:
        return list(_SERIES)
    return [s for s in _SERIES if s.verificado is verificadas]
