import unittest
from app import run
class FiltroTipo(unittest.TestCase):
    def test_acentos_e_caixa(self):
        data={"data":"2026-05-10","tipos":["INTERDICAO"],"ocorrencias":[{"local":"A","tipo":"Interdição","gravidade":3,"inicio":"2026-05-01","fim":"2026-05-20"},{"local":"B","tipo":"Obra","gravidade":2,"inicio":"2026-05-01","fim":"2026-05-20"}]}
        self.assertEqual(run(data)["ativas"],1)
        self.assertEqual(run(data)["ocorrencias"][0]["local"],"A")
        data["tipos"]=[]
        with self.assertRaises(ValueError): run(data)
