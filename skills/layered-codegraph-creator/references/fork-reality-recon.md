# Fork Reality Recon + Deployment Snapshot (make “the live system” explicit)

Goal: eliminate the most common late-stage failure mode — auditing the *wrong* deployed topology/state.

This procedure produces a **deployment snapshot** that the SSOT (especially L6/L12/L13/L14) and Foundry falsifiers can anchor to.

## Non-negotiable rules
- Treat on-chain state as the authority for “what is live,” but treat repo code as the authority for “what it is supposed to be.”
- Never assume a deployed address/topology. Prove it (code exists, proxy points to impl, registry enumerates instances, etc.).
- Record everything with fork metadata so every test is reproducible.

## Required inputs
- `RPC_URL`
- `DEV_FORK_BLOCK`
- `PROMOTION_FORK_BLOCK`
- Any starting hints (optional): docs/README deployment addresses, registry address, factory address, governance timelock address.

## Required output artifact
Create a file **in the target protocol workspace** (not inside this skill folder):
- `deployment_snapshot.md`

Treat `deployment_snapshot.md` as read-only truth you can cite from SSOT layers and Foundry tests.

Minimum sections:
- Fork metadata (chainId, dev/promotion blocks, timestamps)
- Address book (core instances, registries, factories, proxies, implementations)
- Proxy/upgrade graph (proxy → implementation; beacon/diamond if applicable)
- Live gating state (pause flags, caps/limits, market enable flags, oracle freshness/validity gates)
- External dependencies + config (oracles/DEX routers/bridges/registries)
- Enumeration method used (how instances were discovered)

## Procedure

### 0) Freeze fork blocks and record metadata
- Resolve `chainId` and record it.
- Record block timestamps for `DEV_FORK_BLOCK` and `PROMOTION_FORK_BLOCK`.

Example (EVM / Foundry `cast`):
- `cast chain-id --rpc-url "$RPC_URL"`
- `cast block "$DEV_FORK_BLOCK" --rpc-url "$RPC_URL"`
- `cast block "$PROMOTION_FORK_BLOCK" --rpc-url "$RPC_URL"`

### 1) Enumerate candidate “roots” (where deployed topology is discoverable)
Derive candidates from *evidence*, not guesswork:
- Repo: deployment scripts, config files, hardcoded addresses, test fixtures.
- On-chain: registry contracts, factory events, governor/timelock ownership graphs.

Write every candidate root address into `deployment_snapshot.md` with:
- why it was selected (evidence pointer)
- how it will be validated (call, event scan, storage slot proof)

### 2) Classify each address (what is it, and is it code?)
For each candidate address:
- Confirm code exists (non-empty bytecode).
- Record the bytecode hash (or at least code size) at the fork block.

Example (EVM):
- `cast code <addr> --rpc-url "$RPC_URL"`

### 3) Prove proxy patterns (EVM) instead of assuming them
If a contract appears upgradeable, prove what kind:

#### EIP-1967 (transparent/UUPS) slots
Use on-chain storage reads at the proxy address.
- Implementation slot:
  - `0x360894A13BA1A3210667C828492DB98DCA3E2076CC3735A920A3CA505D382BBC`
- Admin slot:
  - `0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103`
- Beacon slot:
  - `0xa3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50`

Example:
- `cast storage <proxy> <slot> --rpc-url "$RPC_URL"`

Record:
- proxy address
- implementation address (if any)
- admin address (if any)
- beacon address (if any)

#### Beacon proxies
- If beacon slot is set, read the beacon’s implementation pointer (method depends on beacon implementation).
- Record beacon → implementation and who can upgrade the beacon.

#### Diamond (EIP-2535) or custom dispatch
- Prove it by:
  - detecting loupe selectors (if present), or
  - locating the dispatch table storage and extracting facet addresses.
- Record facet set and upgrade authority.

#### Minimal proxies (EIP-1167) / clones
- Identify clones via runtime code pattern (optional) and record their implementation target.
- Prefer factory-event enumeration rather than bytecode heuristics.

### 4) Enumerate instances (don’t stop at one address)
This is required for “battle-tested protocols,” where the exploit surface is often per-market/per-vault.

Use evidence-driven enumeration methods:
- **Registry enumeration**: call list functions (`allMarkets()`, `getVault(i)`, etc.).
- **Factory events**: scan `Created/Deployed/MarketAdded` events.
- **Governance actions**: scan proposals/queued transactions that add markets or update config.

Record for each instance:
- instance address
- instance type (what it is)
- discovery method (registry call, event scan, etc.)
- link to controlling registry/factory

### 5) Snapshot live gating state (what makes routes dead/alive)
For each top-value instance:
- Pause flags / emergency switches
- Per-market caps/limits
- Per-user limits (if any)
- Market enabled flags
- Oracle freshness/bounds checks (if present)

Record each gate with:
- variable name (or getter)
- read method (call)
- observed value at `DEV_FORK_BLOCK`
- whether it blocks a permissionless route

### 6) Snapshot external dependencies and their current config
For each dependency:
- Address
- What it controls (price/rate/router/bridge)
- How the protocol reads it (function call sites in SSOT)
- What a normal user can influence (to be modeled later as an influence budget)

### 7) Write SSOT bindings (connect snapshot → codegraph)
Use the snapshot to ground L6/L12:
- Add `ADDR`/`ROLE` nodes for real deployed addresses and authority roots.
- Add topology edges:
  - `PROXY_POINTS_TO` / `UPGRADES_TO`
  - registry/factory instance edges (as needed by the code)
- Add trust edges for dependencies (`TRUSTS`, `EXT_CALLS`).

Do not invent node/edge types. Extend `codegraph/00_schema.md` only when the code/topology requires it.

### 8) Validate the snapshot (minimum sanity checks)
- Confirm every “core” address in the snapshot has code.
- Confirm every proxy has a non-zero implementation pointer.
- Confirm the implementation code also exists.
- Confirm at least one read-only smoke check succeeds for key vars.

### 9) Align deployed code with repo build (avoid auditing the wrong binary)
- Compile the repo using the exact compiler settings discovered in Pass 0 (version, optimizer, remappings).
- Compare deployed runtime bytecode with compiled runtime bytecode (ignore metadata where applicable).
- If mismatch exists, fetch verified source + compiler settings using Etherscan v2 API (see `references/rpc-ethersacnv2.md`) and record the discrepancy.
- Treat unresolved mismatches as a blocking unknown; do not proceed with SSOT assumptions until resolved.

## Non-EVM analogs (keep the same intent)
If not EVM:
- Still create `deployment_snapshot.md`.
- Replace “proxy slots” with the platform’s upgrade mechanism:
  - Solana: program account + program data account + upgrade authority.
  - Move: package versioning/upgrade authority patterns.
  - Cairo/StarkNet: class hash + implementation upgrade path.

The invariant is the same: **prove what code is live and who can change it.**
