# v0.4 exploratory pilot: no observed advantage over the minimal reminder

Date: 2026-10-27. This is a small, model-reviewed pilot, not a benchmark win, proof of equivalence or independent human study. The unchanged full Meta-Skill did not outperform the minimal reminder on these three cases.

## What actually ran

Three tasks were authored in a separate fresh Codex chat without reading the intervention or previous evaluations: incident advice/customer communication, an event notice/reminder, and deterministic revisioned seat allocation. The scenarios are fictional; the candidate answers are authentic model outputs, not software-test fixtures. All returned cases were retained; only JSON field naming and literal-newline normalization were applied before generation, with original/normalized hashes retained.

Each case ran once in all four native conditions, seed 20261027, requested model `gpt-6.1-sol`, low reasoning effort. All 12 CLI attempts completed, outputs were never replaced, and all 12 passed their declared automatic text checks. Three distinct cases are the sample size; twelve answers are not twelve independent task clusters.

The generator used the existing ChatGPT subscription, with subscription-only authentication verification and API-key environment variables removed for all 12 pilot calls. There were no purchases or reset-coupon redemptions. The exact served model revision was not exposed and remains unknown. Separate smoke/body-access probes are integration checks, not pilot outcome samples.

A fresh reviewer chat received only randomly re-keyed packets and the blank rubric, not treatment labels, source prompts, seed or coordinator expectations. It independently recomputed the structured answer and checked word counts. Its configured model/version was not exposed. This is **one model-assisted reviewer in a separate context**, not independent human review or verified model independence.

## Descriptive results

The five quality weights were fixed before generation. Gates refer only to requirements inspectable in the final answer, not execution behavior.

| Condition | Description | Text gate pass | Mean weighted quality / 5 |
|---|---|---:|---:|
| A | No supplied domain Skill | 3/3 | 5.00 |
| B | Domain Skill | 3/3 | 4.95 |
| C | Domain + full Meta-Skill | 3/3 | 5.00 |
| D | Domain + one minimal task-fit reminder | 3/3 | 5.00 |

C-D quality delta: **0.00/5**. C-B and D-B descriptive deltas: **+0.05/5**, both arising from the same single B answer. All paired text-gate deltas were zero. No confidence interval or significance claim is produced: there are only three clusters and unresolved model-version metadata.

The reviewer marked B's incident answer down by 0.5 in correctness for describing a 2.8-second-to-0.9-second improvement as a replay improvement. The prompt supplied the 2.8-second production observation and the 0.9-second replay result, but did not establish a comparable replay baseline. The answer also explicitly retained production uncertainty. The reviewer therefore treated this as a minor precision ambiguity, not a gate failure. This is one model's judgment, not a stable estimated treatment effect.

Eleven answers received maximum scores. That ceiling strongly limits discrimination and may reflect task ease, a generous rubric, evaluator leniency or some combination. It is not evidence that the answers are objectively perfect or that the methods are equivalent.

## Observed runtime, without causal attribution

| Condition | Sum of reported input tokens | Sum of reported output tokens | Mean measured seconds |
|---|---:|---:|---:|
| A | 54,989 | 643 | 21.29 |
| B | 60,726 | 737 | 23.05 |
| C | 62,961 | 733 | 21.70 |
| D | 57,344 | 721 | 21.29 |

Each condition reported 37,248 cached input tokens across its three calls. Counts come from public completion events; they are not monetary cost estimates. Input sizes varied substantially even within similar conditions. The record does not explain every context difference. Neither input differences nor latency differences can be attributed entirely to the intervention, especially with ambient host Skills/instructions, cache behavior, unobserved model revisions and a single repeat.

## Decision for this version

Keep the portable core unchanged and opt-in. Do not add more prompt instructions or complexity on the strength of this pilot. The minimal reminder remains a credible competing baseline, and even no supplied domain Skill reached the same observed quality here. The current evidence supports better measurement infrastructure and working native access, not a superior judgment method.

Before expanding efficacy claims, use tasks where baseline outcomes have headroom, freeze selection/rubrics before outcomes, audit ambient context, improve evaluator calibration, and seek independent human assessment. Do not tune these same three tasks or the current prompt until a win appears. Broader replication, rather than more repeats of an already ceiling-limited pilot, is the next justified research step.

## What the evidence does not establish

- General improvement, absence of regression across domains, equivalence, or causal effects.
- Full no-browsing/no-sending/no-file-write compliance: reviewer packets contain answers, and the pilot's compact traces retained only limited public action summaries.
- Complete host isolation or reproducibility of a pinned served model revision.
- Human utility, independent human reviewer agreement or commercial readiness.

The private experiment record retains original cases, normalization log, fixed plan, prompts, condition map, verbatim outputs, states, measured usage, re-keying receipt, original reviewer CSV/notes, imported model-review provenance and regenerated report. Source releases intentionally exclude those raw private records; full local version checkpoints retain them separately.
