"""Shared validation and immutable JSON output for offline event research."""
import argparse
import hashlib
import json
import math
from datetime import datetime, date
from pathlib import Path

DRAFT = "DRAFT — HUMAN APPROVAL REQUIRED"


def fields(value, required, optional=()):
    if not isinstance(value, dict):
        raise ValueError("Expected an object")
    missing, extra = set(required) - value.keys(), value.keys() - set(required) - set(optional)
    if missing or extra:
        raise ValueError(f"Missing fields: {sorted(missing)}; unsupported fields: {sorted(extra)}")


def num(value, minimum=None, maximum=None):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value):
        raise ValueError("Expected a finite number")
    if minimum is not None and value < minimum or maximum is not None and value > maximum:
        raise ValueError(f"Number outside bounds [{minimum}, {maximum}]")
    return float(value)


def positive(value):
    result = num(value, 0)
    if result == 0:
        raise ValueError("Expected a positive number")
    return result


def string(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Expected a nonempty string")
    return value


def timestamp(value):
    result = datetime.fromisoformat(string(value).replace("Z", "+00:00"))
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError("Timestamp must include a timezone")
    return result


def day(value):
    result = date.fromisoformat(string(value))
    if result.isoformat() != value:
        raise ValueError("Dates must use YYYY-MM-DD")
    return result


def items(value, nonempty=True):
    if not isinstance(value, list) or (nonempty and not value):
        raise ValueError("Expected a nonempty list" if nonempty else "Expected a list")
    return value


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False,
                                    separators=(",", ":")).encode()).hexdigest()


def result(schema, data, **values):
    return dict(schema=schema, status=DRAFT, input_sha256=digest(data), inputs=data, **values)


def cli(functions):
    parser = argparse.ArgumentParser(description="Offline event-driven research; see event-driven/toolkit.md")
    parser.add_argument("workflow", choices=functions)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8-sig"))
        output = json.dumps(functions[args.workflow](data), indent=2, allow_nan=False) + "\n"
        if args.output:
            with args.output.open("x", encoding="utf-8") as handle:
                handle.write(output)
        else:
            print(output, end="")
    except (ValueError, OSError, OverflowError, TypeError) as exc:
        parser.exit(2, f"error: {exc}\n")
