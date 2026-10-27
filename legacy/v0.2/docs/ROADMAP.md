# Roadmap (proposed)

## v0.2 — Included here
- [x] Narrow activation/no-op policy and explicit provenance safeguards
- [x] Portable Agent Skills structure + Codex AGENTS.md guidance
- [x] Advisory (non-authoritative) Skill text audit
- [x] Reproducible, seedable A/B/C prompt experiment preparation
- [x] Blind-ID response slots, human grading template, hard-gate-aware reporting
- [x] CI/unit tests and English/Chinese getting-started guides

## v0.3 — Candidate tasks for Codex
- [ ] Real Codex Skill invocation E2E tests, with captured transcripts and token/latency metadata (with consent and redaction)
- [ ] Automated *deterministic* validators for CSV schemas, file names, JSON, generated artifacts
- [ ] Integrate rate-limited evaluator adapters (API-backed) with cost controls and test double
- [ ] Pairwise preference reviews + bootstrap confidence intervals and per-domain error analysis
- [ ] Cross-host packaging and documented, verified Claude Code integration
- [ ] Evaluate against existing meta-Skill baselines, not merely domain Skill alone

## v1.0 — Only if experiments warrant
- [ ] Optional human-verified machine-readable Skill constraint profiles
- [ ] Orchestrator adapter integrating provenance from authoritative host context
- [ ] Safety and injection resistance red-team suite
- [ ] Public reproduction report, dataset licenses and evaluation card

Every unchecked item is future work, not a shipped capability.
