# Instruções para agentes neste repositório

Curso em notebooks sobre o sistema de projeções do Banco Central do Brasil.
Leia `PLANO.md` antes de qualquer coisa: ele diz o que está pronto, o que falta
e quais decisões já foram tomadas. Atualize-o ao concluir uma aula.

## Idioma

Tudo em português do Brasil: prosa, nomes de função, variáveis, commits,
docstrings. Termos técnicos consagrados ficam no original quando traduzir
confunde (`DSGE`, `prior`, `VAR`, `fan chart` quando usado como nome próprio).

## Regras que não se negociam

1. **Nenhum notebook chama API diretamente.** Dados vêm de `modelosbc.dados`,
   que faz cache em parquet. Fonte nova entra como módulo em `src/modelosbc/dados/`.
2. **Nenhum notebook define cor, fonte ou estilo.** Gráficos saem de
   `modelosbc.viz`. Convenção visual nova entra como função lá.
3. **Toda afirmação sobre o BCB vem com fonte.** Documento e data. Se não achou
   a fonte, escreva que não achou — não preencha com plausível. Coeficiente
   inventado é o pior defeito possível neste repositório.
4. **Série não verificada não entra em aula.** Rode `scripts/verificar_series.py`.
   Um código de série errado devolve números plausíveis da coisa errada.
5. **Conteúdo antes de forma.** Reúna o material primeiro; só então escreva o
   notebook. Esqueleto bonito com conteúdo fino é retrabalho.

## Convenções de código

- Python ≥ 3.11, anotações de tipo, `from __future__ import annotations`.
- Docstring explica *por que*, não *o quê*. O código já diz o quê.
- Linha de até 100 colunas, `ruff` como linter.
- Nada de `print` de depuração em notebook entregue.

## Anatomia de uma aula

Cada notebook segue a mesma espinha:

1. **Pergunta** — o que esta aula responde, em uma frase.
2. **Contexto** — o que o BCB faz aqui, com citação da fonte.
3. **Desenvolvimento** — prosa curta alternando com código e figura.
4. **O que ficou de fora** — limites honestos da reimplementação.
5. **Exercícios** — de um a três, gabarito em `solucoes/`.

Aulas de implementação trocam o item 3 por código executável de ponta a ponta,
partindo de dados reais e terminando em um resultado verificável.

## Antes de dar um módulo por pronto

```bash
ruff check src scripts
python scripts/verificar_series.py --pendentes
jupyter nbconvert --execute --to notebook --inplace modulos/NN-*/**.ipynb
```

Executar em ambiente limpo, com `dados/cache/` vazio, pelo menos uma vez por
módulo: é o único teste que pega dependência escondida em cache.
