"""Plan tools from task-specific availability; never call services or classify prose.

The agent supplies semantic needs and eligibility evidence from the current host.
A successful plan is not evidence that research, extraction or verification ran.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "references" / "tool-capabilities.json"


def select_tools(request: dict, catalog: dict | None = None) -> dict:
    if request.get("schema") != "tool_request/v1":
        raise ValueError("Expected tool_request/v1")
    catalog = catalog or json.loads(CATALOG.read_text(encoding="utf-8"))
    capabilities = catalog["capabilities"]
    workflow = request.get("primary_workflow")
    if workflow not in catalog["workflows"]:
        raise ValueError("Unknown primary_workflow")
    needs = request.get("needs")
    if not isinstance(needs, list) or not needs:
        raise ValueError("Supply at least one evidence or deliverable need")
    rows, seen = [], set()
    for need in needs:
        identity = need.get("id")
        if not isinstance(identity, str) or not identity.strip() or identity in seen:
            raise ValueError("Need IDs must be nonempty and unique")
        seen.add(identity)
        capability = need.get("capability")
        if capability not in capabilities:
            raise ValueError(f"Unknown capability: {capability}")
        policy = capabilities[capability]
        if policy.get("workflows") and workflow not in policy["workflows"]:
            raise ValueError(f"{capability} is outside {workflow}")
        for flag in ("local_only", "required"):
            if type(need.get(flag)) is not bool:
                raise ValueError(f"{identity}: explicitly set {flag}")
        candidates = need.get("candidates", {})
        if not isinstance(candidates, dict):
            raise ValueError("candidates must be keyed by capability provider ID")
        order = list(policy["candidates"])
        unknown = set(candidates) - set(order)
        if unknown:
            raise ValueError(f"Unknown candidates for {capability}: {sorted(unknown)}")
        allowed = need.get("allowed_candidates", order)
        if not isinstance(allowed, list) or any(item not in order for item in allowed):
            raise ValueError("allowed_candidates must be a subset of the capability candidates")
        preferred = need.get("preferred_candidate")
        if preferred is not None:
            if preferred not in order:
                raise ValueError("Unknown preferred_candidate")
            order.remove(preferred)
            order.insert(0, preferred)
        usable, rejected = [], []
        for name in order:
            candidate = candidates.get(name, {})
            if not isinstance(candidate, dict):
                raise ValueError(f"{name}: candidate must be an object")
            if name not in allowed:
                reason = "excluded_by_source_constraint"
            elif candidate.get("state") != "callable":
                reason = "not_callable:" + str(candidate.get("state", "undiscovered"))
            elif candidate.get("eligible") is not True:
                reason = "not_fit_for_this_need"
            elif not isinstance(candidate.get("binding"), str) or not candidate["binding"].strip():
                reason = "missing_current_host_binding"
            elif not isinstance(candidate.get("evidence"), str) or not candidate["evidence"].strip():
                reason = "missing_eligibility_evidence"
            elif candidate.get("execution") not in {"local", "remote"}:
                reason = "unknown_execution_location"
            elif need["local_only"] and candidate["execution"] != "local":
                reason = "local_input_boundary"
            elif candidate.get("effect") not in policy.get("effects", ["read"]):
                reason = "effect_outside_scope"
            else:
                usable.append({"candidate": name, "binding": candidate["binding"]})
                continue
            rejected.append({"candidate": name, "reason": reason})
        rows.append({
            "id": identity,
            "capability": capability,
            "required": need["required"],
            "status": "planned" if usable else "gap",
            "selected": usable[0] if usable else None,
            "alternatives": usable[1:],
            "rejected": rejected,
        })
    return {
        "schema": "tool_plan/v1",
        "primary_workflow": workflow,
        "status": "limited" if any(row["required"] and row["status"] == "gap" for row in rows) else "planned",
        "needs": rows,
        "research_complete": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Local tool_request/v1 JSON")
    args = parser.parse_args()
    try:
        result = select_tools(json.loads(args.input.read_text(encoding="utf-8")))
    except (ValueError, TypeError, KeyError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
