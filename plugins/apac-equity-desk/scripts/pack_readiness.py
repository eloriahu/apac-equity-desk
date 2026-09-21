"""Apply mode-specific completeness and freshness gates to an evidence pack."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from common import load_data, number, parse_timestamp, write_output


REQUIRED = {
    "topic-radar": ("as_of", "market", "quotes"),
    "morning": ("as_of", "country", "session", "overnight_context", "sector_drivers"),
    "wrap": ("as_of", "date", "markets"),
    "color": ("as_of",),
    "earnings": ("as_of", "company", "rows"),
}


def _get(data: dict[str, Any], path: str) -> Any:
    value: Any = data
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def _empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def assess_pack(data: dict[str, Any], mode: str, max_age_minutes: int | None = None) -> dict[str, Any]:
    if mode not in REQUIRED:
        raise ValueError(f"mode must be one of: {', '.join(sorted(REQUIRED))}")
    if not isinstance(data, dict):
        raise ValueError("Evidence pack must be a JSON object.")
    missing = [path for path in REQUIRED[mode] if _empty(_get(data, path))]
    warnings = []
    stale = []

    as_of = parse_timestamp(data.get("as_of"))
    if data.get("as_of") and as_of is None:
        missing.append("as_of(valid offset timestamp)")
    expected_market_timestamp = parse_timestamp(data.get("expected_market_timestamp"))
    if data.get("expected_market_timestamp") and expected_market_timestamp is None:
        missing.append("expected_market_timestamp(valid offset timestamp)")
    reference_time = expected_market_timestamp or as_of
    freshness = data.get("freshness", [])
    if freshness and not isinstance(freshness, list):
        warnings.append("freshness must be an array; freshness checks were skipped")
        freshness = []
    default_limit = 5 if mode == "topic-radar" else 60
    limit = max_age_minutes if max_age_minutes is not None else int(number(data.get("max_age_minutes")) or default_limit)
    if reference_time:
        for item in freshness:
            if not isinstance(item, dict):
                continue
            observed = parse_timestamp(item.get("observed_at"))
            item_id = str(item.get("id") or item.get("field") or "unnamed")
            if observed is None:
                warnings.append(f"{item_id}: missing or invalid observed_at")
                continue
            age = (reference_time - observed).total_seconds() / 60.0
            item_limit = number(item.get("max_age_minutes")) or limit
            if age > item_limit:
                stale.append({"id": item_id, "age_minutes": round(age, 1), "limit_minutes": item_limit})

    if mode == "morning":
        session = data.get("session")
        required_session_field = "opening_tape" if session == "open" else "pre_open_setup" if session == "pre_open" else None
        if required_session_field and _empty(data.get(required_session_field)):
            missing.append(required_session_field)
        if session not in {"open", "pre_open"}:
            warnings.append("morning session should be open or pre_open")
    if mode == "color" and _empty(data.get("tickers")) and _empty(data.get("subject")):
        missing.append("tickers|subject")
    if mode == "topic-radar" and isinstance(data.get("quotes"), list):
        quotes = data["quotes"]
        if len(quotes) < 3:
            warnings.append("fewer than three quotes limits sector comparison")
        if _empty(data.get("provider")) and _empty(data.get("provider_policy")):
            missing.append("provider|provider_policy")
        if _empty(data.get("movement_basis")):
            missing.append("movement_basis")
        quote_times = []
        fallback_time = parse_timestamp(data.get("data_as_of"))
        for position, quote in enumerate(quotes, start=1):
            if not isinstance(quote, dict):
                continue
            item_id = str(quote.get("symbol") or quote.get("name") or f"quote-{position}")
            observed = parse_timestamp(quote.get("timestamp")) or fallback_time
            if observed is None:
                missing.append(f"quotes.{item_id}.timestamp")
                continue
            quote_times.append((item_id, observed))
            if reference_time:
                age = (reference_time - observed).total_seconds() / 60.0
                if age > limit:
                    stale.append({"id": item_id, "age_minutes": round(age, 1), "limit_minutes": limit})
        if len(quote_times) > 1:
            times = [value for _, value in quote_times]
            skew = (max(times) - min(times)).total_seconds() / 60.0
            max_skew = number(data.get("max_skew_minutes")) or 5
            if skew > max_skew:
                stale.append({"id": "quote_capture_skew", "age_minutes": round(skew, 1), "limit_minutes": max_skew})
    if data.get("data_gaps"):
        warnings.append("pack declares data gaps")

    status = "block" if missing or stale else "limited" if warnings else "ready"
    return {
        "mode": mode,
        "status": status,
        "missing": sorted(set(missing)),
        "stale": stale,
        "warnings": warnings,
        "reference_timestamp": reference_time.isoformat() if reference_time else None,
        "can_draft": status != "block",
    }


if __name__ == "__main__":
    import argparse

    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("input")
    cli.add_argument("--mode", required=True, choices=sorted(REQUIRED))
    cli.add_argument("--max-age-minutes", type=int)
    cli.add_argument("--output")
    args = cli.parse_args()
    write_output(assess_pack(load_data(args.input), args.mode, args.max_age_minutes), args.output)
