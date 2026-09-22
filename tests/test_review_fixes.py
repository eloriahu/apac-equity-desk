"""Regression tests for the 0.3.0 review fixes and new helpers."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "plugins" / "apac-equity-desk" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from breadth import calculate_breadth
from evidence_score import score_drivers
from fact_check import audit
from market_snapshot import build_snapshot
from movers import find_movers
from news_cluster import cluster_news
from relative_moves import calculate_relative_moves
import session_clock
from session_clock import load_calendar, market_status


def row(symbol, last, prev=100, **extra):
    return {"symbol": symbol, "market": "CN", "sector": "S", "last": last, "prev_close": prev, **extra}


class RelativeMoveTests(unittest.TestCase):
    def test_peer_median_excludes_the_stock_itself(self):
        result = calculate_relative_moves([row("A", 90), row("B", 100)])
        self.assertAlmostEqual(result[0]["relative_to_peer_ppt"], -10.0)

    def test_lone_stock_has_no_peer_spread(self):
        result = calculate_relative_moves([row("A", 90)])[0]
        self.assertIsNone(result["peer_median_pct"])
        self.assertIsNone(result["relative_to_peer_ppt"])
        self.assertEqual(result["peer_count"], 0)

    def test_supplied_peer_median_is_respected(self):
        result = calculate_relative_moves([row("A", 90, peer_median_pct=-1.0)])[0]
        self.assertAlmostEqual(result["relative_to_peer_ppt"], -9.0)


class CsvInputTests(unittest.TestCase):
    def test_blank_last_falls_back_to_close(self):
        csv_row = {"symbol": "A", "market": "CN", "last": "", "close": "105", "prev_close": "100"}
        snapshot = build_snapshot([csv_row], "2026-09-18T15:00:00+08:00")
        self.assertAlmostEqual(snapshot["rows"][0]["pct_change"], 5.0)
        self.assertEqual(snapshot["data_gaps"], [])
        self.assertEqual(calculate_breadth([csv_row])["groups"]["CN"]["advancers"], 1)

    def test_missing_both_prices_is_a_gap(self):
        snapshot = build_snapshot([{"symbol": "A", "market": "CN", "last": "", "prev_close": "100"}], "x")
        self.assertEqual(snapshot["data_gaps"], ["A: missing last/close"])

    def test_text_booleans_count_as_signals(self):
        movers = find_movers([row("A", "96", "100", fresh_announcement="True")])
        self.assertEqual(len(movers), 1)
        self.assertIn("fresh_announcement", movers[0]["signals"])
        self.assertEqual(find_movers([row("A", "96", "100", fresh_announcement="false")]), [])
        self.assertEqual(len(find_movers([row("A", "96", "100", fresh_announcement="1.0")])), 1)


class NewsClusterTests(unittest.TestCase):
    def test_earliest_uses_instants_not_strings(self):
        clusters = cluster_news([
            {"id": "a", "title": "Alpha beta gamma delta", "source": "X", "published_at": "2026-09-18T02:00:00Z"},
            {"id": "b", "title": "Alpha beta gamma delta", "source": "Y", "published_at": "2026-09-18T09:00:00+08:00"},
        ])
        self.assertEqual(clusters[0]["earliest_published_at"], "2026-09-18T09:00:00+08:00")

    def test_undated_articles_sort_last_and_are_listed(self):
        clusters = cluster_news([
            {"id": "a", "title": "Alpha beta gamma delta", "source": "X"},
            {"id": "b", "title": "Alpha beta gamma delta", "source": "Y", "published_at": "2026-09-18T09:00:00+08:00"},
        ])
        self.assertEqual(clusters[0]["article_ids"], ["b", "a"])
        self.assertEqual(clusters[0]["undated_article_ids"], ["a"])


class FactCheckTests(unittest.TestCase):
    SOURCE = {"id": "s1", "url": "https://example.com/a", "evidence_level": 1, "published_at": "2026-09-18T09:00:00+08:00"}

    def bundle(self, claim, source=None):
        return {"as_of": "2026-09-18T10:00:00+08:00", "claims": [claim], "sources": [source or self.SOURCE]}

    def codes(self, result):
        return {item["code"] for item in result["findings"]}

    def test_clean_bundle_passes(self):
        self.assertEqual(audit(self.bundle({"id": "c1", "source_ids": ["s1"], "confirmed": True}))["status"], "pass")

    def test_string_source_id_is_one_id(self):
        self.assertEqual(audit(self.bundle({"id": "c1", "source_ids": "s1"}))["status"], "pass")

    def test_source_dated_after_as_of_blocks(self):
        future = dict(self.SOURCE, published_at="2026-09-18T11:00:00+08:00")
        result = audit(self.bundle({"id": "c1", "source_ids": ["s1"]}, future))
        self.assertEqual(result["status"], "block")
        self.assertIn("source_after_as_of", self.codes(result))

    def test_causal_claim_without_evidence_level_needs_revision(self):
        unlevelled = {key: value for key, value in self.SOURCE.items() if key != "evidence_level"}
        result = audit(self.bundle({"id": "c1", "source_ids": ["s1"], "causal": True}, unlevelled))
        self.assertIn("unknown_evidence_level", self.codes(result))

    def test_material_move_requires_driver_assessment_and_mechanism(self):
        result = audit(self.bundle({"id": "c1", "source_ids": ["s1"], "movement": True}))
        self.assertEqual(result["status"], "revise")
        self.assertLessEqual({"missing_driver_assessment", "missing_mechanism"}, self.codes(result))

    def test_unresolved_move_with_explanation_passes(self):
        result = audit(self.bundle({
            "id": "c1",
            "source_ids": ["s1"],
            "movement": True,
            "driver_status": "unresolved",
            "mechanism": "Two plausible catalysts fit the timing, but peer dispersion does not distinguish them.",
        }))
        self.assertEqual(result["status"], "pass")

    def test_naive_timestamp_is_flagged(self):
        naive = dict(self.SOURCE, published_at="2026-09-18T09:00:00")
        self.assertIn("invalid_timestamp", self.codes(audit(self.bundle({"id": "c1", "source_ids": ["s1"]}, naive))))

    def test_naive_as_of_is_flagged_not_silently_skipped(self):
        bundle = self.bundle({"id": "c1", "source_ids": ["s1"]})
        bundle["as_of"] = "2026-09-18T10:00:00"
        self.assertIn("invalid_as_of", self.codes(audit(bundle)))

    def test_numeric_source_id_does_not_crash(self):
        source = dict(self.SOURCE, id="5")
        self.assertEqual(audit(self.bundle({"id": "c1", "source_ids": 5}, source))["status"], "pass")

    def test_freshness_limit_uses_observation_time(self):
        source = dict(self.SOURCE, observed_at="2026-09-18T09:55:00+08:00", published_at="2026-09-17T09:00:00+08:00")
        result = audit(self.bundle({"id": "c1", "source_ids": ["s1"], "max_age_minutes": 10}, source))
        self.assertEqual(result["status"], "pass")

    def test_stale_live_evidence_blocks(self):
        source = dict(self.SOURCE, observed_at="2026-09-18T09:30:00+08:00")
        result = audit(self.bundle({"id": "c1", "source_ids": ["s1"], "max_age_minutes": 15}, source))
        self.assertEqual(result["status"], "block")
        self.assertIn("stale_evidence", self.codes(result))

    def test_freshness_without_a_timestamp_needs_revision(self):
        source = {key: value for key, value in self.SOURCE.items() if key != "published_at"}
        result = audit(self.bundle({"id": "c1", "source_ids": ["s1"], "max_age_minutes": 15}, source))
        self.assertIn("freshness_unverifiable", self.codes(result))

    def test_bad_freshness_limit_needs_revision(self):
        result = audit(self.bundle({"id": "c1", "source_ids": ["s1"], "max_age_minutes": -1}))
        self.assertIn("invalid_max_age", self.codes(result))

    def test_repeated_fact_metadata_conflicts_block(self):
        bundle = {
            "as_of": "2026-09-18T10:00:00+08:00",
            "sources": [self.SOURCE],
            "claims": [
                {"id": "c1", "source_ids": ["s1"], "fact_key": "close", "value": 100, "unit": "price", "currency": "JPY", "session": "2026-09-18"},
                {"id": "c2", "source_ids": ["s1"], "fact_key": "close", "value": 100, "unit": "percent", "currency": "USD", "session": "2026-09-17"},
            ],
        }
        result = audit(bundle)
        self.assertEqual(result["status"], "block")
        self.assertLessEqual({"unit_conflict", "currency_conflict", "session_conflict"}, self.codes(result))


class SessionClockTests(unittest.TestCase):
    CALENDAR = load_calendar()

    def status(self, market, stamp, calendar=None):
        instant = datetime.fromisoformat(stamp)
        return market_status(market, instant, calendar or self.CALENDAR)["status"]

    def test_tokyo_phases(self):
        # Friday 2026-09-18, Tokyo is UTC+9.
        self.assertEqual(self.status("JP", "2026-09-18T08:30:00+09:00"), "pre_open")
        self.assertEqual(self.status("JP", "2026-09-18T10:00:00+09:00"), "open")
        self.assertEqual(self.status("JP", "2026-09-18T12:00:00+09:00"), "lunch_break")
        self.assertEqual(self.status("JP", "2026-09-18T15:30:00+09:00"), "closed")

    def test_instant_is_converted_to_local_time(self):
        # 01:30 UTC is 09:30 in Hong Kong: the open, not pre-open.
        self.assertEqual(self.status("HK", "2026-09-18T01:30:00+00:00"), "open")

    def test_weekend_and_supplied_holiday(self):
        self.assertEqual(self.status("KR", "2026-09-19T10:00:00+09:00"), "weekend")
        calendar = dict(self.CALENDAR, holidays={"KR": {"closed": ["2026-09-18"]}})
        self.assertEqual(self.status("KR", "2026-09-18T10:00:00+09:00", calendar), "holiday")

    def test_half_day_closes_early(self):
        calendar = dict(self.CALENDAR, holidays={"HK": {"half_day": {"2026-12-24": "12:00"}}})
        self.assertEqual(self.status("HK", "2026-12-24T13:30:00+08:00", calendar), "closed")

    def test_early_close_before_first_session_is_closed_not_a_crash(self):
        calendar = dict(self.CALENDAR, holidays={"HK": {"half_day": {"2026-12-24": "09:30"}}})
        self.assertEqual(self.status("HK", "2026-12-24T10:00:00+08:00", calendar), "closed")

    def test_sydney_daylight_saving_fallback_without_tz_data(self):
        original = session_clock._zone
        session_clock._zone = lambda spec: None
        try:
            spec = self.CALENDAR["markets"]["AU"]
            winter = session_clock.local_time(spec, datetime.fromisoformat("2026-07-01T00:00:00+00:00"))
            summer = session_clock.local_time(spec, datetime.fromisoformat("2026-12-01T00:00:00+00:00"))
            self.assertEqual(winter.utcoffset().total_seconds() / 3600, 10)
            self.assertEqual(summer.utcoffset().total_seconds() / 3600, 11)
        finally:
            session_clock._zone = original

    def test_command_line(self):
        result = subprocess.run([sys.executable, str(SCRIPTS / "session_clock.py"), "--markets", "JP,SG", "--at", "2026-09-18T10:00:00+09:00"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([m["status"] for m in json.loads(result.stdout)["markets"]], ["open", "open"])


class EvidenceScoreTests(unittest.TestCase):
    def test_rubric_bands_and_ordering(self):
        scored = score_drivers([
            {"id": "chatter", "evidence_level": 4, "freshness": "new", "specificity": "security", "market_fit": "partial"},
            {"id": "filing", "evidence_level": 1, "freshness": 2, "specificity": 2, "market_fit": 2},
        ])
        self.assertEqual([(d["id"], d["score"], d["confidence"]) for d in scored], [("filing", 8, "high"), ("chatter", 5, "medium")])

    def test_unscored_dimension_counts_as_zero_and_is_reported(self):
        scored = score_drivers([{"id": "x", "evidence_level": 2, "freshness": 2, "specificity": 2}])[0]
        self.assertEqual((scored["score"], scored["unscored"]), (5, ["market_fit"]))

    def test_bad_evidence_levels_are_unscored_not_crashes(self):
        for level in ("nan", "inf", 1.9):
            scored = score_drivers([{"id": "x", "evidence_level": level, "freshness": 2, "specificity": 2, "market_fit": 2}])[0]
            self.assertEqual(scored["score_parts"]["authority"], None, level)


if __name__ == "__main__":
    unittest.main()
