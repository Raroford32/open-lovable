# Intent Mining (turn explicit intent into invariants)

Goal: extract intended behavior from docs/tests/configs and convert it into falsifiable invariants and targets without labels.

## Non-negotiable rules
- Treat intent as a hypothesis, not truth.
- Anchor every intent to assets/custody and measurable deltas.
- If enforcement cannot be found, treat it as a target state X.

## Inputs
- README/spec docs, comments, design notes
- Test assertions and revert messages
- Deployment/config scripts, monitoring scripts, runbooks

## Required artifact (in target protocol workspace)
- `intent_ledger.md`

### Intent ledger fields
- Intent statement (plain language)
- Evidence pointer (file/line or URL)
- Enforcement location (function/variable or "missing")
- Measurement point (custody/ledger variable used to verify)
- Status (enforced / partial / missing)
- Candidate invariant + target state X

## Procedure
1) Collect explicit intent statements
- Pull from docs and tests; capture exact phrasing.
- Include constraints like caps, rate bounds, or “must never” statements.

2) Locate enforcement in code
- Trace which functions check or enforce the intent.
- If enforcement is partial, record the gap precisely (which precondition or state update is missing).

3) Convert each intent into an invariant
- Write a computable statement tied to concrete variables/assets.
- Add `INVOLVES` and `MAINTAINS` links in L14.

4) Promote gaps into targets
- For any missing/partial enforcement, write a target state X.
- Seed scenario synthesis with that target.

5) Reconcile with on-chain reality
- If deployed behavior differs from intent, record it as an invariant risk and test it on fork.

## Output discipline
- Keep intent statements capability-first (no vulnerability labels).
- Tie every intent to evidence pointers and measurable deltas.
