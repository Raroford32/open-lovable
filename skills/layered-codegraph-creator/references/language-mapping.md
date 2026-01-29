# Language Mapping Guide

Use this to map language-specific constructs into the generic node/edge schema. Extend the schema only when the code requires it.

## Core mapping rules
- Use `MODULE` for the top-level deployable unit (contract/module/program/package).
- Use `FUNC` for any external entrypoint or internal callable function/instruction.
- Use `VAR` for persisted state: storage fields, account data, resources, PDA data.
- Use `EVENT` for emitted logs or runtime events.
- Use `MOD` for guards/attributes/macros enforcing access or preconditions.
- Use `EXT_CALLS` for cross-program or cross-contract invocations.
- Use `ROLE` and `ADDR` for all authority and trusted identity nodes.

## EVM (Solidity/Vyper)
- `MODULE`: contract
- `IFACE`: interface
- `LIB`: library
- `FUNC`: function, fallback/receive
- `MOD`: modifier
- `VAR`: state variable
- `EVENT`: event
- `ERROR`: custom error
- `EXT_CALLS`: external contract call
- `DELEGATECALLS`: delegatecall-based proxy calls

## Move (Aptos/Sui)
- `MODULE`: Move module or package
- `STRUCT`: resource struct
- `FUNC`: entry function
- `VAR`: resource fields stored on-chain
- `EVENT`: event handle emission
- `EXT_CALLS`: calls into other modules/packages
- `ROLE`: signer/authority derived from address

## Solana (Rust/Anchor)
- `MODULE`: program
- `FUNC`: instruction handler
- `VAR`/`ACCOUNT`: account data structs and PDA-backed storage
- `EXT_CALLS`: CPI (cross-program invocation)
- `ROLE`/`ADDR`: program-derived authorities, signer checks
- `EVENT`: events/logs

## Cairo/StarkNet
- `MODULE`: contract
- `FUNC`: external entrypoint/view
- `VAR`: storage variables
- `EVENT`: events
- `EXT_CALLS`: calls to other contracts
- `ROLE`/`ADDR`: admin, operator, or address-based gating

## CosmWasm
- `MODULE`: contract
- `FUNC`: execute/query/instantiate
- `VAR`: state in storage maps
- `EVENT`: attributes/logs
- `EXT_CALLS`: submessages / external contract calls
- `ROLE`/`ADDR`: sender/admin

## Use this rule when unsure
If a construct changes persistent state, model it as `VAR`/`ACCOUNT` and connect it with `READS`/`WRITES`. If a construct can be called from outside the module, model it as `FUNC` and include it in L5.
