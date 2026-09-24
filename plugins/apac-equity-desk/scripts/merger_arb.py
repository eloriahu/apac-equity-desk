#!/usr/bin/env python3
"""Offline cash/fixed-ratio merger scenarios; monetary outputs per target share."""
import argparse
import json
import math
from pathlib import Path


def number(data, key, minimum=None):
    value = data.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{key} must be an explicit finite number")
    if minimum is not None and value < minimum:
        raise ValueError(f"{key} must be >= {minimum}")
    return float(value)


def positive(data, key):
    value = number(data, key, 0)
    if value == 0:
        raise ValueError(f"{key} must be > 0")
    return value


def calculate(data):
    if not isinstance(data, dict) or data.get("schema") != "merger_arb/v1":
        raise ValueError("schema must be merger_arb/v1")
    allowed = {"schema", "deal_id", "as_of", "currency", "structure", "target_price",
               "cash", "exchange_ratio", "acquirer_price", "hedge_ratio", "capital_base",
               "financed_amount", "funding_rate", "borrow_rate", "rebate_rate",
               "transaction_cost", "scenarios", "notes", "sources"}
    extra = set(data) - allowed
    if extra:
        raise ValueError(f"Unsupported input fields: {sorted(extra)}")
    for key in ("deal_id", "as_of", "currency"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f"{key} must be a nonempty string")
    if data.get("structure") not in {"cash", "fixed_ratio_stock", "fixed_ratio_mixed"}:
        raise ValueError("Only cash and fixed-ratio stock/mixed structures are supported")
    target = positive(data, "target_price")
    cash = number(data, "cash", 0)
    ratio = number(data, "exchange_ratio", 0)
    acquirer = number(data, "acquirer_price", 0)
    hedge = number(data, "hedge_ratio", 0)
    capital = positive(data, "capital_base")
    financed = number(data, "financed_amount", 0)
    funding = number(data, "funding_rate", 0)
    borrow = number(data, "borrow_rate", 0)
    rebate = number(data, "rebate_rate")
    transaction = number(data, "transaction_cost", 0)
    if hedge > ratio:
        raise ValueError("hedge_ratio must be between zero and the contractual exchange_ratio")
    structure = data["structure"]
    if structure == "cash" and (ratio != 0 or cash <= 0 or acquirer != 0):
        raise ValueError("Cash deals require positive cash, zero ratio and zero acquirer_price")
    if structure != "cash" and (ratio <= 0 or acquirer <= 0):
        raise ValueError("Stock/mixed deals require positive ratio and acquirer_price")
    if structure == "fixed_ratio_stock" and cash != 0:
        raise ValueError("All-stock deals require zero cash")
    if structure == "fixed_ratio_mixed" and cash <= 0:
        raise ValueError("Mixed deals require positive cash")

    scenarios = data.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("scenarios must be a nonempty list")
    probabilities = []
    output = []
    names = set()
    warnings = [
        "All amounts are per target share in one currency; FX risk is not modeled.",
        "Static hedge and opening short notional for borrow/rebate; actual path and margin may differ.",
        "Capital denominator and financing base are user inputs, not broker margin estimates.",
        "Annualization is a scenario convention, not a forecast or expected portfolio return.",
    ]
    if transaction == 0 or funding == 0 or (hedge > 0 and borrow == 0):
        warnings.append("One or more cost assumptions are explicitly zero; verify before use.")
    for s in scenarios:
        if not isinstance(s, dict):
            raise ValueError("Each scenario must be an object")
        permitted = {"name", "outcome", "days", "probability", "target_exit",
                     "acquirer_exit", "cash_adjustment", "target_dividend",
                     "acquirer_dividend", "additional_cost", "rationale"}
        if set(s) - permitted:
            raise ValueError(f"Unsupported scenario fields: {sorted(set(s) - permitted)}")
        name = s.get("name")
        if not isinstance(name, str) or not name.strip() or name in names:
            raise ValueError("Each scenario needs a unique nonempty name")
        names.add(name)
        outcome = s.get("outcome")
        if outcome not in {"close", "break"}:
            raise ValueError("outcome must be close or break")
        days = positive(s, "days")
        if not days.is_integer():
            raise ValueError("days must be integer calendar days to settlement/exit")
        probability = None
        if "probability" in s:
            probability = number(s, "probability", 0)
            if probability > 1:
                raise ValueError("probability must be <= 1")
        probabilities.append(probability)
        acquirer_exit = number(s, "acquirer_exit", 0)
        adjustment = number(s, "cash_adjustment")
        target_dividend = number(s, "target_dividend", 0)
        acquirer_dividend = number(s, "acquirer_dividend", 0)
        additional = number(s, "additional_cost", 0)
        if structure == "cash" and (acquirer_exit != 0 or acquirer_dividend != 0):
            raise ValueError("Cash scenarios require zero acquirer_exit and acquirer_dividend")
        if outcome == "close":
            if "target_exit" in s:
                raise ValueError("close target value is computed from consideration, not target_exit")
            if cash + adjustment < 0:
                raise ValueError("Adjusted cash consideration cannot be negative")
            exit_value = cash + adjustment + ratio * acquirer_exit
        else:
            if adjustment != 0:
                raise ValueError("Break scenarios require zero cash_adjustment; use target_exit")
            exit_value = number(s, "target_exit", 0)
        fraction = days / 365
        financing_cost = financed * funding * fraction
        borrow_cost = hedge * acquirer * borrow * fraction
        rebate_income = hedge * acquirer * rebate * fraction
        price_pnl = exit_value - target + hedge * (acquirer - acquirer_exit)
        dividends = target_dividend - hedge * acquirer_dividend
        net_cost = financing_cost + borrow_cost + transaction + additional - rebate_income
        net_pnl = price_pnl + dividends - net_cost
        holding_return = net_pnl / capital
        compounded = None
        if holding_return >= -1:
            try:
                compounded = (1 + holding_return) ** (365 / days) - 1
                if not math.isfinite(compounded):
                    compounded = None
            except OverflowError:
                compounded = None
        if compounded is None:
            warnings.append(f"{name}: compounded annualization undefined or overflowed; left null.")
        output.append({"name": name, "outcome": outcome, "days": int(days),
                       "probability": probability, "target_exit_value": exit_value,
                       "price_pnl": price_pnl, "net_dividends": dividends,
                       "financing_cost": financing_cost, "borrow_cost": borrow_cost,
                       "rebate_income": rebate_income, "transaction_cost": transaction,
                       "additional_cost": additional, "net_pnl": net_pnl,
                       "return_on_capital": holding_return,
                       "simple_annualized_return": holding_return * 365 / days,
                       "compounded_annualized_return": compounded})
    supplied = [p for p in probabilities if p is not None]
    if supplied and (len(supplied) != len(scenarios) or not math.isclose(sum(supplied), 1, abs_tol=1e-9, rel_tol=0)):
        raise ValueError("Supply probabilities for all scenarios summing to 1, or omit all")
    expected = sum(s["probability"] * s["net_pnl"] for s in output) if supplied else None
    threshold = None
    if len(output) == 2 and {s["outcome"] for s in output} == {"close", "break"}:
        success = next(s["net_pnl"] for s in output if s["outcome"] == "close")
        failure = next(s["net_pnl"] for s in output if s["outcome"] == "break")
        if success != failure:
            threshold = -failure / (success - failure)
            if not 0 <= threshold <= 1:
                warnings.append("Break-even probability outside [0,1]; no interior two-state break-even. Not clipped.")
    consideration = cash + ratio * acquirer
    return {"schema": "merger_arb_result/v1", "status": "DRAFT — HUMAN APPROVAL REQUIRED", "deal_id": data["deal_id"],
            "as_of": data["as_of"], "currency": data["currency"], "inputs": data,
            "indicative_consideration": consideration,
            "gross_spread_per_share": consideration - target,
            "gross_spread_on_target": (consideration - target) / target,
            "capital_base": capital, "scenarios": output,
            "expected_net_pnl": expected,
            "expected_return_on_capital": expected / capital if expected is not None else None,
            "two_state_net_pnl_breakeven_probability": threshold,
            "warnings": warnings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8-sig"))
        result = calculate(data)
        rendered = json.dumps(result, indent=2, allow_nan=False) + "\n"
        if args.output:
            # Never overwrite a research snapshot accidentally.
            with args.output.open("x", encoding="utf-8") as handle:
                handle.write(rendered)
        else:
            print(rendered, end="")
    except (OSError, ValueError, OverflowError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    main()
