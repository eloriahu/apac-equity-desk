"""Economic identities, point-in-time controls and state transitions for event research."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy

PLUGIN = Path(__file__).resolve().parents[1] / "plugins" / "apac-equity-desk"
sys.path.insert(0, str(PLUGIN / "scripts"))
from event_tools import radar, document, sensitivity, models, alerts
from event_backtest import backtest


def fixture(name):
    return json.loads((PLUGIN / "examples" / "event-driven" / f"{name}.json").read_text(encoding="utf-8"))


class RadarTests(unittest.TestCase):
    def test_deduplicates_without_counting_wire_copy_as_verification(self):
        r = radar(fixture("radar"))
        self.assertEqual(len(r["candidates"]), 1)
        self.assertEqual(len(r["candidates"][0]["evidence"]), 2)
        self.assertEqual(r["excluded"][0]["reason"], "duplicate_record")

    def test_future_observation_excluded_even_when_publication_is_old(self):
        d = fixture("radar")
        for r in d["records"]:
            r["observed_at"] = "2026-09-25T00:00:00+08:00"
        self.assertEqual(radar(d)["candidates"], [])

    def test_secondary_only_remains_unverified(self):
        d = fixture("radar"); d["records"] = [d["records"][1]]
        self.assertEqual(radar(d)["candidates"][0]["classification"], "needs_review")

    def test_conflicting_concurrent_primary_terms_preserved(self):
        d = fixture("radar"); changed = deepcopy(d["records"][0])
        changed["terms"]["cash"] = 105
        d["records"].append(changed)
        self.assertTrue(radar(d)["candidates"][0]["concurrent_conflict"])

    def test_outside_market_and_time_window_reported(self):
        d = fixture("radar"); d["markets"] = ["JP"]
        self.assertEqual(radar(d)["candidates"], [])
        d = fixture("radar"); d["since"] = d["as_of"]
        self.assertEqual(radar(d)["candidates"], [])


class DocumentTests(unittest.TestCase):
    def test_omission_is_not_contractual_deletion(self):
        terms = {t["term"]: t for t in document(fixture("documents"))["terms"]}
        self.assertEqual(terms["long_stop"]["change"], "not_observed_in_new_document")
        self.assertEqual(terms["cash"]["change"], "value_changed")
        self.assertEqual(terms["financing"]["change"], "unchanged")

    def test_evidence_gap_and_citation_change_distinguished(self):
        d = fixture("documents")
        d["after"]["terms"]["cash"] = dict(value=None, status="unknown", locator="missing appendix")
        cash = next(t for t in document(d)["terms"] if t["term"] == "cash")
        self.assertEqual(cash["change"], "evidence_status_changed")

    def test_missing_locator_and_reversed_chronology_rejected(self):
        d = fixture("documents"); d["after"]["terms"]["cash"]["locator"] = ""
        with self.assertRaises(ValueError): document(d)
        d = fixture("documents"); d["before"], d["after"] = d["after"], d["before"]
        with self.assertRaises(ValueError): document(d)


class SensitivityTests(unittest.TestCase):
    def test_endpoints_equal_scenario_pnl(self):
        d = fixture("sensitivity"); d["close_probabilities"] = [0, 1]
        for row in sensitivity(d)["grid"]:
            expected = row["close_net_pnl"] if row["close_probability"] else row["break_net_pnl"]
            self.assertAlmostEqual(row["expected_net_pnl"], expected)

    def test_delay_reduces_ev_by_probability_weighted_funding(self):
        d = fixture("sensitivity"); d.update(close_probabilities=[.8],break_prices=[80],close_days=[90,180])
        a, b = sensitivity(d)["grid"]
        self.assertAlmostEqual(a["expected_net_pnl"] - b["expected_net_pnl"], .8 * 98 * .04 * 90 / 365)

    def test_breakeven_probability_produces_zero_net_ev(self):
        d = fixture("sensitivity"); d.update(close_probabilities=[.8],break_prices=[80],close_days=[90])
        p = sensitivity(d)["grid"][0]["two_state_net_pnl_breakeven_probability"]
        d["close_probabilities"] = [p]
        self.assertAlmostEqual(sensitivity(d)["grid"][0]["expected_net_pnl"], 0)

    def test_invalid_probabilities_and_three_states_rejected(self):
        d = fixture("sensitivity"); d["close_probabilities"] = [1.1]
        with self.assertRaises(ValueError): sensitivity(d)
        d = fixture("sensitivity"); d["base_deal"] = fixture("cash-deal")
        with self.assertRaises(ValueError): sensitivity(d)


class ModelTests(unittest.TestCase):
    def test_collar_uses_reference_price_and_separate_settlement_mark(self):
        r = models(fixture("models"))["scenarios"][0]["components"][1]
        self.assertEqual(r["exchange_ratio"], .5)
        self.assertEqual(r["payoff_in_component_currency"], 45)

    def test_collar_boundaries_use_explicit_contract_ratios(self):
        for ref, ratio in ((70,.625),(80,.625),(100,.5),(120,50/120),(140,50/120)):
            d = fixture("models"); d["scenarios"][0]["components"][1]["reference_price"] = ref
            self.assertAlmostEqual(models(d)["scenarios"][0]["components"][1]["exchange_ratio"], ratio)

    def test_cvr_discount_and_parent_probability_both_applied(self):
        d = fixture("models")
        d["scenarios"][0]["components"] = [d["scenarios"][0]["components"][2]]
        d["scenarios"][1]["components"][0]["amount"] = 0
        r = models(d)
        self.assertAlmostEqual(r["expected_net_present_value"], .85 * 5 * .4 / 1.05**2 - 60 - .2)

    def test_proration_keeps_residual_stake_value(self):
        d = fixture("proration"); d["discount_rate"] = 0
        self.assertAlmostEqual(models(d)["scenarios"][0]["consideration_pv"], .4*110 + .6*85)

    def test_fx_quote_is_base_currency_per_component_currency(self):
        d = fixture("proration"); d["discount_rate"] = 0
        d["scenarios"][0]["components"][0]["fx_to_base"] = .5
        self.assertAlmostEqual(models(d)["scenarios"][0]["consideration_pv"], 47.5)

    def test_bad_collars_and_unknown_components_rejected(self):
        d = fixture("models"); d["scenarios"][0]["components"][1]["floor"] = 121
        with self.assertRaises(ValueError): models(d)
        d = fixture("models"); d["scenarios"][0]["components"][0]["kind"] = "automatic_hedge"
        with self.assertRaises(ValueError): models(d)


class AlertTests(unittest.TestCase):
    def test_repeat_evaluation_does_not_duplicate(self):
        d = fixture("alerts"); r = alerts(d)
        self.assertEqual({e["kind"] for e in r["events"]}, {"status_changed", "spread_widened", "deadline_near"})
        d["state"] = r["next_state"]
        self.assertEqual(alerts(d)["events"], [])

    def test_baseline_cannot_claim_status_change(self):
        d = fixture("alerts"); d["previous"] = None
        r = alerts(d)
        self.assertTrue(r["baseline_created"])
        self.assertEqual([e["kind"] for e in r["events"]], ["deadline_near"])

    def test_staleness_clears_and_rearms(self):
        d = fixture("alerts"); d["previous"] = None; d["current"]["deadline"] = None
        d["as_of"] = "2026-09-25T10:00:00+08:00"
        r = alerts(d); self.assertEqual(r["events"][0]["kind"], "stale_snapshot")
        d["state"] = r["next_state"]; d["current"]["as_of"] = d["as_of"]
        r = alerts(d); self.assertEqual(r["events"], [])
        d["state"] = r["next_state"]; d["as_of"] = "2026-09-26T11:00:00+08:00"
        self.assertEqual(alerts(d)["events"][0]["kind"], "stale_snapshot")

    def test_future_snapshots_and_cross_deal_state_rejected(self):
        d = fixture("alerts"); d["current"]["as_of"] = "2026-09-30T00:00:00Z"
        with self.assertRaises(ValueError): alerts(d)
        d = fixture("alerts"); d["state"]["deal_id"] = "WRONG"
        with self.assertRaises(ValueError): alerts(d)

    def test_missing_prices_reported_and_terminal_deadlines_suppressed(self):
        d = fixture("alerts"); d["current"]["target_price"] = None
        self.assertIn("missing_price_or_consideration", {e["kind"] for e in alerts(d)["events"]})
        d["current"]["status"] = "settled"
        self.assertNotIn("deadline_near", {e["kind"] for e in alerts(d)["events"]})


class BacktestTests(unittest.TestCase):
    def test_cash_locked_losses_and_unresolved_positions_in_nav(self):
        d = fixture("backtest"); d["entry_cost_bps"] = d["exit_cost_bps"] = 0
        r = backtest(d)
        self.assertEqual(r["curve"][-1]["nav"], 970)
        self.assertEqual(r["curve"][2]["cash"], 100)
        self.assertEqual(r["unresolved_deals"], ["SYNTHETIC-C"])
        self.assertEqual(r["outcome_counts"]["failed"], 1)
        self.assertAlmostEqual(r["summary"]["return"], -.03)

    def test_costs_reduce_nav_by_entry_and_exit_fees(self):
        r = backtest(fixture("backtest"))
        expected = 100 + 300/1.001 + (300/1.001*1.1 + 300/1.001*.8)*.999
        self.assertAlmostEqual(r["curve"][-1]["nav"], expected)
        self.assertGreater(r["total_transaction_cost"], 0)

    def test_execution_price_separate_from_closing_mark(self):
        d = fixture("backtest"); d["trades"][0]["entry_price"] = 90
        self.assertGreater(backtest(d)["curve"][0]["nav"], 1000)

    def test_insufficient_cash_does_not_silently_overallocate(self):
        d = fixture("backtest"); d["max_trade_fraction"] = 1
        for t in d["trades"]: t["allocation"] = 600
        with self.assertRaisesRegex(ValueError, "insufficient settled capital"): backtest(d)

    def test_lookahead_signal_or_source_rejected(self):
        for field in ("signal_at", "source_at"):
            d = fixture("backtest"); d["trades"][0][field] = "2026-01-03T00:00:00+08:00"
            with self.assertRaises(ValueError): backtest(d)

    def test_same_day_closing_mark_cannot_expand_entry_limit(self):
        d = fixture("backtest"); d["max_trade_fraction"] = .35
        d["trades"][1]["allocation"] = 400
        d["sessions"][1]["marks"]["SYNTHETIC-A"] = 1000
        with self.assertRaisesRegex(ValueError, "concentration limit"): backtest(d)

    def test_missing_mark_and_future_policy_rejected(self):
        d = fixture("backtest"); del d["sessions"][2]["marks"]["SYNTHETIC-B"]
        with self.assertRaisesRegex(ValueError, "Missing mark"): backtest(d)
        d = fixture("backtest"); d["policy"]["frozen_at"] = "2026-01-03T00:00:00Z"
        with self.assertRaises(ValueError): backtest(d)

    def test_segment_returns_compound_to_whole_sample(self):
        r = backtest(fixture("backtest"))
        linked = 1
        for s in r["segments"].values(): linked *= 1 + s["return"]
        self.assertAlmostEqual(linked - 1, r["summary"]["return"])

    def test_future_outcome_labels_cannot_change_nav(self):
        d = fixture("backtest"); original = backtest(d)["curve"]
        d["trades"][0]["outcome"] = "withdrawn"
        self.assertEqual(backtest(d)["curve"], original)


class InterfaceTests(unittest.TestCase):
    def test_cli_refuses_overwriting_research_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "out.json"
            command = [sys.executable, str(PLUGIN / "scripts/event_tools.py"), "models",
                       str(PLUGIN / "examples/event-driven/models.json"), "--output", str(output)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            saved = output.read_bytes()
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertEqual(output.read_bytes(), saved)

    def test_all_examples_serialize_strict_json_with_inputs(self):
        for name, function in (("radar",radar),("documents",document),("sensitivity",sensitivity),
                               ("models",models),("proration",models),("alerts",alerts),("backtest",backtest)):
            data = fixture(name); r = function(data)
            json.dumps(r, allow_nan=False)
            self.assertEqual(r["inputs"], data)
            self.assertEqual(len(r["input_sha256"]), 64)

    def test_unknown_fields_and_naive_times_rejected(self):
        d = fixture("models"); d["guess_missing_costs"] = True
        with self.assertRaises(ValueError): models(d)
        d = fixture("radar"); d["as_of"] = "2026-09-24T09:00:00"
        with self.assertRaises(ValueError): radar(d)


if __name__ == "__main__":
    unittest.main()
