"""Software fixtures only; no model calls, genuine study data or claimed calibration result."""
import csv
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from benchmark import prepare, SCORE_FIELDS
from calibration import build, mutate, score
from eval_common import digest, read_json, write_json
from review import REVIEW_FIELDS


class CalibrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.study = self.base / "study"
        cases = [{"id": c, "category": "control_exact", "user_prompt": "TEST FIXTURE task", "domain_skill": "TEST FIXTURE guide",
                  "review_focus": "TEST FIXTURE", "hard_gates": ["TEST FIXTURE"], "validators": []} for c in ("I01", "I02", "I03")]
        cases_path = self.base / "cases.json"
        write_json(cases_path, cases)
        self.rows = prepare(cases_path, self.study, conditions=("C",))
        self.answers = {"I01": "TEST FIXTURE: uncertain finish estimate.", "I02": "Notice\nChildren under 16 must come with an adult.\nReminder\n", "I03": '{"remaining_seats":0}'}
        votes = []
        for row in self.rows:
            key = row["blind_id"]
            answer = self.answers[row["case_id"]]
            (self.study / "outputs" / f"{key}.txt").write_text(answer, encoding="utf-8")
            write_json(self.study / "states" / f"{key}.json", {"status": "completed", "output_sha256": digest(answer), "source": "unit-test-fixture"})
            votes.append({"blind_id": key, "hard_gate": "pass"})
        write_json(self.study / "judges/fixture.ratings.json", {"ratings": votes})
        self.out = self.base / "calibration"

    def ratings(self, match=True):
        manifest = read_json(self.out / "private_manifest.json")
        rows = []
        for sample in manifest["samples"]:
            gate = sample["expected_gate"] if match else "pass"
            row = {"blind_id": sample["blind_id"], "output_sha256": sample["output_sha256"], "hard_gate": gate, "notes": "output-text-only SOFTWARE FIXTURE"}
            if gate == "pass":
                row.update({k: "4" for k in SCORE_FIELDS})
            rows.append(row)
        return rows

    def write_ratings(self, rows):
        path = self.out / "blind/ratings-filled.csv"
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=REVIEW_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def test_mutations_have_explicit_single_defects(self):
        value, _ = mutate("I01", self.answers["I01"])
        self.assertIn("confirmed cause", value)
        self.assertIn("guaranteed", value)
        value, _ = mutate("I02", self.answers["I02"])
        self.assertNotIn("adult", value)
        self.assertEqual(read_json_value(mutate("I03", self.answers["I03"])[0])["remaining_seats"], 1)
        with self.assertRaises(ValueError):
            mutate("I02", "No adult accompaniment line")

    def test_build_is_blinded_provenance_preserved_and_originals_unchanged(self):
        before = {p.name: p.read_bytes() for p in (self.study / "outputs").glob("*.txt")}
        build(self.study, self.out)
        self.assertEqual(before, {p.name: p.read_bytes() for p in (self.study / "outputs").glob("*.txt")})
        manifest = read_json(self.out / "private_manifest.json")
        self.assertEqual(len(manifest["samples"]), 6)
        self.assertEqual(sum(x["variant"] == "modified" for x in manifest["samples"]), 3)
        self.assertTrue(all("NOT a new model output" in x["provenance"] for x in manifest["samples"] if x["variant"] == "modified"))
        self.assertEqual({p.name for p in (self.out / "blind").iterdir()}, {"packets", "ratings.csv", "README.md"})
        for p in (self.out / "blind/packets").glob("*.md"):
            self.assertNotIn("expected_gate", p.read_text(encoding="utf-8"))
        with self.assertRaises(FileExistsError):
            build(self.study, self.out)

    def test_score_measures_detection_and_separates_efficacy(self):
        build(self.study, self.out)
        path = self.write_ratings(self.ratings())
        result = score(self.out, path, "unit-test-evaluator")
        self.assertEqual(result["known_defects_detected"], 3)
        self.assertEqual(result["original_controls_passed"], 3)
        self.assertEqual(result["pairs_discriminated"], 3)
        self.assertEqual(result["kind"], "evaluator_calibration_not_method_efficacy")
        with self.assertRaises(FileExistsError):
            score(self.out, path, "unit-test-evaluator")

    def test_all_pass_judge_is_detected_as_insensitive(self):
        build(self.study, self.out)
        result = score(self.out, self.write_ratings(self.ratings(match=False)), "unit-test-evaluator")
        self.assertEqual(result["known_defects_detected"], 0)
        self.assertEqual(result["pairs_discriminated"], 0)

    def test_duplicate_missing_and_changed_packets_rejected(self):
        build(self.study, self.out)
        rows = self.ratings()
        for bad in (rows[:-1], rows + [rows[0]], [{**rows[0], "output_sha256": "changed"}, *rows[1:]]):
            with self.assertRaises(ValueError):
                score(self.out, self.write_ratings(bad), "unit-test-evaluator")
        packet = next((self.out / "blind/packets").glob("*.md"))
        packet.write_text("CHANGED SOFTWARE FIXTURE", encoding="utf-8")
        with self.assertRaises(ValueError):
            score(self.out, self.write_ratings(rows), "unit-test-evaluator")

    def test_changed_original_refuses_build(self):
        key = self.rows[0]["blind_id"]
        (self.study / "outputs" / f"{key}.txt").write_text("CHANGED", encoding="utf-8")
        with self.assertRaises(ValueError):
            build(self.study, self.out)


def read_json_value(value):
    import json
    return json.loads(value)
