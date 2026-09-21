"""Shared, dependency-free helpers for normalized APAC desk data."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


def number(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return None


def percent_change(last: Any, base: Any) -> float | None:
    last_n, base_n = number(last), number(base)
    if last_n is None or base_n in (None, 0):
        return None
    return (last_n / base_n - 1.0) * 100.0


def price(row: dict[str, Any]) -> float | None:
    """Return `last`, falling back to `close` when `last` is absent or blank (common in CSV)."""
    value = number(row.get("last"))
    return value if value is not None else number(row.get("close"))


def row_pct_change(row: dict[str, Any]) -> float | None:
    """Use a supplied `pct_change`, otherwise compute it from price() and `prev_close`."""
    value = number(row.get("pct_change"))
    return value if value is not None else percent_change(price(row), row.get("prev_close"))


def flag(value: Any) -> bool:
    """Read a boolean signal from JSON (true) or CSV text ("true", "1", "yes", "y")."""
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"true", "yes", "y"}:
        return True
    return number(text) == 1  # 1, 1.0 and "1.0" from spreadsheet exports


def parse_timestamp(value: Any) -> datetime | None:
    """Parse an ISO-8601 timestamp with an offset; naive or malformed values return None."""
    try:
        stamp = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    return stamp if stamp.tzinfo is not None else None


def median(values: Iterable[Any]) -> float | None:
    nums = sorted(v for value in values if (v := number(value)) is not None)
    if not nums:
        return None
    middle = len(nums) // 2
    return nums[middle] if len(nums) % 2 else (nums[middle - 1] + nums[middle]) / 2


def load_data(path: str) -> Any:
    if path == "-":
        return json.load(sys.stdin)
    source = Path(path)
    if source.suffix.lower() == ".csv":
        with source.open(encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    with source.open(encoding="utf-8-sig") as handle:
        return json.load(handle)


def records(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list) and all(isinstance(row, dict) for row in data):
        return data
    if isinstance(data, dict):
        for key in ("rows", "quotes", "records", "articles", "pairs"):
            value = data.get(key)
            if isinstance(value, list) and all(isinstance(row, dict) for row in value):
                return value
    raise ValueError("Input must be an array of objects or an object containing rows/quotes/records/articles/pairs.")


def write_output(payload: Any, output: str | None) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if output:
        Path(output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


def iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def parser(description: str) -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=description)
    result.add_argument("input", help="Normalized JSON/CSV input, or - for JSON stdin")
    result.add_argument("--output", help="Write output to a file instead of stdout")
    return result


def fmt_pct(value: Any, digits: int = 1) -> str:
    value_n = number(value)
    return "n/a" if value_n is None else f"{value_n:+.{digits}f}%"

