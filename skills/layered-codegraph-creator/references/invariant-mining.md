# Invariant Mining (derive targets directly from code)

Goal: produce invariants that are **specific to the protocol’s actual code**, then use them as the primary fuel for scenario synthesis.

In already-audited systems, the highest-yield “unknown” failures are often not a missing check, but a *composed path that violates a latent invariant*.

## Non-negotiable rules
- Derive invariants from code evidence, not from a prefilled vulnerability list.
- Tie each invariant to concrete variables/assets/roles and the functions that maintain them.
- Treat invariants as *attack targets*: always attempt to falsify.

Asset objective rule:
- Do not write invariants in the abstract. Anchor invariants to at least one concrete asset/custody location (real balances) and at least one internal ledger/claim/debt representation.
- If assets/custody are not yet mapped, stop and expand L11 using `references/asset-custody-mapping.md`.

## Inputs
- L7 (authority), L8 (storage), L11 (value/accounting), L12 (trust edges), L13 (state machine)
- SSOT nodes/edges
- `intent_ledger.md` (from `references/intent-mining.md`), if available

## Output
Write invariants into L14 as:
- a single sentence statement (“must never be false”)
- `INVOLVES` links to the relevant vars/assets/roles/custody locations
- `MAINTAINS` links to the functions expected to preserve it
- a “negation form” target state X (used later in scenario synthesis)

## Procedure (evidence-driven)

### 0) Assemble a protocol balance sheet (system-level truth)
Before mining invariants, build a balance sheet grounded in custody↔claims↔debt:
- Use `references/balance-sheet-assembly.md`.
- Output `balance_sheet.md` in the target protocol workspace.

### 1) Identify “truth sources” for the protocol
Build a small set of ground-truth anchors:
- Real custody balances (token `balanceOf`, native balance, cash accessors)
- Internal ledgers (shares, balances, debts, reserves, indices)
- Authority roots (owners/admins/roles/signers)
- Phase variables (pauses/epochs/rounds)

If truth sources are ambiguous (wrappers, strategies, bridges), expand custody modeling first (`references/asset-custody-mapping.md`).

Also enumerate the asset objective map:
- Which assets are the economic objective?
- Where is real custody held?
- Which functions measure that custody (direct `balanceOf`, cash accessors, wrapper conversions)?

This is the anchor for both invariants and later scenarios.

### 2) Extract invariant candidates from code constructs
Use code constructs as generators:

#### Generator A: Preconditions imply invariants
Trigger: any `require`/assert/check.
Action: treat the checked relation as a local invariant and ask:
- “Is this relation expected to hold globally, or only at the start of this function?”
- “Can a later step invalidate it without re-check?”

#### Generator B: Update equations imply conservation/consistency
Trigger: assignments/updates like `total += x`, `balance[user] = f(...)`.
Action: write the implicit relation that the update intends to preserve.
Example forms:
- “sum of per-user balances tracks total supply (within rounding rules).”
- “reserves track real custody (within fee/rounding).”

#### Generator C: Unit conversions imply bounds and drift constraints
Trigger: conversions between units (assets↔shares, debt↔shares, price↔usd).
Action: write invariants about:
- rounding direction and who benefits
- monotonicity of indices
- no-arbitrage between two conversions (if both exist)

Use `references/numeric-semantics.md` to annotate the exact rounding surfaces.

#### Generator D: Authority writes imply authorization invariants
Trigger: any write to admin/role/oracle/router/implementation pointers.
Action: write invariants about who can change what, and when.
Also write invariants about “initialization happens exactly once” when applicable.

Escalation rule:
- Do not treat “auth exists” as sufficient. Map *how* control can change and whether a normal user can reach the write path via ordering/governance/delegation.
- If upgradeability/governance/delegated execution exists, also build L19 using `references/control-plane-mapping.md`.

#### Generator E: State machine transitions imply reachability invariants
Trigger: phase flags/epochs/rounds.
Action: write invariants that relate:
- which operations are enabled in which phase
- which transitions must be irreversible or monotonic
- which checks must hold across phases

#### Generator G: Approval consumption implies owner-binding invariants
Trigger: any value movement that can use approvals (direct `transferFrom`, router pull patterns, executor-based external calls under approvals).
Action: write invariants that bind token movement authority to explicit user intent:
- “token movement using approvals can only source from `msg.sender` (or from an explicit signed authorization), not from arbitrary owners.”
- “a caller cannot cause a system-held spender approval to be applied to attacker-chosen targets/calldata.”

If routers/executors exist, build L20 using `references/approval-surface-mapping.md` and attach falsifier plans early (E1/E2).

#### Generator H: Runtime/precompile acceptance implies backing/authority invariants
Trigger: any mint/credit/withdraw path where correctness depends on runtime/system/precompile validation.
Action: write invariants that bind “acceptance” to accounting:
- “accepted message implies recorded backing for the credited amount”
- “minted claims cannot exceed accounted deposits”

If such dependencies exist, extend L12/L19 using `references/runtime-tcb-mapping.md`.

#### Generator F: Intent vs enforcement mismatches
Trigger: an explicit intent statement from docs/tests or a test assertion.
Action: convert the intent to a computable invariant and identify the enforcement location.
If enforcement is missing or partial, treat the gap as a target state X and seed scenario synthesis.

### 3) Tighten each invariant (make it falsifiable)
For each candidate invariant, add:
- the exact variables/assets/roles involved
- the measurable observable that would disprove it
- the smallest falsifier test idea (even if not written yet)

Avoid vague invariants (“protocol is solvent”). Replace with a computable statement tied to custody/ledger variables.

### 4) Connect invariants to maintainers
For each invariant:
- identify the functions that can change involved vars
- identify the functions that check those vars
- link them using `MAINTAINS` edges (expected maintainers)

This turns invariants into a navigable planning graph for scenario synthesis.

### 5) Convert invariants into scenario targets
Write a “negation form” for each invariant (target bad state X).
Examples (write as states):
- “Ledger credits exceed custody increase.”
- “Debt decreases without repayment custody movement.”
- “A guard is passed under condition C, but C is later invalidated before value movement.”

Then hand these targets to `references/scenario-synthesis.md`.

Before handing off, confirm each target state X includes:
- at least one asset/custody objective
- a measurable delta definition

## Failure mode handling (self-evolving loop)
When an invariant cannot be expressed precisely:
- Treat it as a signal that a missing semantic layer exists.
- Extend SSOT schema only as required (new node/edge types) and re-derive the invariant.
- Prefer adding one new semantic at a time (keep changes auditable).
