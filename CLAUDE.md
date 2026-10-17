# CLAUDE.md

Convenções de trabalho do agente neste projeto. Instruções permanentes valem do
início ao fim; itens marcados **PENDENTE** só são preenchidos na etapa indicada,
com aprovação do usuário.

## O projeto

Motor de cálculo de reembolso de despesas corporativas. CLI que lê um JSON de
despesas e emite um JSON com o valor reembolsável e a justificativa de cada item.

- Interface fixa: `<comando> calcular --input <entrada.json> --output <saida.json>`.
- Formato de entrada fixo: `exemplos/despesas-exemplo.json`.
- O schema de saída é definido na `spec.md`.
- Desafio de Spec Driven Development avaliado por `RUBRICA.md`: o processo é o
  que se avalia, não só o produto.

## Fonte da verdade

| Arquivo (`specs/001-motor-reembolso/`) | Responde | Não pode conter |
|---|---|---|
| `spec.md` | o quê e o porquê | linguagem, biblioteca, classe, função, estrutura de pasta |
| `plan.md` | o como | regra de negócio nova |
| `tasks.md` | em que ordem | — |
| `DECISIONS.md` | o que mudou na spec, por quê e o que quebrou | — |

- Quando código e spec discordarem, a spec está certa e o código é o bug.
- Se a spec parecer errada: aponte o problema e pare. Quem decide é o usuário.
  Se aprovado, corrige-se a spec, registra-se em `DECISIONS.md`, e só então o código.
- Dúvida entre spec e plan: "se eu trocasse de linguagem amanhã, isso mudaria?"
  Se sim, é `plan.md`.
- Regra de negócio vive só na `spec.md`. Não a reproduza neste arquivo, em
  comentário de código, em mensagem de commit nem na memória do agente.

## Quem decide

- **Decisões de negócio pertencem ao usuário.** O agente pode identificar
  ambiguidades, apresentar as interpretações possíveis e explicar as
  consequências de cada uma. Não escolhe uma interpretação, não a escreve na
  spec como decidida e não a resolve no código sem aprovação explícita.
- Decisões técnicas do `plan.md`: o agente pode propor alternativas; o plan só
  vale depois de aprovado pelo usuário.
- Commits: o agente prepara as alterações e sugere a mensagem. Só executa o
  commit após autorização explícita do usuário, dada para aquele commit.

## Ambiguidades da política

- Toda ambiguidade vai para a seção de ambiguidades da `spec.md` (texto
  original, leituras possíveis, decisão, justificativa, regra afetada).
  Ambiguidade resolvida no código sem registro conta como não resolvida.
- As perguntas de exemplo do `DESAFIO.md` não são a lista completa. A lista de
  referência da correção não é publicada; não afirme conhecê-la.
- Todo caso presente em `exemplos/despesas-exemplo.json` precisa estar coberto
  pela spec, nem que seja como fora de escopo.
- Se o usuário explicar no chat uma regra, decisão ou restrição que não está na
  spec: pare e avise. É bug de spec. Corrija spec e `DECISIONS.md` antes de
  continuar.

## Ordem de trabalho

- Base: `spec.md` → `plan.md` → `tasks.md` → código e testes.
- Mudança de requisito (incluindo o Dia 2): `spec.md` → `DECISIONS.md` →
  `tasks.md` → código.
- Especificação e planejamento (`spec.md`, `plan.md`, `tasks.md`,
  `DECISIONS.md`) não dependem de task existente.
- Código de produção e testes, sim: antes de implementar, leia a task
  correspondente em `tasks.md`. Se o pedido não está coberto por nenhuma task,
  avise em vez de implementar.
- Nenhuma regra de negócio entra sem teste.
- Não generalize a arquitetura tentando prever mudanças de requisito futuras.

## Rastreabilidade

- Identificadores: `RN-NNN` e `AMB-NNN` (spec), `DT-NNN` (plan), `T-NNN`
  (tasks), `D-NNN` (DECISIONS).
- Toda task declara o que atende (`RN`/`AMB`) e o critério de aceite
  (normalmente "o teste X passa"). Uma task deve caber em um commit.
- Código pode referenciar identificadores (ex.: `RN-001`) em comentários ou
  referências pertinentes, sem duplicar o texto da regra.
- O nome de cada teste remete ao requisito que ele verifica.
  Padrão de nomenclatura: **PENDENTE** (`plan.md`, estratégia de testes).
- Task concluída é marcada `[x]` em `tasks.md` ao concluir, não em lote no fim.
  O hash do commit é preenchido depois.
- A tabela de cobertura de `tasks.md` é atualizada ao fechar cada fase.
- Tasks novas continuam a numeração existente. Nunca renumere.

## Commits

- Implementação: `feat(T-NNN): <descrição>` e `test(T-NNN): <descrição>`.
- Documentos de especificação: `docs(spec):`, `docs(plan):`, `docs(tasks):`.
- Granularidade compatível com as tasks: nem commits em bloco, nem micro-commits.
- Inclua no commit só os arquivos da alteração em questão. Alterações no working
  tree que não fazem parte da tarefa atual não entram no commit e não são
  descartadas sem autorização.
- Nunca reescreva o histórico (amend, rebase, force push). Erro de convenção é
  registrado no relatório e corrigido dali em diante.
- Prefixo para `DECISIONS.md`, `docs/sessions/`, `README.md`,
  `docs/RELATORIO.md`, `CLAUDE.md` e arquivos de configuração: **PENDENTE**.
- Prefixo para correção de bug em task já concluída: **PENDENTE**.

## Registro de mudanças

- Toda mudança na `spec.md` gera uma entrada `D-NNN` em `DECISIONS.md`, no
  formato do arquivo (gatilho, o que mudou, por quê, o que invalidou, tasks
  afetadas, custo), em ordem cronológica inversa.
- A partir de quando uma alteração da spec passa a exigir entrada: **PENDENTE**.

## Evidências e sessões

- Ao fim de cada sessão de trabalho, lembre o usuário de rodar `/export` e
  salvar em `docs/sessions/NN-descricao-curta.md`. O agente não executa `/export`.
- Em `DECISIONS.md` e `docs/RELATORIO.md`, só evidência real: arquivo, linha,
  hash de commit, trecho de sessão. Não invente evidência e não omita nem
  suavize erros do agente.
- O `README.md` da raiz será substituído pelo README do projeto, que precisa
  permitir rodar e testar sem intervenção.

## Stack e comandos

> **PENDENTE** — preencher a partir de `plan.md` depois que ele for aprovado.

- Linguagem: PENDENTE
- Rodar: PENDENTE
- Testes: PENDENTE
- Lint/format: PENDENTE

## Convenções de código

> **PENDENTE** — preencher a partir de `plan.md` depois que ele for aprovado.

- Representação interna de valores monetários: PENDENTE.
  (Regras de arredondamento e de comparação de valores são de negócio: ficam na spec.)
- Nomenclatura, estrutura de pastas, tratamento de erro: PENDENTE.

## Fora de escopo

- De negócio: definido na `spec.md`. Não duplicar aqui.
- Do repositório: não alterar `template/`.
