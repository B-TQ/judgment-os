# Codex engineering handoff — Judgment OS v0.3

Copy the prompt below into Codex from the repository root. Do not assume v0.2's human-in-the-loop experiment proves the concept.

---

You are upgrading the local **Judgment OS v0.2** repository to a publishable **v0.3 empirical prototype**. Read `README.md`, `docs/architecture.md`, `evals/PROTOCOL.md`, `scripts/benchmark.py`, all tests and the installed Skill before editing.

**Research question:** Can an opt-in judgment-preserving meta-Skill improve task fit on tasks with optional stylistic/procedural defaults without regressing hard-constraint compliance or adding unnecessary process to deterministic tasks?

**Hard rules:**
- Preserve the host instruction hierarchy. Never imply the meta-Skill overrides system, developer, user, safety, tool-contract or genuinely mandatory domain-Skill instructions.
- Do not conflate keyword occurrence with a legally/technically authoritative requirement. Keep automatic audits explicitly advisory.
- Do not claim benchmark wins, create fake output samples, invent token/latency figures or silently run paid APIs.
- Keep the portable Skill short and truly optional. Do not force step-by-step reasoning exposure or candidate lists on every task.
- Favor standard-library tools unless an added dependency is clearly justified.

**Implement in small tested increments:**
1. Add **host-native Codex test adapter**, separate from the existing prompt-simulation mode. Verify official/current Codex invocation mechanics, discoverability and outputs in the environment before claiming integration. If Codex CLI is unavailable, implement an adapter interface + documented dry-run and clearly mark live E2E as blocked. Avoid brittle parsing of private Codex log formats.
2. Add deterministic validators for eligible cases (exact JSON, CSV, mandatory line prefix, strict header order). Make clear that these validate only explicit properties, not all safety constraints or artistic quality.
3. Extend the experiment harness to support anonymous output collation, independent blind judges, incomplete/missing/aborted runs, traceable model/version/settings, and redaction of secrets before public exports. Keep reviewer packets free of treatment labels. The private map must not be published accidentally.
4. Add treatment-level and per-task-class result summaries, paired analysis, uncertainty intervals when sample sizes are adequate, and explicit failure-case reporting. Do not compute confidence intervals for tiny samples as proof of causality.
5. Include at least one competing baseline (e.g., a minimal sentence advising task-fit), so any gain cannot automatically be attributed to the complexity of Judgment OS.
6. Expand unit/integration tests, update README (EN and Chinese), CI and limitations. Run tests and state actual commands/results.

**Definition of done:** A reviewer on a clean machine can clone, run unit tests, generate a seeded experiment, execute or explicitly simulate model runs, blind-grade samples, reproduce a report from provided authentic ratings, and see every limitation. No unverifiable benchmark statistics or compatibility claims.

Work autonomously within scope. If API credentials, real users or approval are needed, implement offline substitutes; do not ask for secrets or publish files containing them. Commit-ready source files and a concise changelog are the deliverables.

---
