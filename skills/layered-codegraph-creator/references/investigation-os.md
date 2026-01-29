# Investigation OS (portfolio control for “keep going until E3”)

Goal: turn “be creative and never give up” into a mechanically enforced investigation loop.

This document defines how to:
- manage a hypothesis portfolio,
- measure progress without pretending safety,
- checkpoint/resume without losing momentum,
- and force escalation when thinking collapses into primary/simple ideas.

## Non-negotiable rules
- Do not optimize for a single favorite hypothesis until something is promoted (E3).
- Do not use “no obvious issues” as a terminal state.
- Every iteration must produce **one of**:
  1) an evidence upgrade (E0→E1→E2→E3), or
  2) a model expansion (new SSOT semantics → new invariants/targets), or
  3) a portfolio mutation (replace dead hypotheses/targets with new ones).

## Required artifacts (in the target protocol workspace)
- `hypothesis_ledger.md` (mandatory; see [`AGENTS.md`](../AGENTS.md:102))
- `unknowns.md` (mandatory; an explicit unknowns ledger)
- `resume_pack.md` (optional but recommended; auto-generated at every stop)

If these surfaces exist in code, also create the corresponding discovery layers (do not treat as optional):
- `codegraph/layers/L19_control_plane.md` (upgrade/init/governance/delegation mapping)
- `codegraph/layers/L20_approval_surface.md` (approval/allowance “latent custody” mapping)
- `codegraph/layers/L21_ordering_model.md` (ordering classification + ordering falsifier plans)
- `codegraph/layers/L22_cycle_mining.md` (conversion graph + cycle hypotheses + drift probes)

## Portfolio structure (the minimum viable search state)
Maintain:
- **Target states X**: pick 3–7 invariant negations at a time.
- **Hypotheses per target**: keep 3 live hypotheses per X.

Diversity constraint per target state X:
- H1: short/simple (warm-up) — minimal chain.
- H2: fusion — state shaping from route A + extraction/settlement from route B.
- H3: cross-module or external-influence — must traverse an external boundary or cross a module boundary.

If the protocol is not modular, interpret “cross-module” as “cross-phase/cross-dependency/cross-measurement-point.”

### Coverage gates (do not allow the portfolio to ignore these)
Across the *whole portfolio* (not per X), ensure at least one live hypothesis exists for each surface that exists in code:
- **Control-plane**: a route where a normal user changes future-behavior control, then monetizes (see `references/control-plane-mapping.md`).
- **Approval surface**: a route where user approvals can be converted into attacker-chosen token movement (see `references/approval-surface-mapping.md`).
- **Ordering-sensitive**: a route that depends on same-block ordering or multi-tx setup/action (see `references/ordering-harness.md`).
- **Cycle drift**: a route that is a profit-positive loop (cycle-once + cycle-N probes) (see `references/cycle-mining.md`).
- **Runtime/TCB boundary**: a route where acceptance by a runtime/precompile/system module is treated as proof of backing/authority (see `references/runtime-tcb-mapping.md`).

If you cannot produce a hypothesis for a surface that exists, that is an explicit **unknown**—write it in `unknowns.md` and treat it as a model expansion task, not “nothing there.”

## Iteration macro (run this loop)

### 1) Select what to try next (avoid premature convergence)
Score each hypothesis roughly (do not overfit):
- **Delta bound** (how much could move) × **reachability** (how live) ÷ **cost** (time/capital/complexity)

Pick:
- 1 exploitation attempt (highest score), and
- 1 exploration attempt (lowest certainty but new lever/operator).

Exploration attempt rule (mandatory):
- Prefer an exploration attempt that advances a currently-uncovered surface from the coverage gates above.

### 2) Define the smallest falsifier step
Before writing a full exploit test, pick the smallest observation that collapses the biggest unknown:
- E1: “is the gate real / value readpoint correct?”
- E2: “does the state move in the predicted direction?”

If the falsifier requires too much setup, shrink the hypothesis until it becomes testable.

### 3) Execute, measure, and classify
After running the falsifier:
- Update `hypothesis_ledger.md` status (E0/E1/E2/E3 + proved/disproved/blocked/unknown).
- Record `whatKilledIt` or `newLeverLearned`.
- Record explicit deltas (custody/ledger/claims/debt).

### 4) Mutate (one change at a time)
Apply exactly one mutation operator per iteration so learning is attributable.
Mutation examples (capability-first):
- change measurement point
- change ordering / split into multi-tx
- change asset path
- change external influence budget
- fuse with another hypothesis

### 5) Escalate if stalled
If 5 iterations occur with no evidence upgrade and no new SSOT semantics:
- force an escalation pass:
  - pick a different target state X,
  - perform operator mining,
  - or expand the deployment snapshot/instance enumeration.

## Checkpoint / resume protocol (never stop “empty”) 
When forced to stop (time/context):
Write `resume_pack.md` with:
- fork metadata used
- current portfolio (targets + 3 hypotheses each)
- last 3 falsifier results
- next 3 mutations (specific)
- missing hard requirements (only if truly blocking)

Treat `resume_pack.md` as the handoff contract to the next session.

## Progress metrics (how to know you are doing real work)
Track counts (rough is fine):
- how many invariants have at least one falsifier attempt
- how many entrypoints have at least one hypothesis card
- how many external inputs have influence budgets (E1 checked)
- how many fusion attempts were tried
- how many control-plane variables have invariants + falsifier stubs (L19)
- how many spender/approval surfaces are mapped with at least one falsifier plan (L20)
- how many top-ranked hypotheses have explicit ordering classification + an ordering attempt if sensitive (L21)
- how many conversion cycles have at least a cycle-once and cycle-N drift probe plan (L22)
- how many runtime/precompile dependencies have an explicit “assumed guarantee” + binding invariant (L12/L19)

If any metric is near-zero, the investigation is not “advanced” yet.

