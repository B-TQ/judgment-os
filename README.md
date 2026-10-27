# Judgment OS

**Check agent outputs. Compare Skill guidance. Keep the evidence honest.**

Judgment OS is a small, offline-first evaluation toolkit for people building Agent Skills and prompts. It provides deterministic answer checks, frozen A/B/C/D studies, controlled live collection and separately re-keyed model-review packets. An optional experimental Skill, Judgment Preserver, is included as a case study.

**Current release: 0.7 · Python 3.11+ · standard library only · MIT.** No pip installation, API key or model call is needed for offline use.

[中文](README.zh-CN.md) · [Quickstart](docs/QUICKSTART.md) · [Commands](docs/CLI.md) · [Evidence](docs/FOLLOWUP_V06_RESULTS.md) · [Contributing](CONTRIBUTING.md)

## Try it in five minutes

Download the source ZIP or clone the repository, then open its root directory:

```sh
python judgment.py doctor
python judgment.py demo --out runs/tutorial-01
python judgment.py check --case Q01 --answer examples/quickstart/correct.json
```

The tutorial prepares **8 empty study slots** and checks two bundled software fixtures: one passes, one intentionally fails. It produces no model answers, ratings or performance claim. Read the generated `START_HERE.md` for the next step. On systems where Python is called `python3`, use that name instead. Choose a fresh output directory on repeat.

To inspect an intentional failure:

```sh
python judgment.py check --case Q01 --answer examples/quickstart/incorrect.json
```

It exits 1 because the example counts a cancelled order. See the [full walkthrough](docs/QUICKSTART.md) for genuine collection and review.

## What it helps with

- Check declared JSON/CSV/text/length properties without calling a model.
- Compare task-only, domain Skill, full core and one-sentence guidance under common binding requirements.
- Keep original outputs, provenance, hashes, failures and blinded reviewer exports separate.
- Preserve reviewer disagreements and analyze review phases explicitly, without turning extra judges into extra task samples.
- Install the optional project-local Skill and remove an unchanged managed installation safely.

Live collection is off by default. The native adapter needs Codex CLI and Git, explicit live flags, an actual model name and the user's authorization. Other genuine outputs can be imported with declared provenance. A read-only sandbox is not privacy isolation.

## What the evidence says

The included full Skill has **not established a general advantage over a one-sentence reminder**. In the eight-case v0.6 follow-up, the comparison was 1 win / 7 ties; the win came from a one-word budget overrun. Initial review-context leakage was disclosed and corrected with a separate projectless review phase. Both phases are retained. This is model-only, small-sample evidence, not equivalence or independent human validation.

The tool's software checks and the optional Skill's efficacy are separate questions. [Read the result and limitations](docs/FOLLOWUP_V06_RESULTS.md). Start with clear requirements and appropriate domain guidance; use the full Skill selectively. [Usage decision](docs/USAGE_DECISION.md).

## Optional Skill

```sh
python judgment.py skill install --project /path/to/existing/project --dry-run
python judgment.py skill install --project /path/to/existing/project
```

Quote paths containing spaces. Explicitly invoke `$judgment-preserver` in a supporting Codex host. No global configuration is changed. Installation refuses an existing Skill; uninstall refuses changed or added files. See [installation and removal](docs/CLI.md#managed-skill-installation). The core text remains the v0.2 content; 0.7 versions the toolkit.

## Development and release

```sh
python -B -m unittest discover -s tests -v
python -B judgment.py selftest --out runs/pipeline-smoke
python -B judgment.py release --check
```

[Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Community conduct](CODE_OF_CONDUCT.md) · [Publishing checklist](docs/PUBLISHING.md) · [Changelog](CHANGELOG.md)

CI is configured for Windows/Linux and Python 3.11/3.14. Local checks do not imply a successful remote Actions run. No CI badge is asserted before a real repository run exists. The manual artifact workflow only builds source; it does not publish a GitHub Release or private research data.

Advanced compatible scripts remain under scripts/. Historical v0.2 source is preserved in legacy/, and old handoff documents are in docs/history/; their instructions do not authorize current actions. Source packaging excludes private runs and review records. Inspect all artifacts before sharing. See [release scope](docs/V0.7_STATUS.md) for tested boundaries.
