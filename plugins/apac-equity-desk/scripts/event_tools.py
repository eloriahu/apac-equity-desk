"""Deal radar, cited term comparison, sensitivity, consideration models and alerts."""
from copy import deepcopy
from itertools import product

from event_common import cli, digest, fields, items, num, positive, result, string, timestamp
from merger_arb import calculate


def radar(data):
    fields(data, ("schema", "as_of", "since", "coverage", "markets", "event_types", "records"))
    if data["schema"] != "deal_radar/v1":
        raise ValueError("schema must be deal_radar/v1")
    as_of, since = timestamp(data["as_of"]), timestamp(data["since"])
    if since > as_of:
        raise ValueError("since must precede as_of")
    string(data["coverage"])
    markets, types = items(data["markets"]), items(data["event_types"])
    for v in markets + types:
        string(v)
    grouped, excluded, seen = {}, [], set()
    for record in items(data["records"], False):
        fields(record, ("deal_id", "market", "event_type", "status", "title", "source_url",
                        "source_type", "published_at", "observed_at", "verified", "terms"))
        for k in ("deal_id", "market", "event_type", "status", "title", "source_url"):
            string(record[k])
        if record["source_type"] not in {"official", "secondary"} or type(record["verified"]) is not bool:
            raise ValueError("source_type must be official/secondary and verified must be boolean")
        if not isinstance(record["terms"], dict):
            raise ValueError("terms must be an object; use {} when unavailable")
        published, observed = timestamp(record["published_at"]), timestamp(record["observed_at"])
        if observed < published:
            raise ValueError("observed_at precedes publication")
        reason = None
        if published > as_of or observed > as_of:
            reason = "not_available_at_cutoff"
        elif published < since:
            reason = "outside_window"
        elif record["market"] not in markets or record["event_type"] not in types:
            reason = "outside_universe"
        identity = digest(record)
        if identity in seen:
            reason = "duplicate_record"
        seen.add(identity)
        if reason:
            excluded.append({"deal_id": record["deal_id"], "source_url": record["source_url"], "reason": reason})
        else:
            grouped.setdefault(record["deal_id"], []).append(record)
    candidates = []
    for deal_id, records in sorted(grouped.items()):
        official = [r for r in records if r["source_type"] == "official" and r["verified"]]
        ranked = sorted(official or records, key=lambda r: (timestamp(r["published_at"]),
                                                          timestamp(r["observed_at"])), reverse=True)
        latest = ranked[0]
        concurrent = [r for r in ranked if timestamp(r["published_at"]) == timestamp(latest["published_at"])]
        conflict = len({digest({"status": r["status"], "terms": r["terms"]}) for r in concurrent}) > 1
        candidates.append({"deal_id": deal_id, "classification": "needs_review" if conflict or not official else "primary_verified",
                           "latest": latest, "concurrent_conflict": conflict, "evidence": records})
    return result("deal_radar_result/v1", data, candidates=candidates, excluded=excluded,
                  warnings=["Coverage is the supplied source universe, not a complete live exchange feed.",
                            "Verification flags are analyst attestations; the helper does not fetch or authenticate documents."])


def document(data):
    fields(data, ("schema", "deal_id", "before", "after"))
    if data["schema"] != "deal_documents/v1":
        raise ValueError("schema must be deal_documents/v1")
    string(data["deal_id"])
    for snap in (data["before"], data["after"]):
        fields(snap, ("document_id", "source_url", "published_at", "terms"))
        string(snap["document_id"])
        string(snap["source_url"])
        timestamp(snap["published_at"])
        if not isinstance(snap["terms"], dict):
            raise ValueError("terms must be an object")
        for key, term in snap["terms"].items():
            string(key)
            fields(term, ("value", "status", "locator"))
            if term["status"] not in {"known", "unknown", "not_applicable"}:
                raise ValueError("Term status must be known, unknown or not_applicable")
            string(term["locator"])
            if (term["value"] is None) != (term["status"] != "known"):
                raise ValueError("Known terms require a value; unknown/not_applicable terms require null")
    before, after = data["before"], data["after"]
    if timestamp(before["published_at"]) > timestamp(after["published_at"]):
        raise ValueError("Document chronology is reversed")
    changes = []
    for key in sorted(before["terms"].keys() | after["terms"].keys()):
        old, new = before["terms"].get(key), after["terms"].get(key)
        if old is None:
            kind = "newly_observed"
        elif new is None:
            kind = "not_observed_in_new_document"
        elif old["status"] != new["status"]:
            kind = "evidence_status_changed"
        elif digest(old["value"]) != digest(new["value"]):
            kind = "value_changed"
        else:
            kind = "unchanged"
        changes.append({"term": key, "change": kind, "before": old, "after": new})
    return result("deal_documents_result/v1", data, terms=changes,
                  warnings=["Normalized term comparison; inspect cited original pages before interpreting legal effect.",
                            "Omission from a newer document does not repeal an earlier contractual provision."])


def sensitivity(data):
    fields(data, ("schema", "base_deal", "close_probabilities", "break_prices", "close_days"))
    if data["schema"] != "probability_sensitivity/v1":
        raise ValueError("schema must be probability_sensitivity/v1")
    base = deepcopy(data["base_deal"])
    calculate(base)
    if len(base["scenarios"]) != 2 or {s["outcome"] for s in base["scenarios"]} != {"close", "break"}:
        raise ValueError("Sensitivity requires exactly one close and one break scenario")
    probabilities = [num(v, 0, 1) for v in items(data["close_probabilities"])]
    breaks = [num(v, 0) for v in items(data["break_prices"])]
    days = [positive(v) for v in items(data["close_days"])]
    if any(not v.is_integer() for v in days):
        raise ValueError("close_days must contain integer calendar days")
    if len(probabilities) * len(breaks) * len(days) > 10000:
        raise ValueError("Grid limited to 10,000 cells")
    rows = []
    for p, b, d in product(probabilities, breaks, days):
        deal = deepcopy(base)
        for s in deal["scenarios"]:
            s["probability"] = p if s["outcome"] == "close" else 1 - p
            if s["outcome"] == "close":
                s["days"] = int(d)
            else:
                s["target_exit"] = b
        model = calculate(deal)
        rows.append({"close_probability": p, "break_price": b, "close_days": int(d),
                     "expected_net_pnl": model["expected_net_pnl"],
                     "expected_return_on_capital": model["expected_return_on_capital"],
                     "two_state_net_pnl_breakeven_probability": model["two_state_net_pnl_breakeven_probability"],
                     "close_net_pnl": next(s["net_pnl"] for s in model["scenarios"] if s["outcome"] == "close"),
                     "break_net_pnl": next(s["net_pnl"] for s in model["scenarios"] if s["outcome"] == "break")})
    return result("probability_sensitivity_result/v1", data, grid=rows,
                  warnings=["Probabilities are assumptions, not estimates inferred from the spread.",
                            "Only close timing varies; break timing and both acquirer exits remain as specified in base_deal.",
                            "Expected P&L is not annualized across different outcome durations."])


def models(data):
    fields(data, ("schema", "deal_id", "as_of", "currency", "target_price", "discount_rate", "cost_pv", "scenarios"))
    if data["schema"] != "deal_models/v1":
        raise ValueError("schema must be deal_models/v1")
    string(data["deal_id"])
    string(data["currency"])
    timestamp(data["as_of"])
    entry, rate, costs = positive(data["target_price"]), num(data["discount_rate"], 0), num(data["cost_pv"], 0)
    output, names = [], set()
    for s in items(data["scenarios"]):
        fields(s, ("name", "probability", "components"))
        name = string(s["name"])
        if name in names:
            raise ValueError("Scenario names must be unique")
        names.add(name)
        p = num(s["probability"], 0, 1)
        components = []
        for c in items(s["components"]):
            if not isinstance(c, dict):
                raise ValueError("Component must be an object")
            kind = c.get("kind")
            common = ("kind", "days", "fx_to_base", "source_locator")
            specifics = {"cash": ("amount",), "stock": ("ratio", "settlement_price"),
                         "fixed_value_collar": ("stock_value", "reference_price", "floor", "ceiling",
                                                "ratio_below_floor", "ratio_above_ceiling", "settlement_price"),
                         "cvr": ("payment", "payment_probability"),
                         "proration": ("accepted_fraction", "accepted_value", "residual_value")}
            if kind not in specifics:
                raise ValueError(f"Unsupported consideration component: {kind}")
            fields(c, common + specifics[kind])
            days, fx = num(c["days"], 0), positive(c["fx_to_base"])
            if not days.is_integer():
                raise ValueError("days must be integer calendar days from valuation")
            string(c["source_locator"])
            ratio = None
            if kind == "cash":
                payoff = num(c["amount"], 0)
            elif kind == "stock":
                ratio = num(c["ratio"], 0)
                payoff = ratio * num(c["settlement_price"], 0)
            elif kind == "fixed_value_collar":
                floor, ceiling = positive(c["floor"]), positive(c["ceiling"])
                if floor >= ceiling:
                    raise ValueError("Collar floor must be below ceiling")
                ref, value = positive(c["reference_price"]), positive(c["stock_value"])
                below, above = positive(c["ratio_below_floor"]), positive(c["ratio_above_ceiling"])
                if below < above:
                    raise ValueError("Fixed-value collar ratio below floor must be >= ratio above ceiling")
                ratio = below if ref <= floor else above if ref >= ceiling else value / ref
                payoff = ratio * num(c["settlement_price"], 0)
            elif kind == "cvr":
                payoff = num(c["payment"], 0) * num(c["payment_probability"], 0, 1)
            else:
                fraction = num(c["accepted_fraction"], 0, 1)
                payoff = fraction * num(c["accepted_value"], 0) + (1 - fraction) * num(c["residual_value"], 0)
            pv = payoff * fx / (1 + rate) ** (days / 365)
            components.append({"kind": kind, "exchange_ratio": ratio, "days": int(days),
                               "payoff_in_component_currency": payoff, "payoff_in_base_currency": payoff * fx,
                               "present_value": pv})
        total = sum(c["present_value"] for c in components)
        output.append({"name": name, "probability": p, "components": components,
                       "consideration_pv": total, "net_present_value": total - entry - costs})
    if abs(sum(s["probability"] for s in output) - 1) > 1e-9:
        raise ValueError("Scenario probabilities must sum to 1")
    return result("deal_models_result/v1", data, scenarios=output,
                  expected_net_present_value=sum(s["probability"] * s["net_present_value"] for s in output),
                  warnings=["Valuation cash flows, not a hedged trading P&L or executable hedge recommendation.",
                            "CVR probabilities are conditional on their parent scenario. Use joint scenarios for dependent or exclusive milestones.",
                            "Collar ratios use contract reference prices; stock proceeds use settlement prices. Contract rounding is supplied explicitly.",
                            "FX rates, proration, costs and residual values are supplied assumptions; taxes and dynamic financing are not inferred."])


def alert_snapshot(snapshot, as_of):
    fields(snapshot, ("deal_id", "as_of", "status", "terms", "target_price", "consideration", "deadline"))
    string(snapshot["deal_id"])
    string(snapshot["status"])
    observed = timestamp(snapshot["as_of"])
    if observed > as_of:
        raise ValueError("Snapshot is later than evaluation time")
    if not isinstance(snapshot["terms"], dict):
        raise ValueError("terms must be an object")
    spread = None
    if snapshot["target_price"] is not None and snapshot["consideration"] is not None:
        spread = (num(snapshot["consideration"], 0) / positive(snapshot["target_price"]) - 1) * 10000
    else:
        for k in ("target_price", "consideration"):
            if snapshot[k] is not None:
                positive(snapshot[k]) if k == "target_price" else num(snapshot[k], 0)
    if snapshot["deadline"] is not None:
        timestamp(snapshot["deadline"])
    return observed, spread


def alerts(data):
    fields(data, ("schema", "as_of", "previous", "current", "rules", "state"))
    if data["schema"] != "deal_alerts/v1":
        raise ValueError("schema must be deal_alerts/v1")
    now = timestamp(data["as_of"])
    rules = data["rules"]
    fields(rules, ("spread_widening_bps", "deadline_days", "stale_hours"))
    for k in rules:
        positive(rules[k])
    state = data["state"]
    fields(state, ("deal_id", "evaluated_at", "active", "seen_changes"))
    active_before = {string(v) for v in items(state["active"], False)}
    seen = {string(v) for v in items(state["seen_changes"], False)}
    current, previous = data["current"], data["previous"]
    observed, spread = alert_snapshot(current, now)
    if state["deal_id"] != current["deal_id"]:
        raise ValueError("Alert state belongs to another deal")
    if state["evaluated_at"] is not None and timestamp(state["evaluated_at"]) > now:
        raise ValueError("Cannot replay alert state backwards")
    events, active = [], set()

    def emit(kind, detail, persistent=False):
        key = digest({"deal_id": current["deal_id"], "kind": kind, "detail": detail})
        if persistent:
            active.add(key)
        if key not in (active_before if persistent else seen):
            events.append({"id": key, "deal_id": current["deal_id"], "kind": kind, "detail": detail})
        if not persistent:
            seen.add(key)

    if previous is not None:
        old_time, old_spread = alert_snapshot(previous, now)
        if previous["deal_id"] != current["deal_id"] or old_time > observed:
            raise ValueError("Snapshots must share deal_id and have ascending timestamps")
        for key in ("status", "terms", "deadline", "consideration"):
            if digest(previous[key]) != digest(current[key]):
                emit(key + "_changed", {"from": previous[key], "to": current[key], "observed_at": current["as_of"]})
        if spread is not None and old_spread is not None and spread - old_spread >= rules["spread_widening_bps"]:
            emit("spread_widened", {"from_bps": old_spread, "to_bps": spread, "observed_at": current["as_of"]})
    terminal = current["status"] in {"completed", "settled", "withdrawn", "terminated", "lapsed"}
    if spread is None and not terminal:
        emit("missing_price_or_consideration", {}, True)
    if not terminal and (now - observed).total_seconds() / 3600 >= rules["stale_hours"]:
        emit("stale_snapshot", {}, True)
    if current["deadline"] is not None and not terminal:
        days_left = (timestamp(current["deadline"]) - now).total_seconds() / 86400
        if days_left <= rules["deadline_days"]:
            emit("deadline_overdue" if days_left < 0 else "deadline_near", {"deadline": current["deadline"]}, True)
    next_state = {"deal_id": current["deal_id"], "evaluated_at": data["as_of"],
                  "active": sorted(active), "seen_changes": sorted(seen)}
    return result("deal_alerts_result/v1", data, events=events, next_state=next_state,
                  baseline_created=previous is None,
                  warnings=["Local research alerts only; no scheduling, delivery or brokerage alert mutation.",
                            "Persist next_state and the current snapshot for the next evaluation; serialize evaluations per deal.",
                            "Spread changes are versus the supplied previous observation, not a rolling high-water mark."])


if __name__ == "__main__":
    cli({"radar": radar, "documents": document, "sensitivity": sensitivity, "models": models, "alerts": alerts})
