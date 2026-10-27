# Local v0.4 verification — 2026-10-27

Actual environment: Windows, Python 3.14.6, Git, `codex-cli 0.163.0-alpha.11`, existing ChatGPT subscription login. Original v0.3 verification is retained in VERIFICATION_V03.md.

## Software

`python -X utf8 -B -m unittest discover -s tests -v`: exit 0, **42 tests passed in 11.608 seconds** in the final recorded code test run. New coverage includes checkpoint creation/verification/corruption/overwrite refusal, VERSION-aware archives, body-only probe staging, API-key environment removal and subscription verification, JSON-safe redaction, non-reasoning public item summaries, model-review provenance and output-text gate scope. Temporary fixtures are software tests, not research data.

`python -X utf8 -B scripts/audit_skills.py .agents/skills/judgment-preserver/SKILL.md --strict-metadata`: exit 0; metadata PASS, seven advisory wording cues.

## Authentic execution and review

- One unmodified-core strict-JSON native smoke call completed with the expected object.
- A separate native body-access probe matched both unpredictable codes placed in copied domain/Meta-Skill bodies, absent from the generation prompt. This proves accessibility in that probe, not effectiveness of the original method.
- All 12 predeclared native pilot calls completed, no retry/replacement, all declared automatic text checks passed. Generator request was `gpt-6.1-sol`, low effort; exact served revision is unknown.
- One fresh, blind model-review task completed all 12 rows; original ratings and notes are preserved. Model-reviewed output-text gates all passed. C and D were tied, and A tied them. See PILOT_V04_RESULTS.md for ceiling/metadata limits.
- Import command explicitly used `--reviewer-kind model` with unknown configured evaluator version disclosed, without `--independent`. Reporting completed with no missing/unrated pilot outputs and no confidence intervals.

The reusable probe command is `python -B scripts/integration_probe.py --out runs/fresh-probe --live --acknowledge-cost --subscription-only --model ACTUAL_MODEL`; dry-run is default without the live flags. Probe-only modifications never alter the shipped core. A final reusable-command verification is retained in the private evidence directory.

## Version preservation

v0.3 source ZIP, SHA-256, delivery note and verification evidence were copied to a separate pre-iteration backup; the source ZIP hash remained `d99613c5fd2956f1a37f04b06e7b247e470f6f16cf624ef754b55f8a18668c11`. A v0.4 working checkpoint was created and verified before unblinding. Final version checkpoints use `checkpoint.py --dest` with separately copied/hashed private evidence, then `--verify`.

Source release uses an allowlist and checksum manifest. It does not include raw study outputs, ratings, receipts, maps, traces, environment files or Git state. Full private evidence remains local and is copied into the private backup, not the source ZIP.

No credit purchase, reset-coupon redemption, public publication, remote push, independent human evaluation, remote CI or general performance claim occurred.
