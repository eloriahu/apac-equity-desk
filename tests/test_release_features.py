from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "plugins" / "apac-equity-desk" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from earnings_surprise import calculate_surprises
from pack_delta import compare_packs
from pack_readiness import assess_pack
from research_ledger import update_ledger
from topic_radar import rank_topics
from transmission_map import build_map


class TopicRadarTests(unittest.TestCase):
    def test_ranks_broad_relative_sector_move_without_claiming_causation(self):
        data = {
            "as_of": "2026-09-21T11:00:00+08:00",
            "market": "HK",
            "benchmark_pct": 0.2,
            "quotes": [
                {"symbol": "A", "name": "A", "sector": "Semiconductors", "pct_change": 4.0, "volume_ratio": 2.0},
                {"symbol": "B", "name": "B", "sector": "Semiconductors", "pct_change": 3.0, "volume_ratio": 1.8},
                {"symbol": "C", "name": "C", "sector": "Semiconductors", "pct_change": 2.0, "volume_ratio": 1.6},
                {"symbol": "D", "name": "D", "sector": "Banks", "pct_change": 0.3},
                {"symbol": "E", "name": "E", "sector": "Banks", "pct_change": -0.1},
            ],
            "news": [{"id": "n1", "published_at": "2026-09-21T10:00:00+08:00", "sectors": ["Semiconductors"], "symbols": []}],
        }
        result = rank_topics(data)
        self.assertEqual(result["topics"][0]["sector"], "Semiconductors")
        self.assertEqual(result["topics"][0]["causal_status"], "not_assessed")
        self.assertEqual(result["topics"][0]["observation"]["breadth_pct"], 100.0)


class ReadinessAndDeltaTests(unittest.TestCase):
    def test_blocks_stale_live_pack(self):
        pack = {
            "as_of": "2026-09-21T11:00:00+08:00",
            "market": "HK",
            "quotes": [{"symbol": "A"}, {"symbol": "B"}, {"symbol": "C"}],
            "freshness": [{"id": "quotes", "observed_at": "2026-09-21T09:00:00+08:00", "max_age_minutes": 30}],
        }
        self.assertEqual(assess_pack(pack, "topic-radar")["status"], "block")

    def test_delta_matches_list_items_by_symbol(self):
        result = compare_packs({"quotes": [{"symbol": "A", "pct": 1.0}]}, {"quotes": [{"symbol": "A", "pct": 2.0}]})
        self.assertEqual(result["counts"]["changed"], 1)
        self.assertEqual(result["changes"][0]["path"], "quotes.A.pct")


class EarningsTransmissionLedgerTests(unittest.TestCase):
    def test_earnings_surprise_and_unit_guard(self):
        rows = calculate_surprises([
            {"metric": "EPS", "actual": 1.1, "consensus": 1.0},
            {"metric": "Revenue", "actual": 10, "consensus": 9, "actual_unit": "bn", "consensus_unit": "mn"},
        ])
        self.assertEqual(rows[0]["result"], "beat")
        self.assertEqual(rows[1]["result"], "unscored")

    def test_transmission_marks_unsupported_edges(self):
        result = build_map({
            "event_node": "event",
            "nodes": [{"id": "event"}, {"id": "stock"}],
            "edges": [{"from": "event", "to": "stock", "mechanism": "cost", "confidence": 0.7, "source_ids": []}],
        })
        self.assertFalse(result["paths"][0]["supported"])

    def test_ledger_preserves_history(self):
        ledger = {"theses": [{"id": "t1", "statement": "test", "history": []}]}
        updated = update_ledger({"ledger": ledger, "observation": {"thesis_id": "t1", "verdict": "weakened", "reason": "counterevidence", "observed_at": "2026-09-21T12:00:00+08:00"}})
        self.assertEqual(updated["theses"][0]["status"], "weakened")
        self.assertEqual(len(updated["theses"][0]["history"]), 1)


class CodexAgentTests(unittest.TestCase):
    def test_project_agents_are_present_and_safe(self):
        import tomllib

        agents = sorted((ROOT / ".codex" / "agents").glob("*.toml"))
        self.assertEqual(len(agents), 5)
        for path in agents:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["name"], path.stem)
            self.assertIn("never", data["developer_instructions"].lower())
            self.assertNotIn("submit_order", data["developer_instructions"])


if __name__ == "__main__":
    unittest.main()
