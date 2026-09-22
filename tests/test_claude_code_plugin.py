"""Packaging checks shared by the Codex and Claude Code plugin builds."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "apac-equity-desk"


class PluginPackagingTests(unittest.TestCase):
    def test_no_brokerage_connector_is_packaged(self):
        self.assertFalse((ROOT / ".mcp.json").exists())
        self.assertFalse((PLUGIN / ".mcp.json").exists())
        self.assertFalse((ROOT / ".codex" / "config.toml").exists())
        self.assertFalse((ROOT / ".claude" / "settings.json").exists())

    def test_manifests_share_release_version_and_have_no_mcp(self):
        codex = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        claude = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        base = codex["version"].split("+", 1)[0]
        self.assertEqual(base, "1.3.0")
        self.assertEqual(claude["version"], base)
        self.assertEqual(marketplace["version"], base)
        self.assertEqual(marketplace["plugins"][0]["version"], base)
        self.assertNotIn("mcpServers", codex)
        self.assertNotIn("mcpServers", claude)

    def test_all_expected_skills_are_packaged(self):
        names = {path.parent.name for path in (PLUGIN / "skills").glob("*/SKILL.md")}
        expected = {
            "apac-market-wrap", "catalyst-analysis", "cross-market-map", "desk",
            "company-fundamentals", "company-quality", "desk-editor", "earnings-review",
            "event-radar", "event-trade-ideas", "idea-funnel", "management-review",
            "market-color", "morning-brief", "parallel-company-research", "parallel-desk",
            "parallel-earnings", "research-review", "signal-ledger", "source-verifier",
            "topic-radar",
        }
        self.assertEqual(names, expected)

    def test_fundamental_workflow_is_routed_and_commanded(self):
        router = (PLUGIN / "skills" / "desk" / "SKILL.md").read_text(encoding="utf-8")
        contract = (PLUGIN / "references" / "data-contract.md").read_text(encoding="utf-8")
        self.assertIn("company-fundamentals", router)
        self.assertIn("fundamental_pack/v1", contract)
        self.assertTrue((PLUGIN / "commands" / "fundamentals.md").is_file())

    def test_automatic_research_workflows_are_packaged(self):
        router = (PLUGIN / "skills" / "desk" / "SKILL.md").read_text(encoding="utf-8")
        contracts = (PLUGIN / "references" / "research-contracts.md").read_text(encoding="utf-8")
        for name in (
            "company-quality", "idea-funnel", "management-review", "research-review",
            "parallel-company-research", "parallel-earnings",
        ):
            self.assertIn(name, router)
        self.assertIn("idea_funnel/v1", contracts)
        self.assertIn("research_review/v1", contracts)

        commands = {path.stem for path in (PLUGIN / "commands").glob("*.md")}
        self.assertTrue({
            "discover", "management", "quality", "research-audit",
            "company-team", "earnings-team",
        }.issubset(commands))

    def test_implicit_invocation_is_explicit_for_router_and_composite_routes(self):
        names = {
            "desk", "market-color", "company-quality", "idea-funnel",
            "management-review", "research-review", "parallel-company-research",
            "parallel-earnings",
        }
        for name in names:
            metadata = (PLUGIN / "skills" / name / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertIn("allow_implicit_invocation: true", metadata, name)

    def test_functional_agent_sets_match_between_hosts(self):
        claude = {path.stem for path in (PLUGIN / "agents").glob("*.md")}
        codex = {path.stem for path in (ROOT / ".codex" / "agents").glob("*.toml")}
        self.assertEqual(claude, codex)
        self.assertTrue({
            "filings-accounting-analyst", "business-kpi-analyst",
            "industry-chain-analyst", "expectations-valuation-analyst",
            "management-governance-analyst", "bear-case-analyst",
        }.issubset(claude))

    def test_agent_prompts_do_not_request_brokerage_tools(self):
        for path in (PLUGIN / "agents").glob("*.md"):
            content = path.read_text(encoding="utf-8").lower()
            self.assertNotIn("mcp__longbridge", content, path.name)
            self.assertIn("never", content, path.name)


if __name__ == "__main__":
    unittest.main()
