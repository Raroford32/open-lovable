---
name: protocol-reading-intent
description: "Multi-pass full-read protocol comprehension and intent extraction: derive “what the system must guarantee” from code/comments/docs and turn it into explicit intents, assumptions, and invariant candidates. Use when starting a new protocol, when mining invariants, when building the SSOT codegraph, or when stuck and needing model expansion instead of repeating shallow hypotheses."
---

# Protocol Reading + Intent Mining

## Outputs (artifacts)
- An “intent ledger” captured in either:
  - `codegraph/layers/L14_invariants.md` (preferred), or
  - a dedicated `intent_ledger.md` (if you want it separate)
- For each intent: a mapping to at least one invariant candidate or an explicit “gap/unknown”

## Multi-pass reading discipline (do not do a single skim)
1) **Pass 0: Alignment + intent**
   - Identify deployable units, upgrade wiring, and external dependencies.
   - Extract explicit intent statements (“must”, “cannot”, “always”, “only if”) from docs/comments/code.
2) **Pass A: Enumerate everything**
   - Inventory all files/modules and their responsibilities.
   - Identify state-holding modules and accounting modules.
3) **Pass B: Authority + storage**
   - List every authority gate, role, owner, guardian, and “caller class” assumption.
   - List every critical storage variable and what it measures.
4) **Pass C: Per-entrypoint deep dive**
   - For each unprivileged entrypoint: levers, guards, state transitions, external calls.
5) **Pass D: System truth**
   - Identify where the system asserts equivalence between:
     - custody ↔ internal ledger ↔ claims/debt
   - Identify where it relies on:
     - oracles, adapters, runtime/precompile validation, or off-chain assumptions.

## Intent → invariant conversion (capability-first)
For each intent, write:
- the “bad state” negation (target state X)
- what asset/custody/claim/debt it constrains
- the readpoints that measure it (how you will measure the delta on fork)
- the smallest falsifier that would disprove it

## References (load only as needed)
- `/root/.codex/skills/layered-codegraph-creator/references/reading-pass-protocol.md`
- `/root/.codex/skills/layered-codegraph-creator/references/intent-mining.md`
- `/root/.codex/skills/layered-codegraph-creator/references/anti-bias-prompts.md`

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
