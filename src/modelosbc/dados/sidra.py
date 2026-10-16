"""Cliente do SIDRA/IBGE — aberturas do IPCA que o SGS não publica.

Base: https://apisidra.ibge.gov.br/values/...

Duas tabelas interessam ao curso:
    1737 — IPCA geral: variação mensal, acumulada no ano e em 12 meses
    7060 — IPCA por grupo, subgrupo, item e subitem (a partir de jan/2020)

Peculiaridade do SIDRA: a primeira linha da resposta é o cabeçalho descritivo,
não um dado. Quem ignora isso ganha uma linha de texto no meio dos números.

A classificação por grupo (alimentação, serviços, industriais) é o insumo do
Módulo 3: é ali que se vê que a inflação agregada é a média de setores que
respondem a coisas diferentes.
"""

from __future__ import annotations

import pandas as pd

from ._http import baixar_json, com_cache

BASE = "https://apisidra.ibge.gov.br/values"

# Variáveis da tabela 7060
VAR_MENSAL = 63
VAR_12_MESES = 2265
PESO = 66

# Grupos do IPCA (classificação c315)
GRUPOS = {
    7170: "Alimentação e bebidas",
    7445: "Habitação",
    7486: "Artigos de residência",
    7558: "Vestuário",
    7625: "Transportes",
    7660: "Saúde e cuidados pessoais",
    7712: "Despesas pessoais",
    7766: "Educação",
    7786: "Comunicação",
}


def _consultar(caminho: str) -> pd.DataFrame:
    dados = baixar_json(f"{BASE}/{caminho}")
    if not dados or len(dados) < 2:
        return pd.DataFrame()
    cabecalho, *linhas = dados
    df = pd.DataFrame(linhas).rename(columns=cabecalho)
    return df


def ipca_por_grupo(inicio_aaaamm: str = "202001", forcar: bool = False) -> pd.DataFrame:
    """Variação mensal do IPCA por grupo, em formato largo (data × grupo)."""
    codigos = ",".join(str(c) for c in GRUPOS)
    caminho = f"t/7060/n1/1/v/{VAR_MENSAL}/p/all/c315/{codigos}/d/v{VAR_MENSAL}%202"

    def construir() -> pd.DataFrame:
        bruto = _consultar(caminho)
        if bruto.empty:
            return bruto
        df = bruto.rename(
            columns={
                "Mês (Código)": "periodo",
                "Geral, grupo, subgrupo, item e subitem": "grupo",
                "Valor": "valor",
            }
        )[["periodo", "grupo", "valor"]]
        df["data"] = pd.to_datetime(df["periodo"], format="%Y%m")
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
        largo = df.pivot_table(index="data", columns="grupo", values="valor")
        return largo.loc[largo.index >= pd.to_datetime(inicio_aaaamm, format="%Y%m")].reset_index()

    df = com_cache("sidra_ipca_grupos", {"inicio": inicio_aaaamm}, construir, forcar=forcar)
    return df.set_index("data")


def pesos_por_grupo(periodo: str = "last", forcar: bool = False) -> pd.Series:
    """Peso de cada grupo na cesta do IPCA — necessário para reagregar setores.

    O peso muda todo mês (é atualizado pelo próprio movimento de preços), então
    reagregação honesta usa o peso do mês, não um peso fixo.
    """
    codigos = ",".join(str(c) for c in GRUPOS)
    caminho = f"t/7060/n1/1/v/{PESO}/p/{periodo}/c315/{codigos}"

    def construir() -> pd.DataFrame:
        bruto = _consultar(caminho)
        if bruto.empty:
            return bruto
        df = bruto.rename(
            columns={"Geral, grupo, subgrupo, item e subitem": "grupo", "Valor": "peso"}
        )[["grupo", "peso"]]
        df["peso"] = pd.to_numeric(df["peso"], errors="coerce")
        return df

    df = com_cache("sidra_pesos_grupos", {"periodo": periodo}, construir, forcar=forcar)
    return df.set_index("grupo")["peso"]
