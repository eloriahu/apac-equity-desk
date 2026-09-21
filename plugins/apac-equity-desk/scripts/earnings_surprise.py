"""Calculate actual-versus-consensus earnings surprises with unit checks."""

from __future__ import annotations

from typing import Any

from common import load_data, number, parser, records, write_output


def calculate_surprises(rows: list[dict[str, Any]], default_tolerance_pct: float = 0.5) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        item = dict(row)
        actual = number(row.get("actual"))
        consensus = number(row.get("consensus"))
        if actual is None or consensus is None:
            item.update({"surprise": None, "surprise_pct": None, "result": "unscored", "error": "actual and consensus are required"})
            output.append(item)
            continue
        mismatches = []
        for label in ("unit", "currency", "period", "basis"):
            actual_value = row.get(f"actual_{label}")
            consensus_value = row.get(f"consensus_{label}")
            if actual_value and consensus_value and actual_value != consensus_value:
                mismatches.append(label)
        if mismatches:
            item.update({"surprise": None, "surprise_pct": None, "result": "unscored", "error": f"actual and consensus differ on: {', '.join(mismatches)}"})
            output.append(item)
            continue
        surprise = actual - consensus
        surprise_pct = None if consensus == 0 else surprise / abs(consensus) * 100.0
        tolerance = number(row.get("tolerance_pct"))
        tolerance = default_tolerance_pct if tolerance is None else abs(tolerance)
        higher_is_better = row.get("lower_is_better") is not True
        effective = surprise if higher_is_better else -surprise
        in_line = abs(surprise_pct) <= tolerance if surprise_pct is not None else surprise == 0
        result = "in_line" if in_line else "beat" if effective > 0 else "miss"
        item.update(
            {
                "surprise": round(surprise, 8),
                "surprise_pct": None if surprise_pct is None else round(surprise_pct, 4),
                "result": result,
                "error": None,
            }
        )
        output.append(item)
    return output


if __name__ == "__main__":
    args = parser(__doc__).parse_args()
    write_output(calculate_surprises(records(load_data(args.input))), args.output)
