# External Influence Budgets (turn “trust edges” into measurable levers)

Goal: remove the biggest hidden assumption in late-stage audits:
> “this oracle/DEX/bridge input is (not) manipulable.”

Instead, treat every external dependency input as a **variable with an influence budget**:
- what a permissionless actor can move,
- by how much,
- at what cost,
- under what timing/phase constraints,
- and how to prove it (E1/E2).

This converts L12 from narrative trust descriptions into scenario fuel for dependency cones and falsifiers.

## Non-negotiable rules
- Never write “unmanipulable” without an E1/E2 check.
- Never write “manipulable” without an explicit **influence action** and an explicit **cost model**.
- Prefer *measurable* budgets (bounds, slippage, latency) over opinions.

## Output (what to record)
In the protocol workspace, extend L12 entries with an **Influence Budget** section per dependency input.

Minimum fields (write as a table or bullet list):
- **Input**: the exact value consumed (price/rate/reserve/decimals/router/implementation pointer/etc.).
- **Read point**: which `FUNC` reads it and where it feeds checks/accounting.
- **Influence actions (permissionless)**: concrete on-chain actions that could change the input.
- **Cost and capital**: fees + capital at risk + required liquidity.
- **Time window / latency**: same-tx? block-to-block? epoch-to-epoch?
- **Bound (rough)**: how far can it move before defenses stop it (slippage bounds, oracle bounds, caps)?
- **Defenses present**: min-out, TWAP, staleness bounds, medianization, circuit breakers.
- **Evidence plan**:
  - E1: read the input on fork and confirm the readpoint is live.
  - E2: smallest test that attempts to move it (or prove it cannot be moved under permissionless constraints).

## Minimal schema hooks (declare only if the code requires them)
If influence budgets become complex, add explicit nodes/edges. Examples:
- Node types: `EXT_INPUT`, `INFLUENCE_BUDGET`
- Edge types:
  - `READS_EXTERNAL_INPUT (FUNC -> EXT_INPUT)`
  - `GATES (EXT_INPUT -> CHECK/VAR)`
  - `INFLUENCE_ACTION (EXT_INPUT -> FUNC/EXTSYS)`

If using different names, add a label map in `codegraph/00_schema.md`.

## Procedure

### 1) Enumerate dependency inputs (not just dependency contracts)
From SSOT evidence:
- For every `EXT_CALLS` in L10/L12, extract the *value(s)* returned/used.
- For every hardcoded address that is used as a router/oracle/registry, extract what values are read.

Do not stop at “Chainlink oracle at X.” Identify:
- which price feed(s)
- which decimals/scales
- which freshness checks
- what fallback logic exists

### 2) Bind each input to protocol checks and accounting
For each input:
- Identify the checks that depend on it (solvency, minOut, caps, phase gates).
- Identify the accounting updates that depend on it (share minting, debt, fees, rewards).

If the dependency is “config-like” (router address, implementation pointer):
- Treat it as an input that controls *future behavior*.
- The influence budget is then “who can change config” and “how quickly.”

If the dependency is runtime/precompile/system-contract validation (bridge receive, message acceptance, native modules):
- Treat it as a TCB boundary input (“acceptance implies backing/authority”).
- Extend the model using `references/runtime-tcb-mapping.md` and bind acceptance to accounting in invariants.

### 3) Write a permissionless influence budget
For each input, ask:
- “What can a normal user do that changes the value read at the read point?”

Examples (still capability-first; not a taxonomy):
- Provide/remove liquidity that changes reserves used by price computation.
- Trade against the same pool used by a spot/TWAP oracle.
- Trigger an update function (if permissionless) that changes stored index/price.
- Route through a different path if the protocol selects among multiple inputs.

If no influence action exists, record that as a hypothesis to be tested (E2 disprover).

### 4) Prove the budget cheaply (E1 before E2)
Before building scenarios that depend on influence:
- Confirm the readpoint is live and which address is queried at the fork block.
- Confirm bounds/guards are live (staleness, deviation, min/max).

Treat this as E1.

### 5) Convert budgets into scenario levers
In scenario synthesis dependency cones:
- Replace vague edges like “oracle manipulation” with:
  - a specific `EXT_INPUT`,
  - a specific permissionless influence action,
  - and a bound/cost/time window.

Then fuse:
- a state-shaping influence budget (make a check accept an invalid state)
with
- an extraction/settlement route (realize the measurable delta).

## Self-evaluation gate
Do not accept scenario portfolios that depend on external values unless:
- at least one influence budget is written per used input, and
- each budget has an E1 check and an E2 plan.

