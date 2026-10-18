# Log de Decisões e Mudanças de Spec

> Uma entrada **toda vez** que a spec mudar. Este arquivo é a prova de que a spec
> foi tratada como artefato vivo e não como cerimônia de abertura.
>
> Spec que não muda em dois dias é spec que ninguém consultou. Mudança não é
> demérito — mudança não registrada é.

Ordem cronológica inversa: a mais recente primeiro.

---

## D-010 — Lote 7: ordem de aplicação das regras · 2026-10-18

**Gatilho:** decisão da AMB-016.

**O que mudou na spec:** §8 preenchida com a ordem de aplicação das regras: validação, arredondamento, cópias, recusas, pendências, estornos de hospedagem, dias de viagem e somas com limites. AMB-016: PENDENTE → a ordem da §8. Aceites da RN-019 tornados concretos. §10 atualizada: nenhuma ambiguidade pendente.

**Por quê:** as cópias são retiradas primeiro, para que o original seja avaliado sozinho; as recusas vêm antes das pendências, para que ninguém revise um item que não poderia ser pago; as demais posições seguem a dependência entre as regras.

**O que isso invalidou:** nenhuma implementação existente. Ficam descartadas as leituras "pendências antes de recusas" e "cópias avaliadas como itens independentes" (AMB-016).

**Tasks afetadas:** nenhuma; `tasks.md` ainda não existe.

**Custo:** 2 arquivos (`spec.md`, `DECISIONS.md`).

---

## D-009 — Lote 6: formato da saída e entrada inválida · 2026-10-18

**Gatilho:** decisões das AMB-021, AMB-024, AMB-025, AMB-027, AMB-031 e AMB-032.

**O que mudou na spec:** §4 preenchida: campos da entrada, estrutura da saída, campos de item, situações e motivos, totais diários, resumo e o exemplo completo da saída para `exemplos/despesas-exemplo.json`. RN-018 (entrada inválida) e RN-019 (item com mais de um motivo) criadas. As seis AMBs passam de PENDENTE à decisão; §10 atualizada.

**Por quê:** AMB-021: calcular parte de um arquivo malformado produziria um resultado em que não se pode confiar. AMB-032: separa o erro de quem gerou o arquivo da decisão sobre a despesa. AMB-024: a saída precisa ser entendida sem a spec e conferida pela regra. AMB-025: mostrar todos os motivos evita recusas sucessivas por motivos já conhecidos. AMB-027: o valor de alimentação e transporte só existe no total do dia. AMB-031: distinguir o que não será pago, o que depende de ação fora do sistema e o que é cópia.

**O que isso invalidou:** nenhuma implementação existente. Ficam descartadas as leituras "item malformado recusado sozinho" (AMB-032), "saída com campo de erro" (AMB-021), "só o motivo determinante" (AMB-025) e "situação parcial por item" em alimentação e transporte (AMB-031).

**Tasks afetadas:** nenhuma; `tasks.md` ainda não existe.

**Custo:** 2 arquivos (`spec.md`, `DECISIONS.md`).

---

## D-008 — Lote 5: duplicatas, estornos e hospedagens sobrepostas · 2026-10-18

**Gatilho:** decisões das AMB-012, AMB-015 e AMB-018.

**O que mudou na spec:** AMB-012: PENDENTE → só o primeiro item é calculado e as duplicatas são desconsideradas (RN-015 criada). AMB-015: PENDENTE → estorno abatido antes do limite, na soma do dia (alimentação e transporte) ou na hospedagem com a mesma data de entrada; total negativo vira R$ 0,00 (RN-016 criada). AMB-018: PENDENTE → hospedagens com noite em comum ficam pendentes de revisão (RN-017 criada). §3: sai a revisão de duplicatas; entram a revisão de hospedagens sobrepostas e a de estornos de hospedagem. Notas de efeito nas AMB-016 e AMB-031; §10 atualizada.

**Por quê:** AMB-012: um lançamento repetido não é uma nova despesa. AMB-015: o estorno reduz o gasto líquido e um total negativo não gera cobrança. AMB-018: duas hospedagens na mesma noite indicam erro ou gasto em dobro, e não há valor por noite.

**O que isso invalidou:** nenhuma implementação existente. Ficam descartadas as leituras "revisar duplicatas" e "recusar todas" (AMB-012); "recusar", "desconsiderar", "abater depois do limite" e "abater do total do período" (AMB-015); "cada hospedagem com o seu teto", "pagar só a de maior valor" e "deixar pendente só a noite sobreposta" (AMB-018).

**Tasks afetadas:** nenhuma; `tasks.md` ainda não existe.

**Custo:** 2 arquivos (`spec.md`, `DECISIONS.md`).

---

## D-007 — Lote 4: viagem e competência · 2026-10-18

**Gatilho:** decisões das AMB-008, AMB-009, AMB-010 e AMB-028, e a exceção para hospedagem na AMB-019.

**O que mudou na spec:** AMB-008: PENDENTE → dia de viagem coberto por estadia ou com palavra de viagem, com a data da hospedagem como data de entrada (RN-013 criada), com o registro da limitação de lazer × trabalho. AMB-009: PENDENTE → ampliação só de alimentação e transporte, só nos dias de viagem. AMB-010: PENDENTE → período igual ao mês da competência; item fora do período recusado; diárias não cortadas (RN-014 criada). AMB-028: PENDENTE → sem tratamento especial. RN-007 alterada com a exceção para hospedagem. Notas de efeito nas AMB-018 e AMB-019; §10 atualizada.

**Por quê:** AMB-008: a entrada não traz o dado de viagem; hospedagem e palavras de deslocamento são os indícios objetivos disponíveis. AMB-009: quem se hospeda já está em viagem. AMB-010: período e competência precisam corresponder, e a data informada é a única referência. AMB-028: a política não diz que a alimentação está incluída na diária. RN-007: chegar na véspera de um dia útil é comum em viagens a trabalho.

**O que isso invalidou:** nenhuma implementação existente. Ficam descartadas as leituras "não aplicar a ampliação" (AMB-008); "ampliar o patamar da nota", "ampliar a hospedagem" e "ampliar o mês inteiro" (AMB-009); "aceitar fora do período" e "cortar diárias fora do período" (AMB-010); "alimentação incluída na diária" (AMB-028). Muda parte da D-004: a hospedagem em dia não útil deixa de ficar sempre pendente.

**Tasks afetadas:** nenhuma; `tasks.md` ainda não existe.

**Custo:** 2 arquivos (`spec.md`, `DECISIONS.md`).

---

## D-006 — Lote 3: nota fiscal obrigatória · 2026-10-18

**Gatilho:** decisões de AMB-005, AMB-006 e AMB-007.

**O que mudou na spec:** AMB-005: PENDENTE → nota obrigatória para valor maior que R$ 100,00. AMB-006: PENDENTE → patamar medido sobre o valor do próprio item, já arredondado. AMB-007: PENDENTE → item sem a nota obrigatória fica pendente de nota fiscal, com R$ 0,00 e fora da soma do dia. RN-012 criada; item novo na §3 (envio posterior da nota); notas de efeito em AMB-016 e AMB-031.

**Por quê:** AMB-005: "acima de" tem o mesmo sentido da AMB-004. AMB-006: a nota é documento de cada despesa. AMB-007: sem a nota a despesa não pode ser paga, mas a falta pode ser sanada com o envio da nota.

**O que isso invalidou:** nenhuma implementação existente. Ficam descartadas as leituras "R$ 100,00 exige nota" (AMB-005), "soma do dia" e "valor depois do limite" (AMB-006), "recusar" e "reembolsar até R$ 100" (AMB-007).

**Tasks afetadas:** nenhuma; `tasks.md` ainda não existe.

**Custo:** 2 arquivos (`spec.md`, `DECISIONS.md`).

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
