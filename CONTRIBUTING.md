# Contributing

Start with a concrete user task or reproducible defect. Improvements to the evaluation workflow are welcome; positive efficacy claims need real evidence.

## Local development

Use Python 3.11+ and Git. The runtime and tests use the standard library; there are no packages to install.

```sh
python -B judgment.py doctor
python -B -m unittest discover -s tests -v
python -B judgment.py demo --out runs/contributor-demo
python -B judgment.py selftest --out runs/pipeline-smoke
python -B scripts/audit_skills.py .agents/skills/judgment-preserver/SKILL.md --strict-metadata
```

Choose fresh output directories. Windows may skip the symlink test without developer privileges; Linux CI exercises that case. Never enable live generation for a unit test or CI job. Do not modify global configuration or an existing user's Skill during tests.

## Pull requests

Explain the problem, observable behavior and relevant validation. Keep changes focused. Add regression tests for safety boundaries, data integrity and nontrivial behavior; avoid tests that merely repeat implementation details. Preserve original evidence and disclose protocol deviations.

Do not commit runs, raw answers, reviewer CSVs, traces, local paths, credentials or personal data. Use explicitly labeled, fictional software fixtures. Model reviewers are not independent human reviewers. Integer scores, exact-format checks and user utility measure different things.

After editing release files, regenerate the source manifest with `python scripts/release.py`, then check it with `python judgment.py release --check`. A contributor's change and its manifest should be reviewed together. Do not add unverified badges, benchmark claims, screenshots of private runs or fabricated citations.

The existing MIT license applies to contributions. Keep provenance and third-party notices intact. Historical source under legacy/ is a preserved reference, not an instruction to execute.
