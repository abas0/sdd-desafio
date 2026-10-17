# Spec — Motor de Cálculo de Reembolso

**Versão:** 1.0 · **Status:** rascunho · **Última alteração:** 2026-10-17

> **Regra de ouro deste arquivo:** ele descreve o QUÊ e o PORQUÊ. Nenhuma linha
> aqui pode citar linguagem, biblioteca, classe, função ou estrutura de pasta.
> Se apareceu solução, o lugar dela é o `plan.md`.
>
> **Teste de aceitação da própria spec:** uma pessoa que nunca viu o projeto
> consegue, lendo só este arquivo, verificar se o sistema está correto?

---

## 1. Problema

<Duas ou três frases. Quem sofre hoje, com o quê, e por quê isso custa caro.>

## 2. Objetivo

<Uma frase. O que passa a ser verdade quando isto existir.>

## 3. Fora de escopo

- Não gerencia o fluxo de revisão de despesas duplicadas: prazo, responsável e desfecho da revisão (ver AMB-012).
- Não gerencia a correção e o reenvio de despesas lançadas com categoria fora da política: quem corrige e em que prazo (ver AMB-017).
- Não oferece lista de categorias no momento do lançamento da despesa; isso pertence ao sistema que gera a entrada (ver AMB-013).

## 4. Entrada e saída

**Entrada:** conforme `exemplos/despesas-exemplo.json`. Campos e significado:

| Campo | Tipo | Significado | Obrigatório |
|---|---|---|---|
| | | | |

**Saída:** definida por mim. Estrutura e significado de cada campo:

| Campo | Tipo | Significado |
|---|---|---|
| | | |

<Cole um exemplo de saída para uma entrada pequena. Vale mais que três parágrafos.>

## 5. Regras de negócio

Cada regra recebe um ID (`RN-001`, ...). As tasks vão referenciar esses IDs.

### RN-001 — Limite diário por categoria

**Regra:** para alimentação e transporte urbano, o valor comparado com o limite diário (R$ 60,00 e R$ 80,00, respectivamente) é a soma das despesas daquela categoria com a mesma data, entendida como a data informada em cada despesa. Despesas de categorias diferentes não entram na mesma soma.
**Origem:** política do RH, itens 1 e 2; AMB-001.
**Aceite:** duas despesas de alimentação em 2026-07-03, de R$ 72,50 e R$ 38,00, formam um total diário de R$ 110,50, que excede o limite de R$ 60,00 em R$ 50,50. Uma despesa de transporte urbano na mesma data não entra nessa soma.

---

## 6. Ambiguidades identificadas e decisões

> **Esta seção é o coração da spec e vale a maior parte dos 25 pontos do critério 1.**
> Uma ambiguidade que você resolveu no código sem registrar aqui conta como
> não resolvida.

### AMB-001 — Unidade de aplicação do limite diário de alimentação e transporte urbano
**Ref. levantamento:** A-01
**Texto original do RH:** "Alimentação tem limite de R$ 60 por dia." / "Transporte urbano tem limite de R$ 80 por dia."
**O que não está claro:** se o limite se aplica a cada despesa individualmente ou à soma das despesas da mesma categoria no mesmo dia.
**Decisão:** o limite se aplica à soma das despesas da mesma categoria com a mesma data, entendida como a data informada em cada despesa. Despesas de categorias diferentes não se somam.
**Justificativa:** a política fala em limite "por dia", não "por despesa"; o que se limita é o gasto diário da categoria.
**Regra afetada:** RN-001
**No exemplo:** d-001 + d-002 (alimentação, 2026-07-03); d-003 + d-004 (transporte urbano, 2026-07-06); d-006 + d-007 (alimentação, 2026-07-09).

### AMB-002 — Divisão do limite diário entre despesas da mesma categoria
**Ref. levantamento:** A-02
**Texto original do RH:** "R$ 60 por dia", "R$ 80 por dia", "Despesas acima do limite são reembolsadas parcialmente."
**O que não está claro:** quando a soma do dia excede o limite e a saída mostra o valor de cada item, quanto do limite cabe a cada despesa. Leituras: na ordem em que aparecem na entrada; a maior primeiro; a menor primeiro; proporcional ao valor.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-001 (decidida: soma diária), AMB-004.
**No exemplo:** d-001 + d-002; d-003 + d-004.

### AMB-003 — Hospedagem com várias noites em um único item
**Ref. levantamento:** A-03
**Texto original do RH:** "Hospedagem tem limite de R$ 250 por diária."
**O que não está claro:** se o limite é R$ 250 por item ou R$ 250 multiplicado pelo número de noites. A entrada não informa o número de noites; ele aparece só no texto livre da descrição. O formato de entrada é fixo; hotel e aluguel por temporada chegam igualmente como hospedagem.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-033.
**No exemplo:** d-010 ("2 diarias", R$ 480,00); d-013 ("3 noites", R$ 690,00).

### AMB-004 — O que é "reembolsadas parcialmente"
**Ref. levantamento:** A-04
**Texto original do RH:** "Despesas acima do limite são reembolsadas parcialmente."
**O que não está claro:** qual parte é reembolsada. Leituras: paga até o limite e corta o excedente; paga outra fração; recusa o item. Fronteira: se "acima do limite" significa estritamente maior que o limite.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**No exemplo:** total de 2026-07-03 (d-001 + d-002); total de 2026-07-06 (d-003 + d-004); d-010; d-013; d-014 (R$ 61,00).

### AMB-005 — Fronteira de "acima de R$ 100" para nota fiscal
**Ref. levantamento:** A-05
**Texto original do RH:** "Nota fiscal é obrigatória acima de R$ 100."
**O que não está claro:** se a exigência vale para valor maior que R$ 100,00 ou maior ou igual a R$ 100,00.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**No exemplo:** d-003 (R$ 100,00, sem nota); d-004 (R$ 100,01, sem nota).

### AMB-006 — Valor sobre o qual se mede o patamar da nota fiscal
**Ref. levantamento:** A-06
**Texto original do RH:** "Nota fiscal é obrigatória acima de R$ 100."
**O que não está claro:** se o patamar é medido sobre o valor original do item, sobre o valor depois do limite ou sobre a soma do dia.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-016.
**No exemplo:** d-004 (R$ 100,01, limite de R$ 80,00); total de 2026-07-06 (R$ 200,01); d-013 (R$ 690,00, sem nota).

### AMB-007 — Consequência da falta de nota fiscal obrigatória
**Ref. levantamento:** A-07
**Texto original do RH:** "Nota fiscal é obrigatória acima de R$ 100."
**O que não está claro:** o que acontece com o item sem nota quando ela é obrigatória. Leituras: recusar o item; reembolsar até R$ 100,00; marcar como pendente.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-031.
**No exemplo:** d-004; d-013.

### AMB-008 — O que caracteriza colaborador "em viagem"
**Ref. levantamento:** A-08
**Texto original do RH:** "Colaborador em viagem tem limites ampliados em 50%."
**O que não está claro:** a entrada não traz nenhuma informação de viagem. Leituras: deduzir de outros dados (existência de hospedagem, palavras na descrição); exigir um dado que a entrada não traz; não aplicar a regra enquanto o dado não existir.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-033.
**No exemplo:** d-003 ("Corrida aeroporto"); d-010 ("Hotel Rio"); d-011 (café no hotel); d-013.

### AMB-009 — Alcance e período da ampliação de 50%
**Ref. levantamento:** A-09
**Texto original do RH:** "Colaborador em viagem tem limites ampliados em 50%."
**O que não está claro:** (1) se, além dos limites de categoria (R$ 90, R$ 120, R$ 375), o patamar de R$ 100 da nota fiscal também é ampliado; (2) se a ampliação vale só nos dias da viagem ou em todo o período de competência em que houve viagem.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-008.
**No exemplo:** depende de AMB-008.

### AMB-010 — Período de competência
**Ref. levantamento:** A-10
**Texto original do RH:** "Despesas devem ser lançadas dentro do período de competência."
**O que não está claro:** se vale a data da despesa ou a data de lançamento (que a entrada não traz); qual informação define o período (competência ou início/fim) se discordarem; se as datas de início e fim estão dentro do período; se o item fora do período é recusado, sinalizado ou admitido com tolerância.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-031, AMB-033.
**No exemplo:** d-008 (2026-04-15, "lancado com atraso"); d-014 (2026-07-31, último dia).

### AMB-011 — Critério de duplicata
**Ref. levantamento:** A-11
**Texto original do RH:** "Duplicatas devem ser tratadas."
**O que não está claro:** quais informações precisam coincidir (data, categoria, fornecedor, valor, descrição, identificador) e se duas despesas idênticas podem ser legítimas.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-029.
**No exemplo:** d-006 e d-007 (iguais em tudo, exceto o identificador).

### AMB-012 — O que significa "tratar" duplicatas
**Ref. levantamento:** A-12
**Texto original do RH:** "Duplicatas devem ser tratadas."
**O que não está claro:** leituras: manter uma e recusar as demais; recusar todas; marcar para revisão. Se uma for mantida, qual. Se a duplicata é desconsiderada antes ou depois da soma diária. Se marcada para revisão, qual valor reembolsável aparece na saída.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-011, AMB-029, AMB-031, AMB-016.
**Fora de escopo relacionado:** fluxo de revisão (§3).
**No exemplo:** d-006 e d-007.

### AMB-013 — Categorias aceitas e comparação do nome
**Ref. levantamento:** A-13
**Texto original do RH:** "Categorias fora da política não são reembolsáveis."
**O que não está claro:** se apenas as três categorias com limite estão na política ou se há outras aceitas; se variações de maiúsculas ou acentos ("ALIMENTACAO") correspondem à mesma categoria.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Fora de escopo relacionado:** lista de categorias no lançamento (§3).
**No exemplo:** d-005 (coworking); d-014 (ALIMENTACAO).

### AMB-014 — Arredondamento e casas decimais
**Ref. levantamento:** A-14
**Texto original do RH:** nenhum — a política não trata do caso.
**O que não está claro:** se valores com mais de duas casas são arredondados, truncados ou recusados; com que regra; em que momento (na entrada, por item, no total); e se a comparação com limites e patamares ocorre antes ou depois do arredondamento.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**No exemplo:** d-011 (R$ 33,333).

### AMB-015 — Valores negativos (estornos)
**Ref. levantamento:** A-15
**Texto original do RH:** nenhum — a política não trata do caso.
**O que não está claro:** leituras: ignorar; recusar como dado inválido; abater do total do dia ou do período; associar a uma despesa original. Se o estorno reduz a soma diária. O que acontece quando só há estorno no dia, na categoria ou na entrada.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-001 (decidida: soma diária), AMB-032.
**No exemplo:** d-009 (−R$ 45,00, transporte urbano, sozinho em 2026-07-11).

### AMB-016 — Ordem de aplicação das regras
**Ref. levantamento:** A-16
**Texto original do RH:** nenhum — a política não define ordem.
**O que não está claro:** quando várias regras incidem sobre o mesmo item (competência, categoria, duplicata, nota fiscal, ampliação por viagem, limite), qual é verificada primeiro. A ordem muda o resultado: d-004 pode terminar com R$ 0,00 ou R$ 80,00 conforme a nota seja verificada antes ou depois do limite; d-006 + d-007 mudam conforme a duplicata seja desconsiderada antes ou depois da soma diária.
**Decisão:** PENDENTE (será registrada na §8)
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** todas as demais.
**No exemplo:** d-004; d-006 + d-007; d-008.

### AMB-017 — Tratamento de item com categoria fora da política
**Ref. levantamento:** A-17
**Texto original do RH:** "Categorias fora da política não são reembolsáveis."
**O que não está claro:** o item não é reembolsado e a saída precisa justificar a decisão; falta definir como ele aparece. Leituras: recusar com justificativa; marcar como pendente de correção (categoria possivelmente lançada por engano); tratar como entrada inválida.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-013, AMB-030, AMB-031, AMB-032.
**Fora de escopo relacionado:** fluxo de correção e reenvio (§3).
**No exemplo:** d-005; d-014, dependendo de AMB-013.

### AMB-018 — Duas hospedagens na mesma data
**Ref. levantamento:** A-18
**Texto original do RH:** "Hospedagem tem limite de R$ 250 por diária."
**O que não está claro:** o comportamento quando há duas hospedagens com a mesma data. Leituras: tratar como duplicata; considerar só o maior valor; somar os valores. A entrada não traz horário de entrada e saída, só a data.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-003, AMB-011.
**No exemplo:** nenhum (d-010 e d-013 não se sobrepõem).

### AMB-019 — Dias não úteis
**Ref. levantamento:** L-01
**Texto original do RH:** nenhum.
**O que não está claro:** a política não distingue dia útil de fim de semana ou feriado. Pela letra, não há restrição; falta confirmar se esse silêncio é intencional.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**No exemplo:** d-012 (sábado, "plantao").

### AMB-020 — Despesa de valor zero
**Ref. levantamento:** L-02
**Texto original do RH:** nenhum.
**O que não está claro:** se uma despesa de R$ 0,00 é válida, recusada ou ignorada.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**No exemplo:** nenhum.

### AMB-021 — Entrada inválida
**Ref. levantamento:** L-03
**Texto original do RH:** nenhum.
**O que não está claro:** o comportamento com informação ausente, data inválida, valor não numérico, identificador repetido ou lista vazia; e se a recusa é do arquivo inteiro ou só do item.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-032.
**No exemplo:** nenhum.

### AMB-022 — Moeda
**Ref. levantamento:** L-04
**Texto original do RH:** a política expressa os valores em "R$".
**O que não está claro:** a entrada não traz moeda; falta confirmar como premissa que todos os valores estão em reais.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**No exemplo:** todos.

### AMB-023 — Teto total no período
**Ref. levantamento:** L-05
**Texto original do RH:** nenhum dos nove itens define teto mensal ou por colaborador.
**O que não está claro:** confirmar como premissa que não há limite global.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**No exemplo:** nenhum.

### AMB-024 — Conteúdo da justificativa
**Ref. levantamento:** L-06
**Texto original do RH:** nenhum; o enunciado exige justificativa por item.
**O que não está claro:** o que a justificativa precisa conter (regra aplicada, valores, mais de um motivo).
**Decisão:** PENDENTE (será resolvida na §4)
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**No exemplo:** todos.

### AMB-025 — Item com mais de um motivo de recusa ou redução
**Ref. levantamento:** L-07
**Texto original do RH:** nenhum.
**O que não está claro:** quando um item incide em mais de uma regra (por exemplo, fora do período e duplicado), se a saída mostra só um motivo ou todos.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-016, AMB-024.
**No exemplo:** d-008, conforme as demais decisões.

### AMB-026 — Uso dos dados do colaborador
**Ref. levantamento:** L-08
**Texto original do RH:** nenhum.
**O que não está claro:** se colaborador e centro de custo têm algum efeito no cálculo ou só são repassados para a saída.
**Decisão:** PENDENTE (será resolvida na §4)
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**No exemplo:** cabeçalho da entrada.

### AMB-027 — Totais na saída
**Ref. levantamento:** L-09
**Texto original do RH:** nenhum; o formato da saída é definido nesta spec.
**O que não está claro:** se a saída traz só valores por item ou também totais por dia, por categoria e do período.
**Decisão:** PENDENTE (será resolvida na §4)
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**No exemplo:** todos.

### AMB-028 — Alimentação durante hospedagem
**Ref. levantamento:** L-10
**Texto original do RH:** nenhum.
**O que não está claro:** se alimentação no próprio local de hospedagem (como café da manhã) tem tratamento diferente, por exemplo por já estar incluída na diária, e se indica viagem (AMB-008).
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-008.
**No exemplo:** d-011.

### AMB-029 — Origem e unicidade do identificador da despesa
**Ref. levantamento:** L-11
**Texto original do RH:** nenhum.
**O que não está claro:** se o identificador é gerado por sistema ou digitado pelo colaborador, e se é único. Identificadores diferentes não provam despesas diferentes; identificadores iguais podem indicar duplicata ou entrada inválida.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Afeta:** AMB-011, AMB-012, AMB-021.
**No exemplo:** d-006 e d-007.

### AMB-030 — Categoria informada versus descrição
**Ref. levantamento:** L-12
**Texto original do RH:** nenhum.
**O que não está claro:** se a categoria informada é aceita como está ou questionada a partir da descrição (uma corrida para o aeroporto como transporte urbano; uma categoria fora da política lançada por engano).
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Afeta:** AMB-008, AMB-013, AMB-017.
**No exemplo:** d-003; d-005.

### AMB-031 — Situações possíveis de um item na saída
**Ref. levantamento:** ponto transversal da revisão
**Texto original do RH:** nenhum.
**O que não está claro:** se a saída admite uma situação de "pendente" (usada como opção em AMB-007, AMB-010, AMB-012 e AMB-017) além de reembolsado integral, parcial e recusado.
**Decisão:** PENDENTE (será resolvida na §4)
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Afeta:** AMB-007, AMB-010, AMB-012, AMB-017.

### AMB-032 — Entrada inválida versus item recusado
**Ref. levantamento:** ponto transversal da revisão
**Texto original do RH:** nenhum.
**O que não está claro:** a diferença entre dado malformado e item válido que não é reembolsado, usada em AMB-015, AMB-017 e AMB-021.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Afeta:** AMB-015, AMB-017, AMB-021.

### AMB-033 — Informação que a entrada não traz
**Ref. levantamento:** ponto transversal da revisão
**Texto original do RH:** nenhum; o enunciado exige respeitar o formato de entrada do exemplo.
**O que não está claro:** se uma informação opcional a mais na entrada (número de noites, indicação de viagem, data de lançamento) respeita ou não o formato exigido.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Afeta:** AMB-003, AMB-008, AMB-010.

---

## 7. Casos de borda

| Caso | Entrada | Comportamento esperado | Regra |
|---|---|---|---|
| | | | |

## 8. Ordem de aplicação das regras

<Quando duas regras incidem sobre a mesma despesa, qual vale primeiro? A ordem
muda o resultado. Declarar isso separa spec boa de spec média.>

## 9. Critérios de aceite

O sistema está pronto quando:

- [ ] <critério verificável, sem ler código>
- [ ] <...>

## 10. O que fica em aberto

- As ambiguidades marcadas como PENDENTE na §6 ainda não têm decisão.
- O valor reembolsado de cada item quando o total do dia excede o limite depende de AMB-002 e AMB-004.
- Se duplicatas, estornos e despesas fora do período entram na soma diária depende de AMB-010, AMB-012, AMB-015 e AMB-016.
- O valor do limite pode ser ampliado para colaborador em viagem (AMB-008 e AMB-009).
