"""Public entry point and managed-installation acceptance tests. No model calls."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import judgment
from skill_install import install, uninstall


class PublicCliTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.project = self.root / "project"
        self.project.mkdir()

    def command(self, *args):
        return subprocess.run([sys.executable, "-X", "utf8", "-B", str(ROOT / "judgment.py"), *args],
                              cwd=self.root, capture_output=True, text=True, encoding="utf-8", timeout=45)

    def test_help_version_and_routed_help_from_other_cwd(self):
        for args in [("--help",), ("--version",), ("prepare", "--help"), ("review", "--help"),
                     ("run", "--help"), ("report", "--help"), ("selftest", "--help")]:
            result = self.command(*args)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(self.command("unknown-command").returncode, 2)

    def test_doctor_never_runs_auth_or_model_commands(self):
        with patch("subprocess.run", side_effect=AssertionError("No subprocess allowed")):
            result = judgment.doctor()
        self.assertEqual(result["model_calls"], 0)
        self.assertTrue(result["python_supported"])
        self.assertIn("not checked", result["live_authentication"])

    def test_tutorial_has_empty_slots_and_labeled_software_checks(self):
        out = self.root / "tutorial"
        result = judgment.tutorial(out)
        self.assertEqual(result["prepared_slots"], 8)
        self.assertEqual(result["model_calls"], 0)
        self.assertEqual(result["ratings"], 0)
        self.assertEqual(result["bundled_software_fixture_checks"], {"correct": "pass", "incorrect": "fail"})
        self.assertTrue(all(not p.read_text(encoding="utf-8").strip() for p in (out / "study/outputs").glob("*.txt")))
        with self.assertRaises(FileExistsError):
            judgment.tutorial(out)

    def test_single_answer_pass_fail_missing_and_unknown_case(self):
        for name, code in (("correct", 0), ("incorrect", 1)):
            r = self.command("check", "--case", "Q01", "--answer", str(ROOT / f"examples/quickstart/{name}.json"))
            self.assertEqual(r.returncode, code, r.stderr)
        for args in [("check", "--case", "unknown", "--answer", str(ROOT / "examples/quickstart/correct.json")),
                     ("check", "--case", "Q01", "--answer", "missing.json")]:
            r = self.command(*args)
            self.assertEqual(r.returncode, 1)
            self.assertNotIn("Traceback", r.stderr)

    def test_install_dry_run_is_read_only_then_round_trip(self):
        planned = install(ROOT, self.project, dry_run=True)
        self.assertTrue(planned["dry_run"])
        self.assertEqual(list(self.project.iterdir()), [])
        install(ROOT, self.project)
        target = self.project / ".agents/skills/judgment-preserver"
        self.assertEqual((target / "SKILL.md").read_bytes(), (ROOT / ".agents/skills/judgment-preserver/SKILL.md").read_bytes())
        uninstall(ROOT, self.project, dry_run=True)
        self.assertTrue(target.is_dir())
        uninstall(ROOT, self.project)
        self.assertFalse(target.exists())

    def test_existing_skill_is_never_overwritten(self):
        target = self.project / ".agents/skills/judgment-preserver"
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("USER WORK", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            install(ROOT, self.project)
        self.assertEqual((target / "SKILL.md").read_text(encoding="utf-8"), "USER WORK")

    def test_changed_or_added_user_files_block_all_uninstall_mutations(self):
        install(ROOT, self.project)
        target = self.project / ".agents/skills/judgment-preserver"
        original = (target / "SKILL.md").read_bytes()
        for mode in ("changed", "extra-file", "extra-empty-directory"):
            if mode == "changed":
                (target / "SKILL.md").write_text("USER EDIT", encoding="utf-8")
            elif mode == "extra-file":
                (target / "mine.txt").write_text("USER WORK", encoding="utf-8")
            else:
                (target / "mine").mkdir()
            with self.assertRaises(ValueError):
                uninstall(ROOT, self.project)
            self.assertTrue((target / ".judgment-os-install.json").exists())
            if mode == "changed":
                self.assertEqual((target / "SKILL.md").read_text(encoding="utf-8"), "USER EDIT")
                (target / "SKILL.md").write_bytes(original)
            elif mode == "extra-file":
                (target / "mine.txt").unlink()
            else:
                (target / "mine").rmdir()

    def test_unrecognized_installation_is_preserved(self):
        target = self.project / ".agents/skills/judgment-preserver"
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("USER WORK", encoding="utf-8")
        with self.assertRaises(FileNotFoundError):
            uninstall(ROOT, self.project)
        self.assertEqual((target / "SKILL.md").read_text(encoding="utf-8"), "USER WORK")

    def test_parent_link_outside_project_is_rejected(self):
        outside = self.root / "outside"
        outside.mkdir()
        try:
            (self.project / ".agents").symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"Symlink privilege unavailable: {exc}")
        with self.assertRaises(ValueError):
            install(ROOT, self.project)
        self.assertEqual(list(outside.iterdir()), [])

    def test_public_errors_are_concise(self):
        r = self.command("review", "report", "--out", str(self.root / "missing"))
        self.assertEqual(r.returncode, 1)
        self.assertNotIn("Traceback", r.stderr)

    def test_public_report_requires_explicit_phase_selection(self):
        for args in [("report", "--out", "unused"), ("review", "report", "--out", "unused")]:
            r = self.command(*args)
            self.assertEqual(r.returncode, 1)
            self.assertIn("Select a review phase", r.stderr)
