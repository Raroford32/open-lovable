# Cycle Mining (profit-positive loops without “one broken check”)

Goal: find scenarios where **each step is locally valid**, yet the composition forms a loop that yields net positive output per iteration.
These routes often evade “single-function invariant thinking” and require explicit simulation to surface.

This is not a vulnerability label. It is a structural target:
> A normal user can execute a cycle of protocol actions that returns to the same state variables but increases attacker value (or decreases protocol custody).

## Output (required artifact)
Create `codegraph/layers/L22_cycle_mining.md` with:
- a **Conversion Edge Inventory** (what conversions exist)
- candidate cycle skeletons (2–8 steps)
- smallest falsifier stubs (cycle once; cycle N times; amount-regime probes)

## Conversion edges to inventory (evidence-driven)
From SSOT coverage (L10/L11/L12/L13):
- assets ↔ shares (deposit/mint, withdraw/redeem)
- shares ↔ rewards (stake/unstake, claim)
- token ↔ LP (mint/burn LP; pool joins/exits)
- debt ↔ collateral (borrow/repay; liquidation paths)
- internal stable ↔ external stable (swap paths)
- any “index / sharePrice / exchangeRate” based conversion

For each conversion edge record:
- formula location
- rounding points and direction
- external inputs consumed (if any)
- state machine constraints (cooldowns, epochs, phases)

## Cycle discovery procedure

### 1) Build a conversion graph (small)
Nodes: value-bearing representations (assets, shares, LP, debt, rewards).
Edges: conversion functions.

### 2) Search for short cycles first
Start with 2–4 edge cycles:
- deposit → stake → unstake → withdraw
- deposit → mint claim → redeem → withdraw
- swap A→B → protocol action uses B → swap back

### 3) Probe “amount regimes”
Many cycles only become positive in specific regimes:
- dust-sized repeated loops (rounding bias)
- large transient moves (measurement shift)
- mixed: large move then many small loops

### 4) Attach an economic objective
Every candidate cycle must name:
- target custody location(s)
- how the delta is measured (attacker balance, protocol custody)
- the maximum bound (pool reserves/caps)

## Smallest falsifiers
- **Cycle-once**: run the cycle once and measure whether attacker value increased.
- **Cycle-N**: repeat N times and see if drift accumulates.
- **Regime sweep**: try dust vs medium vs large amounts to find discontinuities.

## Self-evaluation gate
You are not done if the protocol contains conversions and you have not attempted:
- at least one short cycle hypothesis, and
- at least one “repeat N times” drift probe.

