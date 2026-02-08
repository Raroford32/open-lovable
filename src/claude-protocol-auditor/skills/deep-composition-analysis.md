---
description: "Discover vulnerabilities that only exist in the composition of multiple contracts — audit shadow exploitation, trust transitivity"
---

# Skill: Deep Composition Analysis

## Purpose
Discover vulnerabilities that ONLY exist in the composition of multiple contracts/protocols.
These are the highest-value findings in heavily audited protocols.

## Composition Bug Taxonomy (Novel — Not Named Classes)

### 1. Audit Shadow Exploitation
When multiple auditors reviewed different scopes, the INTERACTION between scopes was reviewed by neither.
- Identify each contract's audit history (if available from docs/repos)
- Map contract interactions that CROSS audit boundaries
- These cross-boundary interactions are highest priority for novel bugs

### 2. Trust Transitivity Chains
A trusts B (verified). B trusts C (verified). A→C trust was NEVER verified.
```
Protocol → DEX Router → Pool → Token
          ↑ audited      ↑ audited
          └── A→Token trust NOT audited ──┘
```
- Map all trust chains longer than 2 hops
- The LAST hop in a trust chain is most likely to be exploitable

### 3. State Synchronization Failures
Two contracts maintain coupled state (e.g., both track a balance).
If they can go out of sync, one of them is "lying" and the other can be exploited.
- Identify all cross-contract state coupling
- For each: can one side be updated without the other?
- If yes: what happens when the stale side is read?

### 4. Callback State Window Exploitation
When contract A calls contract B, there's a TIME WINDOW where A's state is "in between" writes.
If B calls back to A (or to C which reads A), A's state is inconsistent.
```
A.deposit() {
    balances[user] += amount;       // State updated
    token.transferFrom(user, this); // External call — B could callback to A
    totalDeposits += amount;        // State NOT YET updated during callback
}
// During callback: balances[user] is updated but totalDeposits is NOT
// → solvency check (totalDeposits >= sum(balances)) would PASS incorrectly
```
- Find ALL state writes that happen BEFORE and AFTER external calls
- The state written AFTER is stale during the external call
- This is exploitable if ANY path reads the stale value during the call

### 5. Shared Resource Contention
Two protocols read/write the same external state (e.g., same oracle, same DEX pool).
Manipulating the shared state affects both protocols differently.
```
Protocol A reads price from Uniswap V3 pool X (TWAP)
Protocol B reads price from same pool X (spot)
→ Manipulate pool X: A sees TWAP (delayed), B sees spot (immediate)
→ Arbitrage the price difference between A and B
```

### 6. Emergency/Pause Interaction Bugs
When protocol A pauses, what happens to protocol B that depends on A?
- Can B's users still withdraw if A is paused?
- Does B handle A's revert gracefully?
- Can A's pause be used to TRAP value in B?

### 7. Fee/Slippage Stacking
Multiple protocols each apply their own fees/slippage.
The combined effect may be larger than any individual protocol's users expect.
```
Deposit into Yield Aggregator (0.5% fee)
→ Deposits into Lending Protocol (0.1% deposit fee)
→ Lending Protocol invests in Strategy (0.2% management fee)
Total: 0.8% — but user saw "0.5% fee" on the aggregator UI
```

### 8. Liquidity Fragmentation Exploitation
Protocol assumes liquidity depth based on a pool that can be temporarily drained.
```
Protocol A reads Uniswap V3 pool liquidity: "sufficient depth for $10M"
Attacker drains liquidity via concentrated position removal
Protocol A's swap now experiences 50% slippage instead of 0.1%
```

### 9. Governance Cross-Protocol Attacks
Use governance of protocol A to change behavior affecting protocol B's users.
```
Protocol A has a fee parameter controlled by governance
Protocol B integrates A and passes A's fee to users
Attacker flash-votes to increase A's fee to 99%
B's users now pay 99% fee on their next transaction
```

### 10. Oracle Price Source Divergence
Two paths to the "same price" give different results at the same block.
```
Path 1: Chainlink ETH/USD
Path 2: Uniswap V3 TWAP ETH/USDC → USDC/USD ≈ 1.0
Result: Path 1 = $3000.00, Path 2 = $2998.50
→ Protocol uses Path 1 for lending, Path 2 for liquidation
→ Tiny arbitrage in normal conditions, massive gap during volatility
```

## Detection Methodology

### Step 1: Build the interaction graph
```
For each contract C in the universe:
  For each external call in C:
    Record: C → target (with calldata/value classification)
```

### Step 2: Find cross-cutting state dependencies
```
For each state variable S read by contract C:
  Is S written by a different contract D?
  Is S a return value from an external call?
  Can the writer/source be manipulated?
```

### Step 3: Identify callback windows
```
For each external call between state writes:
  What state is "half-updated" at the call point?
  What paths could execute during the callback?
  What would those paths see (stale state)?
```

### Step 4: Design composition discriminators
```
For each identified composition pattern:
  Build a Tenderly bundle simulation that:
  1. Sets up the pre-attack state
  2. Executes the cross-contract sequence
  3. Measures the invariant violation
```

## Evidence Requirements
- Every composition finding must have a multi-contract trace
- The trace must show state across ALL involved contracts
- The invariant violation must be measured in value terms
- Feasibility must be assessed (can an attacker actually trigger this sequence?)
