# Spec — Motor de Cálculo de Reembolso

**Versão:** 1.0 · **Status:** rascunho · **Última alteração:** 2026-10-18

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
- Não trata despesa em moeda estrangeira; todos os valores da entrada são considerados em reais (ver AMB-022).
- Não aplica teto total de reembolso por período nem por colaborador (ver AMB-023).
- Não gerencia o fluxo de revisão de despesas em dia não útil: prazo, responsável e desfecho da revisão (ver AMB-019).
- Não considera feriados estaduais ou municipais (ver AMB-019).

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

### RN-002 — Teto de reembolso

**Regra:** o valor reembolsado sujeito a um limite nunca excede esse limite. Se o valor sujeito ao limite é menor ou igual ao limite, é reembolsado integralmente; se é maior, reembolsa-se exatamente o valor do limite. Para alimentação e transporte urbano, o valor sujeito ao limite é a soma do dia (RN-001); para hospedagem, a unidade depende de AMB-003. Esta regra não impede reduções previstas em outras regras.
**Origem:** política do RH, item 4; AMB-004.
**Aceite:**
- alimentação com total de R$ 61,00 no dia → R$ 60,00 reembolsados no dia; R$ 1,00 não reembolsado;
- alimentação com total de R$ 60,00 no dia → R$ 60,00 reembolsados no dia;
- transporte urbano com total de R$ 80,01 no dia → R$ 80,00 reembolsados no dia; R$ 0,01 não reembolsado;
- alimentação em 2026-07-03 com total de R$ 110,50 → R$ 60,00 reembolsados no dia; o valor é registrado no total do dia, sem divisão entre os itens (RN-003).

### RN-003 — Reembolso apurado por dia

**Regra:** para alimentação e transporte urbano, o valor reembolsado é apurado e apresentado no total da categoria no dia. Nenhum valor reembolsado é atribuído individualmente aos itens que compõem esse total; cada item é apresentado com sua situação e a indicação do total do dia a que pertence. Quando o total do dia tem um único item, o valor do dia corresponde a esse item.
**Origem:** AMB-002.
**Aceite:** em 2026-07-03, as despesas de alimentação de R$ 72,50 e R$ 38,00 aparecem como itens do total de alimentação do dia; o total do dia é R$ 110,50 e o valor reembolsado do dia é R$ 60,00; nenhum valor reembolsado individual é atribuído a esses itens.

### RN-004 — Teto de hospedagem por diária

**Regra:** o teto de reembolso de um item de hospedagem é R$ 250,00 multiplicado pelo número de diárias, determinado conforme AMB-003. O teto é aplicado conforme RN-002.
**Origem:** política do RH, item 3; AMB-003.
**Aceite:**
- "Hotel Rio - 2 diarias", R$ 480,00 → 2 diárias, teto R$ 500,00, R$ 480,00 dentro do teto;
- "Airbnb 3 noites", R$ 690,00 → 3 diárias, teto R$ 750,00, R$ 690,00 dentro do teto;
- "Pousada - duas Diárias", R$ 600,00 → 2 diárias, teto R$ 500,00, R$ 500,00 reembolsados;
- "Hotel - 2 diárias e 1 noite", R$ 700,00 → 3 diárias, teto R$ 750,00, R$ 700,00 dentro do teto;
- "Hotel - 2 diárias + meia diária", R$ 600,00 → "meia" ignorada, 2 diárias, teto R$ 500,00, R$ 500,00 reembolsados;
- "Hotel 3 estrelas", R$ 300,00 → nenhum número antes de "diária" ou "noite" → 1 diária, R$ 250,00 reembolsados;
- "Hotel - 0 diárias", R$ 300,00 → número inválido → 1 diária, R$ 250,00 reembolsados;
- "Hotel - meia diária", R$ 150,00 → número inválido → 1 diária, R$ 150,00 dentro do teto.

### RN-005 — Itens de mesmo conteúdo

**Regra:** dois itens têm o mesmo conteúdo quando coincidem a data, a categoria, a descrição, o fornecedor, o valor e a indicação de nota fiscal. O identificador não entra na comparação. Os textos (categoria, descrição e fornecedor) são comparados sem diferenciar maiúsculas de minúsculas, letras com e sem acento, nem espaços no início, no fim ou repetidos entre palavras. A comparação de valores com mais de duas casas decimais segue a AMB-014.
**Origem:** AMB-011, AMB-029.
**Aceite:**
- d-006 e d-007 (2026-07-09, alimentação, "Almoco", "Bistro Central", R$ 54,90, com nota) → mesmo conteúdo, apesar dos identificadores diferentes;
- "Almoço" / "Bistro Central" e "almoco" / "bistro  central" → mesmo conteúdo;
- d-003 (R$ 100,00) e d-004 (R$ 100,01), mesmo fornecedor e mesma data → conteúdo diferente (valor e descrição);
- dois itens iguais em tudo, exceto que um tem nota fiscal e o outro não → conteúdo diferente.

### RN-006 — Identificador repetido

**Regra:** o identificador da despesa deve ser único no arquivo. Quando dois ou mais itens têm o mesmo identificador:
- se todos têm o mesmo conteúdo (RN-005), só o primeiro na ordem do arquivo é calculado; os demais são apresentados como desconsiderados por identificador repetido, com referência ao item calculado;
- se algum deles tem conteúdo diferente de outro, nenhum desses itens é calculado; todos são apresentados como recusados por identificador repetido com conteúdo diferente.

Itens desconsiderados ou recusados por esta regra não entram na soma do dia (RN-001). Os demais itens do arquivo são calculados normalmente. O nome de cada situação na saída é definido na AMB-031.
**Origem:** AMB-029.
**Aceite:**
- dois itens `d-020` com o mesmo conteúdo (alimentação, 2026-07-05, R$ 30,00) → o primeiro é calculado e o segundo é desconsiderado, com referência ao primeiro; o total de alimentação de 2026-07-05 é R$ 30,00;
- dois itens `d-020`, um de alimentação em 2026-07-05 (R$ 30,00) e outro de transporte urbano em 2026-07-12 (R$ 45,00) → os dois são recusados e não entram nos totais desses dias;
- três itens `d-020`, dois de alimentação com o mesmo conteúdo (2026-07-05, R$ 30,00) e um de transporte urbano (2026-07-12, R$ 45,00), em qualquer ordem → os três são recusados.

### RN-007 — Dia não útil

**Regra:** são dias não úteis o sábado, o domingo e os feriados nacionais: 01/01, 21/04, 01/05, 07/09, 12/10, 02/11, 15/11, 20/11 e 25/12, além da Sexta-feira Santa (dois dias antes do Domingo de Páscoa do ano). Feriados estaduais e municipais não são considerados. A despesa com data em dia não útil não é reembolsada: fica com valor reembolsado de R$ 0,00, é apresentada como pendente de revisão por dia não útil e não entra na soma do dia (RN-001). O nome da situação na saída é definido na AMB-031.
**Origem:** AMB-019.
**Aceite:**
- d-012 (2026-07-18, sábado, alimentação, R$ 47,20) → pendente de revisão, R$ 0,00, fora do total de alimentação de 2026-07-18;
- despesa em 2026-04-03 (Sexta-feira Santa) ou em 2026-04-21 (terça-feira, Tiradentes) → pendente de revisão;
- despesa em 2026-02-17 (terça-feira de Carnaval) ou em 2026-07-20 (segunda-feira) → dia útil, segue as demais regras.

### RN-008 — Despesa de valor zero

**Regra:** despesa de valor R$ 0,00, já arredondado conforme a RN-009, é recusada por não haver valor a reembolsar. É apresentada na saída com justificativa e não entra na soma do dia (RN-001).
**Origem:** AMB-020.
**Aceite:** item de R$ 0,00 → recusado; não altera o total do dia.

### RN-009 — Arredondamento dos valores da entrada

**Regra:** antes de qualquer outra regra, cada valor da entrada é arredondado para duas casas decimais. Se a parte descartada é igual ou maior que 0,005, arredonda-se afastando do zero; se é menor, ela é descartada. Todas as regras seguintes usam o valor arredondado.
**Origem:** AMB-014.
**Aceite:**
- d-011, R$ 33,333 → R$ 33,33;
- R$ 33,335 → R$ 33,34;
- −R$ 45,005 → −R$ 45,01;
- uma única alimentação no dia de R$ 60,004 → R$ 60,00, igual ao limite, reembolso integral (RN-002);
- R$ 0,004 → R$ 0,00 → valor zero, recusado (RN-008).

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
**Decisão:** para alimentação e transporte urbano, o valor reembolsado é apurado no total da categoria no dia (RN-001, RN-002), sem divisão entre os itens que compõem esse total. Cada item é apresentado com sua situação e com a indicação do total do dia de que faz parte.
**Justificativa:** a política fixa o limite por dia; o valor reembolsável é, portanto, do dia, e reparti-lo entre os itens exigiria um critério que a política não fornece.
**Regra afetada:** RN-003
**Depende de:** AMB-001 e AMB-004 (decididas).
**No exemplo:** d-001 + d-002; d-003 + d-004.

### AMB-003 — Hospedagem com várias noites em um único item
**Ref. levantamento:** A-03
**Texto original do RH:** "Hospedagem tem limite de R$ 250 por diária."
**O que não está claro:** se o limite é R$ 250 por item ou R$ 250 multiplicado pelo número de noites. A entrada não informa o número de noites; ele aparece só no texto livre da descrição. O formato de entrada é fixo; hotel e aluguel por temporada chegam igualmente como hospedagem.
**Decisão:** o limite de hospedagem é de R$ 250,00 por diária; o teto do item é R$ 250,00 multiplicado pelo número de diárias. O número de diárias é lido na descrição:
- conta o número escrito imediatamente antes da palavra "diária" ou "noite", em qualquer forma — singular ou plural, maiúsculas ou minúsculas, com ou sem acento, inclusive "diária(s)" e "noite(s)";
- o número pode estar em algarismos ("2 diarias") ou por extenso ("duas diarias"), sem limite máximo;
- só é válido um número inteiro maior ou igual a 1; meia, zero ou valor negativo são ignorados;
- se houver mais de uma ocorrência válida, os números são somados ("2 diárias e 1 noite" = 3 diárias);
- se a descrição não trouxer nenhum número válido, considera-se uma diária.

**Justificativa:** a política fixa o teto por diária, e hospedagens como aluguel por temporada são pagas de uma vez; o teto precisa acompanhar o número de diárias da estadia.
**Regra afetada:** RN-004
**Depende de:** AMB-033 (decidida).
**No exemplo:** d-010 ("2 diarias", R$ 480,00); d-013 ("3 noites", R$ 690,00).

### AMB-004 — O que é "reembolsadas parcialmente"
**Ref. levantamento:** A-04
**Texto original do RH:** "Despesas acima do limite são reembolsadas parcialmente."
**O que não está claro:** qual parte é reembolsada (até o limite, outra fração ou nada) e se "acima do limite" inclui o valor igual ao limite.
**Decisão:** quando o valor sujeito ao limite é maior que o limite (por exemplo, R$ 60,01 em alimentação), reembolsa-se até o valor do limite e o excedente não é reembolsado. Valor igual ao limite não está acima dele e é reembolsado integralmente.
**Justificativa:** os valores da política funcionam como teto de gasto: paga-se até o teto, nunca acima dele.
**Regra afetada:** RN-002
**No exemplo:** total de 2026-07-03 (d-001 + d-002); total de 2026-07-06 (d-003 + d-004); d-010; d-013; d-014 (R$ 61,00).

### AMB-005 — Fronteira de "acima de R$ 100" para nota fiscal
**Ref. levantamento:** A-05
**Texto original do RH:** "Nota fiscal é obrigatória acima de R$ 100."
**O que não está claro:** se a exigência vale para valor maior que R$ 100,00 ou maior ou igual a R$ 100,00.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Efeito de AMB-014:** a fronteira é comparada com o valor já arredondado (RN-009).
**No exemplo:** d-003 (R$ 100,00, sem nota); d-004 (R$ 100,01, sem nota).

### AMB-006 — Valor sobre o qual se mede o patamar da nota fiscal
**Ref. levantamento:** A-06
**Texto original do RH:** "Nota fiscal é obrigatória acima de R$ 100."
**O que não está claro:** se o patamar é medido sobre o valor original do item, sobre o valor depois do limite ou sobre a soma do dia.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-016.
**Efeito de AMB-002:** não existe valor pago por item; a leitura "valor depois do limite" só se aplica ao total do dia.
**No exemplo:** d-004 (R$ 100,01, limite de R$ 80,00); total de 2026-07-06 (R$ 200,01); d-013 (R$ 690,00, sem nota).

### AMB-007 — Consequência da falta de nota fiscal obrigatória
**Ref. levantamento:** A-07
**Texto original do RH:** "Nota fiscal é obrigatória acima de R$ 100."
**O que não está claro:** o que acontece com o item sem nota quando ela é obrigatória. Leituras: recusar o item; reembolsar até R$ 100,00; marcar como pendente.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-031.
**Efeito de AMB-002:** recusar o item ou limitá-lo a R$ 100,00 altera quanto ele contribui para o total do dia.
**No exemplo:** d-004; d-013.

### AMB-008 — O que caracteriza colaborador "em viagem"
**Ref. levantamento:** A-08
**Texto original do RH:** "Colaborador em viagem tem limites ampliados em 50%."
**O que não está claro:** a entrada não traz nenhuma informação de viagem. Leituras: deduzir de outros dados (existência de hospedagem, palavras na descrição); exigir um dado que a entrada não traz; não aplicar a regra enquanto o dado não existir.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-033 (decidida).
**Efeito de AMB-033:** a leitura "exigir um dado que a entrada não traz" fica descartada.
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
**Depende de:** AMB-031, AMB-033 (decidida).
**Efeito de AMB-033:** a leitura "data de lançamento" fica descartada, pois a entrada não traz essa data.
**Efeito de AMB-003:** uma hospedagem de várias diárias pode ter diárias fora do período de competência.
**No exemplo:** d-008 (2026-04-15, "lancado com atraso"); d-014 (2026-07-31, último dia).

### AMB-011 — Critério de duplicata
**Ref. levantamento:** A-11
**Texto original do RH:** "Duplicatas devem ser tratadas."
**O que não está claro:** quais informações precisam coincidir (data, categoria, fornecedor, valor, descrição, identificador) e se duas despesas idênticas podem ser legítimas.
**Decisão:** são duplicatas os itens com o mesmo conteúdo, conforme a RN-005: todos os campos coincidem, exceto o identificador. Os textos são comparados sem diferenciar maiúsculas, acentos e espaços a mais. O que acontece com as duplicatas, inclusive se duas despesas idênticas podem ser legítimas, é decidido na AMB-012.
**Justificativa:** o identificador não distingue despesas (AMB-029). Um lançamento repetido reproduz todos os demais dados, e diferenças só de grafia não tornam duas despesas diferentes.
**Regra afetada:** RN-005
**Depende de:** AMB-029 (decidida); comparação de valores: AMB-014.
**Afeta:** AMB-012, AMB-018.
**No exemplo:** d-006 e d-007 (mesmo conteúdo, identificadores diferentes).

### AMB-012 — O que significa "tratar" duplicatas
**Ref. levantamento:** A-12
**Texto original do RH:** "Duplicatas devem ser tratadas."
**O que não está claro:** leituras: manter uma e recusar as demais; recusar todas; marcar para revisão. Se uma for mantida, qual. Se a duplicata é desconsiderada antes ou depois da soma diária. Se marcada para revisão, qual valor reembolsável aparece na saída.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-011 e AMB-029 (decididas), AMB-031, AMB-016.
**Efeito de AMB-011 e AMB-029:** o critério de duplicata é a RN-005. Itens com o mesmo identificador e o mesmo conteúdo já são tratados pela RN-006 (o primeiro é calculado, os demais são desconsiderados); o tratamento de duplicatas com identificadores diferentes deve ser coerente com ela.
**Fora de escopo relacionado:** fluxo de revisão (§3).
**No exemplo:** d-006 e d-007.

### AMB-013 — Categorias aceitas e comparação do nome
**Ref. levantamento:** A-13
**Texto original do RH:** "Categorias fora da política não são reembolsáveis."
**O que não está claro:** se apenas as três categorias com limite estão na política ou se há outras aceitas; se variações de maiúsculas ou acentos ("ALIMENTACAO") correspondem à mesma categoria.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Efeito de AMB-011:** na comparação de duplicatas, categorias são comparadas sem diferenciar maiúsculas, acentos e espaços (RN-005). Se isso também vale para reconhecer a categoria na política, a AMB-013 decide.
**Fora de escopo relacionado:** lista de categorias no lançamento (§3).
**No exemplo:** d-005 (coworking); d-014 (ALIMENTACAO).

### AMB-014 — Arredondamento e casas decimais
**Ref. levantamento:** A-14
**Texto original do RH:** nenhum — a política não trata do caso.
**O que não está claro:** se valores com mais de duas casas são arredondados, truncados ou recusados; com que regra; em que momento (na entrada, por item, no total); e se a comparação com limites e patamares ocorre antes ou depois do arredondamento.
**Decisão:** cada valor da entrada é arredondado para duas casas, com 0,005 arredondado afastando do zero, antes de qualquer outra regra (RN-009).
**Justificativa:** o reembolso é pago em centavos; arredondar na entrada faz todas as regras trabalharem sobre o valor que de fato pode ser pago.
**Regra afetada:** RN-009
**Efeito de AMB-002:** não há sobra de centavos a repartir entre itens.
**No exemplo:** d-011 (R$ 33,333).

### AMB-015 — Valores negativos (estornos)
**Ref. levantamento:** A-15
**Texto original do RH:** nenhum — a política não trata do caso.
**O que não está claro:** leituras: ignorar; recusar como dado inválido; abater do total do dia ou do período; associar a uma despesa original. Se o estorno reduz a soma diária. O que acontece quando só há estorno no dia, na categoria ou na entrada.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-001 (decidida: soma diária), AMB-032.
**Efeito de AMB-002:** a leitura "associar a uma despesa original" não se aplica a categorias com limite diário; "abater do total do dia" continua possível.
**Efeito de AMB-014:** o arredondamento de valores negativos segue a RN-009.
**No exemplo:** d-009 (−R$ 45,00, transporte urbano, sozinho em 2026-07-11).

### AMB-016 — Ordem de aplicação das regras
**Ref. levantamento:** A-16
**Texto original do RH:** nenhum — a política não define ordem.
**O que não está claro:** quando várias regras incidem sobre o mesmo item (competência, categoria, duplicata, nota fiscal, ampliação por viagem, limite), qual é verificada primeiro. A ordem muda o resultado: d-004 pode terminar com R$ 0,00 ou R$ 80,00 conforme a nota seja verificada antes ou depois do limite; d-006 + d-007 mudam conforme a duplicata seja desconsiderada antes ou depois da soma diária.
**Decisão:** PENDENTE (será registrada na §8)
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** todas as demais.
**Efeito de AMB-014:** o arredondamento é a primeira etapa (RN-009).
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
**Depende de:** AMB-003 e AMB-011 (decididas).
**Efeito de AMB-002:** se a decisão for "somar", RN-003 passa a valer também para hospedagem.
**Efeito de AMB-011:** duas hospedagens na mesma data só são duplicatas se tiverem o mesmo conteúdo (RN-005); com valor ou descrição diferentes, a leitura "tratar como duplicata" não se aplica.
**Efeito de AMB-003:** uma hospedagem de várias diárias cobre várias datas e pode se sobrepor a outra mesmo com datas informadas diferentes.
**No exemplo:** nenhum (d-010 e d-013 não se sobrepõem).

### AMB-019 — Dias não úteis
**Ref. levantamento:** L-01
**Texto original do RH:** nenhum.
**O que não está claro:** a política não distingue dia útil de fim de semana ou feriado. Pela letra, não há restrição; falta confirmar se esse silêncio é intencional.
**Decisão:** despesa em dia não útil (sábado, domingo ou feriado nacional, conforme RN-007) não é reembolsada e fica pendente de revisão. O fluxo de revisão e os feriados estaduais e municipais estão fora de escopo (§3).
**Justificativa:** a política não menciona dia não útil, mas a despesa nesse dia foge do padrão de trabalho e precisa ser confirmada antes do reembolso. A lista de feriados fica na spec porque a entrada não a traz (AMB-033).
**Regra afetada:** RN-007
**No exemplo:** d-012 (sábado, "plantao").

### AMB-020 — Despesa de valor zero
**Ref. levantamento:** L-02
**Texto original do RH:** nenhum.
**O que não está claro:** se uma despesa de R$ 0,00 é válida, recusada ou ignorada.
**Decisão:** despesa de valor R$ 0,00 é recusada, por não haver valor a reembolsar. Aparece na saída com justificativa e não entra na soma do dia.
**Justificativa:** não há gasto a reembolsar; recusá-la com justificativa mantém o item visível na saída.
**Regra afetada:** RN-008
**No exemplo:** nenhum.

### AMB-021 — Entrada inválida
**Ref. levantamento:** L-03
**Texto original do RH:** nenhum.
**O que não está claro:** o comportamento com informação ausente, data inválida, valor não numérico, identificador repetido ou lista vazia; e se a recusa é do arquivo inteiro ou só do item.
**Decisão:** PENDENTE
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Depende de:** AMB-032.
**Efeito de AMB-029:** identificador repetido não torna a entrada inválida; é tratado pela RN-006.
**No exemplo:** nenhum.

### AMB-022 — Moeda
**Ref. levantamento:** L-04
**Texto original do RH:** a política expressa os valores em "R$".
**O que não está claro:** a entrada não traz moeda; falta confirmar como premissa que todos os valores estão em reais.
**Decisão:** premissa: todos os valores da entrada estão em reais; não há conversão de moeda. Despesa em moeda estrangeira está fora de escopo (§3).
**Justificativa:** a política expressa os valores em reais e a entrada não informa moeda (AMB-033).
**Regra afetada:** nenhuma (premissa).
**No exemplo:** todos.

### AMB-023 — Teto total no período
**Ref. levantamento:** L-05
**Texto original do RH:** nenhum dos nove itens define teto mensal ou por colaborador.
**O que não está claro:** confirmar como premissa que não há limite global.
**Decisão:** premissa: não há teto total por período nem por colaborador; valem só os limites da política. Teto global está fora de escopo (§3).
**Justificativa:** nenhum item da política define teto global.
**Regra afetada:** nenhuma (premissa).
**No exemplo:** nenhum.

### AMB-024 — Conteúdo da justificativa
**Ref. levantamento:** L-06
**Texto original do RH:** nenhum; o enunciado exige justificativa por item.
**O que não está claro:** o que a justificativa precisa conter (regra aplicada, valores, mais de um motivo).
**Decisão:** PENDENTE (será resolvida na §4)
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Efeito de AMB-002:** a justificativa do item cita o total do dia de que faz parte; o total do dia precisa de justificativa própria.
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
**Decisão:** os dados do colaborador (identificador, nome e centro de custo) não afetam o cálculo e são repetidos na saída sem alteração.
**Justificativa:** a política não vincula limites ao colaborador nem ao centro de custo; repeti-los na saída identifica de quem é o reembolso.
**Regra afetada:** §4 (saída).
**No exemplo:** cabeçalho da entrada.

### AMB-027 — Totais na saída
**Ref. levantamento:** L-09
**Texto original do RH:** nenhum; o formato da saída é definido nesta spec.
**O que não está claro:** se a saída traz só valores por item ou também totais por dia, por categoria e do período.
**Decisão:** PENDENTE (será resolvida na §4)
**Justificativa:** PENDENTE
**Regra afetada:** PENDENTE
**Efeito de AMB-002:** parcialmente decidida — a saída precisa ter o total por categoria e dia para alimentação e transporte urbano; os demais totais seguem pendentes.
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
**Decisão:** identificadores diferentes não provam que as despesas são diferentes; o identificador não entra na comparação de duplicatas (AMB-011). O identificador deve ser único no arquivo. Itens com o mesmo identificador seguem a RN-006: com o mesmo conteúdo, só o primeiro na ordem do arquivo é calculado; com conteúdo diferente, todos são recusados.
**Justificativa:** a saída identifica cada item pelo identificador (RN-003). Com o mesmo conteúdo, os itens são o mesmo lançamento; com conteúdo diferente, não há como saber qual deles é o correto.
**Regra afetada:** RN-005, RN-006
**Afeta:** AMB-011, AMB-012, AMB-021.
**No exemplo:** nenhum identificador repetido. d-006 e d-007 têm identificadores diferentes e mesmo conteúdo (AMB-011).

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
**Efeito de AMB-002:** "reembolsado parcialmente" não pode ser situação do item em categoria com limite diário; é preciso uma situação do dia ou uma situação do item como "compõe o total do dia".
**Efeito de AMB-019:** passa a existir a situação "pendente de revisão por dia não útil", com valor de R$ 0,00 (RN-007).
**Efeito de AMB-029:** a saída precisa de uma situação para o item desconsiderado por identificador repetido e outra para o item recusado por identificador repetido com conteúdo diferente.

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
**Decisão:** a entrada não recebe campos além dos presentes em `exemplos/despesas-exemplo.json`.
**Justificativa:** o formato de entrada é fixo pelo enunciado.
**Regra afetada:** nenhuma; restringe as opções de AMB-003, AMB-008 e AMB-010.
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
- Como o total do dia e a situação de cada item aparecem na saída depende da §4 (AMB-024, AMB-027, AMB-031).
- Se duplicatas, estornos e despesas fora do período entram na soma diária depende de AMB-010, AMB-012, AMB-015 e AMB-016.
- O valor do limite pode ser ampliado para colaborador em viagem (AMB-008 e AMB-009).
