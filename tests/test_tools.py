import contextlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import release
from eval_common import read_json

ROOT = Path(__file__).resolve().parents[1]


class ToolTests(unittest.TestCase):
    def test_demo_cli_has_no_outputs_or_scores(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "demo"
            result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/demo.py"), "--out", str(out), "--cli", "definitely-absent-codex-fixture"],
                                    capture_output=True, text=True, encoding="utf-8", timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr)
            summary = read_json(out / "demo_summary.json")
            self.assertEqual(summary["model_calls"], 0)
            self.assertEqual(summary["candidate_answers"], 0)
            for mode in summary["modes"].values():
                self.assertEqual(mode["slots"], 64)
                self.assertEqual(mode["dry_run_plans"], 64)
                self.assertEqual(mode["missing_outputs"], 64)
                self.assertFalse(mode["cli_probe"]["available"])
                self.assertTrue(mode["empty_report_refused"])

    def test_release_allowlist_and_reproducible_zip(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            root = base / "source"
            root.mkdir()
            for name in release.TOP:
                (root / name).write_text("TEST SOURCE FIXTURE", encoding="utf-8")
            (root / "VERSION").write_text("0.4\n", encoding="utf-8")
            for name in (".agents/skills/judgment-preserver/SKILL.md", "distribution/judgment-preserver-v0.2-SKILL.md"):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("SKILL FIXTURE", encoding="utf-8")
            private = ("runs/study/private_condition_map.json", "docs/private_condition_map.json", "evals/alice.receipt.json", "docs/review-exports/answer.md", "evals/.env",
                       "evals/paired_judges/j1.ratings.json", "docs/paired_report.json", "evals/study_plan.json")
            for name in private:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("MUST NOT SHIP", encoding="utf-8")
            with patch.object(release, "ROOT", root), contextlib.redirect_stdout(io.StringIO()):
                release.main([])
                release.main(["--check", "--zip", str(base / "a.zip")])
                release.main(["--check", "--zip", str(base / "b.zip")])
                self.assertEqual((base / "a.zip").read_bytes(), (base / "b.zip").read_bytes())
                with zipfile.ZipFile(base / "a.zip") as z:
                    self.assertTrue(all("MUST NOT SHIP" not in z.read(name).decode("utf-8") for name in z.namelist()))
                (root / "README.md").write_text("modified", encoding="utf-8")
                with self.assertRaises(ValueError):
                    release.main(["--check"])

    def test_case_generation_is_reproducible(self):
        before = (ROOT / "evals/cases.json").read_bytes()
        # Authoring helper is executed in an isolated copy, never rewriting the shipped fixture.
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            (base / "scripts").mkdir()
            (base / "evals").mkdir()
            script = base / "scripts/make_cases.py"
            script.write_bytes((ROOT / "scripts/make_cases.py").read_bytes())
            result = subprocess.run([sys.executable, "-B", str(script)], capture_output=True, timeout=15)
            self.assertEqual(result.returncode, 0)
            self.assertEqual((base / "evals/cases.json").read_bytes(), before)
