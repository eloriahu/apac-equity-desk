import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1] / "plugins" / "apac-equity-desk"
sys.path.insert(0, str(ROOT / "scripts"))
from merger_arb import calculate


def fixture(name="cash-deal.json"):
    return json.loads((ROOT / "examples" / "event-driven" / name).read_text(encoding="utf-8"))


class MergerScenarios(unittest.TestCase):
    def zero_cost_pair(self):
        data = fixture()
        data["funding_rate"] = 0
        data["transaction_cost"] = 0
        data["scenarios"] = [data["scenarios"][0], data["scenarios"][2]]
        for s in data["scenarios"]:
            s.pop("probability")
        return data

    def test_cash_costs_can_erase_gross_spread(self):
        data = fixture()
        for s in data["scenarios"]:
            s["days"] = 365
        result = calculate(data)
        self.assertEqual(result["gross_spread_per_share"], 2)
        self.assertAlmostEqual(result["scenarios"][0]["net_pnl"], -2.02)
        self.assertLess(result["expected_net_pnl"], 0)

    def test_delay_increases_carry_and_lowers_return(self):
        rows = calculate(fixture())["scenarios"]
        self.assertGreater(rows[0]["net_pnl"], rows[1]["net_pnl"])
        self.assertAlmostEqual(rows[1]["financing_cost"], 2 * rows[0]["financing_cost"])

    def test_break_loss_is_signed_and_probability_is_optional(self):
        result = calculate(self.zero_cost_pair())
        self.assertEqual(result["scenarios"][1]["net_pnl"], -18)
        self.assertIsNone(result["expected_net_pnl"])
        self.assertAlmostEqual(result["two_state_net_pnl_breakeven_probability"], 0.9)

    def test_expected_pnl_uses_signed_loss(self):
        data = self.zero_cost_pair()
        data["scenarios"][0]["probability"] = 0.9
        data["scenarios"][1]["probability"] = 0.1
        self.assertAlmostEqual(calculate(data)["expected_net_pnl"], 0)

    def test_mixed_full_hedge_cancels_close_acquirer_move(self):
        for exit_price in [0, 50, 80, 100, 150]:
            data = fixture("mixed-deal.json")
            data["scenarios"][0]["acquirer_exit"] = exit_price
            self.assertAlmostEqual(calculate(data)["scenarios"][0]["price_pnl"], 2)

    def test_stock_only_and_partial_hedge(self):
        data = fixture("mixed-deal.json")
        data.update(structure="fixed_ratio_stock", cash=0, target_price=48)
        self.assertEqual(calculate(data)["scenarios"][0]["price_pnl"], 2)
        data["hedge_ratio"] = 0.25
        self.assertEqual(calculate(data)["scenarios"][0]["price_pnl"], -3)

    def test_break_both_legs_and_dividends(self):
        data = fixture("mixed-deal.json")
        data["scenarios"][1]["acquirer_dividend"] = 2
        row = calculate(data)["scenarios"][1]
        self.assertEqual(row["price_pnl"], -28)
        self.assertEqual(row["net_dividends"], -1)

    def test_dividend_offer_adjustment_not_double_counted(self):
        data = self.zero_cost_pair()
        data["scenarios"][0].update(target_dividend=1, cash_adjustment=-1)
        self.assertEqual(calculate(data)["scenarios"][0]["net_pnl"], 2)

    def test_borrow_rebate_and_capital_denominator(self):
        data = fixture("mixed-deal.json")
        data["scenarios"][0]["days"] = 365
        row = calculate(data)["scenarios"][0]
        self.assertEqual(row["borrow_cost"], 1)
        self.assertEqual(row["rebate_income"], 0.5)
        self.assertAlmostEqual(row["net_pnl"], -1.32)
        self.assertAlmostEqual(row["return_on_capital"], -1.32 / 90)

    def test_breakeven_not_clipped(self):
        data = self.zero_cost_pair()
        data["transaction_cost"] = 3
        self.assertAlmostEqual(calculate(data)["two_state_net_pnl_breakeven_probability"], 1.05)

    def test_equal_outcomes_and_loss_over_capital(self):
        data = self.zero_cost_pair()
        data["scenarios"][1]["target_exit"] = 100
        self.assertIsNone(calculate(data)["two_state_net_pnl_breakeven_probability"])
        data["scenarios"][1]["target_exit"] = 0
        data["capital_base"] = 10
        self.assertIsNone(calculate(data)["scenarios"][1]["compounded_annualized_return"])

    def test_invalid_inputs(self):
        invalid = [("target_price", 0), ("capital_base", 0), ("funding_rate", -1),
                   ("target_price", float("nan")), ("cash", True), ("hedge_ratio", 1),
                   ("structure", "collar"), ("cvr", 5)]
        for key, value in invalid:
            with self.subTest(key=key, value=value):
                data = fixture()
                data[key] = value
                with self.assertRaises(ValueError):
                    calculate(data)
        for value in [0, -10, 1.5, float("inf")]:
            data = fixture()
            data["scenarios"][0]["days"] = value
            with self.assertRaises(ValueError):
                calculate(data)

    def test_missing_or_invalid_probability_and_cost(self):
        for key, value in [("probability", 0.5), ("probability", 2), ("additional_cost", -1)]:
            data = fixture()
            data["scenarios"][0][key] = value
            with self.assertRaises(ValueError):
                calculate(data)
        for key in ["probability", "target_dividend"]:
            data = fixture()
            del data["scenarios"][0][key]
            with self.assertRaises(ValueError):
                calculate(data)

    def test_input_is_preserved(self):
        data = fixture()
        original = copy.deepcopy(data)
        calculate(data)
        self.assertEqual(data, original)

    def test_cli_json_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "result.json"
            command = [sys.executable, str(ROOT / "scripts" / "merger_arb.py"),
                       str(ROOT / "examples" / "event-driven" / "cash-deal.json"), "--output", str(output)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(json.loads(output.read_text())["schema"], "merger_arb_result/v1")
            second = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(second.returncode, 2)


if __name__ == "__main__":
    unittest.main()
