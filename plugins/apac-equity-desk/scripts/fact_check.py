"""Audit a structured claim/source bundle for common desk-research failures."""

from __future__ import annotations

from collections import defaultdict
from math import isfinite
from typing import Any
from urllib.parse import urlparse

from common import load_data, number, parse_timestamp, parser, write_output


def _valid_url(value: Any) -> bool:
    parsed = urlparse(str(value or ""))
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def audit(bundle: dict[str, Any]) -> dict[str, Any]:
    claims = bundle.get("claims", [])
    sources = {str(source.get("id")): source for source in bundle.get("sources", []) if source.get("id")}
    findings: list[dict[str, str]] = []
    numeric_facts: dict[str, list[dict[str, Any]]] = defaultdict(list)
    as_of = parse_timestamp(bundle.get("as_of"))

    def flag(severity: str, code: str, claim_id: str, detail: str) -> None:
        findings.append({"severity": severity, "code": code, "claim_id": claim_id, "detail": detail})

    if bundle.get("as_of") and as_of is None:
        flag("revise", "invalid_as_of", "bundle", "as_of is not ISO-8601 with an offset; sources were not checked against it.")

    for claim in claims:
        claim_id = str(claim.get("id", "unknown"))
        raw_ids = claim.get("source_ids", [])
        # A bare string is one ID; iterating it would split "s1" into "s", "1".
        if raw_ids is None or raw_ids == "":
            source_ids = []
        elif isinstance(raw_ids, (list, tuple)):
            source_ids = [str(value) for value in raw_ids]
        else:
            source_ids = [str(raw_ids)]
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
        if claim.get("causal") is True and linked and not levels:
            flag("revise", "unknown_evidence_level", claim_id, "Causal claim cites sources with no evidence_level.")
        if claim.get("confirmed") is True and not any(level == 1 for level in levels):
            flag("revise", "confirmation_without_primary", claim_id, "Confirmed wording lacks Level 1 support.")
        evidence_times = []
        for source in linked:
            if not _valid_url(source.get("url")):
                flag("revise", "invalid_url", claim_id, f"Source {source.get('id')} has no valid HTTP(S) URL.")
            parsed_times = {}
            for field in ("published_at", "observed_at"):
                timestamp = source.get(field)
                if not timestamp:
                    continue
                parsed = parse_timestamp(timestamp)
                if parsed is None:
                    flag("revise", "invalid_timestamp", claim_id, f"Source {source.get('id')} {field} is not ISO-8601 with an offset.")
                    continue
                parsed_times[field] = parsed
                if as_of is not None and parsed > as_of:
                    flag("block", "source_after_as_of", claim_id, f"Source {source.get('id')} {field} is after the bundle as_of {bundle.get('as_of')}.")
            # Quotes and other observations use observed_at. Publication time is
            # the fallback for news and filings.
            evidence_time = parsed_times.get("observed_at") or parsed_times.get("published_at")
            if evidence_time is not None and (as_of is None or evidence_time <= as_of):
                evidence_times.append(evidence_time)

        max_age_raw = claim.get("max_age_minutes")
        if max_age_raw not in (None, ""):
            max_age = number(max_age_raw)
            if max_age is None or not isfinite(max_age) or max_age < 0:
                flag("revise", "invalid_max_age", claim_id, "max_age_minutes must be a non-negative finite number.")
            elif as_of is None or not evidence_times:
                flag("revise", "freshness_unverifiable", claim_id, "Freshness was required but no usable as_of/evidence timestamp was available.")
            else:
                age_minutes = (as_of - max(evidence_times)).total_seconds() / 60.0
                if age_minutes > max_age:
                    flag("block", "stale_evidence", claim_id, f"Freshest linked evidence is {age_minutes:.1f} minutes old; limit is {max_age:g} minutes.")
        fact_key, value = claim.get("fact_key"), number(claim.get("value"))
        if fact_key and value is not None:
            numeric_facts[str(fact_key)].append({
                "claim_id": claim_id,
                "value": value,
                "tolerance": number(claim.get("tolerance")) or 0.0,
                "unit": str(claim.get("unit", "")).strip(),
                "currency": str(claim.get("currency", "")).strip(),
                "session": str(claim.get("session", "")).strip(),
            })

    for fact_key, values in numeric_facts.items():
        base = values[0]
        for item in values[1:]:
            if abs(base["value"] - item["value"]) > max(base["tolerance"], item["tolerance"]):
                flag("block", "numeric_conflict", item["claim_id"], f"{fact_key} conflicts with {base['claim_id']}: {item['value']} vs {base['value']}.")
        for field in ("unit", "currency", "session"):
            normalized = {item[field].casefold() for item in values if item[field]}
            if len(normalized) > 1:
                detail = ", ".join(sorted({item[field] for item in values if item[field]}))
                flag("block", f"{field}_conflict", str(fact_key), f"Repeated fact {fact_key} mixes {field} values: {detail}.")

    status = "block" if any(item["severity"] == "block" for item in findings) else "revise" if findings else "pass"
    return {"status": status, "claims_checked": len(claims), "sources_checked": len(sources), "findings": findings}


if __name__ == "__main__":
    args = parser(__doc__).parse_args()
    data = load_data(args.input)
    if not isinstance(data, dict):
        raise SystemExit("Fact-check input must be a JSON object.")
    write_output(audit(data), args.output)

