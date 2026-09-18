"""Render an APAC close-wrap draft from a structured market pack."""

from __future__ import annotations

from typing import Any

from common import fmt_pct, load_data

BANNER = "DRAFT — HUMAN APPROVAL REQUIRED"


def _items(values: Any) -> str:
    if not values: return "n/a"
    if isinstance(values, str): return values
    return "; ".join(str(value.get("summary", value)) if isinstance(value, dict) else str(value) for value in values)


def render(pack: dict[str, Any]) -> str:
    if not pack.get("date") or not pack.get("markets"):
        raise ValueError("Market-wrap pack requires date and markets.")
    lines = [BANNER, "", f"APAC close — {pack['date']}", _items(pack.get("regional_lead")), ""]
    for market in pack["markets"]:
        name = market.get("name", "Market")
        indices = ", ".join(f"{item.get('name', item.get('symbol', 'index'))} {fmt_pct(item.get('pct_change'))}" for item in market.get("indices", [])) or "indices unavailable"
        breadth = market.get("breadth", {})
        breadth_text = f"breadth {breadth.get('advancers', 'n/a')}/{breadth.get('decliners', 'n/a')} advancers/decliners"
        sectors = _items(market.get("sectors"))
        movers = _items(market.get("movers"))
        catalysts = _items(market.get("catalysts"))
        flows = _items(market.get("flows"))
        lines.extend([f"{name} — {indices}; {breadth_text}. Sectors: {sectors}. Movers: {movers}. Drivers: {catalysts}. Flows/turnover: {flows}.", ""])
    if pack.get("cross_asset"): lines.append(f"Cross-asset: {_items(pack['cross_asset'])}.")
    if pack.get("tomorrow"): lines.append(f"Tomorrow: {_items(pack['tomorrow'])}.")
    if pack.get("data_gaps"): lines.append(f"Data gaps: {_items(pack['data_gaps'])}.")
    lines.append(f"As of: {pack.get('as_of', 'not supplied')}.")
    return "\n".join(lines).strip() + "\n"


if __name__ == "__main__":
    import argparse
    from pathlib import Path
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("input")
    cli.add_argument("--output")
    args = cli.parse_args()
    text = render(load_data(args.input))
    if args.output: Path(args.output).write_text(text, encoding="utf-8")
    else: print(text, end="")
