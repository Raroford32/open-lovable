---
description: "Model economic attack viability — flash loan costs, sandwich economics, liquidation cascades, MEV extraction"
---

# Skill: Economic Attack Modeling

## Purpose
Model the economic viability of attack sequences. Determine if a hypothetical
vulnerability is ACTUALLY profitable after all costs are accounted for.

## Attack Economics Framework

### Revenue Side
What does the attacker GET from the exploit?

1. **Direct token extraction**: tokens transferred from protocol to attacker
2. **Share price manipulation**: buy cheap shares → inflate value → sell expensive shares
3. **Liquidation profit**: force liquidation → buy at discount
4. **Oracle arbitrage**: manipulate oracle → trade against mispricing
5. **Sandwich profit**: frontrun/backrun victim transaction
6. **MEV extraction**: reorder transactions for profit
7. **Governance capture**: use governance to redirect funds

### Cost Side
What does the attacker PAY?

1. **Gas costs**: estimate at various base fees (30-200 gwei)
   ```
   gas_cost = gas_used * base_fee * ETH_price
   ```

2. **Flash loan fees**:
   | Source | Fee |
   |--------|-----|
   | Aave V3 | 0.05% (0.09% for older markets) |
   | Balancer | 0% |
   | dYdX | 0% |
   | Uniswap V2/V3 flash | 0.3% / varies |
   | MakerDAO flash mint | 0% |

3. **DEX swap fees and slippage**:
   ```
   swap_cost = amount * fee_tier + price_impact(amount, liquidity_depth)
   ```
   - Uniswap V3: 0.01%, 0.05%, 0.3%, 1% tiers
   - Curve: 0.04% typical
   - Balancer: 0.01-10% (pool-specific)

4. **Oracle manipulation cost**:
   - Spot price: cost of moving pool by X% = f(liquidity_depth, target_move)
   - TWAP: cost × number_of_blocks_to_maintain × capital_lockup_time
   - Chainlink: cannot manipulate (except via underlying market)

5. **MEV priority fee / builder bribe**:
   - Priority gas: 2-50 gwei (varies with congestion)
   - Builder bribe: typically 30-90% of extracted value
   - Total MEV cost: priority_fee + builder_bribe

6. **Market impact of setup/unwind**:
   - Setup: acquiring tokens, creating positions
   - Unwind: selling stolen tokens, closing positions
   - Larger amounts = more slippage = less profit

7. **Protocol fees**:
   - Entry/exit fees on vaults
   - Borrowing interest (if holding position across blocks)
   - Withdrawal delays (opportunity cost)

### Net Profit Calculation
```
net_profit = revenue - gas_costs - flash_fees - swap_costs - oracle_manipulation_cost - mev_costs - market_impact - protocol_fees
```

**Minimum viable exploit**: net_profit > 0 after ALL costs

### Robustness Testing
Verify profitability survives perturbations:
- Gas +20%: `net_profit_20pct_gas = net_profit - (gas_costs * 0.2)`
- Liquidity -20%: recalculate swap costs with 80% liquidity depth
- Timing +1 block: add 1 block to any timing-sensitive steps
- Weaker ordering tier: can profit be achieved without builder access?

## Flash Loan Capital Planning

### Multi-source flash loan strategy
```
Need $50M for attack:
- Aave V3 ETH: borrow 15000 ETH ($45M) — 0.05% fee = $22.5K
- Balancer WETH: borrow 1000 ETH ($3M) — 0% fee
- dYdX USDC: borrow $2M — 0% fee
Total capital: $50M
Total flash fees: $22.5K
```

### Flash loan composability
Flash loans can be NESTED:
```
Aave flash loan →
  Use borrowed ETH as collateral in Compound →
  Borrow USDC from Compound →
  Use USDC to manipulate Curve pool →
  Profit from price difference →
  Repay Compound →
  Repay Aave
```

## MEV Ordering Analysis

### Ordering Tiers
1. **Public mempool**: Anyone can see pending txs. Attacker competes with all MEV searchers.
   - Cost: HIGH competition, may need large bribe
   - Reliability: LOW (may be frontrun by other searchers)

2. **Private relay (Flashbots Protect)**: Transaction is hidden until included.
   - Cost: MEDIUM (builder bribe only, no competition)
   - Reliability: MEDIUM (builder may not include)

3. **Builder access**: Attacker IS the block builder or has exclusive deal.
   - Cost: LOW (no competition)
   - Reliability: HIGH (can guarantee ordering)

### Sandwich Attack Economics
```
profit = victim_trade_amount * price_impact_extraction - (2 * swap_fee) - gas_for_2_txs - builder_bribe
```

### Multi-block Attack Economics
```
block_1_cost = setup_gas + capital_lockup_opportunity_cost
block_2_cost = execution_gas + unwind_gas
total_cost = block_1_cost + block_2_cost + flash_fees + swap_fees
profit = revenue - total_cost
```
Multi-block attacks are MORE EXPENSIVE but can access bugs that single-block attacks cannot.

## Profit Optimization

Given a confirmed vulnerability with parameter `amount`:
```
profit(amount) = revenue(amount) - costs(amount)

revenue(amount) = f(amount)  # protocol-specific, often sublinear
costs(amount) = flash_fee(amount) + swap_cost(amount) + gas  # often superlinear

optimal_amount = argmax(profit(amount))
```

Binary search or analytical solution for optimal attack size.

## Evidence Output
For each hypothesis:
```yaml
hypothesis_id: H-001
revenue_estimate: 500 ETH
costs:
  gas: 0.5 ETH (at 50 gwei)
  flash_fees: 0.25 ETH (Aave 0.05% on 500 ETH)
  swap_slippage: 2 ETH (estimated from Uniswap V3 WETH/USDC depth)
  mev_bribe: 100 ETH (20% of gross to builder)
  protocol_fees: 0 ETH
  total_costs: 102.75 ETH
net_profit: 397.25 ETH
robustness:
  gas_plus_20: 397.15 ETH (still profitable)
  liquidity_minus_20: 394.75 ETH (still profitable)
  timing_plus_1_block: 395 ETH (still profitable)
  weaker_ordering: "Requires at minimum private relay (public mempool = competitive)"
verdict: ECONOMICALLY_VIABLE
```
