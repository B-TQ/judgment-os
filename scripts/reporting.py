"""Descriptive, hard-gate-aware summaries with case-clustered paired analysis."""
import csv
from collections import Counter, defaultdict
import json
import math
from pathlib import Path
import random
import statistics

from eval_common import digest, load_mapping, read_json, redact, write_json
from benchmark import CONDITIONS, FIELDS, SCORE_FIELDS, WEIGHTS, validate_run
from review import parse_scores


def mean(values):
    return statistics.mean(values) if values else None


def interval(case_values, seed=42):
    """Bootstrap independent case clusters, not repeated outputs or judge rows."""
    values = list(case_values)
    if len(values) < 10:
        return None
    rng = random.Random(seed)
    estimates = sorted(statistics.mean(rng.choices(values, k=len(values))) for _ in range(2000))
    return [estimates[49], estimates[1949]]


def load_ratings(out, mapping, validation):
    documents = [read_json(p) for p in sorted((out / "judges").glob("*.ratings.json"))]
    collected, seen = [], set()
    if documents:
        # Never silently combine legacy local rows with independent reviewer data.
        with (out / "ratings.csv").open(encoding="utf-8-sig", newline="") as f:
            if any(row.get("hard_gate", "").strip() for row in csv.DictReader(f)):
                raise ValueError("Mixed legacy/local ratings and imported reviewer data; use one source")
        for doc in documents:
            for row in doc["ratings"]:
                scores = row["scores"]
                raw = {"hard_gate": row["hard_gate"], "notes": row.get("notes", "")}
                raw.update({k: str(scores[i]) if scores else "" for i, k in enumerate(SCORE_FIELDS)})
                parsed = parse_scores(raw)
                collected.append({**parsed, "blind_id": row["blind_id"], "output_sha256": row["output_sha256"],
                                  "reviewer": doc["reviewer"], "independence_declared": doc["independence_declared"],
                                  "reviewer_kind": doc.get("reviewer_kind", "human"), "reviewer_model": doc.get("reviewer_model")})
    else:
        with (out / "ratings.csv").open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != list(FIELDS):
                raise ValueError("Unexpected legacy/local rating columns")
            for row in reader:
                key = row.get("blind_id", "").strip()
                if key not in mapping or key in seen or None in row or any(v is None for v in row.values()):
                    raise ValueError("Unknown/duplicate blind_id or malformed local rating row")
                seen.add(key)
                parsed = parse_scores(row)
                if parsed:
                    collected.append({**parsed, "blind_id": key, "reviewer": "local-unblinded",
                                      "independence_declared": False, "reviewer_kind": "human", "reviewer_model": None})
    seen.clear()
    for row in collected:
        key = row["blind_id"]
        pair = (row["reviewer"], key)
        if key not in mapping or pair in seen:
            raise ValueError("Unknown/duplicate judge-output rating")
        seen.add(pair)
        answer_path = out / "outputs" / f"{key}.txt"
        answer = answer_path.read_text(encoding="utf-8") if answer_path.exists() else ""
        if not answer.strip():
            raise ValueError(f"Rated output is missing: {key}")
        if row.get("output_sha256") and row["output_sha256"] != digest(answer):
            raise ValueError(f"Rated output changed: {key}")
        if row["hard_gate"] == "pass" and validation[key]["status"] == "fail":
            raise ValueError(f"Human pass contradicts deterministic failure: {key}")
        row["output_sha256"] = digest(answer)
        row["quality"] = sum(w * x for w, x in zip(WEIGHTS, row["scores"])) if row["scores"] else None
    return collected


def report(out):
    out = Path(out)
    mapping = load_mapping(out)
    protocol = read_json(out / "protocol.json")
    validation = validate_run(out)
    ratings = load_ratings(out, mapping, validation)
    if not ratings:
        raise ValueError("No ratings yet: populate ratings.csv or import independent human judgments")
    votes = defaultdict(list)
    for row in ratings:
        votes[row["blind_id"]].append(row)
    aggregated = {}
    for key, rows in votes.items():
        passed = all(r["hard_gate"] == "pass" for r in rows)
        aggregated[key] = {**mapping[key], "pass": passed, "judges": len(rows),
                           "disagreement": len({r["hard_gate"] for r in rows}) > 1,
                           "quality": mean([r["quality"] for r in rows]) if passed else None}
    states = {}
    for key in mapping:
        p = out / "states" / f"{key}.json"
        states[key] = read_json(p) if p.exists() else {"status": "untracked"}

    def summarize(keys):
        rows = [aggregated[k] for k in keys if k in aggregated]
        passed = [x for x in rows if x["pass"]]
        latencies = [states[k]["latency_seconds"] for k in keys
                     if isinstance(states[k].get("latency_seconds"), (int, float))
                     and math.isfinite(states[k]["latency_seconds"]) and states[k]["latency_seconds"] >= 0]
        usages = [states[k]["usage"] for k in keys if isinstance(states[k].get("usage"), dict)]
        tokens = Counter()
        for usage in usages:
            tokens.update({k: v for k, v in usage.items() if type(v) is int and v >= 0})
        return {"expected": len(keys), "outputs": sum(validation[k]["status"] != "missing" for k in keys),
                "rated": len(rows), "unrated": len(keys) - len(rows), "hard_gate_pass": len(passed),
                "hard_gate_fail": len(rows) - len(passed), "pass_rate": len(passed) / len(rows) if rows else None,
                "quality_on_pass": mean([r["quality"] for r in passed]),
                "judge_disagreements": sum(r["disagreement"] for r in rows),
                "deterministic_failures": sum(validation[k]["status"] == "fail" for k in keys),
                "measured_latency_slots": len(latencies), "mean_measured_latency_seconds": mean(latencies),
                "usage_reporting_slots": len(usages), "reported_usage_totals": dict(tokens) if usages else None,
                "run_statuses": dict(Counter(states[k]["status"] for k in keys))}

    conditions = protocol.get("conditions", list(CONDITIONS))
    summary = {c: summarize([k for k, v in mapping.items() if v["condition"] == c]) for c in conditions}
    categories = sorted({v["category"] for v in mapping.values()})
    classes = {cls: {c: summarize([k for k, v in mapping.items() if v["condition"] == c and v["category"] == cls])
                     for c in conditions} for cls in categories}
    by_pair = {(v["case_id"], v["repeat"], v["condition"]): v for v in aggregated.values()}
    paired = []
    for left, right in (("C", "B"), ("D", "B"), ("C", "D")):
        for scope in ("all", "open", "control"):
            gate, quality = defaultdict(list), defaultdict(list)
            mismatches, unverified = 0, 0
            for (case, rep, condition), value in by_pair.items():
                if condition != left or scope != "all" and not value["category"].startswith(scope):
                    continue
                other = by_pair.get((case, rep, right))
                if other is None:
                    continue
                a, b = states[value["blind_id"]], states[other["blind_id"]]
                profile_fields = ("model_requested", "model_version_observed", "settings", "cli_version")
                if any(a.get(k) and b.get(k) and a[k] != b[k] for k in profile_fields):
                    mismatches += 1
                    continue
                if not all(a.get(k) and b.get(k) for k in ("model_requested", "model_version_observed", "settings")):
                    unverified += 1
                gate[case].append(int(value["pass"]) - int(other["pass"]))
                if value["pass"] and other["pass"]:
                    quality[case].append(value["quality"] - other["quality"])
            for metric, xs in (("hard_gate_pass_delta", gate), ("quality_on_both_pass_delta", quality)):
                case_means = [statistics.mean(x) for x in xs.values()]
                paired.append({"comparison": f"{left}-{right}", "scope": scope, "metric": metric,
                               "matched_outputs": sum(map(len, xs.values())), "case_clusters": len(xs),
                               "excluded_profile_mismatches": mismatches, "metadata_unverified_pairs": unverified,
                               "mean_delta": mean(case_means), "bootstrap_95_interval": interval(case_means) if not unverified else None,
                               "interval_rule": "2000 seeded case-cluster resamples; suppressed below 10 distinct cases or with unverified model/version/settings"})
    failures = [{"blind_id": k, "case_id": v["case_id"], "condition": v["condition"],
                 "checks": validation[k]["checks"], "notes": [r["notes"] for r in votes[k]]}
                for k, v in aggregated.items() if not v["pass"]]
    profiles = Counter(json.dumps({k: s.get(k) for k in ("source", "model_requested", "model_version_observed", "cli_version", "settings")}, sort_keys=True)
                       for s in states.values() if s["status"] == "completed")
    evidence = [{"profile": json.loads(p), "slots": n} for p, n in sorted(profiles.items())]
    reviewers = {r["reviewer"]: {"independence_declared": r["independence_declared"], "verified": False,
                                "kind": r["reviewer_kind"], "model": r["reviewer_model"]} for r in ratings}
    result = {"schema_version": 3, "mode": protocol["mode"], "conditions": summary,
              "task_classes": classes, "paired": paired, "failures": failures,
              "reviewers": reviewers, "rating_rows": len(ratings), "rated_outputs": len(aggregated),
              "gate_scope": "output_text_only", "behavioral_compliance_established": False,
              "execution_profiles": evidence, "missing_outputs": [k for k in mapping if validation[k]["status"] == "missing"],
              "unrated_outputs": [k for k in mapping if k not in aggregated],
              "input_fingerprints": {"protocol": digest(json.dumps(protocol, sort_keys=True)),
                  "ratings": digest(json.dumps(ratings, sort_keys=True)),
                  "mapping": digest(json.dumps(mapping, sort_keys=True))},
              "empirical_claim": "No causal or performance-improvement claim; data authenticity and human reviewer independence are not software-verifiable."}
    write_json(out / "report.json", result)
    fmt = lambda x: "n/a" if x is None else f"{x:.2f}"
    review_label = "Human ratings only" if all(r["reviewer_kind"] == "human" for r in ratings) else "Includes model-assisted ratings; no independent human evidence established"
    lines = ["# Judgment OS v0.4 — descriptive report", "", f"**{review_label}.** No causal claims or proven performance lift.",
             "", "Gate scope: output text only. No-browsing/no-sending/no-file-write behavior is not established by answer packets.",
             "", f"Mode: {protocol['mode']}. Rating rows: {len(ratings)}; distinct rated outputs: {len(aggregated)}.",
             "", "## Overall", "", "| Condition | Expected | Outputs | Rated | Hard-gate pass | Fail | Quality on passes |",
             "|---|---:|---:|---:|---:|---:|---:|"]
    for c, s in summary.items():
        lines.append(f"| {c} | {s['expected']} | {s['outputs']} | {s['rated']} | {s['hard_gate_pass']} | {s['hard_gate_fail']} | {fmt(s['quality_on_pass'])}/5 |")
    lines += ["", "A: no domain Skill. B: domain Skill. C: domain + Judgment Preserver. D: domain + minimal task-fit reminder.",
              "", "Pass rates use rated outputs only. Missing, pending, aborted, failed, dry-run and unreviewed slots are disclosed separately, with no imputed quality scores.",
              "", "## By task class", "", "| Class | Condition | Expected | Rated | Pass | Quality on passes |",
              "|---|---|---:|---:|---:|---:|"]
    for cls, groups in classes.items():
        for c, s in groups.items():
            lines.append(f"| {cls} | {c} | {s['expected']} | {s['rated']} | {s['hard_gate_pass']} | {fmt(s['quality_on_pass'])} |")
    lines += ["", "## Paired analysis", "", "Each case is weighted equally after averaging its matched repeats. Quality pairs require both outputs to pass.",
              "", "| Comparison | Scope | Metric | Matches | Distinct cases | Delta | 95% interval |", "|---|---|---|---:|---:|---:|---|"]
    for p in paired:
        ci = p["bootstrap_95_interval"]
        ci_text = f"[{ci[0]:.3f}, {ci[1]:.3f}]" if ci else "suppressed: sample size or unknown metadata"
        lines.append(f"| {p['comparison']} | {p['scope']} | {p['metric']} | {p['matched_outputs']} | {p['case_clusters']} | {fmt(p['mean_delta'])} | {ci_text} |")
    lines += ["", "## Failure cases", ""]
    lines += [f"- {f['blind_id']} ({f['case_id']}, {f['condition']}): " +
              redact("; ".join(f["notes"]) or "gate failed; no reviewer explanation supplied").replace("\n", " ") for f in failures]
    if not failures:
        lines.append("No failed gates among rated outputs; this says nothing about unrated outputs.")
    lines += ["", "## Run states and reviewer declarations", "", "```json", json.dumps({"states": {c: s["run_statuses"] for c, s in summary.items()}, "reviewers": reviewers}, indent=2), "```",
              "", "## Interpretation limits", "", "- Imported judges are averaged per output; any gate failure fails that output. Disagreements are retained in report.json.",
              "- Local ratings.csv is unblinded and independence is not established. Imported independence is only an operator declaration.",
              "- Deterministic validators cover declared text properties, not all safety, correctness or aesthetics.",
              "- Reports use complete observed pairs; selective missingness and pass-only quality can bias comparisons.",
              "- Bootstrap intervals are descriptive, case-clustered, and not causal proof. Hand-authored cases are not a random population sample.",
              "- Different models/settings, unknown versions, ambient skills and unsuccessful activation invalidate strong attribution; inspect execution_profiles in report.json.",
              "- Known profile mismatches are excluded from paired deltas. Unknown model/version/settings keep exploratory deltas but suppress intervals; counts are in report.json.",
              "- Native staging/command completion does not prove Skill discovery or activation. Live traces require human inspection.",
              "- Token usage and latency are only recorded when actually measured; no estimated usage is invented.",
              "- This private report reveals treatments. Do not give it to blind reviewers or publish the experiment directory.", ""]
    path = out / "report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {path} from {len(aggregated)} rated outputs; {len(mapping) - len(aggregated)} slots unrated.")
    return path
