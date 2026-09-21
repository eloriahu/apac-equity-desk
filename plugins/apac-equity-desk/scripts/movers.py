"""Flag material movers using the desk's multi-signal trigger."""

from __future__ import annotations

from typing import Any

from common import flag, load_data, number, parser, records, write_output
from relative_moves import calculate_relative_moves


def find_movers(rows: list[dict[str, Any]], min_signals: int = 2) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in calculate_relative_moves(rows):
        move = number(row.get("pct_change"))
        relative = number(row.get("relative_to_peer_ppt"))
        volume_ratio = number(row.get("volume_ratio"))
        if volume_ratio is None and number(row.get("volume")) is not None and number(row.get("avg_volume_20d")) not in (None, 0):
            volume_ratio = number(row.get("volume")) / number(row.get("avg_volume_20d"))
        contribution = number(row.get("index_contribution_ppt"))
        signals: list[str] = []
        if move is not None and abs(move) > 3: signals.append("absolute_move")
        if relative is not None and abs(relative) > 2: signals.append("sector_relative_move")
        if volume_ratio is not None and volume_ratio > 1.8: signals.append("abnormal_volume")
        if contribution is not None and abs(contribution) >= 0.05: signals.append("index_contribution")
        for field, label in (("fresh_announcement", "fresh_announcement"), ("commodity_shock", "commodity_move"),
                             ("estimate_revision", "estimate_revision"), ("policy_headline", "policy_headline"),
                             ("unusual_flow", "unusual_flow")):
            if flag(row.get(field)): signals.append(label)
        if number(row.get("ah_divergence_pct")) is not None and abs(number(row.get("ah_divergence_pct"))) > 2:
            signals.append("ah_divergence")
        if len(signals) >= min_signals:
            item = dict(row)
            item.update({"volume_ratio": volume_ratio, "signals": signals, "signal_count": len(signals)})
            output.append(item)
    return sorted(output, key=lambda row: (row["signal_count"], abs(number(row.get("pct_change")) or 0)), reverse=True)


if __name__ == "__main__":
    cli = parser(__doc__)
    cli.add_argument("--min-signals", type=int, default=2)
    args = cli.parse_args()
    write_output(find_movers(records(load_data(args.input)), args.min_signals), args.output)

