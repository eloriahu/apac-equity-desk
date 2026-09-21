"""Compare two evidence packs and report additions, removals and material changes."""

from __future__ import annotations

import argparse
from typing import Any

from common import load_data, number, write_output


def _walk(before: Any, after: Any, path: str, threshold: float, changes: list[dict[str, Any]]) -> None:
    if isinstance(before, dict) and isinstance(after, dict):
        for key in sorted(before.keys() | after.keys()):
            child = f"{path}.{key}" if path else key
            if key not in before:
                changes.append({"kind": "added", "path": child, "after": after[key]})
            elif key not in after:
                changes.append({"kind": "removed", "path": child, "before": before[key]})
            else:
                _walk(before[key], after[key], child, threshold, changes)
        return
    if isinstance(before, list) and isinstance(after, list):
        before_by_id = _keyed(before)
        after_by_id = _keyed(after)
        if before_by_id is not None and after_by_id is not None:
            _walk(before_by_id, after_by_id, path, threshold, changes)
        elif before != after:
            changes.append({"kind": "changed", "path": path, "before": before, "after": after})
        return
    if before == after:
        return
    before_n, after_n = number(before), number(after)
    if before_n is not None and after_n is not None:
        delta = after_n - before_n
        if abs(delta) < threshold:
            return
        changes.append({"kind": "changed", "path": path, "before": before, "after": after, "delta": round(delta, 8)})
    else:
        changes.append({"kind": "changed", "path": path, "before": before, "after": after})


def _keyed(values: list[Any]) -> dict[str, Any] | None:
    if not values or not all(isinstance(value, dict) for value in values):
        return None
    for candidate in ("id", "symbol", "name", "market"):
        if all(candidate in value for value in values):
            keys = [str(value[candidate]) for value in values]
            if len(keys) == len(set(keys)):
                return {key: value for key, value in zip(keys, values)}
    return None


def compare_packs(before: dict[str, Any], after: dict[str, Any], threshold: float = 0.0) -> dict[str, Any]:
    if not isinstance(before, dict) or not isinstance(after, dict):
        raise ValueError("Both packs must be JSON objects.")
    changes: list[dict[str, Any]] = []
    _walk(before, after, "", max(threshold, 0.0), changes)
    counts = {kind: sum(change["kind"] == kind for change in changes) for kind in ("added", "removed", "changed")}
    return {
        "schema_version": 1,
        "before_as_of": before.get("as_of"),
        "after_as_of": after.get("as_of"),
        "material_threshold": threshold,
        "counts": counts,
        "changes": changes,
    }


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("before")
    cli.add_argument("after")
    cli.add_argument("--threshold", type=float, default=0.0)
    cli.add_argument("--output")
    args = cli.parse_args()
    write_output(compare_packs(load_data(args.before), load_data(args.after), args.threshold), args.output)
