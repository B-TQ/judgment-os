import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from benchmark import prepare
from codex_adapter import collect, discover, parse_events, run, run_lock, subscription_environment
from eval_common import read_json

ROOT = Path(__file__).resolve().parents[1]
PROBE = {"available": True, "executable": "fixture-codex", "version": "fixture-1"}


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name) / "run"
        self.runs = prepare(ROOT / "evals/cases.json", self.out)
        self.key = self.runs[0]["blind_id"]

    def test_missing_cli_and_dry_run_never_calls_model(self):
        with patch("codex_adapter.shutil.which", return_value=None):
            self.assertFalse(discover()["available"])
        with patch("codex_adapter.discover", return_value={"available": False}), patch("codex_adapter.subprocess.run") as call:
            plans = run(self.out, max_runs=2)
            call.assert_not_called()
            self.assertEqual(len(plans), 2)
            self.assertEqual(plans[0]["status"], "dry_run")
            self.assertEqual((self.out / "outputs" / f"{self.key}.txt").read_text(), "")

    def test_live_requires_explicit_cost_model_and_cli(self):
        for args in ({"live": True}, {"live": True, "acknowledge_cost": True}):
            with self.assertRaises(ValueError):
                run(self.out, **args)
        with patch("codex_adapter.discover", return_value={"available": False}):
            with self.assertRaises(ValueError):
                run(self.out, live=True, acknowledge_cost=True, model="fixture")

    def test_live_collects_final_message_and_public_usage_only(self):
        def fake(command, **kwargs):
            Path(command[command.index("--output-last-message") + 1]).write_text("TEST FIXTURE answer", encoding="utf-8")
            self.assertEqual(command[-1], "-")
            self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", command)
            stream = '\n'.join(json.dumps(v) for v in (
                {"type": "item.completed", "item": {"type": "reasoning", "text": "DO NOT RETAIN"}},
                {"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 2}}))
            return subprocess.CompletedProcess(command, 0, stream, "token=private-value")
        with patch("codex_adapter.discover", return_value=PROBE), patch("codex_adapter.verify_inputs", return_value=("task", Path(self.temp.name))), patch("codex_adapter.subprocess.run", side_effect=fake):
            state = run(self.out, live=True, acknowledge_cost=True, model="fixture", ids=[self.key])[0]
        self.assertEqual(state["status"], "completed")
        self.assertEqual(state["usage"]["input_tokens"], 10)
        self.assertIsNone(state["model_version_observed"])
        self.assertNotIn("DO NOT RETAIN", (self.out / "traces" / f"{self.key}.events.json").read_text())
        self.assertNotIn("private-value", (self.out / "traces" / f"{self.key}.stderr.txt").read_text())
        self.assertFalse((self.out / "traces" / f"{self.key}.last-message.tmp").exists())

    def test_failure_timeout_and_interrupt_do_not_become_results(self):
        for exc, expected in ((subprocess.TimeoutExpired("fixture", 1), "aborted"),
                              (OSError("fixture failure"), "failed"), (KeyboardInterrupt(), "aborted")):
            state_path = self.out / "states" / f"{self.key}.json"
            state_path.write_text('{"status":"pending"}', encoding="utf-8")
            with patch("codex_adapter.discover", return_value=PROBE), patch("codex_adapter.verify_inputs", return_value=("task", Path(self.temp.name))), patch("codex_adapter.subprocess.run", side_effect=exc):
                if isinstance(exc, KeyboardInterrupt):
                    with self.assertRaises(KeyboardInterrupt):
                        run(self.out, live=True, acknowledge_cost=True, model="fixture", ids=[self.key])
                else:
                    run(self.out, live=True, acknowledge_cost=True, model="fixture", ids=[self.key])
            self.assertEqual(read_json(state_path)["status"], expected)
            self.assertEqual((self.out / "outputs" / f"{self.key}.txt").read_text(), "")
            self.assertFalse((self.out / ".adapter.lock").exists())

    def test_malformed_or_failed_events(self):
        self.assertTrue(parse_events('{"type":"turn.failed"}')["failed"])
        with self.assertRaises(ValueError):
            parse_events("not json")
        with patch("codex_adapter.discover", return_value=PROBE), patch("codex_adapter.verify_inputs", return_value=("task", Path(self.temp.name))), patch("codex_adapter.subprocess.run", return_value=subprocess.CompletedProcess([], 0, 'not json', '')):
            result = run(self.out, live=True, acknowledge_cost=True, model="fixture", ids=[self.key])
        self.assertEqual(result[0]["status"], "failed")

    def test_secret_redaction_preserves_event_json_structure(self):
        result = parse_events(json.dumps({"type": "error", "error": {"message": 'token=private-value "quoted"', "retryable": False}}))
        self.assertTrue(result["failed"])
        self.assertIs(result["events"][0]["error"]["retryable"], False)
        self.assertNotIn("private-value", json.dumps(result))
        tool = parse_events(json.dumps({"type": "item.completed", "item": {"type": "mcp_tool_call", "server": "fixture", "tool": "read", "arguments": {"secret": "DO NOT RETAIN"}}}))
        self.assertEqual(tool["events"][0]["item"]["type"], "mcp_tool_call")
        self.assertNotIn("DO NOT RETAIN", json.dumps(tool))
        with self.assertRaises(ValueError):
            parse_events('{"type":"item.completed","item":null}')

    def test_subscription_only_strips_api_keys_and_checks_login(self):
        with patch.dict("codex_adapter.os.environ", {"OPENAI_API_KEY": "TEST-KEY", "CODEX_API_KEY": "TEST-KEY-2"}), patch("codex_adapter.subprocess.run", return_value=subprocess.CompletedProcess([], 0, "Logged in using ChatGPT", "")) as call:
            environment = subscription_environment("fixture-codex")
            self.assertNotIn("OPENAI_API_KEY", environment)
            self.assertNotIn("CODEX_API_KEY", environment)
            self.assertEqual(call.call_args.args[0], ["fixture-codex", "login", "status"])
        with patch("codex_adapter.subprocess.run", return_value=subprocess.CompletedProcess([], 0, "Logged in using API key", "")):
            with self.assertRaises(ValueError):
                subscription_environment("fixture-codex")

    def test_manual_collection_provenance_and_overwrite(self):
        answer = Path(self.temp.name) / "answer.txt"
        answer.write_text("TEST FIXTURE", encoding="utf-8")
        collect(self.out, self.key, answer, "fixture", "fixture-v1", "unit-test fixture")
        state = read_json(self.out / "states" / f"{self.key}.json")
        self.assertEqual(state["status"], "completed")
        self.assertIsNone(state["latency_seconds"])
        with self.assertRaises(ValueError):
            collect(self.out, self.key, answer, "fixture", "fixture-v1", "test")
        with run_lock(self.out):
            with self.assertRaises(ValueError):
                with run_lock(self.out):
                    pass

    @unittest.skipUnless(shutil.which("git"), "native staging requires git")
    def test_native_skill_presence_and_explicit_invocation(self):
        out = Path(self.temp.name) / "native"
        cases = ROOT / "evals/cases.json"
        rows = prepare(cases, out, mode="codex-native")
        for row in rows:
            base = out / "workspaces" / row["blind_id"]
            self.assertTrue((base / ".git").is_dir())
            self.assertEqual((base / ".agents/skills/domain-fixture/SKILL.md").exists(), row["condition"] in "BCD")
            self.assertEqual((base / ".agents/skills/judgment-preserver/SKILL.md").exists(), row["condition"] == "C")
            prompt = (out / "prompts" / f"{row['blind_id']}.md").read_text(encoding="utf-8")
            self.assertEqual("$judgment-preserver" in prompt, row["condition"] == "C")
