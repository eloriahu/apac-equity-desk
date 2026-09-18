"""Calculate currency-adjusted A/H share premiums."""

from __future__ import annotations

from typing import Any

from common import load_data, number, parser, records, write_output


def calculate_ah_premiums(pairs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for pair in pairs:
        item = dict(pair)
        a_price, h_price, fx = number(pair.get("a_price_cny")), number(pair.get("h_price_hkd")), number(pair.get("hkd_per_cny"))
        item["a_price_hkd"] = a_price * fx if a_price is not None and fx is not None else None
        item["ah_premium_pct"] = ((a_price * fx / h_price) - 1) * 100 if None not in (a_price, h_price, fx) and h_price else None
        item["formula"] = "(a_price_cny * hkd_per_cny / h_price_hkd - 1) * 100"
        result.append(item)
    return result


if __name__ == "__main__":
    args = parser(__doc__).parse_args()
    write_output(calculate_ah_premiums(records(load_data(args.input))), args.output)
