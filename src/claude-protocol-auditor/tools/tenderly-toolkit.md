# Tool: Tenderly Toolkit

## Overview
Tenderly provides evidence-grade decoded traces, controlled simulations, bundle simulation, and Virtual TestNets. It is the PRIMARY evidence source for E3 proof artifacts.

## Environment Setup
```bash
# Required env vars (from .env)
TENDERLY_NODE_RPC_URL=        # Tenderly Node RPC (decoded traces)
TENDERLY_ACCESS_KEY=          # API access key
TENDERLY_ACCOUNT_SLUG=        # Account slug
TENDERLY_PROJECT_SLUG=        # Project slug
TENDERLY_VNET_RPC_URL=        # Virtual TestNet RPC
TENDERLY_VNET_ADMIN_RPC_URL=  # VNet admin cheatcodes
```

## 1. Transaction Tracing (Decoded)

### Via Tenderly Node RPC
```bash
# Full decoded trace of a historical transaction
curl -s "$TENDERLY_NODE_RPC_URL" -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenderly_traceTransaction",
    "params": ["'$TX_HASH'"],
    "id": 1
  }' | python3 -m json.tool > "$ENGAGEMENT_ROOT/tenderly/rpc/trace-$TX_HASH.json"
```

### Key fields in trace response:
- `result.trace[]` — decoded call tree (function names, args, return values)
- `result.stateDiff` — storage changes per contract
- `result.assetChanges` — token/ETH transfers with decoded amounts
- `result.balanceChanges` — balance deltas per address

## 2. Transaction Simulation (What-If)

### Single transaction simulation
```bash
# Simulate a transaction without sending it
curl -s "$TENDERLY_NODE_RPC_URL" -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenderly_simulateTransaction",
    "params": [{
      "from": "'$FROM'",
      "to": "'$TO'",
      "data": "'$CALLDATA'",
      "value": "'$VALUE'",
      "gas": "0x1312D00",
      "gasPrice": "0x0"
    }, "'$BLOCK_NUMBER'"],
    "id": 1
  }' | python3 -m json.tool > "$ENGAGEMENT_ROOT/tenderly/rpc/sim-$LABEL.json"
```

### With state overrides (powerful for hypothesis testing)
```bash
curl -s "$TENDERLY_NODE_RPC_URL" -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenderly_simulateTransaction",
    "params": [{
      "from": "'$FROM'",
      "to": "'$TO'",
      "data": "'$CALLDATA'",
      "value": "0x0",
      "gas": "0x1312D00"
    }, "'$BLOCK_NUMBER'", {
      "'$CONTRACT_ADDR'": {
        "stateDiff": {
          "'$SLOT'": "'$VALUE'"
        }
      }
    }],
    "id": 1
  }' | python3 -m json.tool > "$ENGAGEMENT_ROOT/tenderly/rpc/sim-override-$LABEL.json"
```

## 3. Bundle Simulation (Atomic Multi-TX)

### Simulate multiple transactions in sequence (same block)
```bash
curl -s "$TENDERLY_NODE_RPC_URL" -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenderly_simulateBundle",
    "params": [[
      {
        "from": "'$ATTACKER'",
        "to": "'$TARGET1'",
        "data": "'$CALLDATA1'",
        "value": "0x0",
        "gas": "0x1312D00"
      },
      {
        "from": "'$ATTACKER'",
        "to": "'$TARGET2'",
        "data": "'$CALLDATA2'",
        "value": "0x0",
        "gas": "0x1312D00"
      }
    ], "'$BLOCK_NUMBER'"],
    "id": 1
  }' | python3 -m json.tool > "$ENGAGEMENT_ROOT/tenderly/rpc/bundle-$LABEL.json"
```

## 4. Virtual TestNet (Multi-Block Lab)

### Create a Virtual TestNet
```bash
# Via API
curl -s "https://api.tenderly.co/api/v1/account/$TENDERLY_ACCOUNT_SLUG/project/$TENDERLY_PROJECT_SLUG/vnets" \
  -X POST \
  -H "X-Access-Key: $TENDERLY_ACCESS_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "'$PROTOCOL_SLUG'-lab",
    "display_name": "'$PROTOCOL_SLUG' Investigation Lab",
    "fork_config": {
      "network_id": '$CHAIN_ID',
      "block_number": '$FORK_BLOCK'
    },
    "virtual_network_config": {
      "chain_config": {
        "chain_id": '$CHAIN_ID'
      }
    },
    "sync_state_config": {
      "enabled": false
    },
    "explorer_page_config": {
      "enabled": true,
      "verification_visibility": "src"
    }
  }' | python3 -m json.tool
```

### VNet Admin RPC Cheatcodes
```bash
# Snapshot state
curl -s "$TENDERLY_VNET_ADMIN_RPC_URL" -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"evm_snapshot","params":[],"id":1}'

# Revert to snapshot
curl -s "$TENDERLY_VNET_ADMIN_RPC_URL" -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"evm_revert","params":["'$SNAPSHOT_ID'"],"id":1}'

# Set time
curl -s "$TENDERLY_VNET_ADMIN_RPC_URL" -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"evm_setNextBlockTimestamp","params":["'$TIMESTAMP'"],"id":1}'

# Mine blocks
curl -s "$TENDERLY_VNET_ADMIN_RPC_URL" -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"evm_mine","params":[],"id":1}'

# Set balance
curl -s "$TENDERLY_VNET_ADMIN_RPC_URL" -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tenderly_setBalance","params":["'$ADDR'","0xDE0B6B3A7640000"],"id":1}'

# Set storage
curl -s "$TENDERLY_VNET_ADMIN_RPC_URL" -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tenderly_setStorageAt","params":["'$ADDR'","'$SLOT'","'$VALUE'"],"id":1}'
```

## 5. Simulation API (Project-Scoped)

### Full simulation with decoded traces
```bash
curl -s "$TENDERLY_PROJECT_API_URL/simulate" \
  -X POST \
  -H "X-Access-Key: $TENDERLY_ACCESS_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "save": true,
    "save_if_fails": true,
    "simulation_type": "full",
    "network_id": "'$CHAIN_ID'",
    "block_number": '$FORK_BLOCK',
    "from": "'$FROM'",
    "to": "'$TO'",
    "input": "'$CALLDATA'",
    "value": "'$VALUE'",
    "gas": 20000000
  }' | python3 -m json.tool > "$ENGAGEMENT_ROOT/tenderly/api/sim-$LABEL.json"
```

## 6. Evidence Extraction Helpers

### Extract touched addresses from saved trace
```bash
python3 -c "
import json, sys, re
data = json.load(open(sys.argv[1]))
addrs = set()
for item in data.get('result', {}).get('trace', []):
    if 'to' in item: addrs.add(item['to'].lower())
    if 'from' in item: addrs.add(item['from'].lower())
for addr in sorted(addrs):
    print(addr)
" "$ENGAGEMENT_ROOT/tenderly/rpc/trace-$TX_HASH.json" > "$ENGAGEMENT_ROOT/notes/touched-addresses.txt"
```

### Extract balance changes from simulation
```bash
python3 -c "
import json, sys
data = json.load(open(sys.argv[1]))
for change in data.get('result', {}).get('assetChanges', []):
    print(f\"{change.get('address')} {change.get('token_info',{}).get('symbol','ETH')} {change.get('amount')} ({change.get('type')})\")
" "$ENGAGEMENT_ROOT/tenderly/rpc/sim-$LABEL.json"
```

## Best Practices

1. **Save ALL JSON responses** under `<engagement_root>/tenderly/` — these are your evidence artifacts
2. **Use descriptive labels** in filenames (not just tx hashes)
3. **Prefer bundle simulation** for multi-step sequences (single RPC call, atomic)
4. **Use Virtual TestNets** for multi-block experiments (time manipulation, epoch crossing)
5. **Always decode** — Tenderly provides function names, arg values, and return values when contracts are verified
6. **State overrides** are your cheapest discriminator — test "what if X were true" without complex setup
