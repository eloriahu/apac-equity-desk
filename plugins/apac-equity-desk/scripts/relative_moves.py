"""Calculate stock moves relative to sector peers and benchmarks."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from common import load_data, median, number, parser, percent_change, records, write_output


def calculate_relative_moves(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    changes: list[float | None] = []
    groups: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows:
        value = number(row.get("pct_change"))
        value = value if value is not None else percent_change(row.get("last", row.get("close")), row.get("prev_close"))
        changes.append(value)
        if value is not None:
            groups[(str(row.get("market", "")), str(row.get("sector", "")))].append(value)
    result: list[dict[str, Any]] = []
    for row, change in zip(rows, changes):
        item = dict(row)
        peer = number(row.get("peer_median_pct"))
        if peer is None:
            peer = median(groups[(str(row.get("market", "")), str(row.get("sector", "")))])
        benchmark = number(row.get("benchmark_pct"))
        item.update({
            "pct_change": change,
            "peer_median_pct": peer,
            "relative_to_peer_ppt": change - peer if change is not None and peer is not None else None,
            "benchmark_pct": benchmark,
            "relative_to_benchmark_ppt": change - benchmark if change is not None and benchmark is not None else None,
        })
        result.append(item)
    return result


if __name__ == "__main__":
    args = parser(__doc__).parse_args()
    write_output(calculate_relative_moves(records(load_data(args.input))), args.output)

