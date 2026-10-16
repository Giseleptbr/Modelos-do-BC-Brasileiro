"""Configuração central do pacote: caminhos, cache e parâmetros de rede.

Tudo que é caminho de disco passa por aqui. Nenhum notebook deve montar
caminho na mão — assim o repositório roda igual na sua máquina, no CI e em
qualquer clone novo.
"""

from __future__ import annotations

import os
from pathlib import Path

# Raiz do repositório: este arquivo vive em src/modelosbc/config.py
RAIZ = Path(__file__).resolve().parents[2]

DADOS = RAIZ / "dados"
CACHE = Path(os.environ.get("MODELOSBC_CACHE", DADOS / "cache"))
SEED = DADOS / "seed"
FIGURAS = RAIZ / "figuras"
REFERENCIAS = RAIZ / "referencias"

for _p in (CACHE, SEED, FIGURAS):
    _p.mkdir(parents=True, exist_ok=True)

# --- Rede -------------------------------------------------------------------
# Validade do cache em horas. Séries do BCB são revisadas; 12h evita rebaixar
# tudo a cada execução sem congelar dado velho por dias.
CACHE_HORAS = float(os.environ.get("MODELOSBC_CACHE_HORAS", 12))

TIMEOUT = 30          # segundos por requisição
TENTATIVAS = 3        # retentativas em erro de rede ou 5xx
ESPERA_BASE = 1.5     # segundos; backoff exponencial entre tentativas

USER_AGENT = (
    "modelosbc/0.1 (curso educacional; "
    "https://github.com/Giseleptbr/Modelos-do-BC-Brasileiro)"
)

# --- Convenções do curso ----------------------------------------------------
# Início padrão das séries. 2003 é o começo do período de metas já estabilizado
# após o choque de 2002 — antes disso a economia é outra e os coeficientes
# estimados viram média de dois regimes.
INICIO_PADRAO = "2003-01-01"

META_INFLACAO = 3.0   # % a.a., meta contínua vigente
BANDA = 1.5           # ponto percentual, intervalo de tolerância
