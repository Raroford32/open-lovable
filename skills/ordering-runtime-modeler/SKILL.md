---
name: ordering-runtime-modeler
description: "Model adversarial execution reality: ordering sensitivity (same-block bracketing, bundling, multi-tx setup/action) and runtime/precompile trust boundaries used as “proof” in value-bearing paths. Use when building `codegraph/layers/L21_ordering_model.md`, when hypotheses depend on ordering, or when the protocol relies on runtime validation for authority/backing checks."
---

# Ordering + Runtime Modeler

## Output (L21 ordering model + runtime/TCB notes)
In `codegraph/layers/L21_ordering_model.md`, record per hypothesis/primitive:
- ordering-independent / ordering-sensitive / multi-tx
- what must persist across tx (if multi-tx)
- smallest ordering falsifier plan (before/after bracketing, same-block)

Also record runtime/TCB assumptions in:
- `codegraph/layers/L12_external_systems.md` (trust assumptions)
- `codegraph/layers/L19_control_plane.md` (if runtime validates authority/backing)

## Procedure
1) Classify ordering dependence for each top-ranked hypothesis.
2) For ordering-sensitive hypotheses, write two falsifier variants:
   - “attacker before victim” and “attacker after victim” (or equivalent bracketing)
3) For multi-tx hypotheses, write explicit setup/action split and why state persists.
4) Map runtime/precompile trust boundaries:
   - what message/acceptance is treated as proof
   - where that proof is coupled to accounting/custody changes
5) Bind assumptions to invariants (so falsifiers can disprove them).

## References (load only as needed)
- `/root/.codex/skills/layered-codegraph-creator/references/ordering-harness.md`
- `/root/.codex/skills/layered-codegraph-creator/references/runtime-tcb-mapping.md`
