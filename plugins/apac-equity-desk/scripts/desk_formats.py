"""Render house-style evidence packs without inventing facts or explanations.

Strings are analyst-authored prose. Objects with summary/source_ids preserve
inline citations. Validation checks structure, not factual truth.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Any
from urllib.parse import urlparse

BANNER = "DRAFT — HUMAN APPROVAL REQUIRED"


def validate_pack(pack: dict[str, Any]) -> None:
    if not isinstance(pack, dict):
        raise ValueError("A desk pack must be a JSON object.")
    timestamp = pack.get("as_of")
    if not isinstance(timestamp, str):
        raise ValueError("as_of must be an ISO timestamp with a timezone offset.")
    try:
        stamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("as_of must be an ISO timestamp with a timezone offset.") from exc
    if stamp.tzinfo is None:
        raise ValueError("as_of must include a timezone offset.")
    sources = pack.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError("sources must be an array.")
    ids = set()
    for source in sources:
        if not isinstance(source, dict) or not isinstance(source.get("id"), str) or not source["id"]:
            raise ValueError("Every source needs a nonempty string id.")
        if source["id"] in ids:
            raise ValueError(f"Duplicate source id: {source['id']}")
        ids.add(source["id"])
        parsed = urlparse(str(source.get("url", "")))
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError(f"Invalid source URL: {source['id']}")


def text(value: Any, sources: list[dict[str, Any]]) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    if not isinstance(value, dict) or not isinstance(value.get("summary"), str) or not value["summary"].strip():
        raise ValueError("Text must be a nonempty string or an object with summary.")
    result = value["summary"].strip()
    refs = value.get("source_ids", [])
    if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
        raise ValueError("source_ids must be an array of strings.")
    index = {source["id"]: source for source in sources}
    links = []
    for ref in dict.fromkeys(refs):
        if ref not in index:
            raise ValueError(f"Unknown source id: {ref}")
        source = index[ref]
        label = str(source.get("label") or ref).replace("[", "\\[").replace("]", "\\]")
        url = source["url"].replace("(", "%28").replace(")", "%29")
        links.append(f"[{label}]({url})")
    return result + (" " + " ".join(links) if links else "")


def paragraphs(block: dict[str, Any], field: str, sources: list[dict[str, Any]], required: bool = False) -> list[str]:
    values = block.get(field)
    if values is None or values == []:
        if required:
            raise ValueError(f"{field} must contain at least one paragraph.")
        return []
    if not isinstance(values, list):
        raise ValueError(f"{field} must be an array of text entries.")
    return [text(value, sources) for value in values]


def bullets(values: Any, sources: list[dict[str, Any]]) -> str:
    if not isinstance(values, list):
        raise ValueError("Bullet entries must be an array.")
    return "\n".join("- " + text(value, sources) for value in values)


def header(pack: dict[str, Any], title: str) -> list[str]:
    blocks = [BANNER]
    if pack.get("synthetic") is True:
        blocks.append("SYNTHETIC EXAMPLE — NOT MARKET DATA")
    blocks.extend([title, f"As of {pack['as_of']}"])
    return blocks


def review_notes(pack: dict[str, Any], sources: list[dict[str, Any]]) -> list[str]:
    blocks = []
    if pack.get("data_gaps"):
        blocks.append("Data gaps for review:\n\n" + bullets(pack["data_gaps"], sources))
    if pack.get("review_notes"):
        blocks.append("Editorial notes:\n\n" + bullets(pack["review_notes"], sources))
    return blocks


def render_close(pack: dict[str, Any]) -> str:
    validate_pack(pack)
    try:
        date.fromisoformat(pack["date"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("A close pack needs an ISO date.") from exc
    markets = pack.get("markets")
    if not isinstance(markets, list) or not markets:
        raise ValueError("A close pack needs at least one market.")
    sources = pack.get("sources", [])
    blocks = header(pack, f"Market close — {pack['date']}")
    for market in markets:
        if not isinstance(market, dict) or not isinstance(market.get("name"), str) or not market["name"].strip():
            raise ValueError("Every market needs a name.")
        if market.get("session") != "closed":
            raise ValueError(f"{market['name']}: a close wrap requires session=closed.")
        blocks.append(market["name"])
        blocks.extend(paragraphs(market, "lead", sources, required=True))
        for field in ("local_policy", "fx_rates", "macro_data", "sector_laggards", "sector_leaders"):
            blocks.extend(paragraphs(market, field, sources))
        if market.get("desk_aside"):
            blocks.append(text(market["desk_aside"], sources))
        if market.get("corporate_headlines"):
            blocks.append("**Corporate Headlines**\n\n" + bullets(market["corporate_headlines"], sources))
    blocks.extend(review_notes(pack, sources))
    return "\n\n".join(blocks) + "\n"


def render_theme(pack: dict[str, Any]) -> str:
    validate_pack(pack)
    headline = pack.get("headline")
    if not isinstance(headline, str) or not headline.strip():
        raise ValueError("A theme pack needs a headline.")
    tickers = pack.get("tickers")
    if not isinstance(tickers, list) or not tickers or any(not isinstance(ticker, str) or not ticker.strip() for ticker in tickers):
        raise ValueError("A theme pack needs verified ticker strings.")
    sources = pack.get("sources", [])
    blocks = header(pack, headline.strip())
    # Markdown hard breaks retain the separate ticker lines in rendered output.
    blocks.append("  \n".join(ticker.strip() for ticker in tickers))
    blocks.extend(paragraphs(pack, "move_context", sources, required=True))
    blocks.extend(paragraphs(pack, "fundamental_hook", sources))
    if pack.get("mixed_evidence"):
        blocks.append("Evidence so far:\n\n" + bullets(pack["mixed_evidence"], sources))
    if pack.get("implications"):
        blocks.append("Implications:\n\n" + bullets(pack["implications"], sources))
    if not pack.get("watch"):
        raise ValueError("A theme pack needs at least one watch point.")
    blocks.append("Things to watch:\n\n" + bullets(pack["watch"], sources))
    blocks.extend(review_notes(pack, sources))
    return "\n\n".join(blocks) + "\n"


def render_morning(pack: dict[str, Any]) -> str:
    validate_pack(pack)
    country = pack.get("country")
    if not isinstance(country, str) or not country.strip():
        raise ValueError("A morning pack needs a country.")
    session = pack.get("session")
    if session not in {"open", "pre_open"}:
        raise ValueError("A morning note requires session=open or pre_open.")
    # Fail closed on contradictory structure instead of dropping live-tape claims.
    if session == "pre_open" and pack.get("opening_tape"):
        raise ValueError("A pre-open pack cannot contain observed opening_tape.")
    if session == "open" and pack.get("pre_open_setup"):
        raise ValueError("An open-session pack should use opening_tape, not pre_open_setup.")
    tag = pack.get("country_tag", "")
    if not isinstance(tag, str):
        raise ValueError("country_tag must be a string.")
    title = f"{tag} {country.upper()} {'MORNING' if session == 'open' else 'PRE-OPEN'}".strip()
    sources = pack.get("sources", [])
    blocks = header(pack, title)
    first = "opening_tape" if session == "open" else "pre_open_setup"
    blocks.extend(paragraphs(pack, first, sources, required=True))
    blocks.extend(paragraphs(pack, "overnight_context", sources, required=True))
    blocks.extend(paragraphs(pack, "local_context", sources))
    blocks.extend(paragraphs(pack, "sector_drivers", sources, required=True))
    blocks.extend(paragraphs(pack, "research_focus", sources))
    if pack.get("watch") is not None:
        watch = bullets(pack["watch"], sources)
        if watch:
            blocks.append("Things to watch:\n\n" + watch)
    blocks.extend(review_notes(pack, sources))
    return "\n\n".join(blocks) + "\n"
