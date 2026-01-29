# Operator Mining (invent new composition operators from code constructs)

Goal: force “beyond-known” creativity without relying on predefined vulnerability categories.

In this skill, an **operator** is not a label (“oracle bug”).
An operator is a reusable *composition move* derived from a concrete semantic discontinuity in the code.

## Non-negotiable rules
- Treat the operator list in [`scenario-synthesis.md`](../references/scenario-synthesis.md:84) as examples only.
- Invent operators whenever new constructs are found.
- Every operator must:
  - cite SSOT evidence (nodes/edges), and
  - immediately produce at least one hypothesis card.

## Output
In the protocol workspace, maintain an **Operator Registry** inside `codegraph/layers/L18_learnings.md`:
- one operator card per discovered discontinuity
- link each operator to at least one hypothesis ID in the hypothesis ledger

Operator card format:
- **Name**: short, structural (not a vuln category)
- **Trigger construct**: exact code pattern / call boundary / state transition
- **Semantic discontinuity**: what “changes meaning” across the boundary
- **Target state X**: which invariant negation it can help reach
- **Route skeleton**: 2–6 steps (entrypoint → … → effect)
- **Evidence pointers**: SSOT node/edge chain
- **Smallest falsifier**: one observation that collapses uncertainty
- **Learned constraints**: what killed it previously (if any)
- **Next mutation suggestion**: one lever to change

## How to mine operators (repeatable procedure)

### 1) Scan for semantic discontinuities (per module and per entrypoint)
While building L9/L10/L11/L12, maintain a “discontinuity log.” Add an item whenever you see:
- **Measurement points**: balance/price/rate/index readpoints (especially cached vs live).
- **Conversions**: assets↔shares, debt↔index, price↔usd, decimals/scale boundaries.
- **State machine boundaries**: phase/epoch/round transitions, pausing, settlement.
- **Authority boundaries**: role changes, config updates, initialization.
- **External call boundaries**: calls with callbacks, try/catch fallbacks, delegatecall boundaries.
- **Duplicated views**: same concept computed in multiple modules or multiple ways.
- **Batching/aggregation**: multicall, meta-transactions, “execute” routers.
- **Time dependence**: block.timestamp/number, TWAP windows, delayed settlement.

Do not classify these as “vulns.” Classify them as “meaning can diverge here.”

### 2) Turn each discontinuity into an operator
For each discontinuity item, write an operator card.

Naming rule:
- name the discontinuity, not the outcome.
  - Good: “Cached value used after external state change,” “Two modules compute the same quantity differently.”
  - Bad: “oracle exploit,” “reentrancy.”

### 3) Force at least one hypothesis per operator
Immediately create one hypothesis card that uses the operator:
- pick a target state X
- use the operator as the route generator
- define the smallest falsifier

### 4) Promote operators by learning
When a falsifier kills a hypothesis:
- do not delete the operator
- update the operator card with “learned constraints” and “next mutation suggestion”

This is how the system becomes strictly stronger over time.

## Self-evaluation gate
If scenario generation becomes repetitive:
- count how many operator cards exist in L18
- if low, you are not mining operators; restart at Step 1.

