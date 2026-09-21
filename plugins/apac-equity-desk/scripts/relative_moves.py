"""Calculate stock moves relative to sector peers and benchmarks.

The peer median excludes the stock itself (leave-one-out). Including it pulls the
median toward the stock and understates the relative move, badly so in small
baskets. A stock with no priced peers gets a null peer median, not a zero spread.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from common import load_data, median, number, parser, records, row_pct_change, write_output


def calculate_relative_moves(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    changes = [row_pct_change(row) for row in rows]
    groups: dict[tuple[str, str], list[int]] = defaultdict(list)
    for index, (row, change) in enumerate(zip(rows, changes)):
        if change is not None:
            groups[(str(row.get("market", "")), str(row.get("sector", "")))].append(index)
    result: list[dict[str, Any]] = []
    for index, (row, change) in enumerate(zip(rows, changes)):
        item = dict(row)
        peer = number(row.get("peer_median_pct"))
        peer_count = None
        if peer is None:
            members = groups[(str(row.get("market", "")), str(row.get("sector", "")))]
            peers = [changes[other] for other in members if other != index]
            peer, peer_count = median(peers), len(peers)
        benchmark = number(row.get("benchmark_pct"))
        item.update({
            "pct_change": change,
            "peer_median_pct": peer,
            "peer_count": peer_count,
            "relative_to_peer_ppt": change - peer if change is not None and peer is not None else None,
            "benchmark_pct": benchmark,
            "relative_to_benchmark_ppt": change - benchmark if change is not None and benchmark is not None else None,
        })
        result.append(item)
    return result


if __name__ == "__main__":
    args = parser(__doc__).parse_args()
    write_output(calculate_relative_moves(records(load_data(args.input))), args.output)
