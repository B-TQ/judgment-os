#!/usr/bin/env python3
"""Judgment OS: local, dependency-free entry point. No model calls by default."""
import argparse
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))


def doctor():
    return {"version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
            "python_supported": sys.version_info >= (3, 11),
            "python": sys.version.split()[0], "offline_ready": sys.version_info >= (3, 11),
            "git_available": shutil.which("git") is not None,
            "codex_on_path": shutil.which("codex") is not None or shutil.which("codex.exe") is not None,
            "live_authentication": "not checked; no account or credential reads",
            "model_calls": 0}


def tutorial(out, native=False):
    from benchmark import prepare
    from eval_common import write_json
    from validators import validate
    out = Path(out).resolve()
    if out.exists():
        raise FileExistsError("Choose a fresh tutorial directory")
    cases_path = ROOT / "examples/quickstart/cases.json"
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    checks = {}
    for name in ("correct", "incorrect"):
        answer = (ROOT / f"examples/quickstart/{name}.json").read_text(encoding="utf-8")
        checks[name] = validate(cases[0]["validators"], answer)["status"]
    assert checks == {"correct": "pass", "incorrect": "fail"}
    rows = prepare(cases_path, out / "study", seed=42, repeats=1,
                   mode="codex-native" if native else "prompt-simulation")
    summary = {"kind": "offline_tutorial_not_method_evidence", "model_calls": 0,
               "candidate_answers": 0, "ratings": 0, "prepared_slots": len(rows),
               "bundled_software_fixture_checks": checks,
               "next": "Run 'python judgment.py run --out STUDY --max-runs 1' for a dry-run plan. Live execution requires explicit flags and your own authorization."}
    write_json(out / "demo_summary.json", summary)
    (out / "START_HERE.md").write_text(
        "# Offline tutorial\n\nThese two bundled answers are software fixtures, not model outputs. "
        "The correct fixture passes and the incorrect fixture fails. The study contains eight empty A/B/C/D slots. "
        "No model answers or ratings were fabricated. No model or account was contacted.\n\n"
        "From the repository root, use `python judgment.py run --out \"" + str(out / "study") +
        "\" --max-runs 1` to inspect a dry-run plan. See docs/QUICKSTART.md for genuine collection and review.\n",
        encoding="utf-8")
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, epilog="Python 3.11+. Source checkout only; no pip install or API key needed for offline use.")
    parser.add_argument("--version", action="version", version=(ROOT / "VERSION").read_text(encoding="utf-8").strip())
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="Check local prerequisites without reading credentials or calling a model")
    p = sub.add_parser("demo", help="Run the small offline tutorial; no generated answers or ratings")
    p.add_argument("--out", required=True)
    p.add_argument("--native", action="store_true", help="Also stage native Skill files; requires Git")
    p = sub.add_parser("check", help="Check one answer against a case's declared deterministic properties")
    p.add_argument("--cases", default=str(ROOT / "examples/quickstart/cases.json"))
    p.add_argument("--case", required=True)
    p.add_argument("--answer", required=True)
    p = sub.add_parser("skill", help="Install/uninstall the unchanged optional project Skill")
    p.add_argument("action", choices=("install", "uninstall"))
    p.add_argument("--project", required=True)
    p.add_argument("--dry-run", action="store_true")
    routes = {"prepare": ("benchmark", "prepare"), "run": ("codex_adapter", "run"),
              "collect": ("codex_adapter", "collect"), "validate": ("benchmark", "validate"),
              "review": ("paired_review", None), "report": ("paired_review", "report"),
              "selftest": ("demo", None), "release": ("release", None)}
    for name in routes:
        sub.add_parser(name, add_help=False, help={"prepare": "Freeze case/condition inputs into a new study",
            "run": "Plan adapter calls (dry-run by default)", "collect": "Import a verbatim externally generated answer with provenance",
            "validate": "Validate actual study outputs", "review": "Export/import same-task model review",
            "report": "Report an explicit reviewer phase", "selftest": "Run the larger offline pipeline smoke test",
            "release": "Verify or package allowlisted source"}[name])
    args, remainder = parser.parse_known_args(argv)
    if args.command in routes:
        import importlib
        module_name, prefix = routes[args.command]
        is_report = args.command == "report" or (args.command == "review" and remainder[:1] == ["report"])
        if is_report and not any(x in ("--help", "-h") for x in remainder):
            if "--all-reviewers" in remainder:
                remainder.remove("--all-reviewers")
            elif not any(x == "--reviewer" or x.startswith("--reviewer=") for x in remainder):
                raise ValueError("Select a review phase with --reviewer ID (repeat as needed), or explicitly choose --all-reviewers")
        module = importlib.import_module(module_name)
        return module.main(([prefix] if prefix else []) + remainder)
    if remainder:
        parser.error("unrecognized arguments: " + " ".join(remainder))
    if args.command == "doctor":
        result = doctor()
    elif args.command == "demo":
        result = tutorial(args.out, args.native)
    elif args.command == "check":
        from benchmark import read_cases
        from validators import validate
        cases = {c["id"]: c for c in read_cases(args.cases)}
        if args.case not in cases:
            raise ValueError("Unknown case ID")
        result = validate(cases[args.case].get("validators", []), Path(args.answer).read_text(encoding="utf-8"))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "pass" else (1 if result["status"] == "fail" else 2)
    else:
        from skill_install import install, uninstall
        result = (install if args.action == "install" else uninstall)(ROOT, args.project, args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
