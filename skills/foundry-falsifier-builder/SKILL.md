---
name: foundry-falsifier-builder
description: "Convert hypotheses into minimal, deterministic Foundry fork/sim falsifiers that measure economic deltas and classify evidence (E0–E3), including latest-fork promotion with live gating checks. Use when writing or iterating `*.t.sol` tests, when verifying hypotheses on a fork, or when promoting an E2 proof to E3 on a near-latest block."
---

# Foundry Falsifier Builder

## Evidence Contract
- E1: verify preconditions/gates on fork (read-only).
- E2: prove/disprove with a Foundry test that produces a measurable delta.
- E3: rerun the same falsifier on a near-latest fork with gating checks re-verified.

Do not treat E0/E1 as “real”. Only E2/E3 can prove or disprove.

## Minimal Falsifier Pattern (recommended)
1) Select fork in-test
   - `vm.createSelectFork(vm.envString(\"RPC_URL\"), vm.envUint(\"DEV_FORK_BLOCK\"))`
2) Do read-only gating checks (in-test is fine)
   - pause/caps/oracle/enable flags relevant to the route
3) Execute the smallest call chain
4) Measure deltas explicitly
   - protocol custody balances
   - attacker balances/claims/debts
   - critical accounting vars
5) Classify result + mutate
   - update `hypothesis_ledger.md` (status + whatKilledIt/newLeverLearned/nextMutation)

## Modeling Aid Rules (do not accidentally fake a vuln)
- `vm.store`, `deal`, and privileged impersonation are exploration aids only; they block promotion.
- If used, immediately plan a mutation replacing the aid with a permissionless acquisition path.

## Promotion Gate (latest fork)
After any E2 success:
1) Switch to `PROMOTION_FORK_BLOCK`.
2) Re-run the same test path with the same measurements.
3) Re-verify live gating checks.
4) Record whether it is promoted (E3), blocked, not reproducible, or unknown.

## References (load only as needed)
- `/root/.codex/skills/layered-codegraph-creator/references/falsifier-harness.md`
- `/root/.codex/skills/layered-codegraph-creator/references/ordering-harness.md`
