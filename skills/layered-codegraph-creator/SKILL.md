---
name: layered-codegraph-creator
description: Manual, evidence-driven creation of complete layered codegraphs (SSOT nodes/edges/layers) for smart-contract protocols across languages and runtimes, plus invariant-first scenario synthesis and fork/sim falsification to discover novel, compositional exploit routes without relying on predefined vulnerability taxonomies.
---

# Layered Codegraph Creator

## Purpose
Build a complete, queryable, protocol model (a layered codegraph derived strictly from code + build config), then use that model to **derive invariants** and **synthesize novel, compositional scenarios** that attempt to falsify those invariants under permissionless, real-chain constraints.

This skill is intentionally designed for “already-audited” systems where known vulnerability pattern matching has low yield. The objective is not to recognize a pattern; the objective is to *create a falsifiable hypothesis* by composing unrelated edges/levers until a measurable bad state becomes reachable.

## Core operating principles (optimize for unknown unknowns)
- Use evidence-first modeling: derive every node/edge from actual code/config; avoid assumptions.
- Use capability language, not vulnerability labels: express hypotheses as “a normal user can force state X,” not as a category name.
- Use multi-pass reading: read the full codebase multiple times with different goals; treat each pass as incomplete.
- Use self-evolving investigation: after each falsifier attempt, record learnings, mutate hypotheses, and update the codegraph + invariants.
- Use anti-bias discipline: prevent premature narrowing; prefer breadth before focus.

Operating stance for battle-tested targets:
- Assume a permissionless, economically meaningful weakness exists in the live protocol state.
- Treat traditional “known-pattern hunting” as low-yield.
- Treat repeated falsifier failures as normal; require learning + mutation, not abandonment.
- Treat value as the objective: anchor every scenario in a concrete asset/custody target and a measurable delta.

## Investigation posture (do not try to prove safety)
- Treat “prove safe / no issue exists” as an invalid subgoal for this target class.
- Report interim results only as:
  - “no promoted scenario yet” + current evidence level(s) + next 3 mutations.
- If reasoning converges to “safe,” treat it as bias and restart from invariant negations + dependency cones.

## Creativity enforcement (escalate beyond “primary” hypotheses)
- Treat one-step or single-module hypotheses as warm-up only.
- Require composed hypotheses per top target state X:
  - state shaping + settlement/extraction.
- Require at least one fusion attempt when stuck:
  - keep state shaping from hypothesis A, attach extraction/settlement from hypothesis B.
- Require at least one cross-module route if the protocol is modular.

## Persistence rule (do not stop because “nothing obvious”)
- If a session must end due to time/context, do not conclude safety.
- Output:
  - hypothesis ledger excerpt
  - what was disproved/blocked and why
  - next mutation plan (top 3)
- Stop only under `AGENTS.md` stop conditions.

## Reality + safety gates
- Permissionless by default: do not assume stolen keys/admin collusion/off-chain coercion. Treat privilege only if it is obtainable via a publicly reachable state transition.
- Fork/sim proofs only: treat scenarios as *hypotheses* until a fork/sim test demonstrates a measurable delta.
- Safe output: avoid packaging results as real-world draining instructions. Prove invariant violation and quantify delta in-test.

## Mainnet reproducibility gate (promotion rule)
- Treat a scenario as **promoted** only if it reproduces on a **latest mainnet fork** with all permissionless preconditions satisfied (paused flags false, caps/limits live, liquidity present).
- Allow earlier-stage hypotheses to exist without fork proof, but label them clearly as *unproven* and drive them toward the smallest falsifier.
- If a hypothesis only works on an old block or under non-live state, label it explicitly as **not currently reproducible** and do not elevate it.
- Record the exact fork block and the on-chain gating checks (pause/cap/guardian) that were verified.

## Schema hygiene (no predefined schema, no artificial caps)
- Start with an empty schema and let the code define it.
- Declare every node/edge type before use in `codegraph/00_schema.md`.
- Prefer reuse of existing types when semantics match; introduce a new type only when a code construct cannot be represented otherwise.
- Maintain a label map in `codegraph/00_schema.md` if renaming types, and treat helper scripts as optional if a non-default schema is used.

## Workflow (use this every time)
0. Establish fork reality and deployed topology (required for late-stage audits):
   - Create a `deployment_snapshot.md` in the target protocol workspace using `references/fork-reality-recon.md`.
   - Use `AGENTS.md` Phase 0/0b to standardize fork blocks and gating checks.
0b. Run a multi-pass full-read protocol to maximize coverage before narrowing; use `references/reading-pass-protocol.md`.
0c. Mine explicit intent and map it to invariants; use `references/intent-mining.md`.
1. Set up the SSOT layout in `codegraph/` (schema, nodes, edges, layers). Use Markdown only.
2. Follow L1-L14 in `references/layered-codegraph-manual.md` to achieve complete coverage.
3. Derive the schema from the code as you go (start empty; declare types before use). Ensure `codegraph/00_schema.md` contains `## Node Types` and `## Edge Types` sections for compatibility with `scripts/validate_codegraph.py`.
4. Model language-specific constructs via `references/language-mapping.md` (extend schema only when required by the code).
5. Model value-bearing truth explicitly:
   - custody vs ledger vs claims via `references/asset-custody-mapping.md`
   - units/scale/rounding/drift via `references/numeric-semantics.md`
6. Build an asset objective map (assets → custody locations → measurement functions → exit measurement) and require every scenario to reference it (see `references/asset-custody-mapping.md` and `AGENTS.md`).
7. Mine invariants from the codegraph using `references/invariant-mining.md` and write them into L14.
8. Synthesize scenarios by composing multi-module edges/levers (without taxonomy) using `references/scenario-synthesis.md`.
9. Convert scenario hypotheses into falsifiers using `references/falsifier-harness.md`, then run fork/sim proofs.
10. Record learnings and mutate hypotheses (L18). Each mutation may require updating nodes/edges and revisiting invariants.
11. Run execution discipline from `AGENTS.md` (evidence ladder, hypothesis ledger, latest-fork promotion gate) and portfolio control from `references/investigation-os.md`.
12. Stop only after the manual’s completeness gates and the protocol-specific checklist are fully closed.

## Required outputs
- `codegraph/00_schema.md` (schema used; include label map if any)
- `codegraph/01_nodes.md` (all nodes with stable IDs)
- `codegraph/02_edges.md` (all edges with types + attributes)
- `codegraph/layers/` (L1-L14 per the manual; L15-L22 for exploit discovery extensions)
- `codegraph/diagrams/` (optional renders; never replace SSOT)

## Quality bar
- The graph must be explainable, queryable, and complete.
- Every edge must point to a declared node.
- Every entrypoint, state change, external call site, authority gate, and asset movement is represented.
- Every critical accounting/auth/control-plane variable is tied to at least one invariant and at least one falsifier attempt.

## Resources
- `references/layered-codegraph-manual.md` (full workflow, layers, completeness gates)
- `references/language-mapping.md` (language-agnostic mapping guidance)
- `references/fork-reality-recon.md` (deployment snapshot + fork reality reconnaissance)
- `references/asset-custody-mapping.md` (custody vs ledger vs claims)
- `references/numeric-semantics.md` (units/scale/rounding/drift surfaces)
- `references/balance-sheet-assembly.md` (construct protocol balance sheet → system-level invariant targets)
- `references/invariant-mining.md` (derive invariants from code + SSOT)
- `references/scenario-synthesis.md` (compose edges/levers into novel scenarios)
- `references/external-influence-budgets.md` (model external inputs as measurable influence budgets)
- `references/control-plane-mapping.md` (upgrade/admin/governance/delegation as first-class surfaces)
- `references/approval-surface-mapping.md` (approvals/allowances as latent custody surfaces)
- `references/ordering-harness.md` (ordering-sensitive and multi-tx scenario discipline)
- `references/cycle-mining.md` (profit-positive loop discovery)
- `references/runtime-tcb-mapping.md` (precompiles/runtime validation as TCB dependencies)
- `references/anti-bias-prompts.md` (prevent premature narrowing; capability rewrite prompts)
- `references/exploit-primitives.md` (capability-first primitive cards)
- `references/operator-mining.md` (invent new composition operators from semantic discontinuities)
- `references/falsifier-harness.md` (fork/sim proof template + friction checklist)
- `references/investigation-os.md` (portfolio control, progress metrics, checkpoint/resume discipline)
- `references/reading-pass-protocol.md` (multi-pass full-read coverage protocol)
- `references/intent-mining.md` (intent extraction → invariants + target states)
- `references/rpc-ethersacnv2.md` (RPC + Etherscan v2 API source of truth)
- `AGENTS.md` (Foundry-backed execution playbook: evidence ladder, hypothesis ledger, promotion gate)
- `scripts/validate_codegraph.py` (SSOT consistency check; `python3 scripts/validate_codegraph.py codegraph`)
- `scripts/triage_entrypoints.py` (optional ranking helper; assumes canonical edge labels unless adapted)
