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
| Parsing/validação | biblioteca padrão (`json`, números lidos como decimal), validação escrita à mão (DT-006) | nenhuma dependência além do pytest | pydantic: mais um `pip install` |
| Aritmética monetária | inteiros em centavos (DT-003) | soma e comparação exatas | float: erro de representação |

## 2. Arquitetura

Script `reembolso.py` na raiz e pasta `motor/` com o cálculo (DT-008).

```
entrada JSON → leitura (arredonda, valida) → regras por item (identificador, valor zero,
categoria, descrição, dia não útil, nota, ...) → agregação por dia e categoria (limites)
→ saída JSON
```

| Peça | O que faz |
|---|---|
| `reembolso.py` | interpreta o comando `calcular --input --output`, lê e grava os arquivos |
| `motor/leitura.py` | converte o JSON em despesas, com valores em centavos (DT-003), e valida a entrada |
| `motor/regras_item.py` | aplica as regras que decidem a situação de cada item |
| `motor/agregacao.py` | forma os totais por dia e categoria e aplica os limites |
| `motor/saida.py` | monta o JSON de saída com as justificativas |
| `motor/politica.py` | valores da política (DT-007) |

A ordem exata das etapas segue a §8 da spec (AMB-016).

**Fronteiras:** só `reembolso.py` lê e grava arquivos. Os módulos de `motor/` são funções sem leitura nem escrita de arquivos: recebem dados e devolvem dados, e são testados isoladamente.

## 3. Modelo de dados

PENDENTE: depende da §4 da spec (formato da saída).

## 4. Como a política é representada

Constantes em `motor/politica.py` (DT-007): limites por categoria, categorias da política, palavras por categoria e feriados nacionais. Nenhum valor da política aparece fora desse arquivo.

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

### DT-006 — Leitura e validação da entrada

**Contexto:** a entrada tem formato fixo e poucos campos; os valores precisam ser lidos sem ponto flutuante (DT-003).
**Decisão:** biblioteca padrão: `json` com os números lidos como decimal; validação escrita à mão.
**Alternativa descartada:** pydantic, que exigiria mais um `pip install` no README.
**Consequência:** nenhuma dependência além do pytest; a validação fica explícita no código.

### DT-007 — Representação da política

**Contexto:** limites, categorias, palavras e feriados precisam ficar num lugar só; a mudança do dia 2 tende a alterar regras, não só valores.
**Decisão:** constantes em um único arquivo de código, `motor/politica.py`.
**Alternativa descartada:** arquivo de dados (`politica.json`): uma regra nova exigiria mudar código e dados, e um arquivo a mais precisaria ser lido e validado.
**Consequência:** mudar um valor é trocar uma linha; mudar uma regra mexe no módulo da regra e, se preciso, em `politica.py`.

### DT-008 — Organização do código

**Contexto:** cada RN precisa ser testável isoladamente, e a mudança do dia 2 deve cair em poucos lugares.
**Decisão:** script `reembolso.py` (comando e arquivos) e pasta `motor/` com `leitura`, `regras_item`, `agregacao`, `saida` e `politica`.
**Alternativa descartada:** tudo em `reembolso.py`, que mistura leitura, regras e saída. A pasta não se chama `reembolso/` para não ter o mesmo nome do script.
**Consequência:** o núcleo de regras não lê nem grava arquivos e é testado sem eles.

### DT-009 — Níveis de teste

**Contexto:** cada RN precisa de teste próprio para fechar a rastreabilidade.
**Decisão:** testes unitários por RN, um arquivo por regra, e um teste ponta a ponta com `exemplos/despesas-exemplo.json`.
**Alternativa descartada:** só testes ponta a ponta, em que uma falha não aponta a regra.
**Consequência:** mais testes, mas cada falha indica a RN afetada.

## 6. Estratégia de testes

- **Nível:** unitário por RN e um ponta a ponta com o exemplo (DT-009).
- **Cada `RN-NNN` da spec tem teste?** sim: cada RN tem um arquivo de teste, e cada caso de aceite da spec vira ao menos um teste.
- **Casos de borda da seção 7 da spec:** PENDENTE (bloco 2).
- **Nomenclatura:** conforme DT-005.

## 7. Riscos

| Risco | Probabilidade | O que faço se acontecer |
|---|---|---|
| | | |
