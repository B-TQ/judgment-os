import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from benchmark import prepare, packets, analyze, read_cases, SCORE_FIELDS  # noqa: E402


class BenchmarkTests(unittest.TestCase):
    def test_cases_are_valid_and_balanced(self):
        cases = read_cases(ROOT / "evals/cases.json")
        self.assertEqual(len(cases), 16)
        self.assertEqual(len([c for c in cases if c["category"].startswith("open")]), 8)
        self.assertEqual(len([c for c in cases if c["category"].startswith("control")]), 8)

    def test_seed_and_condition_balancing(self):
        with tempfile.TemporaryDirectory() as td:
            a = Path(td) / "a"
            b = Path(td) / "b"
            first = prepare(ROOT / "evals/cases.json", a, seed=7, repeats=2)
            second = prepare(ROOT / "evals/cases.json", b, seed=7, repeats=2)
            self.assertEqual(first, second)
            self.assertEqual(len(first), 16 * 2 * 3)
            for case_id in set(row["case_id"] for row in first):
                vals = [row["condition"] for row in first if row["case_id"] == case_id]
                self.assertEqual(vals.count("A"), 2)
                self.assertEqual(vals.count("B"), 2)
                self.assertEqual(vals.count("C"), 2)

    def test_blind_packet_and_hard_gate_report(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)/"pilot"
            runs = prepare(ROOT/"evals/cases.json", out)
            chosen = runs[:3]
            rows=[]
            for n, run in enumerate(chosen):
                (out/"outputs"/f"{run['blind_id']}.txt").write_text(f"Answer {n}",encoding="utf-8")
                entry={"blind_id":run["blind_id"],"hard_gate":"fail" if n==0 else "pass", "notes":"unit-test fixture"}
                if n:
                    entry.update({field: "4" for field in SCORE_FIELDS})
                rows.append(entry)
            packets(out)
            for run in chosen:
                packet=(out/"review_packets"/f"{run['blind_id']}.md").read_text(encoding="utf-8")
                self.assertNotIn("Judgment-preserver Skill excerpt",packet)
                self.assertIn("Candidate answer",packet)
            with (out/"ratings.csv").open("w",encoding="utf-8",newline="") as f:
                writer=csv.DictWriter(f,fieldnames=("blind_id","hard_gate",*SCORE_FIELDS,"notes"))
                writer.writeheader()
                writer.writerows(rows)
            report=analyze(out).read_text(encoding="utf-8")
            self.assertIn("Hard-gate pass",report)
            self.assertIn("Human ratings only",report)
            self.assertIn("4.00/5",report)

    def test_report_refuses_fake_empty_results(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)/"pilot"
            prepare(ROOT/"evals/cases.json", out)
            with self.assertRaisesRegex(ValueError,"No ratings yet"):
                analyze(out)


if __name__ == "__main__":
    unittest.main()
