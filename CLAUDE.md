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

## Multi-agent mode

`plugins/apac-equity-desk/agents/` holds three subagents Codex cannot load:
`market-pack-builder`, `catalyst-investigator` and `desk-verifier`. Only
`skills/parallel-desk/SKILL.md` may reference them, so the Codex build never
depends on a component it cannot see; a test enforces that.

Fan out by market, not by function. Inside one market the data work and the news
work are sequential, because the mover list decides which catalysts matter.
Across markets they are independent.

Subagents return `data-contract.md` packs, never prose. Drafting and editing
stay in the parent context so one context owns the house voice, and figures
carry across as returned rather than being re-derived at a context boundary.

Reach for it only when the request spans several markets or several names. A
single-market request pays the dispatch cost and gets the same note.

Agent frontmatter is real YAML, so the `description` goes last and in a block
scalar (`description: |`). The examples inside it contain blank lines and lines
such as `user: "..."`; as a bare scalar, YAML ends the value at the first blank
line and reads the rest as more keys, which silently drops the `tools:` line and
launches the agent with every tool, `Write` and `Edit` included. Keep every
other key above the description. A test enforces the shape.

Each agent declares a read-only `tools:` allowlist rather than a
`disallowedTools:` denylist — a denylist was observed not to remove `Write` from
a dispatched agent. Both `Bash` and `PowerShell` are granted because Windows
resolves the shell tool to `PowerShell` only.

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
