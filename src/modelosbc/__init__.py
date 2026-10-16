"""modelosbc — ferramentas do curso "Modelos do Banco Central".

Reimplementação didática, em Python, do sistema de projeções que sustenta o
Relatório de Política Monetária do Banco Central do Brasil.

Isto não é o modelo oficial do BCB. É uma reconstrução a partir da
documentação pública, feita para ensinar como as peças se encaixam.

Uso típico no topo de um notebook:

    from modelosbc import dados, util, viz
    viz.estilo()
    ipca = dados.sgs.serie("ipca_mensal")
"""

from . import config, dados, util, viz

__version__ = "0.1.0"
__all__ = ["config", "dados", "util", "viz"]
