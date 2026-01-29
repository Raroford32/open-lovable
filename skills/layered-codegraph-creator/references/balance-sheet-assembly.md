# Protocol Balance Sheet Assembly (custody ↔ claims ↔ debt)

Goal: produce protocol-specific, “system-level” invariants that are hard to see by reading one function at a time.

This procedure builds a balance sheet grounded in:
- real custody locations (what is actually held),
- internal ledgers (what the protocol thinks it holds/owes),
- claims and debts (what users can redeem/borrow),
- and the conversion equations connecting them.

## Non-negotiable rules
- Do not write “solvent” as an invariant. Write computable equations.
- Use explicit units/scales for every quantity (`references/numeric-semantics.md`).
- Separate:
  - **stock variables** (balances, totalSupply, reserves)
  - **flow variables** (fees, interest accrual per block)
  - **conversion variables** (exchange rates, indices)

## Output (in the target protocol workspace)
Create `balance_sheet.md`.

Minimum sections:
- Asset inventory
- Custody map summary (by holder)
- Claim/debt inventory
- Conversion equations
- Balance sheet equations (must-hold relations)
- “How it can break” notes (feeds scenario synthesis)

## Procedure

### 1) Enumerate assets and value-bearing representations
List:
- underlyings (ERC20/native/NFT if value-bearing)
- share/receipt tokens
- reward tokens
- debt representations (debt tokens, account debt vars)

### 2) Build custody totals (assets at rest)
For each asset A:
- list custody locations `H1..Hn` (protocol address, strategy, escrow, pool, bridge, etc.)
- define the measurement function per holder (balanceOf/native/cash accessor)

Write:
`Custody(A) = Σ balanceOf(A, Hi)`

If custody is indirect (wrapper shares), expand:
- `Custody(A) = shares(Hi) * exchangeRate(Hi)` with units.

### 3) Enumerate liabilities/claims/debts
For each user-facing claim/debt representation:
- what variable represents it
- how it is redeemed/settled
- unit and scale

Examples (write in protocol-specific terms):
- `TotalShares(A)`
- `TotalDebt(A)`
- `UserClaim(u,A)`

### 4) Write conversion equations (the glue)
Write the precise formulas the protocol uses:
- assets↔shares conversions
- debt↔index conversions
- fee and reserve updates

For each equation, record:
- where rounding happens
- whether it is cached
- whether it depends on external inputs

### 5) Assemble balance sheet equations
Write the system relations that “must never be false” (with tolerances if rounding):

Examples (must be adapted to the actual protocol):
- `Custody(A) + Receivables(A) >= RedeemableClaims(A)`
- `RecordedDebt(A) <= MaxBorrowable(A)`
- `TotalShares(A) * SharePrice(A) ≈ Custody(A) - Fees(A)`

If the protocol intentionally runs fractional reserves, encode that as an explicit policy variable.

### 6) Derive invariant targets (negations)
For each equation, write a target bad state X:
- “Redeemable claims exceed custody by Δ.”
- “Debt decreases without custody repayment.”
- “Two conversion paths create an arbitrage loop with positive drift.”

Each target must include:
- the target asset/custody
- measurable delta definition

### 7) Feed scenario synthesis
Every balance-sheet equation provides:
- a target state X
- a dependency cone (which vars/funcs/inputs influence it)

Use these to generate multi-step composed routes.

## Self-evaluation gate
You are not done if:
- any top-value asset lacks a custody total equation
- any user-facing claim/debt lacks a conversion equation
- invariants exist but are not tied to these equations

