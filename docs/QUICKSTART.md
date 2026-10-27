# Five-minute local quickstart

[中文](QUICKSTART.zh-CN.md) · [Documentation map](README.md) · [Use the optional Skill instead](USAGE_DECISION.md#english)

This page covers the evaluation toolkit. For the optional Skill's preview/install/invoke/remove path, use the guide above. These are separate entry points; offline evaluation does not install the Skill or authorize model calls.

Use Python 3.11+. Download the source ZIP or clone this repository, open its root directory, and run these commands. Nothing needs pip installation and no API key is required. Use `python3` if that is your interpreter name.

```sh
python judgment.py doctor
python judgment.py demo --out runs/tutorial-01
python judgment.py check --case Q01 --answer examples/quickstart/correct.json
```

The tutorial freezes eight empty A/B/C/D slots and writes `runs/tutorial-01/START_HERE.md` plus `demo_summary.json`. It checks two clearly labeled software fixtures: one passes, one intentionally fails. It creates **zero model answers and zero ratings**. The example is a software walkthrough, not method-performance data. Repeating the tutorial requires a fresh output directory.

For an automatic fresh-directory walkthrough, use `python scripts/try_demo.py`. Windows users with Python installed can double-click `TRY_DEMO.cmd`. These shortcuts run doctor, demo and the correct-answer check only. They change no global settings.

To see a real failure exit code:

```sh
python judgment.py check --case Q01 --answer examples/quickstart/incorrect.json
```

This intentionally exits 1 because it counts a cancelled order. Exit 0 means the declared properties passed; exit 1 means failure/error; argument errors and an answer with no applicable checks can exit 2. A property check does not establish overall task quality.

## Prepare your own study

Use examples/quickstart/cases.json as the small schema example, or evals/followup_v06_cases.json for the eight-task set. Keep reviewer-only focus/anchors and validator expected values outside generator prompts.

```sh
python judgment.py prepare --cases examples/quickstart/cases.json --out runs/my-study --seed 42 --repeats 1
python judgment.py run --out runs/my-study --max-runs 1
```

The second command is a dry run. The four conditions are A task only, B domain Skill, C domain Skill plus full core, D domain Skill plus the one-sentence reminder. Every condition receives the same binding requirements. Use `--mode codex-native` at preparation if you want actual staged Skill files; this needs Git. File staging alone does not prove activation.

## Genuine answers and review

For externally produced answers, `python judgment.py collect --help` lists required source/model/version metadata. The operator is responsible for provenance; use real unknown-version labels rather than inventing precision. For native live generation, first obtain the user's authorization, inspect the CLI and existing subscription login, then explicitly add `--live --acknowledge-cost --subscription-only --model ACTUAL_MODEL` and a bounded `--max-runs`. Nothing in this quickstart authorizes spending or supplies a real model name for your account.

After all four conditions for each case are genuinely complete:

```sh
python judgment.py validate --out runs/my-study
python judgment.py review export --out runs/my-study --dest review-exports/judge-01 --reviewer judge01
```

Share only that export directory. Use fresh projectless reviewer contexts with the known scope supplied directly; prohibit chat/project inventories, archive discovery and historical study access. See PAIRED_REVIEW.md for the archive-metadata leakage found in v0.6 and the corrective procedure. A reviewer fills new quality-filled.csv/pairs-filled.csv files without changing templates.

```sh
python judgment.py review import --out runs/my-study --reviewer judge01 --quality review-exports/judge-01/quality-filled.csv --pairs review-exports/judge-01/pairs-filled.csv --model "Actual model provenance, explicitly unknown where needed"
python judgment.py report --out runs/my-study --reviewer judge01
```

Add a separately re-keyed reviewer with another ID for a second review. Select each phase explicitly when reporting; do not pool corrections into additional task samples. Preserve raw results, failures and disagreements. No ratings means no performance report. The same-task importer currently supports model reviewers; the older single-answer workflow supports declared human review separately.

See CLI.md for command reference, USAGE_DECISION.md for the optional Skill, and REPRODUCE.md for the historical advanced workflow.
