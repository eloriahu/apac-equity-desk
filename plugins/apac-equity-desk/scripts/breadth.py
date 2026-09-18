"""Calculate APAC market or sector breadth from normalized quote rows."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from common import load_data, number, parser, percent_change, records, write_output


def calculate_breadth(rows: list[dict[str, Any]], group_by: str = "market") -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get(group_by, "UNKNOWN"))].append(row)
    output: dict[str, Any] = {}
    for group, members in sorted(grouped.items()):
        changes = [percent_change(r.get("last", r.get("close")), r.get("prev_close")) for r in members]
        valid_changes = [v for v in changes if v is not None]
        up_volume = sum((number(r.get("volume")) or 0) for r, v in zip(members, changes) if v is not None and v > 0)
        down_volume = sum((number(r.get("volume")) or 0) for r, v in zip(members, changes) if v is not None and v < 0)
        dma_pairs = [(number(r.get("last", r.get("close"))), number(r.get("dma20"))) for r in members]
        dma_pairs = [(last, dma) for last, dma in dma_pairs if last is not None and dma is not None]
        highs = sum(1 for r in members if number(r.get("last", r.get("close"))) is not None and number(r.get("high_52w")) is not None and number(r.get("last", r.get("close"))) >= number(r.get("high_52w")))
        lows = sum(1 for r in members if number(r.get("last", r.get("close"))) is not None and number(r.get("low_52w")) is not None and number(r.get("last", r.get("close"))) <= number(r.get("low_52w")))
        advancers, decliners = sum(v > 0 for v in valid_changes), sum(v < 0 for v in valid_changes)
        output[group] = {
            "universe": len(members), "priced": len(valid_changes), "advancers": advancers,
            "decliners": decliners, "unchanged": sum(v == 0 for v in valid_changes),
            "advance_decline_ratio": advancers / decliners if decliners else None,
            "up_down_volume_ratio": up_volume / down_volume if down_volume else None,
            "pct_above_20dma": sum(last > dma for last, dma in dma_pairs) / len(dma_pairs) * 100 if dma_pairs else None,
            "new_52w_highs": highs, "new_52w_lows": lows,
        }
    return {"group_by": group_by, "groups": output}


if __name__ == "__main__":
    cli = parser(__doc__)
    cli.add_argument("--group-by", default="market", choices=("market", "sector", "industry"))
    args = cli.parse_args()
    write_output(calculate_breadth(records(load_data(args.input)), args.group_by), args.output)

