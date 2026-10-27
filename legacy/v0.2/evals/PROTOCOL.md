# Evaluation protocol — no claimed scores

This is a **human-in-the-loop** benchmark scaffold. The scripts do **not** call an LLM, run Codex, or grade quality automatically.

## Conditions
- **A**: user request alone (control, no domain Skill excerpt)
- **B**: user request + experiment-supplied domain Skill excerpt
- **C**: user request + same domain excerpt + Judgment Preserver excerpt

All three are assembled in prompt text. This is **not** the same as host-native Skill invocation, and results must be described as such. The model should run with identical settings, available tools, and reference materials across conditions. The 16 cases cover open creative choices and strict/no-op controls.

## Commands

```bash
python scripts/benchmark.py prepare --out runs/pilot --seed 42 --repeats 3
```

This creates `prompts/<blind_id>.md`, empty `outputs/<blind_id>.txt`, a hidden mapping, and an empty `ratings.csv`. For each prompt file, submit it to the same model and paste the resulting answer verbatim into the identically named output file. Record latency, token usage, and model version separately if supported (not currently automated).

```bash
python scripts/benchmark.py packets --out runs/pilot
```

Share only `review_packets/` and `ratings.csv` with a reviewer. **Do not share `prompts/` or `private_condition_map.json`.** Review packets include user prompts, predeclared hard-gate checks, and anonymous responses. Candidate text can still accidentally reveal treatment identity, so this is not perfect blinding.

Complete `ratings.csv`: `hard_gate` = `pass` or `fail`. For passing outputs enter scores 0–5 in `goal_fit`, `correctness`, `judgment`, `useful_originality`, `efficiency`. Failed gates are logged as failures and excluded from *quality-on-pass* averages. Do not silently convert failure to a low creative score. Notes are optional.

```bash
python scripts/benchmark.py report --out runs/pilot
```

This writes a descriptive `report.md` derived only from completed ratings. Unrated slots are omitted. Never claim performance improvement from the empty template, or from tests conducted entirely by the same model that authored the project.

## Suggested review dimensions

- **Hard-gate pass/fail**: safety, permissions, exact schema, mandatory skill procedure, and explicit user requirements.
- **Goal fit**: 30%. Is the user's actual need addressed?
- **Correctness/verifiability**: 30%. Are statements, format and artifacts sound?
- **Judgment**: 20%. Were meaningful choices handled intelligently?
- **Useful originality**: 10%. Does distinctiveness help this task, not merely differ?
- **Efficiency**: 10%. Avoids unnecessary process and verbosity.

## Minimum honesty bar for public reporting

Report every condition and case with the same model, prompt settings, tools and repeats; disclose failed gates, exclusions, missing answers and costs. Provide anonymized review criteria, negative cases, task-class results and at least one failure analysis. Ideally have independent reviewers, replicates, more models, actual host-native invocation and baseline competing solutions.
