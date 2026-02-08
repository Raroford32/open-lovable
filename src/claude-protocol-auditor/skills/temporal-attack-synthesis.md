---
description: "Synthesize temporal attack sequences — ordering dependencies, multi-block windows, epoch boundary exploits"
---

# Skill: Temporal Attack Synthesis

## Purpose
Discover and model attacks that exploit TIME as a dimension —
multi-block sequences, epoch boundaries, TWAP manipulation,
delayed operations, and block property dependencies.

## Temporal Attack Classes

### 1. Multi-Block Oracle Manipulation
**Target**: TWAP-based price oracles (Uniswap V3 TWAP, custom implementations)

**Mechanics**:
- TWAP = time-weighted average price over a window (e.g., 30 minutes)
- To move TWAP by X%, attacker must move spot price by X% for the entire window
- Cost = capital_locked × duration × opportunity_cost + swap_fees

**Attack Pattern**:
```
Block N:     Borrow tokens via flash loan → deposit into lending → swap to move spot price
Block N+1:   Maintain position (pay swap fees to keep price moved)
...
Block N+K:   TWAP has moved sufficiently → exploit mispricing in target protocol
Block N+K+1: Unwind position, repay flash loan, collect profit
```

**Key Variables**:
- TWAP window length (longer = more expensive to manipulate)
- Pool liquidity depth (deeper = more expensive to move)
- Number of blocks needed (= window_seconds / 12)
- Capital lockup per block

**Cost Model**:
```
twap_manipulation_cost = swap_amount * fee_per_block * num_blocks + capital_opportunity_cost
```

### 2. Epoch/Period Boundary Exploitation
**Target**: Protocols with discrete time periods (staking epochs, reward periods, voting periods)

**Mechanics**:
- Protocol behavior changes at epoch boundaries
- Attacker times actions to straddle the boundary

**Attack Patterns**:
```
Pattern A: "Last-Second Deposit"
  - Wait until epoch N is about to end
  - Deposit large amount just before epoch boundary
  - Claim full epoch rewards for epoch N (only contributed for 1 block)
  - Withdraw at start of epoch N+1

Pattern B: "Double Claim"
  - Claim rewards for epoch N
  - Protocol updates state for epoch N+1
  - If there's a window where both epochs are "claimable"
  - Claim for epoch N+1 as well

Pattern C: "Epoch Reset Attack"
  - Trigger epoch advancement at an unexpected time
  - Protocol state is inconsistent during transition
  - Exploit the inconsistency before it resolves
```

### 3. Delayed Operation Exploitation
**Target**: Protocols with timelocked/delayed operations (withdrawals, unstaking, governance execution)

**Mechanics**:
- User initiates action at time T
- Action completes at time T+delay
- During delay: protocol state may change, oracle prices may change, conditions may invalidate

**Attack Patterns**:
```
Pattern A: "Stale Delay"
  - Initiate withdrawal at price P (high)
  - Price drops to P/2 during delay
  - Withdrawal executes at old price P
  - Attacker extracts value at expense of remaining depositors

Pattern B: "Queue Manipulation"
  - Fill withdrawal queue with many small requests
  - Large legitimate withdrawal gets delayed behind the queue
  - Attacker can front-run the delayed withdrawal

Pattern C: "Delay Race"
  - Initiate two competing delayed operations
  - The first to execute changes state for the second
  - Attacker controls which executes first
```

### 4. Block Property Exploitation
**Target**: Logic that depends on block.timestamp, block.number, block.basefee, PREVRANDAO

**Mechanics**:
```
block.timestamp: Proposer can shift ±15 seconds (Ethereum)
block.number: Predictable, but block times vary
block.basefee: Varies with congestion, can be manipulated via gas usage
PREVRANDAO: Proposer knows it before building the block
```

**Attack Patterns**:
```
Pattern A: "Timestamp Manipulation" (proposer = attacker)
  - Protocol uses timestamp for interest calculation
  - Proposer shifts timestamp by +15 seconds
  - Extra interest accrues, affecting exchange rates

Pattern B: "PREVRANDAO Pre-knowledge"
  - Protocol uses PREVRANDAO for randomness
  - Proposer knows PREVRANDAO before the block is built
  - Proposer only includes the block if PREVRANDAO is favorable

Pattern C: "Basefee Dependency"
  - Protocol has gas-sensitive logic (e.g., refund calculations)
  - Attacker creates high-gas transactions to inflate basefee
  - Victim's transaction becomes more expensive or behaves differently
```

### 5. Interest Rate Manipulation
**Target**: Lending protocols with utilization-based interest rates

**Mechanics**:
- Interest rate = f(utilization) where utilization = total_borrowed / total_deposited
- Attacker can change utilization by borrowing/depositing

**Attack Patterns**:
```
Pattern A: "Rate Spike Attack"
  - Borrow large amount → utilization spikes → interest rate spikes
  - Other borrowers now pay very high interest
  - Attacker repays quickly → keeps the interest differential profit
  - Works if interest is per-block and attacker repays same block

Pattern B: "Rate Compression"
  - Deposit large amount → utilization drops → interest rate drops
  - Depositors earn less interest
  - Attacker's large deposit earns at the lower rate
  - But attacker can borrow elsewhere at the lower rate for arbitrage

Pattern C: "Liquidation via Rate Spike"
  - Borrower has position near liquidation threshold
  - Attacker spikes interest rate → accrued interest pushes position below threshold
  - Attacker liquidates the position for profit
```

### 6. Cross-Block Sandwich Attacks
**Target**: Any operation that spans multiple blocks

**Mechanics**:
- Victim submits transaction in block N
- Attacker controls block N-1 (setup) and block N+1 (profit)

**Attack Pattern**:
```
Block N-1: Attacker manipulates state (price, liquidity, etc.)
Block N:   Victim's transaction executes against manipulated state
Block N+1: Attacker unwinds manipulation and collects profit
```

## Temporal Feasibility Assessment

For each temporal attack, assess:

| Factor | Question | Impact |
|--------|----------|--------|
| Ordering tier | Does attacker need builder access? | Feasibility |
| Capital lockup | How much capital is locked per block? | Cost |
| Duration | How many blocks is the attack? | Cost × risk |
| Competition | Are other searchers competing? | Reliability |
| Detection | Can the attack be detected and front-run? | Reliability |
| Gas cost | Total gas across all blocks | Cost |

## Testing Temporal Attacks

### Using Tenderly Virtual TestNet:
```bash
# Create VNet at fork block
# Execute setup transactions
# Advance time: evm_setNextBlockTimestamp
# Mine blocks: evm_mine
# Execute attack transactions
# Verify state changes
```

### Using Foundry:
```solidity
// Multi-block test
function test_temporal_attack() public {
    vm.createSelectFork(vm.envString("ETH_RPC_URL"), FORK_BLOCK);

    // Block N: Setup
    vm.startPrank(attacker);
    protocol.deposit(setupAmount);
    vm.stopPrank();

    // Advance to next block
    vm.roll(block.number + 1);
    vm.warp(block.timestamp + 12);

    // Block N+1: Attack
    vm.startPrank(attacker);
    protocol.exploit();
    vm.stopPrank();

    // Verify profit
    assertGt(token.balanceOf(attacker), initialBalance);
}
```
