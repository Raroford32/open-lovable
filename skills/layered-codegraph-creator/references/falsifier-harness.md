# Falsifier Harness (fork/sim proofs without “drain guides”)

Goal: convert a hypothesis into a reproducible, measurable, permissionless proof on a fork/sim.

## Template (fill this per primitive)
- **Target state X**: the invariant violation or accounting divergence you expect.
- **Setup**: the minimal on-chain state needed (balances, approvals, listings, caps, oracle state, etc.).
- **Action**: the smallest call sequence (single tx if possible).
- **Ordering classification** (required if any step is ordering-sensitive):
  - ordering-independent / ordering-sensitive / multi-tx
  - include the smallest ordering falsifier plan (see `references/ordering-harness.md`)
- **Cost (raw + normalized)**:
  - gas used (units) for the minimal call sequence
  - fees paid (flash fees, DEX fees, protocol fees), if any
  - any required capital/input assets (if any), reported as:
    - `token` (symbol + address), `decimals`
    - `raw` (base units integer)
    - `normalized` (human units decimal string)
  - any capital locked/at-risk (collateral, LP shares, liquidation exposure), if any
- **Post-condition**: a measurable delta:
  - protocol custody decreases, or
  - attacker claim increases, or
  - attacker debt decreases,
  - plus the exact variable(s) that became inconsistent.
- **Derived (optional but high-signal)**:
  - ratios (`reward/delta`, `profit/capitalIn`)
  - efficiency (`profitPerGas`, `rewardPerGas`)
  - exit value: quote `delta`/`profit` into a reference stable asset (USDC/USDT) and record the quote path + units
- **Falsifier**: what observation would disprove the primitive immediately.

## Disproof is a success (per-hypothesis)
Negative results are expected. When the smallest test disproves a hypothesis:
- make the disproof explicit (delta == 0 or guard/revert)
- record the exact killer (check/guard/rounding/ordering)
- mutate one lever and retry

Disproof is not “protocol safe.” It only closes the specific hypothesis.

## Production friction checklist (encode it in the test)
- **Permissionless**: only public entrypoints; no assumed roles or stolen keys.
- **Ordering risk**: if the primitive needs a specific order, classify it and force the order in-test; also try an adversarial order (see `references/ordering-harness.md`).
- **MEV interference**: note if a third party can capture it by reordering.
- **Revert fragility**: identify the one external call failure that kills it.
- **Built-in defenses**: slippage/min-out/caps/pauses/oracle bounds; test whether they block *the capability*.

## Multi-agent / competition harness (required for “battle-tested” targets)
Late-stage failures often depend on *who else can act* (keepers, liquidators, arbitrageurs, searchers), not just whether one tx works.

For each falsifier, add a minimal “competition check” section:
- **Actors**:
  - attacker (permissionless)
  - competitor (another permissionless actor with the same capabilities)
- **Race model** (approximation):
  - reorder two sequences (competitor-first vs attacker-first)
  - if multi-tx, also test interleaving across blocks (roll/warp as needed)
- **Capture test**:
  - if competitor can realize the same measurable delta (or prevent attacker), record it.
- **Outcome classification**:
  - *non-stealable*: attacker profit survives competitor ordering
  - *stealable*: competitor can capture; record whether the scenario still represents a protocol invariant violation or only an ordering-dependent opportunity
  - *blocked by ecosystem*: keepers/liquidators restore invariants before extraction is possible

Record these in the hypothesis ledger under `exitMeasurement` + `permissionlessPreconditions`:
- whether ordering is required
- whether MEV can steal it
- whether attacker still wins under competition

## “Is this live?” checklist (avoid dead hypotheses)
- **Paused/disabled**: confirm the relevant entrypoints/markets aren’t gated by a live pause flag.
- **Caps/limits**: check borrow caps, mint limits, per-user TVL limits, min-out/max-in thresholds.
- **Oracle reality**: confirm the reference value used in checks is obtainable/manipulable under your stated preconditions.
- **Token reality**: if the primitive depends on weird token behavior, use a token that actually has that behavior (or model it explicitly in-test).
- **Liquidity reality**: if value must exit through a DEX/bridge, include slippage bounds and route constraints in the test.

## Keeper / liquidator ecology (permissionless realism)
If the protocol has automated actors (keepers/liquidators/arbs) that are permissionless:
- Identify their public entrypoints and what they can restore/change.
- In falsifiers, add a “keeper interference attempt”:
  - execute the keeper/liquidator action between attacker steps (or immediately after)
  - measure whether the attacker’s delta persists or is neutralized

Treat “ecosystem restores state” as a real constraint, not a dismissal.

## After-action loop (self-evaluation)
After running the falsifier, write down:
- **Result**: proved / disproved / blocked by guard / unknown (needs more evidence).
- **What killed it (if killed)**: the exact condition and where it lives (guard/check/rounding).
- **New lever discovered**: any unexpected edge behavior you can reuse.
- **Next mutated hypothesis**: smallest change to try next (lever, order, timing, token, state shaping).

Also update the SSOT if the falsifier revealed missing semantics:
- Add any missing nodes/edges discovered during testing.
- Reconcile layers (especially L11 and L14) if the observed behavior contradicts prior assumptions.

## Safe output rule
Write tests that prove the bad state and quantify the delta, but avoid packaging it as a real-world draining recipe (no “run these txs on mainnet” instructions).
