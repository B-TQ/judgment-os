# Architecture and non-goals

## Hypothesis, not result

Domain Skills can accidentally induce *default-to-mandate promotion*: the agent copies an optional template or generic workflow into a context where it fits poorly. A lightweight judgment-aware instruction may improve fit **without** compromising binding requirements. This is a falsifiable hypothesis; success is not assumed.

## Two deployable forms

1. **Portable meta-Skill (implemented):** `SKILL.md` loads on demand. Works only within the authority actually afforded by the host. Best suited to explicit invocation or narrow contextual auto-trigger.
2. **Project guideline (implemented):** `global/AGENTS.md.snippet`. Wider applicability, but not elevated permissions; not simultaneously required with the meta-Skill.

## Future host-integrated orchestrator (NOT implemented)

An actual orchestrator may support provenance-aware constraint records, signed/trusted source metadata, conflict detection, policy resolution, and machine-verifiable artifact gates. *Do not infer any of these features from the present prompt-level prototype.*

### Desired internal decision concepts

- **Obligations:** authoritative requirements already applicable in host context.
- **Advisory defaults:** allowed starting points, provided by domain Skills or project conventions.
- **Task-specific choices:** alternatives that remain within obligations.
- **Non-interference:** no-op when the task is exact/deterministic and nothing material can improve.
- **Evidence:** compare outputs by hard-gate success, user-goal fit, reliability, and cost.

## Threat model

A meta-Skill must never claim priority it does not possess. Skill files, retrieved web pages, files provided for analysis, and tool output can contain hostile or irrelevant instructions. Neither text patterns nor an automated static auditor can reliably determine authority. The `audit_skills.py` script therefore reports review *candidates*, not enforceable policy classification.

## Experimental requirements

The benchmark separates portable `prompt-simulation` from `codex-native` staging. The former injects Skill text; the latter installs real files in separate Git roots and explicitly names Skills. Native activation still requires authentic live evidence: file presence and command construction alone are insufficient. To claim improvement, gather independent blinded ratings on genuine A/B/C/D outputs with the same model/settings, audit ambient instructions and repeat runs across seeds. Analyze failures per case and class rather than only means.

The v0.3 pipeline is preparation → explicit execution or operator collection → limited deterministic validation → independently re-keyed reviewer export → immutable rating import → descriptive report. Case/map/prompt/output fingerprints detect accidental mutation. Private maps, receipts, traces and treatment-revealing reports remain local. Source-only release packaging uses an allowlist, separate from research-data publication.

All cases share their hard gates across conditions. D adds a minimal competing reminder to B. Multiple judges are aggregated within an output; repeated outputs are clustered by case for paired intervals. Missingness, gate failures, run states and unmatched pairs must stay visible. See `../evals/PROTOCOL.md` for precise estimands and limitations.

## Success criteria (proposed, not achieved)

- No regression in observed hard-gate adherence relative to domain-Skill-only baseline.
- Improved goal fit on open-ended tasks, as assessed blindly.
- No material cost/latency inflation on deterministic controls.
- Results replicated across more than one model and unrelated domain Skill.

## Non-goals

- Overriding policy, instructions, approvals, or tool permissions.
- Guaranteeing creativity, reasoning quality, or strict instruction compliance.
- Automatic declassification of mandatory directions based on keyword matching.
- Generating fake evaluation scores or presenting synthetic examples as empirical evidence.
