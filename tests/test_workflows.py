from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "plugins" / "apac-equity-desk" / "scripts"
FIXTURES = Path(__file__).parent / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from ah_premium import calculate_ah_premiums
from breadth import calculate_breadth
from fact_check import audit
from market_snapshot import build_snapshot
from movers import find_movers
from news_cluster import cluster_news
from relative_moves import calculate_relative_moves
from render_market_color import render as render_color
from render_market_wrap import render as render_wrap


def fixture(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class CalculationTests(unittest.TestCase):
    def test_snapshot_and_relative_move(self):
        quotes = fixture("quotes.json")
        snapshot = build_snapshot(quotes, "2026-09-18T15:00:00+08:00")
        catl = snapshot["rows"][0]
        self.assertAlmostEqual(catl["pct_change"], -4.0)
        self.assertAlmostEqual(catl["volume_ratio"], 2.4)
        relative = calculate_relative_moves(quotes)[0]
        # Peers exclude CATL itself: median(-3.0, -2.0) = -2.5.
        self.assertAlmostEqual(relative["peer_median_pct"], -2.5)
        self.assertAlmostEqual(relative["relative_to_peer_ppt"], -1.5)
        self.assertEqual(relative["peer_count"], 2)

    def test_breadth_and_multi_signal_mover(self):
        quotes = fixture("quotes.json")
        breadth = calculate_breadth(quotes)["groups"]["CN"]
        self.assertEqual((breadth["advancers"], breadth["decliners"]), (0, 3))
        movers = find_movers(quotes)
        self.assertEqual(movers[0]["symbol"], "300750.SZ")
        self.assertGreaterEqual(movers[0]["signal_count"], 3)

    def test_ah_premium_and_news_deduplication(self):
        premium = calculate_ah_premiums(fixture("ah_pairs.json"))[0]
        self.assertAlmostEqual(premium["ah_premium_pct"], 3.68, places=2)
        clusters = cluster_news(fixture("news.json"), threshold=0.35)
        self.assertEqual(len(clusters), 2)
        self.assertEqual(max(cluster["article_count"] for cluster in clusters), 2)


class PriorityWorkflowTests(unittest.TestCase):
    def test_market_color_is_draft_and_calibrates_chatter(self):
        output = render_color(fixture("market_color_pack.json"))
        self.assertTrue(output.startswith("DRAFT — HUMAN APPROVAL REQUIRED"))
        self.assertIn("underperforming its peer basket by 1.5ppt", output)
        self.assertIn("Unconfirmed", output)
        self.assertIn("Watch:", output)

    def test_market_wrap_covers_six_focus_markets(self):
        output = render_wrap(fixture("market_wrap_pack.json"))
        for market in ("China", "Hong Kong", "Japan", "Korea", "Australia", "Singapore"):
            self.assertIn(f"{market} —", output)
        self.assertIn("Tomorrow:", output)
        self.assertIn("Data gaps:", output)

    def test_fact_checker_blocks_level4_causality(self):
        result = audit(fixture("claims.json"))
        self.assertEqual(result["status"], "block")
        self.assertIn("level4_causality", {item["code"] for item in result["findings"]})


if __name__ == "__main__":
    unittest.main()
