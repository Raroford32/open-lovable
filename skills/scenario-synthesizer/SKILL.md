---
name: scenario-synthesizer
description: "Synthesize novel, compositional, permissionless exploit hypotheses from invariant negations and SSOT edges (state shaping + settlement/extraction), including fusion, cross-module routes, external influence budgets, operator mining, and cycle mining. Use when generating hypotheses per target state X, writing L15–L18/L22 layers, or when stalled and needing creative escalation beyond primary patterns."
---

# Scenario Synthesizer

## Output (primitives + hypotheses)
For each target state X, produce 3 hypotheses (mandatory diversity):
- H1 warm-up (minimal chain)
- H2 fusion (state shaping + extraction from different routes)
- H3 cross-module or external boundary

Record each hypothesis in:
- `hypothesis_ledger.md` (mandatory), and
- `codegraph/layers/L16_primitives.md` (primitive cards), and/or
- `codegraph/layers/L15_attack_surface.md` (entrypoint levers + guards)

If the protocol has conversions, also update:
- `codegraph/layers/L22_cycle_mining.md`

## Procedure
1) Start from invariant negations (target states X).
2) For each X, identify:
   - **state shaping** levers (inputs/order/time/caller type/external influence)
   - **extraction/settlement** route (custody/claim/debt delta + exit measurement)
3) Force composition
   - add at least one orthogonal lever if the route is too “single-module”.
4) Force fusion when stuck
   - keep state shaping from hypothesis A, attach extraction from hypothesis B.
5) Run cycle mining when conversions exist
   - propose cycle-once and cycle-N drift probes (amount-regime variants).
6) Record the smallest falsifier per hypothesis (hand off to Foundry).

## References (load only as needed)
- `/root/.codex/skills/layered-codegraph-creator/references/scenario-synthesis.md`
- `/root/.codex/skills/layered-codegraph-creator/references/exploit-primitives.md`
- `/root/.codex/skills/layered-codegraph-creator/references/operator-mining.md`
- `/root/.codex/skills/layered-codegraph-creator/references/cycle-mining.md`
- `/root/.codex/skills/layered-codegraph-creator/references/external-influence-budgets.md`
- `/root/.codex/skills/layered-codegraph-creator/references/anti-bias-prompts.md`
