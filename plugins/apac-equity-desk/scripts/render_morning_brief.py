"""Render an opening-tape morning snippet or explicitly labelled pre-open note."""
from __future__ import annotations

import argparse
from pathlib import Path

from common import load_data
from desk_formats import render_morning


def render(pack):
    if pack.get("format") != "desk-morning":
        raise ValueError("Morning snippets require format=desk-morning.")
    return render_morning(pack)


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
