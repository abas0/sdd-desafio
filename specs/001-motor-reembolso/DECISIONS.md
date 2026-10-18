# Log de Decisões e Mudanças de Spec

> Uma entrada **toda vez** que a spec mudar. Este arquivo é a prova de que a spec
> foi tratada como artefato vivo e não como cerimônia de abertura.
>
> Spec que não muda em dois dias é spec que ninguém consultou. Mudança não é
> demérito — mudança não registrada é.

Ordem cronológica inversa: a mais recente primeiro.

---

## D-005 — Lote 2: categorias da política e descrição compatível · 2026-10-18

**Gatilho:** decisões de AMB-013, AMB-017 e AMB-030.

**O que mudou na spec:** AMB-013: PENDENTE → só alimentação, transporte urbano e hospedagem estão na política, reconhecidas sem diferenciar maiúsculas, acentos, espaços, sublinhado e hífen (RN-010 criada). AMB-017: PENDENTE → item com categoria fora da política é recusado (RN-010). AMB-030: PENDENTE → item é recusado quando a descrição tem palavra de outra categoria e nenhuma da sua (RN-011 criada, com a lista de palavras por categoria). Item da §3 sobre correção e reenvio reescrito.

**Por quê:** AMB-013: são as únicas categorias citadas na política; diferenças de grafia não mudam a categoria. AMB-017: a política diz que essas categorias "não são reembolsáveis". AMB-030: a categoria define o limite aplicado; uma descrição que aponta só para outra categoria indica erro de lançamento.

**O que isso invalidou:** nenhuma implementação existente. Ficam descartadas as leituras "outras categorias aceitas sem limite" (AMB-013); "pendente de correção" e "entrada inválida" (AMB-017); "categoria informada vale sem verificação" e "exigir sempre uma palavra da categoria" (AMB-030).

**Tasks afetadas:** nenhuma; `tasks.md` ainda não existe.

**Custo:** 2 arquivos (`spec.md`, `DECISIONS.md`).

---

## D-004 — Lote 1: premissas, dia não útil, valor zero e arredondamento · 2026-10-18

**Gatilho:** decisões de AMB-014, AMB-019, AMB-020, AMB-022, AMB-023 e AMB-026.

**O que mudou na spec:** AMB-014: PENDENTE → cada valor da entrada é arredondado para duas casas, com 0,005 afastando do zero, antes de qualquer outra regra (RN-009 criada). AMB-019: PENDENTE → despesa em sábado, domingo ou feriado nacional não é reembolsada e fica pendente de revisão (RN-007 criada). AMB-020: PENDENTE → despesa de R$ 0,00 é recusada (RN-008 criada). AMB-022 e AMB-023: registradas como premissas (valores em reais; sem teto global). AMB-026: dados do colaborador não afetam o cálculo e são repetidos na saída. Quatro itens novos na §3 (moeda estrangeira, teto global, fluxo de revisão de dia não útil, feriados estaduais e municipais). Notas de efeito em AMB-005, AMB-015, AMB-016 e AMB-031.

**Por quê:** AMB-014: o reembolso é pago em centavos; arredondar na entrada faz todas as regras trabalharem sobre o valor que de fato pode ser pago. AMB-019: a despesa em dia não útil foge do padrão de trabalho e precisa ser confirmada antes do reembolso. AMB-020: não há gasto a reembolsar. AMB-022 e AMB-023: a política expressa valores em reais e não define teto global. AMB-026: a política não vincula limites ao colaborador; repeti-lo na saída identifica de quem é o reembolso.

**O que isso invalidou:** nenhuma implementação existente. Ficam descartadas as opções da AMB-014 que arredondam só no total, truncam ou recusam valores com mais de duas casas, e a leitura "dia não útil segue as regras normais" (AMB-019).

**Tasks afetadas:** nenhuma; `tasks.md` ainda não existe.

**Custo:** 2 arquivos (`spec.md`, `DECISIONS.md`).

---

## D-003 — Critério de duplicata e identificador repetido · 2026-10-18

**Gatilho:** decisões de AMB-029 e AMB-011.

**O que mudou na spec:** AMB-029: PENDENTE → o identificador não distingue despesas e deve ser único no arquivo; repetido com o mesmo conteúdo, só o primeiro é calculado; com conteúdo diferente, todos são recusados (RN-006 criada). AMB-011: PENDENTE → duplicatas são itens com o mesmo conteúdo, exceto o identificador, com textos comparados sem diferenciar maiúsculas, acentos e espaços (RN-005 criada). Notas de efeito em AMB-012, AMB-013, AMB-018, AMB-021 e AMB-031; formatação da §10 corrigida.

**Por quê:** a saída identifica cada item pelo identificador (RN-003). Com o mesmo conteúdo, os itens são o mesmo lançamento; com conteúdo diferente, não há como saber qual é o correto. Um lançamento repetido reproduz todos os demais dados, e diferenças só de grafia não tornam duas despesas diferentes.

**O que isso invalidou:** nenhuma implementação existente. Ficam descartadas as leituras "identificador repetido torna a entrada inválida" (AMB-021) e "identificador diferente prova despesa diferente" (AMB-029), e também os critérios de duplicata que ignoram a descrição, a nota fiscal ou a categoria (AMB-011).

**Tasks afetadas:** nenhuma; `tasks.md` ainda não existe.

**Custo:** 2 arquivos (`spec.md`, `DECISIONS.md`).

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
