"""Rank observable APAC sector moves as research topics without asserting causation.

Input is a JSON object with ``as_of``, ``market``, ``quotes`` and optional
``news``. Quotes use the shared quote-row contract and should include ``sector``.
The output is a deterministic shortlist for an analyst to investigate.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any

from common import load_data, median, number, parse_timestamp, row_pct_change, write_output


def _volume_ratio(row: dict[str, Any]) -> float | None:
    supplied = number(row.get("volume_ratio"))
    if supplied is not None:
        return supplied
    volume = number(row.get("volume"))
    normal = number(row.get("avg_volume_20d"))
    if volume is None or normal in (None, 0):
        return None
    return volume / normal


def _fresh_news(
    news: list[dict[str, Any]], sector: str, symbols: set[str], as_of: datetime, hours: int
) -> list[dict[str, Any]]:
    cutoff = as_of - timedelta(hours=hours)
    result = []
    for item in news:
        if not isinstance(item, dict):
            continue
        published = parse_timestamp(item.get("published_at"))
        if published is None or not cutoff <= published <= as_of:
            continue
        sectors = item.get("sectors", [])
        symbols_value = item.get("symbols", [])
        sectors = [sectors] if isinstance(sectors, str) else sectors
        symbols_value = [symbols_value] if isinstance(symbols_value, str) else symbols_value
        item_sectors = {str(value).strip().lower() for value in sectors}
        item_symbols = {str(value).strip() for value in symbols_value}
        if sector.lower() in item_sectors or symbols.intersection(item_symbols):
            result.append(item)
    return sorted(result, key=lambda item: str(item.get("published_at")), reverse=True)


def rank_topics(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("Topic-radar input must be a JSON object.")
    as_of = parse_timestamp(data.get("as_of"))
    if as_of is None:
        raise ValueError("as_of must be an ISO-8601 timestamp with an offset.")
    market = str(data.get("market", "")).strip()
    if not market:
        raise ValueError("market is required.")
    quotes = data.get("quotes")
    if not isinstance(quotes, list) or not quotes:
        raise ValueError("quotes must be a non-empty array.")
    news = data.get("news", [])
    if not isinstance(news, list):
        raise ValueError("news must be an array when supplied.")
    benchmark = number(data.get("benchmark_pct")) or 0.0
    max_news_age = max(int(number(data.get("max_news_age_hours")) or 24), 0)

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    ignored = []
    for row in quotes:
        if not isinstance(row, dict):
            continue
        sector = str(row.get("sector", "")).strip()
        change = row_pct_change(row)
        if not sector or change is None:
            ignored.append(str(row.get("symbol") or row.get("name") or "unknown"))
            continue
        normalized = dict(row)
        normalized["_change"] = change
        normalized["_volume_ratio"] = _volume_ratio(row)
        grouped[sector].append(normalized)

    topics = []
    for sector, rows in grouped.items():
        moves = [row["_change"] for row in rows]
        sector_move = median(moves)
        assert sector_move is not None
        direction = "higher" if sector_move > 0 else "lower" if sector_move < 0 else "flat"
        aligned = sum(1 for move in moves if (move > 0) == (sector_move > 0)) if sector_move else 0
        breadth = aligned / len(moves) * 100.0 if sector_move else 0.0
        relative = sector_move - benchmark
        volume_ratio = median(row["_volume_ratio"] for row in rows)
        symbols = {str(row.get("symbol", "")).strip() for row in rows}
        related_news = _fresh_news(news, sector, symbols, as_of, max_news_age)

        magnitude_points = min(abs(sector_move) / 4.0 * 35.0, 35.0)
        relative_points = min(abs(relative) / 3.0 * 20.0, 20.0)
        breadth_points = breadth / 100.0 * 20.0
        volume_points = (
            min(max(volume_ratio - 1.0, 0.0), 1.0) * 10.0 if volume_ratio is not None else 0.0
        )
        news_points = min(len(related_news), 3) * 5.0
        score = round(magnitude_points + relative_points + breadth_points + volume_points + news_points, 1)

        leaders = sorted(rows, key=lambda row: abs(row["_change"]), reverse=True)[:3]
        signals = []
        if abs(sector_move) >= 2.0:
            signals.append("absolute sector move >= 2%")
        if abs(relative) >= 1.5:
            signals.append("benchmark-relative move >= 1.5ppt")
        if breadth >= 70.0:
            signals.append("broad participation >= 70%")
        if volume_ratio is not None and volume_ratio >= 1.5:
            signals.append("median volume >= 1.5x normal")
        if related_news:
            signals.append("fresh related news available for investigation")

        gaps = []
        if len(rows) < 3:
            gaps.append("sector basket has fewer than three priced names")
        if volume_ratio is None:
            gaps.append("volume context unavailable")
        if not related_news:
            gaps.append("no fresh related news in the supplied pack")

        topics.append(
            {
                "rank": 0,
                "sector": sector,
                "direction": direction,
                "topic": f"{sector} {direction} in {market}",
                "attention_score": score,
                "observation": {
                    "median_move_pct": round(sector_move, 4),
                    "benchmark_pct": round(benchmark, 4),
                    "relative_move_ppt": round(relative, 4),
                    "breadth_pct": round(breadth, 1),
                    "median_volume_ratio": None if volume_ratio is None else round(volume_ratio, 3),
                    "constituents": len(rows),
                },
                "leaders": [
                    {
                        "symbol": row.get("symbol"),
                        "name": row.get("name"),
                        "pct_change": round(row["_change"], 4),
                    }
                    for row in leaders
                ],
                "fresh_news_ids": [item.get("id") for item in related_news if item.get("id")],
                "trigger_signals": signals,
                "evidence_gaps": gaps,
                "causal_status": "not_assessed",
            }
        )

    topics.sort(key=lambda item: (item["attention_score"], abs(item["observation"]["median_move_pct"])), reverse=True)
    for index, item in enumerate(topics, start=1):
        item["rank"] = index
    limit = int(number(data.get("limit")) or 5)
    return {
        "schema_version": 1,
        "as_of": data["as_of"],
        "market": market,
        "benchmark_pct": benchmark,
        "topics": topics[: max(limit, 0)],
        "ignored_quotes": ignored,
        "note": "Ranking identifies observable topics only. It does not establish why a sector moved.",
    }


if __name__ == "__main__":
    import argparse

    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("input")
    cli.add_argument("--output")
    args = cli.parse_args()
    write_output(rank_topics(load_data(args.input)), args.output)
