"""All answers/ratings in this file are explicit software-test fixtures, never study data."""
import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from benchmark import FIELDS, SCORE_FIELDS, analyze, prepare, validate_run
from codex_adapter import collect
from eval_common import read_json, redact
from eval_common import write_json
from reporting import interval
from review import REVIEW_FIELDS, export_review, import_ratings

ROOT = Path(__file__).resolve().parents[1]


def write_csv(path, rows, fields=REVIEW_FIELDS):
    with Path(path).open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.out = self.base / "private"
        self.runs = prepare(ROOT / "evals/cases.json", self.out)
        self.keys = [r["blind_id"] for r in self.runs if r["case_id"] == "O01"]

    def collect_key(self, key, text="TEST FIXTURE answer"):
        answer = self.base / "answer.txt"
        answer.write_text(text, encoding="utf-8")
        collect(self.out, key, answer, "unit-test-model", "fixture-1", "explicit software-test fixture")

    def export(self, reviewer="alice"):
        dest = self.base / reviewer
        export_review(self.out, dest, reviewer, extra=("private-literal",))
        with (dest / "ratings.csv").open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        return dest, rows

    def fill(self, dest, rows, fail_first=False):
        for i, row in enumerate(rows):
            row["hard_gate"] = "fail" if fail_first and i == 0 else "pass"
            if row["hard_gate"] == "pass":
                row.update({k: "4" for k in SCORE_FIELDS})
            else:
                row["notes"] = "TEST FIXTURE failed gate"
        write_csv(dest / "ratings.csv", rows)

    def test_export_allowlist_rekey_redact_and_import(self):
        self.collect_key(self.keys[0], "TEST FIXTURE sk-1234567890abcdefghijkl user@example.com private-literal")
        dest, rows = self.export()
        self.assertEqual({p.name for p in dest.iterdir()}, {"README.md", "ratings.csv", "packets"})
        for p in dest.rglob("*"):
            if p.is_file():
                text = p.read_text(encoding="utf-8")
                for secret in (self.keys[0], "1234567890abcdefghijkl", "user@example.com", "private-literal", "private_condition_map", "condition\":"):
                    self.assertNotIn(secret, text)
        self.assertTrue(rows[0]["blind_id"].startswith("R"))
        self.fill(dest, rows)
        import_ratings(self.out, "alice", dest / "ratings.csv", independent=True)
        analyze(self.out)
        report = read_json(self.out / "report.json")
        self.assertEqual(report["rated_outputs"], 1)
        self.assertEqual(report["reviewers"]["alice"], {"independence_declared": True, "verified": False, "kind": "human", "model": None})
        self.assertEqual(len(report["missing_outputs"]), 63)

    def test_empty_or_nested_exports_rejected(self):
        with self.assertRaisesRegex(ValueError, "No actual outputs"):
            export_review(self.out, self.base / "empty", "alice")
        with self.assertRaises(ValueError):
            export_review(self.out, self.out / "public", "alice")
        with self.assertRaises(ValueError):
            export_review(self.out, self.base, "../alice")

    def test_model_review_is_labeled_and_cannot_claim_human_independence(self):
        self.collect_key(self.keys[0])
        dest, rows = self.export()
        self.fill(dest, rows)
        with self.assertRaises(ValueError):
            import_ratings(self.out, "alice", dest / "ratings.csv", independent=True,
                           reviewer_kind="model", reviewer_model="unit-test-model")
        with self.assertRaises(ValueError):
            import_ratings(self.out, "alice", dest / "ratings.csv", reviewer_kind="model")
        import_ratings(self.out, "alice", dest / "ratings.csv", reviewer_kind="model", reviewer_model="unit-test-model")
        analyze(self.out)
        report = read_json(self.out / "report.json")
        self.assertEqual(report["reviewers"]["alice"]["kind"], "model")
        self.assertFalse(report["reviewers"]["alice"]["independence_declared"])
        self.assertEqual(report["gate_scope"], "output_text_only")
        self.assertFalse(report["behavioral_compliance_established"])
        self.assertIn("Includes model-assisted ratings", (self.out / "report.md").read_text(encoding="utf-8"))

    def test_duplicate_unknown_hash_and_nonfinite_ratings_rejected(self):
        self.collect_key(self.keys[0])
        dest, rows = self.export()
        self.fill(dest, rows)
        original = dict(rows[0])
        bad_sets = ([original, original], [{**original, "blind_id": "unknown"}],
                    [{**original, "output_sha256": "changed"}], [{**original, "goal_fit": "NaN"}],
                    [{**original, "goal_fit": "Infinity"}], [{**original, "hard_gate": "maybe"}],
                    [{**original, "hard_gate": "fail"}])
        for bad in bad_sets:
            write_csv(dest / "ratings.csv", bad)
            with self.assertRaises(ValueError):
                import_ratings(self.out, "alice", dest / "ratings.csv")
        self.assertFalse((self.out / "judges/alice.ratings.json").exists())

    def test_changed_output_cannot_keep_old_rating(self):
        self.collect_key(self.keys[0])
        dest, rows = self.export()
        self.fill(dest, rows)
        (self.out / "outputs" / f"{self.keys[0]}.txt").write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "changed"):
            import_ratings(self.out, "alice", dest / "ratings.csv")

    def test_deterministic_failure_cannot_be_scored_as_pass(self):
        key = next(r["blind_id"] for r in self.runs if r["case_id"] == "C02")
        self.collect_key(key, "NOT JSON -- TEST FIXTURE")
        dest, rows = self.export()
        self.fill(dest, rows)
        with self.assertRaisesRegex(ValueError, "deterministic"):
            import_ratings(self.out, "alice", dest / "ratings.csv")

    def test_multiple_judges_aggregate_outputs_once_and_keep_disagreement(self):
        self.collect_key(self.keys[0])
        for reviewer, fail in (("alice", False), ("bob", True)):
            dest, rows = self.export(reviewer)
            self.fill(dest, rows, fail_first=fail)
            import_ratings(self.out, reviewer, dest / "ratings.csv", independent=True)
        analyze(self.out)
        result = read_json(self.out / "report.json")
        self.assertEqual(result["rating_rows"], 2)
        self.assertEqual(result["rated_outputs"], 1)
        cond = self.runs[0]["condition"]
        self.assertEqual(result["conditions"][cond]["judge_disagreements"], 1)
        self.assertEqual(result["conditions"][cond]["hard_gate_fail"], 1)
        self.assertIsNone(result["conditions"][cond]["quality_on_pass"])

    def test_legacy_local_ratings_reject_duplicates_and_empty_output(self):
        row = {"blind_id": self.keys[0], "hard_gate": "pass", **{k: "4" for k in SCORE_FIELDS}}
        write_csv(self.out / "ratings.csv", [row], FIELDS)
        with self.assertRaisesRegex(ValueError, "missing"):
            analyze(self.out)
        self.collect_key(self.keys[0])
        write_csv(self.out / "ratings.csv", [row, row], FIELDS)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            analyze(self.out)

    def test_missing_output_state_and_case_snapshot_integrity(self):
        (self.out / "outputs" / f"{self.keys[0]}.txt").unlink()
        result = validate_run(self.out)
        self.assertEqual(result[self.keys[0]]["status"], "missing")
        cases = read_json(self.out / "cases_snapshot.json")
        cases[0]["hard_gates"] = []
        (self.out / "cases_snapshot.json").write_text(json.dumps(cases), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "snapshot changed"):
            validate_run(self.out)

    def test_redaction_limit_patterns(self):
        text = redact('Bearer abcdef123456 sk-123456789012345 api_key=abcdef\nC:\\Users\\someone\\file.txt')
        for literal in ("abcdef123456", "123456789012345", "api_key=abcdef", "someone"):
            self.assertNotIn(literal, text)


class PairedTests(unittest.TestCase):
    def test_intervals_use_cases_not_repeats(self):
        self.assertIsNone(interval([1] * 9))
        self.assertEqual(interval([1] * 10), [1, 1])
        self.assertEqual(interval(list(range(16))), interval(list(range(16))))

    def test_paired_complete_pairs_and_failure_exclusions(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "private"
            runs = prepare(ROOT / "evals/cases.json", out, repeats=2)
            rows = []
            for r in runs:
                if r["case_id"] != "O01" or r["condition"] not in "BCD":
                    continue
                (out / "outputs" / f"{r['blind_id']}.txt").write_text("TEST FIXTURE", encoding="utf-8")
                fail = r["condition"] == "B" and r["repeat"] == 2
                row = {"blind_id": r["blind_id"], "hard_gate": "fail" if fail else "pass", "notes": "TEST FIXTURE"}
                if not fail:
                    row.update({k: "4" if r["condition"] == "C" else "3" for k in SCORE_FIELDS})
                rows.append(row)
            write_csv(out / "ratings.csv", rows, FIELDS)
            analyze(out)
            result = read_json(out / "report.json")
            gate = next(p for p in result["paired"] if p["comparison"] == "C-B" and p["scope"] == "all" and p["metric"] == "hard_gate_pass_delta")
            quality = next(p for p in result["paired"] if p["comparison"] == "C-B" and p["scope"] == "all" and p["metric"] == "quality_on_both_pass_delta")
            self.assertEqual(gate["matched_outputs"], 2)
            self.assertEqual(gate["case_clusters"], 1)
            self.assertEqual(gate["mean_delta"], 0.5)
            self.assertEqual(quality["matched_outputs"], 1)
            self.assertAlmostEqual(quality["mean_delta"], 1)
            self.assertIsNone(gate["bootstrap_95_interval"])
            self.assertEqual(gate["metadata_unverified_pairs"], 2)

    def test_known_model_mismatch_is_excluded_from_paired_estimate(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "private"
            runs = prepare(ROOT / "evals/cases.json", out)
            rows = []
            for r in runs:
                if r["case_id"] != "O01" or r["condition"] not in "BC":
                    continue
                (out / "outputs" / f"{r['blind_id']}.txt").write_text("TEST FIXTURE", encoding="utf-8")
                write_json(out / "states" / f"{r['blind_id']}.json", {"status": "completed", "model_requested": "model-" + r["condition"],
                    "model_version_observed": "fixture-v1", "settings": {"effort": "low"}, "usage": None})
                rows.append({"blind_id": r["blind_id"], "hard_gate": "pass", **{k: "4" for k in SCORE_FIELDS}})
            write_csv(out / "ratings.csv", rows, FIELDS)
            analyze(out)
            result = read_json(out / "report.json")
            pair = next(p for p in result["paired"] if p["comparison"] == "C-B" and p["scope"] == "all" and p["metric"] == "hard_gate_pass_delta")
            self.assertEqual(pair["excluded_profile_mismatches"], 1)
            self.assertEqual(pair["matched_outputs"], 0)
            self.assertIsNone(pair["mean_delta"])
