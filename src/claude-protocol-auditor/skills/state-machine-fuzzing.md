---
description: "Fuzz protocol state machine for unreachable states that are actually reachable — implicit state testing"
---

# Skill: State Machine Fuzzing

## Purpose
Extract implicit state machines from smart contracts and systematically
explore ILLEGAL state transitions that lead to exploitable conditions.

## State Machine Extraction

### Step 1: Identify State Variables
For each contract, categorize all storage variables:

**Protocol State** (enum-like or boolean):
```solidity
bool public paused;           // Binary state
uint8 public phase;           // Multi-phase lifecycle
bool public initialized;      // Initialization state
bool public deprecated;       // Deprecation flag
```

**Accounting State** (continuous):
```solidity
uint256 public totalSupply;   // Token accounting
uint256 public totalAssets;   // Asset accounting
mapping(address => uint256) public balances;
```

**Configuration State** (rarely changing):
```solidity
address public oracle;
uint256 public feeRate;
address public admin;
```

### Step 2: Map State Transitions
For each external/public function, record:
```
function_name:
  reads: [state_var_1, state_var_2]
  writes: [state_var_3, state_var_4]
  preconditions: [require statements]
  postconditions: [implicit state]
  external_calls: [contracts called]
```

### Step 3: Build Transition Graph
```
State A (initialized=false) --initialize()--> State B (initialized=true, admin=caller)
State B (paused=false) --deposit()--> State B (totalSupply += shares)
State B (paused=false) --withdraw()--> State B (totalSupply -= shares)
State B --pause()--> State C (paused=true)
State C --unpause()--> State B (paused=false)
State B --upgrade()--> State D (impl=newImpl)
```

### Step 4: Find Illegal Transitions
An "illegal" transition is one that:
1. Should NOT be possible according to the protocol design
2. BUT can be triggered by a specific call sequence

**Common illegal transitions:**
- `initialized=true → initialized=false` (re-initialization)
- `admin=deployer → admin=attacker` (unauthorized admin change)
- `totalAssets > totalLiabilities → totalAssets < totalLiabilities` (insolvency)
- `sharePrice=X → sharePrice=X/2` (share price crash without loss event)
- `paused=true → functions still execute` (pause bypass)

### Step 5: Design Sequence to Reach Illegal State
For each illegal transition:
1. What is the SHORTEST call sequence that achieves it?
2. What preconditions must be met?
3. Can those preconditions be met by an attacker?
4. If yes: that's your hypothesis — test it on a fork.

## State Space Reduction for Fuzzing

### Problem: Exponential state space
With N state variables, each with M possible values, there are M^N states.
Fuzzing all of them is intractable.

### Solution: Hypothesis-guided state targeting
Instead of exploring ALL states, target SPECIFIC dangerous state combinations:

1. **Boundary states**: Each variable at its min/max value
   ```
   totalSupply = 0, 1, type(uint256).max
   balance = 0, 1, type(uint256).max
   sharePrice = 0, 1, type(uint256).max
   ```

2. **Inconsistent states**: Variables that should be correlated but aren't
   ```
   totalSupply > 0 but totalAssets == 0  (shares exist but no assets)
   totalAssets > 0 but totalSupply == 0  (assets exist but no shares)
   balances[user] > totalSupply          (user has more than total)
   ```

3. **Transition boundary states**: Just before/after a state change
   ```
   paused=false → deposit → paused=true → (can still withdraw?)
   phase=1 → advance → phase=2 → (can phase=1 functions still execute?)
   ```

### ItyFuzz Integration
Use ItyFuzz's state-aware fuzzing to target these combinations:

```solidity
// Invariant that targets inconsistent state
function invariant_noGhostShares() public view {
    if (vault.totalSupply() > 0) {
        require(vault.totalAssets() > 0, "Ghost shares: supply without assets");
    }
}

// Invariant that targets transition boundary
function invariant_pauseRespected() public view {
    if (vault.paused()) {
        // This invariant is checked AFTER fuzzer calls functions
        // If any value-changing function executed during pause, this fails
        require(
            vault.totalAssets() == lastAssets && vault.totalSupply() == lastSupply,
            "State changed while paused"
        );
    }
}
```

## Multi-Contract State Machine Analysis

### Cross-contract state coupling
When contract A and B have coupled state machines:
```
A.state = ACTIVE, B.state = ACTIVE  →  Normal operation
A.state = PAUSED, B.state = ACTIVE  →  B operates on stale A data?
A.state = ACTIVE, B.state = UPGRADED →  A calls old B interface?
```

### Desynchronization attacks
Find sequences where:
1. A and B start in consistent state
2. A's state changes (via legitimate operation)
3. B's state is NOT updated (because the update path is missing or delayed)
4. B now operates on stale assumptions about A
5. This produces an exploitable inconsistency

## Evidence Template
```yaml
state_machine:
  contract: "0x..."
  states_identified: 5
  transitions_mapped: 12
  illegal_transitions_found: 2

  illegal_transition_1:
    from: "initialized=true, admin=deployer"
    to: "initialized=true, admin=attacker"
    sequence:
      - "call reinitialize() on implementation contract directly"
      - "implementation sets admin to msg.sender"
      - "proxy still points to implementation"
      - "attacker now controls admin"
    evidence: "<engagement_root>/tenderly/rpc/sim-reinit-bypass.json"
```
