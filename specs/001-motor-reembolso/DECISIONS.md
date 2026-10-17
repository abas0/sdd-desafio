# Log de Decisões e Mudanças de Spec

> Uma entrada **toda vez** que a spec mudar. Este arquivo é a prova de que a spec
> foi tratada como artefato vivo e não como cerimônia de abertura.
>
> Spec que não muda em dois dias é spec que ninguém consultou. Mudança não é
> demérito — mudança não registrada é.

Ordem cronológica inversa: a mais recente primeiro.

---

## D-002 — Teto de hospedagem por diária e formato de entrada fixo · 2026-10-17

**Gatilho:** decisões de AMB-033 e AMB-003.

**O que mudou na spec:** AMB-033: PENDENTE → a entrada não recebe campos além dos do exemplo. AMB-003: PENDENTE → teto de hospedagem de R$ 250,00 por diária, com o número de diárias lido na descrição e uma diária quando não houver número válido (RN-004 criada). Notas de efeito em AMB-008, AMB-010 e AMB-018; §10 atualizada.

**Por quê:** AMB-033: o formato de entrada é fixo pelo enunciado. AMB-003: a política fixa o teto por diária, e hospedagens como aluguel por temporada são pagas de uma vez; o teto precisa acompanhar o número de diárias da estadia.

**O que isso invalidou:** nenhuma implementação existente. Ficam descartadas as leituras "um lançamento por diária" e "campo opcional com o número de diárias" (AMB-003), "exigir um dado que a entrada não traz" (AMB-008) e "data de lançamento" (AMB-010).

**Tasks afetadas:** nenhuma; `tasks.md` ainda não existe.

**Custo:** 2 arquivos (`spec.md`, `DECISIONS.md`).

---

## D-001 — Teto de reembolso e valor apurado por dia · 2026-10-17

**Gatilho:** decisões de AMB-004 e AMB-002 tomadas após a versão de referência da spec (commit `39baa6e`).

**O que mudou na spec:** AMB-004: PENDENTE → reembolso até o limite, excedente não reembolsado, valor igual ao limite integral (RN-002 criada). AMB-002: PENDENTE → valor reembolsado apurado no total da categoria no dia, sem divisão entre itens (RN-003 criada). Notas de efeito em AMB-006, AMB-007, AMB-014, AMB-015, AMB-018, AMB-024, AMB-027 e AMB-031; §10 atualizada.

**Por quê:** AMB-004: os valores da política funcionam como teto de gasto. AMB-002: a política fixa o limite por dia; o valor reembolsável é, portanto, do dia, e reparti-lo entre os itens exigiria um critério que a política não fornece.

**O que isso invalidou:** nenhuma implementação existente. Deixam de se aplicar a categorias com limite diário as leituras "valor depois do limite" (AMB-006) e "associar a uma despesa original" (AMB-015). A descrição da saída em `CLAUDE.md` foi ajustada.

**Tasks afetadas:** nenhuma; `tasks.md` ainda não existe.

**Custo:** 3 arquivos (`spec.md`, `CLAUDE.md`, `DECISIONS.md`).
