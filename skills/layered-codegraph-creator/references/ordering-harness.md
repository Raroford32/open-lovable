# Ordering Harness (same-block / multi-tx reality)

Goal: stop silently assuming “nice” execution order.
Many economically meaningful routes are:
- **ordering-sensitive** (bracketing / same-block positioning), or
- **multi-tx** (setup then action), or
- **competition-sensitive** (another actor can steal the ordering or the delta).

This file defines a repeatable way to **classify** and **test** ordering dependence without turning notes into operational playbooks.

## Output (required artifact)
Create `codegraph/layers/L21_ordering_model.md`:
- per hypothesis: ordering classification + smallest ordering falsifier plan

Ordering classifications:
- **ordering-independent**: works without special ordering
- **ordering-sensitive**: requires a specific before/after ordering
- **multi-tx**: requires state persistence across txs (document which state and why)

## Minimal evidence rules
- Never write “requires bracketing” without a concrete in-test ordering plan.
- Never write “safe from ordering” without at least one adversarial ordering attempt (E2 disproof).

## How to model ordering in Foundry tests (high-level)
You cannot model the mempool directly, but you can model the *consequences*:
- attacker tx executes before victim tx
- attacker tx executes after victim tx
- two competing attackers exist and one wins
- setup tx executes, then time advances, then action tx executes

### A) Same-block ordering (within one test)
Write the test as a sequence of calls that represent transactions:
- Tx1: attacker pre-shapes state
- Tx2: victim/protocol action
- Tx3: attacker post-shapes/realizes delta

Record which assumptions are necessary:
- “attacker can place tx before” vs “attacker can place tx after”

### B) Multi-tx setup/action
If the route depends on time/epoch/cooldowns:
- Tx1: setup state
- advance block/time
- Tx2: action/realization

In the hypothesis ledger, record:
- what state persists across txs
- what could invalidate it between txs (competition risk)

### C) Competition sensitivity
If a route is likely to be stolen by another actor:
- add an “adversary” address and try the same action between your steps
- record whether your route still yields a delta (or whether it is purely race-based)

## Smallest falsifier templates (choose the smallest one)
- **Ordering flip**: run the exact same steps but swap Tx1/Tx3 and confirm the delta disappears.
- **Interloper insertion**: insert an adversary action between steps and see if your delta survives.
- **Time window**: vary block/time boundaries to see if the route is robust or only works at a narrow window.

## Self-evaluation gate
You are not done if your scenario portfolio lacks:
- at least one ordering-sensitive hypothesis attempt (if the protocol uses AMMs, auctions, or observable state transitions), and
- an explicit ordering classification for each top-ranked hypothesis.

