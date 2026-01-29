# Control‑Plane Mapping (who controls future behavior)

Goal: make “future behavior control” a first‑class, evidence‑driven target, so investigations don’t miss routes where an attacker:
- first acquires control over **configuration / upgradeability / execution roots**, then
- monetizes later via normal-looking downstream actions.

This is not a “vulnerability category.” It is a protocol surface where **meaning changes**:
> “the same external call now executes different code,” or  
> “the same entrypoint now has different authorization rules,” or  
> “the same accounting path now reads different dependencies.”

## What counts as control‑plane (include all that exist in code)
- Upgradeability: proxy admin, implementation pointers, beacons, upgrade executors.
- Initialization: initializer flags, `initialize()` reachability, post‑deploy setup transactions.
- Authority roots: `owner`, `admin`, `guardian`, `roles`, allowlists/whitelists, registries.
- Governance executors: proposal execution, timelocks, module managers.
- Delegated execution roots: meta‑tx forwarders, delegated EOAs, “executor” abstractions, module/fuse systems that can call arbitrary targets.
- Runtime trust boundaries: if a precompile/runtime module validates messages that trigger mint/credit, treat that validation path as control‑plane (see `runtime-tcb-mapping.md`).

## Output (required artifact)
Create `codegraph/layers/L19_control_plane.md` containing:
- a **Control‑Plane Objective Map** (what control variables exist, who controls them, and how control can change)
- **control‑plane invariants** (what must never be false)
- **smallest falsifier stubs** (E1/E2 plans)

## Capability framing (required)
Write control‑plane target states as capabilities, e.g.:
- “A normal user can cause a future behavior root (implementation pointer / admin / executor allowlist) to become attacker‑controlled.”
- “A normal user can make the system accept a ‘configured’ state that was never authorized by the intended controller.”

## Minimal schema hooks (declare only if you need them)
If the protocol has complex control‑plane, represent it explicitly:
- Node types (examples): `CONTROL_VAR`, `CONTROL_ROOT`, `ROLE`, `CONFIG_ITEM`, `EXECUTION_ROOT`
- Edge types (examples):
  - `CONTROLS (ADDR/ROLE -> CONTROL_VAR)`
  - `WRITES_CONTROL (FUNC -> CONTROL_VAR)`
  - `AUTHORIZES_CONTROL_WRITE (CHECK/ROLE -> WRITES_CONTROL)`
  - `CHANGES_BEHAVIOR_OF (CONTROL_VAR -> FUNC/MODULE)`
  - `DELEGATES_EXECUTION (ADDR/FUNC -> ADDR/FUNC)` (meta‑tx / delegated EOAs / module systems)

If using different names, add a label map in `codegraph/00_schema.md`.

## Procedure

### 1) Enumerate control variables (from SSOT evidence)
From L5/L7/L8/L10/L12 coverage:
- Find every storage slot/var that:
  - selects an implementation or delegate target
  - stores an admin/owner/role
  - stores allowlists/whitelists/registries
  - stores module/fuse pointers
  - stores “initialized” flags or deployment-time config

Record each as a `CONTROL_VAR` with:
- location (contract + slot/var)
- semantic role (“selects implementation”, “authorizes”, “selects executor”, etc.)
- read sites (which functions depend on it)

### 2) Enumerate all write paths and their guards
For each `CONTROL_VAR`:
- list every function that writes it
- list the guard/check chain that gates each write
- include indirect writes (delegatecall‑based admin systems, module managers)

### 3) Enumerate permissionless acquisition paths
This is the critical “beyond-known” step: do not assume writes are safe because they are “admin-only.”

For each write path, ask:
- Is there a **permissionless** route to satisfy the guard?
  - deployment ordering (init/role assignment races)
  - governance vote capture (temporary voting power concentration)
  - delegated execution roots that allow attacker-chosen external calls
  - module/fuse registration that can be shaped by an unprivileged caller

If uncertain, write the smallest E1 check:
- read guard state on fork (paused flags, role membership, init flags)

### 4) Define control‑plane invariants (computable statements)
Examples (adapt to the protocol):
- “Only the intended controller can change `CONTROL_VAR X`.”
- “`initialize()` can only transition once, and only under intended caller/context.”
- “An execution root cannot be redirected to an attacker-chosen target by an unprivileged caller.”

Tie each invariant to concrete vars and funcs:
- `INVOLVES (INVARIANT -> CONTROL_VAR/FUNC/ROLE)`

### 5) Compose monetization routes (state shaping → extraction)
Control‑plane acquisition is often only Step 1.
For each control‑plane target state X, attach a minimal monetization route:
- “after acquiring control, what is the smallest downstream path that changes custody/claim/debt?”

This keeps hypotheses economic and testable.

### 6) Write smallest falsifiers (E1/E2)
For each control‑plane hypothesis:
- E1: prove on fork that the control var is real and writable via the hypothesized path
- E2: minimal test that changes the control var (without privileged impersonation) and shows a measurable downstream effect

## Self‑evaluation gate
You are not done if any of these exist in code but are not mapped:
- proxy/beacon upgrade controls
- initialization flags / post-deploy configuration steps
- governance executor / timelock pathways
- delegated execution roots / meta‑tx forwarders
- allowlists/whitelists that gate value paths

