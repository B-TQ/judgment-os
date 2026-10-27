#!/usr/bin/env python3
"""Codex CLI adapter. Default run is a plan-only dry-run, with no model call."""
from __future__ import annotations
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import hashlib
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

from eval_common import digest, load_mapping, private_file, read_json, redact, write_json

REQUIRED_FLAGS = ("--json", "--output-last-message", "--sandbox", "--ephemeral", "--ignore-user-config")


def now():
    return datetime.now(timezone.utc).isoformat()


def discover(cli=None):
    candidate = cli or shutil.which("codex") or shutil.which("codex.exe")
    if not candidate:
        return {"available": False, "reason": "Codex CLI not found; dry-run remains available"}
    candidate = str(Path(candidate).resolve()) if Path(candidate).is_file() else shutil.which(candidate)
    if not candidate or Path(candidate).suffix.lower() in (".cmd", ".bat", ".ps1"):
        return {"available": False, "reason": "Specify a native codex executable (shell wrappers unsupported)"}
    try:
        version = subprocess.run([candidate, "--version"], capture_output=True, text=True,
                                 encoding="utf-8", errors="replace", timeout=15, check=False)
        help_run = subprocess.run([candidate, "exec", "--help"], capture_output=True, text=True,
                                  encoding="utf-8", errors="replace", timeout=15, check=False)
        missing = [flag for flag in REQUIRED_FLAGS if flag not in help_run.stdout]
        return {"available": version.returncode == help_run.returncode == 0 and not missing,
                "executable": candidate, "version": redact(version.stdout.strip()),
                "missing_flags": missing, "checked_at": now()}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"available": False, "reason": redact(str(exc))}


@contextmanager
def run_lock(out):
    path = Path(out) / ".adapter.lock"
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ValueError("Adapter lock exists; inspect running process before manually removing stale lock") from exc
    try:
        os.write(fd, str(os.getpid()).encode())
        yield
    finally:
        os.close(fd)
        path.unlink(missing_ok=True)


def parse_events(text):
    """Use public exec JSONL only. Do not retain reasoning items or private logs."""
    usage, events, failed = {}, [], False
    for line in text.splitlines():
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict) or not isinstance(value.get("type"), str):
            raise ValueError("Exec JSONL event must be an object with a string type")
        kind = value.get("type")
        if kind == "turn.completed":
            if not isinstance(value.get("usage", {}), dict):
                raise ValueError("Invalid usage event")
            usage = {k: v for k, v in value.get("usage", {}).items()
                     if isinstance(v, int) and not isinstance(v, bool) and v >= 0}
        if kind in ("turn.failed", "error"):
            failed = True
        # A compact redacted audit trail, not raw transcripts or chain of thought.
        if kind in ("turn.started", "turn.completed", "turn.failed", "error", "thread.started"):
            safe = {k: v for k, v in value.items() if k in ("type", "usage", "thread_id", "error", "message")}
            events.append(redact_value(safe))
        elif kind == "item.completed":
            item = value.get("item")
            if not isinstance(item, dict) or not isinstance(item.get("type"), str):
                raise ValueError("Invalid completed item event")
            if item["type"] != "reasoning":
                # Retain tool/action type metadata, not arguments, returned data or reasoning.
                safe = {k: item[k] for k in ("id", "type", "command", "exit_code", "status", "server", "tool", "url") if k in item}
                events.append({"type": kind, "item": redact_value(safe)})
    return {"usage": usage or None, "failed": failed,
            "completed": any(e["type"] == "turn.completed" for e in events), "events": events}


def redact_value(value):
    """Redact string leaves without changing JSON quoting or numeric types."""
    if isinstance(value, str):
        return redact(value)
    if isinstance(value, list):
        return [redact_value(x) for x in value]
    if isinstance(value, dict):
        return {k: redact_value(v) for k, v in value.items()}
    return value


def subscription_environment(executable):
    environment = {k: v for k, v in os.environ.items() if k.upper() not in ("OPENAI_API_KEY", "CODEX_API_KEY")}
    status = subprocess.run([executable, "login", "status"], env=environment, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", timeout=15, check=False)
    # Do not print authentication material; the documented status is sufficient.
    if status.returncode or "logged in using chatgpt" not in (status.stdout + status.stderr).lower():
        raise ValueError("Subscription-only mode requires an existing ChatGPT login; no model call made")
    return environment


def command_for(executable, workspace, answer_file, model, effort=None):
    command = [executable, "exec", "--json", "--ephemeral", "--ignore-user-config",
               "--sandbox", "read-only", "--skip-git-repo-check", "-C", str(workspace),
               "--model", model, "--output-last-message", str(answer_file)]
    if effort:
        command += ["-c", f'model_reasoning_effort="{effort}"']
    return command + ["-"]


def verify_inputs(out, key, entry, mode):
    prompt = (out / "prompts" / f"{key}.md").read_text(encoding="utf-8")
    if digest(prompt) != entry["prompt_sha256"]:
        raise ValueError(f"Prompt changed since preparation: {key}")
    if mode == "codex-native":
        workspace = (out / "workspaces" / key).resolve()
        actual = {str(p.relative_to(workspace)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in workspace.rglob("*") if p.is_file() and ".git" not in p.relative_to(workspace).parts}
        if actual != entry["workspace_files"] or not (workspace / ".git").is_dir():
            raise ValueError(f"Native workspace changed: {key}")
    else:
        # Avoid accidentally discovering the repository's meta-Skill in all groups.
        workspace = (out / "workspaces" / key).resolve()
        workspace.mkdir(parents=True, exist_ok=True)
        if not (workspace / ".git").exists():
            git = shutil.which("git")
            if not git:
                raise ValueError("Live CLI execution requires git for separate discovery roots")
            subprocess.run([git, "init", "--quiet", str(workspace)], check=True,
                           capture_output=True, timeout=20)
    return prompt, workspace


def run(out, cli=None, live=False, acknowledge_cost=False, model=None,
        max_runs=1, timeout=180, effort=None, ids=None, subscription_only=False):
    out = Path(out).resolve()
    if max_runs < 1 or not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("max-runs and timeout must be positive")
    if live and (not acknowledge_cost or not model):
        raise ValueError("Live execution requires --acknowledge-cost and an explicit --model")
    mapping = load_mapping(out)
    if ids and set(ids) - set(mapping):
        raise ValueError("Unknown selected blind_id")
    protocol = read_json(out / "protocol.json")
    probe = discover(cli)
    write_json(out / "cli_probe.json", probe)
    if live and not probe["available"]:
        raise ValueError("CLI capability probe failed; no live call made (see cli_probe.json)")
    environment = subscription_environment(probe["executable"]) if live and subscription_only else None
    selected = [key for key in mapping if not ids or key in ids]
    plans = []
    with run_lock(out):
        for key in selected:
            state_path = out / "states" / f"{key}.json"
            state = read_json(state_path)
            output = out / "outputs" / f"{key}.txt"
            if state["status"] not in ("pending", "dry_run") or output.read_text(encoding="utf-8").strip():
                continue  # never overwrite a completed/failed/interrupted slot
            entry = mapping[key]
            prompt = (out / "prompts" / f"{key}.md").read_text(encoding="utf-8")
            if digest(prompt) != entry["prompt_sha256"]:
                raise ValueError(f"Prompt changed since preparation: {key}")
            workspace = out / "workspaces" / key
            answer_file = out / "traces" / f"{key}.last-message.tmp"
            command = command_for(probe.get("executable", "codex"), workspace, answer_file, model or "<MODEL_REQUIRED>", effort)
            plan = {"blind_id": key, "mode": protocol["mode"], "command": command,
                    "status": "dry_run", "model_requested": model, "cli_available": probe["available"],
                    "native_activation": "not_verified", "prompt_sha256": digest(prompt)}
            if not live:
                write_json(state_path, plan)
                plans.append(plan)
            else:
                prompt, workspace = verify_inputs(out, key, entry, protocol["mode"])
                state = {**plan, "status": "running", "started_at": now(), "cli_version": probe["version"],
                         "model_version_observed": None, "settings": {"reasoning_effort": effort,
                         "sandbox": "read-only", "ignore_user_config": True},
                         "subscription_only_verified": bool(subscription_only),
                         "ambient_skills": "not_isolated; inspect in dedicated environment before publication"}
                write_json(state_path, state)
                start = time.monotonic()
                try:
                    completed = subprocess.run(command, input=prompt, capture_output=True, text=True,
                                               encoding="utf-8", errors="replace", timeout=timeout, check=False, env=environment)
                    state["exit_code"] = completed.returncode
                    parsed = parse_events(completed.stdout)
                    state["usage"] = parsed["usage"]
                    write_json(out / "traces" / f"{key}.events.json", parsed["events"])
                    (out / "traces" / f"{key}.stderr.txt").write_text(redact(completed.stderr), encoding="utf-8")
                    answer = answer_file.read_text(encoding="utf-8") if answer_file.exists() else ""
                    if completed.returncode or parsed["failed"] or not parsed["completed"] or not answer.strip():
                        state.update(status="failed", reason="Nonzero exit, failed/incomplete events, or empty final message")
                    else:
                        output.write_text(answer, encoding="utf-8")
                        private_file(output)
                        state.update(status="completed", output_sha256=digest(answer), source="codex-exec")
                except subprocess.TimeoutExpired:
                    state.update(status="aborted", reason="timeout")
                except KeyboardInterrupt:
                    state.update(status="aborted", reason="operator_interrupt")
                    raise
                except (OSError, ValueError, subprocess.SubprocessError) as exc:
                    state.update(status="failed", reason=redact(str(exc)))
                finally:
                    answer_file.unlink(missing_ok=True)
                    state.update(finished_at=now(), latency_seconds=time.monotonic() - start)
                    write_json(state_path, state)
                plans.append(state)
            if len(plans) >= max_runs:
                break
        write_json(out / "adapter_plan.json", plans)
    print(f"{'Live attempts' if live else 'Dry-run plans'}: {len(plans)}; model outputs are never synthesized.")
    return plans


def collect(out, key, answer_file, model, model_version, source, settings=None):
    """Collect externally produced verbatim output with operator-declared provenance."""
    out = Path(out)
    mapping = load_mapping(out)
    if key not in mapping or not all((model.strip(), model_version.strip(), source.strip())):
        raise ValueError("Known blind_id, model, version and source are required")
    if digest((out / "prompts" / f"{key}.md").read_text(encoding="utf-8")) != mapping[key]["prompt_sha256"]:
        raise ValueError("Prompt changed since preparation")
    answer = Path(answer_file).read_text(encoding="utf-8")
    if not answer.strip():
        raise ValueError("Cannot collect empty output")
    with run_lock(out):
        target = out / "outputs" / f"{key}.txt"
        state_path = out / "states" / f"{key}.json"
        state = read_json(state_path)
        if target.read_text(encoding="utf-8").strip() or state["status"] not in ("pending", "dry_run"):
            raise ValueError("Slot already attempted/populated; use a new experiment")
        target.write_text(answer, encoding="utf-8")
        private_file(target)
        write_json(state_path, {"status": "completed", "source": source, "provenance": "operator-declared, not independently authenticated",
                   "model_requested": model, "model_version_observed": model_version, "settings": settings or {},
                   "output_sha256": digest(answer), "collected_at": now(), "usage": None, "latency_seconds": None,
                   "native_activation": "not_verified"})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("probe")
    p.add_argument("--cli")
    p = sub.add_parser("run")
    p.add_argument("--out", required=True)
    p.add_argument("--cli")
    p.add_argument("--live", action="store_true")
    p.add_argument("--acknowledge-cost", action="store_true")
    p.add_argument("--subscription-only", action="store_true", help="Require existing ChatGPT login and remove API-key env vars from child")
    p.add_argument("--model")
    p.add_argument("--max-runs", type=int, default=1)
    p.add_argument("--timeout", type=float, default=180)
    p.add_argument("--effort", choices=("minimal", "low", "medium", "high", "xhigh"))
    p.add_argument("--id", action="append", dest="ids")
    p = sub.add_parser("collect")
    for name in ("out", "id", "answer-file", "model", "model-version", "source"):
        p.add_argument("--" + name, required=True)
    p.add_argument("--settings-file")
    args = parser.parse_args(argv)
    try:
        if args.command == "probe":
            result = discover(args.cli)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result["available"] else 1
        if args.command == "collect":
            collect(args.out, args.id, args.answer_file, args.model, args.model_version, args.source,
                    read_json(args.settings_file) if args.settings_file else None)
        else:
            results = run(args.out, args.cli, args.live, args.acknowledge_cost, args.model,
                          args.max_runs, args.timeout, args.effort, args.ids, args.subscription_only)
            if any(r["status"] in ("failed", "aborted") for r in results):
                return 1
        return 0
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
