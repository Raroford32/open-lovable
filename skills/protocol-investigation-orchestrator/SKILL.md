---
name: protocol-investigation-orchestrator
description: End-to-end, self-evolving orchestration for investigating smart-contract protocols for permissionless, economically meaningful vulnerabilities using a layered SSOT codegraph, invariant negations, compositional scenario synthesis, and Foundry fork/sim falsifiers with latest-fork promotion. Use when the user asks to “investigate a protocol”, “find an exploit/vuln”, “do a deep audit”, “build SSOT + invariants + falsifiers”, or wants the agent to autonomously iterate hypotheses until stop conditions.
---

# Protocol Investigation Orchestrator

## Operating Contract (autonomy + rigor)
- Treat “prove safe / nothing found” as invalid. Drive toward an E3-promoted falsifier or an exhaustion checkpoint under explicit stop conditions.
- Do not ask the user what to do next after each step. Instead, decide the next highest-signal action from the evidence ladder + portfolio control (only ask for missing hard requirements: repo, deployed topology, RPC).
- Keep progress measurable: every iteration must produce an evidence upgrade, a model expansion, or a portfolio mutation.
- Keep outputs safe: prove invariant violation in-test; do not package as an operational draining guide.

## Quick Start (do this immediately)
1) Ensure hard requirements exist:
   - protocol repo + build config
   - deployed topology (addresses) or deploy scripts
   - RPC endpoint
   - Foundry (`forge`, `cast`)
2) Standardize env vars (do not hardcode secrets in code):
   - `RPC_URL`
   - `DEV_FORK_BLOCK`
   - `PROMOTION_FORK_BLOCK`
3) Scaffold investigation artifacts in the target workspace:
   - Run `python3 /root/.codex/skills/protocol-investigation-orchestrator/scripts/init_investigation_workspace.py --path <workspace>`
4) Start Phase 0/0b fork reality immediately (E1 evidence), before deep codegraph work.

## Skill Map (pick focused modules by phase)
Use these skills as “attention lenses” (one phase at a time). Load only what you are executing now.
- Phase 0/0b (fork reality, topology, gating): use `fork-reality-recon`
- Pass protocol reading + intent extraction: use `protocol-reading-intent`
- SSOT + layers build/validation + entrypoint triage: use `ssot-codegraph-builder`
- Value truth (assets/custody/claims/debt + numeric semantics): use `value-custody-mapper`
- Control plane (upgrade/init/roles/governance/delegation): use `control-plane-mapper`
- Approval surfaces (spender/allowance → custody routes): use `approval-surface-mapper`
- Ordering/runtime trust boundaries: use `ordering-runtime-modeler`
- Invariants + target states X: use `invariant-miner`
- Scenario synthesis (fusion/cross-module/cycles/operators): use `scenario-synthesizer`
- Foundry falsifiers + promotion gate: use `foundry-falsifier-builder`
- Report/resume packs (safe, evidence-linked): use `capability-first-reporting`

## Orchestration Loop (repeat until stop conditions)
1) **Select targets X**: keep 3–7 invariant negations alive at a time (diverse).
2) **Keep 3 hypotheses per X** (mandatory diversity):
   - H1 warm-up (short chain)
   - H2 fusion (state shaping + extraction from different routes)
   - H3 cross-module / external boundary
3) **Before writing heavy tests**, do E1 checks cheaply (fork reads / `cast`) to confirm the route is live (not paused/capped/oracle-dead).
4) **Write the smallest falsifier** that could disprove the hypothesis (E2), measure deltas explicitly, then mutate.
5) **Promotion gate**: rerun any E2 success on the latest fork (`PROMOTION_FORK_BLOCK`) with gating checks re-verified (E3 only if it still holds).
6) **Stall escalation rule**: if ~5 iterations produce no evidence upgrade and no new SSOT semantics, force escalation:
   - switch to a different target X,
   - do operator mining,
   - expand topology/deployment snapshot,
   - or force a new surface (control-plane / approvals / ordering / cycles / runtime-TCB).

## Canonical References (load only when needed)
Use these as the source-of-truth playbooks for the deep details:
- `/root/.codex/skills/layered-codegraph-creator/references/investigation-os.md`
- `/root/.codex/skills/layered-codegraph-creator/references/layered-codegraph-manual.md`
- `/root/.codex/skills/layered-codegraph-creator/references/falsifier-harness.md`
- `/root/.codex/skills/layered-codegraph-creator/references/anti-bias-prompts.md`

## Output Discipline (what “done” looks like)
- Maintain: `deployment_snapshot.md`, `codegraph/` SSOT + layers, `hypothesis_ledger.md`, `unknowns.md`, Foundry tests, and a reproducibility record (fork blocks + gating checks).
- Stop only when:
  - an E3 scenario exists, or
  - the investigation is exhausted under explicit completeness + self-evaluation gates (and you emit a resume pack with the next mutation plan).
