# Scenario Synthesis (compose edges into novel, permissionless routes)

Goal: turn a complete, layered codegraph into **new exploit scenarios** by *composition*, not by matching a known vulnerability name.

This is the phase that tends to surface “unknown” vulnerabilities: combine multiple small, locally-correct behaviors into a globally bad state.

## Non-negotiable rules
- Use capability language only.
  - Write “a normal user can force state X” (target bad state), not a category name.
- Use evidence-first pointers.
  - Every scenario must point to a minimal chain of SSOT nodes/edges that makes it plausible.
- Use permissionless assumptions.
  - Do not assume stolen keys/admin collusion/off-chain coercion.
  - If privilege appears, treat it only if it is obtainable via a publicly reachable state transition.
- Use fork/sim proofs.
  - Treat every scenario as a hypothesis until a falsifier produces a measurable delta.
- Follow the safe-output rule.
  - Prove invariant violation and quantify delta in-test; avoid packaging as a real-world drain recipe.

## Inputs (required)
- SSOT: `codegraph/01_nodes.md`, `codegraph/02_edges.md`
- Coverage layers: L5 (entrypoints), L7 (authority), L8 (storage), L10/L12 (external calls/trust), L11 (value/accounting), L13 (state machine), L14 (invariants)

## Output (what to write)
Write scenarios as hypothesis cards (one per candidate route):
- **Target state X**: an invariant-violation state (or a clearly wrong accounting relation).
- **Target asset and custody**: which asset/custody location(s) or claims are expected to change; what “profit” means in measurable terms.
- **Broken assumption**: the implicit belief the system relies on.
- **Permissionless preconditions**: concrete on-chain state + caller context + ordering/timing.
- **Route sketch**: a minimal sequence of calls/transitions that should move the system toward X.
- **Measurable effect**: which custody/ledger/claim/debt variables move and in which direction.
- **Exit measurement**: how the delta is measured/quoted on fork (and what exit constraints are assumed).
- **Evidence pointers**: SSOT node/edge chain(s) that justify each step.
- **Smallest falsifier**: the simplest fork/sim test that can disprove it.

## Procedure (coverage-first → focus)

### 0) Establish the “scenario search space” from the codegraph (no prefilled taxonomy)
Derive candidate levers directly from SSOT evidence:
- Every unprivileged entrypoint in L5 is a starting node.
- Every external call edge is a potential semantic discontinuity.
- Every unit conversion or rounding point is a potential drift surface.
- Every trust edge (oracle/DEX/bridge/registry) is a potential influence point.
- Every state machine transition/flag is a potential reachability gate.
- Every control-plane write path (init/upgrade/role/grant/whitelist/governance executor) is a potential permissionless privilege-acquisition lever (see `references/control-plane-mapping.md`).
- Every approval consumption site is a potential “latent custody” lever where user approvals can be converted into transfers (see `references/approval-surface-mapping.md`).
- Every measurement that can be affected by same-block ordering should be treated as an ordering lever (see `references/ordering-harness.md`).

Do not choose a “vulnerability class.” Choose a **target bad state X** and then search for routes.

### 0b) Anchor every target state in an asset objective (do not lose the economic target)
Before writing routes, name the asset/custody objective explicitly:
- Which asset is ultimately being extracted or whose ledger is being falsified?
- Where does the real custody sit, and which function measures it?

If the hypothesis cannot name at least one custody location or measurable claim/debt delta, it is not yet an economic scenario. Return to L11 and `references/asset-custody-mapping.md` and make the value target explicit.

### 1) Start from invariants (L14) and turn them into targets
For each invariant, write its negation as a target state X, in capability form.
Examples (write as states, not labels):
- “Ledger credits exceed real custody increase for asset A at holder H.”
- “Recorded debt decreases without paying the real debt asset.”
- “A check is passed, then invalidated later in the same tx, but the system does not re-check.”

If invariants are weak or vague, expand them using `references/invariant-mining.md` and `references/intent-mining.md` before attempting scenarios.

### 2) Build a dependency cone for the invariant
For each target state X:
1. Identify the `VAR`/`ASSET`/`CUSTODY` nodes involved.
2. Walk edges to find:
   - which functions write the relevant vars
   - which functions read them in checks
   - which functions move the relevant custody balances
   - which external systems influence values used by checks
   - which external *inputs* are consumed, and what their influence budgets are
3. Collect a set of “invariant-relevant functions.”

When a route depends on an external value, replace vague reasoning with an explicit influence budget:
- use `references/external-influence-budgets.md`
- require: influence action + cost model + time window + bound + E1/E2 plan

This produces a concrete search space: entrypoints that can reach invariant-relevant writes/reads.

### 3) Compose a route (build it from SSOT edges)
Construct a candidate route as an ordered chain:
- Start: a permissionless entrypoint.
- Middle: internal calls, external calls, state transitions.
- End: a write/read/custody movement that can make X true.

Do not require the route to be “obviously related.” In compositional exploits, intermediate steps often only exist to *shape state* so a later check accepts an invalid state.

### 4) Apply composition operators (derive them from code constructs)
Use these as *operators*, not as a taxonomy. Each operator is triggered by a concrete code construct.

Before relying on this list, run operator mining:
- Use `references/operator-mining.md` to invent new operators from semantic discontinuities.
- Record operators in L18 so future passes are strictly stronger.

#### Operator A: “Check, then invalidate”
Trigger: a `require`/assert/check that depends on a value that can change later.
Action: search for any subsequent write (same tx or later tx) that can invalidate the checked assumption without triggering a re-check.
Evidence: `READS`/`WRITES` edges plus call ordering.

#### Operator B: “Measure reality at a manipulable point”
Trigger: a function measures balance/cash/price/index from an address or external system.
Action: search for routes where the measured value can be temporarily increased/decreased (callbacks, flash movement, time-of-measurement windows), or where the holder chosen is influenceable.
Evidence: `MEASURES_BALANCE_AT`, custody edges, and external call sites.

#### Operator C: “Unit conversion drift accumulation”
Trigger: integer division, `mulDiv`, exchange rate conversion, share math, fee math, index updates.
Action: search for repetition loops (same call repeated N times) that bias rounding in one direction.
Evidence: conversion expressions + `HAS_UNIT`/`CONVERTS`/`ROUNDS` edges.

#### Operator D: “Cross-module view mismatch”
Trigger: two modules rely on the same conceptual quantity but compute/validate it differently.
Action: search for a route where module A accepts a value that module B does not fully enforce (or enforces under different timing/order).
Evidence: `ACCOUNTING_DEPENDS_ON` edges, shared vars, duplicated formulas.

#### Operator E: “State machine reachability shaping”
Trigger: phase flags/epochs/rounds/pauses that gate behavior.
Action: search for permissionless transitions or edge-state creation that enables a high-impact path (including creating a “rare” state cheaply).
Evidence: `TRANSITIONS`, `ENABLED_IN`, `DISABLED_IN` edges.

#### Operator F: “Control-plane capture, then monetize”
Trigger: a control variable exists that changes future behavior (init/upgrade/admin/whitelist/governance executor).
Action: search for a permissionless route to change that control variable (ordering, governance, delegated execution), then attach the smallest downstream path that realizes a custody/claim/debt delta.
Evidence: control-plane var write paths + guard chain + downstream value-touch edges. Use `references/control-plane-mapping.md`.

#### Operator G: “Approved spender becomes a transfer proxy”
Trigger: a user-approved spender executes caller-chosen targets/calldata (or otherwise uses approvals with an attacker-influenceable `owner`).
Action: search for a route that makes the spender call token movement against a third-party owner that never expressed fresh intent.
Evidence: approval consumption site + executor/target/call boundary. Use `references/approval-surface-mapping.md`.

#### Operator H: “Positive cycle drift”
Trigger: a multi-step conversion loop exists (assets↔shares↔rewards↔swaps) that returns to the same representation.
Action: test whether one full loop yields net positive output under specific amount regimes or repetition.
Evidence: conversion edges + rounding points + any external inputs. Use `references/cycle-mining.md`.

This operator list is intentionally incomplete.
- Add new operators whenever a new code construct creates a semantic discontinuity.
- Record new operators/levers learned in L18 so future passes are strictly stronger.

Each time an operator suggests a route, immediately write the **smallest falsifier** that would disprove it.

### 4b) Run a divergent brainstorm pass (generate candidates before pruning)
Avoid converging too early. Novel exploit scenarios often require trying multiple unrelated compositions before the “real” route appears.

For each target state X:
- Generate multiple distinct candidate routes before discarding any.
- Force diversity by changing exactly one dimension at a time:
  - starting entrypoint
  - caller type/context (EOA vs contract, callback-capable caller, batching/aggregator)
  - ordering (swap call order, split/merge calls into a single tx)
  - phase (pre/post transition, paused/unpaused gates if reachable)
  - external dependency (different oracle/DEX/bridge path if the code supports it)
  - asset selection (different underlying/share/reward token paths)
  - amount regime (dust-sized vs large; repeated N-times loops to probe rounding drift)
  - time (block.timestamp/block.number windows when used)

For each candidate, write a stub hypothesis card immediately:
- Target state X
- Route sketch
- Evidence pointers (SSOT chain)
- Smallest falsifier idea

Do not prune because a component “looks standard” or “has been audited.” Prune only after a falsifier or a concrete guard/reachability argument kills it.

### 4c) Apply mutation operators (novelty by controlled edits)
When a hypothesis is killed, mutate it instead of abandoning the target state.

Mutation operators (apply one per iteration):
- Replace a measurement point:
  - swap a balance/cash accessor used by checks (where the code offers alternatives)
  - move from “measure at protocol address” to “measure at strategy/custodian address” if modeled
- Replace a trust edge:
  - route through a different external system interaction already present in the codegraph
  - shift influence from direct manipulation to state shaping that changes the trusted input indirectly
- Replace a state path:
  - introduce a reachable phase transition before the main action
  - split into multi-tx setup + action when ordering/state persistence matters
- Replace an arithmetic regime:
  - change amounts to trigger different rounding branches
  - repeat a step to test accumulation bias
- Replace the “who benefits” direction:
  - switch from “attacker gains custody” to “attacker reduces debt/obligation”
  - switch from “profit extraction” to “protocol insolvency state” (then search for extraction)
- Fuse hypotheses (composition from unrelated parts):
  - keep state shaping from hypothesis A (the part that makes a check accept something)
  - attach extraction/settlement from hypothesis B (the part that realizes the delta)

### 5) Validate constraints (before spending time)
For each candidate scenario:
- List all guards/caps/pauses and whether they are live.
- List required capital/liquidity assumptions.
- Decide whether the scenario is single-tx (preferred) or multi-tx (allowed; document ordering risk).

### 6) Write the falsifier (then learn and mutate)
Use `references/falsifier-harness.md`.

After each falsifier attempt:
- Record what killed it (exact check and location).
- Record what lever was learned.
- Mutate the hypothesis (change one lever/ordering/asset/state) and try again.
- If a new construct is discovered, update SSOT and revisit invariants.

## “Highest intelligence” behavior (what to force internally)
- Refuse to stop at “seems safe.”
- Treat every unknown as a concrete work item (add to checklist).
- Prefer hypothesis mutation over deeper speculation.
- Re-read the code after each major falsifier failure (assume the missing lever is in an unmodeled edge).

## Creativity escalator (avoid “primary vuln thinking”)
When the scenario set collapses into simple one-step ideas, force escalation before proceeding:
- Add one more independent lever to the route (state shaping + extraction).
- Force fusion: merge the best state-shaping hypothesis with the best extraction/settlement hypothesis.
- Increase route length by one edge (add an extra internal/external call boundary).
- Change one axis of the route (caller type, ordering, time/phase, measurement point, asset selection).

Treat this as a required step for battle-tested targets, not as an optional “extra.”

## Self-evaluation gate (ensure enough attempts; detect simplification)
Before concluding that scenario synthesis is “exhausted”:
- Confirm that every scenario card has an explicit target asset/custody and an exit measurement.
- Confirm that each critical invariant has at least one attempted falsifier (proved/disproved/blocked/unknown).
- Confirm that at least one scenario attempts to exploit each:
  - custody vs ledger mismatch surface (if value-bearing)
  - unit/rounding drift surface (if conversions exist)
  - trust edge influence surface (if external dependencies exist)
  - phase/flag reachability surface (if a state machine exists)
  These are not categories; they are structural surfaces derived from SSOT evidence.
- Confirm that at least one scenario is cross-module (edges from multiple modules) if the protocol is modular.
- If any item fails, return to dependency cones and run another divergent brainstorm pass.
