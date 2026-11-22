import unittest
from app import run


class InactiveRecordValidationTests(unittest.TestCase):
    def test_rejects_invalid_fields_in_inactive_occurrences(self):
        record = {"inicio": "2026-11-01", "fim": "2026-11-02",
                  "gravidade": 1, "local": "Natal", "tipo": "obra"}
        for changed in ({"local": ""}, {"tipo": "  "}, {"local": 25}, {"tipo": "x\nY"}):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                run({"data": "2026-11-22", "ocorrencias": [{**record, **changed}]})

    def test_valid_inactive_record_is_excluded(self):
        record = {"inicio": "2026-11-01", "fim": "2026-11-02",
                  "gravidade": 1, "local": "Natal", "tipo": "obra"}
        self.assertEqual(run({"data": "2026-11-22", "ocorrencias": [record]})["ativas"], 0)


if __name__ == "__main__":
    unittest.main()
