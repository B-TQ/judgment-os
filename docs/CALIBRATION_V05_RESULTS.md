# v0.5 evaluator sanity calibration

Date: 2026-10-27. This checks detection of explicit defects, not Judgment OS efficacy or population-level judge reliability.

## Fixed construction and provenance

All three C-condition answers from the v0.4 pilot were selected before calibration review. Each was copied unchanged as a control and copied again with a recorded programmatic modification. These three modified candidates are **not new authentic model generations** and never enter the treatment-effect report. Original controls were previously passed by one model reviewer; they are not independent human gold labels.

| Case | Programmatic modification | Expected text decision |
|---|---|---|
| I01 incident advice | Append that the cause is confirmed and completion guaranteed, despite the task's explicit uncertainty | fail |
| I02 event copy | Remove the required under-16 adult-accompaniment line | fail |
| I03 allocation JSON | Change remaining_seats from 0 to 1 while preserving valid JSON | fail |

I01 contains two related unsupported certainty claims; this calibration does not identify which one caused rejection. Each original control was expected to pass based on the prior text review. The fixed plan, exact mutations, original output fingerprints and expected labels were saved privately before grading.

Six packets were randomly re-keyed and shuffled. A fresh model-review task saw only the blind directory and neutral rubric, not source study, expected labels, mutation records or previous scores. It checked counts and recomputed the allocation. Its configured model and served revision were not exposed, and it is not independent human evidence. Procedure limits information disclosure but is not cryptographic host isolation.

## Observed result

| Check | Observed |
|---|---:|
| Original controls passed | 3/3 |
| Predeclared defective copies rejected | 3/3 |
| Pairs correctly distinguished | 3/3 |
| Incomplete review rows | 0 |

The immutable scorer validated every alias, output hash, packet fingerprint, completed row and pass/fail score contract. Original reviewer CSV and notes were retained. No ratings were manually changed to match expectations, and no v0.4 output, rating or report was replaced.

## Interpretation and decision

The fresh review is not simply an unconditional all-pass decision rule on these obvious sentinels. It detected omitted required content, an incorrect exact value and unsupported certainty. That supports using this procedure as a basic sanity check.

It does **not** establish that the v0.4 maximum scores were well calibrated, that subtle usefulness differences can be detected reliably, that the same model/context would always behave this way, or that three controls estimate specificity in a real population. No confidence intervals or reliability percentage is claimed.

The main research conclusion therefore remains unchanged: the three-task v0.4 pilot showed no observed advantage of the full Meta-Skill over the minimal reminder, under one model reviewer and substantial ceiling/host/version limits. Keep the original core optional and unchanged. Further efficacy work needs harder independently selected practical tasks, evaluator calibration beyond obvious defects, cleaner context and preferably independent human utility judgments. Adding prompt complexity or repeating the same easy tasks is not justified by this record.

## Reproduction and preservation

`calibration.py build` uses the frozen v0.4 private originals; give only its `blind/` to a fresh reviewer. `calibration.py score` reproduces the counts from the saved genuine model-review CSV, with explicit evaluator provenance. The build/scorer is intentionally specific to these three documented cases.

No new treatment-generation CLI calls were made in v0.5. Private calibration materials/results remain outside source release; version backups retain them separately with hashes. Local software verification passed 48 tests. Source release/clean extraction and checkpoint verification are recorded separately.
