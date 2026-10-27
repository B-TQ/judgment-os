# Judgment OS

**Skills should extend an agent's expertise — not replace its judgment.**

**Version:** v0.2 experimental prototype · **Status:** not benchmarked / no proven performance lift

Judgment OS explores how AI agents can use domain-specific Skills without confusing optional examples, recommended workflows, and aesthetic defaults with requirements that apply universally. It aims to preserve **useful discretion within binding constraints**, not to relax safety, permissions, strict formats, or the user's explicit instructions.

> **Important:** The current release is a prompt-level Agent Skill plus offline testing utilities. It is **not** a privileged policy engine or a runtime Skill orchestrator. It cannot override the host's instruction hierarchy.

## Quick start (Codex)

Copy `.agents/skills/judgment-preserver/` into the same location in your project or into `~/.agents/skills/judgment-preserver/` for user-level use. Codex can discover local skills at these paths. For targeted use, explicitly mention `$judgment-preserver` alongside the relevant domain Skill on a task where optional templates or workflow defaults are likely to dominate a better solution. See official docs: <https://learn.chatgpt.com/docs/build-skills>.

For general project-level guidance, optionally paste `global/AGENTS.md.snippet` into your project's `AGENTS.md`. You do not need both deployment styles at once; compare them separately in experiments.

For other hosts, inspect that host's Skill loading and priority rules before claiming compatibility.

## What changed in v0.2

| Area | v0.1 | v0.2 |
|---|---|---|
| Judgment behavior | Broad principles | Minimum-intervention / no-op policy, explicit provenance boundaries |
| Conflict handling | Described in prose | Illustrative decision-boundary reference, no false authority claims |
| Skill inspection | None | Dependency-free metadata check + **advisory** wording review |
| Evaluations | 14 manual cases | 16 JSON cases (8 open / 8 strict controls), seeded A/B/C prompt generator |
| Human reviewing | Manual outline | Blind response slots, packet generation, CSV rubric, hard-gate-aware report |
| Project hygiene | Minimal files | Unit tests, GitHub Actions workflow, license, roadmap, Codex follow-on brief |

No empirical increase in originality, instruction following, or task success has been measured by this package.

## Fastest verification

Requires Python 3.11+, standard library only.

```bash
python -m unittest discover -s tests -v
python scripts/audit_skills.py .agents/skills/judgment-preserver/SKILL.md --strict-metadata
python scripts/benchmark.py prepare --out runs/pilot --seed 42 --repeats 1
```

Do not confuse passing **software tests** with having proven the **AI behavior hypothesis**. Tests here check the local harness and data integrity only.

The benchmark intentionally makes **no model calls**. Run generated `prompts/` through your chosen model, collect the verbatim responses in matching `outputs/` files, then:

```bash
python scripts/benchmark.py packets --out runs/pilot
# Give reviewer only review_packets/ + ratings.csv; have reviewer fill ratings.csv
python scripts/benchmark.py report --out runs/pilot
```

Without actual ratings, `report` stops with an error rather than inventing results. For the full reproducible protocol, see [`evals/PROTOCOL.md`](evals/PROTOCOL.md).

## Repository map

```text
.agents/skills/judgment-preserver/
  SKILL.md                      # The installable, constrained meta-Skill
  references/decision-boundaries.md
scripts/
  audit_skills.py               # Human-review candidates, not policy decisions
  benchmark.py                  # Prompt generation, blinded packets, ratings report
  make_cases.py                 # 16 authored experiment cases (build helper)
evals/
  cases.json                    # Published task/control fixtures
  PROTOCOL.md                   # Experimental protocol & limitations
global/AGENTS.md.snippet        # Optional project-level guidance
tests/                          # Test harness unit tests
docs/architecture.md            # Hypothesis, threat model, boundaries
docs/ROADMAP.md                 # Future work (clearly unimplemented)
docs/CODEX_HANDOFF.md           # Ready-to-paste Codex engineering brief
README.zh-CN.md                 # Chinese guide
```

## Why a meta-Skill alone cannot solve this problem

Adding more instructions could itself degrade flexibility, and an ordinary Skill has no special power to reinterpret higher-priority policy or mandatory procedures. This project therefore makes **non-interference** a first-class goal: if no useful discretionary choice is available, skip the overhead. Real provenance-aware constraint resolution requires host integration and must not be faked using keyword classification.

See [`docs/architecture.md`](docs/architecture.md) for design principles and explicit non-goals.

## Publish / contribute carefully

- Do not advertise a benchmark win until external A/B/C outputs exist and reviewers have scored them blind.
- Do not claim cross-host compatibility without actual end-to-end invocation tests.
- Prefer small, documented revisions with controls for regressions in accuracy and mandatory behavior.
- If you publish this as your repository, replace contributor copyright wording if appropriate for your ownership and check the license before release.

## Sources and format references

- Agent Skills specification: <https://agentskills.io/specification>
- OpenAI Skill authoring and Codex setup: <https://learn.chatgpt.com/docs/build-skills>
- Anthropic authoring best practices: <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices>

MIT License. Feedback and critical reproductions welcome.
