"""Camada de rede e cache em parquet, compartilhada por SGS, Focus e SIDRA.

Regra do repositório: nenhum notebook chama API diretamente. Todo acesso passa
por aqui, e toda resposta vira parquet em `dados/cache/`. Consequência prática:
a primeira execução baixa, as seguintes leem do disco, e o curso continua
rodando offline — inclusive quando a API do BCB está fora do ar.
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

import pandas as pd
import requests

from ..config import CACHE, CACHE_HORAS, ESPERA_BASE, SEED, TENTATIVAS, TIMEOUT, USER_AGENT

_SESSAO: requests.Session | None = None


def sessao() -> requests.Session:
    """Sessão HTTP única, com User-Agent identificando o projeto."""
    global _SESSAO
    if _SESSAO is None:
        _SESSAO = requests.Session()
        _SESSAO.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})
    return _SESSAO


def baixar_json(url: str, params: dict[str, Any] | None = None) -> Any:
    """GET com retentativa e backoff exponencial. Devolve o JSON decodificado.

    Erros 4xx (exceto 429) não são retentados: pedido malformado não melhora
    com insistência. 429 e 5xx são retentados.
    """
    ultimo_erro: Exception | None = None
    for tentativa in range(1, TENTATIVAS + 1):
        try:
            r = sessao().get(url, params=params, timeout=TIMEOUT)
            if r.status_code == 429 or 500 <= r.status_code < 600:
                raise requests.HTTPError(f"HTTP {r.status_code}", response=r)
            r.raise_for_status()
            if not r.content:
                return []
            return r.json()
        except (requests.RequestException, json.JSONDecodeError) as e:
            ultimo_erro = e
            if isinstance(e, requests.HTTPError) and e.response is not None:
                cod = e.response.status_code
                if 400 <= cod < 500 and cod != 429:
                    raise
            if tentativa < TENTATIVAS:
                time.sleep(ESPERA_BASE ** tentativa)
    raise RuntimeError(f"Falha ao baixar {url} após {TENTATIVAS} tentativas") from ultimo_erro


def _chave(nome: str, params: dict[str, Any]) -> Path:
    """Caminho de cache determinístico: nome legível + hash dos parâmetros."""
    assinatura = json.dumps(params, sort_keys=True, default=str)
    digest = hashlib.sha256(assinatura.encode()).hexdigest()[:10]
    return CACHE / f"{nome}__{digest}.parquet"


def _fresco(caminho: Path, horas: float) -> bool:
    if not caminho.exists():
        return False
    idade = datetime.now(timezone.utc) - datetime.fromtimestamp(
        caminho.stat().st_mtime, tz=timezone.utc
    )
    return idade < timedelta(hours=horas)


def com_cache(
    nome: str,
    params: dict[str, Any],
    construtor: Callable[[], pd.DataFrame],
    horas: float | None = None,
    forcar: bool = False,
) -> pd.DataFrame:
    """Devolve o DataFrame de `construtor`, usando parquet em disco quando fresco.

    Ordem de resolução:
      1. cache fresco em `dados/cache/`;
      2. `construtor()` — ou seja, a rede;
      3. seed versionada em `dados/seed/` (se a rede falhar);
      4. cache vencido, se existir.

    Os passos 3 e 4 existem para que uma aula não dependa de a API estar no ar.
    """
    caminho = _chave(nome, params)
    horas = CACHE_HORAS if horas is None else horas

    if not forcar and _fresco(caminho, horas):
        return pd.read_parquet(caminho)

    try:
        df = construtor()
        if df is not None and not df.empty:
            df.to_parquet(caminho, index=False)
            return df
        raise ValueError(f"{nome}: a fonte devolveu um conjunto vazio")
    except Exception as erro:
        semente = SEED / f"{nome}.parquet"
        if semente.exists():
            print(f"[modelosbc] {nome}: rede indisponível ({erro}). Usando seed versionada.")
            return pd.read_parquet(semente)
        if caminho.exists():
            print(f"[modelosbc] {nome}: rede indisponível ({erro}). Usando cache vencido.")
            return pd.read_parquet(caminho)
        raise


def limpar_cache(padrao: str = "*") -> int:
    """Apaga arquivos de cache que casem com `padrao`. Devolve quantos saíram."""
    arquivos = list(CACHE.glob(f"{padrao}.parquet"))
    for a in arquivos:
        a.unlink()
    return len(arquivos)
