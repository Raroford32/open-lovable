---
name: capability-first-reporting
description: "Produce safe, capability-first, evidence-linked investigation reports and resume packs: tie a target bad state X to measurable deltas, SSOT node/edge chains, and a minimal Foundry falsifier; avoid operational drain guidance. Use when writing a final report, handing off to another session, or checkpointing after hypotheses are proved/disproved/blocked."
---

# Capability-First Reporting

## Report Output (safe + evidence-linked)
Produce:
- a capability statement (“a normal user can force target state X”)
- permissionless preconditions (explicit)
- measurable delta (custody↓ / attacker claim↑ / attacker debt↓) under stated exit constraints
- minimal reproduction (Foundry test name + file path)
- SSOT evidence pointers (node/edge chains)
- root cause explanation (why invariant is falsified)
- fix sketch + regression test suggestion

Avoid:
- step-by-step operational exploitation playbooks
- publishing secrets (RPC/API keys)

## Resume Pack (when stopping without promotion)
Write `resume_pack.md` containing:
- fork metadata used
- current portfolio (targets + 3 hypotheses each)
- last 3 falsifier results
- next 3 mutations (specific)
- missing hard requirements (only if truly blocking)

## References (load only as needed)
- `/root/.codex/skills/layered-codegraph-creator/references/anti-bias-prompts.md`
