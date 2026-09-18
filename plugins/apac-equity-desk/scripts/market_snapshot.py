"""Calculate normalized quote metrics and market summaries."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from common import iso_now, load_data, median, number, parser, percent_change, records, write_output


def build_snapshot(rows: list[dict[str, Any]], as_of: str | None = None) -> dict[str, Any]:
    enriched: list[dict[str, Any]] = []
    by_market: dict[str, list[dict[str, Any]]] = defaultdict(list)
    gaps: list[str] = []
    for source in rows:
        row = dict(source)
        symbol = str(row.get("symbol", "unknown"))
        pct = percent_change(row.get("last", row.get("close")), row.get("prev_close"))
        row["pct_change"] = pct
        row["volume_ratio"] = (
            number(row.get("volume")) / number(row.get("avg_volume_20d"))
            if number(row.get("volume")) is not None and number(row.get("avg_volume_20d")) not in (None, 0)
            else None
        )
        row["turnover_ratio"] = (
            number(row.get("turnover")) / number(row.get("avg_turnover_20d"))
            if number(row.get("turnover")) is not None and number(row.get("avg_turnover_20d")) not in (None, 0)
            else None
        )
        high, low, previous = number(row.get("high")), number(row.get("low")), number(row.get("prev_close"))
        row["intraday_range_pct"] = ((high - low) / previous * 100) if None not in (high, low, previous) and previous else None
        row["vs_vwap_pct"] = percent_change(row.get("last", row.get("close")), row.get("vwap"))
        weight = number(row.get("index_weight"))
        row["index_contribution_ppt"] = pct * weight / 100 if pct is not None and weight is not None else None
        missing = [field for field in ("market", "last", "prev_close") if row.get(field) in (None, "")]
        if missing:
            gaps.append(f"{symbol}: missing {', '.join(missing)}")
        enriched.append(row)
        by_market[str(row.get("market", "UNKNOWN"))].append(row)

    summaries: dict[str, Any] = {}
    for market, market_rows in sorted(by_market.items()):
        changes = [row["pct_change"] for row in market_rows if row["pct_change"] is not None]
        summaries[market] = {
            "securities": len(market_rows),
            "median_pct_change": median(changes),
            "advancers": sum(value > 0 for value in changes),
            "decliners": sum(value < 0 for value in changes),
            "unchanged": sum(value == 0 for value in changes),
            "total_turnover": sum(number(row.get("turnover")) or 0 for row in market_rows),
        }
    return {"as_of": as_of or iso_now(), "markets": summaries, "rows": enriched, "data_gaps": gaps}


if __name__ == "__main__":
    cli = parser(__doc__)
    cli.add_argument("--as-of")
    args = cli.parse_args()
    write_output(build_snapshot(records(load_data(args.input)), args.as_of), args.output)

