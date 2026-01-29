---
name: invariant-miner
description: "Derive protocol-specific invariants from SSOT + intent + value truth and convert them into explicit target bad states X with measurable deltas. Use when building `codegraph/layers/L14_invariants.md`, selecting target states for scenario synthesis, or when you need computable statements that can be disproved via Foundry falsifiers."
---

# Invariant Miner

## Output (L14 invariants + targets X)
In `codegraph/layers/L14_invariants.md`, write for each invariant:
- statement (computable, tied to concrete vars/assets/roles)
- involved SSOT nodes/edges
- measurement readpoints (how to measure delta on fork)
- negation (target bad state X)
- smallest falsifier idea (what would disprove it)

Also maintain a shortlist of 3–7 target states X to drive scenario synthesis.

## Procedure
1) Collect inputs
   - SSOT semantics from `codegraph/`
   - intent statements (from reading/intent mining)
   - asset objective map (custody/claims/debt + readpoints)
2) Identify critical truth couplings
   - custody ↔ internal ledger ↔ claims/debt
3) Write invariants as bindings, not slogans
   - bind accounting vars to custody readpoints and external dependencies.
4) Write explicit negations
   - turn each invariant into a target bad state X (“a normal user can force X”).
5) Rank targets X by value bound × reachability ÷ cost.

## References (load only as needed)
- `/root/.codex/skills/layered-codegraph-creator/references/invariant-mining.md`
- `/root/.codex/skills/layered-codegraph-creator/references/balance-sheet-assembly.md`
- `/root/.codex/skills/layered-codegraph-creator/references/asset-custody-mapping.md`
