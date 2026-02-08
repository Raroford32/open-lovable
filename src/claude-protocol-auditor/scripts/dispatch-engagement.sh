#!/usr/bin/env bash
# Claude Protocol Auditor v3.0 — Engagement Dispatch Script
# Architecture: Parallel Intelligence → Convergence → Cook
# This script initializes an engagement workspace and prints the v3.0 dispatch plan.
# Actual agent spawning is done by Claude Code's Task tool reading agent prompt files.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDITOR_ROOT="$(dirname "$SCRIPT_DIR")"

# Load environment
if [ -f "$AUDITOR_ROOT/.env" ]; then
    set -a; . "$AUDITOR_ROOT/.env"; set +a
fi

# Parse arguments
PROTOCOL_SLUG="${1:?Usage: dispatch-engagement.sh <protocol_slug> <chain_id> <fork_block> <seed_addresses>}"
CHAIN_ID="${2:?Missing chain_id}"
FORK_BLOCK="${3:?Missing fork_block}"
SEED_ADDRS="${4:?Missing seed_addresses (comma-separated)}"

ENGAGEMENT_ROOT="${ENGAGEMENTS_DIR:-analysis/engagements}/$PROTOCOL_SLUG"

echo "=== Claude Protocol Auditor v3.0 — Engagement Dispatch ==="
echo "Architecture: Parallel Intelligence → Convergence → Cook"
echo ""
echo "Protocol:     $PROTOCOL_SLUG"
echo "Chain ID:     $CHAIN_ID"
echo "Fork Block:   $FORK_BLOCK"
echo "Seed Addrs:   $SEED_ADDRS"
echo "Engagement:   $ENGAGEMENT_ROOT"
echo ""

# Create engagement workspace
mkdir -p "$ENGAGEMENT_ROOT"/{contract-bundles,tenderly/{rpc,api},notes,proofs,agent-outputs}

# Create index.yaml
cat > "$ENGAGEMENT_ROOT/index.yaml" << EOF
# Engagement Index — v3.0
protocol: $PROTOCOL_SLUG
chain_id: $CHAIN_ID
fork_block: $FORK_BLOCK
seed_addresses:
$(echo "$SEED_ADDRS" | tr ',' '\n' | sed 's/^/  - /')

rpc_url_env: ETH_RPC_URL
etherscan_key_env: ETHERSCAN_API_KEY
tenderly_node_rpc_url_env: TENDERLY_NODE_RPC_URL
tenderly_access_key_env: TENDERLY_ACCESS_KEY
tenderly_account_slug: ${TENDERLY_ACCOUNT_SLUG:-}
tenderly_project_slug: ${TENDERLY_PROJECT_SLUG:-}

engagement_root: $ENGAGEMENT_ROOT
auditor_root: $AUDITOR_ROOT

agent_outputs: $ENGAGEMENT_ROOT/agent-outputs
notes: $ENGAGEMENT_ROOT/notes
proofs: $ENGAGEMENT_ROOT/proofs
tenderly_evidence: $ENGAGEMENT_ROOT/tenderly
EOF

# Create memory.md
cat > "$ENGAGEMENT_ROOT/memory.md" << EOF
# Memory ($PROTOCOL_SLUG)

## Pinned Reality
- chain_id: $CHAIN_ID
- fork_block: $FORK_BLOCK
- attacker_tier: builder (assume worst case)
- capital_model: flash loans available (Aave V3 + Balancer + dYdX)

## Phase 1: Contract Universe (pending — run reality-anchor + universe-cartographer)
- seed addresses: $SEED_ADDRS
- proxies→impls: TBD
- source acquired: TBD

## Phase 2: Parallel Intelligence (pending — run all 8 Phase 2 agents)
- protocol-logic-dissector: TBD
- economic-model-analyst: TBD
- state-machine-explorer: TBD
- cross-function-weaver: TBD
- temporal-sequence-analyst: TBD
- numeric-precision-analyst: TBD
- oracle-external-analyst: TBD
- control-flow-mapper: TBD

## Phase 3: Convergence (pending — run convergence-synthesizer)
- Committed CP: TBD
- Backup CPs: TBD
- Pivot count: 0

## Next Action
- Run Phase 1: reality-anchor → universe-cartographer
EOF

# Create empty note stubs
for note in value-model entrypoints; do
    if [ ! -f "$ENGAGEMENT_ROOT/notes/$note.md" ]; then
        echo "# $note" > "$ENGAGEMENT_ROOT/notes/$note.md"
        echo "" >> "$ENGAGEMENT_ROOT/notes/$note.md"
        echo "## Status: EMPTY — Pending agent analysis" >> "$ENGAGEMENT_ROOT/notes/$note.md"
    fi
done

# Create orchestrator state
cat > "$ENGAGEMENT_ROOT/orchestrator-state.md" << EOF
# Orchestrator State

## Current Phase: 0 (initialized)
## Committed Convergence Point: none
## Pivot Count: 0

## Phase 2 Agent Status
| Agent | Status | Key Findings Count | Top Finding |
|-------|--------|-------------------|-------------|
| protocol-logic-dissector | pending | - | - |
| economic-model-analyst | pending | - | - |
| state-machine-explorer | pending | - | - |
| cross-function-weaver | pending | - | - |
| temporal-sequence-analyst | pending | - | - |
| numeric-precision-analyst | pending | - | - |
| oracle-external-analyst | pending | - | - |
| control-flow-mapper | pending | - | - |

## Convergence Points
| CP | Region | Score | Density | Status |
|----|--------|-------|---------|--------|

## Belief Log
| Phase | Belief Change | Evidence |
|-------|--------------|----------|
| 0 | Engagement initialized | index.yaml |

## Next Action
Run Phase 1: reality-anchor → universe-cartographer
EOF

echo "=== Workspace Created ==="
echo ""
echo "=== v3.0 Agent Dispatch Plan ==="
echo ""
echo "PHASE 1: Pin Reality (Sequential)"
echo "  1. reality-anchor          → Validate RPC, fork block, chain ID"
echo "  2. universe-cartographer   → Map all contracts, resolve proxies, acquire source"
echo ""
echo "PHASE 2: Parallel Intelligence (ALL 8 agents SIMULTANEOUSLY)"
echo "  ┌─ protocol-logic-dissector   → Intent vs implementation gaps, implicit invariants"
echo "  ├─ economic-model-analyst     → Value equations, custody/entitlements, measurement gaps"
echo "  ├─ state-machine-explorer     → Implicit states, transitions, desynchronization"
echo "  ├─ cross-function-weaver      → State dependencies, stale data, composition bugs"
echo "  ├─ temporal-sequence-analyst   → Ordering dependencies, timing, epoch boundaries"
echo "  ├─ numeric-precision-analyst   → Exchange rates, rounding, arithmetic edges"
echo "  ├─ oracle-external-analyst     → External trust, manipulation economics"
echo "  └─ control-flow-mapper         → Authority graph, governance timing, keeper deps"
echo ""
echo "PHASE 3: Convergence (Single agent reads ALL Phase 2 outputs)"
echo "  → convergence-synthesizer    → Build convergence matrix, find multi-lens convergence"
echo "  → COMMIT to top convergence point (CP-1)"
echo ""
echo "PHASE 3.5: Quick Validation"
echo "  → Orchestrator runs 1 cast call / simulation to validate CP-1 thesis"
echo ""
echo "PHASE 4: Deep Drill (1-3 on-demand specialists for committed CP)"
echo "  Available: flash-economics-lab, callback-reentry-analyst, upgrade-proxy-analyst,"
echo "            storage-layout-hunter, governance-attack-lab, bridge-crosschain-analyst,"
echo "            evm-underbelly-lab, token-semantics-analyst, numeric-boundary-explorer"
echo ""
echo "PHASE 5: Cook (Single agent builds ONE exploit step-by-step)"
echo "  → scenario-cooker            → Verify pre-conditions → test each step → write PoC"
echo ""
echo "PHASE 6: Proof & Review (Sequential)"
echo "  1. proof-constructor         → Build E3-grade evidence"
echo "  2. adversarial-reviewer      → Challenge every assumption"
echo "  3. report-synthesizer        → Final report (if finding confirmed)"
echo ""
echo "=== Ready for Claude Code Task tool agent dispatch ==="
echo "=== Load agent prompts from: $AUDITOR_ROOT/agents/ ==="
