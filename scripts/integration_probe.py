#!/usr/bin/env python3
"""Native Skill-body access probe, separate from behavioral efficacy evaluation."""
import argparse
import json
from pathlib import Path
import secrets
import shutil
import sys

from benchmark import ROOT, prepare
from codex_adapter import run
from eval_common import digest, read_json, write_json


def stage(out):
    out = Path(out)
    if out.exists():
        raise FileExistsError("Use a fresh integration-probe directory")
    material = out / "probe-material"
    material.mkdir(parents=True)
    codes = {name: secrets.token_hex(12) for name in ("domain-fixture", "judgment-preserver")}
    core = ROOT / ".agents/skills/judgment-preserver"
    target = material / "judgment-preserver"
    shutil.copytree(core, target)
    original = (target / "SKILL.md").read_text(encoding="utf-8")
    text = original + "\n\n## Integration probe only\nThe judgment-preserver verification code is " + codes["judgment-preserver"] + ". Return it exactly when asked for the verification code.\n"
    (target / "SKILL.md").write_text(text, encoding="utf-8")
    case = {"id": "P01", "category": "integration_probe", "user_prompt":
            "Use both explicitly named Skills. Return a JSON object mapping each named skill to its verification code found only inside its body. If a body is unavailable, return UNAVAILABLE for that entry. Do not inspect other directories.",
            "domain_skill": "# Domain Integration Probe\nThe domain-fixture verification code is " + codes["domain-fixture"] + ". Return it exactly when asked for the verification code.",
            "review_focus": "Skill-body accessibility only, not effectiveness.", "hard_gates": ["Return only a JSON object."], "validators": []}
    write_json(material / "cases.json", [case])
    rows = prepare(material / "cases.json", out / "run", mode="codex-native", conditions=("C",), skill_path=target / "SKILL.md")
    prompt = (out / "run/prompts" / f"{rows[0]['blind_id']}.md").read_text(encoding="utf-8")
    if any(code in prompt for code in codes.values()):
        raise ValueError("Probe codes leaked into generation prompt")
    write_json(out / "expected_codes.json", {"codes": codes, "core_skill_sha256": digest(original),
               "probe_skill_sha256": digest(text), "prompt_contains_codes": False})
    return rows[0]["blind_id"]


def probe(out, cli=None, live=False, model=None, acknowledge_cost=False, subscription_only=False):
    out = Path(out)
    key = stage(out)
    states = run(out / "run", cli=cli, live=live, acknowledge_cost=acknowledge_cost, model=model,
                 max_runs=1, timeout=90, effort="low", subscription_only=subscription_only)
    answer = (out / "run/outputs" / f"{key}.txt").read_text(encoding="utf-8")
    try:
        value = json.loads(answer) if answer.strip() else None
    except ValueError:
        value = None
    result = {"probe_status": states[0]["status"], "body_access_verified": value == read_json(out / "expected_codes.json")["codes"],
              "modified_probe_skill": True, "prompt_contains_codes": False,
              "interpretation": "Matching unpredictable body-only codes establishes body access in this probe; it does not establish original-skill efficacy, full compliance or host isolation."}
    write_json(out / "probe_result.json", result)
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    parser.add_argument("--cli")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--model")
    parser.add_argument("--acknowledge-cost", action="store_true")
    parser.add_argument("--subscription-only", action="store_true")
    args = parser.parse_args()
    try:
        result = probe(args.out, args.cli, args.live, args.model, args.acknowledge_cost, args.subscription_only)
        if args.live and not result["body_access_verified"]:
            sys.exit(1)
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
