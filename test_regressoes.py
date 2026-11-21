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

    def test_reject_noncanonical_dates_and_impossible_calendar_days(self):
        for bad in ("20261115", "2026-1-15", "2026-11-5", "2026-02-29", "2026/11/15", "  "):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                run({"data": bad, "ocorrencias": []})

    def test_reject_noncanonical_dates_inside_occurrences(self):
        record = {"inicio": "2026-11-15", "fim": "2026-11-16",
                  "gravidade": 1, "local": "Natal", "tipo": "obra"}
        for field in ("inicio", "fim"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                run({"data": "2026-11-15",
                     "ocorrencias": [{**record, field: "20261115"}]})

if __name__ == "__main__": unittest.main()
