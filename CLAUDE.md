# APAC Equity Desk instructions (Claude Code)

The desk rules are shared with the Codex build and live in one file. Read it first:

@AGENTS.md

## Claude Code specifics

Skills live in `plugins/apac-equity-desk/skills/`. Paths inside a `SKILL.md` such as
`../../references/house-style.md` resolve against that skill's own directory, which
Claude Code reports as the skill's base directory when the skill loads.

Slash commands in `plugins/apac-equity-desk/commands/` are the explicit route for
a short request: `/desk Japan wrap` is the Claude Code equivalent of Codex's
`$desk Japan wrap`. Plain English still works; the commands only remove ambiguity.

A command shadows a skill of the same name, which drops that skill out of the
list Claude Code offers and stops natural-language requests routing into it.
Commands are therefore named for the desk phrase (`/wrap`, `/color`, `/morning`)
rather than the skill directory. `desk` is the one deliberate overlap: the
`/desk` command reads `skills/desk/SKILL.md` and does that skill's job. A test
in `tests/test_claude_code_plugin.py` enforces this.

Run the Python helpers with the repository's interpreter, for example
`python plugins/apac-equity-desk/scripts/session_clock.py --markets JP`.
They read normalized JSON/CSV on stdin or as a path argument and never take
credentials.

## Tool permissions

`.claude/settings.json` holds the read-only Longbridge boundary for work done
inside this repository:

- `permissions.allow` lists the Longbridge tools Longbridge itself annotates
  `read_only_hint = true`, minus reads of the user's own account.
- `permissions.deny` lists every order, alert, DCA, grid, watchlist, sharelist
  and community-post write tool by name, plus glob rules covering those families
  so a newly published tool in them is blocked before review.

Deny always beats allow in Claude Code, and a deny rule cannot be overridden by
an allow rule, a permission mode or a hook. A Longbridge tool that is in neither
list prompts the user instead of running silently. Do not add a tool to `allow`
without checking its read-only annotation, and never propose editing the deny
list to unblock a call.
