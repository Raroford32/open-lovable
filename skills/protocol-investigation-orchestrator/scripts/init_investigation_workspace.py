#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path


def _write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a protocol investigation workspace (codegraph SSOT + layers + ledgers)."
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Workspace root (default: current directory). Files are created only if missing.",
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()
    codegraph_dir = root / "codegraph"
    layers_dir = codegraph_dir / "layers"
    diagrams_dir = codegraph_dir / "diagrams"

    created: list[Path] = []

    created += [p for p in [codegraph_dir, layers_dir, diagrams_dir] if not p.exists()]
    codegraph_dir.mkdir(parents=True, exist_ok=True)
    layers_dir.mkdir(parents=True, exist_ok=True)
    diagrams_dir.mkdir(parents=True, exist_ok=True)

    ssot_files: dict[Path, str] = {
        codegraph_dir / "00_schema.md": (
            "# Codegraph Schema (SSOT)\n\n"
            "## Node Types\n\n"
            "- \n\n"
            "## Edge Types\n\n"
            "- \n\n"
            "## Label Map (optional)\n\n"
            "- CANONICAL -> ACTUAL\n"
        ),
        codegraph_dir / "01_nodes.md": "# Codegraph Nodes (SSOT)\n\n- \n",
        codegraph_dir / "02_edges.md": "# Codegraph Edges (SSOT)\n\n- EDGE_TYPE | SRC -> DST | attrs...\n",
    }

    for path, content in ssot_files.items():
        if _write_if_missing(path, content):
            created.append(path)

    layer_files: dict[str, str] = {
        "L1_repo.md": "# L1 — Repository Inventory\n",
        "L2_catalog.md": "# L2 — Module Catalog\n",
        "L3_types.md": "# L3 — Type System\n",
        "L4_inheritance.md": "# L4 — Inheritance + Overrides\n",
        "L5_external_surface.md": "# L5 — External Surface\n",
        "L6_deployment_topology.md": "# L6 — Deployment + Topology\n",
        "L7_authority.md": "# L7 — Authority\n",
        "L8_storage.md": "# L8 — Storage\n",
        "L9_function_semantics.md": "# L9 — Function Semantics\n",
        "L10_call_graph.md": "# L10 — Call Graph\n",
        "L11_value_accounting.md": "# L11 — Value + Accounting\n",
        "L12_external_systems.md": "# L12 — External Systems + Trust Assumptions\n",
        "L13_state_machine.md": "# L13 — State Machine\n",
        "L14_invariants.md": "# L14 — Invariants\n",
        "L15_attack_surface.md": "# L15 — Attack Surface (permissionless)\n",
        "L16_primitives.md": "# L16 — Exploit Primitives (capability-first)\n",
        "L17_falsifiers.md": "# L17 — Falsifiers + Proofs\n",
        "L18_learnings.md": "# L18 — Learnings + Mutation\n",
        "L19_control_plane.md": "# L19 — Control Plane Objective Map\n",
        "L20_approval_surface.md": "# L20 — Approval Surface Objective Map\n",
        "L21_ordering_model.md": "# L21 — Ordering Model\n",
        "L22_cycle_mining.md": "# L22 — Cycle Mining\n",
    }

    for filename, header in layer_files.items():
        if _write_if_missing(layers_dir / filename, header):
            created.append(layers_dir / filename)

    ledgers: dict[Path, str] = {
        root / "hypothesis_ledger.md": (
            "# Hypothesis Ledger\n\n"
            "| scenarioId | targetStateX | targetAssetsAndCustody | permissionlessPreconditions | routeSketch | evidencePointers | falsifier | status | measurableDelta | exitMeasurement | costAndCapital | capitalMinimizationPlan | whatKilledIt | newLeverLearned | nextMutation |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
        ),
        root / "unknowns.md": "# Unknowns Ledger\n\n- \n",
        root / "resume_pack.md": (
            "# Resume Pack\n\n"
            "## Fork Metadata\n\n"
            "- chain:\n"
            "- chainId:\n"
            "- RPC provider:\n"
            "- DEV_FORK_BLOCK:\n"
            "- PROMOTION_FORK_BLOCK:\n\n"
            "## Portfolio Snapshot\n\n"
            "- target states X:\n"
            "- live hypotheses (3 per X):\n\n"
            "## Last 3 Falsifier Results\n\n"
            "- \n\n"
            "## Next 3 Mutations (specific)\n\n"
            "- \n\n"
            "## Missing Hard Requirements (if any)\n\n"
            "- \n"
        ),
        root / "deployment_snapshot.md": "# Deployment Snapshot\n\n- \n",
    }

    for path, content in ledgers.items():
        if _write_if_missing(path, content):
            created.append(path)

    if not created:
        print("No changes (all scaffold files already exist).")
        return

    print("Scaffold created:")
    for path in created:
        try:
            rel = path.relative_to(root)
            print(f"- {rel}")
        except ValueError:
            print(f"- {path}")


if __name__ == "__main__":
    main()

