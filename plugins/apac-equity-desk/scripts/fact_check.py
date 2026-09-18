"""Audit a structured claim/source bundle for common desk-research failures."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any
from urllib.parse import urlparse

from common import load_data, number, parser, write_output


def _valid_url(value: Any) -> bool:
    parsed = urlparse(str(value or ""))
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def audit(bundle: dict[str, Any]) -> dict[str, Any]:
    claims = bundle.get("claims", [])
    sources = {str(source.get("id")): source for source in bundle.get("sources", []) if source.get("id")}
    findings: list[dict[str, str]] = []
    numeric_facts: dict[str, list[tuple[str, float, float]]] = defaultdict(list)

    def flag(severity: str, code: str, claim_id: str, detail: str) -> None:
        findings.append({"severity": severity, "code": code, "claim_id": claim_id, "detail": detail})

    for claim in claims:
        claim_id = str(claim.get("id", "unknown"))
        source_ids = [str(value) for value in claim.get("source_ids", [])]
        if not source_ids:
            flag("block", "uncited_claim", claim_id, "Claim has no source IDs.")
            continue
        linked = [sources[source_id] for source_id in source_ids if source_id in sources]
        missing = [source_id for source_id in source_ids if source_id not in sources]
        if missing:
            flag("block", "missing_source", claim_id, f"Unknown source IDs: {', '.join(missing)}")
        levels = [int(source.get("evidence_level")) for source in linked if str(source.get("evidence_level", "")).isdigit()]
        if claim.get("causal") is True and levels and min(levels) >= 4:
            flag("block", "level4_causality", claim_id, "Causal claim relies only on Level 4 evidence.")
        if claim.get("confirmed") is True and not any(level == 1 for level in levels):
            flag("revise", "confirmation_without_primary", claim_id, "Confirmed wording lacks Level 1 support.")
        for source in linked:
            if not _valid_url(source.get("url")):
                flag("revise", "invalid_url", claim_id, f"Source {source.get('id')} has no valid HTTP(S) URL.")
            timestamp = source.get("published_at")
            if timestamp:
                try: datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
                except ValueError: flag("revise", "invalid_timestamp", claim_id, f"Source {source.get('id')} timestamp is not ISO-8601.")
        fact_key, value = claim.get("fact_key"), number(claim.get("value"))
        if fact_key and value is not None:
            numeric_facts[str(fact_key)].append((claim_id, value, number(claim.get("tolerance")) or 0.0))

    for fact_key, values in numeric_facts.items():
        base_id, base, tolerance = values[0]
        for claim_id, value, own_tolerance in values[1:]:
            if abs(base - value) > max(tolerance, own_tolerance):
                flag("block", "numeric_conflict", claim_id, f"{fact_key} conflicts with {base_id}: {value} vs {base}.")

    status = "block" if any(item["severity"] == "block" for item in findings) else "revise" if findings else "pass"
    return {"status": status, "claims_checked": len(claims), "sources_checked": len(sources), "findings": findings}


if __name__ == "__main__":
    args = parser(__doc__).parse_args()
    data = load_data(args.input)
    if not isinstance(data, dict):
        raise SystemExit("Fact-check input must be a JSON object.")
    write_output(audit(data), args.output)

