"""Render a compact market-colour draft from a validated evidence pack."""

from __future__ import annotations

from typing import Any

from common import fmt_pct, load_data, number

BANNER = "DRAFT — HUMAN APPROVAL REQUIRED"


def _join(items: Any) -> str:
    if not items:
        return "None identified."
    if isinstance(items, str):
        return items
    return "; ".join(str(item.get("summary", item)) if isinstance(item, dict) else str(item) for item in items)


def render(pack: dict[str, Any]) -> str:
    if pack.get("format") == "desk-theme":
        from desk_formats import render_theme
        return render_theme(pack)
    if pack.get("format") not in (None, "single-stock"):
        raise ValueError("Unknown colour format; use desk-theme or single-stock.")
    required = ("as_of", "subject", "move", "relative", "catalysts", "watch")
    missing = [key for key in required if not pack.get(key)]
    if missing:
        raise ValueError(f"Market-colour pack missing: {', '.join(missing)}")
    subject, move, relative = pack["subject"], pack["move"], pack["relative"]
    name = subject.get("name") or subject.get("symbol") or "Security"
    ticker = subject.get("desk_ticker") or subject.get("symbol") or ""
    move_pct = number(move.get("pct_change"))
    peer_spread = number(relative.get("peer_spread_ppt"))
    lead = f"{name} {ticker} {fmt_pct(move_pct)}"
    if peer_spread is not None:
        lead += f", {'outperforming' if peer_spread >= 0 else 'underperforming'} its peer basket by {abs(peer_spread):.1f}ppt"
    lead += f" as of {pack['as_of']}."

    catalysts = sorted(pack.get("catalysts", []), key=lambda item: {"high": 0, "medium": 1, "low": 2}.get(str(item.get("confidence", "low")).lower(), 3))
    confirmed = [item for item in catalysts if str(item.get("status", "")).lower() == "confirmed"]
    catalyst_line = _join(confirmed[:1]) if confirmed else "No single catalyst is confirmed. " + _join(catalysts[:2])
    lines = [BANNER, "", lead, "", f"What/relative: {_join(move.get('detail'))} {_join(relative.get('detail'))}".strip(),
             f"Catalyst: {catalyst_line}"]
    if pack.get("secondary_factors"): lines.append(f"Secondary factors: {_join(pack['secondary_factors'])}")
    if pack.get("flow_technical"): lines.append(f"Flow/technical: {_join(pack['flow_technical'])}")
    if pack.get("chatter"):
        chatter = pack["chatter"]
        prefix = "Unconfirmed chatter: " if "unconfirmed" not in str(chatter).lower() else "Chatter: "
        lines.append(prefix + _join(chatter))
    if pack.get("read_through"): lines.append(f"Read-through: {_join(pack['read_through'])}")
    lines.append(f"Watch: {_join(pack['watch'])}")
    if pack.get("data_gaps"): lines.append(f"Data gaps: {_join(pack['data_gaps'])}")
    return "\n".join(lines).strip() + "\n"


if __name__ == "__main__":
    import argparse
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("input")
    cli.add_argument("--output")
    args = cli.parse_args()
    payload = load_data(args.input)
    text = render(payload)
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
