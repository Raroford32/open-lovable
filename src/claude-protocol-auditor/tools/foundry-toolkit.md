# Tool: Foundry Toolkit

## Overview
Foundry (forge, cast, anvil, chisel) is the primary on-chain interaction and PoC development toolkit.

## Key Commands for Protocol Auditing

### Cast — On-Chain Queries (Read-Only)

```bash
# Chain/block validation
cast chain-id --rpc-url "$RPC_URL"
cast block $FORK_BLOCK --rpc-url "$RPC_URL"
cast block-number --rpc-url "$RPC_URL"

# Contract interrogation
cast code $ADDR --rpc-url "$RPC_URL" -b $FORK_BLOCK          # Get bytecode
cast code $ADDR --rpc-url "$RPC_URL" -b $FORK_BLOCK | wc -c  # Bytecode size
cast abi-decode "function()(address)" $(cast call $ADDR "owner()" --rpc-url "$RPC_URL" -b $FORK_BLOCK)

# Storage reads
cast storage $ADDR $SLOT --rpc-url "$RPC_URL" -b $FORK_BLOCK
# EIP-1967 implementation slot
cast storage $ADDR 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc --rpc-url "$RPC_URL" -b $FORK_BLOCK
# EIP-1967 admin slot
cast storage $ADDR 0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103 --rpc-url "$RPC_URL" -b $FORK_BLOCK
# Beacon slot
cast storage $ADDR 0xa3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50 --rpc-url "$RPC_URL" -b $FORK_BLOCK

# Mapping/array slot computation
cast index address $KEY $BASE_SLOT      # mapping(address => ...)
cast index uint256 $KEY $BASE_SLOT      # mapping(uint256 => ...)

# Balance queries
cast balance $ADDR --rpc-url "$RPC_URL" -b $FORK_BLOCK       # ETH balance
cast call $TOKEN "balanceOf(address)(uint256)" $ADDR --rpc-url "$RPC_URL" -b $FORK_BLOCK  # ERC20 balance
cast call $TOKEN "totalSupply()(uint256)" --rpc-url "$RPC_URL" -b $FORK_BLOCK

# Function calls (read-only)
cast call $ADDR "functionName(argTypes)(returnTypes)" $ARGS --rpc-url "$RPC_URL" -b $FORK_BLOCK

# ABI encoding/decoding
cast abi-encode "function(uint256,address)" $AMOUNT $ADDR
cast abi-decode "function()(uint256,address)" $DATA
cast 4byte $SELECTOR                    # Look up function signature
cast sig "transfer(address,uint256)"    # Get selector for signature

# Transaction analysis
cast tx $TX_HASH --rpc-url "$RPC_URL"
cast receipt $TX_HASH --rpc-url "$RPC_URL"
cast run $TX_HASH --rpc-url "$RPC_URL"  # Replay transaction with trace
```

### Forge — Testing and PoC Development

```bash
# Fork testing
forge test --fork-url "$RPC_URL" --fork-block-number $FORK_BLOCK -vvvv

# Specific test
forge test --match-test "test_exploit" --fork-url "$RPC_URL" --fork-block-number $FORK_BLOCK -vvvv

# Gas reporting
forge test --gas-report --fork-url "$RPC_URL" --fork-block-number $FORK_BLOCK

# Storage layout inspection
forge inspect $CONTRACT storage-layout --pretty

# Contract compilation
forge build

# Script execution (for complex PoCs)
forge script script/Exploit.s.sol --fork-url "$RPC_URL" --fork-block-number $FORK_BLOCK -vvvv
```

### Anvil — Local Fork

```bash
# Start local fork
anvil --fork-url "$RPC_URL" --fork-block-number $FORK_BLOCK --port 8545

# With state file (for reproducibility)
anvil --fork-url "$RPC_URL" --fork-block-number $FORK_BLOCK --dump-state state.json
anvil --load-state state.json

# With impersonation
anvil --fork-url "$RPC_URL" --fork-block-number $FORK_BLOCK --auto-impersonate
```

### Forge Cheatcodes (in Solidity tests)

```solidity
// Fork management
vm.createSelectFork(vm.envString("RPC_URL"), FORK_BLOCK);

// Account manipulation
vm.deal(address(this), 1000 ether);                          // Set ETH balance
deal(address(token), address(this), 1000000e18);             // Set ERC20 balance
vm.prank(targetAddress);                                      // Next call as targetAddress
vm.startPrank(targetAddress);                                 // All calls as targetAddress

// Time/block manipulation
vm.warp(block.timestamp + 1 days);                           // Set timestamp
vm.roll(block.number + 100);                                  // Set block number

// Storage manipulation
vm.store(address(contract), bytes32(slot), bytes32(value));   // Write storage
vm.load(address(contract), bytes32(slot));                    // Read storage

// Expectations
vm.expectRevert("message");                                   // Expect revert
vm.expectEmit(true, true, false, true);                      // Expect event

// Snapshots
uint256 snapshot = vm.snapshot();                              // Save state
vm.revertTo(snapshot);                                         // Restore state

// Labels (for trace readability)
vm.label(address(contract), "VaultProxy");
```

## PoC Template for Protocol Exploits

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";

interface IProtocol {
    // Add protocol-specific interfaces
}

contract ExploitPoC is Test {
    // Protocol references
    IProtocol public target;
    address public attacker = address(0xBEEF);

    // Constants
    uint256 constant FORK_BLOCK = 0; // SET THIS

    function setUp() public {
        vm.createSelectFork(vm.envString("ETH_RPC_URL"), FORK_BLOCK);
        target = IProtocol(0x0); // SET THIS
        vm.label(address(target), "Target");
        vm.label(attacker, "Attacker");
    }

    function test_exploit() public {
        // Record pre-attack state
        uint256 preBalance = address(attacker).balance;

        vm.startPrank(attacker);

        // === SETUP PHASE ===
        // Prepare attack prerequisites

        // === DISTORTION PHASE ===
        // Manipulate protocol state

        // === REALIZATION PHASE ===
        // Extract profit

        // === UNWIND PHASE ===
        // Clean up (repay flash loans, etc.)

        vm.stopPrank();

        // Record post-attack state
        uint256 postBalance = address(attacker).balance;

        // Assert profit
        uint256 profit = postBalance - preBalance;
        console.log("Profit (wei):", profit);
        console.log("Profit (ETH):", profit / 1e18);
        assertGt(profit, 0, "Attack must be profitable");

        // Assert specific invariant violation
        // assertLt(target.totalAssets(), target.totalLiabilities(), "Solvency violated");
    }

    function test_exploit_robustness_gas_plus_20() public {
        // Same exploit with gas * 1.2
        // Verify still profitable
    }

    function test_exploit_robustness_liquidity_minus_20() public {
        // Same exploit with reduced liquidity
        // Verify still profitable
    }
}
```
