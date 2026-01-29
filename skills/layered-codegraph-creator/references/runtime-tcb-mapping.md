# Runtime / Precompile TCB Mapping (chain logic as a dependency)

Goal: avoid a common blind spot:
> some economically meaningful failures live in chain runtime / precompile validation paths, not in ordinary Solidity invariants.

Treat runtime and precompile logic as part of the protocol’s **trusted computing base (TCB)** when it:
- validates messages that trigger mint/credit/withdrawal, or
- performs cross-domain accounting (bridges, native modules), or
- provides privileged services to contracts (precompiles).

## Output (required artifact)
In the target protocol workspace, extend L12 (external dependencies) and L19 (control-plane) with:
- a list of runtime/precompile dependencies
- “accepted message” → “accounting recorded” coupling points
- smallest falsifier stubs (black-box if source is unavailable)

## What to treat as runtime/precompile dependencies
Evidence-driven (only include what the protocol actually uses):
- precompile addresses and their call sites
- bridge modules that accept “messages” or “proofs”
- chain-specific system contracts that validate deposits/withdrawals
- any module where “acceptance” is treated as proof of collateral or authority

## Procedure

### 1) Enumerate call sites
From SSOT L10/L12:
- list every call to a precompile/system contract
- list every “message handling” path (bridge receive, cross-domain executor)

### 2) Define the assumed guarantee
For each dependency, write:
- “If this call succeeds, what does the protocol assume is true?”
  - collateral exists
  - supply cap respected
  - signer set honored
  - message authenticity proven

### 3) Bind acceptance to accounting
Find the coupling points where that assumed guarantee becomes real:
- where collateral is recorded in storage
- where supply is incremented
- where custody is released

Write invariants that bind the two:
- “Minted claims must be backed by recorded collateral.”
- “Accepted message must correspond to exactly one accounted deposit.”

### 4) Evidence plan (black-box friendly)
Even if runtime code is not readable:
- E1: confirm on fork which dependency addresses are called and what success/failure signals look like.
- E2: write smallest tests that attempt malformed/edge-case messages and observe whether accounting can be advanced without the intended backing.

## Self-evaluation gate
You are not done if:
- the protocol uses any precompile/system contract in value-bearing paths and you have not written (a) its assumed guarantee and (b) an invariant binding that guarantee to accounting.

