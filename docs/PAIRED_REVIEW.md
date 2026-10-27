# Same-task blind review

`paired_review.py` supplements the legacy independent-answer 0–5 review. It keeps its own receipts, imports and report; never mix its anchored 0–4 scores with the older scale. It currently requires every A/B/C/D slot to be completed. If a study is incomplete, preserve it as incomplete rather than filling missing outputs or hiding failed attempts.

```powershell
python -B scripts/paired_review.py export --out runs/study --dest review-exports/judge-01 --reviewer judge01
```

Share **only** `review-exports/judge-01` with a fresh reviewer. It contains task groups, instructions, `quality.csv` and `pairs.csv`. Each group has four independently randomized candidate aliases. The packets include all binding task text, authored quality anchors/focus, candidate final answers and declared deterministic check results. They exclude the domain/core Skills and private condition map. Inspect exports for residual identifying or sensitive content: pattern redaction and random aliases do not guarantee anonymity.

The reviewer creates `quality-filled.csv` and `pairs-filled.csv`, leaving templates unchanged. Every candidate and all six same-task pairs must be reviewed. Passing answers get one integer 0–4 score; failed answers leave quality blank. Every decision needs specific evidence. A text-check pass does not prove all requirements, and execution behavior cannot be established from final text.

```powershell
python -B scripts/paired_review.py import --out runs/study --reviewer judge01 --quality review-exports/judge-01/quality-filled.csv --pairs review-exports/judge-01/pairs-filled.csv --model "Actual reviewer model, or explicitly unknown provenance"
python -B scripts/paired_review.py report --out runs/study
```

Use a new reviewer ID and export directory for the second reviewer. Imports are immutable; correct genuine review mistakes through a new reviewer/version, preserving the original. The current import interface supports model reviewers only and always records that no independent human validation occurred.

`paired_report.json` is private analysis: condition-level passing-only scores, judge-specific win/tie/loss contrasts, and case-level concordance. Disagreement is retained as `disputed`, including win/tie differences. Two judges do not establish truth. No efficacy interval, significance test or causality claim is generated. Per-case output hashes are checked again when reporting.

Receipts and imports are ordinary local integrity records, not signed attestations. The coordinator and local files remain trusted. Source packaging excludes `paired_judges` and `paired_report.json`; keep actual private study directories outside the source or under `runs/`.


## Keep review contexts and phases separate

For strict review isolation, use a fresh projectless chat and supply that known status explicitly. Do not give it a project to locate; prohibit chat/project inventories, session state/index and archive history. Requirement-archive discovery APIs can attach summaries of other chats even when only identity metadata is requested. A reviewer saying it ignored an incidental summary does not prove lack of influence. Preserve and disclose such exposures; never erase the first ratings.

A corrected phase must use new reviewer IDs/aliases and a documented amendment. Keep the same output hashes and report the original phase as well. Select reviewers explicitly:

```powershell
python -B scripts/paired_review.py report --out runs/study --reviewer judge01 --reviewer judge02
```

The report records `reviewer_selection`. Without `--reviewer`, all imported reviews are included; this is unsuitable when different phases should remain separate. Save each derived report under its phase before generating another. Imports themselves stay immutable. Additional judges do not add task samples or establish independent human validation.
