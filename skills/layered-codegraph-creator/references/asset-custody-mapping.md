# Asset Custody Mapping (for L11 and exploit primitives)

Goal: make “where value actually sits” explicit, so later reasoning can talk about *real balances vs internal ledgers vs claims*.

## Definitions (use these words consistently)
- **Asset**: the thing with external realizable value (ERC20/native/NFT, or an external claim like a staked LP).
- **Custody location**: an on-chain address (contract/EOA) that actually holds the asset at rest (`balanceOf(holder)` / native balance).
- **Internal ledger**: protocol storage that tracks balances/claims/debts (may diverge from reality).
- **Claim token**: a transferable representation of a claim (shares/LP/receipt/debt token). A claim is not custody.

## Minimal schema extensions (declare only if you need them)
Node types (examples):
- `CUSTODY` (an `(ASSET, holder)` pair)
- `UNIT` (optional: see `numeric-semantics.md`)

Edge types (examples):
- `HELD_BY` (`ASSET -> ADDR/MODULE/INSTANCE`) with `method=balanceOf|nativeBalance|vaultShare`
- `CUSTODY_OF` (`CUSTODY -> ASSET`)
- `CUSTODIAN` (`CUSTODY -> ADDR/MODULE/INSTANCE`)
- `MEASURES_BALANCE_AT` (`FUNC -> CUSTODY`) with `how=balanceOf(address(this))|getCash()|...`
- `CREDITS_LEDGER` / `DEBITS_LEDGER` (`FUNC -> VAR`) with `asset=...`

Do not prefill these labels. If you use different names, add a label map in `codegraph/00_schema.md`.

## Procedure: build the custody map
1. List every `ASSET` that matters (underlyings, share/receipt tokens, reward tokens, debt representations, fee tokens).
2. For each `ASSET`, enumerate plausible holders:
   - protocol contracts (`address(this)` patterns)
   - per-user escrow contracts (vault per user, proxy per market)
   - external systems (DEX pools, staking contracts, bridge escrow, oracle feed contracts if value-bearing)
3. For each holder candidate, find *how the protocol measures reality*:
   - `IERC20(asset).balanceOf(holder)`
   - `address(holder).balance` (native)
   - “cash” accessors (`getCash()`) and what they call
   - wrapper share conversions (`vault.convertToAssets()`, `exchangeRate`, etc.)
4. Create custody entries:
   - Prefer explicit `CUSTODY:ASSET@HOLDER` nodes if the protocol has many holders/strategies.
   - For simple protocols, `HELD_BY` edges may be enough.
5. For each `FUNC` that moves value, annotate:
   - **Direction**: in/out/mint/burn/escrow/claim
   - **Custody change**: which holder loses/gains real balance
   - **Ledger change**: which `VAR`s change (shares, debt, reserves, fees)

## Custody patterns to capture (evidence-driven)
- **Pull-in**: `transferFrom(user, protocol, amount)` or native `msg.value`.
- **Push-out**: `transfer(protocol, user, amount)` or native send.
- **Third-party move**: protocol calls an external system that moves tokens (DEX swap, bridge send, staking deposit).
- **Approval-based**: protocol sets allowance then external pulls tokens later.
- **User-approval latent custody**: users approve spenders/routers; value can move from user wallets if the spender can be turned into an attacker-chosen transfer proxy (see `references/approval-surface-mapping.md`).
- **Non-standard token behavior**: fee-on-transfer, rebasing, returns-false, hooks/callbacks.

## Custody-driven exploit primitive generator (no labels)
When you have the custody map, ask per entrypoint:
- Can a user make the protocol **credit a ledger** without the corresponding **custody increase**?
- Can a user make the protocol **release custody** without the corresponding **ledger debit**?
- Can a user force the protocol to **measure balance** at a manipulable holder (temporary balance, flash mint, callback window)?
- Can a user route through a path where **the protocol assumes standard ERC20 behavior** but the token violates it?

Output each “yes/maybe” as:
`capability + broken assumption + on-chain preconditions + measurable delta` (see `exploit-primitives.md`).

