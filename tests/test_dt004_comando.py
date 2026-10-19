import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def test_dt004_help_lista_comando_calcular():
    resultado = subprocess.run(
        [sys.executable, "reembolso.py", "--help"],
        cwd=RAIZ,
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 0
    assert "calcular" in resultado.stdout
