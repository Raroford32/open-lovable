---
description: "Launch attacker-mindset vulnerability discovery against a deployed DeFi protocol using Parallel Intelligence → Convergence → Cook pipeline"
---

# /hunt — Protocol Vulnerability Discovery

Think like an attacker. Hunt novel, unnamed, complex protocol-logic vulnerabilities in heavily audited DeFi protocols — the kind where every basic pattern has been checked 10 times and the ONLY bugs that remain are buried in the protocol's OWN logic complexity.

## Usage

```
/hunt <protocol_slug> <chain_id> <fork_block> <seed_addresses>
```

**Parameters:**
- `protocol_slug` — Short name for the engagement (e.g., `aave-v3`, `morpho-blue`)
- `chain_id` — Target chain (1=Ethereum, 42161=Arbitrum, 10=Optimism, 8453=Base)
- `fork_block` — Finalized block number to pin the fork (must be finalized, not pending)
- `seed_addresses` — Comma-separated contract addresses to start discovery from

**Example:**
```
/hunt morpho-blue 1 19500000 0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb
```

## What Happens

### Prerequisites
- `ETH_RPC_URL` environment variable set (archive node recommended)
- `ETHERSCAN_API_KEY` environment variable set
- Foundry installed (`forge`, `cast`, `anvil`)
- Tenderly access configured (optional but recommended for traces)

### Pipeline Execution

**Phase 1 — Pin Reality** (sequential, ~10 min)
1. `reality-anchor` validates RPC endpoint, chain ID, fork block finality
2. `universe-cartographer` discovers all contracts (proxy resolution, source acquisition, dependency graph)
3. Universe cartographer extracts trust boundary inventory, config snapshot, and asset flow graph

**Phase 2 — Parallel Intelligence** (8 agents simultaneously, ~45 min)
All agents read the same codebase through different analytical lenses:
- Protocol Logic Dissector — intent vs implementation gaps, implicit invariants, EIP-7702 impact
- Economic Model Analyst — value equations, custody vs entitlements, measurement-settlement gaps
- State Machine Explorer — implicit states, transitions, repetition shaping, config-state coupling
- Cross-Function Weaver — state dependencies, differential pairs, mid-tx ordering, permissionless+external
- Temporal Sequence Analyst — ordering dependencies, multi-block windows, epoch boundaries
- Numeric Precision Analyst — arithmetic precision, library-as-protocol, scale amplification
- Oracle & External Analyst — external trust, manipulation economics, bridges, hooks, bidirectional deps
- Control Flow Mapper — authority graph, EIP-7702 threat model, blast-radius, post-upgrade breaks

**Phase 3 — Convergence** (~15 min)
`convergence-synthesizer` reads ALL Phase 2 outputs and builds a convergence matrix.
Finds where 2+ lenses flag the SAME code region. Applies 2026 amplifiers (EIP-7702, differential mismatch, library-as-protocol, permissionless+external, post-upgrade). Commits to top convergence point.

**Phase 3.5 — Quick Validation** (~5 min)
Orchestrator runs up to 6 structured tests on fork before investing in deep-dive:
value computation, differential, mid-transaction ordering, trust assumption, permissionless+external, precision scale. Any contradiction → pivot to CP-2.

**Phase 4 — Deep Drill** (1-3 specialists, ~30 min)
On-demand specialists deep-dive the committed convergence point.
Available: flash-economics-lab, callback-reentry-analyst, upgrade-proxy-analyst, storage-layout-hunter, governance-attack-lab, bridge-crosschain-analyst, evm-underbelly-lab, token-semantics-analyst, numeric-boundary-explorer.

**Phase 5 — Cook** (~30 min)
`scenario-cooker` builds ONE complete exploit step-by-step, testing each step on fork.
Writes Foundry PoC. Itemizes ALL costs (gas, flash fees, slippage, MEV, protocol fees).

**Phase 6 — Proof** (~20 min)
`proof-constructor` builds E3-grade evidence. `adversarial-reviewer` challenges every assumption.
Finding must be: reproducible, permissionless, profitable after ALL costs, robust to gas+20%/liquidity-20%/timing+1 block.

## Dispatch

To initialize the engagement workspace and see the full dispatch plan:

```bash
bash scripts/dispatch-engagement.sh <protocol_slug> <chain_id> <fork_block> <seed_addresses>
```

Then load the orchestrator agent prompt and begin Phase 1:

```
Read agents/tier1-foundation/orchestrator.md and execute the pipeline for the engagement at analysis/engagements/<protocol_slug>/
```

## Architecture Reference

See `CLAUDE.md` for the complete system description, `config/agent-topology.yaml` for the pipeline topology, and `config/coverage-gates.yaml` for phase validation criteria.
