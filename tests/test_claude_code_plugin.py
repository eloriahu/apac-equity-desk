"""Checks that the Claude Code build stays in step with the Codex build.

The two CLIs read different manifests and enforce tool access differently, so
these tests pin the parts that must not drift: the same skills, the same
read-only Longbridge boundary and the same plugin identity.
"""
from __future__ import annotations

import fnmatch
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "apac-equity-desk"
PREFIX = "mcp__longbridge__"

# Tools that mutate an account or a shared surface, plus reads of the user's own
# account. Mirrors ReadOnlyAllowlistTests in test_review_fixes.py.
WRITE_TOOLS = {
    "submit_order", "replace_order", "cancel_order", "alert_add", "alert_delete", "alert_enable", "alert_disable",
    "create_watchlist_group", "update_watchlist_group", "delete_watchlist_group", "topic_create", "topic_create_reply",
    "dca_create", "dca_update", "dca_pause", "dca_resume", "dca_stop", "grid_submit", "grid_replace", "grid_cancel",
    "grid_suspend", "grid_restart", "sharelist_create", "sharelist_delete", "sharelist_add", "sharelist_remove", "sharelist_sort",
}
ACCOUNT_READS = {
    "account_balance", "stock_positions", "today_orders", "history_orders",
    "bank_cards", "withdrawals", "short_margin", "screener_user_strategies",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def codex_allowlist() -> set[str]:
    import tomllib

    config = tomllib.loads((ROOT / ".codex" / "config.toml").read_text(encoding="utf-8"))
    return set(config["mcp_servers"]["longbridge"]["enabled_tools"])


class ManifestTests(unittest.TestCase):
    def test_claude_plugin_manifest_matches_codex_manifest(self):
        claude = load_json(PLUGIN / ".claude-plugin" / "plugin.json")
        codex = load_json(PLUGIN / ".codex-plugin" / "plugin.json")
        self.assertEqual(claude["name"], codex["name"])
        # Codex local development adds a +codex.<cachebuster> suffix; Claude
        # and the package metadata share the underlying release version.
        self.assertEqual(claude["version"], codex["version"].split("+", 1)[0])
        self.assertEqual(claude["description"], codex["description"])

    def test_marketplace_points_at_the_plugin(self):
        marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json")
        self.assertEqual(marketplace["name"], "apac-equity-desk")
        self.assertIn("name", marketplace["owner"])
        entries = marketplace["plugins"]
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry["source"], "./plugins/apac-equity-desk")
        self.assertTrue((ROOT / entry["source"]).is_dir())
        self.assertEqual(entry["version"], load_json(PLUGIN / ".claude-plugin" / "plugin.json")["version"])

    def test_release_versions_stay_in_sync(self):
        version = load_json(PLUGIN / ".codex-plugin" / "plugin.json")["version"].split("+", 1)[0]
        claude = load_json(PLUGIN / ".claude-plugin" / "plugin.json")["version"]
        marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json")
        pyproject = re.search(r'^version = "([^"]+)"$', (ROOT / "pyproject.toml").read_text(encoding="utf-8"), re.M)
        lock = re.search(r'^version = "([^"]+)"$', (ROOT / "uv.lock").read_text(encoding="utf-8"), re.M)
        self.assertIsNotNone(pyproject)
        self.assertIsNotNone(lock)
        self.assertEqual(
            {version, claude, marketplace["version"], marketplace["plugins"][0]["version"], pyproject.group(1), lock.group(1)},
            {version},
        )

    def test_mcp_config_is_the_read_only_longbridge_endpoint(self):
        for path in (ROOT / ".mcp.json", PLUGIN / ".mcp.json"):
            servers = load_json(path)["mcpServers"]
            self.assertEqual(set(servers), {"longbridge"}, path)
            self.assertEqual(servers["longbridge"]["url"], "https://mcp.longbridge.com", path)

    def test_claude_md_imports_the_shared_desk_rules(self):
        self.assertIn("@AGENTS.md", (ROOT / "CLAUDE.md").read_text(encoding="utf-8"))


class PermissionTests(unittest.TestCase):
    def setUp(self):
        try:
            import tomllib  # noqa: F401
        except ImportError:
            self.skipTest("tomllib needs Python 3.11+")
        permissions = load_json(ROOT / ".claude" / "settings.json")["permissions"]
        self.allow = permissions["allow"]
        self.deny = permissions["deny"]
        self.allowed_tools = {rule.removeprefix(PREFIX) for rule in self.allow}

    def test_every_rule_is_scoped_to_longbridge(self):
        for rule in self.allow + self.deny:
            self.assertTrue(rule.startswith(PREFIX), rule)

    def test_allowlist_matches_the_codex_allowlist(self):
        # "authenticate" is deliberately absent: the OAuth handshake should prompt.
        self.assertEqual(self.allowed_tools, codex_allowlist() - {"authenticate"})

    def test_no_allow_rule_uses_a_wildcard(self):
        for rule in self.allow:
            self.assertNotIn("*", rule, rule)

    def test_write_and_account_tools_are_denied_by_name(self):
        denied = {rule.removeprefix(PREFIX) for rule in self.deny}
        self.assertLessEqual(WRITE_TOOLS, denied)
        self.assertLessEqual(ACCOUNT_READS, denied)

    def test_deny_rules_never_shadow_an_allowed_read(self):
        # Deny beats allow in Claude Code, so a careless glob would silently
        # disable a research tool.
        patterns = [rule.removeprefix(PREFIX) for rule in self.deny]
        shadowed = sorted(
            tool for tool in self.allowed_tools
            for pattern in patterns
            if fnmatch.fnmatchcase(tool, pattern)
        )
        self.assertEqual(shadowed, [])

    def test_write_tool_families_are_covered_by_globs(self):
        patterns = [rule.removeprefix(PREFIX) for rule in self.deny if "*" in rule]
        for future_tool in ("alert_snooze", "dca_archive", "grid_pause", "sharelist_rename",
                            "rename_watchlist_group", "submit_basket", "account_statements"):
            self.assertTrue(
                any(fnmatch.fnmatchcase(future_tool, p) for p in patterns),
                f"no glob deny covers {future_tool}",
            )


class ComponentDiscoveryTests(unittest.TestCase):
    SKILLS = {
        "apac-market-wrap", "catalyst-analysis", "desk", "desk-editor",
        "event-trade-ideas", "market-color", "morning-brief", "parallel-desk",
        "source-verifier",
    }
    COMMANDS = {
        "catalyst", "check", "color", "desk",
        "ideas", "morning", "parallel", "tighten", "wrap",
    }
    AGENTS = {
        "catalyst-investigator", "chief-editor", "country-researcher",
        "desk-verifier", "market-data-analyst",
    }
    # A command shadows a skill of the same name: the skill drops out of the
    # skill list Claude Code offers, so natural-language routing into it stops
    # working. "desk" is the one deliberate overlap, because the /desk command
    # reads skills/desk/SKILL.md and does that skill's job explicitly.
    INTENTIONAL_SHADOWS = {"desk"}

    def test_skills_are_discoverable_by_both_clis(self):
        found = {d.name for d in (PLUGIN / "skills").iterdir() if d.is_dir()}
        self.assertEqual(found, self.SKILLS)
        for name in found:
            skill = PLUGIN / "skills" / name / "SKILL.md"
            self.assertTrue(skill.is_file(), skill)
            self.assertTrue(skill.read_text(encoding="utf-8").startswith("---\n"), skill)

    def test_commands_exist_with_frontmatter(self):
        found = {p.stem for p in (PLUGIN / "commands").glob("*.md")}
        self.assertEqual(found, self.COMMANDS)
        for name in sorted(found):
            text = (PLUGIN / "commands" / f"{name}.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"), name)
            self.assertIn("description:", text.split("---")[1], name)

    def test_commands_do_not_shadow_skills(self):
        collisions = (self.COMMANDS & self.SKILLS) - self.INTENTIONAL_SHADOWS
        self.assertEqual(collisions, set(), f"rename these commands: {sorted(collisions)}")

    def agent_frontmatter(self, name: str) -> str:
        text = (PLUGIN / "agents" / f"{name}.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"), name)
        return text[4:].split("\n---\n", 1)[0]

    def test_agents_are_well_formed(self):
        found = {p.stem for p in (PLUGIN / "agents").glob("*.md")}
        self.assertEqual(found, self.AGENTS)
        for name in sorted(found):
            front = self.agent_frontmatter(name)
            for field in ("name:", "description:", "model:", "color:", "tools:"):
                self.assertIn(field, front, f"{name} is missing {field}")
            declared = re.search(r"^name:\s*(\S+)", front, re.M).group(1)
            self.assertEqual(declared, name, "agent name must match its filename")
            self.assertIn("<example>", front, f"{name} needs triggering examples")

    def test_agent_frontmatter_is_parseable_yaml(self):
        # The description carries <example> blocks containing blank lines and
        # lines such as `user: "..."`. As a bare scalar, YAML ends the value at
        # the first blank line and reads the rest as more keys, so a `tools:`
        # written after it never reaches Claude Code and the agent silently
        # launches with every tool. Keep the description last and in a block
        # scalar, with every other key ahead of it.
        for name in sorted(self.AGENTS):
            front = self.agent_frontmatter(name)
            self.assertIn("description: |", front, f"{name} needs a block scalar")
            self.assertEqual(front.count("tools:"), 1, f"{name} has a stray tools line")
            desc_at = front.index("description:")
            for key in ("name:", "model:", "color:", "tools:"):
                self.assertLess(front.index(key), desc_at, f"{key} must precede description in {name}")
            body = front.split("description: |", 1)[1]
            for line in body.splitlines():
                if line.strip():
                    self.assertTrue(line.startswith("  "), f"unindented block-scalar line in {name}: {line!r}")

    def test_agents_cannot_write_to_the_repository(self):
        for name in sorted(self.AGENTS):
            front = self.agent_frontmatter(name)
            granted = {x.strip() for x in re.search(r"^tools:\s*(.+)$", front, re.M).group(1).split(",")}
            for banned in ("Write", "Edit", "NotebookEdit", "*"):
                self.assertNotIn(banned, granted, f"{name} must not be granted {banned}")
            self.assertIn("Read", granted, name)
            self.assertIn("mcp__longbridge__*", granted, name)
            # Windows resolves the shell tool to PowerShell, POSIX hosts to Bash.
            self.assertTrue({"Bash", "PowerShell"} <= granted, f"{name} needs both shell tools")

    def test_agent_names_do_not_collide(self):
        self.assertEqual(self.AGENTS & self.SKILLS, set())
        self.assertEqual(self.AGENTS & self.COMMANDS, set())

    def test_only_the_parallel_skill_depends_on_agents(self):
        # Codex loads skills but not agents/. Any other skill that told the
        # model to dispatch one would break the Codex build silently.
        for skill in sorted(self.SKILLS - {"parallel-desk"}):
            text = (PLUGIN / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
            for agent in self.AGENTS:
                self.assertNotIn(agent, text, f"{skill} references the {agent} agent")

    def test_commands_reference_real_skill_files(self):
        for path in (PLUGIN / "commands").glob("*.md"):
            for line in path.read_text(encoding="utf-8").splitlines():
                if "${CLAUDE_PLUGIN_ROOT}/" not in line:
                    continue
                target = line.split("${CLAUDE_PLUGIN_ROOT}/")[1].split("`")[0].strip()
                self.assertTrue((PLUGIN / target).is_file(), f"{path.name} -> {target}")


if __name__ == "__main__":
    unittest.main()
