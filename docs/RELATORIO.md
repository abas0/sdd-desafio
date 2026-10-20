# Relatório — Desafio SDD

**Aluno:** Ana Beatriz Araújo de Sousa · **Repositório:** https://github.com/abas0/sdd-desafio · **Data:** 2026-10-19

> Isto não é redação. São **evidências**. Toda afirmação deve vir acompanhada de
> arquivo, hash de commit ou trecho de sessão exportada. Um parágrafo bonito sem
> evidência vale menos que uma frase curta com um hash.
>
> Vale 20 dos 100 pontos, e é a seção que mais separa notas.

---

## Delegação

*O que você fez, o que o Claude fez, e por que dividiu assim.*

**A divisão:**

| Atividade | Quem | Por quê |
|---|---|---|
| Identificar ambiguidades | Claude levantou a lista inicial; eu revisei e acrescentei pontos (A-17 a A-19, L-11 e L-12, que viraram AMB-017, AMB-018, AMB-029, AMB-030 e outras) | o levantamento exaustivo é trabalho mecânico; o que eu conhecia de rotina de reembolso (reenvio de nota, Airbnb, categoria lançada errada) o modelo não tinha. Evidência: `docs/sessions/01-analise-estrutura-claude-md-ambiguidades.md` |
| Decidir as ambiguidades | eu, todas as 33 | decisão de negócio é minha; o `CLAUDE.md` proíbe o agente de escolher (seção "Quem decide"). O Claude apresentava opções, consequências e os itens do exemplo afetados |
| Escrever a spec | Claude redigiu; eu aprovei cada texto antes de gravar ("pode gravar") | a redação é rápida para o modelo; a revisão de cada trecho era o meu controle. 15 commits `docs(spec)` e 14 entradas em `DECISIONS.md` |
| Desenhar a arquitetura | Claude propôs as opções (DT-001 a DT-010); eu escolhi | só o Python estava instalado; escolhi centavos inteiros (DT-003) e aceitei as recomendações em DT-006 a DT-008. Evidência: `specs/001-motor-reembolso/plan.md`, commit `be50c4f` |
| Implementar | Claude, uma task por commit, com autorização por fase | 21 tasks, commits `f4cb359` a `e910888` |
| Escrever testes | Claude | 199 testes, um arquivo por regra (DT-009) |
| Absorver o envelope | não feito | o envelope chegou, mas não houve tempo de absorvê-lo antes do prazo (ver "O envelope") |

**Onde deleguei e me arrependi:** no ritmo do trabalho. Começamos decidindo uma ambiguidade por vez, com várias rodadas de perguntas para cada uma; isso consumiu a maior parte do tempo. Quando passamos a decidir em lotes (`docs/sessions/05-lote-1-e-plan-rascunho.md`, linha 8166: "Podemo fazer em lote e podemos já ir decidindo as questões do plan.md"), o avanço foi muito maior: os lotes 1 a 7 e o plan foram decididos no mesmo dia, 18/10 (commits `88cd026` a `be50c4f`). Provavelmente teríamos chegado ao envelope se tivéssemos trabalhado assim desde o início.

**Onde não deleguei e deveria ter delegado:** eu deveria ter discutido o ritmo das atividades antes de aceitar a forma de condução proposta, em vez de seguir o padrão uma-a-uma até perceber o atraso.

**Usei subagentes / skills / MCP / hooks?** Não. Trabalhei em uma única sessão do Claude Code, com o `CLAUDE.md` como guia de convenções. Uma vez o modo automático do Claude Code bloqueou um comando que mexia diretamente na área de preparação do git (para separar os lotes 2 e 3 em commits diferentes); o mesmo resultado foi obtido com comandos comuns. Isso está registrado na sessão exportada do dia 2.

---

## Descrição

*Como você transformou requisito ambíguo em requisito verificável.*

Requisito: **"Hospedagem tem limite de R$ 250 por diária."** (política do RH, item 3)

**Versão 1 (minha primeira escrita):** AMB-003 no commit `39baa6e`

> ```
> ### AMB-003 — Hospedagem com várias noites em um único item
> **O que não está claro:** se o limite é R$ 250 por item ou R$ 250 multiplicado pelo
> número de noites. A entrada não informa o número de noites; ele aparece só no texto
> livre da descrição.
> **Decisão:** PENDENTE
> ```

**Versão final:** RN-004 e AMB-003 (`specs/001-motor-reembolso/spec.md`)

> ```
> ### RN-004 — Teto de hospedagem por diária
> **Regra:** o teto de reembolso de um item de hospedagem é R$ 250,00 multiplicado pelo
> número de diárias, determinado conforme AMB-003. O teto é aplicado conforme RN-002.
> **Aceite:**
> - "Hotel Rio - 2 diarias", R$ 480,00 → 2 diárias, teto R$ 500,00, R$ 480,00 dentro do teto;
> - "Airbnb 3 noites", R$ 690,00 → 3 diárias, teto R$ 750,00, R$ 690,00 dentro do teto;
> - "Hotel - 2 diárias e 1 noite", R$ 700,00 → 3 diárias, teto R$ 750,00;
> - "Hotel - 2 diárias + meia diária", R$ 600,00 → "meia" ignorada, 2 diárias, R$ 500,00;
> - "Hotel 3 estrelas", R$ 300,00 → nenhum número antes de "diária" ou "noite" → 1 diária;
> - "Hotel - 0 diárias", R$ 300,00 → número inválido → 1 diária, R$ 250,00.
>
> AMB-003 — Decisão: conta o número escrito imediatamente antes de "diária" ou "noite",
> em qualquer forma; em algarismos ou por extenso; só inteiros ≥ 1; ocorrências válidas
> são somadas; sem número válido, uma diária.
> ```

**O que estava ambíguo:** a unidade do limite (por item ou por diária) e, decidida a unidade, de onde tirar o número de diárias, já que a entrada não tem esse campo e o formato de entrada é fixo (AMB-033).

**Como percebi:** olhando o JSON de exemplo. d-013 ("Airbnb 3 noites", R$ 690,00) é uma hospedagem de várias noites paga de uma vez; com "R$ 250 por item" ela seria cortada para R$ 250,00, o que não faz sentido para uma estadia de três noites. Decidir "por diária" levou à segunda pergunta: como contar as diárias num texto livre. Os aceites com "duas", "meia", "0" e "2 diárias e 1 noite" vieram dessa discussão.

**Commit da mudança:** `3e802b2` (decisão da AMB-003 e criação da RN-004). A implementação está em `4cf93b0` (T-005, número de diárias) e `9ca5c0f` (T-018, teto).

---

## Discernimento

*Onde o Claude errou e você pegou.*

### Caso 1

**O que ele propôs:** na AMB-002 ("como dividir o limite diário entre as despesas do mesmo dia"), o Claude apresentou só quatro formas de **dividir** os R$ 60,00 do dia entre d-001 e d-002: na ordem da entrada, maior primeiro, menor primeiro, proporcional.

**Por que estava errado:** a pergunta partia de uma premissa que o próprio Claude tinha escrito no `CLAUDE.md` ("o valor reembolsável e a justificativa de cada item"). A política fixa o limite **por dia**; repartir o valor do dia entre os itens exigiria um critério que a política não fornece. As quatro opções inventavam esse critério.

**Como eu detectei:** ao ler as opções, respondi que o que fazia sentido era apurar o valor no somatório diário da categoria. Só então o Claude apresentou a opção B (valor reembolsado só no total do dia, sem divisão entre itens), que eu escolhi. A descrição da saída no `CLAUDE.md` foi corrigida.

**O que eu fiz:** escolhi a opção B, que virou a RN-003 (valor apurado por dia) e eliminou a necessidade de um critério de divisão. Pedi também a lista das ambiguidades afetadas por essa escolha antes de decidir.

**Onde está a evidência:** `docs/sessions/03-decisoes-amb-002-003-004-033.md`, linhas 5221 a 5290 (as quatro opções de divisão, a minha resposta na linha 5236 e a opção B apresentada em seguida); commit `0175952` (AMB-002 e RN-003; ajuste do `CLAUDE.md`).

### Caso 2

**O que ele propôs:** no lote 4, respondi "marca se for dia útil" à pergunta sobre se itens não reembolsados marcam o dia como de viagem. O Claude interpretou que a restrição "dia útil" não mudava nenhum valor e propôs escrever a regra sem ela.

**Por que estava errado:** não era isso que eu queria dizer. Eu queria garantir que alimentação e transporte em dia não útil não fossem reembolsados mesmo durante uma viagem (por exemplo, um happy hour no fim de semana).

**Como eu detectei:** li a proposta e respondi explicando o que eu quis dizer. A discussão levou ao registro explícito da limitação "lazer × trabalho" na AMB-008.

**Onde está a evidência:** `docs/sessions/07-lotes-4-a-7-spec-completa-e-plan-aprovado.md`, linhas 11387 (minha resposta) e 11448 (a correção); commit `a8ffd1f`.

**Padrão que eu notei:** o Claude tende a se ancorar no que já está escrito, inclusive no que ele mesmo escreveu (Caso 1), e a "simplificar" uma resposta minha para a leitura que dá menos trabalho (Caso 2). Outros erros do agente registrados nas sessões:
- **Dados pessoais nos exports.** O Claude escreveu o nome do meu usuário do Windows no chat e, depois, um trecho do meu e-mail dentro de um comando de busca; os dois foram parar nos exports. Corrigi os arquivos antes dos commits (exports 03, 05 e 07).
- **Contradição na própria spec.** O texto da RN-017 (hospedagens sobrepostas), redigido pelo Claude e aprovado por mim, contradizia o aceite da RN-016 (estorno de hospedagem). O próprio Claude encontrou o problema ao implementar a T-014, parou e pediu decisão. Corrigido pela D-012 (`75812e3`) antes do código (`c66a602`).

---

## Diligência

*O que você verificou antes de aceitar.*

**Meu procedimento de verificação:** para a spec, nenhum texto era gravado sem que eu visse a redação exata e dissesse "pode gravar"; quando a mudança era grande, pedi o texto completo para reavaliar (lote 4: `docs/sessions/07-lotes-4-a-7-spec-completa-e-plan-aprovado.md`, linha 11685, "traga o lote 4 completo e atualizado para eu reavilar"). Cada decisão tem justificativa e entrada em `DECISIONS.md`. Os commits só eram feitos com a minha autorização (por commit na fase de spec; por fase na implementação). Ao final, rodei eu mesma `python -m pytest` (199 passando) e o comando `calcular` sobre o exemplo, conferindo o total de R$ 788,23 no arquivo gerado.

**Li o diff inteiro em que porcentagem das entregas?** A spec, o plan e o `DECISIONS.md` foram revisados a cada sessão, trecho por trecho. O código eu li rapidamente; não revisei linha por linha os diffs de implementação.

**O que aceitei sem verificar direito, e o que me custou:** o código de implementação, como dito acima. A proteção foi indireta: o teste ponta a ponta compara a saída do programa com o JSON de exemplo que eu aprovei na spec antes de existir código. Também aceitei uma exceção à regra do `CLAUDE.md` "nunca reescreva o histórico": pedi um amend do primeiro commit de spec, antes de qualquer push, para incluir alterações que eu tinha feito à mão (`39baa6e`).

**Testes: quem escreveu, e como você sabe que eles testam a coisa certa?** Todos os testes foram escritos pelo Claude, o mesmo agente que escreveu o código. O que reduz o risco de "teste que passa fácil":
- os casos de teste são os aceites da spec (cada RN tem casos de aceite numéricos, aprovados por mim antes do código) e os casos de borda da §7;
- a saída completa do exemplo foi escrita na §4 da spec e aprovada no commit `21c0d17`, antes do primeiro commit de código (`f4cb359`); `tests/test_ponta_a_ponta.py` compara a saída gerada com esse JSON;
- o nome de cada teste começa pelo identificador da regra (DT-005), e a tabela de cobertura do `tasks.md` liga regra → task → teste.

---

## O envelope

*A mudança de requisito do Dia 2.*

O envelope chegou, mas **não foi absorvido**. Com o prazo para o dia seguinte e pouco tempo disponível, decidi entregar o sistema base completo (spec fechada, 21 tasks, 199 testes, saída do exemplo idêntica à da spec) em vez de começar uma mudança que eu não conseguiria terminar.

**Quantos arquivos toquei na mão:** 0 (não absorvido).
**Quanto tempo levou:** não se aplica.
**Diff de absorção:** não se aplica.

**Absorveu de graça:** não avaliado.

**Resistiu:** não avaliado.

**Ordem em que fiz:** não se aplica. O fluxo previsto para a mudança está no `CLAUDE.md` ("Mudança de requisito: spec.md → DECISIONS.md → tasks.md → código") e foi usado duas vezes durante a implementação, quando a spec precisou mudar (D-012 e D-013: `75812e3` antes de `c66a602`; `b13ff53` antes de `d6761a3`).

**Se eu tivesse escrito a spec original sabendo desta mudança:** não avaliado.

**O que a spec me poupou, em concreto:** não se aplica ao envelope. Durante a implementação, a spec poupou retrabalho: a saída do exemplo já estava definida campo a campo na §4, e o código foi escrito para reproduzi-la.

---

## Fechamento

**Para qual tamanho de projeto isto valeu a pena?** Para um projeto como este: regras de negócio cheias de lacunas, em que uma decisão afeta várias outras (a AMB-002 mudou o formato da saída e mais oito ambiguidades). Escrever antes de codar fez as contradições aparecerem no papel, e a implementação das 21 tasks levou poucas horas.

**Para qual não valeria?** Para algo pequeno e de regra óbvia, ou um protótipo descartável: o custo de 33 ambiguidades documentadas e 14 entradas de decisão não se paga.

**O que eu faria diferente:** combinar o ritmo de trabalho logo no início (decidir em lotes desde a primeira sessão) e reservar tempo para o dia 2 antes de aprofundar casos de borda.

**A coisa mais desconfortável que aprendi sobre como eu trabalho com IA:** o modelo apresenta opções com tanta segurança que é fácil escolher uma delas sem perceber que a pergunta já estava enquadrada errado (Caso 1). E, sem uma regra de ritmo, eu segui o ritmo que a conversa impôs.
