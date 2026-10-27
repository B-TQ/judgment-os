"""Software fixtures only: integrity, orientation, gate precedence and disagreement."""
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from benchmark import prepare
from eval_common import digest, read_json, write_json
from paired_review import export, import_review, report, csv_read, csv_write, QUALITY_FIELDS, PAIR_FIELDS


class PairedReviewTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.out = self.root / "run"
        cases = [{"id": "FIX", "category": "open_fit", "user_prompt": "FIXTURE task",
                  "domain_skill": "FIXTURE guide", "review_focus": "FIXTURE focus", "hard_gates": [],
                  "validators": [], "quality_anchors": {"3": "FIXTURE correct"}}]
        write_json(self.root / "cases.json", cases)
        self.mapping = prepare(self.root / "cases.json", self.out)
        for entry in self.mapping:
            key = entry["blind_id"]
            answer = f"SOFTWARE FIXTURE {key}"
            (self.out / "outputs" / f"{key}.txt").write_text(answer, encoding="utf-8")
            write_json(self.out / "states" / f"{key}.json", {"status": "completed", "output_sha256": digest(answer)})

    def fixture(self, reviewer="j1", preferred="C", fail=None):
        dest = self.root / reviewer
        export(self.out, dest, reviewer)
        receipt = read_json(self.out / "paired_judges" / f"{reviewer}.receipt.json")
        condition = {e["blind_id"]: e["condition"] for e in self.mapping}
        aliases = receipt["aliases"]
        conditions = {a: condition[r["blind_id"]] for a, r in aliases.items()}
        quality = csv_read(dest / "quality.csv", QUALITY_FIELDS)
        for row in quality:
            passing = conditions[row["candidate_id"]] != fail
            row.update(hard_gate="pass" if passing else "fail", quality="3" if passing else "", evidence="SOFTWARE FIXTURE evidence")
        pairs = csv_read(dest / "pairs.csv", PAIR_FIELDS)
        for row in pairs:
            left, right = conditions[row["left_id"]], conditions[row["right_id"]]
            choice = "right" if left == fail else ("left" if right == fail else (
                "left" if left == preferred else ("right" if right == preferred else "tie")))
            row.update(choice=choice, evidence="SOFTWARE FIXTURE comparison")
        q, p = dest / "quality-filled.csv", dest / "pairs-filled.csv"
        csv_write(q, QUALITY_FIELDS, quality)
        csv_write(p, PAIR_FIELDS, pairs)
        return dest, q, p, quality, pairs

    def test_export_blinds_condition_and_rekeys_each_review(self):
        a, *_ = self.fixture()
        b, *_ = self.fixture("j2")
        ra = read_json(self.out / "paired_judges/j1.receipt.json")
        rb = read_json(self.out / "paired_judges/j2.receipt.json")
        self.assertFalse(set(ra["aliases"]) & set(rb["aliases"]))
        self.assertEqual(len(ra["pairs"]), 6)
        for dest in (a, b):
            text = "".join(p.read_text(encoding="utf-8") for p in (dest / "groups").glob("*.md"))
            self.assertNotIn("condition", text)
            self.assertNotIn("domain_skill", text)
            self.assertNotIn("paired_judges", text)
        with self.assertRaises(FileExistsError):
            export(self.out, self.root / "another", "j1")

    def test_complete_import_pair_orientation_and_disagreement(self):
        _, q, p, *_ = self.fixture()
        import_review(self.out, "j1", q, p, "SOFTWARE FIXTURE")
        _, q, p, *_ = self.fixture("j2", preferred="D")
        import_review(self.out, "j2", q, p, "SOFTWARE FIXTURE")
        result = report(self.out)
        self.assertEqual(result["judges"][0]["comparisons"]["C-D"]["counts"], {"win": 1, "tie": 0, "loss": 0})
        self.assertEqual(result["judges"][1]["comparisons"]["C-D"]["counts"], {"win": 0, "tie": 0, "loss": 1})
        self.assertEqual(next(r for r in result["concordance"] if r["comparison"] == "C-D")["agreement"], "disputed")

    def test_missing_duplicate_invalid_scores_and_unexplained_ratings_rejected(self):
        _, q, p, rows, _ = self.fixture()
        for bad in (rows[:-1], rows + [rows[0]], [{**rows[0], "quality": "nan"}, *rows[1:]],
                    [{**rows[0], "quality": "4.0"}, *rows[1:]], [{**rows[0], "evidence": ""}, *rows[1:]]):
            csv_write(q, QUALITY_FIELDS, bad)
            with self.assertRaises(ValueError):
                import_review(self.out, "j1", q, p, "SOFTWARE FIXTURE")

    def test_missing_reversed_and_duplicate_pairs_rejected(self):
        _, q, p, _, rows = self.fixture()
        for bad in (rows[:-1], rows + [rows[0]],
                    [{**rows[0], "left_id": rows[0]["right_id"], "right_id": rows[0]["left_id"]}, *rows[1:]]):
            csv_write(p, PAIR_FIELDS, bad)
            with self.assertRaises(ValueError):
                import_review(self.out, "j1", q, p, "SOFTWARE FIXTURE")

    def test_gate_precedence_enforced(self):
        _, q, p, _, rows = self.fixture(fail="C")
        import_review(self.out, "j1", q, p, "SOFTWARE FIXTURE")
        result = report(self.out)
        self.assertEqual(result["judges"][0]["conditions"]["C"]["pass"], 0)
        _, q, p, _, rows = self.fixture("j2", fail="C")
        receipt = read_json(self.out / "paired_judges/j2.receipt.json")
        ckey = next(e["blind_id"] for e in self.mapping if e["condition"] == "C")
        ca = next(a for a, r in receipt["aliases"].items() if r["blind_id"] == ckey)
        row = next(r for r in rows if ca in (r["left_id"], r["right_id"]))
        row["choice"] = "tie"
        csv_write(p, PAIR_FIELDS, rows)
        with self.assertRaises(ValueError):
            import_review(self.out, "j2", q, p, "SOFTWARE FIXTURE")

    def test_changed_packet_or_output_rejected_and_import_never_overwritten(self):
        dest, q, p, *_ = self.fixture()
        packet = next((dest / "groups").glob("*.md"))
        original = packet.read_text(encoding="utf-8")
        packet.write_text("CHANGED FIXTURE", encoding="utf-8")
        with self.assertRaises(ValueError):
            import_review(self.out, "j1", q, p, "SOFTWARE FIXTURE")
        packet.write_text(original, encoding="utf-8")
        import_review(self.out, "j1", q, p, "SOFTWARE FIXTURE")
        with self.assertRaises(FileExistsError):
            import_review(self.out, "j1", q, p, "SOFTWARE FIXTURE")
        next((self.out / "outputs").glob("*.txt")).write_text("CHANGED FIXTURE", encoding="utf-8")
        with self.assertRaises(ValueError):
            report(self.out)

    def test_deterministic_fail_cannot_be_overruled_by_model_pass(self):
        cases = read_json(self.out / "cases_snapshot.json")
        cases[0]["validators"] = [{"kind": "exact_text", "value": "REQUIRED FIXTURE"}]
        # Build a new frozen study, rather than editing a protocol's inputs.
        write_json(self.root / "cases2.json", cases)
        self.out = self.root / "run2"
        self.mapping = prepare(self.root / "cases2.json", self.out)
        for e in self.mapping:
            answer = "WRONG FIXTURE"
            (self.out / "outputs" / f"{e['blind_id']}.txt").write_text(answer, encoding="utf-8")
            write_json(self.out / "states" / f"{e['blind_id']}.json", {"status": "completed", "output_sha256": digest(answer)})
        _, q, p, *_ = self.fixture()
        with self.assertRaises(ValueError):
            import_review(self.out, "j1", q, p, "SOFTWARE FIXTURE")

    def test_pending_or_incomplete_conditions_cannot_export(self):
        key = self.mapping[0]["blind_id"]
        write_json(self.out / "states" / f"{key}.json", {"status": "pending"})
        with self.assertRaises(ValueError):
            export(self.out, self.root / "bad", "j1")
        self.assertFalse((self.root / "bad").exists())

    def test_review_phases_can_be_selected_without_silent_pooling(self):
        _, q, p, *_ = self.fixture()
        import_review(self.out, "j1", q, p, "SOFTWARE FIXTURE")
        _, q, p, *_ = self.fixture("j2", preferred="D")
        import_review(self.out, "j2", q, p, "SOFTWARE FIXTURE")
        selected = report(self.out, ["j2"])
        self.assertEqual(selected["reviewer_selection"], ["j2"])
        self.assertEqual(selected["judges"][0]["comparisons"]["C-D"]["counts"]["loss"], 1)
        for invalid in ([], ["j1", "j1"], ["unknown"], ["../j1"]):
            with self.assertRaises(ValueError):
                report(self.out, invalid)


if __name__ == "__main__":
    unittest.main()
