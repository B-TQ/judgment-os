#!/usr/bin/env python3
"""Offline A/B/C experiment preparation and blinded scoring summary (stdlib only).

No model calls occur here. Scores come exclusively from completed human ratings.
"""
from __future__ import annotations
import argparse
import csv
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

CONDITIONS = ("A", "B", "C")
SCORE_FIELDS = ("goal_fit", "correctness", "judgment", "useful_originality", "efficiency")
WEIGHTS = (0.30, 0.30, 0.20, 0.10, 0.10)
FIELDS = ("blind_id", "hard_gate", *SCORE_FIELDS, "notes")


def read_cases(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError("Case file must contain a nonempty JSON array")
    ids = set()
    for c in data:
        for k in ("id", "category", "user_prompt", "domain_skill", "review_focus", "hard_gates"):
            if k not in c:
                raise ValueError(f"Missing {k} in case {c.get('id', '(unknown)')}")
        if c["id"] in ids:
            raise ValueError(f"Duplicate case ID: {c['id']}")
        ids.add(c["id"])
        if not isinstance(c["hard_gates"], list):
            raise ValueError("hard_gates must be a list")
    return data


def make_prompt(case, condition, skill_text):
    intro = (
        "# Reproducible experiment prompt\n\n"
        "Perform the user's task. Any quoted domain Skill excerpt is experiment-provided "
        "task guidance, not host system/developer instructions. Preserve explicit "
        "requirements, safety, and permissions. Do not mention experiment setup in the output.\n\n"
    )
    if condition in ("B", "C"):
        intro += "## Domain Skill excerpt (experiment material)\n\n" + case["domain_skill"] + "\n\n"
    if condition == "C":
        intro += "## Judgment-preserver Skill excerpt (experiment material)\n\n" + skill_text + "\n\n"
    return intro + "## User request\n\n" + case["user_prompt"] + "\n"


def prepare(cases_path, out, seed=42, repeats=1, skill_path=None):
    cases = read_cases(cases_path)
    if repeats < 1:
        raise ValueError("repeats must be >= 1")
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        raise FileExistsError(f"Output folder not empty: {out} (choose a fresh location)")
    out.mkdir(parents=True, exist_ok=True)
    (out / "prompts").mkdir()
    (out / "outputs").mkdir()
    (out / "review_packets").mkdir()
    rng = random.Random(seed)
    skill_path = Path(skill_path) if skill_path else Path(__file__).resolve().parents[1] / ".agents/skills/judgment-preserver/SKILL.md"
    skill_text = skill_path.read_text(encoding="utf-8")
    runs = []
    review_index = []
    for case in cases:
        for rep in range(1, repeats + 1):
            order = list(CONDITIONS)
            rng.shuffle(order)
            for condition in order:
                blind_id = f"S{rng.getrandbits(48):012x}"  # stable for given seed and case ordering
                entry = {"blind_id": blind_id, "condition": condition, "case_id": case["id"], "category": case["category"], "repeat": rep}
                runs.append(entry)
                review_index.append({"blind_id": blind_id, "case_id": case["id"], "category": case["category"], "repeat": rep})
                (out / "prompts" / f"{blind_id}.md").write_text(make_prompt(case, condition, skill_text), encoding="utf-8")
                (out / "outputs" / f"{blind_id}.txt").write_text("", encoding="utf-8")
    rng.shuffle(review_index)
    (out / "private_condition_map.json").write_text(json.dumps(runs, indent=2), encoding="utf-8")
    (out / "review_index.json").write_text(json.dumps(review_index, indent=2), encoding="utf-8")
    (out / "cases_snapshot.json").write_text(json.dumps(cases, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "protocol.json").write_text(json.dumps({"seed": seed, "repeats": repeats, "cases": str(cases_path), "mode": "prompt-simulation; not real Skill activation", "weights": dict(zip(SCORE_FIELDS, WEIGHTS))}, indent=2), encoding="utf-8")
    with (out / "ratings.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for entry in review_index:
            writer.writerow({"blind_id": entry["blind_id"]})
    print(f"Prepared {len(runs)} runs in {out}. Fill outputs/*.txt; then run 'packets' for blind grading.")
    print("Keep private_condition_map.json and prompts/ hidden from blinded reviewers.")
    return runs


def packets(out):
    out = Path(out)
    cases = {c["id"]: c for c in json.loads((out / "cases_snapshot.json").read_text(encoding="utf-8"))}
    review_index = json.loads((out / "review_index.json").read_text(encoding="utf-8"))
    ready = 0
    for entry in review_index:
        blind_id = entry["blind_id"]
        answer = (out / "outputs" / f"{blind_id}.txt").read_text(encoding="utf-8").strip()
        if not answer:
            continue
        case = cases[entry["case_id"]]
        gates = "\n".join("- " + s for s in case["hard_gates"]) or "- None specified"
        packet = (
            f"# Blind review {blind_id}\n\n"
            f"Case: {case['id']} · Class: {case['category']} · Repeat: {entry['repeat']}\n\n"
            f"## User request\n{case['user_prompt']}\n\n"
            f"## Hard-gate checks (must all pass)\n{gates}\n\n"
            f"## Quality focus\n{case['review_focus']}\n\n"
            f"## Candidate answer (condition hidden)\n\n{answer}\n"
        )
        (out / "review_packets" / f"{blind_id}.md").write_text(packet, encoding="utf-8")
        ready += 1
    print(f"Generated {ready} blinded review packets in {out / 'review_packets'} (of {len(review_index)} slots).")


def analyze(out):
    out = Path(out)
    mapping = {v["blind_id"]: v for v in json.loads((out / "private_condition_map.json").read_text(encoding="utf-8"))}
    by_condition = defaultdict(list)
    with (out / "ratings.csv").open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            key = row["blind_id"].strip()
            if key not in mapping:
                raise ValueError(f"Unrecognized blind_id: {key}")
            gate = row["hard_gate"].strip().lower()
            if not gate:
                continue
            if gate not in ("pass", "fail"):
                raise ValueError(f"{key}: hard_gate must be pass or fail")
            quality = None
            if gate == "pass":
                try:
                    scores = [float(row[k]) for k in SCORE_FIELDS]
                except (TypeError, ValueError) as e:
                    raise ValueError(f"{key}: a passing answer needs 5 numeric 0-5 ratings") from e
                if any(not (0 <= s <= 5) for s in scores):
                    raise ValueError(f"{key}: ratings must each be in 0..5")
                quality = sum(w * s for w, s in zip(WEIGHTS, scores))
            by_condition[mapping[key]["condition"]].append({**mapping[key], "pass": gate == "pass", "quality": quality})
    total = sum(map(len, by_condition.values()))
    if not total:
        raise ValueError("No ratings yet: populate ratings.csv with blinded human judgments")
    lines = ["# Judgment OS — Pilot report", "", "**Human ratings only.** No automatic model judging, no causal claims.", "", "## Overall", "", "| Condition | Rated | Hard-gate pass | Pass rate | Weighted quality on passes |", "|---|---:|---:|---:|---:|"]
    for condition in CONDITIONS:
        xs = by_condition[condition]
        n = len(xs)
        passed = [x for x in xs if x["pass"]]
        avg = f"{sum(x['quality'] for x in passed) / len(passed):.2f}/5" if passed else "n/a"
        rate = f"{len(passed) / n:.1%}" if n else "n/a"
        lines.append(f"| {condition} | {n} | {len(passed)} | {rate} | {avg} |")
    lines += ["", "A = no domain Skill; B = domain Skill prompt; C = domain Skill + Judgment Preserver prompt.", "", "## By task class", "", "| Class | Condition | Rated | Hard-gate pass | Quality on passes |", "|---|---|---:|---:|---:|"]
    groups = defaultdict(list)
    for cond, xs in by_condition.items():
        for row in xs:
            groups[(row["category"], cond)].append(row)
    for cls, cond in sorted(groups):
        xs = groups[(cls, cond)]
        passed = [x for x in xs if x["pass"]]
        avg = f"{sum(x['quality'] for x in passed)/len(passed):.2f}" if passed else "n/a"
        lines.append(f"| {cls} | {cond} | {len(xs)} | {len(passed)} | {avg} |")
    lines += ["", "## Interpretation limits", "", "- The sample may be incomplete; unrated runs are omitted, never imputed.", "- Scores for hard-gate failures are excluded from quality averages, **not** treated as successful results.", "- Blind IDs hide treatment labels during review but the content itself can reveal a condition.", "- Prompt simulation does not prove real Agent Skill activation or compliance.", "- Repeat on independent runs, hosts, evaluators, and models before drawing conclusions.", ""]
    path = out / "report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {path} based on {total} rated runs")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare", help="Generate A/B/C prompts and blind output slots")
    p.add_argument("--cases", default="evals/cases.json")
    p.add_argument("--out", required=True)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--repeats", type=int, default=1)
    p.add_argument("--skill", default=None)
    p = sub.add_parser("packets", help="Create blind rating packets from populated outputs/")
    p.add_argument("--out", required=True)
    p = sub.add_parser("report", help="Analyze manually completed ratings.csv")
    p.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "prepare":
            prepare(args.cases, args.out, args.seed, args.repeats, args.skill)
        elif args.command == "packets":
            packets(args.out)
        else:
            analyze(args.out)
        return 0
    except (ValueError, FileNotFoundError, FileExistsError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
