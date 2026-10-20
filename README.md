# Motor de Cálculo de Reembolso

Linha de comando que lê um arquivo JSON com as despesas de um colaborador em um mês de competência e grava um JSON com o valor reembolsável e a justificativa de cada decisão, conforme a política de reembolso do RH.

O que o sistema faz, e por quê, está em [`specs/001-motor-reembolso/spec.md`](specs/001-motor-reembolso/spec.md). Este projeto foi feito com Spec Driven Development: a spec é a fonte da verdade, e o código e os testes seguem dela.

## Requisitos

- Python 3.10 ou superior (testado em 3.14).
- pytest, só para rodar os testes.

## Como rodar

Na raiz do repositório:

```bash
python reembolso.py calcular --input exemplos/despesas-exemplo.json --output saida.json
```

- Entrada: no formato de [`exemplos/despesas-exemplo.json`](exemplos/despesas-exemplo.json) (spec §4).
- Saída: o JSON descrito na spec §4. Para o exemplo acima, o resultado esperado está na própria spec (§4, "Exemplo"); o total reembolsado é R$ 788,23.
- Entrada inválida (spec RN-018): nenhum arquivo é gravado, a mensagem com o problema vai para a saída de erro e o comando termina com código 1.

## Como testar

```bash
pip install -r requirements.txt
python -m pytest
```

Cada regra de negócio (`RN-NNN`) tem seu arquivo de teste em `tests/`, com o nome `test_rnNNN_<assunto>.py`; cada função de teste começa com o identificador da regra. O teste `tests/test_ponta_a_ponta.py` roda o comando sobre o exemplo e compara a saída com a da spec.

## Estrutura

```
reembolso.py                  # comando calcular: lê e grava os arquivos
motor/                        # cálculo, sem leitura nem escrita de arquivos
  leitura.py                  #   validação da entrada e arredondamento (etapas 1 e 2 da spec §8)
  regras_item.py              #   cópias, recusas, pendências e estornos de hospedagem (etapas 3 a 6)
  viagem.py                   #   dias de viagem (etapa 7)
  agregacao.py                #   somas do dia, limites e teto de hospedagem (etapa 8)
  saida.py                    #   montagem da saída, justificativas e escrita do JSON
  politica.py                 #   valores da política (limites, categorias, palavras, feriados)
tests/                        # um arquivo por regra, mais o teste ponta a ponta
specs/001-motor-reembolso/
  spec.md                     # o quê e o porquê: regras, ambiguidades e decisões
  plan.md                     # o como: stack, arquitetura e decisões técnicas
  tasks.md                    # as tasks, com commit e teste de cada uma
  DECISIONS.md                # registro das mudanças da spec
docs/sessions/                # exports das sessões de trabalho com o Claude Code
```

## Sobre o desafio

O enunciado original está em [`DESAFIO.md`](DESAFIO.md), a forma de avaliação em [`RUBRICA.md`](RUBRICA.md) e as dúvidas de processo em [`FAQ.md`](FAQ.md).
