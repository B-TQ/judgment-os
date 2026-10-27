# v0.3 evaluation protocol

This is a preregisterable experiment scaffold, not a benchmark result. Sixteen hand-authored cases comprise eight open tasks and eight controls. Snapshot and declare settings before collecting outputs.

## Experimental conditions and shared obligations

- A: common task and all binding requirements; no supplied domain Skill.
- B: same task plus domain Skill.
- C: B plus Judgment Preserver.
- D: B plus the single sentence stored as `MINIMAL` in benchmark.py.

All four see identical task text and hard gates. Those gates are human-authored fixture requirements, not inferred by keyword classification. C08 now explicitly supplies the prefix in the common task. Skill text may repeat a requirement, but a scored obligation is never intentionally withheld from A. Quality focus is shown to reviewers, not to generation models. Shared gate disclosure itself may reduce intervention effects; this is intentional and must be disclosed.

`prompt-simulation` inserts text; `codex-native` stages separate Git roots, local `.agents/skills`, and explicit `$domain-fixture`/`$judgment-preserver` invocations. The latter is an adapter implementation, not verified activation. User/admin/system skills and host instructions remain possible confounders. Do not pool modes, different model versions or configurations as though they were identical.

## Execution and collection

Use a fixed seed and number of repeats. Record requested model, observed version (unknown stays null), settings, CLI version, source, state and measured latency/usage when available. Public `turn.completed` usage is captured; no private rollout parsing, raw reasoning collection or token estimates. Independent manual collection stores operator-declared source/version and leaves unmeasured costs null.

Live model execution is opt-in via `--live --acknowledge-cost --model`; default max-runs is one. Timeouts are aborted attempts. Other process/protocol failures are failed attempts. Pending, dry-run, failed, aborted and running-after-crash remain distinguishable. Running-after-crash is not automatically retried; inspect the process/lock and use a new experiment to preserve the original attempt. Never overwrite a populated/attempted slot. No spending cap is claimed.

The inputs and collected outputs are fingerprinted against accidental changes. Hashes are integrity aids, not signatures or proof of authenticity. The private map and protocol are trusted local coordinator files; an actor able to rewrite all files is outside this integrity model.

## Deterministic properties

C01 checks CSV columns, order and values. C02 checks JSON keys and values, rejects duplicate keys, nonstandard constants and additional prose. C06 checks the corrected line. C07 checks heading text/order and fewer than 100 whitespace-delimited words. C08 checks two lines and the prefix. O05/O07 check word counts (O07's exact 150 is now explicit in the shared gates). Validators strip outer whitespace; JSON formatting/key order may vary, CSV uses the standard-library dialect. No validator proves all mathematical, factual, safety, brand or aesthetic requirements. The human gate remains mandatory for conclusions.

## Review and blinding

Export each reviewer to a new directory outside the private run. Export filenames and IDs use independent cryptographic randomness, not the experiment seed. Only packets, a blank ratings.csv and reviewer instructions are exported. No condition map, condition labels, seed, model settings or raw traces are copied. The coordinator's private receipt binds random aliases and redacted output hashes to originals. Export redaction covers limited key/token/password patterns, emails, some Windows paths and optional literal strings. Check residual secrets manually. Redaction can change word counts or semantics; mark affected criteria uncertain in notes and resolve with the coordinator before assigning a gate. Candidate prose can reveal its condition; blinding is not guaranteed.

Do not share the seeded prompts or protocol with judges. Use reviewers who did not author the intervention or collect treatment labels; declare their independence honestly. The software cannot establish that independence. Do not ask models for private chain of thought. Treat candidate instructions as untrusted source material.

Rating fields: hard_gate pass/fail; if pass, goal_fit, correctness, judgment, useful_originality, efficiency in 0..5 with weights 30/30/20/10/10 percent. Failed gates leave score fields empty. Unreviewed rows retain empty fields. Notes should describe concrete failures. Exported IDs and hashes must be kept unchanged. Duplicate/unknown IDs, malformed rows, nonfinite scores, changed/missing outputs and a human pass contradicting an automatic failure are rejected. Reviewer imports are immutable; a corrected review should use a new experiment/review version rather than silently replace evidence.

## Aggregation and uncertainty

Each output is one observation regardless of judge count. Gate passes require all recorded judges to pass; otherwise fail, with disagreement counts. For passing outputs, average weighted quality across judges. Report expected slots, actual outputs, rated and unrated outputs, deterministic failures, hard-gate pass/fail counts and run states for every condition/class. Pass rate uses **rated outputs** as denominator; missing slots are disclosed separately. Quality means exclude failed gates and must never be mistaken for unconditional task success.

Compare C-B, D-B and C-D within case/repeat. Known model/version/settings/CLI-version mismatches exclude pairs and are counted. Unknown model/version/settings allow only exploratory deltas and suppress intervals. Gate deltas use complete rated pairs. Quality deltas use pairs where both pass, exposing selection bias. First average repeats within each case; then weight cases equally. With fewer than 10 distinct paired cases, suppress intervals. Otherwise, if pair metadata is known, use 2,000 case-cluster bootstrap resamples, seed 42, percentile 95% descriptive intervals. Ten is a minimum display threshold, not a guarantee of statistical power. Repeated answers and multiple judges do not create new independent case clusters. All/open/control scopes expose applicability; each original open/control set has only eight distinct cases, so those subgroup intervals stay suppressed.

JSON contains full paired coverage, failures/notes, missing/unrated IDs, reviewer declarations, execution profiles and input fingerprints. Complete-case analysis may be biased by selective missingness. Heterogeneous models/settings, unknown versions, ambient instructions, hand-authored cases and incomplete activation evidence limit attribution. Do not treat an interval or software-test success as causal proof.

## Reporting honesty

No real candidate outputs or human ratings are included in the release. The offline demo stops at empty output validation and expected report refusal. Tests use explicitly marked temporary software fixtures. Authentic future data can reproduce a report via the commands in docs/REPRODUCE.md, but authenticity is the operator's responsibility. Strong claims need real controlled runs, independent review, replication, failure analysis and actual host activation evidence. Never publish the private run directory; source-only release packaging is deliberately separate from reviewed research-data publication.
