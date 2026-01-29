---
name: control-plane-mapper
description: "Map and attack-model the protocol control plane as value-bearing state: upgradeability, initialization, roles/owners/guardians, governance executors, module registries, delegated execution roots, and any publicly reachable paths that change future behavior control. Use when building `codegraph/layers/L19_control_plane.md`, deriving control-plane invariants, or synthesizing “control acquisition → monetization” scenarios."
---

# Control Plane Mapper

## Output (L19 control plane objective map)
In `codegraph/layers/L19_control_plane.md`, record for each control variable:
- current controller (who can change it now)
- every write path (function(s) + guard chain)
- every read site (where behavior depends on it)
- whether a normal user can reach the write path (directly or via governance/delegation/ordering)
- a control-plane objective state (“normal user can make X attacker-controlled”)
- at least one monetization route (control → custody/claim/debt delta)
- at least one falsifier stub

## Procedure
1) Enumerate control-plane state
   - proxy admin/implementation pointers, initializer state
   - roles/owners/guardians, role-grant paths
   - governance executors, proposal execution routes
   - registries/allowlists, module selectors, permission maps
   - delegated execution (forwarders/executors/meta-tx roots)
2) Trace write paths end-to-end
   - include ordering sensitivity and cross-module paths
3) Define invariants + target states X
   - “only controller C can set variable V” is not enough; also bind to custody effects
4) Define the smallest falsifier
   - measure: control variable change + minimal downstream custody/claim/debt delta

## References (load only as needed)
- `/root/.codex/skills/layered-codegraph-creator/references/control-plane-mapping.md`
- `/root/.codex/skills/layered-codegraph-creator/references/runtime-tcb-mapping.md`

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
