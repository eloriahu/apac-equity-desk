from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "apac-equity-desk"


class AutomaticRoutingPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.routing = (PLUGIN / "references" / "intent-routing.md").read_text(encoding="utf-8")
        cls.desk = (PLUGIN / "skills" / "desk" / "SKILL.md").read_text(encoding="utf-8")
        cls.color = (PLUGIN / "skills" / "market-color" / "SKILL.md").read_text(encoding="utf-8")
        cls.fundamentals = (
            PLUGIN / "skills" / "company-fundamentals" / "SKILL.md"
        ).read_text(encoding="utf-8")
        cls.company_team = (
            PLUGIN / "skills" / "parallel-company-research" / "SKILL.md"
        ).read_text(encoding="utf-8")
        cls.earnings_team = (
            PLUGIN / "skills" / "parallel-earnings" / "SKILL.md"
        ).read_text(encoding="utf-8")
        cls.eval_cases = json.loads(
            (PLUGIN / "references" / "routing-evals.json").read_text(encoding="utf-8")
        )["cases"]

    def test_router_classifies_five_decision_dimensions(self):
        for phrase in (
            "Observation or question", "Research horizon", "Requested deliverable",
            "Evidence availability", "Complexity and consequence",
        ):
            self.assertIn(phrase, self.routing)
        for field in (
            "primary_workflow", "required_enrichers", "optional_followups",
            "execution_mode", "reason", "stop_conditions",
        ):
            self.assertIn(field, self.desk + self.routing)

    def test_one_stock_move_uses_lean_composite_color(self):
        self.assertIn("TSMC is up 6%, why?", self.routing)
        self.assertIn("market-color", self.routing)
        self.assertIn("no team", self.routing)
        for lane in (
            "company-specific", "regulatory", "peers", "sentiment", "fundamental",
        ):
            self.assertIn(lane, self.color.lower() + self.routing.lower())
        self.assertIn("Do not automatically run a full idea funnel", self.color)

    def test_idea_route_requires_candidate_intent_or_central_chain(self):
        self.assertIn("who benefits/loses", self.routing)
        self.assertIn("cross-market chain is central", self.routing)
        self.assertIn("Find AI power bottlenecks", self.routing)

    def test_agent_escalation_distinguishes_micro_and_full_team(self):
        self.assertIn("One-wave micro-team", self.routing)
        self.assertIn("Full team", self.routing)
        self.assertIn("quick", self.routing.lower())
        self.assertIn("at most three workers", self.routing)
        self.assertIn("Agents never spawn other agents", self.routing)
        self.assertIn("agreement between agents does not raise confidence", self.routing)
        for full_team_skill in (self.company_team, self.earnings_team):
            frontmatter = full_team_skill.split("---", 2)[1].lower()
            self.assertIn("explicitly parallel", frontmatter)
            self.assertIn("one-wave micro-team", frontmatter)
            self.assertNotIn("conflicted, high-consequence", frontmatter)

    def test_route_graph_and_handoffs_are_bounded(self):
        self.assertIn("exactly one lead route", self.routing)
        self.assertIn("one-way support graph", self.routing)
        self.assertIn("Public Equity Investing", self.routing)
        self.assertIn("full initiation", self.routing)
        self.assertIn("automatically", self.routing)
        self.assertIn("Portfolio sizing or hedge design routes only", self.routing)
        self.assertIn("prior thesis/report", self.routing)
        self.assertIn("ambiguous ticker/listing", self.routing)

    def test_full_initiation_has_one_hero_artifact_owner(self):
        frontmatter = self.fundamentals.split("---", 2)[1].lower()
        self.assertNotIn("initiate on this name", frontmatter)
        self.assertIn("public equity investing", frontmatter)
        self.assertIn("rather than owning a duplicate hero deliverable", frontmatter)
        self.assertIn("automatically when available", self.routing)

    def test_machine_readable_route_acceptance_cases(self):
        self.assertEqual(len(self.eval_cases), 18)
        self.assertEqual(len({case["id"] for case in self.eval_cases}), 18)
        by_id = {case["id"]: case for case in self.eval_cases}
        for case in self.eval_cases:
            self.assertIsInstance(case["primary_workflow"], str)
            self.assertNotIn(case["primary_workflow"], case["required_enrichers"])
            self.assertIn(case["execution_mode"], {"single", "composed", "agent-team"})
            self.assertIn(case["team"], {"none", "micro", "full"})
            if case["action"] == "clarify":
                self.assertEqual(case["clarification_count"], 1)
                self.assertEqual(case["team"], "none")
        self.assertEqual(by_id["one-stock-move"]["primary_workflow"], "market-color")
        self.assertIn("idea-funnel", by_id["one-stock-move"]["forbidden_workflows"])
        self.assertEqual(by_id["move-to-beneficiaries"]["primary_workflow"], "market-color")
        self.assertIn("idea-funnel", by_id["move-to-beneficiaries"]["required_enrichers"])
        self.assertEqual(by_id["bottleneck-discovery"]["primary_workflow"], "idea-funnel")
        self.assertEqual(by_id["full-initiation-dcf"]["hero_artifact_owner"], "public-equity-investing")
        self.assertEqual(by_id["quick-earnings"]["team"], "none")
        self.assertEqual(by_id["explicit-full-team"]["team"], "full")
        self.assertEqual(by_id["thesis-without-baseline"]["action"], "clarify")
        self.assertEqual(by_id["ambiguous-ticker"]["clarification_count"], 1)
        self.assertEqual(by_id["filing-delta"]["primary_workflow"], "filing-change")
        self.assertEqual(by_id["estimate-revision"]["primary_workflow"], "expectations-change")
        self.assertEqual(by_id["foreign-flow"]["primary_workflow"], "ownership-flow")
        self.assertEqual(by_id["street-consensus-challenge"]["primary_workflow"], "consensus-challenge")
        for identity, primary in {
            "merger-spread": "merger-arb",
            "special-situation-screen": "special-situations",
            "deal-watchlist-update": "deal-monitor",
            "takeover-price-move": "market-color",
            "policy-event-ideas": "event-trade-ideas",
            "general-event-calendar": "event-radar",
        }.items():
            self.assertEqual(by_id[identity]["primary_workflow"], primary)
            self.assertTrue((PLUGIN / "skills" / primary / "SKILL.md").is_file())


class ResearchContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contracts = (PLUGIN / "references" / "research-contracts.md").read_text(encoding="utf-8")

    def test_contracts_are_schema_only_and_source_independent(self):
        self.assertIn("idea_funnel/v1", self.contracts)
        self.assertIn("research_review/v1", self.contracts)
        for schema in ("filing_change/v1", "expectations_bridge/v1", "ownership_flow/v1"):
            self.assertIn(schema, self.contracts)
        self.assertIn("consensus_challenge/v1", self.contracts)
        self.assertIn("must not import", self.contracts)
        self.assertIn("independence_group", self.contracts)

    def test_idea_funnel_blocks_ranking_on_broken_required_links(self):
        self.assertIn("causal_gate", self.contracts)
        self.assertIn("any required link not `supported` blocks all ranking", self.contracts)
        self.assertIn("rankability_reasons", self.contracts)

    def test_research_review_has_drift_and_publication_gates(self):
        for phrase in (
            "comparison_status", "substantive_state", "limited_no_baseline",
            "effect_on_conclusion", "publication gate", "unverifiable",
        ):
            self.assertIn(phrase, self.contracts)


if __name__ == "__main__":
    unittest.main()
