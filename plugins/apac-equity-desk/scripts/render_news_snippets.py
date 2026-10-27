"""Render reviewed pre-open news items, preserving their order and inline sources."""
from __future__ import annotations

import argparse
from pathlib import Path

from common import load_data
from desk_formats import header, review_notes, text, validate_pack


def single_paragraph(value, field):
    if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
        raise ValueError(f"{field} must be a nonempty single-paragraph string.")
    return value.strip()


def render(pack):
    validate_pack(pack)
    if pack.get("format") != "desk-news-snippets":
        raise ValueError("News snippets require format=desk-news-snippets.")
    country = single_paragraph(pack.get("country"), "country")
    if pack.get("session") != "pre_open":
        raise ValueError("News snippets require session=pre_open.")
    if pack.get("opening_tape"):
        raise ValueError("A pre-open digest cannot contain observed opening_tape.")
    retrospective = pack.get("retrospective", False)
    if not isinstance(retrospective, bool):
        raise ValueError("retrospective must be a boolean.")
    items = pack.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("items must contain at least one news item.")

    sources = pack.get("sources", [])
    status = "RETROSPECTIVE PRE-OPEN" if retrospective else "PRE-OPEN"
    blocks = header(pack, f"{country} News Snippets:")
    blocks[-1] = f"{status} | Information cutoff {pack['as_of']}"
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Every news item must be an object.")
        summary = single_paragraph(item.get("summary"), "summary")
        refs = item.get("source_ids")
        if not isinstance(refs, list) or not refs:
            raise ValueError("Every news item needs nonempty source_ids.")
        if "headline" in item:
            headline = single_paragraph(item["headline"], "headline")
            summary = f"{headline}: {summary}"
        blocks.append(text({"summary": summary, "source_ids": refs}, sources))
    blocks.extend(review_notes(pack, sources))
    return "\n\n".join(blocks) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("--output")
    args = parser.parse_args()
    result = render(load_data(args.input))
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
    else:
        print(result, end="")
