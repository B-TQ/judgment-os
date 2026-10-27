import sys
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_skills import audit  # noqa: E402


class SkillAuditTests(unittest.TestCase):
    def test_shipped_skill_manifest_passes(self):
        report=audit(ROOT/".agents/skills/judgment-preserver/SKILL.md")
        self.assertTrue(report["metadata_valid"], report["issues"])
        self.assertTrue(report["review_cues"])

    def test_invalid_directory_or_metadata_fails(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"bad-name"/"SKILL.md"
            path.parent.mkdir()
            path.write_text("---\nname: Not Valid\ndescription: ok\n---\nBody",encoding="utf-8")
            report=audit(path)
            self.assertFalse(report["metadata_valid"])

    def test_wording_is_just_cue_not_permission(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"safe-name"/"SKILL.md"
            path.parent.mkdir()
            path.write_text("---\nname: safe-name\ndescription: test\n---\nYou must keep evidence.",encoding="utf-8")
            report=audit(path)
            self.assertTrue(report["metadata_valid"])
            self.assertIn("never assign authority", report["caveat"])
            self.assertEqual(report["review_cues"][0]["signals"],["mandatory_wording_candidate"])


if __name__ == "__main__":
    unittest.main()
