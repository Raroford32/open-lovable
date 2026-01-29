#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


_BULLET_RE = re.compile(r"^\s*-\s+")


def _csv_set(value: str) -> set[str]:
    items = [v.strip() for v in value.split(",")]
    return {v for v in items if v}


def parse_label_map(schema_path: Path) -> dict[str, str]:
    """Parse an optional label map from `codegraph/00_schema.md`.

    Supported section headers (case-insensitive):
    - "## Label Map"
    - "## Label Mapping"

    Supported bullet formats:
    - `- CANONICAL -> ACTUAL`
    - `- CANONICAL = ACTUAL`
    - `- CANONICAL: ACTUAL`

    If no map exists, return an empty dict.
    """

    try:
        lines = schema_path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return {}

    mapping: dict[str, str] = {}
    in_section = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            header = stripped[3:].strip().lower()
            in_section = header in {"label map", "label mapping", "label-map", "label-mapping"}
            continue

        if not in_section:
            continue

        if not _BULLET_RE.match(line):
            continue

        token = _BULLET_RE.sub("", line).strip()
        if not token:
            continue

        for sep in ("->", "=", ":"):
            if sep not in token:
                continue
            src, dst = [s.strip() for s in token.split(sep, 1)]
            if src and dst:
                mapping[src] = dst
            break

    return mapping


def _node_type(node: str) -> str:
    return node.split(":", 1)[0] if ":" in node else ""


@dataclass(frozen=True)
class Edge:
    edge_type: str
    src: str
    dst: str
    line_no: int


def _read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def parse_nodes(nodes_path: Path) -> set[str]:
    nodes: set[str] = set()
    for line in _read_lines(nodes_path):
        if not _BULLET_RE.match(line):
            continue
        token = _BULLET_RE.sub("", line).strip()
        if not token or ":" not in token:
            continue
        nodes.add(token)
    return nodes


def parse_edges(edges_path: Path) -> list[Edge]:
    edges: list[Edge] = []
    for line_no, line in enumerate(_read_lines(edges_path), start=1):
        if not _BULLET_RE.match(line):
            continue
        token = _BULLET_RE.sub("", line).strip()
        if not token:
            continue
        parts = [p.strip() for p in token.split("|")]
        if len(parts) < 2:
            continue
        edge_type = parts[0]
        link = parts[1]
        if "->" not in link:
            continue
        src, dst = [s.strip() for s in link.split("->", 1)]
        if not src or not dst:
            continue
        edges.append(Edge(edge_type=edge_type, src=src, dst=dst, line_no=line_no))
    return edges


def is_typed(node: str, type_name: str) -> bool:
    return node.startswith(f"{type_name}:")


def triage(
    codegraph_dir: Path,
    limit: int,
    permissionless_only: bool,
    *,
    func_type: str,
    asset_type: str,
    value_edge_types: set[str],
    call_edge_types: set[str],
    reads_edge_type: str,
    writes_edge_type: str,
    role_edge_type: str,
) -> list[str]:
    nodes_path = codegraph_dir / "01_nodes.md"
    edges_path = codegraph_dir / "02_edges.md"

    nodes = parse_nodes(nodes_path)
    edges = parse_edges(edges_path)

    funcs = sorted([n for n in nodes if is_typed(n, func_type)])

    by_func: dict[str, dict[str, object]] = {}
    for func in funcs:
        by_func[func] = {
            "value_edges": 0,
            "call_edges": 0,
            "reads": 0,
            "writes": 0,
            "roles": set(),
            "assets": set(),
        }

    for edge in edges:
        if edge.src not in by_func:
            continue
        stats = by_func[edge.src]
        if edge.edge_type in value_edge_types:
            stats["value_edges"] = int(stats["value_edges"]) + 1
            if is_typed(edge.dst, asset_type):
                stats["assets"].add(edge.dst)
        elif edge.edge_type in call_edge_types:
            stats["call_edges"] = int(stats["call_edges"]) + 1
        elif edge.edge_type == reads_edge_type:
            stats["reads"] = int(stats["reads"]) + 1
        elif edge.edge_type == writes_edge_type:
            stats["writes"] = int(stats["writes"]) + 1
        elif edge.edge_type == role_edge_type:
            stats["roles"].add(edge.dst)

    ranked = []
    for func, stats in by_func.items():
        roles = stats["roles"]
        if permissionless_only and roles:
            continue
        ranked.append(
            (
                int(stats["value_edges"]),
                len(stats["assets"]),
                int(stats["call_edges"]),
                int(stats["writes"]),
                int(stats["reads"]),
                func,
            )
        )

    ranked.sort(reverse=True)

    lines: list[str] = []
    for value_edges, asset_count, call_edges, writes, reads, func in ranked[:limit]:
        stats = by_func[func]
        roles = sorted(stats["roles"])
        assets = sorted(stats["assets"])
        role_str = "none" if not roles else ",".join(roles)
        asset_str = "none" if not assets else ",".join(assets)
        lines.append(
            f"- {func} | value_edges={value_edges} assets={asset_str} calls={call_edges} writes={writes} reads={reads} roles={role_str}"
        )
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Triage codegraph functions by value-touch + privilege signals (SSOT-driven). "
            "Supports an optional label map in codegraph/00_schema.md (## Label Map)."
        )
    )
    parser.add_argument("codegraph_dir", nargs="?", default="codegraph", help="Path to codegraph directory.")
    parser.add_argument("--limit", type=int, default=50, help="Max functions to print.")
    parser.add_argument(
        "--permissionless-only",
        action="store_true",
        help="Only include funcs with no explicit REQUIRES_ROLE edges.",
    )
    parser.add_argument(
        "--no-label-map",
        action="store_true",
        help="Ignore any label map in 00_schema.md (use CLI-provided canonical names).",
    )
    parser.add_argument(
        "--func-type",
        default="FUNC",
        help="Node type prefix for function nodes (default: FUNC).",
    )
    parser.add_argument(
        "--asset-type",
        default="ASSET",
        help="Node type prefix for asset nodes (default: ASSET).",
    )
    parser.add_argument(
        "--value-edges",
        default="TRANSFERS,MINTS,BURNS,COLLECTS_FEE",
        help="Comma-separated edge types to treat as value-touch signals.",
    )
    parser.add_argument(
        "--call-edges",
        default="EXT_CALLS,DELEGATECALLS,STATICCALLS",
        help="Comma-separated edge types to treat as call signals.",
    )
    parser.add_argument(
        "--reads-edge",
        default="READS",
        help="Edge type representing reads (default: READS).",
    )
    parser.add_argument(
        "--writes-edge",
        default="WRITES",
        help="Edge type representing writes (default: WRITES).",
    )
    parser.add_argument(
        "--role-edge",
        default="REQUIRES_ROLE",
        help="Edge type representing explicit privilege requirements (default: REQUIRES_ROLE).",
    )
    args = parser.parse_args()

    codegraph_dir = Path(args.codegraph_dir)
    label_map = {} if args.no_label_map else parse_label_map(codegraph_dir / "00_schema.md")

    def m(label: str) -> str:
        return label_map.get(label, label)

    lines = triage(
        codegraph_dir,
        limit=args.limit,
        permissionless_only=args.permissionless_only,
        func_type=m(args.func_type),
        asset_type=m(args.asset_type),
        value_edge_types={m(t) for t in _csv_set(args.value_edges)},
        call_edge_types={m(t) for t in _csv_set(args.call_edges)},
        reads_edge_type=m(args.reads_edge),
        writes_edge_type=m(args.writes_edge),
        role_edge_type=m(args.role_edge),
    )
    print("# Triage (higher first)")
    if len(lines) == 0:
        print(
            "- (no FUNC nodes found in SSOT; triage requires FUNC nodes + value edges like TRANSFERS/MINTS/BURNS/COLLECTS_FEE)"
        )
    for line in lines:
        print(line)


if __name__ == "__main__":
    main()
