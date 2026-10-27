# Illustrative decision examples — NOT benchmark outputs

These are **hand-authored illustrations**, not responses from real A/B/C model runs. Do not cite them as measured performance.

## Open visual brief

**User:** "Create a 5-slide underground music exhibition deck; kinetic culture-magazine mood."

**Domain Skill default (optional):** white background + blue lines + centered title.

**Overgeneralized behavior (undesirable):** blindly applies blue corporate slides despite the user's specific editorial request.

**Judgment-aware behavior (desired, not guaranteed):** retains legible titles and technical slide checks, but explores editorial grids, stronger typographic hierarchy and collage-like visual rhythm aligned with the user's stated audience.

## Hard requirement

**User:** "Keep the mandatory 24px clear area around the logo. Make everything else daring."

**Bad 'creativity enhancement':** shrinks clear-space to achieve a more visually balanced layout.

**Good judgment:** keeps at least 24px and uses color, composition and imagery elsewhere for experimentation.

## Deterministic output

**User:** "Output exactly JSON `{"status":"ok","count":2}` and nothing else."

**Good judgment:** returns exactly the required JSON. No explanations or visual flourish. The meta-Skill should effectively be a no-op.

## Skill conflict requiring authority, not cleverness

**Scenario:** a higher-priority, authorized output contract requires a fixed schema, while a domain Skill suggests extra decorative fields.

**Good judgment:** preserve the fixed schema; omit optional extras. If the competing demands are both mandatory and irreconcilable, explain or escalate rather than quietly rewriting either.
