---
description: "Extract implicit invariants from protocol code that are not documented — find the assumptions the protocol relies on but never states"
---

# Skill: Novel Invariant Mining

## Purpose
Automatically discover protocol invariants from source code and value flows,
then systematically search for sequences that violate them.

## Invariant Categories

### 1. Conservation Invariants
Something is conserved across operations.
```
totalAssets == sum(all_user_deposits) - sum(all_user_withdrawals) + sum(yield_earned) - sum(fees_taken)
totalSupply == sum(all_balances)
pool.reserve0 * pool.reserve1 >= k (for constant product AMMs)
sum(collateral_values) >= sum(debt_values) * collateral_ratio
```

**Mining method**: For each state variable that changes on deposit/withdraw/transfer:
- Track what increases it and what decreases it
- The SUM across all increases should equal the SUM across all decreases (conservation)
- If not: there's either a fee (intended) or a leak (bug)

### 2. Monotonicity Invariants
Something only goes in one direction.
```
sharePrice >= previous_sharePrice (share price never decreases without loss event)
totalEarned[user] >= previous_totalEarned[user] (earned rewards never decrease)
nonce[user] > previous_nonce[user] (nonces always increase)
block.timestamp > previous_timestamp (time always moves forward)
```

**Mining method**: For each state variable:
- Identify all functions that modify it
- Is it ALWAYS modified in the same direction?
- If yes: it's a monotonicity invariant
- Then: search for sequences where it moves the WRONG direction

### 3. Solvency Invariants
The protocol can always meet its obligations.
```
totalAssets >= totalLiabilities
reserve >= sum(pending_withdrawals)
collateral_value >= debt_value * min_ratio
treasury >= sum(unclaimed_rewards)
```

**Mining method**: Identify:
- What the protocol HOLDS (assets, reserves, collateral)
- What the protocol OWES (liabilities, pending withdrawals, debt, unclaimed rewards)
- Write the inequality
- Search for sequences that flip it

### 4. Exchange Rate Invariants
Conversion rates are consistent and fair.
```
convertToShares(convertToAssets(shares)) == shares (round-trip consistency)
convertToAssets(shares) * totalSupply == totalAssets * shares (proportionality)
pricePerShare_after_deposit >= pricePerShare_before_deposit (no dilution)
```

**Mining method**: For each conversion function:
- Test round-trip: X → convert → convert_back → should equal X (±1 for rounding)
- Test proportionality: each user's share of total should equal their proportional claim
- Test monotonicity: deposit/yield should never decrease price per share

### 5. Ordering Invariants
Operations must happen in a specific order.
```
deposit must happen before withdraw
propose must happen before execute (governance)
borrow must happen before repay
stake must happen before claim
lock must happen before unlock
```

**Mining method**: For each state machine transition:
- What preconditions are checked?
- Can those preconditions be met via an ALTERNATIVE path?
- If a function requires state X to be true, can state X be set TRUE by an attacker?

### 6. Uniqueness Invariants
Something should be unique but might not be enforced.
```
token_id is unique within collection
nonce is unique per user
proposal_id is unique
position_id is unique per user
```

**Mining method**: For each ID/nonce:
- How is it generated?
- Can collisions occur? (counter overflow, hash collision, reuse after deletion)

### 7. Access Invariants
Who can do what should be consistent.
```
only admin can upgrade
only owner can withdraw
only governance can change parameters
only user can claim their own rewards
```

**Mining method**: For each privileged function:
- What storage encodes the privilege?
- Can that storage be written by a non-privileged party?
- Are there INDIRECT paths to privilege (delegation, callback, proxy confusion)?

## Invariant Formalization

### Convert to Solidity assertions:
```solidity
// Conservation
function invariant_conservation() public view {
    assertEq(
        token.balanceOf(address(vault)),
        vault.totalAssets(),
        "Vault balance != totalAssets"
    );
}

// Monotonicity
function invariant_sharePriceMonotonic() public view {
    uint256 currentPrice = vault.convertToAssets(1e18);
    assertGe(currentPrice, lastKnownPrice, "Share price decreased");
}

// Solvency
function invariant_solvency() public view {
    assertGe(
        vault.totalAssets(),
        vault.totalSupply() * vault.pricePerShare() / 1e18,
        "Protocol insolvent"
    );
}
```

### Convert to ItyFuzz invariants:
```solidity
// ItyFuzz reports bug when these REVERT
function invariant_conservation() public view {
    require(
        token.balanceOf(address(vault)) >= vault.totalAssets(),
        "Conservation violated"
    );
}
```

## Violation Search Strategy

1. **Cheapest first**: Tenderly simulation with state overrides
   - Override one variable to a boundary value
   - Check if the invariant holds
   - If not: the override is the ATTACK — find a sequence that achieves it

2. **Sequence search**: ItyFuzz with custom invariants
   - Encode the invariant as an `invariant_*()` function
   - Let the fuzzer find sequences that violate it
   - Focus targets on contracts that WRITE the invariant's variables

3. **Boundary amplification**: Test invariants at extreme states
   - Empty protocol (zero deposits, zero supply)
   - Maximum protocol (max deposits, max supply)
   - Just after deployment (uninitialized state)
   - During emergency/pause
   - After upgrade
