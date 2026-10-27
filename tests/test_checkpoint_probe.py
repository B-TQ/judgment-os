import contextlib
import hashlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import release
from checkpoint import checkpoint, verify
from integration_probe import stage
from eval_common import load_mapping, read_json


class CheckpointProbeTests(unittest.TestCase):
    def test_checkpoint_retains_source_evidence_and_refuses_overwrite(self):
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
            evidence = base / "evidence"
            evidence.mkdir()
            (evidence / "observed.txt").write_text("TEST EVIDENCE FIXTURE", encoding="utf-8")
            dest = base / "backup"
            with patch.object(release, "ROOT", root), contextlib.redirect_stdout(io.StringIO()):
                release.main([])
                record = checkpoint(dest, [evidence])
                self.assertEqual(record["status"], "complete")
                self.assertTrue(record["private"])
                with zipfile.ZipFile(dest / record["source_archive"]) as z:
                    self.assertTrue(all(n.startswith("judgment-os-v0.4/") for n in z.namelist()))
                (evidence / "observed.txt").write_text("MODIFIED ORIGINAL", encoding="utf-8")
                self.assertEqual((dest / "private-evidence-1/observed.txt").read_text(), "TEST EVIDENCE FIXTURE")
                self.assertEqual(hashlib.sha256((dest / record["source_archive"]).read_bytes()).hexdigest(), record["source_sha256"])
                self.assertEqual(verify(dest)["version"], "0.4")
                with self.assertRaises(FileExistsError):
                    checkpoint(dest, [evidence])
                with self.assertRaises(ValueError):
                    checkpoint(root / "nested-backup")
                (dest / "private-evidence-1/observed.txt").write_text("CORRUPTED BACKUP", encoding="utf-8")
                with self.assertRaises(ValueError):
                    verify(dest)

    def test_body_probe_keeps_codes_out_of_prompt_and_freezes_staged_skill(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "probe"
            key = stage(out)
            expected = read_json(out / "expected_codes.json")
            prompt = (out / "run/prompts" / f"{key}.md").read_text(encoding="utf-8")
            self.assertTrue(all(c not in prompt for c in expected["codes"].values()))
            mapping = load_mapping(out / "run")
            self.assertIn(key, mapping)
            self.assertNotEqual(expected["core_skill_sha256"], expected["probe_skill_sha256"])
            for name, code in expected["codes"].items():
                text = (out / "run/workspaces" / key / ".agents/skills" / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(code, text)
