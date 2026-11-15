import unittest
from app import run

class OccurrenceTests(unittest.TestCase):
    def test_inclusive_dates_and_priority(self):
        data={"data":"2026-11-15","ocorrencias":[{"inicio":"2026-11-15","fim":"2026-11-16","gravidade":1,"local":"Natal","tipo":"obra"},{"inicio":"2026-11-14","fim":"2026-11-15","gravidade":3,"local":"Parnamirim","tipo":"bloqueio"},{"inicio":"2026-11-16","fim":"2026-11-17","gravidade":2,"local":"Macaíba","tipo":"alagamento"}]}
        result=run(data)
        self.assertEqual(result["ativas"],2)
        self.assertEqual([x["local"] for x in result["ocorrencias"]],["Parnamirim","Natal"])

    def test_invalid_severity_rejected(self):
        with self.assertRaises(ValueError):
            run({"data":"2026-11-15","ocorrencias":[{"inicio":"2026-11-15","fim":"2026-11-15","gravidade":4,"local":"Natal","tipo":"obra"}]})

    def test_inverted_dates_rejected(self):
        with self.assertRaises(ValueError):
            run({"data":"2026-11-15","ocorrencias":[{"inicio":"2026-11-16","fim":"2026-11-15","gravidade":1,"local":"Natal","tipo":"obra"}]})

if __name__ == "__main__": unittest.main()
