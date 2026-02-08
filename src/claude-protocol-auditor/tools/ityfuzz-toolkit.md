# Tool: ItyFuzz Toolkit

## Overview
ItyFuzz is a sequence-driven smart contract fuzzer that discovers multi-step exploit sequences. It is the PRIMARY dynamic testing tool for finding unknown cross-contract vulnerabilities.

## Installation Check
```bash
ityfuzz --version
ityfuzz evm --help
```

## Campaign Modes

### 1. Onchain Fork (Address Mode) — MOST COMMON
For testing against real deployed protocol state:
```bash
ityfuzz evm \
  -t $TARGET_ADDRS \          # Comma-separated contract addresses
  -c $CHAIN_TYPE \            # eth, bsc, polygon, arbitrum, etc.
  -b $FORK_BLOCK \            # Fork block number
  -f \                        # Enable flash loans
  -k "$ETHERSCAN_API_KEY" \   # For source/ABI fetching
  -w $WORKDIR \               # Campaign output directory
  --detectors high_confidence
```

### 2. Offchain (Glob Mode) — For local artifacts
```bash
ityfuzz evm \
  -t './build/*' \            # Glob of .abi + .bin files
  --detectors high_confidence \
  -w $WORKDIR
```

### 3. Foundry Harness (Setup Mode) — For complex initialization
```bash
ityfuzz evm \
  -m test/Harness.sol:HarnessContract \
  -f \
  -w $WORKDIR \
  -- forge test
```

## Critical Flags Reference

### Target configuration
- `-t, --target` — Addresses (onchain) or glob (offchain)
- `-c, --chain-type` — Chain type for onchain mode
- `-b, --onchain-block-number` — Fork block for onchain
- `-m, --deployment-script` — Foundry harness file:contract
- `--force-abi address:path/to/abi.json` — Override ABI for specific address

### Search configuration
- `-f, --flashloan` — Enable flash loan support (ALWAYS use for DeFi)
- `--concolic` — Enable concolic execution (for hard branch conditions)
- `--concolic-caller` — Concolic for msg.sender constraints
- `--concolic-timeout` — Timeout for concolic solver
- `--run-forever` — Don't stop after first bug found
- `--seed N` — Random seed (vary across campaigns for diversity)

### Detectors
- `--detectors high_confidence` — Default, good starting point
- `--detectors fund_loss` — Focus on fund extraction
- `--detectors reentrancy` — Focus on reentrancy
- `--detectors selfdestruct` — Focus on self-destruct vulnerabilities
- `--detectors arbitrary_external_call` — Focus on arbitrary calls
- Custom combinations: `--detectors fund_loss,reentrancy,selfdestruct`

### Output control
- `-w, --work-dir` — Campaign output directory
- `--write-relationship` — Write relations.log (function call graph)

## Campaign Escalation Protocol

### Pass A: Baseline (5 minutes)
```bash
ityfuzz evm -t $TARGETS -c $CHAIN -b $BLOCK -f -k "$KEY" \
  --detectors high_confidence \
  -w $WORKDIR/passA
```

### Pass B: Concolic (15 minutes)
```bash
ityfuzz evm -t $TARGETS -c $CHAIN -b $BLOCK -f -k "$KEY" \
  --detectors high_confidence \
  --concolic --concolic-caller \
  -w $WORKDIR/passB
```

### Pass C: Wide detectors (30 minutes)
```bash
ityfuzz evm -t $TARGETS -c $CHAIN -b $BLOCK -f -k "$KEY" \
  --detectors fund_loss,reentrancy,selfdestruct,arbitrary_external_call \
  --concolic --concolic-caller \
  -w $WORKDIR/passC
```

### Pass D: Long hunt (1+ hours, varied seeds)
```bash
for seed in 1 42 1337 9999; do
  ityfuzz evm -t $TARGETS -c $CHAIN -b $BLOCK -f -k "$KEY" \
    --detectors high_confidence \
    --concolic --concolic-caller \
    --run-forever \
    --seed $seed \
    -w $WORKDIR/passD-seed$seed &
done
wait
```

## Output Analysis

### Work directory structure
```
$WORKDIR/
├── vuln_info.jsonl              # Machine-readable vulnerability findings
├── vulnerabilities/
│   ├── <bug_id>.t.sol           # Generated Foundry PoC
│   ├── <bug_id>_replayable      # Minimized replay trace
│   └── ...
├── corpus/                       # Interesting inputs (for resume)
├── relations.log                 # Function call relationships (if --write-relationship)
├── stdout.log                    # Captured stdout
└── stderr.log                    # Captured stderr
```

### Parse vulnerability findings
```bash
# Count findings
wc -l $WORKDIR/vuln_info.jsonl

# Pretty print findings
python3 -c "
import json
for line in open('$WORKDIR/vuln_info.jsonl'):
    data = json.loads(line)
    print(f\"Type: {data.get('type')}\")
    print(f\"Severity: {data.get('severity')}\")
    print(f\"Description: {data.get('description')}\")
    print('---')
"

# List generated PoCs
ls -la $WORKDIR/vulnerabilities/*.t.sol 2>/dev/null

# List replay files
ls -la $WORKDIR/vulnerabilities/*_replayable 2>/dev/null
```

### Replay a found trace
```bash
ityfuzz evm \
  --replay-file "$WORKDIR/vulnerabilities/*_replayable" \
  -t $TARGETS -c $CHAIN -b $BLOCK \
  -k "$KEY" \
  -w $WORKDIR/replay
```

## Harness Writing for Hypothesis Testing

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";

// Import protocol interfaces
interface IVault {
    function deposit(uint256 assets, address receiver) external returns (uint256);
    function withdraw(uint256 assets, address receiver, address owner) external returns (uint256);
    function totalAssets() external view returns (uint256);
    function totalSupply() external view returns (uint256);
    function convertToAssets(uint256 shares) external view returns (uint256);
}

contract HypothesisHarness is Test {
    IVault public vault;
    IERC20 public asset;

    address[] private _targets;

    function setUp() public {
        vm.createSelectFork(vm.envString("ETH_RPC_URL"), FORK_BLOCK);
        vault = IVault(VAULT_ADDR);
        asset = IERC20(ASSET_ADDR);

        // Set up targets for ItyFuzz
        _targets.push(address(vault));
        _targets.push(address(asset));

        // Give the fuzzer some tokens to work with
        deal(address(asset), address(this), 1000000e18);
        asset.approve(address(vault), type(uint256).max);
    }

    // Invariant: share price should never decrease by more than fees
    function invariant_sharePrice() public view {
        if (vault.totalSupply() == 0) return;
        uint256 pricePerShare = vault.convertToAssets(1e18);
        // Share price should be >= 1:1 (no loss without explicit fee)
        require(pricePerShare >= 0.99e18, "SHARE_PRICE_CRASHED");
    }

    // Invariant: solvency — assets >= liabilities
    function invariant_solvency() public view {
        uint256 totalAssets = vault.totalAssets();
        uint256 totalLiabilities = vault.totalSupply(); // simplified
        require(totalAssets >= totalLiabilities, "INSOLVENT");
    }

    function targetContracts() public view returns (address[] memory) {
        return _targets;
    }

    // Restrict selectors to the most interesting functions
    function targetSelectors() public pure returns (FuzzSelector[] memory) {
        FuzzSelector[] memory selectors = new FuzzSelector[](2);
        bytes4[] memory vaultSelectors = new bytes4[](2);
        vaultSelectors[0] = IVault.deposit.selector;
        vaultSelectors[1] = IVault.withdraw.selector;
        selectors[0] = FuzzSelector(VAULT_ADDR, vaultSelectors);
        return selectors;
    }
}
```

## Best Practices

1. **NEVER run blind fuzzing** — always start with a hypothesis
2. **Start narrow** — minimal target set for the specific hypothesis
3. **Widen only when stuck** — add contracts only if evidence suggests they're needed
4. **Use flash loans for DeFi** — `-f` flag unlocks capital-free attack sequences
5. **Vary seeds** — different seeds explore different state spaces
6. **Save EVERYTHING** — campaigns are expensive to reproduce
7. **Escalate systematically** — Pass A→B→C→D, don't jump to long runs
8. **Confirm with Tenderly** — fuzzer finds are hypotheses until traced with evidence
