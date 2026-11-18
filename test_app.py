from tempfile import TemporaryDirectory
import json
from pathlib import Path
import subprocess
import sys
import tempfile
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

    def test_cli_aceita_json_com_bom(self):
        exemplo = (ROOT / "exemplo.json").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as diretorio:
            arquivo = Path(diretorio) / "exemplo-bom.json"
            arquivo.write_text(exemplo, encoding="utf-8-sig")
            result = subprocess.run(
                [sys.executable, str(ROOT / "app.py"), str(arquivo)],
                capture_output=True, text=True, encoding="utf-8", check=True,
            )
        self.assertEqual(json.loads(result.stdout), run(json.loads(exemplo)))

    def test_cli_rejeita_chave_json_repetida(self):
        exemplo = (ROOT / "exemplo.json").read_text(encoding="utf-8").lstrip()
        chave = next(iter(json.loads(exemplo)))
        conteudo = "{" + json.dumps(chave) + ": null," + exemplo[1:]
        with tempfile.TemporaryDirectory() as diretorio:
            arquivo = Path(diretorio) / "exemplo-repetido.json"
            arquivo.write_text(conteudo, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "app.py"), str(arquivo)],
                capture_output=True, text=True, encoding="utf-8",
            )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("Campo JSON repetido", result.stderr)


class JsonEstritoCliTest(unittest.TestCase):
    def test_cli_rejeita_constantes_numericas_nao_padronizadas(self):
        exemplo = json.loads((ROOT / "exemplo.json").read_text(encoding="utf-8"))
        with TemporaryDirectory() as pasta:
            entrada = Path(pasta) / "entrada.json"
            for constante in ("NaN", "Infinity", "-Infinity"):
                with self.subTest(constante=constante):
                    exemplo["metadados"] = {"observacao": "CONSTANTE_TESTE"}
                    entrada.write_text(
                        json.dumps(exemplo).replace('"CONSTANTE_TESTE"', constante),
                        encoding="utf-8",
                    )
                    resultado = subprocess.run(
                        [sys.executable, str(ROOT / "app.py"), str(entrada)],
                        capture_output=True, text=True, encoding="utf-8",
                    )
                    self.assertEqual(resultado.returncode, 2)
                    self.assertIn(constante, resultado.stderr)
                    self.assertEqual(resultado.stdout, "")
