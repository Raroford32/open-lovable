# Reading Pass Protocol (max-coverage, zero-label bias)

Goal: enforce a full, multi-pass read that captures every discoverable semantic before narrowing.

## Non-negotiable rules
- Read the entire codebase at least twice with different objectives.
- Treat each pass as incomplete; after each pass, update SSOT + unknowns.
- Convert every insight into one of: SSOT node/edge, checklist item, invariant candidate, or unknown to resolve.

## Required artifacts (in the target protocol workspace)
- `unknowns.md`
- `protocol_checklist.md` (or the protocol-specific checklist in L1/L14)
- `reading_log.md` (optional but recommended; one section per pass)

## Pass 0 — Build + artifact pass (no code execution required)
- Inventory build configs, compiler settings, remappings, codegen outputs.
- Record compiler flags, optimizer settings, and conditional compilation gates.
- Record generated artifacts (ABIs, bindings, deployment outputs) and where they feed runtime behavior.
- Add checklist items tied to each artifact and feature gate.

## Pass 1 — Surface + topology pass
- Enumerate modules and entrypoints; populate L1-L6.
- Create or update `deployment_snapshot.md` and confirm topology.

## Pass 2 — Authority + gating pass
- Walk every entrypoint and record every gate (roles, requires, caps, pauses).
- Update L7 and the live gating checklist.

## Pass 2b — Control-plane pass (future behavior control)
- Map upgradeability/admin/initializer/governance/delegation surfaces as first-class semantics.
- Identify every control variable that can change future behavior (implementation pointers, admins, executors, registries, allowlists).
- Record permissionless acquisition routes (deployment ordering, governance vote capture, delegated execution roots).
- Create/update `codegraph/layers/L19_control_plane.md`.
- Follow `references/control-plane-mapping.md`.

## Pass 3 — Storage + state pass
- Map storage layout, caches, snapshots, epoch markers, and phase variables.
- Update L8 and L13; record any state that is measured indirectly.

## Pass 4 — Value + accounting pass
- Map custody, ledgers, conversions, rounding, and fee paths.
- Update L11 and `numeric-semantics.md` annotations.

## Pass 4b — Approval surface pass (user approvals as latent custody)
- Enumerate user-facing spenders (routers/vaults/executors/legacy contracts) and how approvals are consumed.
- Identify any route where the spender can move tokens from an owner that is not strictly bound to `msg.sender` (or an explicit signed authorization).
- Create/update `codegraph/layers/L20_approval_surface.md`.
- Follow `references/approval-surface-mapping.md`.

## Pass 5 — External dependency + influence pass
- Map every external system and its readpoints.
- Assign influence budgets and record evidence plans (L12).

## Pass 5b — Runtime / precompile TCB pass (chain logic as a dependency)
- Enumerate any runtime/system/precompile dependencies used in value-bearing paths.
- For each, write the assumed guarantee (“if accepted, what is presumed proven?”) and bind it to accounting.
- Follow `references/runtime-tcb-mapping.md`.

## Pass 6 — Intent + assumption pass
- Run `references/intent-mining.md`.
- Convert explicit intent into invariants; record mismatches as target states.

## Pass 7 — Scenario synthesis pass
- Use invariants to generate target states and scenario candidates.
- Produce falsifier stubs for the highest-value targets.

## Pass 7b — Ordering + cycle pass (structure-first discovery)
- For top-ranked hypotheses, classify ordering dependence (ordering-independent / ordering-sensitive / multi-tx) and add an explicit ordering falsifier plan.
- Build at least one candidate conversion cycle and write cycle-once + cycle-N drift probes.
- Create/update:
  - `codegraph/layers/L21_ordering_model.md` (see `references/ordering-harness.md`)
  - `codegraph/layers/L22_cycle_mining.md` (see `references/cycle-mining.md`)

## Iteration rule (self-evolving)
- After any falsifier failure without a clear root cause, rerun the most relevant pass and expand SSOT.
- After two consecutive failures, rerun Pass 0 or Pass 6 to avoid missing intent/constraints.

## Stop conditions
- Stop only when:
  - the protocol-specific checklist is closed,
  - the unknowns ledger is resolved,
  - top-ranked invariants have falsifier attempts,
  - and (if the surfaces exist in code) L19–L22 are created with at least one falsifier attempt or falsifier plan per surface.
