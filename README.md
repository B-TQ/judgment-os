# Judgment OS v0.6

An experimental task-adaptation Skill and auditable evaluation toolkit. It preserves domain expertise and binding requirements while expressing when optional defaults should be adapted. It is not an operating system or an enforcement boundary.

Start with [usage guidance](docs/USAGE_DECISION.md). Clear task requirements and an appropriate domain Skill are the starting point. The full core remains opt-in; broad superiority over a one-sentence reminder has not been established. The core text is unchanged since v0.2.

This version adds eight independently authored work tasks, a fixed 32-slot A/B/C/D native follow-up, and two initial and two corrective same-task model reviews, reported by phase. Gate decisions, anchored 0–4 quality, pairwise preferences and disagreement remain separate. Read the [results](docs/FOLLOWUP_V06_RESULTS.md), [predeclared design](docs/STUDY_PROTOCOL_V06.md) and [status](docs/V0.6_STATUS.md). Previous [pilot results](docs/PILOT_V04_RESULTS.md) and [obvious-defect calibration](docs/CALIBRATION_V05_RESULTS.md) are distinct evidence, not proof of general efficacy.

To try the full Skill, copy `.agents/skills/judgment-preserver/` with its references into the target project's same directory, then explicitly invoke `$judgment-preserver` in a supporting Codex host. No Python or global configuration change is needed to use its text. The shorter comparator is in [examples/minimal-reminder.txt](examples/minimal-reminder.txt). Do not stack guidance by default or reinterpret mandatory rules as optional.

For the evaluation tools, use Python 3.11+ without third-party Python dependencies; native workspace staging also needs Git:

```powershell
python -B -m unittest discover -s tests -v
python -B scripts/audit_skills.py .agents/skills/judgment-preserver/SKILL.md --strict-metadata
python -B scripts/demo.py --out runs/demo-01
python -B scripts/release.py --check
```

The offline demo creates empty slots and plans, never model answers or ratings. Choose a fresh directory on repeat. Unit-test outputs are software fixtures, not research evidence.

See [reproduction](docs/REPRODUCE.md) and [same-task review](docs/PAIRED_REVIEW.md). A has only the task; B adds domain guidance; C adds the full core; D adds the one-sentence reminder. Binding requirements are common to all conditions. Adapter execution defaults to dry-run. Live subscription execution requires explicit `--live --acknowledge-cost --subscription-only --model ACTUAL_MODEL` and a bounded `--max-runs`; it does not buy or reset quota.

Share only independently exported review directories. Model reviewers must be identified as such, unknown versions remain unknown, and output-text review cannot establish all execution restrictions. Native staging alone does not prove Skill use. Host instructions, synthetic tasks, shared-model bias and missing human utility assessment limit inference.

Source packaging is allowlisted and excludes private studies, traces, maps and ratings. Use `scripts/release.py --check --zip EXTERNAL_NEW_ZIP`, then `scripts/checkpoint.py --dest EXTERNAL_NEW_DIRECTORY --evidence PRIVATE_STUDY`, and `--verify` to check the backup. Never overwrite versions. Inspect artifacts before distribution. The full original v0.2 is in `legacy/v0.2/`; the portable core copy retains its v0.2 filename because its content is unchanged. MIT license. Configured remote CI is not executed CI.
