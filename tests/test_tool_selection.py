"""Exercise tool choices under realistic host/input failures, without paid calls."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "apac-equity-desk"
sys.path.insert(0, str(PLUGIN / "scripts"))
from tool_selection import select_tools


class ToolSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads(
            (PLUGIN / "references" / "tool-selection-evals.json").read_text(encoding="utf-8")
        )["cases"]
        cls.by_id = {case["id"]: case for case in cls.cases}

    def request(self, identity):
        return copy.deepcopy(self.by_id[identity]["request"])

    def test_task_specific_choices_and_fallbacks(self):
        for case in self.cases:
            with self.subTest(case=case["id"], question=case["prompt"]):
                before = copy.deepcopy(case["request"])
                result = select_tools(case["request"])
                self.assertEqual(result["status"], case["expected"]["status"])
                chosen = [row["selected"]["candidate"] if row["selected"] else None for row in result["needs"]]
                self.assertEqual(chosen, case["expected"]["selected"])
                self.assertFalse(result["research_complete"])
                self.assertEqual(before, case["request"])

    def test_one_question_keeps_multiple_tools_and_complementary_roles(self):
        request = self.request("multi-tool-earnings-question")
        result = select_tools(request)
        self.assertEqual(result["primary_workflow"], "earnings-review")
        self.assertEqual(len(result["needs"]), 6)
        by_id = {row["id"]: row for row in result["needs"]}
        self.assertEqual(by_id["extract-results-table"]["selected"]["candidate"], "docling")
        self.assertEqual(by_id["verify-original-page"]["selected"]["candidate"], "pdf-reader")
        self.assertEqual(by_id["extract-results-table"]["capability"], by_id["verify-original-page"]["capability"])
        self.assertTrue(all(row["selected"] for row in result["needs"]))

    def test_partial_failure_retains_successful_needs(self):
        request = self.request("financial-pdf")
        missing = self.request("missing-live-price")["needs"][0]
        missing["id"] = "market-reaction"
        request["needs"].append(missing)
        result = select_tools(request)
        self.assertEqual(result["status"], "limited")
        self.assertEqual(result["needs"][0]["selected"]["candidate"], "docling")
        self.assertIsNone(result["needs"][1]["selected"])
        request["needs"][1]["required"] = False
        self.assertEqual(select_tools(request)["status"], "planned")

    def test_failed_preference_does_not_repeat_or_expand_sources(self):
        request = self.request("explicit-provider")
        need = request["needs"][0]
        need["candidates"]["longbridge-quotes"]["state"] = "failed"
        result = select_tools(request)
        self.assertEqual(result["needs"][0]["selected"]["candidate"], "openbb")
        need["allowed_candidates"] = ["longbridge-quotes"]
        self.assertEqual(select_tools(request)["status"], "limited")

    def test_development_tools_cannot_be_selected_for_market_research(self):
        request = self.request("code-navigation")
        request["primary_workflow"] = "market-color"
        with self.assertRaisesRegex(ValueError, "outside market-color"):
            select_tools(request)

    def test_local_edits_are_limited_to_capabilities_that_allow_them(self):
        request = self.request("code-navigation")
        request["needs"][0]["candidates"]["serena"]["effect"] = "local_write"
        self.assertEqual(select_tools(request)["needs"][0]["selected"]["candidate"], "serena")
        request = self.request("fresh-bloomberg")
        need = request["needs"][0]
        for candidate in need["candidates"].values():
            candidate["effect"] = "local_write"
        self.assertEqual(select_tools(request)["status"], "limited")

    def test_unknown_or_unverified_bindings_never_become_available(self):
        for field, value in (("execution", "unknown"), ("evidence", ""), ("eligible", "true")):
            request = self.request("binding-required")
            candidate = request["needs"][0]["candidates"]["docling"]
            candidate["binding"] = "synthetic::docling"
            candidate[field] = value
            self.assertEqual(select_tools(request)["status"], "limited")

    def test_rejects_typoed_contracts_instead_of_silently_dropping_needs(self):
        for mutation in (
            lambda r: r.update(schema="tool_request/v2"),
            lambda r: r.update(primary_workflow="unknown"),
            lambda r: r.update(needs=[]),
            lambda r: r["needs"].append(copy.deepcopy(r["needs"][0])),
            lambda r: r["needs"][0].update(capability="invented-capability"),
            lambda r: r["needs"][0].update(local_only="true"),
            lambda r: r["needs"][0].update(required=None),
            lambda r: r["needs"][0].update(preferred_candidate="invented-tool"),
            lambda r: r["needs"][0].update(allowed_candidates=["invented-tool"]),
            lambda r: r["needs"][0]["candidates"].update({"invented-tool": {}}),
        ):
            request = self.request("financial-pdf")
            mutation(request)
            with self.assertRaises(ValueError):
                select_tools(request)

    def test_direct_entrypoints_reach_the_shared_procedure(self):
        catalog = json.loads((PLUGIN / "references" / "tool-capabilities.json").read_text(encoding="utf-8"))
        skills = list((PLUGIN / "skills").glob("*/SKILL.md"))
        self.assertEqual(set(catalog["workflows"]), {p.parent.name for p in skills} | {"public-equity-investing"})
        for path in skills:
            self.assertIn("../../references/tool-selection.md", path.read_text(encoding="utf-8"), path.parent.name)
        self.assertEqual(len(self.cases), len(self.by_id))


if __name__ == "__main__":
    unittest.main()
