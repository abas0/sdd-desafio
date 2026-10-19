# Tasks — Motor de Cálculo de Reembolso

> Cada task é pequena o bastante para virar **um commit**. Se você não consegue
> descrever o critério de aceite como "o teste X passa", a task está grande demais.
>
> Marque `[x]` conforme conclui — ao longo do caminho, não tudo no fim. O histórico
> de quando cada task foi marcada é lido na correção.

**Formato do commit:** `feat(T-003): <descrição>` · `test(T-003): <descrição>`

Os testes ficam em `tests/`. O aceite de cada task é "os testes do arquivo indicado passam".

---

## Fase 1 — Fundação

- [x] **T-001** — Estrutura do projeto: `reembolso.py`, `motor/`, `tests/` e `requirements.txt` com o pytest
  - **Atende:** DT-001, DT-002, DT-004, DT-008
  - **Aceite:** `python -m pytest` roda; `python reembolso.py --help` mostra o comando `calcular`
  - **Commit:** `f4cb359`

- [x] **T-002** — Leitura e validação da entrada
  - **Atende:** RN-018, AMB-021, AMB-032, AMB-033
  - **Aceite:** `tests/test_rn018_entrada_invalida.py`
  - **Commit:** `c3baaf7`

- [x] **T-003** — Arredondamento e conversão dos valores em centavos
  - **Atende:** RN-009, AMB-014, DT-003
  - **Aceite:** `tests/test_rn009_arredondamento.py`
  - **Commit:** `8d30976`

- [x] **T-004** — Calendário: fins de semana, feriados nacionais e Sexta-feira Santa
  - **Atende:** RN-007 (parte), AMB-019
  - **Aceite:** `tests/test_rn007_calendario.py`
  - **Commit:** `0ae59e7`

- [x] **T-005** — Número de diárias lido na descrição
  - **Atende:** RN-004 (parte), AMB-003
  - **Aceite:** `tests/test_rn004_diarias.py`
  - **Commit:** `4cf93b0`

## Fase 2 — Regras por item

- [x] **T-006** — Mesmo conteúdo e identificador repetido
  - **Atende:** RN-005, RN-006, AMB-011, AMB-029
  - **Aceite:** `tests/test_rn005_mesmo_conteudo.py`, `tests/test_rn006_identificador_repetido.py`
  - **Commit:** `e888a81`

- [x] **T-007** — Duplicatas
  - **Atende:** RN-015, AMB-012
  - **Aceite:** `tests/test_rn015_duplicatas.py`
  - **Commit:** `5239b5c`

- [x] **T-008** — Categorias da política
  - **Atende:** RN-010, AMB-013, AMB-017
  - **Aceite:** `tests/test_rn010_categorias.py`
  - **Commit:** `32f2157`

- [x] **T-009** — Descrição compatível com a categoria
  - **Atende:** RN-011, AMB-030
  - **Aceite:** `tests/test_rn011_descricao.py`
  - **Commit:** `2c08444`

- [x] **T-010** — Período de competência
  - **Atende:** RN-014, AMB-010
  - **Aceite:** `tests/test_rn014_periodo.py`
  - **Commit:** `2c5c4d0`

- [x] **T-011** — Valor zero
  - **Atende:** RN-008, AMB-020
  - **Aceite:** `tests/test_rn008_valor_zero.py`
  - **Commit:** `44f7b3d`

- [x] **T-012** — Dia não útil, com a exceção para hospedagem
  - **Atende:** RN-007, AMB-019
  - **Aceite:** `tests/test_rn007_dia_nao_util.py`
  - **Commit:** `2e2861d`; correção `c66a602` (D-012)

- [x] **T-013** — Nota fiscal obrigatória
  - **Atende:** RN-012, AMB-005, AMB-006, AMB-007
  - **Aceite:** `tests/test_rn012_nota_fiscal.py`
  - **Commit:** `8cf8ee6`

- [x] **T-014** — Hospedagens sobrepostas
  - **Atende:** RN-017, AMB-018
  - **Aceite:** `tests/test_rn017_sobreposicao.py`
  - **Commit:** `6cc1318`

- [x] **T-015** — Ordem das regras e `outros_motivos`
  - **Atende:** RN-019, AMB-016, AMB-025
  - **Aceite:** `tests/test_rn019_ordem_e_motivos.py`
  - **Commit:** `ac1bc87`

## Fase 3 — Valores

- [x] **T-016** — Dias de viagem
  - **Atende:** RN-013, AMB-008, AMB-009, AMB-028
  - **Aceite:** `tests/test_rn013_viagem.py`
  - **Commit:** `829677b`

- [x] **T-017** — Soma do dia, limite e valor apurado por dia
  - **Atende:** RN-001, RN-002, RN-003, AMB-001, AMB-002, AMB-004
  - **Aceite:** `tests/test_rn001_limite_diario.py`, `tests/test_rn002_teto.py`, `tests/test_rn003_valor_por_dia.py`
  - **Commit:** `8f04e7c`

- [x] **T-018** — Teto de hospedagem
  - **Atende:** RN-004, RN-002
  - **Aceite:** `tests/test_rn004_teto_hospedagem.py`
  - **Commit:** `9ca5c0f`

- [x] **T-019** — Estornos
  - **Atende:** RN-016, AMB-015
  - **Aceite:** `tests/test_rn016_estornos.py`
  - **Commit:** `f0ed8d6`

## Fase 4 — Saída e CLI

- [ ] **T-020** — Montagem da saída, justificativas, resumo e escritor do JSON
  - **Atende:** spec §4, AMB-024, AMB-026, AMB-027, AMB-031, DT-010
  - **Aceite:** `tests/test_saida.py`
  - **Commit:**

- [ ] **T-021** — Comando `calcular` de ponta a ponta, erro de entrada e README
  - **Atende:** spec §9, RN-018
  - **Aceite:** `tests/test_ponta_a_ponta.py` (compara a saída do exemplo com o JSON da §4 da spec)
  - **Commit:**

---

## Fase 5 — Envelope (criar no Dia 2)

<Novas tasks a partir da mudança de requisito. Numeração continua de onde parou —
não reinicie e não renumere as antigas: a numeração é o eixo da rastreabilidade.>

---

## Cobertura

Preenchida ao fechar cada fase.

| Regra da spec | Task | Teste |
|---|---|---|
| RN-004 (número de diárias), AMB-003 | T-005 | `tests/test_rn004_diarias.py` |
| RN-007 (calendário), AMB-019 | T-004 | `tests/test_rn007_calendario.py` |
| RN-009, AMB-014 | T-003 | `tests/test_rn009_arredondamento.py` |
| RN-018, AMB-021, AMB-032, AMB-033 | T-002 | `tests/test_rn018_entrada_invalida.py` |
| RN-014 (período inválido) | T-002 | `tests/test_rn018_entrada_invalida.py::test_rn018_periodo_diferente_do_mes_da_competencia_e_invalido` |
| RN-005, AMB-011 | T-006 | `tests/test_rn005_mesmo_conteudo.py` |
| RN-006, AMB-029 | T-006 | `tests/test_rn006_identificador_repetido.py` |
| RN-007 (dia não útil), AMB-019 | T-012 | `tests/test_rn007_dia_nao_util.py` |
| RN-008, AMB-020 | T-011 | `tests/test_rn008_valor_zero.py` |
| RN-010, AMB-013, AMB-017 | T-008 | `tests/test_rn010_categorias.py` |
| RN-011, AMB-030 | T-009 | `tests/test_rn011_descricao.py` |
| RN-012, AMB-005, AMB-006, AMB-007 | T-013 | `tests/test_rn012_nota_fiscal.py` |
| RN-014, AMB-010 | T-010 | `tests/test_rn014_periodo.py` |
| RN-015, AMB-012 | T-007 | `tests/test_rn015_duplicatas.py` |
| RN-017, AMB-018 | T-014 | `tests/test_rn017_sobreposicao.py` |
| RN-019, AMB-016, AMB-025 | T-015 | `tests/test_rn019_ordem_e_motivos.py` |
| RN-001, AMB-001 | T-017 | `tests/test_rn001_limite_diario.py` |
| RN-002, AMB-004 | T-017 | `tests/test_rn002_teto.py` |
| RN-003, AMB-002 | T-017 | `tests/test_rn003_valor_por_dia.py` |
| RN-004 (teto) | T-018 | `tests/test_rn004_teto_hospedagem.py` |
| RN-013, AMB-008, AMB-009, AMB-028 | T-016 | `tests/test_rn013_viagem.py` |
| RN-016, AMB-015 | T-019 | `tests/test_rn016_estornos.py` |

AMB-022 e AMB-023 são premissas, sem comportamento a testar: não têm task.
