"""Report whether APAC markets are pre-open, open, at lunch or closed at a given instant.

Offline fallback for the skills' "check the market clock" step. Prefer Longbridge
market_status / trading_days when connected. Holidays are only known when the
calendar (or --holidays file) lists them; otherwise the output says so.
"""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, time, timedelta, timezone, tzinfo
from pathlib import Path
from typing import Any

from common import parse_timestamp, write_output

CALENDAR = Path(__file__).resolve().parents[1] / "references" / "market-calendars.json"


def _fixed(offset: str) -> timezone:
    sign = -1 if offset.startswith("-") else 1
    hours, minutes = offset.lstrip("+-").split(":")
    return timezone(sign * timedelta(hours=int(hours), minutes=int(minutes)))


def _first_sunday(year: int, month: int) -> date:
    first = date(year, month, 1)
    return first + timedelta(days=(6 - first.weekday()) % 7)


def _au_dst(standard_local: datetime) -> bool:
    # NSW daylight saving: 02:00 standard time on the first Sunday of October
    # until 02:00 standard time (03:00 daylight) on the first Sunday of April.
    naive = standard_local.replace(tzinfo=None)
    start = datetime.combine(_first_sunday(naive.year, 10), time(2))
    end = datetime.combine(_first_sunday(naive.year, 4), time(2))
    return naive >= start or naive < end


def _zone(spec: dict[str, Any]) -> tzinfo | None:
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(spec["timezone"])
    except Exception:  # zoneinfo missing tz data (plain Windows Python without tzdata)
        return None


def local_time(spec: dict[str, Any], instant: datetime) -> datetime:
    zone = _zone(spec)
    if zone is not None:
        return instant.astimezone(zone)
    standard = instant.astimezone(_fixed(spec["utc_offset"]))
    if spec.get("dst") == "AU" and _au_dst(standard):
        return instant.astimezone(timezone(standard.utcoffset() + timedelta(hours=1)))
    return standard


def _sessions(spec: dict[str, Any], early_close: str | None) -> list[tuple[time, time]]:
    result = []
    for window in spec["regular_session"]:
        start, end = (time.fromisoformat(part) for part in window.split("-"))
        if early_close:
            cutoff = time.fromisoformat(early_close)
            if start >= cutoff:
                continue
            end = min(end, cutoff)
        result.append((start, end))
    return result


def market_status(code: str, instant: datetime, calendar: dict[str, Any]) -> dict[str, Any]:
    spec = calendar["markets"][code]
    holidays = calendar.get("holidays", {}).get(code)
    local = local_time(spec, instant)
    today = local.date().isoformat()
    closed_dates = set((holidays or {}).get("closed", []))
    early_close = (holidays or {}).get("half_day", {}).get(today)
    now = local.time().replace(tzinfo=None)
    sessions = _sessions(spec, early_close)

    if local.weekday() >= 5:
        status = "weekend"
    elif today in closed_dates:
        status = "holiday"
    elif not sessions:
        # An early close at or before the first session start leaves no trading.
        status = "closed"
    elif now < sessions[0][0]:
        status = "pre_open"
    elif now >= sessions[-1][1]:
        status = "closed"
    elif any(start <= now < end for start, end in sessions):
        status = "open"
    else:
        status = "lunch_break"

    return {
        "market": code,
        "name": spec.get("name", code),
        "local_time": local.isoformat(timespec="minutes"),
        "timezone": spec["timezone"],
        "status": status,
        "session_date": today,
        "half_day_close": early_close,
        "holiday_calendar_loaded": holidays is not None,
        "sessions": [f"{start:%H:%M}-{end:%H:%M}" for start, end in sessions],
    }


def load_calendar(path: Path = CALENDAR, holidays_path: str | None = None) -> dict[str, Any]:
    calendar = json.loads(path.read_text(encoding="utf-8"))
    calendar.setdefault("holidays", {})
    if holidays_path:
        calendar["holidays"].update(json.loads(Path(holidays_path).read_text(encoding="utf-8")))
    calendar["holidays"] = {key: value for key, value in calendar["holidays"].items() if not key.startswith("_")}
    return calendar


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--markets", default="CN,HK,JP,KR,AU,SG", help="Comma-separated market codes")
    cli.add_argument("--at", help="ISO timestamp with offset; defaults to now")
    cli.add_argument("--holidays", help="JSON file of verified closed dates / half days per market")
    cli.add_argument("--output")
    args = cli.parse_args()
    instant = parse_timestamp(args.at) if args.at else datetime.now(timezone.utc)
    if instant is None:
        raise SystemExit("--at must be an ISO timestamp with a timezone offset.")
    calendar = load_calendar(holidays_path=args.holidays)
    unknown = [code for code in args.markets.split(",") if code not in calendar["markets"]]
    if unknown:
        raise SystemExit(f"Unknown market code(s): {', '.join(unknown)}. Known: {', '.join(calendar['markets'])}")
    write_output({
        "as_of": instant.isoformat(timespec="seconds"),
        "markets": [market_status(code, instant, calendar) for code in args.markets.split(",")],
    }, args.output)
