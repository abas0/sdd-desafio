# Spec — Motor de Cálculo de Reembolso

**Versão:** 1.0 · **Status:** rascunho · **Última alteração:** 2026-10-19

> **Regra de ouro deste arquivo:** ele descreve o QUÊ e o PORQUÊ. Nenhuma linha
> aqui pode citar linguagem, biblioteca, classe, função ou estrutura de pasta.
> Se apareceu solução, o lugar dela é o `plan.md`.
>
> **Teste de aceitação da própria spec:** uma pessoa que nunca viu o projeto
> consegue, lendo só este arquivo, verificar se o sistema está correto?

---

## 1. Problema

O RH recebe as despesas lançadas pelos colaboradores e precisa aplicar uma política de reembolso de nove itens, escrita em linguagem natural e com lacunas. Aplicada à mão, a mesma despesa recebe decisões diferentes conforme quem a analisa, e o colaborador nem sempre sabe por que recebeu menos do que gastou.

## 2. Objetivo

Dado o arquivo de despesas de um colaborador em um período de competência, o sistema calcula, sempre da mesma forma, quanto é reembolsado e justifica a decisão sobre cada despesa, conforme as regras desta spec.

## 3. Fora de escopo

- Não gerencia o fluxo de revisão de hospedagens sobrepostas: prazo, responsável e desfecho (ver AMB-018).
- Não gerencia o fluxo de revisão de estornos de hospedagem sem estadia correspondente nem a reavaliação de itens pendentes com estornos vinculados (ver AMB-015).
- Não gerencia o envio posterior da nota fiscal: prazo e reavaliação do item pendente (ver AMB-007).
- Não gerencia a correção e o reenvio de despesas recusadas por categoria fora da política ou por descrição incompatível com a categoria: quem corrige e em que prazo (ver AMB-017, AMB-030).
- Não oferece lista de categorias no momento do lançamento da despesa; isso pertence ao sistema que gera a entrada (ver AMB-013).
- Não trata despesa em moeda estrangeira; todos os valores da entrada são considerados em reais (ver AMB-022).
- Não aplica teto total de reembolso por período nem por colaborador (ver AMB-023).
- Não gerencia o fluxo de revisão de despesas em dia não útil: prazo, responsável e desfecho da revisão (ver AMB-019).
- Não considera feriados estaduais ou municipais (ver AMB-019).

## 4. Entrada e saída

**Entrada:** conforme `exemplos/despesas-exemplo.json`. Campos e significado:

| Campo | Tipo | Significado | Obrigatório |
|---|---|---|---|
| `colaborador.id` | texto | identificador do colaborador | sim |
| `colaborador.nome` | texto | nome do colaborador | sim |
| `colaborador.centro_custo` | texto | centro de custo | sim |
| `periodo.competencia` | texto AAAA-MM | mês de competência | sim |
| `periodo.inicio` | data AAAA-MM-DD | primeiro dia do período (RN-014) | sim |
| `periodo.fim` | data AAAA-MM-DD | último dia do período (RN-014) | sim |
| `despesas` | lista | despesas do período; pode ser vazia | sim |
| `despesas[].id` | texto não vazio | identificador da despesa, único no arquivo (RN-006) | sim |
| `despesas[].data` | data AAAA-MM-DD | data da despesa; em hospedagem, data de entrada (RN-013) | sim |
| `despesas[].categoria` | texto | categoria informada (RN-010) | sim |
| `despesas[].descricao` | texto não vazio | descrição livre (RN-004, RN-011, RN-013) | sim |
| `despesas[].fornecedor` | texto não vazio | fornecedor | sim |
| `despesas[].valor` | número | valor em reais; negativo é estorno (RN-016) | sim |
| `despesas[].tem_nota_fiscal` | verdadeiro ou falso | se há nota fiscal (RN-012) | sim |

Entrada que não atende a esta tabela é inválida (RN-018). Campos a mais são ignorados.

**Saída:** um JSON com cinco partes:

| Campo | Tipo | Significado |
|---|---|---|
| `colaborador` | objeto | copiado da entrada, sem alteração (AMB-026) |
| `periodo` | objeto | copiado da entrada, sem alteração |
| `itens` | lista | um registro por despesa da entrada, na mesma ordem |
| `totais_diarios` | lista | um registro por dia e categoria de alimentação ou transporte urbano com pelo menos um item na soma (RN-003), em ordem de data e categoria |
| `resumo` | objeto | totais do período |

Campos de cada item:

| Campo | Tipo | Significado |
|---|---|---|
| `id`, `data`, `descricao`, `fornecedor`, `tem_nota_fiscal` | como na entrada | copiados da entrada |
| `categoria_informada` | texto | categoria como veio na entrada |
| `categoria` | texto ou nulo | categoria reconhecida (RN-010): `alimentacao`, `transporte_urbano` ou `hospedagem`; nulo se fora da política |
| `valor_informado` | número | valor como veio na entrada |
| `valor_considerado` | número | valor arredondado (RN-009) |
| `situacao` | texto | ver tabela de situações |
| `motivo` | texto ou nulo | ver tabela de situações |
| `outros_motivos` | lista | motivos de outras regras que também se aplicariam, na ordem da §8 (RN-019); vazia se não houver |
| `referencia` | texto ou nulo | `id` do item relacionado: item calculado (duplicata ou identificador repetido) ou hospedagem vinculada (estorno) |
| `total_do_dia` | objeto ou nulo | `{ "data", "categoria" }` do total a que o item pertence; só para alimentação e transporte urbano na soma do dia |
| `diarias`, `teto` | número | só para hospedagem calculada (RN-004) |
| `valor_liquido` | número | só para hospedagem com estorno abatido (RN-016): valor depois do abatimento, comparado com o teto |
| `valor_reembolsado` | número ou nulo | hospedagem calculada: valor pago; item não reembolsado: 0.00; item na soma do dia ou estorno abatido: nulo, pois o valor está no total do dia ou na hospedagem (RN-003) |
| `regras` | lista | RNs aplicadas |
| `justificativa` | texto | motivo, valores comparados e limite ou teto (AMB-024) |

Situações e motivos (AMB-031):

| `situacao` | Quando | `motivo` |
|---|---|---|
| `compoe_total_do_dia` | alimentação ou transporte urbano na soma do dia | nulo |
| `abatido` | estorno de hospedagem abatido de uma hospedagem calculada (RN-016) | nulo |
| `reembolsado` | hospedagem dentro do teto | nulo |
| `reembolsado_parcialmente` | hospedagem acima do teto | nulo |
| `recusado` | não será pago | `categoria_fora_da_politica`, `descricao_incompativel`, `fora_do_periodo`, `valor_zero`, `identificador_repetido_conteudo_diferente` |
| `pendente` | pode ser pago após uma ação fora do sistema | `nota_fiscal_ausente`, `dia_nao_util`, `sobreposicao_hospedagem`, `estorno_sem_hospedagem` |
| `desconsiderado` | cópia de outro item | `duplicata`, `identificador_repetido` |

Estorno vinculado a hospedagem não reembolsada recebe a mesma situação e o mesmo motivo dela, com `referencia` para ela (RN-016).

Campos de cada total diário: `data`, `categoria`, `itens` (ids na soma), `valor_total` (pode ser negativo), `em_viagem` (RN-013), `limite`, `valor_reembolsado`, `situacao` (`integral` se o total é menor ou igual ao limite e maior que zero; `parcial` se é maior que o limite; `sem_valor` se é menor ou igual a zero), `regras` e `justificativa`.

Campos do resumo: `total_reembolsado` (soma dos `valor_reembolsado` dos totais diários e das hospedagens calculadas) e `quantidade_por_situacao` (as sete situações, inclusive as com zero).

Valores monetários são escritos com exatamente duas casas decimais, em reais; `valor_informado` repete a entrada. O texto das justificativas abaixo é ilustrativo: o que se exige é o conteúdo (motivo, valores comparados, limite ou teto).

**Exemplo:** saída para `exemplos/despesas-exemplo.json`.

```json
{
  "colaborador": { "id": "c-0417", "nome": "Marina Volpi", "centro_custo": "CC-ENG-PLATAFORMA" },
  "periodo": { "competencia": "2026-07", "inicio": "2026-07-01", "fim": "2026-07-31" },
  "itens": [
    {
      "id": "d-001", "data": "2026-07-03",
      "categoria_informada": "alimentacao", "categoria": "alimentacao",
      "descricao": "Almoco com cliente", "fornecedor": "Restaurante Tavola",
      "valor_informado": 72.50, "valor_considerado": 72.50, "tem_nota_fiscal": true,
      "situacao": "compoe_total_do_dia", "motivo": null, "outros_motivos": [], "referencia": null,
      "total_do_dia": { "data": "2026-07-03", "categoria": "alimentacao" },
      "valor_reembolsado": null,
      "regras": ["RN-001", "RN-003"],
      "justificativa": "Compõe o total de alimentação de 2026-07-03; o valor reembolsado é apurado no total do dia."
    },
    {
      "id": "d-002", "data": "2026-07-03",
      "categoria_informada": "alimentacao", "categoria": "alimentacao",
      "descricao": "Jantar apos reuniao", "fornecedor": "Cantina do Porto",
      "valor_informado": 38.00, "valor_considerado": 38.00, "tem_nota_fiscal": true,
      "situacao": "compoe_total_do_dia", "motivo": null, "outros_motivos": [], "referencia": null,
      "total_do_dia": { "data": "2026-07-03", "categoria": "alimentacao" },
      "valor_reembolsado": null,
      "regras": ["RN-001", "RN-003"],
      "justificativa": "Compõe o total de alimentação de 2026-07-03; o valor reembolsado é apurado no total do dia."
    },
    {
      "id": "d-003", "data": "2026-07-06",
      "categoria_informada": "transporte_urbano", "categoria": "transporte_urbano",
      "descricao": "Corrida aeroporto", "fornecedor": "TaxiApp",
      "valor_informado": 100.00, "valor_considerado": 100.00, "tem_nota_fiscal": false,
      "situacao": "compoe_total_do_dia", "motivo": null, "outros_motivos": [], "referencia": null,
      "total_do_dia": { "data": "2026-07-06", "categoria": "transporte_urbano" },
      "valor_reembolsado": null,
      "regras": ["RN-012", "RN-001", "RN-003"],
      "justificativa": "Valor de R$ 100,00 não exige nota fiscal; compõe o total de transporte urbano de 2026-07-06."
    },
    {
      "id": "d-004", "data": "2026-07-06",
      "categoria_informada": "transporte_urbano", "categoria": "transporte_urbano",
      "descricao": "Corrida hotel", "fornecedor": "TaxiApp",
      "valor_informado": 100.01, "valor_considerado": 100.01, "tem_nota_fiscal": false,
      "situacao": "pendente", "motivo": "nota_fiscal_ausente", "outros_motivos": [], "referencia": null,
      "total_do_dia": null,
      "valor_reembolsado": 0.00,
      "regras": ["RN-012"],
      "justificativa": "Valor de R$ 100,01 acima de R$ 100,00 sem nota fiscal; pendente até o envio da nota."
    },
    {
      "id": "d-005", "data": "2026-07-07",
      "categoria_informada": "coworking", "categoria": null,
      "descricao": "Diaria em espaco compartilhado", "fornecedor": "HubOffice",
      "valor_informado": 89.00, "valor_considerado": 89.00, "tem_nota_fiscal": true,
      "situacao": "recusado", "motivo": "categoria_fora_da_politica", "outros_motivos": [], "referencia": null,
      "total_do_dia": null,
      "valor_reembolsado": 0.00,
      "regras": ["RN-010"],
      "justificativa": "Categoria \"coworking\" fora da política (alimentação, transporte urbano, hospedagem)."
    },
    {
      "id": "d-006", "data": "2026-07-09",
      "categoria_informada": "alimentacao", "categoria": "alimentacao",
      "descricao": "Almoco", "fornecedor": "Bistro Central",
      "valor_informado": 54.90, "valor_considerado": 54.90, "tem_nota_fiscal": true,
      "situacao": "compoe_total_do_dia", "motivo": null, "outros_motivos": [], "referencia": null,
      "total_do_dia": { "data": "2026-07-09", "categoria": "alimentacao" },
      "valor_reembolsado": null,
      "regras": ["RN-001", "RN-003"],
      "justificativa": "Compõe o total de alimentação de 2026-07-09; o valor reembolsado é apurado no total do dia."
    },
    {
      "id": "d-007", "data": "2026-07-09",
      "categoria_informada": "alimentacao", "categoria": "alimentacao",
      "descricao": "Almoco", "fornecedor": "Bistro Central",
      "valor_informado": 54.90, "valor_considerado": 54.90, "tem_nota_fiscal": true,
      "situacao": "desconsiderado", "motivo": "duplicata", "outros_motivos": [], "referencia": "d-006",
      "total_do_dia": null,
      "valor_reembolsado": 0.00,
      "regras": ["RN-005", "RN-015"],
      "justificativa": "Mesmo conteúdo de d-006; desconsiderado por duplicata."
    },
    {
      "id": "d-008", "data": "2026-04-15",
      "categoria_informada": "alimentacao", "categoria": "alimentacao",
      "descricao": "Almoco de abril lancado com atraso", "fornecedor": "Restaurante Tavola",
      "valor_informado": 41.00, "valor_considerado": 41.00, "tem_nota_fiscal": true,
      "situacao": "recusado", "motivo": "fora_do_periodo", "outros_motivos": [], "referencia": null,
      "total_do_dia": null,
      "valor_reembolsado": 0.00,
      "regras": ["RN-014"],
      "justificativa": "Data 2026-04-15 fora do período de 2026-07-01 a 2026-07-31."
    },
    {
      "id": "d-009", "data": "2026-07-11",
      "categoria_informada": "transporte_urbano", "categoria": "transporte_urbano",
      "descricao": "Estorno de corrida cancelada", "fornecedor": "TaxiApp",
      "valor_informado": -45.00, "valor_considerado": -45.00, "tem_nota_fiscal": false,
      "situacao": "pendente", "motivo": "dia_nao_util", "outros_motivos": [], "referencia": null,
      "total_do_dia": null,
      "valor_reembolsado": 0.00,
      "regras": ["RN-007"],
      "justificativa": "2026-07-11 é sábado; transporte urbano em dia não útil fica pendente de revisão."
    },
    {
      "id": "d-010", "data": "2026-07-14",
      "categoria_informada": "hospedagem", "categoria": "hospedagem",
      "descricao": "Hotel Rio - 2 diarias", "fornecedor": "Hotel Copa Sul",
      "valor_informado": 480.00, "valor_considerado": 480.00, "tem_nota_fiscal": true,
      "situacao": "reembolsado", "motivo": null, "outros_motivos": [], "referencia": null,
      "total_do_dia": null,
      "diarias": 2, "teto": 500.00,
      "valor_reembolsado": 480.00,
      "regras": ["RN-004", "RN-002"],
      "justificativa": "2 diárias, teto de R$ 500,00; valor de R$ 480,00 dentro do teto."
    },
    {
      "id": "d-011", "data": "2026-07-15",
      "categoria_informada": "alimentacao", "categoria": "alimentacao",
      "descricao": "Cafe da manha hotel", "fornecedor": "Hotel Copa Sul",
      "valor_informado": 33.333, "valor_considerado": 33.33, "tem_nota_fiscal": true,
      "situacao": "compoe_total_do_dia", "motivo": null, "outros_motivos": [], "referencia": null,
      "total_do_dia": { "data": "2026-07-15", "categoria": "alimentacao" },
      "valor_reembolsado": null,
      "regras": ["RN-009", "RN-001", "RN-003"],
      "justificativa": "Valor de R$ 33,333 arredondado para R$ 33,33; compõe o total de alimentação de 2026-07-15."
    },
    {
      "id": "d-012", "data": "2026-07-18",
      "categoria_informada": "alimentacao", "categoria": "alimentacao",
      "descricao": "Almoco de sabado - plantao", "fornecedor": "Padaria Uniao",
      "valor_informado": 47.20, "valor_considerado": 47.20, "tem_nota_fiscal": true,
      "situacao": "pendente", "motivo": "dia_nao_util", "outros_motivos": [], "referencia": null,
      "total_do_dia": null,
      "valor_reembolsado": 0.00,
      "regras": ["RN-007"],
      "justificativa": "2026-07-18 é sábado; alimentação em dia não útil fica pendente de revisão."
    },
    {
      "id": "d-013", "data": "2026-07-22",
      "categoria_informada": "hospedagem", "categoria": "hospedagem",
      "descricao": "Airbnb 3 noites", "fornecedor": "Airbnb",
      "valor_informado": 690.00, "valor_considerado": 690.00, "tem_nota_fiscal": false,
      "situacao": "pendente", "motivo": "nota_fiscal_ausente", "outros_motivos": [], "referencia": null,
      "total_do_dia": null,
      "valor_reembolsado": 0.00,
      "regras": ["RN-012"],
      "justificativa": "Valor de R$ 690,00 acima de R$ 100,00 sem nota fiscal; pendente até o envio da nota."
    },
    {
      "id": "d-014", "data": "2026-07-31",
      "categoria_informada": "ALIMENTACAO", "categoria": "alimentacao",
      "descricao": "Jantar de encerramento", "fornecedor": "Restaurante Tavola",
      "valor_informado": 61.00, "valor_considerado": 61.00, "tem_nota_fiscal": true,
      "situacao": "compoe_total_do_dia", "motivo": null, "outros_motivos": [], "referencia": null,
      "total_do_dia": { "data": "2026-07-31", "categoria": "alimentacao" },
      "valor_reembolsado": null,
      "regras": ["RN-010", "RN-001", "RN-003"],
      "justificativa": "Categoria \"ALIMENTACAO\" reconhecida como alimentação; compõe o total de alimentação de 2026-07-31."
    }
  ],
  "totais_diarios": [
    {
      "data": "2026-07-03", "categoria": "alimentacao", "itens": ["d-001", "d-002"],
      "valor_total": 110.50, "em_viagem": false, "limite": 60.00,
      "valor_reembolsado": 60.00, "situacao": "parcial",
      "regras": ["RN-001", "RN-002", "RN-003"],
      "justificativa": "Total de R$ 110,50 acima do limite diário de R$ 60,00; reembolsados R$ 60,00."
    },
    {
      "data": "2026-07-06", "categoria": "transporte_urbano", "itens": ["d-003"],
      "valor_total": 100.00, "em_viagem": true, "limite": 120.00,
      "valor_reembolsado": 100.00, "situacao": "integral",
      "regras": ["RN-013", "RN-001", "RN-002", "RN-003"],
      "justificativa": "Dia de viagem (\"aeroporto\" em d-003): limite ampliado para R$ 120,00. Total de R$ 100,00 dentro do limite; reembolsados R$ 100,00."
    },
    {
      "data": "2026-07-09", "categoria": "alimentacao", "itens": ["d-006"],
      "valor_total": 54.90, "em_viagem": false, "limite": 60.00,
      "valor_reembolsado": 54.90, "situacao": "integral",
      "regras": ["RN-001", "RN-002", "RN-003"],
      "justificativa": "Total de R$ 54,90 dentro do limite diário de R$ 60,00; reembolsados R$ 54,90."
    },
    {
      "data": "2026-07-15", "categoria": "alimentacao", "itens": ["d-011"],
      "valor_total": 33.33, "em_viagem": true, "limite": 90.00,
      "valor_reembolsado": 33.33, "situacao": "integral",
      "regras": ["RN-013", "RN-001", "RN-002", "RN-003"],
      "justificativa": "Dia de viagem (estadia de d-010): limite ampliado para R$ 90,00. Total de R$ 33,33 dentro do limite; reembolsados R$ 33,33."
    },
    {
      "data": "2026-07-31", "categoria": "alimentacao", "itens": ["d-014"],
      "valor_total": 61.00, "em_viagem": false, "limite": 60.00,
      "valor_reembolsado": 60.00, "situacao": "parcial",
      "regras": ["RN-001", "RN-002", "RN-003"],
      "justificativa": "Total de R$ 61,00 acima do limite diário de R$ 60,00; reembolsados R$ 60,00."
    }
  ],
  "resumo": {
    "total_reembolsado": 788.23,
    "quantidade_por_situacao": {
      "compoe_total_do_dia": 6, "abatido": 0, "reembolsado": 1, "reembolsado_parcialmente": 0,
      "recusado": 2, "pendente": 4, "desconsiderado": 1
    }
  }
}
```

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

**Exceção:** um item de hospedagem com data de entrada em dia não útil segue as demais regras se os dias cobertos pela estadia (RN-013) incluem pelo menos um dia útil. Estornos de hospedagem não são estadias: em dia não útil, ficam pendentes de revisão como os demais itens. Alimentação e transporte urbano em dia não útil ficam pendentes de revisão mesmo em dia de viagem.
**Origem:** AMB-019, AMB-008.
**Aceite:**
- d-012 (2026-07-18, sábado, alimentação, R$ 47,20) → pendente de revisão, R$ 0,00, fora do total de alimentação de 2026-07-18;
- despesa em 2026-04-03 (Sexta-feira Santa) ou em 2026-04-21 (terça-feira, Tiradentes) → pendente de revisão;
- despesa em 2026-02-17 (terça-feira de Carnaval) ou em 2026-07-20 (segunda-feira) → dia útil, segue as demais regras;
- hospedagem com entrada em 2026-07-19 (domingo), 1 diária → cobre 19 e 20/07 (segunda) → segue as demais regras;
- hospedagem com entrada em 2026-07-18 (sábado), 1 diária → cobre 18 e 19/07, sem dia útil → pendente de revisão;
- jantar em 2026-07-19 (domingo), durante essa estadia → pendente de revisão;
- estorno de hospedagem em 2026-07-18 (sábado), "Estorno 2 diárias", −R$ 80,00 → pendente de revisão.

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

### RN-010 — Categorias da política

**Regra:** as categorias da política são alimentação, transporte urbano e hospedagem. A categoria informada é reconhecida sem diferenciar maiúsculas e minúsculas, letras com e sem acento, nem espaços no início, no fim ou repetidos entre palavras; sublinhado, espaço e hífen são equivalentes. Item cuja categoria não corresponde a nenhuma delas é recusado com a justificativa "categoria fora da política", fica com valor reembolsado de R$ 0,00 e não entra em nenhuma soma do dia.
**Origem:** política do RH, itens 1, 2, 3 e 9; AMB-013, AMB-017.
**Aceite:**
- d-014, "ALIMENTACAO" → alimentação; total de alimentação de 2026-07-31 de R$ 61,00 → R$ 60,00 (RN-002);
- "Alimentação", "Transporte Urbano" e "transporte-urbano" → reconhecidas como alimentação e transporte urbano;
- d-005, "coworking" → recusado, categoria fora da política, R$ 0,00.

### RN-011 — Descrição compatível com a categoria

**Regra:** item cuja descrição contém palavra associada a outra categoria e nenhuma palavra associada à sua própria categoria é recusado com a justificativa "descrição incompatível com a categoria", fica com R$ 0,00 e não entra em nenhuma soma do dia. Descrição sem palavra de nenhuma categoria não é recusada por esta regra. Palavras por categoria:

| Categoria | Palavras |
|---|---|
| alimentação | almoço, jantar, café, lanche, refeição, restaurante, padaria |
| transporte urbano | corrida, táxi, uber, ônibus, metrô |
| hospedagem | hotel, pousada, hostel, airbnb, diária, noite |

As palavras são comparadas sem diferenciar maiúsculas e acentos, como palavra inteira, no singular ou no plural.
**Origem:** AMB-030.
**Aceite:**
- d-011, alimentação, "Cafe da manha hotel" → aceito: tem "hotel" (hospedagem), mas também "café";
- d-004, transporte urbano, "Corrida hotel" → aceito: tem "hotel", mas também "corrida";
- alimentação, "Hotel Copa Sul" → recusado: só tem palavra de hospedagem;
- hospedagem, "Almoço com cliente" → recusado: só tem palavra de alimentação;
- alimentação, "Despesa diversa" → aceito: nenhuma palavra de nenhuma categoria;
- hospedagem, "Jantar no hotel" → aceito: tem "hotel", da própria categoria;
- os 12 itens do exemplo com categoria da política → todos aceitos por esta regra.

### RN-012 — Nota fiscal obrigatória

**Regra:** a nota fiscal é obrigatória para item com valor, já arredondado (RN-009), maior que R$ 100,00. Item sem nota fiscal quando ela é obrigatória não é reembolsado: fica com R$ 0,00, é apresentado como pendente de nota fiscal e não entra na soma do dia (RN-001). O nome da situação na saída é definido na AMB-031.
**Origem:** política do RH, item 5; AMB-005, AMB-006, AMB-007.
**Aceite:**
- d-003, R$ 100,00 sem nota → nota não exigida, segue as demais regras;
- d-004, R$ 100,01 sem nota → pendente de nota fiscal, R$ 0,00;
- total de transporte urbano de 2026-07-06 → só d-003, R$ 100,00 → R$ 80,00 reembolsados (RN-002);
- d-013, R$ 690,00 sem nota → pendente de nota fiscal, R$ 0,00;
- d-010, R$ 480,00 com nota → segue a RN-004;
- R$ 100,004 sem nota → arredondado para R$ 100,00 → nota não exigida.

### RN-013 — Colaborador em viagem

**Regra:** a data informada na hospedagem é a data de entrada. A estadia cobre a data de entrada, os dias seguintes, um por diária (RN-004), e o dia de saída: são cobertos "número de diárias + 1" dias. Um dia é de viagem quando:
- é coberto por uma estadia; ou
- há na data um item cuja descrição contém uma das palavras de viagem: aeroporto, rodoviária, viagem, voo ou embarque. A comparação segue a RN-011.

Esses itens marcam o dia como de viagem mesmo que não sejam reembolsados (recusados, pendentes ou desconsiderados). Em dia de viagem, os limites diários de alimentação e transporte urbano são ampliados em 50%: passam a R$ 90,00 e R$ 120,00. O teto de hospedagem e o patamar da nota fiscal (RN-012) não mudam. Em dia não útil, a ampliação não tem efeito, porque alimentação e transporte ficam pendentes (RN-007).
**Origem:** política do RH, item 6; AMB-008, AMB-009.
**Aceite:**
- d-010 (entrada em 2026-07-14, "2 diarias") → 14, 15 e 16/07 são dias de viagem;
- d-013 (entrada em 2026-07-22, "3 noites", pendente de nota) → 22 a 25/07 são dias de viagem;
- d-003 ("Corrida aeroporto", 06/07) → dia de viagem; o total de transporte urbano de 06/07 é R$ 100,00 (d-004 está pendente) → R$ 100,00 reembolsados (limite de R$ 120,00);
- d-011 (15/07, alimentação, R$ 33,33) → limite de R$ 90,00; R$ 33,33 reembolsados;
- alimentação de R$ 80,00 em 2026-07-23 (dia coberto por d-013) → R$ 80,00 reembolsados;
- 03/07, alimentação de R$ 110,50, sem viagem → R$ 60,00 reembolsados;
- hospedagem em dia de viagem → o teto continua em R$ 250,00 por diária;
- corrida de R$ 110,00 sem nota em dia de viagem → pendente de nota fiscal.

### RN-014 — Período de competência

**Regra:** o período vai do início ao fim informados, incluindo os dois dias. O início deve ser o primeiro dia do mês da competência, e o fim, o último dia desse mês; caso contrário, a entrada é inválida (AMB-021). Um item com data fora do período é recusado com a justificativa "fora do período de competência", fica com R$ 0,00 e não entra em nenhuma soma. Para hospedagem, vale a data de entrada informada: diárias que passam do fim do período não são cortadas.
**Origem:** política do RH, item 7; AMB-010.
**Aceite:**
- d-008 (2026-04-15) → recusado, fora do período;
- d-014 (2026-07-31) e um item em 2026-07-01 → dentro do período;
- competência 2026-07 com fim em 2026-07-15 ou em 2026-08-05 → entrada inválida;
- hospedagem com entrada em 2026-07-30, "3 diárias", R$ 600,00 → dentro do período, teto de R$ 750,00, R$ 600,00 reembolsados;
- hospedagem com entrada em 2026-08-10 no arquivo de julho → recusada, fora do período.

### RN-015 — Duplicatas

**Regra:** quando dois ou mais itens com identificadores diferentes têm o mesmo conteúdo (RN-005), só o primeiro na ordem do arquivo é calculado. Os demais são apresentados como desconsiderados por duplicata, com referência ao item calculado, e não entram na soma do dia.
**Origem:** política do RH, item 8; AMB-012.
**Aceite:**
- d-006 → calculado; d-007 → desconsiderado por duplicata, com referência a d-006; o total de alimentação de 2026-07-09 é R$ 54,90 → R$ 54,90 reembolsados;
- três itens com o mesmo conteúdo → o primeiro é calculado e os outros dois são desconsiderados.

### RN-016 — Estornos

**Regra:** item de valor negativo é um estorno.
- **Alimentação e transporte urbano:** o estorno entra na soma do dia da sua categoria (RN-001) e a reduz antes da comparação com o limite (RN-002). Se o total do dia ficar negativo, o valor reembolsado do dia é R$ 0,00, e o saldo negativo não é descontado de outros dias.
- **Hospedagem:** o estorno é abatido do item de hospedagem com a mesma data de entrada, antes da comparação com o teto (RN-004). Sem hospedagem com essa data de entrada, o estorno fica pendente de revisão, com R$ 0,00. Se a hospedagem correspondente não for reembolsada (pendente, recusada ou desconsiderada), o estorno fica na mesma situação, com referência a ela, e R$ 0,00.

**Origem:** AMB-015.
**Aceite:**
- corrida de R$ 100,00 e estorno de −R$ 45,00 no mesmo dia útil, sem viagem → total de R$ 55,00 → R$ 55,00 reembolsados;
- corridas de R$ 150,00 e estorno de −R$ 45,00 → total de R$ 105,00 → R$ 80,00 reembolsados;
- estorno de −R$ 45,00 sozinho em dia útil → total de −R$ 45,00 → R$ 0,00;
- d-009 (−R$ 45,00, 2026-07-11, sábado) → pendente de revisão por dia não útil (RN-007);
- hospedagem com entrada em 2026-07-14, 2 diárias, R$ 480,00, e estorno de hospedagem em 2026-07-14 de −R$ 80,00 → R$ 400,00 líquidos, abaixo do teto de R$ 500,00 → R$ 400,00 reembolsados;
- estorno de hospedagem em 2026-07-16, sem hospedagem com essa data de entrada → pendente de revisão, R$ 0,00;
- hospedagem com entrada em 2026-07-22, sem nota, R$ 690,00 (pendente de nota fiscal), e estorno de hospedagem em 2026-07-22 de −R$ 50,00 → o estorno fica pendente de nota fiscal, com referência à hospedagem, R$ 0,00.

### RN-017 — Hospedagens sobrepostas

**Regra:** as noites de uma estadia são a data de entrada e os dias seguintes, uma noite por diária (RN-004); o dia de saída não é noite. Itens de hospedagem que têm pelo menos uma noite em comum ficam todos pendentes de revisão por sobreposição de hospedagem, com R$ 0,00. Estornos de hospedagem (valor negativo) não são estadias e não entram nesta verificação.
**Origem:** AMB-018.
**Aceite:**
- A (entrada em 2026-07-20, 2 diárias) e B (entrada em 2026-07-21, 1 diária) → a noite de 21/07 é comum → os dois ficam pendentes;
- A (entrada em 2026-07-20, 2 diárias) e B (entrada em 2026-07-22, 1 diária) → não há noite em comum → seguem as demais regras;
- d-010 (noites de 14 e 15/07) e d-013 (noites de 22 a 24/07) → não há sobreposição;
- hospedagem com entrada em 2026-07-14, 2 diárias, e estorno de hospedagem em 2026-07-14 → não há sobreposição; o estorno segue a RN-016.

### RN-018 — Entrada inválida

**Regra:** a entrada é inválida quando: não é um JSON válido; falta `colaborador`, `periodo` ou `despesas`; o período não corresponde ao mês da competência (RN-014); ou algum item não tem todos os campos da §4, ou tem um campo com tipo ou formato errado (`id`, descrição ou fornecedor vazios ou que não são texto, data fora do formato AAAA-MM-DD ou que não existe, valor que não é número, nota que não é verdadeiro ou falso). Campos a mais são ignorados. Com entrada inválida, nenhuma saída é gravada; o sistema informa qual é o problema e termina indicando erro. Uma lista de despesas vazia é válida: a saída não tem itens e o total é R$ 0,00.
**Origem:** AMB-021, AMB-032.
**Aceite:**
- item com `"valor": "abc"` → entrada inválida, sem saída;
- item com `"data": "2026-02-30"` → entrada inválida;
- item sem `fornecedor` → entrada inválida;
- item com um campo a mais (`"moeda": "BRL"`) → campo ignorado, cálculo normal;
- `"despesas": []` → saída sem itens, `total_reembolsado` de 0.00.

### RN-019 — Item com mais de um motivo

**Regra:** a situação e o motivo de um item são os da primeira regra que se aplica a ele, na ordem da §8. Os motivos das demais regras que também se aplicariam aparecem em `outros_motivos`, na mesma ordem.
**Origem:** AMB-025.
**Aceite:**
- alimentação em 2026-04-18 (sábado, fora do período) → recusado, motivo `fora_do_periodo`, `outros_motivos`: [`dia_nao_util`];
- duas despesas iguais fora do período → a primeira é recusada (`fora_do_periodo`); a segunda é desconsiderada (`duplicata`), com `outros_motivos`: [`fora_do_periodo`];
- duas hospedagens idênticas → a segunda é desconsiderada (`duplicata`); a primeira é calculada normalmente, sem sobreposição.

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
**Decisão:** a nota é obrigatória para valor maior que R$ 100,00; R$ 100,00 exato não exige nota (RN-012).
**Justificativa:** "acima de" tem na spec o mesmo sentido da AMB-004: maior que o valor.
**Regra afetada:** RN-012
**Efeito de AMB-014:** a fronteira é comparada com o valor já arredondado (RN-009).
**No exemplo:** d-003 (R$ 100,00, sem nota); d-004 (R$ 100,01, sem nota).

### AMB-006 — Valor sobre o qual se mede o patamar da nota fiscal
**Ref. levantamento:** A-06
**Texto original do RH:** "Nota fiscal é obrigatória acima de R$ 100."
**O que não está claro:** se o patamar é medido sobre o valor original do item, sobre o valor depois do limite ou sobre a soma do dia.
**Decisão:** o patamar é medido sobre o valor do próprio item, já arredondado, e não sobre a soma do dia nem sobre o valor depois do limite (RN-012).
**Justificativa:** a nota fiscal é documento de cada despesa; o patamar se mede no valor da própria despesa.
**Regra afetada:** RN-012
**Depende de:** AMB-016.
**Efeito de AMB-002:** não existe valor pago por item; a leitura "valor depois do limite" só se aplica ao total do dia.
**No exemplo:** d-004 (R$ 100,01, limite de R$ 80,00); total de 2026-07-06 (R$ 200,01); d-013 (R$ 690,00, sem nota).

### AMB-007 — Consequência da falta de nota fiscal obrigatória
**Ref. levantamento:** A-07
**Texto original do RH:** "Nota fiscal é obrigatória acima de R$ 100."
**O que não está claro:** o que acontece com o item sem nota quando ela é obrigatória. Leituras: recusar o item; reembolsar até R$ 100,00; marcar como pendente.
**Decisão:** o item sem a nota obrigatória fica pendente de nota fiscal, com R$ 0,00 e fora da soma do dia (RN-012). O envio posterior da nota está fora de escopo (§3).
**Justificativa:** sem a nota obrigatória, a despesa não pode ser paga. A falta pode ser sanada com o envio da nota, por isso o item fica pendente, e não recusado.
**Regra afetada:** RN-012
**Depende de:** AMB-031.
**Efeito de AMB-002:** recusar o item ou limitá-lo a R$ 100,00 altera quanto ele contribui para o total do dia.
**No exemplo:** d-004; d-013.

### AMB-008 — O que caracteriza colaborador "em viagem"
**Ref. levantamento:** A-08
**Texto original do RH:** "Colaborador em viagem tem limites ampliados em 50%."
**O que não está claro:** a entrada não traz nenhuma informação de viagem. Leituras: deduzir de outros dados (existência de hospedagem, palavras na descrição); exigir um dado que a entrada não traz; não aplicar a regra enquanto o dado não existir.
**Decisão:** o dia de viagem é definido pela RN-013, considerando a data informada na hospedagem como data de entrada.
**Justificativa:** a entrada não traz o dado de viagem (AMB-033). Hospedagem e palavras de deslocamento são os indícios objetivos disponíveis, e a data de entrada permite saber quais dias a estadia cobre.
**Limitação:** a entrada não informa o horário nem a finalidade da despesa. Em dia útil, o sistema não distingue gasto de lazer (por exemplo, um happy hour) de gasto de trabalho, e ambos seguem as regras normais. Em dia não útil, alimentação e transporte ficam pendentes de revisão (RN-007).
**Regra afetada:** RN-013, RN-007
**Depende de:** AMB-033 (decidida).
**Efeito de AMB-033:** a leitura "exigir um dado que a entrada não traz" fica descartada.
**No exemplo:** d-003 ("Corrida aeroporto"); d-010 ("Hotel Rio"); d-011 (café no hotel); d-013.

### AMB-009 — Alcance e período da ampliação de 50%
**Ref. levantamento:** A-09
**Texto original do RH:** "Colaborador em viagem tem limites ampliados em 50%."
**O que não está claro:** (1) se, além dos limites de categoria (R$ 90, R$ 120, R$ 375), o patamar de R$ 100 da nota fiscal também é ampliado; (2) se a ampliação vale só nos dias da viagem ou em todo o período de competência em que houve viagem.
**Decisão:** a ampliação vale para alimentação (R$ 90,00) e transporte urbano (R$ 120,00), só nos dias de viagem. O teto de hospedagem e o patamar da nota fiscal não mudam (RN-013).
**Justificativa:** quem se hospeda já está em viagem, então o teto de hospedagem já é um teto de viagem. Manter a nota acima de R$ 100 evita dois patamares diferentes.
**Regra afetada:** RN-013
**Depende de:** AMB-008.
**No exemplo:** depende de AMB-008.

### AMB-010 — Período de competência
**Ref. levantamento:** A-10
**Texto original do RH:** "Despesas devem ser lançadas dentro do período de competência."
**O que não está claro:** se vale a data da despesa ou a data de lançamento (que a entrada não traz); qual informação define o período (competência ou início/fim) se discordarem; se as datas de início e fim estão dentro do período; se o item fora do período é recusado, sinalizado ou admitido com tolerância.
**Decisão:** vale a data informada da despesa. O período vai do início ao fim informados, inclusive, e deve ser exatamente o mês da competência; se não for, a entrada é inválida. Um item fora do período é recusado. Uma hospedagem cujas diárias passam do fim do período não é cortada (RN-014).
**Justificativa:** a entrada traz o período e a competência, que precisam corresponder. Manter a data informada como única referência evita cortar diárias sem saber o valor de cada uma.
**Regra afetada:** RN-014
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
**Decisão:** só o primeiro item na ordem do arquivo é calculado; os demais são desconsiderados por duplicata, com referência a ele, e não entram na soma do dia (RN-015).
**Justificativa:** um lançamento repetido não é uma nova despesa. Tratá-lo como o identificador repetido (RN-006) mantém uma única regra para o mesmo caso.
**Regra afetada:** RN-015
**Depende de:** AMB-011 e AMB-029 (decididas), AMB-031, AMB-016.
**Efeito de AMB-011 e AMB-029:** o critério de duplicata é a RN-005. Itens com o mesmo identificador e o mesmo conteúdo já são tratados pela RN-006 (o primeiro é calculado, os demais são desconsiderados); o tratamento de duplicatas com identificadores diferentes deve ser coerente com ela.
**Fora de escopo relacionado:** fluxo de revisão (§3).
**No exemplo:** d-006 e d-007.

### AMB-013 — Categorias aceitas e comparação do nome
**Ref. levantamento:** A-13
**Texto original do RH:** "Categorias fora da política não são reembolsáveis."
**O que não está claro:** se apenas as três categorias com limite estão na política ou se há outras aceitas; se variações de maiúsculas ou acentos ("ALIMENTACAO") correspondem à mesma categoria.
**Decisão:** só alimentação, transporte urbano e hospedagem estão na política. A categoria é reconhecida sem diferenciar maiúsculas, acentos e espaços a mais, com sublinhado, espaço e hífen equivalentes (RN-010).
**Justificativa:** são as únicas categorias citadas na política; diferenças de grafia não mudam a categoria.
**Regra afetada:** RN-010
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
**Decisão:** o estorno é abatido antes do limite: em alimentação e transporte, da soma do dia da categoria, e total negativo vira R$ 0,00; em hospedagem, do item com a mesma data de entrada. Sem esse item, o estorno fica pendente de revisão; se o item não for reembolsado, o estorno acompanha a situação dele (RN-016).
**Justificativa:** o estorno devolve ao colaborador parte do que ele gastou, então abatê-lo antes do limite calcula o reembolso sobre o gasto líquido. Um total negativo não gera cobrança: a empresa apenas não paga. Um estorno vinculado a uma hospedagem segue o destino dela, para ser descontado quando ela for reavaliada.
**Regra afetada:** RN-016
**Depende de:** AMB-001 (decidida: soma diária), AMB-032.
**Efeito de AMB-002:** a leitura "associar a uma despesa original" não se aplica a categorias com limite diário; "abater do total do dia" continua possível.
**Efeito de AMB-014:** o arredondamento de valores negativos segue a RN-009.
**No exemplo:** d-009 (−R$ 45,00, transporte urbano, sozinho em 2026-07-11).

### AMB-016 — Ordem de aplicação das regras
**Ref. levantamento:** A-16
**Texto original do RH:** nenhum — a política não define ordem.
**O que não está claro:** quando várias regras incidem sobre o mesmo item (competência, categoria, duplicata, nota fiscal, ampliação por viagem, limite), qual é verificada primeiro. A ordem muda o resultado: d-004 pode terminar com R$ 0,00 ou R$ 80,00 conforme a nota seja verificada antes ou depois do limite; d-006 + d-007 mudam conforme a duplicata seja desconsiderada antes ou depois da soma diária.
**Decisão:** a ordem da §8.
**Justificativa:** as cópias são retiradas primeiro, para que o original seja avaliado sozinho e duas hospedagens idênticas não se sobreponham. As recusas vêm antes das pendências: o que nunca será pago aparece como recusado, e ninguém revisa um item que não poderia ser pago de qualquer forma. Arredondamento, dias de viagem e limites seguem a dependência entre as regras.
**Regra afetada:** §8, RN-019
**Depende de:** todas as demais.
**Efeito de AMB-014:** o arredondamento é a primeira etapa (RN-009).
**Efeito de AMB-007:** a nota é verificada no item, antes da soma do dia (RN-012).
**Efeito de AMB-012, AMB-015 e AMB-018:** duplicatas e estornos são tratados antes do limite (RN-015, RN-016). Duas hospedagens idênticas também têm as mesmas noites: fica para a §8 decidir se vale a RN-015 (uma é desconsiderada) ou a RN-017 (as duas ficam pendentes).
**No exemplo:** d-004; d-006 + d-007; d-008.

### AMB-017 — Tratamento de item com categoria fora da política
**Ref. levantamento:** A-17
**Texto original do RH:** "Categorias fora da política não são reembolsáveis."
**O que não está claro:** o item não é reembolsado e a saída precisa justificar a decisão; falta definir como ele aparece. Leituras: recusar com justificativa; marcar como pendente de correção (categoria possivelmente lançada por engano); tratar como entrada inválida.
**Decisão:** o item com categoria fora da política é recusado, com justificativa e R$ 0,00 (RN-010). A correção e o reenvio estão fora de escopo (§3).
**Justificativa:** a política diz que essas categorias "não são reembolsáveis"; a recusa é a leitura direta.
**Regra afetada:** RN-010
**Depende de:** AMB-013, AMB-030, AMB-031, AMB-032.
**Fora de escopo relacionado:** fluxo de correção e reenvio (§3).
**No exemplo:** d-005; d-014, dependendo de AMB-013.

### AMB-018 — Duas hospedagens na mesma data
**Ref. levantamento:** A-18
**Texto original do RH:** "Hospedagem tem limite de R$ 250 por diária."
**O que não está claro:** o comportamento quando há duas hospedagens com a mesma data. Leituras: tratar como duplicata; considerar só o maior valor; somar os valores. A entrada não traz horário de entrada e saída, só a data.
**Decisão:** hospedagens se sobrepõem quando têm pelo menos uma noite em comum; o dia de saída não conta. Todos os itens sobrepostos ficam pendentes de revisão, com R$ 0,00 (RN-017).
**Justificativa:** duas hospedagens na mesma noite indicam erro ou gasto em dobro. Sem o valor de cada noite, não há como pagar só a parte sem conflito.
**Regra afetada:** RN-017
**Depende de:** AMB-003 e AMB-011 (decididas).
**Efeito de AMB-002:** se a decisão for "somar", RN-003 passa a valer também para hospedagem.
**Efeito de AMB-011:** duas hospedagens na mesma data só são duplicatas se tiverem o mesmo conteúdo (RN-005); com valor ou descrição diferentes, a leitura "tratar como duplicata" não se aplica.
**Efeito de AMB-003:** uma hospedagem de várias diárias cobre várias datas e pode se sobrepor a outra mesmo com datas informadas diferentes.
**Efeito de AMB-008:** a data informada da hospedagem é a data de entrada. Com isso, estadias podem se sobrepor mesmo com datas diferentes.
**No exemplo:** nenhum (d-010 e d-013 não se sobrepõem).

### AMB-019 — Dias não úteis
**Ref. levantamento:** L-01
**Texto original do RH:** nenhum.
**O que não está claro:** a política não distingue dia útil de fim de semana ou feriado. Pela letra, não há restrição; falta confirmar se esse silêncio é intencional.
**Decisão:** despesa em dia não útil (sábado, domingo ou feriado nacional, conforme RN-007) não é reembolsada e fica pendente de revisão. O fluxo de revisão e os feriados estaduais e municipais estão fora de escopo (§3).
**Justificativa:** a política não menciona dia não útil, mas a despesa nesse dia foge do padrão de trabalho e precisa ser confirmada antes do reembolso. A lista de feriados fica na spec porque a entrada não a traz (AMB-033).
**Regra afetada:** RN-007
**Efeito de AMB-008:** a hospedagem com entrada em dia não útil segue as demais regras se a estadia cobre pelo menos um dia útil (RN-007).
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
**Decisão:** as condições da RN-018. Com entrada inválida, não há saída; o sistema informa o problema e indica erro. Uma lista vazia é válida.
**Justificativa:** calcular parte de um arquivo malformado produziria um resultado em que não se pode confiar.
**Regra afetada:** RN-018
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
**Decisão:** a justificativa é um texto com o motivo, os valores comparados e o limite ou teto. O campo `regras` lista as RNs aplicadas (§4).
**Justificativa:** quem lê a saída precisa entender a decisão sem consultar a spec, e quem confere precisa da regra.
**Regra afetada:** §4 (saída)
**Efeito de AMB-002:** a justificativa do item cita o total do dia de que faz parte; o total do dia precisa de justificativa própria.
**No exemplo:** todos.

### AMB-025 — Item com mais de um motivo de recusa ou redução
**Ref. levantamento:** L-07
**Texto original do RH:** nenhum.
**O que não está claro:** quando um item incide em mais de uma regra (por exemplo, fora do período e duplicado), se a saída mostra só um motivo ou todos.
**Decisão:** a situação e o motivo são os da primeira regra que se aplica, na ordem da §8; os demais motivos aparecem em `outros_motivos` (RN-019).
**Justificativa:** mostrar todos os motivos evita que um item corrigido num ponto seja recusado de novo por outro já conhecido.
**Regra afetada:** RN-019
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
**Decisão:** totais por dia e categoria para alimentação e transporte urbano, e um resumo com o total reembolsado e a quantidade de itens por situação (§4).
**Justificativa:** o valor de alimentação e transporte só existe no total do dia (RN-003); o resumo dá o valor a pagar.
**Regra afetada:** §4 (saída)
**Efeito de AMB-002:** parcialmente decidida — a saída precisa ter o total por categoria e dia para alimentação e transporte urbano; os demais totais seguem pendentes.
**No exemplo:** todos.

### AMB-028 — Alimentação durante hospedagem
**Ref. levantamento:** L-10
**Texto original do RH:** nenhum.
**O que não está claro:** se alimentação no próprio local de hospedagem (como café da manhã) tem tratamento diferente, por exemplo por já estar incluída na diária, e se indica viagem (AMB-008).
**Decisão:** sem tratamento especial; segue a regra de alimentação.
**Justificativa:** a política não diz que a alimentação está incluída na diária.
**Regra afetada:** nenhuma (segue RN-001 e RN-013).
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
**Decisão:** o item é recusado quando a descrição contém palavra associada a outra categoria e nenhuma palavra associada à categoria informada (RN-011). Descrição sem palavra de nenhuma categoria é aceita.
**Justificativa:** a categoria define o limite aplicado; uma descrição que aponta só para outra categoria indica erro de lançamento. Exigir sempre uma palavra da categoria recusaria descrições legítimas que não usam as palavras da lista.
**Palavras não incluídas:**
- "99" (aplicativo de transporte): seria confundido com números na descrição ("2 diarias");
- estacionamento e pedágio: não está claro que sejam transporte urbano;
- coworking: não é categoria da política.

**Regra afetada:** RN-011
**Afeta:** AMB-008, AMB-013, AMB-017.
**No exemplo:** d-003; d-005.

### AMB-031 — Situações possíveis de um item na saída
**Ref. levantamento:** ponto transversal da revisão
**Texto original do RH:** nenhum.
**O que não está claro:** se a saída admite uma situação de "pendente" (usada como opção em AMB-007, AMB-010, AMB-012 e AMB-017) além de reembolsado integral, parcial e recusado.
**Decisão:** as situações são `compoe_total_do_dia`, `abatido`, `reembolsado`, `reembolsado_parcialmente`, `recusado`, `pendente` e `desconsiderado`, com os motivos da §4.
**Justificativa:** distinguir o que não será pago (recusado), o que depende de uma ação fora do sistema (pendente) e o que é cópia de outro item (desconsiderado).
**Regra afetada:** §4 (saída)
**Afeta:** AMB-007, AMB-010, AMB-012, AMB-017.
**Efeito de AMB-002:** "reembolsado parcialmente" não pode ser situação do item em categoria com limite diário; é preciso uma situação do dia ou uma situação do item como "compõe o total do dia".
**Efeito de AMB-019:** passa a existir a situação "pendente de revisão por dia não útil", com valor de R$ 0,00 (RN-007).
**Efeito de AMB-007:** passa a existir a situação "pendente de nota fiscal", com valor de R$ 0,00 (RN-012).
**Efeito de AMB-012, AMB-015 e AMB-018:** passam a existir as situações "desconsiderado por duplicata", "pendente de revisão por sobreposição de hospedagem" e "pendente de revisão: estorno sem hospedagem correspondente". Além disso, um estorno pode ter a mesma situação da hospedagem a que está vinculado.
**Efeito de AMB-029:** a saída precisa de uma situação para o item desconsiderado por identificador repetido e outra para o item recusado por identificador repetido com conteúdo diferente.

### AMB-032 — Entrada inválida versus item recusado
**Ref. levantamento:** ponto transversal da revisão
**Texto original do RH:** nenhum.
**O que não está claro:** a diferença entre dado malformado e item válido que não é reembolsado, usada em AMB-015, AMB-017 e AMB-021.
**Decisão:** um dado malformado torna a entrada inteira inválida (RN-018). Um item bem formado que não é pago fica recusado, pendente ou desconsiderado, sempre com motivo (§4).
**Justificativa:** separa o erro de quem gerou o arquivo da decisão sobre a despesa.
**Regra afetada:** RN-018
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
| Total igual ao limite | alimentação, total do dia de R$ 60,00 | R$ 60,00, situação `integral` | RN-002 |
| Um centavo acima do limite | alimentação, total do dia de R$ 60,01 | R$ 60,00, situação `parcial` | RN-002 |
| Nota no limite | R$ 100,00 sem nota | nota não exigida | RN-012 |
| Nota acima do limite | R$ 100,01 sem nota | pendente, `nota_fiscal_ausente` | RN-012 |
| Arredondamento que evita a nota | R$ 100,004 sem nota | R$ 100,00; nota não exigida | RN-009, RN-012 |
| Meio centavo | R$ 33,335 | R$ 33,34 | RN-009 |
| Valor zero | R$ 0,00 | recusado, `valor_zero` | RN-008 |
| Estorno sozinho no dia | −R$ 45,00 em dia útil | total do dia −R$ 45,00; reembolso R$ 0,00, `sem_valor` | RN-016 |
| Categoria com grafia diferente | "ALIMENTACAO", "transporte-urbano" | reconhecidas | RN-010 |
| Categoria fora da política | "coworking" | recusado, `categoria_fora_da_politica` | RN-010 |
| Descrição de outra categoria | hospedagem "Almoço com cliente" | recusado, `descricao_incompativel` | RN-011 |
| Hospedagem sem número de diárias | "Hotel 3 estrelas" | 1 diária, teto de R$ 250,00 | RN-004 |
| Hospedagem com entrada no domingo | domingo, 1 diária | cobre a segunda; segue as demais regras | RN-007, RN-013 |
| Feriado móvel | despesa na Sexta-feira Santa | pendente, `dia_nao_util` | RN-007 |
| Dia de viagem | alimentação em dia coberto por hospedagem | limite de R$ 90,00 | RN-013 |
| Último dia do período | data 2026-07-31 | dentro do período | RN-014 |
| Mesmo id, conteúdo diferente | dois `d-020` diferentes | os dois recusados | RN-006 |
| Hospedagens com noite em comum | entradas em 20/07 (2 diárias) e 21/07 (1 diária) | as duas pendentes, `sobreposicao_hospedagem` | RN-017 |
| Dois motivos | sábado e fora do período | recusado (`fora_do_periodo`), `outros_motivos`: [`dia_nao_util`] | RN-019, §8 |
| Item malformado | `"valor": "abc"` | entrada inválida, sem saída | RN-018 |
| Lista vazia | `"despesas": []` | saída sem itens, total R$ 0,00 | RN-018 |

## 8. Ordem de aplicação das regras

1. **Validação da entrada** (RN-018). Se a entrada for inválida, nada é calculado.
2. **Arredondamento** dos valores (RN-009).
3. **Cópias:** identificador repetido (RN-006) e duplicata (RN-015), com os valores já arredondados.
4. **Recusas**, nesta ordem: categoria (RN-010), descrição (RN-011), período (RN-014) e valor zero (RN-008).
5. **Pendências**, nesta ordem: dia não útil (RN-007), nota fiscal (RN-012) e sobreposição de hospedagens (RN-017).
6. **Estornos de hospedagem** (RN-016), conforme a situação da hospedagem correspondente.
7. **Dias de viagem** (RN-013), com todos os itens da entrada.
8. **Somas do dia, estornos e limites** (RN-001 a RN-004, RN-016).

A situação e o motivo de cada item vêm da primeira regra das etapas 3 a 5 que se aplica a ele. As demais regras dessas etapas que também se aplicariam vão para `outros_motivos`, na mesma ordem (RN-019). Itens desconsiderados ou recusados nas etapas 3 e 4 não entram na verificação de sobreposição nem nas somas.

## 9. Critérios de aceite

O sistema está pronto quando:

- [ ] `<comando> calcular --input exemplos/despesas-exemplo.json --output <saida.json>` grava uma saída igual à do exemplo da §4 em todos os campos, exceto o texto das justificativas.
- [ ] Cada caso de aceite das RN-001 a RN-019 produz o resultado descrito na regra.
- [ ] Cada caso da §7 produz o comportamento descrito.
- [ ] A saída tem um item por despesa da entrada, na mesma ordem, cada um com situação e justificativa.
- [ ] Nenhum valor reembolsado ultrapassa o limite ou o teto aplicável.
- [ ] `total_reembolsado` é igual à soma dos totais diários e das hospedagens calculadas.
- [ ] Com entrada inválida, nenhuma saída é gravada, o problema é informado e o comando termina indicando erro.
- [ ] A mesma entrada produz sempre a mesma saída.

## 10. O que fica em aberto

- Nenhuma ambiguidade da §6 está pendente.