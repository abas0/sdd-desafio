# Plano Técnico — Motor de Cálculo de Reembolso

**Versão:** 1.0 · **Baseado na spec:** 1.0 · **Status:** rascunho, **não aprovado**

> Aqui mora o COMO. Este arquivo pode e deve falar de linguagem, biblioteca e
> arquitetura. O que ele **não** pode é introduzir regra de negócio nova — se
> apareceu uma, ela pertence à `spec.md`.

> As decisões abaixo foram tomadas em paralelo com a spec. O plan só vale após
> aprovação, com a spec fechada.

---

## 1. Stack

| Escolha | O quê | Por quê | O que descartei e por quê |
|---|---|---|---|
| Linguagem | Python 3 (testado em 3.14) | já instalado no ambiente; roda sem instalar outra linguagem | outras linguagens: exigem instalação |
| Testes | pytest | testes mais legíveis, com um caso de aceite por função | unittest: mais verboso |
| Parsing/validação | PENDENTE (bloco 2) | | |
| Aritmética monetária | inteiros em centavos (DT-003) | soma e comparação exatas | float: erro de representação |

## 2. Arquitetura

PENDENTE (bloco 2).

```
entrada JSON → <...> → <...> → saída JSON
```

**Fronteiras:** PENDENTE (bloco 2).

## 3. Modelo de dados

PENDENTE (bloco 2).

## 4. Como a política é representada

PENDENTE (bloco 2).

## 5. Decisões técnicas

### DT-001 — Linguagem

**Contexto:** o README precisa permitir rodar e testar sem intervenção; o único ambiente instalado é Python 3.14.
**Decisão:** Python 3.
**Alternativa descartada:** outras linguagens, que exigem instalar outro ambiente aqui e em quem for avaliar.
**Consequência:** o README tem uma única pré-condição, o Python.

### DT-002 — Testes

**Contexto:** cada RN tem casos de aceite que precisam virar testes.
**Decisão:** pytest.
**Alternativa descartada:** unittest, da biblioteca padrão, mais verboso.
**Consequência:** o README inclui `pip install pytest`.

### DT-003 — Aritmética monetária

**Contexto:** a spec arredonda cada valor da entrada para duas casas antes de qualquer regra (RN-009).
**Decisão:** valores representados internamente como inteiros em centavos. Na leitura, o número do JSON é interpretado como decimal exato, sem passar por ponto flutuante, e convertido em centavos conforme a RN-009.
**Alternativa descartada:** float, que causa erro de representação: 33,335 em ponto flutuante vira 33,33499…, que arredondaria para 33,33, violando a RN-009.
**Consequência:** soma e comparação exatas; arredondar só nos totais exigiria mudar esta DT.

### DT-004 — Forma do comando

**Contexto:** a interface é fixa: `<comando> calcular --input <entrada.json> --output <saida.json>`.
**Decisão:** `python reembolso.py calcular --input <entrada.json> --output <saida.json>`.
**Alternativa descartada:** `python -m` (exige estrutura de pacote para chamar) e comando instalado (exige `pip install -e .`).
**Consequência:** roda sem instalação, a partir da raiz do repositório.

### DT-005 — Nome dos testes

**Contexto:** o nome de cada teste precisa remeter ao requisito que verifica.
**Decisão:** `test_rn001_<caso>` e `test_amb011_<caso>`.
**Alternativa descartada:** uma classe por regra (`TestRN001`), com a rastreabilidade menos visível na listagem.
**Consequência:** a rastreabilidade fica visível em qualquer listagem de testes.

## 6. Estratégia de testes

- **Nível:** PENDENTE (bloco 2).
- **Cada `RN-NNN` da spec tem teste?** PENDENTE (bloco 2).
- **Casos de borda da seção 7 da spec:** PENDENTE (bloco 2).
- **Nomenclatura:** conforme DT-005.

## 7. Riscos

| Risco | Probabilidade | O que faço se acontecer |
|---|---|---|
| | | |
