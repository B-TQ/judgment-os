import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validators import validate


class ValidatorTests(unittest.TestCase):
    def test_json_exact_and_invalid(self):
        spec = [{"kind": "json_exact", "value": {"count": 2, "status": "ok"}}]
        for text in ('{"status":"ok","count":2}', ' {"count":2,"status":"ok"}\n'):
            self.assertEqual(validate(spec, text)["status"], "pass")
        for text in ('```json\n{}\n```', '{"count":2,"count":2,"status":"ok"}',
                     '{"count":true,"status":"ok"}', '{"count":2,"status":"ok","x":0}', 'NaN'):
            self.assertEqual(validate(spec, text)["status"], "fail")

    def test_csv_order_and_extra_rows(self):
        spec = [{"kind": "csv_exact", "headers": ["a", "b"], "rows": [["x", "y"]]}]
        self.assertEqual(validate(spec, 'a,b\r\nx,y\r\n')["status"], "pass")
        for text in ('b,a\nx,y', 'a,b\nx,y\nz,w', 'Here:\na,b\nx,y'):
            self.assertEqual(validate(spec, text)["status"], "fail")

    def test_prefix_and_headings(self):
        spec = [{"kind": "lines_prefix", "lines": 2, "prefix": "Fictional object:"}]
        self.assertEqual(validate(spec, "Fictional object: Clock\nTime sleeps.")["status"], "pass")
        self.assertEqual(validate(spec, "Clock\nTime sleeps.")["status"], "fail")
        self.assertEqual(validate(spec, "Fictional object: Clock\n\nTime sleeps.")["status"], "fail")
        headings = [{"kind": "headings", "values": ["# Summary", "## Facts", "## Risks"]}]
        self.assertEqual(validate(headings, '# Summary\nHi\n## Facts\nYes\n## Risks\nUnknown')["status"], "pass")
        self.assertEqual(validate(headings, '# Summary\n## Risks\n## Facts')["status"], "fail")
        self.assertEqual(validate([], "anything")["status"], "not_applicable")

    def test_word_count_and_unknown(self):
        spec = [{"kind": "word_count", "min": 2, "max": 3}]
        self.assertEqual(validate(spec, "one two")["status"], "pass")
        self.assertEqual(validate(spec, "one")["status"], "fail")
        with self.assertRaises(ValueError):
            validate([{"kind": "guess_safety"}], "")

    def test_invalid_configurations_fail_instead_of_becoming_output_failures(self):
        for spec in ({"kind": "json_exact"}, {"kind": "word_count", "min": 5, "max": 2},
                     {"kind": "lines_prefix", "lines": 0, "prefix": ""},
                     {"kind": "csv_exact", "headers": ["x"], "rows": [[1]]},
                     {"kind": "headings", "values": ["not a heading"]}):
            with self.assertRaises(ValueError):
                validate([spec], "")
