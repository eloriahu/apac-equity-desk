"""Offline daily, fully funded long-only event portfolio replay using supplied decisions."""
from event_common import cli, day, fields, items, num, positive, result, string, timestamp


def metrics(rows, initial, benchmark_start):
    peak, drawdown = initial, 0.0
    for row in rows:
        peak = max(peak, row["nav"])
        drawdown = min(drawdown, row["nav"] / peak - 1) if peak else drawdown
    return {"return": rows[-1]["nav"] / initial - 1 if initial else None,
            "benchmark_return": rows[-1]["benchmark"] / benchmark_start - 1,
            "max_drawdown": drawdown, "observations": len(rows)}


def backtest(data):
    fields(data, ("schema", "currency", "initial_capital", "cash_rate", "entry_cost_bps", "exit_cost_bps",
                  "max_trade_fraction", "policy", "coverage", "splits", "sessions", "trades"))
    if data["schema"] != "event_backtest/v1":
        raise ValueError("schema must be event_backtest/v1")
    string(data["currency"])
    capital, cash_rate = positive(data["initial_capital"]), num(data["cash_rate"], 0)
    entry_fee, exit_fee = num(data["entry_cost_bps"], 0, 10000) / 10000, num(data["exit_cost_bps"], 0, 10000) / 10000
    max_fraction = positive(data["max_trade_fraction"])
    if max_fraction > 1:
        raise ValueError("max_trade_fraction must be <= 1")
    fields(data["policy"], ("frozen_at", "selection_rule", "sizing_rule", "benchmark"))
    frozen = timestamp(data["policy"]["frozen_at"])
    for k in ("selection_rule", "sizing_rule", "benchmark"):
        string(data["policy"][k])
    fields(data["coverage"], ("universe", "source", "survivorship_limitations", "excluded_deals"))
    for k in ("universe", "source", "survivorship_limitations"):
        string(data["coverage"][k])
    for excluded in items(data["coverage"]["excluded_deals"], False):
        fields(excluded, ("deal_id", "reason"))
        string(excluded["deal_id"])
        string(excluded["reason"])
    sessions = items(data["sessions"])
    dates = []
    for row in sessions:
        fields(row, ("date", "benchmark", "marks"))
        dates.append(day(row["date"]))
        positive(row["benchmark"])
        if not isinstance(row["marks"], dict):
            raise ValueError("marks must be an object")
        for k, value in row["marks"].items():
            string(k)
            num(value, 0)
    if len(dates) < 3 or dates != sorted(set(dates)):
        raise ValueError("At least three unique, ascending sessions required")
    if frozen.date() >= dates[0]:
        raise ValueError("Policy must be frozen before the first sample date")
    fields(data["splits"], ("train_end", "validation_end"))
    train_end, validation_end = day(data["splits"]["train_end"]), day(data["splits"]["validation_end"])
    if train_end not in dates or validation_end not in dates or not dates[0] <= train_end < validation_end < dates[-1]:
        raise ValueError("Train, validation and test must be nonempty chronological segments")
    trades, ordered = {}, []
    for t in items(data["trades"], False):
        fields(t, ("deal_id", "source_url", "source_at", "signal_at", "entry_at", "entry_price", "exit_date", "exit_price", "outcome", "allocation"))
        key = string(t["deal_id"])
        string(t["source_url"])
        if key in trades:
            raise ValueError("Only one position per deal_id is supported")
        source, signal, entry = timestamp(t["source_at"]), timestamp(t["signal_at"]), timestamp(t["entry_at"])
        if not source <= signal < entry or frozen > signal:
            raise ValueError("Require frozen policy and source available by signal, strictly before entry")
        start, end = entry.date(), day(t["exit_date"]) if t["exit_date"] is not None else None
        if start not in dates or end is not None and (end not in dates or end <= start):
            raise ValueError("Entry/exit must be sample sessions; exit must follow entry")
        if t["outcome"] not in {"completed", "failed", "withdrawn", "unresolved"}:
            raise ValueError("Unsupported outcome")
        if (end is None) != (t["outcome"] == "unresolved"):
            raise ValueError("Unresolved deals must have null exit_date; resolved deals require settlement/exit date")
        positive(t["entry_price"])
        if end is None and t["exit_price"] is not None:
            raise ValueError("Unresolved deals require null exit_price")
        if end is not None:
            num(t["exit_price"], 0)
        positive(t["allocation"])
        for d, row in zip(dates, sessions):
            if start <= d and (end is None or d <= end) and key not in row["marks"]:
                raise ValueError(f"Missing mark for {key} on {d}; no forward fill or outcome-based deletion")
        trades[key] = dict(t, start=start, end=end)
        ordered.append(key)
    if any(set(row["marks"]) - trades.keys() for row in sessions):
        raise ValueError("Marks contain unknown deal IDs")

    cash, live, curve, completed, total_fees = capital, {}, [], [], 0.0
    for index, (d, row) in enumerate(zip(dates, sessions)):
        if index:
            cash *= (1 + cash_rate) ** ((d - dates[index - 1]).days / 365)
        for key in list(live):
            if trades[key]["end"] == d:
                position = live.pop(key)
                proceeds = position["shares"] * trades[key]["exit_price"]
                fee = proceeds * exit_fee
                cash += proceeds - fee
                total_fees += fee
                completed.append({"deal_id": key, "outcome": trades[key]["outcome"],
                                  "net_pnl": proceeds - fee - position["allocated"],
                                  "return_on_allocated_capital": (proceeds - fee) / position["allocated"] - 1})
        # Use prior-session marks: today's closing marks are unavailable at an intraday entry.
        # Settled exits above are assumed cash-available before this session's entries.
        prior_marks = sessions[index - 1]["marks"] if index else {}
        pre_nav = cash + sum(p["shares"] * prior_marks[k] for k, p in live.items())
        for key in ordered:
            trade = trades[key]
            if trade["start"] != d:
                continue
            allocated = trade["allocation"]
            if allocated > max_fraction * pre_nav + 1e-8:
                raise ValueError(f"{key}: allocation exceeds pre-entry NAV concentration limit")
            if allocated > cash + 1e-8:
                raise ValueError(f"{key}: insufficient settled capital; overlapping deals cannot reuse cash")
            shares = allocated / (trade["entry_price"] * (1 + entry_fee))
            fee = shares * trade["entry_price"] * entry_fee
            live[key] = {"shares": shares, "allocated": allocated}
            cash = max(0.0, cash - allocated)
            total_fees += fee
        exposure = sum(p["shares"] * row["marks"][k] for k, p in live.items())
        curve.append({"date": row["date"], "nav": cash + exposure, "cash": cash,
                      "long_market_value": exposure, "open_deals": len(live), "benchmark": row["benchmark"]})
    segments, previous_nav, previous_benchmark = {}, capital, sessions[0]["benchmark"]
    for name, selected in (("train", [r for r in curve if day(r["date"]) <= train_end]),
                           ("validation", [r for r in curve if train_end < day(r["date"]) <= validation_end]),
                           ("test", [r for r in curve if day(r["date"]) > validation_end])):
        segments[name] = metrics(selected, previous_nav, previous_benchmark)
        previous_nav, previous_benchmark = selected[-1]["nav"], selected[-1]["benchmark"]
    return result("event_backtest_result/v1", data, curve=curve,
                  summary=metrics(curve, capital, sessions[0]["benchmark"]), segments=segments,
                  total_transaction_cost=total_fees, resolved_trades=completed,
                  unresolved_deals=sorted(live),
                  outcome_counts={v: sum(t["outcome"] == v for t in trades.values())
                                  for v in ("completed", "failed", "withdrawn", "unresolved")},
                  warnings=["Replay of supplied historical decisions, not proof of an unbiased opportunity universe or automatic strategy discovery.",
                            "Fully funded long-only positions in one currency, fractional shares, no leverage or short leg.",
                            "Allocation includes entry costs; exit_date is the cash-available settlement/exit date. Marks must include distributions consistently.",
                            "Benchmark is a supplied total-return series. Costs include user-assumed fees/slippage; liquidity and taxes are not inferred.",
                            "Signals precede execution; validate original source availability, selection and sizing against archived point-in-time records.",
                            "Segments report a frozen-policy replay, not model fitting or cross-validation; holdings continue across split boundaries.",
                            "No carry-forward for missing marks; unresolved deals remain marked in NAV. Drawdown is observed only at supplied sessions."])


if __name__ == "__main__":
    cli({"backtest": backtest})
