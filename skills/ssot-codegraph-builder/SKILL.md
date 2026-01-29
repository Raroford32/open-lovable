---
name: ssot-codegraph-builder
description: "Create and maintain a layered SSOT codegraph for a smart-contract protocol: derive schema from code/build config, assign stable node IDs, record typed edges, build L1–L14 layers, and validate consistency. Use when generating or updating `codegraph/00_schema.md`, `codegraph/01_nodes.md`, `codegraph/02_edges.md`, `codegraph/layers/*`, or when triaging entrypoints from the SSOT to drive invariant mining and exploit-hypothesis work."
---

# SSOT Codegraph Builder

## SSOT Discipline (non-negotiable)
- Derive schema from code/config (start empty; declare labels before use).
- Give every entity a stable node ID in `codegraph/01_nodes.md`.
- Represent relationships only as typed edges in `codegraph/02_edges.md`.
- Treat `codegraph/layers/*` as views/filters over SSOT (never the SSOT).

## Minimal Workflow
1) Initialize SSOT layout
   - Create `codegraph/00_schema.md` with required headings:
     - `## Node Types`
     - `## Edge Types`
   - Create `codegraph/01_nodes.md` and `codegraph/02_edges.md`.
2) Build L1–L6 (enumeration + deployment reality)
   - Inventory repo, modules, types, external surface, deployment topology.
3) Build L7–L11 (authority + storage + semantics + calls + value/accounting)
4) Build L12–L14 (external systems + state machine + invariants)
5) Validate SSOT consistency early/often
   - Run `python3 /root/.codex/skills/layered-codegraph-creator/scripts/validate_codegraph.py codegraph`
6) Triage permissionless entrypoints from SSOT (once value edges exist)
   - Run `python3 /root/.codex/skills/layered-codegraph-creator/scripts/triage_entrypoints.py codegraph --permissionless-only --limit 50`

## Common Failure Modes (avoid)
- Writing layers without backing SSOT nodes/edges (guaranteed omissions).
- Using generic schemas not forced by the code (breaks SSOT semantics).
- Treating tests/diagrams as truth instead of codegraph SSOT.

## Primary References (load only as needed)
- `/root/.codex/skills/layered-codegraph-creator/references/layered-codegraph-manual.md`
- `/root/.codex/skills/layered-codegraph-creator/references/language-mapping.md`
