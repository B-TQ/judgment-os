# Reproduce v0.5

Run commands from the extracted `judgment-os-v0.3` root. Python 3.11+ and Git are the only local prerequisites for native staging. No Python packages, credentials or network access are needed for tests/demo; CLI capability probing is local help/version only. Choose a fresh run/export directory for each attempt. Paths and model names below are placeholders to replace with genuine values.

## 1. Offline verification

```powershell
python -B -m unittest discover -s tests -v
python -B scripts/audit_skills.py .agents/skills/judgment-preserver/SKILL.md --strict-metadata
python -B scripts/demo.py --out runs/reproduce-offline-01
python -B scripts/release.py --check
```

Open `runs/reproduce-offline-01/demo_summary.json`. With Git installed, both modes should have 64 slots and 64 dry-run plans, zero answers, zero scores, 64 missing outputs, and expected refusal to report empty ratings. Without Git, only simulation is demonstrated and native staging is explicitly marked unavailable. The demo log is software evidence, not an evaluation transcript.

## 2. Prepare and inspect

```powershell
python -B scripts/benchmark.py prepare --out runs/study-01 --seed 42 --repeats 3
python -B scripts/codex_adapter.py run --out runs/study-01 --max-runs 4
```

This creates 192 simulation slots and four plans; it calls no model. Open `protocol.json` and `adapter_plan.json` locally. Keep `private_condition_map.json`, `prompts/`, protocol, snapshots, outputs, traces and state private. Never give the private directory to a judge.

For real Skill files use a different prepared run:

```powershell
python -B scripts/benchmark.py prepare --out runs/native-01 --mode codex-native --seed 42 --repeats 3
python -B scripts/codex_adapter.py probe --cli /absolute/path/to/codex
python -B scripts/codex_adapter.py run --out runs/native-01 --cli /absolute/path/to/codex --max-runs 4
```

On Windows provide the native `.exe`, not a .cmd/.bat/.ps1 wrapper. The probe reads only `--version` and `exec --help`. If unavailable or missing required flags, dry-run still works and live execution refuses to start. The native workspaces are local Git repositories solely to establish Skill discovery boundaries, not claims of process isolation. User/admin/system Skills and instructions still need auditing in a clean environment.

## 3. Authentic outputs: choose an explicit source

For a later authorized live CLI experiment, replace the model and executable placeholders. This command **uses model quota or money** and was not run during this delivery:

```powershell
python -B scripts/codex_adapter.py run --out runs/native-01 --cli /absolute/path/to/codex --live --acknowledge-cost --subscription-only --model YOUR_ACTUAL_MODEL --max-runs 4 --timeout 180 --effort low
```

`--id SLOT_ID` can select a particular slot and is repeatable. Without it, attempts use the seeded preparation order. The default cap is one attempt per invocation. There is no automatic retry, overwrite or monetary budget guarantee. Pin settings consistently. Unknown resolved model versions remain null instead of being guessed. Live completion records measured latency, public usage if emitted, exit status and redacted public event summaries. Reasoning items are excluded. Temporary final-message files are removed. Raw final answers remain private and verbatim.

Alternatively collect a real externally produced answer:

```powershell
python -B scripts/codex_adapter.py collect --out runs/study-01 --id SLOT_ID --answer-file /path/to/verbatim-answer.txt --model ACTUAL_MODEL --model-version ACTUAL_VERSION --source external-model-session
```

Add `--settings-file /path/to/settings.json` to record external generation settings. `unknown` can be used only when the version is actually unavailable; that limitation remains visible. The adapter does not independently authenticate operator-declared outputs. Do not use made-up answers, software-test fixtures or self-assigned scores as evidence.

After collecting genuine outputs:

```powershell
python -B scripts/benchmark.py validate --out runs/study-01
```

Inspect `validation.json`; failures include declared-property checks only. A failed automated check must be resolved transparently with a new attempt/experiment, not by granting an inconsistent human pass. Preserve failed attempt evidence.

## 4. Export independent reviewer packets

```powershell
python -B scripts/benchmark.py export-review --out runs/study-01 --dest review-exports/alice-01 --reviewer alice
```

Optionally add `--redact-file /path/to/private-literals.txt` containing one sensitive literal per line. The separate export contains only `packets/`, `ratings.csv`, `README.md`; the receipt that maps aliases and hashes stays private. Inspect those files for residual personal information, credentials and treatment clues before sharing. Do not send prompts, protocol, seed or coordinator reports. Source content can reveal treatment despite re-keying.

Give the prepared export to a real reviewer who has not seen condition labels. They fill hard_gate pass/fail. Passing rows need five numeric 0–5 scores; failing rows leave scores blank and should explain the concrete failure in notes. Leave unread rows unscored. Keep IDs and hashes intact. A redaction that changes judgeable properties must be noted and privately resolved before a pass is recorded.

Use another fresh export/reviewer ID for a second reviewer. Independence is established by study procedure, not by the software flag.

## 5. Import genuine ratings and reproduce the report

```powershell
python -B scripts/benchmark.py import-ratings --out runs/study-01 --reviewer alice --ratings review-exports/alice-01/ratings.csv --independent
python -B scripts/benchmark.py report --out runs/study-01
```

Imports refuse duplicates, unknown IDs, hash mismatches, empty/changed outputs, invalid numeric values, malformed schemas or contradictory passes. Imports cannot overwrite prior reviewer data. A new review version must preserve rather than silently replace prior evidence. Use one final imported file per reviewer; partial rows are allowed, but once imported that reviewer ID cannot be amended.

`report.md` and `report.json` contain only the provided ratings and actual output coverage; no missing quality is imputed. Imported judges are averaged within each output; gates require unanimity. Compare complete matched case/repeat pairs; quality compares only double-passing pairs. Case means, rather than repeats or judge rows, form the bootstrap units. Intervals below 10 distinct cases are suppressed. This prevents a large repeat count from creating a false sense of sample size. It does not fix selection bias or establish causality.

Expected-slot counts, missing/unrated IDs, failed cases, disagreement counts, execution profiles, measured latency/usage coverage and input fingerprints are available in JSON. Known model/version/configuration/CLI-version mismatches exclude paired observations; unknown model/version/settings preserve exploratory deltas but suppress intervals. These reports reveal treatment labels, so keep them away from blind reviewers. A small private native pilot has model-assisted, output-text-only ratings; no independent human efficacy result is established.

## 6. Compatibility and source release

v0.4 adds `--subscription-only` to live adapter calls. It checks the existing ChatGPT login and removes API-key environment variables from the child; it does not purchase credits, redeem reset coupons or guarantee a specific resolved model revision.

For an explicitly model-assisted review, import with `--reviewer-kind model --reviewer-model "documented model provenance or explicitly unknown"`, without `--independent`. The CSV fields remain compatible. Gate decisions are output-text-only: answer packets cannot establish no-tool-action requirements.

Version checkpoints use `python -B scripts/checkpoint.py --dest /external/new-backup --evidence /private/evidence-directory` after a valid release checksum; verify using `--verify /external/new-backup`. Existing destinations are rejected. Evidence copies are private and separately fingerprinted. The source archive prefix follows VERSION. The original v0.3 verification record remains in VERIFICATION_V03.md.

`prepare --conditions ABC` retains three groups. Local `packets` and root `ratings.csv` remain unblinded compatibility helpers; the report rejects mixing their filled rows with imported judges. Old v0.2 run folders use the archived v0.2 harness. Default v0.3 has four groups and a different seeded order, so old IDs cannot be compared by filename.

```powershell
python -B scripts/release.py --check
python -B scripts/release.py --check --zip ../Judgment-OS-v0.5.zip
```

After source edits, run `python -B scripts/release.py` once to regenerate checksums, review changes, then check/package. The ZIP includes allowlisted source and archived v0.2 files; it excludes runs, exports, traces, environment files and Git metadata. This does not replace manual source review or authorize publication. Public research-data export requires a separate reviewed workflow; do not zip a private run.

## Official integration references (checked 2026-10-27)

- [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode): public JSONL, completion usage and final-message output.
- [CLI reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli): model, sandbox, ephemeral, ignored user config, stdin prompt and other argument contracts.
- [Local Skill discovery](https://learn.chatgpt.com/docs/build-skills): repository/user/admin/system scopes and explicit invocation.

Local observed CLI: `codex-cli 0.163.0-alpha.11`. Read-only capability checks passed; v0.4 additionally completed limited native calls and a body-only nonce probe. Full behavioral efficacy, clean-host isolation and independent human evaluation remain unverified.

## Evaluator calibration, separate from efficacy

Use `python -B scripts/calibration.py build --study /private/native-pilot-01 --out /private/new-calibration`, share only its blind/ directory, and score a genuinely completed review with `python -B scripts/calibration.py score --out /private/new-calibration --ratings /private/new-calibration/blind/ratings-filled.csv --reviewer-model "actual or explicitly unknown provenance"`. This targets the three documented I01/I02/I03 C originals. Modified sentinels are programmatic calibration data, never new model generations or treatment outcomes. Do not share the private expected-label manifest. See CALIBRATION_V05_RESULTS.md.
