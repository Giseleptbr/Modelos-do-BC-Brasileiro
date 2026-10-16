#!/usr/bin/env python3
"""Confere cada série do catálogo contra os metadados públicos do BCB.

Por que isso existe: um código de série errado não levanta exceção. Ele devolve
números plausíveis da coisa errada — e aí a aula ensina algo falso. Este script
busca o nome oficial de cada código em dadosabertos.bcb.gov.br e mostra, ao
lado, o rótulo que o catálogo afirma, além da última observação disponível.

Uso:
    python scripts/verificar_series.py
    python scripts/verificar_series.py --pendentes   # só as verificado=False

Saída: tabela no terminal e `dados/seed/catalogo_verificado.csv`.
Confirme olho no olho e então marque `verificado=True` no catálogo.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from modelosbc.config import SEED, USER_AGENT  # noqa: E402
from modelosbc.dados import catalogo  # noqa: E402

CKAN = "https://dadosabertos.bcb.gov.br/api/3/action/package_search"
SGS = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/1"


def nome_oficial(codigo: int, sessao: requests.Session) -> str:
    """Nome publicado pelo BCB no portal de dados abertos, ou '?' se não achar."""
    try:
        r = sessao.get(CKAN, params={"q": f"name:{codigo}-*", "rows": 5}, timeout=30)
        r.raise_for_status()
        resultados = r.json()["result"]["results"]
    except Exception as e:  # rede fora, portal mudou: não é motivo para abortar
        return f"(falhou: {type(e).__name__})"

    for pacote in resultados:
        if pacote.get("name", "").startswith(f"{codigo}-"):
            return pacote.get("title", "?")
    return "?"


def ultima_observacao(codigo: int, sessao: requests.Session) -> tuple[str, str]:
    try:
        r = sessao.get(SGS.format(codigo=codigo), params={"formato": "json"}, timeout=30)
        r.raise_for_status()
        linha = r.json()[0]
        return linha["data"], linha["valor"]
    except Exception as e:
        return "-", f"(falhou: {type(e).__name__})"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pendentes", action="store_true",
                    help="verifica apenas as séries ainda não confirmadas")
    args = ap.parse_args()

    series = catalogo.listar(verificadas=False) if args.pendentes else catalogo.listar()
    sessao = requests.Session()
    sessao.headers.update({"User-Agent": USER_AGENT})

    linhas = []
    for s in series:
        oficial = nome_oficial(s.codigo, sessao)
        data, valor = ultima_observacao(s.codigo, sessao)
        linhas.append({
            "chave": s.chave,
            "codigo": s.codigo,
            "rotulo_no_catalogo": s.rotulo,
            "nome_oficial_bcb": oficial,
            "ultima_data": data,
            "ultimo_valor": valor,
            "ja_verificado": s.verificado,
        })

    df = pd.DataFrame(linhas)
    destino = SEED / "catalogo_verificado.csv"
    df.to_csv(destino, index=False)

    with pd.option_context("display.max_colwidth", 60, "display.width", 200):
        print(df.to_string(index=False))
    print(f"\nSalvo em {destino}")
    print("Compare 'rotulo_no_catalogo' com 'nome_oficial_bcb'. Divergiu, corrija "
          "o catálogo antes de usar a série em aula.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
