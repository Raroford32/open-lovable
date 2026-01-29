---
name: approval-surface-mapper
description: "Map and attack-model user approvals/allowances as latent custody: enumerate spender/router/vault/executor surfaces, how approvals are consumed, and whether an unprivileged caller can turn approvals into attacker-chosen token movement. Use when building `codegraph/layers/L20_approval_surface.md`, auditing routers/executors, or investigating “approval drain” routes without relying on generic vulnerability taxonomies."
---

# Approval Surface Mapper

## Output (L20 approval surface objective map)
In `codegraph/layers/L20_approval_surface.md`, record:
- every spender the system asks users to approve (current + legacy)
- how the spender is invoked (entrypoints, forwarding/executor patterns, calldata control)
- whether the caller can influence:
  - token address
  - `from` address / owner selection
  - destination
  - amount
  - arbitrary external call targets
- smallest falsifier attempt per top spender surface (can/cannot/unknown)

## Procedure
1) Enumerate spender surfaces
   - routers, vaults, executors, forwarders, adapters, “legacy” contracts.
2) Trace approval consumption sites
   - `transferFrom` callsites and any delegated call mechanism.
3) Identify attacker-chosen movement routes
   - unrestricted external call sites
   - executor abstractions with caller-chosen target/calldata
4) Write a falsifier plan
   - prove whether approvals can be converted into unauthorized movement (permissionless).

## References (load only as needed)
- `/root/.codex/skills/layered-codegraph-creator/references/approval-surface-mapping.md`

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
