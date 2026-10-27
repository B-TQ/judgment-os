# v0.4 exploratory native pilot — fixed before generation

The original pilot plan and hashes are retained privately with the experiment. This document describes the design; it is not a preregistration with an external registry.

- Three fictional but practical tasks were authored in a separate fresh Codex chat, which was instructed not to read the intervention, existing evaluations or this chat. This is independently tasked **AI authorship**, not independent human task design.
- Tasks cover incident decision/communication, two-channel public information, and deterministic revisioned seat allocation. Domain guides have 496, 546 and 529 English words respectively (as checked by the design task).
- All three cases are included. Before generation, only schema normalization was performed: literal newline separators were decoded, `max_words` became `min`/`max`, and `expected` became `value`. Task content and expected answers were not changed. Original and normalized hashes plus the edit log remain in the private experiment record.
- Four conditions A/B/C/D are used, with the original core Skill unchanged: no domain, domain only, domain plus full Meta-Skill, and domain plus minimal reminder. The native mode stages real Skill files in separate Git roots. No treatment is selectively omitted after viewing outputs.
- Requested generator: `gpt-6.1-sol`, reasoning effort low, seed 20261027, one repeat, maximum 12 generation calls. The exact resolved model revision is not observed and will not be guessed.
- Existing ChatGPT subscription authentication is used. The subscription-only adapter removes API-key environment variables for the child and checks login status. No credits are purchased and no reset coupon is used.
- No retry or answer replacement is allowed. Failed, missing and aborted attempts are retained. Quota is checked between small batches; shared account usage is not attributed entirely to this project.
- Primary comparisons: C-D and C-B. With only three case clusters, no confidence interval, significance or general performance claim is justified.
- A fresh reviewer task receives only re-keyed output packets, the rubric and blank CSV. It does not receive generation prompts, condition labels, seed, map, runtime metadata or expected treatment ranking. It is **model-assisted review**, not independent human evidence.
- Review gates apply to output-text requirements only. Answer-only packets cannot establish no-browsing/no-sending/no-file-write behavior. The report must retain this scope explicitly.
- The fixed quality weights remain goal fit 30%, correctness 30%, judgment 20%, useful originality 10%, efficiency 10%. For deterministic tasks, appropriate exactness is valuable; extra novelty or visible reasoning is not a benefit.
- Ties, losses, missingness, failed gates and extra token/latency cost will be reported. Inconclusive results will not motivate changing the same benchmark or prompt until a win appears.

Two separate preliminary probes precede the pilot: one unmodified-core strict JSON native smoke call, and one probe-only modified Skill-body code test. Matching unpredictable body-only codes establishes body accessibility in that probe; it does not prove that the original Meta-Skill improves judgments or that the host is uncontaminated. These probes are not included as pilot outcome samples.
