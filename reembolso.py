"""Comando de linha do motor de reembolso (DT-004).

Uso: python reembolso.py calcular --input <entrada.json> --output <saida.json>
"""

import argparse
import sys
from pathlib import Path

from motor.leitura import ler_entrada
from motor.modelo import EntradaInvalida
from motor.saida import escrever_json, montar_resultado


def criar_parser():
    parser = argparse.ArgumentParser(
        prog="reembolso.py",
        description="Motor de cálculo de reembolso de despesas corporativas.",
    )
    comandos = parser.add_subparsers(dest="comando", required=True)
    calcular = comandos.add_parser(
        "calcular", help="calcula o reembolso de um arquivo de despesas"
    )
    calcular.add_argument("--input", required=True, help="arquivo JSON de entrada")
    calcular.add_argument("--output", required=True, help="arquivo JSON de saída")
    return parser


def calcular(entrada, saida):
    """Lê a entrada, calcula e grava a saída. Com entrada inválida, nada é gravado (RN-018)."""
    try:
        texto = Path(entrada).read_text(encoding="utf-8")
    except OSError as erro:
        raise EntradaInvalida(f"não foi possível ler '{entrada}': {erro.strerror}") from erro
    except UnicodeDecodeError as erro:
        raise EntradaInvalida(f"'{entrada}' não está em UTF-8") from erro
    resultado = montar_resultado(ler_entrada(texto))
    Path(saida).write_text(escrever_json(resultado) + "\n", encoding="utf-8")


def main(argv=None):
    # Mensagens em UTF-8 também quando a saída de erro não é um terminal (ex.: Windows).
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    args = criar_parser().parse_args(argv)
    try:
        calcular(args.input, args.output)
    except EntradaInvalida as erro:
        print(f"Entrada inválida: {erro}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
