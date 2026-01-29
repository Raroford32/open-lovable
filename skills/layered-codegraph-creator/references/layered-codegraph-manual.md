# Manual Layered Codegraph Workflow (Language-Agnostic)

This is a manual, data-driven workflow for building a complete protocol codegraph from smart-contract code in any language/runtime. The graph is layered: the same nodes appear in multiple views (structure, calls, storage, authority, value flow, upgrades, external systems, etc.).

## Table of contents
- The one rule that makes this complete
- Step 0 - Derive the schema from the code (no predefined schema)
- Step 1 - Repository inventory layer (L1)
- Step 2 - Contract/module catalog layer (L2)
- Step 3 - Type system layer (L3)
- Step 4 - Inheritance + override layer (L4)
- Step 5 - External surface layer (L5)
- Step 6 - Deployment + topology layer (L6)
- Step 7 - Authority layer (L7)
- Step 8 - Storage layer (L8)
- Step 9 - Function semantics layer (L9)
- Step 10 - Call graph layer (L10)
- Step 11 - Value & accounting layer (L11)
- Step 12 - External systems + trust assumptions (L12)
- Step 13 - State machine layer (L13)
- Step 14 - Invariants layer (L14)
- Discovery extensions (L15-L18)

## The one rule that makes this complete
Do not draw diagrams first. Create a single source of truth (SSOT) for nodes and edges, then render any diagrams from it. This prevents silent omissions.

Recommended SSOT layout (Markdown only):
- `codegraph/00_schema.md` - the schema used (node/edge types and attributes)
- `codegraph/01_nodes.md` - every entity gets a stable ID
- `codegraph/02_edges.md` - every relationship is an edge with a type
- `codegraph/layers/` - each layer is a filtered view of the same SSOT

## Step 0 - Derive the schema from the code (no predefined schema)
Start with an empty schema and let the code define it. Do not assume a fixed list of node or edge types.

Rules:
- Create `codegraph/00_schema.md` first.
- Include these required headings (keep lists empty until the code forces entries):
  - `## Node Types`
  - `## Edge Types`
  This matches the expectations of `scripts/validate_codegraph.py`.
- As you read the code, add node/edge types only when you see them in the code or build config.
- Before using any label in `01_nodes.md` or `02_edges.md`, declare it in `00_schema.md`.
- If you prefer different label names than the ones shown later in this manual, add a label map in `00_schema.md` and stay consistent.

Schema discovery prompts (do not prefill; use only if the code shows them):
- Source artifacts and build config (files, packages, compiler flags, remappings).
- Deployable units and modules (contracts, libraries, interfaces).
- Types and data definitions (structs, enums, aliases).
- Functions/entrypoints and guards/modifiers.
- Persistent state (storage variables, slots, account data).
- Events/errors/logs.
- Authority and identities (roles, addresses, signers).
- External systems and assets.
- Deployment topology (proxies, factories, implementations).
- Trust assumptions, state machines, invariants.

Label note:
- Any label names in this manual (for example `READS`, `WRITES`) are examples. Use them or replace them, but define them in `00_schema.md` before use.

## Step 1 - Repository inventory layer (L1)
Create `L1_repo.md`:
1. List every contract source file and classify it:
   - core (critical state and accounting)
   - periphery (routers, helpers, adapters)
   - interfaces
   - libraries
   - adapters/integrations
   - mocks/tests (exclude from production graph but capture assumptions)
2. For each `FILE` node, record:
   - language version/pragma/feature gates
   - imports
   - declared modules/contracts/interfaces

Output: a complete `IMPORTS` graph and `DECLARES` coverage.

Completeness gate: every source file appears exactly once as a `FILE` node.

## Step 2 - Contract/module catalog layer (L2)
Create `L2_catalog.md` with one card per `MODULE`/`LIB`/`IFACE`:
- Purpose in one sentence
- Stateful or stateless
- Deployable or library-only
- Upgrade-facing (proxy/upgrade path)
- External entrypoints count (public/external/entry functions + default handlers)

Completeness gate: every declared module/library/interface is in this catalog.

## Step 3 - Type system layer (L3)
For each `STRUCT`/`ENUM`/`TYPE`:
- where declared
- fields/variants
- which `VAR` uses it
- which `FUNC` takes/returns it

Edges:
- `DECLARES (MODULE -> STRUCT/ENUM/TYPE)`
- `USES_TYPE (VAR/FUNC -> TYPE/STRUCT/ENUM)`

Completeness gate: every struct/enum/type used anywhere has a node.

## Step 4 - Inheritance + override layer (L4)
For each module:
- List full linearized inheritance/trait/impl chain (in order)
- List overridden functions and their origins
- List inherited modifiers/guards used

Edges:
- `INHERITS`
- `IMPLEMENTS`
- `OVERRIDES (FUNC -> FUNC)`

Completeness gate: every override in code appears as an `OVERRIDES` edge.

## Step 5 - External surface layer (L5)
For each module, enumerate:
- public/external/entrypoint functions
- default handlers (fallback/receive or runtime equivalents)
- standard callbacks and hooks (token receivers, DEX callbacks, cross-chain handlers, program hooks)

For each `FUNC`:
- signature
- visibility
- mutability
- modifiers/guards (exact order)
- whether it can move value
- whether it can change auth

Edges:
- `HAS_MEMBER`
- `GUARDED_BY`
- `TRANSFERS` (if applicable)

Completeness gate: every public/external/entry function is present, including inherited entrypoints.

## Step 6 - Deployment + topology layer (L6)
A protocol includes how contracts are instantiated.

Create nodes for:
- `PROXY` patterns (transparent/UUPS/beacon/diamond/etc.)
- `FACTORY` patterns (CREATE2, clones, program deployers)
- `IMPL` targets
- registries/singletons

For each deployable piece:
- constructor/initializer args
- who can initialize
- one-time guards
- whether a factory produces instances

Edges:
- `CREATES (FACTORY_FUNC -> MODULE_INSTANCE_TYPE)`
- `INITIALIZES (FUNC -> VAR set)`
- `PROXY_POINTS_TO (PROXY -> IMPL)`
- `UPGRADES_TO (upgrade FUNC/ROLE -> IMPL)`

Completeness gate: every path from deployment entry to live stateful instance is described.

## Step 7 - Authority layer (L7)
Build the permission graph. No shortcuts.

Create `ROLE` nodes for any authority pattern:
- owner/admin/guardian/keeper
- access-control roles
- explicit address checks
- signature-based auth

For each function, record all gating logic:
- modifiers/guards
- inline requires/checks
- signature checks
- tx.origin checks (if any)

Edges:
- `REQUIRES_ROLE`
- `GUARDED_BY`
- `WRITES_AUTH`
- `TRUSTS (ROLE/ADDR -> authority root)`

Completeness gate: for every state-changing entrypoint, you can answer "Who can call this?" with a concrete role/address set (even if "anyone").

## Step 8 - Storage layer (L8)
This layer hides upgrade and accounting bugs.

For each stateful module:
1. List state vars in exact order
2. Identify:
   - packed fields
   - mappings/dictionaries and key/value types
   - dynamic arrays
   - nested structs
   - storage gaps/reserved slots
   - namespaced storage or runtime-specific storage containers
3. Identify special slots/accessors:
   - proxy/admin slots
   - manual storage in assembly/unsafe blocks
   - hashed slot derivations

Edges:
- `HAS_MEMBER (MODULE -> VAR)`
- `STORAGE_SLOT (VAR -> slot descriptor)`
- `USES_STORAGE_NAMESPACE (MODULE -> namespaceId)`

Completeness gate: every manual storage access is captured as a storage access node/edge.

## Step 9 - Function semantics layer (L9)
Go function-by-function (entrypoints first, then internals).

For each `FUNC`:
- Preconditions (requires)
- Postconditions (must hold after)
- Storage reads/writes (exact vars)
- Events/logs emitted
- External calls performed
- Revert modes (custom errors, error strings)
- Reentrancy posture (external call before state finalization)

Edges:
- `READS`
- `WRITES`
- `EMITS`
- `EXT_CALLS` / `DELEGATECALLS` / `STATICCALLS`
- `REVERTS_WITH`

Completeness gate: every external call site is recorded as an edge.

## Step 10 - Call graph layer (L10)
Build call trees for each entrypoint:
- mark call kind (internal/external/delegate/static)
- indicate before/after critical state writes
- mark reentrancy risk points

Edges:
- `CALLS`, `EXT_CALLS`, `DELEGATECALLS`, `STATICCALLS`

Completeness gate: every function referenced by a call edge exists as a node.

## Step 11 - Value & accounting layer (L11)
Create `ASSET` nodes for:
- tokens/coins/NFTs
- LP/receipt/share tokens
- native currency

For each function that touches assets:
- debits/credits
- fee formulas and rounding
- custody model (held vs sent out)
- mint/burn authorities

Add an explicit custody map when value can sit in multiple places (vaults/strategies/DEX pools/bridge escrows), or when the protocol uses “cash” accessors:
- See `asset-custody-mapping.md` for custody definitions and the minimal schema hooks.
- See `numeric-semantics.md` for units/scale/rounding annotations (avoid hand-waving “modulo rounding”).

Edges:
- `TRANSFERS`
- `MINTS` / `BURNS`
- `COLLECTS_FEE`
- `ACCOUNTING_DEPENDS_ON (VAR -> VAR)`

Completeness gate: for each asset, list all functions that can move it and all functions that change its accounting variables.

## Step 12 - External systems + trust assumptions (L12)
For every external dependency:
- what it is (oracle, DEX, bridge, registry)
- the assumption relied on (freshness, bounds, immutability)
- failure mode if assumption breaks
- whether calls are guarded (try/catch or fallback behavior)

For late-stage audits, add an **Influence Budget** per dependency input:
- Use `references/external-influence-budgets.md`.
- Treat each external input as a variable with a permissionless influence budget (actions, cost, bounds, latency) and an E1/E2 evidence plan.

Edges:
- `TRUSTS (MODULE/FUNC -> EXTSYS : assumption)`
- `EXT_CALLS (FUNC -> EXTSYS)`

Completeness gate: every hardcoded address, registry, oracle, router, messenger, or precompile used appears here.

## Step 13 - State machine layer (L13)
If the protocol has phases (paused/unpaused, epochs, rounds, auctions, governance), model them explicitly.

Nodes and edges:
- `STATE` nodes
- `TRANSITIONS (FUNC : fromState -> toState)`
- `ENABLED_IN (FUNC -> STATE)`
- `DISABLED_IN (FUNC -> STATE)`

Completeness gate: every phase/flag variable participates in a state model.

## Step 14 - Invariants layer (L14)
Write what must never be false:
- conservation (sum of balances = total supply)
- bounds (utilization <= 100%)
- monotonicity (timestamps only increase)
- authorization (only admin can change X)
- upgrade safety (storage layout compatible)

For deeper, code-derived invariant mining (beyond these examples), use `references/invariant-mining.md`.

For system-level invariants (custody↔claims↔debt), assemble a balance sheet first:
- Use `references/balance-sheet-assembly.md`.

Edges:
- `MAINTAINS (FUNC -> INVARIANT)`
- `INVOLVES (INVARIANT -> VAR/ASSET/ROLE)`

Completeness gate: every critical accounting/auth variable has at least one invariant.

## Discovery extensions (L15-L22)
If the goal is exploit discovery (not just documentation), add these layers after L14. They are still evidence-driven and schema-extensible.

### Step 15 - Attack surface layer (L15)
Create `codegraph/layers/L15_attack_surface.md`:
- For each unprivileged entrypoint, list:
  - attacker-controlled levers (inputs/order/timing/caller type/token behavior)
  - the exact checks/guards it must satisfy
  - custody movements and ledger updates (link to L11)
  - external dependencies relied on (link to L12)
Optional: if you already have a partial SSOT, run `scripts/triage_entrypoints.py` to rank functions by value-touch edges and explicit role requirements, then start L15 from the top of that list.
Autopilot default: if the repo already contains fork/sim tests (Foundry/Hardhat/etc.), use them as the initial “live falsifiers” and backfill L15 from the entrypoints those tests exercise (highest signal, lowest cost).

Completeness gate: every public/external entrypoint in L5 appears here, classified as privileged or unprivileged.

### Step 16 - Exploit primitives layer (L16)
Create `codegraph/layers/L16_primitives.md`:
- Generate capability statements: “a normal user can force the system to accept state X.”
- For each primitive, include broken assumption + on-chain preconditions + measurable effect + evidence pointers.
- Use `exploit-primitives.md` for the exact card format and constraints.
- For scenario synthesis that intentionally composes unrelated levers/edges into a route, use `references/scenario-synthesis.md`.
Hard gate: discard any primitive that requires assumed compromised keys/roles unless the role can be obtained permissionlessly via a publicly reachable state transition.

Completeness gate: every L15 entrypoint has at least one “no/unknown/yes” primitive attempt, with the smallest falsifier next.

### Step 17 - Falsifiers & proof layer (L17)
Create `codegraph/layers/L17_falsifiers.md`:
- For each primitive, write the smallest fork/sim test that would prove or disprove it.
- Prove only on fork/sim; avoid turning notes into real-world draining guides.
- Use `falsifier-harness.md` for a compact proof template + friction checklist.
- Record the exact cost (gas units + any required capital) and the measurable delta for each proved case.

Completeness gate: top-ranked primitives (by value bound) each have an executable falsifier plan.

### Step 18 - Learnings & mutation layer (L18)
Create `codegraph/layers/L18_learnings.md`:
- After each falsifier attempt, record: what killed it, what new lever was discovered, and the next mutated hypothesis.
- Keep it capability-first (no labels) and evidence-linked (point back to the SSOT nodes/edges and the test artifact).

Also maintain an Operator Registry in L18:
- Use `references/operator-mining.md`.
- Each newly discovered semantic discontinuity must produce an operator card and at least one hypothesis.

If focus collapses prematurely or reasoning starts “pattern matching,” use `references/anti-bias-prompts.md` and restart from SSOT evidence.

Completeness gate: every “top-ranked” primitive has a learning entry, even if disproved.

### Step 19 - Control-plane layer (L19)
Create `codegraph/layers/L19_control_plane.md`:
- Build a Control-Plane Objective Map: upgradeability, initialization, roles, governance executors, and delegated execution roots.
- Treat “future behavior control” as value-bearing: record how a normal user could reach control writes (including ordering and governance routes).
- Use `references/control-plane-mapping.md`.
- If the protocol relies on runtime/precompile validation in value-bearing paths, integrate it here and in L12 using `references/runtime-tcb-mapping.md`.

Completeness gate:
- every control-plane variable has: (a) read sites, (b) write paths, (c) guard chain, and (d) at least one invariant + falsifier stub.

### Step 20 - Approval surface layer (L20)
Create `codegraph/layers/L20_approval_surface.md`:
- Map user-facing spenders (routers/vaults/executors/legacy contracts) and how approvals are consumed.
- Identify routes that can convert approvals into attacker-chosen token movements.
- Use `references/approval-surface-mapping.md`.

Completeness gate:
- every user-facing spender surface has at least one “can/cannot/unknown” primitive attempt and a smallest falsifier plan.

### Step 21 - Ordering model layer (L21)
Create `codegraph/layers/L21_ordering_model.md`:
- For each top-ranked primitive/hypothesis, classify ordering dependence:
  - ordering-independent / ordering-sensitive / multi-tx
- Add a smallest ordering falsifier plan for ordering-sensitive hypotheses.
- Use `references/ordering-harness.md`.

Completeness gate:
- every top-ranked primitive has an ordering classification and (if needed) an ordering falsifier.

### Step 22 - Cycle mining layer (L22)
Create `codegraph/layers/L22_cycle_mining.md`:
- Inventory conversion edges (assets↔shares, shares↔rewards, token↔LP, debt↔collateral).
- Propose candidate cycles and write smallest falsifiers (cycle-once, cycle-N, amount-regime probes).
- Use `references/cycle-mining.md`.

Completeness gate:
- if the protocol has conversions, at least one cycle hypothesis and one cycle-N drift probe exist (with a falsifier plan).

## Manual workflow (keeps you sane)
Pass 0: Alignment + intent (build configs, deployment snapshot, bytecode alignment, intent mining)
Pass A: Enumerate everything (L1-L6)
Pass B: Authority + storage (L7-L8)
Pass C: Per-entrypoint deep dive (L9-L11)
Pass D: System truth (L12-L14)
Pass E (optional): Attack primitives + falsifiers (L15-L18)

## Protocol-specific completeness checklist (build it during the run)
Create a checklist that is derived from the protocol’s actual code and build config. Do not use a generic or prefilled list. The checklist must evolve as you discover new constructs.

How to build it:
- Start empty. As you encounter a concrete construct (file, module, entrypoint, external call site, storage slot, role gate, asset movement, external dependency, upgrade path), add a checklist item tied to that exact construct.
- Each checklist item must reference a concrete node/edge or a code location that will become one.
- If you discover a new pattern or subsystem mid-way, add new checklist items immediately and revisit earlier layers to reconcile.

How to close it:
- After L14, run a full checklist pass. Any unchecked item is a hard stop: return to the code and fill in nodes/edges/layers until the item is resolved.
- If the checklist grows during closure, restart the pass. Finish only when all items are checked and the SSOT matches every checklist item.

## Nothing-missed checklist
You are not done until all of these are true:
- Deployment snapshot exists and bytecode alignment is recorded.
- Intent ledger exists and each intent maps to an invariant or an explicit gap.
- Every source file is in L1.
- Every module/library/interface is in L2.
- Every struct/enum/custom type used is in L3.
- Every inheritance/override is in L4.
- Every public/external/entry function (including inherited) is in L5.
- Every initializer/deployment topology is in L6.
- Every state-changing entrypoint has a concrete caller set in L7.
- Every storage var and every manual storage access is in L8.
- Every function has READ/WRITE/EMIT/REVERT annotations in L9 (reachable ones at minimum).
- Every external call site is recorded in L10/L12.
- Every asset movement has edges and accounting ties in L11.
- Every external dependency has a trust assumption in L12.
- Every phase/flag variable participates in L13.
- Every critical accounting/auth variable has at least one invariant in L14.

## Final deliverable layout (recommended)
- `codegraph/00_schema.md`
- `codegraph/01_nodes.md`
- `codegraph/02_edges.md`
- `codegraph/layers/L1_repo.md`
- `codegraph/layers/L2_catalog.md`
- `...`
- `codegraph/layers/L14_invariants.md`
- `codegraph/diagrams/` (optional)

## Tiny example of nodes/edges
Node entry:
- `FUNC:Vault.deposit(address,uint256)`
  - in: `MODULE:Vault`
  - visibility: `external`
  - payable: `no`

Edge entries:
- `GUARDED_BY | FUNC:Vault.deposit -> MOD:nonReentrant`
- `READS      | FUNC:Vault.deposit -> VAR:Vault.totalAssets`
- `WRITES     | FUNC:Vault.deposit -> VAR:Vault.totalShares`
- `EXT_CALLS  | FUNC:Vault.deposit -> ASSET:USDC | method=transferFrom`
- `EMITS      | FUNC:Vault.deposit -> EVENT:Deposit(address,uint256,uint256)`

If you do this correctly, the codegraph answers questions like:
- Which paths lead from unprivileged entrypoints to value transfers?
- Which functions can change oracle addresses?
- Which storage variables are written before external calls?
- Which authority can upgrade which implementation?
- Where do we rely on external systems behaving correctly?
