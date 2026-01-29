---
name: value-custody-mapper
description: "Map protocol value truth: enumerate assets, custody locations, internal ledgers/claims/debts, measurement readpoints, and numeric semantics (units/scale/rounding). Use when you need an asset objective map, a balance-sheet view, or when turning invariants and scenarios into measurable deltas on fork (custody↓ / attacker claim↑ / attacker debt↓)."
---

# Value Custody Mapper

## Output (asset objective map)
For each protocol-relevant asset, record:
- **asset**: address/symbol/decimals (and wrapper conversion rules)
- **custody locations**: where it sits at rest (protocol contracts, vaults, external systems)
- **measurement readpoints**: how “truth” is measured (`balanceOf`, cash, totalAssets, exchangeRate, etc.)
- **internal ledgers**: shares/claims/debt representations that purport to track that custody
- **exit measurement**: how delta is quoted on fork under realistic exit constraints

## Procedure
1) Enumerate assets (underlyings, shares, reward tokens, debt tokens, LP/wrappers).
2) Build custody map (custody ↔ measurement function ↔ holder address).
3) Map ledgers/claims/debts to custody and identify coupling points.
4) Record numeric semantics:
   - units/scale/decimals
   - rounding direction + loss surfaces
   - time-based accrual or drift surfaces
5) Assemble a “protocol balance sheet” view (system-level targets).

## Why this skill is mandatory
- Without custody/readpoint mapping, “profit” claims are non-evaluable.
- Without numeric semantics, many invariant candidates are wrong by units/rounding/time.

## References (load only as needed)
- `/root/.codex/skills/layered-codegraph-creator/references/asset-custody-mapping.md`
- `/root/.codex/skills/layered-codegraph-creator/references/numeric-semantics.md`
- `/root/.codex/skills/layered-codegraph-creator/references/balance-sheet-assembly.md`

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
