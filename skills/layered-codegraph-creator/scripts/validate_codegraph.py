#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


_BULLET_RE = re.compile(r"^\s*-\s+")


@dataclass(frozen=True)
class Edge:
    edge_type: str
    src: str
    dst: str
    raw: str
    line_no: int


def _read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        raise SystemExit(f"missing file: {path}")


def parse_schema(schema_path: Path) -> tuple[set[str], set[str]]:
    node_types: set[str] = set()
    edge_types: set[str] = set()
    section: str | None = None
    for line in _read_lines(schema_path):
        stripped = line.strip()
        if stripped == "## Node Types":
            section = "nodes"
            continue
        if stripped == "## Edge Types":
            section = "edges"
            continue
        if not _BULLET_RE.match(line):
            continue
        label = _BULLET_RE.sub("", line).strip()
        if not label:
            continue
        if section == "nodes":
            node_types.add(label)
        elif section == "edges":
            edge_types.add(label)
    return node_types, edge_types


def parse_nodes(nodes_path: Path) -> dict[str, str]:
    nodes: dict[str, str] = {}
    for line_no, line in enumerate(_read_lines(nodes_path), start=1):
        if not _BULLET_RE.match(line):
            continue
        token = _BULLET_RE.sub("", line).strip()
        if not token or token.startswith(("http://", "https://")):
            continue
        if ":" not in token:
            continue
        node_type, _ = token.split(":", 1)
        nodes[token] = node_type
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
        edges.append(Edge(edge_type=edge_type, src=src, dst=dst, raw=line, line_no=line_no))
    return edges


def validate(codegraph_dir: Path) -> int:
    schema_path = codegraph_dir / "00_schema.md"
    nodes_path = codegraph_dir / "01_nodes.md"
    edges_path = codegraph_dir / "02_edges.md"

    node_types, edge_types = parse_schema(schema_path)
    nodes = parse_nodes(nodes_path)
    edges = parse_edges(edges_path)

    errors: list[str] = []

    for node, node_type in sorted(nodes.items()):
        if node_type not in node_types:
            errors.append(f"node type not in schema: {node_type} ({node})")

    for edge in edges:
        if edge.edge_type not in edge_types:
            errors.append(f"{edges_path}:{edge.line_no}: edge type not in schema: {edge.edge_type}")
        if edge.src not in nodes:
            errors.append(f"{edges_path}:{edge.line_no}: missing src node: {edge.src}")
        if edge.dst not in nodes:
            errors.append(f"{edges_path}:{edge.line_no}: missing dst node: {edge.dst}")

    if errors:
        print("codegraph validation: FAIL", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    print("codegraph validation: OK")
    print(f"- nodes: {len(nodes)}")
    print(f"- edges: {len(edges)}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a layered codegraph SSOT (schema/nodes/edges).")
    parser.add_argument("codegraph_dir", nargs="?", default="codegraph", help="Path to codegraph directory.")
    args = parser.parse_args()
    raise SystemExit(validate(Path(args.codegraph_dir)))


if __name__ == "__main__":
    main()

