"""Trace evidence-linked event transmission paths across APAC markets and securities."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from common import load_data, number, write_output


def build_map(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("Transmission input must be an object.")
    nodes = data.get("nodes")
    edges = data.get("edges")
    start = str(data.get("event_node", ""))
    if not isinstance(nodes, list) or not isinstance(edges, list) or not start:
        raise ValueError("nodes, edges and event_node are required.")
    node_map = {str(node.get("id")): node for node in nodes if isinstance(node, dict) and node.get("id")}
    if start not in node_map:
        raise ValueError("event_node must match a node id.")
    graph: dict[str, list[dict[str, Any]]] = defaultdict(list)
    issues = []
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        source, target = str(edge.get("from", "")), str(edge.get("to", ""))
        if source not in node_map or target not in node_map:
            issues.append(f"edge {source}->{target} references a missing node")
            continue
        confidence = number(edge.get("confidence"))
        if confidence is None or not 0.0 <= confidence <= 1.0:
            issues.append(f"edge {source}->{target} requires confidence between 0 and 1")
            continue
        if not str(edge.get("mechanism", "")).strip():
            issues.append(f"edge {source}->{target} has no mechanism")
            continue
        graph[source].append(edge)

    max_depth = int(number(data.get("max_depth")) or 4)
    paths = []
    cycles = []

    def visit(node_id: str, path_nodes: list[str], path_edges: list[dict[str, Any]]) -> None:
        outgoing = graph.get(node_id, [])
        if path_edges and (not outgoing or len(path_edges) >= max_depth):
            confidence = 1.0
            for edge in path_edges:
                confidence *= number(edge.get("confidence")) or 0.0
            paths.append(
                {
                    "nodes": path_nodes,
                    "labels": [node_map[item].get("label", item) for item in path_nodes],
                    "mechanisms": [edge.get("mechanism") for edge in path_edges],
                    "source_ids": sorted({source for edge in path_edges for source in edge.get("source_ids", [])}),
                    "supported": all(bool(edge.get("source_ids")) for edge in path_edges),
                    "confidence_product": round(confidence, 4),
                }
            )
        for edge in outgoing:
            target = str(edge["to"])
            if target in path_nodes:
                cycles.append(path_nodes + [target])
                continue
            if len(path_edges) < max_depth:
                visit(target, path_nodes + [target], path_edges + [edge])

    visit(start, [start], [])
    paths.sort(key=lambda path: (path["supported"], path["confidence_product"], len(path["nodes"])), reverse=True)
    return {"schema_version": 1, "event_node": start, "paths": paths, "cycles": cycles, "issues": issues}


if __name__ == "__main__":
    import argparse

    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("input")
    cli.add_argument("--output")
    args = cli.parse_args()
    write_output(build_map(load_data(args.input)), args.output)
