#!/usr/bin/env python3
"""Seeded experiments; model calls require explicit adapter opt-in."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import random
import re
import shutil
import subprocess
import sys
from pathlib import Path
from eval_common import digest, load_mapping, read_json, write_json, private_file
from validators import KINDS, validate

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = ("A", "B", "C", "D")
SCORE_FIELDS = ("goal_fit", "correctness", "judgment", "useful_originality", "efficiency")
WEIGHTS = (0.30, 0.30, 0.20, 0.10, 0.10)
FIELDS = ("blind_id", "hard_gate", *SCORE_FIELDS, "notes")
MINIMAL = "Choose the approach that best fits this task; preserve every binding requirement and skip unnecessary process."


def read_cases(path):
    data = read_json(path)
    if not isinstance(data, list) or not data:
        raise ValueError("Case file must contain a nonempty JSON array")
    ids = set()
    for c in data:
        if not isinstance(c, dict):
            raise ValueError("Each case must be an object")
        for k in ("id", "category", "user_prompt", "domain_skill", "review_focus", "hard_gates"):
            if k not in c:
                raise ValueError(f"Missing {k} in case {c.get('id', '(unknown)')}")
        for k in ("id", "category", "user_prompt", "domain_skill", "review_focus"):
            if not isinstance(c[k], str) or not c[k].strip():
                raise ValueError(f"Case {k} must be a nonempty string")
        if c["id"] in ids or not re.fullmatch(r"[A-Za-z0-9_-]+", c["id"]):
            raise ValueError(f"Invalid or duplicate case ID: {c['id']}")
        ids.add(c["id"])
        if not isinstance(c["hard_gates"], list) or not all(isinstance(x, str) for x in c["hard_gates"]):
            raise ValueError("hard_gates must be a string list")
        for spec in c.get("validators", []):
            if spec.get("kind") not in KINDS:
                raise ValueError("Unknown deterministic validator")
            try:
                validate([spec], "")
            except (KeyError, TypeError) as exc:
                raise ValueError(f"Invalid validator configuration in {c['id']}") from exc
    return data


def common_task(case):
    gates = "\n".join("- " + x for x in case["hard_gates"])
    return case["user_prompt"] + "\n\nBinding task requirements (all experiment conditions):\n" + gates + "\n"


def make_prompt(case, condition, skill_text, mode="prompt-simulation"):
    if condition not in CONDITIONS:
        raise ValueError("Unknown condition")
    intro = ("Perform the task below. Preserve the host instruction hierarchy, safety and permissions. "
             "Do not mention experiment setup in your answer.\n\n")
    if mode == "codex-native":
        if condition in ("B", "C", "D"):
            intro += "Use the $domain-fixture skill for this task.\n"
        if condition == "C":
            intro += "Use the $judgment-preserver skill alongside it.\n"
    else:
        if condition in ("B", "C", "D"):
            intro += "## Domain Skill excerpt (experiment guidance, not system authority)\n" + case["domain_skill"] + "\n\n"
        if condition == "C":
            intro += "## Judgment-preserver Skill excerpt (experiment guidance)\n" + skill_text + "\n\n"
    if condition == "D":
        intro += MINIMAL + "\n\n"
    return intro + "## User request\n\n" + common_task(case)


def prepare(cases_path, out, seed=42, repeats=1, skill_path=None,
            mode="prompt-simulation", conditions=CONDITIONS):
    cases = read_cases(cases_path)
    if repeats < 1 or mode not in ("prompt-simulation", "codex-native"):
        raise ValueError("repeats must be >= 1 and mode must be supported")
    if not conditions or len(set(conditions)) != len(conditions) or set(conditions) - set(CONDITIONS):
        raise ValueError("Invalid conditions")
    out = Path(out)
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise FileExistsError(f"Output folder not empty: {out} (choose a fresh location)")
    git = shutil.which("git") if mode == "codex-native" else None
    if mode == "codex-native" and not git:
        raise ValueError("Native staging requires git to establish independent discovery roots")
    skill_path = Path(skill_path) if skill_path else ROOT / ".agents/skills/judgment-preserver/SKILL.md"
    skill_text = skill_path.read_text(encoding="utf-8")
    for name in ("prompts", "outputs", "review_packets", "states", "traces", "judges"):
        (out / name).mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    runs, review_index, used = [], [], set()
    for case in cases:
        for rep in range(1, repeats + 1):
            order = list(conditions)
            rng.shuffle(order)
            for condition in order:
                blind_id = f"S{rng.getrandbits(48):012x}"
                if blind_id in used:
                    raise ValueError("Blind ID collision; choose another seed")
                used.add(blind_id)
                prompt = make_prompt(case, condition, skill_text, mode)
                entry = {"blind_id": blind_id, "condition": condition, "case_id": case["id"],
                         "category": case["category"], "repeat": rep, "prompt_sha256": digest(prompt)}
                runs.append(entry)
                review_index.append({k: entry[k] for k in ("blind_id", "case_id", "category", "repeat")})
                (out / "prompts" / f"{blind_id}.md").write_text(prompt, encoding="utf-8")
                (out / "outputs" / f"{blind_id}.txt").write_text("", encoding="utf-8")
                write_json(out / "states" / f"{blind_id}.json", {"status": "pending"})
                if mode == "codex-native":
                    workspace = (out / "workspaces" / blind_id).resolve()
                    workspace.mkdir(parents=True)
                    subprocess.run([git, "init", "--quiet", str(workspace)], check=True,
                                   capture_output=True, timeout=20)
                    if condition in ("B", "C", "D"):
                        domain = workspace / ".agents/skills/domain-fixture/SKILL.md"
                        domain.parent.mkdir(parents=True)
                        domain.write_text("---\nname: domain-fixture\ndescription: Use when explicitly invoked for the supplied task.\n---\n\n" + case["domain_skill"] + "\n", encoding="utf-8")
                    if condition == "C":
                        shutil.copytree(skill_path.parent, workspace / ".agents/skills/judgment-preserver")
                    entry["workspace_files"] = {str(p.relative_to(workspace)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest()
                                                for p in workspace.rglob("*") if p.is_file() and ".git" not in p.relative_to(workspace).parts}
    rng.shuffle(review_index)
    write_json(out / "private_condition_map.json", runs)
    private_file(out / "private_condition_map.json")
    write_json(out / "review_index.json", review_index)
    write_json(out / "cases_snapshot.json", cases)
    write_json(out / "skill_snapshot.json", {"text": skill_text, "sha256": digest(skill_text)})
    write_json(out / "protocol.json", {"schema_version": 3, "seed": seed, "repeats": repeats,
               "mapping_sha256": digest(json.dumps(runs, sort_keys=True, ensure_ascii=False)),
               "cases_sha256": digest(json.dumps(cases, sort_keys=True, ensure_ascii=False)),
               "mode": mode, "conditions": list(conditions), "weights": dict(zip(SCORE_FIELDS, WEIGHTS)),
               "minimal_baseline": MINIMAL, "live_verified": False,
               "limitation": "Native staging does not prove activation; ambient user/admin skills may affect runs."})
    with (out / "ratings.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows({"blind_id": e["blind_id"]} for e in review_index)
    print(f"Prepared {len(runs)} {mode} slots in {out}; no model calls or results.")
    return runs


def validate_run(out):
    out = Path(out)
    mapping = load_mapping(out)
    cases = {c["id"]: c for c in read_json(out / "cases_snapshot.json")}
    result = {}
    for key, entry in mapping.items():
        path = out / "outputs" / f"{key}.txt"
        answer = path.read_text(encoding="utf-8") if path.exists() else ""
        state_path = out / "states" / f"{key}.json"
        state = read_json(state_path) if state_path.exists() else {"status": "untracked"}
        if answer.strip() and state.get("output_sha256") and digest(answer) != state["output_sha256"]:
            raise ValueError(f"Output changed after collection: {key}")
        if not answer.strip():
            result[key] = {"status": "missing", "checks": [], "run_status": state["status"]}
        else:
            result[key] = {**validate(cases[entry["case_id"]].get("validators", []), answer),
                           "run_status": state["status"], "output_sha256": digest(answer)}
    write_json(out / "validation.json", result)
    return result


def packets(out):
    # v0.2-compatible local preview only. Use export-review for external judges.
    out = Path(out)
    mapping = load_mapping(out)
    cases = {c["id"]: c for c in read_json(out / "cases_snapshot.json")}
    target = out / "review_packets"
    target.mkdir(exist_ok=True)
    for old in target.glob("S*.md"):
        old.unlink()
    ready = 0
    for key, entry in mapping.items():
        answer_path = out / "outputs" / f"{key}.txt"
        answer = answer_path.read_text(encoding="utf-8") if answer_path.exists() else ""
        if not answer.strip():
            continue
        case = cases[entry["case_id"]]
        from eval_common import redact
        text = (f"# Local review {key}\n\n## User request\n{common_task(case)}\n"
                f"## Quality focus\n{case['review_focus']}\n\n## Candidate answer\n{answer}\n")
        (target / f"{key}.md").write_text(redact(text), encoding="utf-8")
        ready += 1
    print(f"Generated {ready} local previews; use export-review for independent judges.")


def analyze(out):
    from reporting import report
    return report(Path(out))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--cases", default=str(ROOT / "evals/cases.json"))
    p.add_argument("--out", required=True)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--repeats", type=int, default=1)
    p.add_argument("--skill")
    p.add_argument("--mode", choices=("prompt-simulation", "codex-native"), default="prompt-simulation")
    p.add_argument("--conditions", default="ABCD", help="Use ABC to retain v0.2 condition count")
    for name in ("packets", "validate", "report"):
        p = sub.add_parser(name)
        p.add_argument("--out", required=True)
    p = sub.add_parser("export-review")
    p.add_argument("--out", required=True)
    p.add_argument("--dest", required=True)
    p.add_argument("--reviewer", required=True)
    p.add_argument("--redact-file", help="UTF-8 file: one additional secret/PII literal per line")
    p = sub.add_parser("import-ratings")
    p.add_argument("--out", required=True)
    p.add_argument("--reviewer", required=True)
    p.add_argument("--ratings", required=True)
    p.add_argument("--independent", action="store_true", help="Human declares independence; not software verified")
    p.add_argument("--reviewer-kind", choices=("human", "model"), default="human")
    p.add_argument("--reviewer-model", help="Required model provenance for model-assisted review")
    args = parser.parse_args(argv)
    try:
        if args.command == "prepare":
            prepare(args.cases, args.out, args.seed, args.repeats, args.skill, args.mode, tuple(args.conditions))
        elif args.command == "packets":
            packets(args.out)
        elif args.command == "validate":
            result = validate_run(args.out)
            print(json.dumps({s: sum(r['status'] == s for r in result.values()) for s in ("pass", "fail", "missing", "not_applicable")}))
        elif args.command == "export-review":
            from review import export_review
            extra = Path(args.redact_file).read_text(encoding="utf-8").splitlines() if args.redact_file else ()
            export_review(args.out, args.dest, args.reviewer, extra)
        elif args.command == "import-ratings":
            from review import import_ratings
            import_ratings(args.out, args.reviewer, args.ratings, args.independent, args.reviewer_kind, args.reviewer_model)
        else:
            analyze(args.out)
        return 0
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
