#!/usr/bin/env python3
"""Reproducible offline smoke demo. Never generates candidate answers or ratings."""
import argparse
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import shutil
import sys

from benchmark import ROOT, analyze, prepare, validate_run
from codex_adapter import run
from eval_common import read_json, write_json


def demo(out, cli=None):
    out = Path(out)
    if out.exists():
        raise FileExistsError("Choose a new demo directory")
    out.mkdir(parents=True)
    summary = {"kind": "offline software smoke demonstration", "model_calls": 0,
               "candidate_answers": 0, "human_ratings": 0, "performance_claim": None, "modes": {}}
    modes = ["prompt-simulation"] + (["codex-native"] if shutil.which("git") else [])
    with (out / "demo.log").open("w", encoding="utf-8") as log, redirect_stdout(log):
        for mode in modes:
            target = out / mode
            rows = prepare(ROOT / "evals/cases.json", target, seed=42, repeats=1, mode=mode)
            plans = run(target, cli=cli, live=False, max_runs=len(rows))
            result = validate_run(target)
            try:
                analyze(target)
                raise AssertionError("Empty ratings unexpectedly produced a report")
            except ValueError as exc:
                if "No ratings yet" not in str(exc):
                    raise
                print("Expected report refusal:", exc)
            answers = [p for p in (target / "outputs").glob("*.txt") if p.read_text(encoding="utf-8").strip()]
            if answers or any(x["status"] != "dry_run" for x in plans):
                raise AssertionError("Dry-run must not create model responses")
            summary["modes"][mode] = {"slots": len(rows), "dry_run_plans": len(plans),
                                      "missing_outputs": sum(x["status"] == "missing" for x in result.values()),
                                      "empty_report_refused": True, "cli_probe": read_json(target / "cli_probe.json")}
    if "codex-native" not in modes:
        summary["native_staging_blocker"] = "git unavailable"
    write_json(out / "demo_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    parser.add_argument("--cli")
    args = parser.parse_args()
    try:
        demo(args.out, args.cli)
    except (ValueError, OSError, AssertionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
