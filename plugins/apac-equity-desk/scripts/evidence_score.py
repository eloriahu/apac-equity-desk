"""Score proposed price drivers with the 0-8 rubric in references/source-priority.md.

Input rows: `id`, `summary`, `evidence_level` (1-4), `freshness`, `specificity`,
`market_fit`. Freshness/specificity/market_fit accept the rubric's 0-2 points or
its words. The score is editorial confidence, not a probability.
"""

from __future__ import annotations

from typing import Any

from common import load_data, number, parser, records, write_output

AUTHORITY = {1: 2, 2: 1, 3: 1, 4: 0}
WORDS = {
    "freshness": {"first_disclosed": 2, "new": 2, "updated": 1, "stale": 0, "unknown": 0},
    "specificity": {"security": 2, "direct": 2, "sector": 1, "read_through": 1, "macro": 0},
    "market_fit": {"strong": 2, "partial": 1, "contradicts": 0, "none": 0},
}


def _points(dimension: str, value: Any) -> int | None:
    if isinstance(value, str) and value.strip().lower() in WORDS[dimension]:
        return WORDS[dimension][value.strip().lower()]
    points = number(value)
    return int(points) if points is not None and points in (0, 1, 2) else None


def band(score: int) -> str:
    return "high" if score >= 7 else "medium" if score >= 4 else "low"


def score_drivers(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for row in rows:
        item = dict(row)
        level = number(row.get("evidence_level"))
        # Only whole levels 1-4 count; 1.9, nan or inf are unscored, not truncated.
        parts = {"authority": AUTHORITY.get(int(level)) if level in (1, 2, 3, 4) else None}
        parts.update({dimension: _points(dimension, row.get(dimension)) for dimension in WORDS})
        missing = [name for name, value in parts.items() if value is None]
        # An unscored dimension counts as zero, so a gap can only lower confidence.
        total = sum(value or 0 for value in parts.values())
        item.update({"score_parts": parts, "score": total, "confidence": band(total), "unscored": missing})
        result.append(item)
    return sorted(result, key=lambda item: item["score"], reverse=True)


if __name__ == "__main__":
    args = parser(__doc__).parse_args()
    write_output(score_drivers(records(load_data(args.input))), args.output)
