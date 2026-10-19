"""Comando de linha do motor de reembolso (DT-004).

Uso: python reembolso.py calcular --input <entrada.json> --output <saida.json>
"""

import argparse
import sys


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


def main(argv=None):
    criar_parser().parse_args(argv)
    print("calcular: ainda não implementado", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
