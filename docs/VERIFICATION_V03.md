# Local verification — 2026-10-27

Environment actually exercised: Windows, Python 3.14.6, Git available. Codex local executable reported `codex-cli 0.163.0-alpha.11`. No authentic model invocation or remote CI run was performed.

## Commands and observed results

```powershell
python -X utf8 -B -m unittest discover -s tests -v
```

Exit 0. **37 tests passed**, 11.675 seconds on the final recorded source test run. Coverage includes the original audit/benchmark behaviors, four-way balance and shared requirements, deterministic validators, missing/changed/duplicate data, CLI mock success/failure/timeout/interruption, native filesystem staging, independent re-keyed review imports, multiple-judge disagreements, model-profile mismatch exclusion, paired clustering, no-data refusal, real subprocess offline demo and reproducible source ZIP exclusion checks.

Tests explicitly use software fixtures. Their mock `Live attempts` log lines do not represent model calls. Temporary fixture answers and scores are cleaned up and are not delivered as empirical data.

```powershell
python -X utf8 -B scripts/audit_skills.py .agents/skills/judgment-preserver/SKILL.md --strict-metadata
```

Exit 0. Metadata PASS; seven advisory wording cues. These cues are not permission or authority classifications.

```powershell
python -X utf8 -B scripts/codex_adapter.py probe --cli PATH_TO_NATIVE_CODEX
```

Exit 0. CLI version/help returned supported `--json`, `--output-last-message`, `--sandbox`, `--ephemeral`, `--ignore-user-config` flags; no required flags missing. Only read-only help/version were invoked.

```powershell
python -X utf8 -B scripts/demo.py --out runs/delivery-offline --cli PATH_TO_NATIVE_CODEX
```

Exit 0. Results for both modes:

| Mode | Slots | Dry-run plans | Missing outputs | Empty-rating report refused |
|---|---:|---:|---:|---|
| prompt-simulation | 64 | 64 | 64 | yes |
| codex-native | 64 | 64 | 64 | yes |

Model calls: **0**. Candidate answers: **0**. Human ratings: **0**. Performance claim: none. Each native slot has its own Git root and the condition-appropriate files; actual host loading remains unverified.

## Release verification

```powershell
python -X utf8 -B scripts/release.py
python -X utf8 -B scripts/release.py --check --zip ../Judgment-OS-v0.3-Codex-Full-Package.zip
```

Checksums cover the allowlisted current source plus the original 24-file v0.2 archive. Runtime outputs, reviewer exports, traces, state, secrets files and Git metadata are excluded. The released ZIP can be extracted and verified with `python -B scripts/release.py --check`; the packaging tests also check byte-identical archives from identical source.

Full local logs and deployment-specific executable paths stay outside the source package in the project's verification directory. No benchmark scores are supplied. A future genuine efficacy report needs actual controlled model runs and independent reviewers; software checks do not substitute for them.

Not exercised: genuine model E2E, actual Skill activation, remote CI, Linux, Python 3.11, other hosts, independent evaluator data or public publication.
