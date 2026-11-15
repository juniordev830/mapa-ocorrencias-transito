import json
from pathlib import Path
import subprocess
import sys
import unittest

from app import run

ROOT = Path(__file__).resolve().parent


class ProjetoTest(unittest.TestCase):
    def test_exemplo_documentado(self):
        data = json.loads((ROOT / "exemplo.json").read_text(encoding="utf-8"))
        result = run(data)
        self.assertEqual(result['ativas'], 1)

    def test_filtra_ocorrencias_com_gravidade_minima(self):
        base = {"inicio": "2026-11-15", "fim": "2026-11-16", "tipo": "obra"}
        data = {"data": "2026-11-15", "gravidade_minima": 2, "ocorrencias": [
            dict(base, local="A", gravidade=1),
            dict(base, local="B", gravidade=2),
            dict(base, local="C", gravidade=3),
        ]}
        self.assertEqual([row["local"] for row in run(data)["ocorrencias"]], ["C", "B"])
        self.assertEqual(run(dict(data, gravidade_minima=1))["ativas"], 3)

    def test_rejeita_campos_de_filtro_e_listas_invalidas(self):
        with self.assertRaises(ValueError):
            run({"data": "2026-11-15", "ocorrencias": {}})
        for invalid in (0, 4, True):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                run({"data": "2026-11-15", "ocorrencias": [], "gravidade_minima": invalid})

    def test_cli_com_exemplo(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "app.py"), str(ROOT / "exemplo.json")],
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        self.assertEqual(json.loads(result.stdout)['ativas'], 1)

    def test_rejeita_dados_incompletos(self):
        with self.assertRaises((KeyError, ValueError, TypeError)):
            run({})

    def test_data_inclusiva_e_ordem_gravidade(self):
        item = dict(local="Natal", tipo="Obra", inicio="2026-11-14", fim="2026-11-14", gravidade=1)
        result = run(dict(data="2026-11-14", ocorrencias=[item, dict(item, gravidade=3)]))
        self.assertEqual(result["ativas"], 2)
        self.assertEqual([o["gravidade"] for o in result["ocorrencias"]], [3, 1])

    def test_rejeita_periodo_invertido(self):
        with self.assertRaises(ValueError):
            run(dict(data="2026-11-14", ocorrencias=[dict(local="Natal", tipo="Obra", inicio="2026-11-15", fim="2026-11-14", gravidade=1)]))
