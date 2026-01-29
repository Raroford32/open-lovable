# Approval Surface Mapping (user approvals as latent custody)

Goal: capture a major real‑world surface that often looks “outside the protocol” but is still on‑chain and permissionless:
> user wallets grant approvals to spender contracts, and an attacker finds a route that turns those approvals into unauthorized custody movement.

This is not “about approvals” as a category. It is about a specific capability:
- **A normal user can cause an approved spender to move tokens in a way not bound to explicit user intent.**

## Output (required artifact)
Create `codegraph/layers/L20_approval_surface.md` containing:
- an **Approval Surface Map** (which spenders users approve, and how approvals are consumed)
- routes that can convert approvals into attacker‑chosen transfers
- smallest falsifier stubs for top surfaces

## What to model (evidence-driven)
Include all that exist:
- Any contract that users are instructed to approve (routers, vaults, executors, legacy contracts).
- Any code path that results in `transferFrom(owner, …)` where `owner` is *not* strictly bound to `msg.sender`.
- Any “executor” abstraction where caller chooses:
  - a target contract and calldata, and
  - the system performs that call while holding approvals or being the approved spender.
- Legacy/deprecated contracts still callable or still approved by users.

## Minimal schema hooks (declare only if needed)
If approval surfaces are important, model them explicitly:
- Node types (examples): `APPROVAL`, `SPENDER`, `OWNER_SET`
- Edge types (examples):
  - `APPROVES (OWNER -> SPENDER)` with `asset=TOKEN` and `amountPolicy=exact|unbounded`
  - `CONSUMES_APPROVAL (FUNC -> APPROVAL)` (or `CALLS_TRANSFER_FROM`)
  - `OWNER_SOURCE (FUNC -> VAR/INPUT)` (where does `owner` come from?)

If using different names, add a label map in `codegraph/00_schema.md`.

## Procedure

### 1) Enumerate spender surfaces
From SSOT evidence:
- Identify contracts that are approved by users (docs, UI, or code patterns like “approve this router”).
- Identify contracts that themselves set approvals to other systems (approval chains).

Record spenders and their role:
- router, vault, module, executor, legacy

### 2) Enumerate “approval consumption” sites
Find all places where token movement can be triggered using approvals:
- direct `transferFrom`
- external calls to other spenders that pull tokens using approvals
- delegated execution that can call `transferFrom` on arbitrary tokens

For each site, record:
- who is the `spender` in ERC20 terms (which contract is actually calling `transferFrom`)
- how `owner` is determined (must be bound to `msg.sender`, or it is attacker-influenceable)

### 3) Identify attacker-chosen transfer routes
Ask per spender:
- Can a normal user make the spender call `transferFrom(victim, attacker, amount)`?

High-signal triggers:
- caller supplies a target + calldata and the spender executes it
- batching / multicall / execute() routers that do not constrain targets and calldata
- “executor” parameters that accept arbitrary contracts

### 4) Define invariants (capability states, not labels)
Examples (adapt to code):
- “A spender can only transfer tokens from `msg.sender` (or from an explicitly signed authorization), not from arbitrary owners.”
- “Arbitrary external execution must never run under a context that holds approvals enabling third-party transfers.”

### 5) Smallest falsifiers (E1/E2)
E1 checks:
- enumerate which spenders are approved on fork (spot check known holders or protocol UI defaults)
- confirm that approval consumption sites are reachable via permissionless entrypoints

E2 falsifier idea (generic):
- create an attacker contract that calls the permissionless entrypoint with an executor/target/call sequence intended to invoke `transferFrom(victim, attacker, amount)`
- measure whether any transfer succeeds without explicit victim intent

## Self-evaluation gate
You are not done if:
- any user-facing router/executor exists and you have not modeled whether it can be turned into a general transfer proxy, or
- any legacy contract remains approved by users and still has callable value-movement logic.

