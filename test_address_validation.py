"""Verifica a sanitização de endereços antes de produzir links de busca."""
import unittest
from app import busca, run


class AddressValidationTests(unittest.TestCase):
    def test_rejeita_enderecos_com_controles_ou_grandes_demais(self):
        for value in ("Natal\nRN", "Rua\x00B", "A" * 301):
            with self.subTest(value=value[:20]), self.assertRaises(ValueError):
                busca(value)

    def test_preserva_unicode_e_espacos_normais(self):
        self.assertIn("S%C3%A3o+Gon%C3%A7alo", busca("  São Gonçalo  "))

    def test_rejeita_local_invalido_em_ocorrencia_ativa(self):
        occurrence = {"inicio":"2026-11-22", "fim":"2026-11-23",
                      "gravidade":2, "local":"Rua\nA", "tipo":"alagamento"}
        with self.assertRaisesRegex(ValueError, "controle"):
            run({"data":"2026-11-22", "ocorrencias":[occurrence]})


if __name__ == "__main__":
    unittest.main()
