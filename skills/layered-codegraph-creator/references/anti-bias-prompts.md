# Anti-bias Prompts (prevent premature narrowing)

Goal: keep the investigation in an “open world” posture long enough to find novel, compositional routes.

Use this document whenever reasoning starts to:
- jump to a known vulnerability name
- assume audited patterns are safe
- over-focus on a single subsystem before SSOT coverage exists
- conclude safety without a falsifier

## Core rules
- Replace any label/category thinking with a capability statement.
- Prefer evidence chains over intuition.
- Keep an explicit ledger of unknowns and close it systematically.

## Label-to-capability rewrite (mandatory)
If the mind produces a label, immediately rewrite as:
- “A normal user can force the system to accept reference value V that violates bound B under preconditions P, leading to measurable delta D.”

If a rewrite cannot be produced, treat the label as unsupported speculation and return to SSOT evidence.

## Coverage forcing prompts (run at each layer gate)
Use these prompts before moving past a layer:
- “Does every public/external entrypoint exist as a node and appear in L5 and L15?”
- “Is every external call site represented as an edge?”
- “Is every authority gate represented (including inline checks)?”
- “Is every storage var and every manual storage access represented?”
- “For value-bearing vars, are units and rounding surfaces annotated?”
- “For each critical var, does at least one invariant exist, and does at least one falsifier attempt exist?”

If any answer is “no,” treat it as a hard stop and return to the SSOT.

## Unknowns ledger (keep it explicit)
Maintain a running list of unknowns during reading:
- unclear semantics
- missing edges
- unclear custody location
- unclear unit/scale
- unclear phase reachability
- unclear authority root

Each unknown must be converted into either:
- a new SSOT node/edge and an updated layer entry, or
- a falsifier observation that resolves it

Do not allow unknowns to persist silently.

## Scenario anti-bias prompts (use during synthesis)
When stuck or over-focused:
- “Choose a different invariant target state X and restart from its dependency cone.”
- “Pick a different permissionless entrypoint and search for a path into invariant-relevant writes.”
- “If reasoning is single-module, force a cross-module route (find a shared var or shared external system).”
- “If reasoning is single-tx, consider a multi-tx state-shaping setup (document ordering/MEV risk).”
- “If assumptions are about token behavior or oracle behavior, verify whether that behavior exists on live chain or can be modeled in-test.”

## Stop conditions (do not stop early)
Do not stop because:
- “it looks standard”
- “it’s been audited”
- “no obvious vuln patterns”

Stop only when:
- SSOT completeness gates are closed
- invariants exist for each critical variable
- top-ranked invariants have falsifier attempts
- learnings/mutations are recorded for disproved hypotheses

## Self-evaluation checkpoint (ensure enough work happened)
Use this checkpoint whenever reasoning feels “done” but evidence is thin.

Run this as a written audit log:
- List what is proven vs assumed:
  - proven: backed by SSOT edges and a falsifier observation
  - assumed: not yet tested or not yet modeled
- Count (at least qualitatively) the investigation surface covered:
  - how many entrypoints have at least one hypothesis card
  - how many invariants have at least one falsifier attempt
  - how many external dependencies have at least one influence/bypass attempt (if influence is permissionless)
  - how many custody locations are modeled for value-bearing assets
- If “assumed” dominates “proven,” treat it as simplification and return to falsifiers.

## Brainstorm trigger (when stuck or over-focused)
When scenario generation stops producing new candidates:
- Switch targets: pick a different invariant negation (target state X).
- Switch starting points: pick a different permissionless entrypoint.
- Force diversity: run the divergent brainstorm pass in `references/scenario-synthesis.md`.

## Anti-simplification rule (mandatory)
Do not conclude “safe” from absence of known patterns.
Conclude “no current scenario found” only after:
- SSOT completeness gates are closed
- a meaningful set of falsifiers were attempted and logged
- learnings were used to mutate and retry hypotheses

## Anti-safety-proof rule (mandatory)
Do not set “prove safe / no issue exists” as a goal.

When tempted to write a safe conclusion:
- Rewrite as: “no promoted scenario yet” + “what evidence exists (E0/E1/E2)” + “next 3 mutations.”
- If next mutations cannot be produced, treat it as premature convergence and restart from invariant negations + the dependency cone.

## Creativity checkpoint (mandatory)
If the work starts repeating “simple primary” hypotheses:
- Check the last 5 hypotheses.
- If they are mostly single-step or single-module, force a creativity escalation:
  - run a divergent brainstorm pass (forced diversity dimensions)
  - add one more independent lever (state shaping + settlement)
  - perform at least one fusion attempt

Do not confuse repetition with coverage.
