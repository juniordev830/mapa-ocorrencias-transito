import unittest
from app import run


class OccurrenceBoundsTests(unittest.TestCase):
    def test_rejects_large_input_list_before_processing(self):
        with self.assertRaisesRegex(ValueError, "5000"):
            run({"data": "2026-11-22", "ocorrencias": [{}] * 5001})

    def test_accepts_limit_of_empty_list(self):
        self.assertEqual(run({"data": "2026-11-22", "ocorrencias": []})["ativas"], 0)

    def test_rejects_non_object_list_members(self):
        with self.assertRaises(ValueError):
            run({"data": "2026-11-22", "ocorrencias": [None]})


if __name__ == "__main__":
    unittest.main()
