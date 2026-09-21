# APAC Equity Desk

For minipanda's happy friends.

`apac-equity-desk` is a plugin and reference repository for sell-side APAC equity market colour, close wraps, catalyst work and event-driven idea generation. It installs into both the **Codex CLI** and the **Claude Code CLI** from one set of skills, references and helpers. It is optimized for China, Hong Kong, Japan, Korea, Australia and Singapore.

The system separates collection from judgment:

1. Longbridge supplies the primary live market and company data where coverage and entitlements permit.
2. Optional AKShare, Tushare and Jin10 adapters can fill China breadth, structured fundamentals/flows and fast macro-news gaps.
3. The Python helpers normalize and calculate facts before prose is drafted.
4. `source-verifier` and `desk-editor` challenge causal claims, contradictory evidence and numerical consistency.
5. Every publishable artifact remains a draft until a human approves it. Trading tools are never used.

## Just tell the desk what you need

You do not need to write a detailed prompt. Type these in a new Codex or Claude Code session after installation:

| You type | The desk handles |
| --- | --- |
| Japan morning | Opening tape, overnight context and sectors |
| Japan wrap | Full house-style country close and Corporate Headlines |
| CATL colour | Relative move, evidence-ranked explanations and watch points |
| Ideas from this | Up to three researched event scenarios with invalidation |
| Check this | Facts, citations, timestamps and contradictions |
| Tighten this | A concise edit of the draft you supply |

Research drafts include source verification and a desk-editor pass. House style,
source ranking and session/date handling are already designed in. Add instructions
only to override a default—for example, "Japan wrap, 300 words".

Natural-language skill selection depends on the session context. To select the
desk explicitly, type `$desk Japan wrap` in Codex or `/desk Japan wrap` in Claude
Code. Follow-ups such as "Ideas from this" use the event in the current session;
supply it if you are starting a fresh one.

Claude Code also exposes one slash command per workflow: `/morning`, `/wrap`,
`/color`, `/catalyst`, `/ideas`, `/check` and `/tighten`. They take the same
short arguments, for example `/wrap Japan, 300 words`. `/parallel` runs a
multi-market request with researcher subagents.

## What can this do for you?

Use it to turn market data and news into a draft you can review quickly. The examples below are prompts to paste into a **new Codex or Claude Code session after installation**, not commands to run in PowerShell. Live research needs connected, entitled data sources; you can also supply quotes, news links and an evidence pack yourself.

### 1. Explain why a stock is moving

Turn a price alert into concise trader-ready colour: the move, performance versus peers, volume context, possible catalysts and what to watch next. Separate verified disclosures from structural background and unconfirmed chatter.

> Why is CATL moving?

### 2. Write the closing market wrap

Build a country or regional recap covering indices, breadth, sectors, notable movers, turnover, flows and the session's main news. Identify missing inputs before drafting.

> China and HK wrap

You can also request Japan, Korea, Australia, Singapore or the full APAC region when suitable data is connected or supplied.

### 3. Write a short morning snippet

Lead with the current opening tape and index divergence, then cover overnight markets, policy events and sector leadership in three short paragraphs. If the market is still closed, the note is labelled PRE-OPEN and discusses expectations. An extended watchlist is available when requested.

> Japan morning

### 4. Test a catalyst before repeating it

Compare competing explanations for a move. Ask whether the news is new, whether its timing fits the price action, and whether peers support or contradict the explanation.

> Challenge the catalyst

### 5. Develop event-driven research ideas

Turn a verified event into a few research scenarios with a clear mechanism, time horizon, catalyst, risks and invalidation. This workflow frames ideas for discussion; it does not execute trades.

> Ideas from this

### 6. Run a regional request in parallel (Claude Code only)

For a request that spans several markets or several names, the Claude Code build
can gather the evidence concurrently: one researcher subagent per market, one
catalyst investigator per contested name, an independent verifier that audits
the draft without having seen how it was written, and the house-style drafting
kept in one context.

> /parallel APAC wrap

The split is by market, not by function. Within a single market the data work
and the news work are sequential — the mover list decides which catalysts matter
— so a subagent boundary between them buys nothing. Subagents exchange
`data-contract.md` packs rather than prose, because every prose hand-off is a
place a number gets retyped.

This costs roughly one gathering pass per market, so it is worth it for a
regional wrap and wasteful for a single country. Ordinary requests never fan
out. Codex ignores the `agents/` directory and runs the same workflows
sequentially.

### 7. Check a draft's facts and sources

Review claims for citation support, timestamps, units, numerical conflicts and unsupported causal language. Reposts of one story should not become multiple independent confirmations.

> Check this

### 8. Tighten a note before sending it

Give a completed draft a senior editorial pass: sharpen the lead, remove repetition, challenge weak explanations and preserve uncertainty. Supply the evidence with the draft; the editor does not collect missing data.

> Tighten this to 120 words

### A typical desk day

Start with “Japan morning”, ask “CATL colour” when a stock moves, and finish with “Japan wrap”. Verification and editing are included in each research draft. Follow up with “Challenge the catalyst” or “Ideas from this” when an event warrants deeper work.

These workflows run when requested. Installing the plugin does not create scheduled briefs, continuous monitoring or automatic distribution; those require separate setup. Every research draft stays subject to human publication approval.

## Our three default desk formats

The writing defaults follow the desk's preferred structure. The original samples are not reproduced in this public repository; the bundled examples use synthetic facts and fictional names.

- **Country close:** index divergence and heavyweight concentration; local policy; FX and rates; macro actual versus expectations; detailed losing and winning sectors; Corporate Headlines at the end. Flowing paragraphs, familiar desk shorthand and useful name/move lists. Usually 500–900 words, adjusted to the session.
- **Intraday theme:** a punchy headline and ticker block, competing explanations for the move, the fundamental hook, mixed evidence, cross-market implications and dated watch points. Usually 180–350 words; ask for a flash when you want less.
- **Morning snippet:** a country header such as `{JA} JAPAN MORNING`, the local opening tape first, overnight context second and sector leadership last. Usually 150–250 words. Pre-open expectations are explicitly distinguished from observed opening moves.

Evidence ranking stays in the research pack and informs the prose. Citations remain beside the claims; missing inputs go into separate review notes. Supplied humour is optional, with no automatically invented jokes. Taiwan themes can be researched with supplied or connected data, but no new Taiwan data feed is included.

These house formats apply by default; you do not need to ask for "house style". The regional digest and labelled single-stock layout remain available when explicitly requested.

Try the synthetic layouts locally:

```sh
python plugins/apac-equity-desk/scripts/render_market_wrap.py tests/fixtures/japan_close_house.json
python plugins/apac-equity-desk/scripts/render_market_color.py tests/fixtures/optical_theme_house.json
python plugins/apac-equity-desk/scripts/render_morning_brief.py tests/fixtures/japan_morning_house.json
```

The [house-style guide](plugins/apac-equity-desk/references/house-style.md) describes voice and sequencing. The [data contract](plugins/apac-equity-desk/references/data-contract.md#house-narrative-packs) documents the input formats.

## Repository layout

```text
AGENTS.md                           Desk-wide operating rules (shared)
CLAUDE.md                           Claude Code entry point; imports AGENTS.md
.codex/config.toml                  Codex MCP defaults + read-only tool allowlist
.claude/settings.json               Claude Code read-only tool permissions
.claude-plugin/marketplace.json     Claude Code marketplace manifest
.agents/plugins/marketplace.json    Codex marketplace manifest
.mcp.json                           Longbridge connection for in-repo sessions
config/providers.example.toml       Optional provider settings
plugins/apac-equity-desk/
  .claude-plugin/plugin.json        Claude Code plugin manifest
  .codex-plugin/plugin.json         Codex plugin manifest
  .mcp.json                         Longbridge hosted MCP connection
  skills/                           Short-request entrypoint + eight workflows
  commands/                         Claude Code slash commands for each workflow
  agents/                           Claude Code researcher/verifier subagents
  references/                       House style, data contract and mappings
  scripts/                          Deterministic calculation/rendering helpers
tests/                              Offline fixtures and unit tests
```

Both CLIs load the same `skills/`, `references/` and `scripts/`. Only the
manifests, the instruction entry point and the permission format differ.

## Quick start

### Codex CLI

```sh
codex plugin marketplace add https://github.com/eloriahu/apac-equity-desk
codex plugin add apac-equity-desk@apac-equity-desk
```

Start a new Codex task after installation. Try `$desk Japan wrap` or simply “Japan morning”.

To update an installed copy:

```sh
codex plugin marketplace upgrade apac-equity-desk
codex plugin add apac-equity-desk@apac-equity-desk
```

### Claude Code CLI

Run these at the Claude Code prompt, not in a shell:

```text
/plugin marketplace add eloriahu/apac-equity-desk
/plugin install apac-equity-desk@apac-equity-desk
```

Then try `/desk Japan wrap`, `/morning Japan`, or simply “Japan morning”.
Read the [safety boundary](#safety-boundary) before connecting Longbridge:
unlike Codex, an installed Claude Code plugin cannot ship its own permission
rules, so the read-only boundary needs one block copied into your settings.

To update an installed copy:

```text
/plugin marketplace update apac-equity-desk
```

### Either CLI

Complete Longbridge OAuth when prompted. Quote coverage depends on account entitlements; the official hosted MCP emphasizes US/HK and the scaffold requires approved fallback data for uncovered markets.

This is version 0.3.0: a research workflow scaffold with short-request routing, built-in review passes, house-style narrative formats, an offline market clock, a driver-scoring helper, a read-only Longbridge tool allowlist and offline tests. Live account integration has not been validated. Optional AKShare, Tushare and Jin10 entries are configuration examples, not implemented collectors. Market calendars and symbol mappings are starter data and need verification for the chosen provider and trading date.

All numbers, events, URLs and dates in `tests/fixtures/` are synthetic test data, not verified market facts. The renderers format supplied packs; they do not independently research or prove the content. The fact-check helper checks selected structural issues and does not establish that a source supports a claim.

Run the offline test suite with the bundled or system Python:

```powershell
python -m unittest discover -s tests -v
```

Try the included fixtures:

```powershell
python plugins/apac-equity-desk/scripts/market_snapshot.py tests/fixtures/quotes.json
python plugins/apac-equity-desk/scripts/render_market_color.py tests/fixtures/market_color_pack.json
python plugins/apac-equity-desk/scripts/render_market_wrap.py tests/fixtures/market_wrap_pack.json
python plugins/apac-equity-desk/scripts/session_clock.py --markets JP,HK,AU
```

The scripts consume normalized JSON/CSV rather than credentials. The agent collects live data with MCP tools, saves or pipes only the required fields, and runs the calculation helpers. See the plugin's `references/data-contract.md` for schemas and `references/integrations.md` for provider boundaries.

## Safety boundary

This repository is research-only. It must not submit, replace, cancel or stage orders; alter positions, alerts, watchlists or DCA/grid plans; or publish/send a draft without the user's explicit approval at that moment.

The upstream Longbridge MCP exposes trading and account-write tools. Each CLI
enforces the read-only boundary with its own mechanism, and the two are not
identical.

**Codex.** `.codex/config.toml` sets an `enabled_tools` allowlist for the `longbridge` server: only tools Longbridge itself marks read-only, minus reads of your own account (balances, positions, orders, statements, bank cards). Codex enforces this list, so the model cannot call anything outside it. New Longbridge tools stay blocked until they are reviewed and added.

**Claude Code.** Claude Code has no equivalent “only these tools” setting, so `.claude/settings.json` reproduces the boundary with permission rules:

- `permissions.allow` holds the same read-only tools as the Codex allowlist, so research calls run without prompting.
- `permissions.deny` names every order, alert, DCA, grid, watchlist, sharelist and community-post write tool, plus the account reads. Deny beats allow in Claude Code and cannot be overridden by an allow rule, a permission mode or a hook.
- Glob deny rules such as `mcp__longbridge__dca_*` cover those families, so a newly published tool inside one is blocked before anyone reviews it.

Claude Code applies `allow` rules from a project only after you accept the workspace trust dialog, because they grant capability. `deny` rules only restrict, so they apply from the first session whether or not you have trusted the folder. Until you trust it, the boundary still holds; research calls just prompt you one by one. Accept the trust dialog the first time you run Claude Code in this repository to stop the prompting.

One behavioural difference is worth knowing: a brand-new Longbridge tool outside every denied family is neither allowed nor denied, so Claude Code **prompts you** rather than refusing outright. Codex refuses it without asking. Decline unfamiliar tools at the prompt and open an issue.

`tests/test_claude_code_plugin.py` checks that the two builds still describe the same boundary: the allow list matches the Codex allowlist, every write and account tool is denied by name, and no deny glob accidentally shadows a research tool.

**Outside this repository.** Neither installed plugin carries its permission rules with it. For Codex, copy the `[mcp_servers.longbridge]` block into your user `~/.codex/config.toml`. For Claude Code, copy the `permissions` block from `.claude/settings.json` into `~/.claude/settings.json`. Also use least-privilege credentials where supported, and do not grant trading access for this desk workflow. Credentials, private client information and proprietary research must remain outside this public repository.

## Changelog

**0.3.0**

- Fixed: peer medians now exclude the stock itself. Before, a stock was compared against a basket that included it, which understated relative moves (by half in a two-stock basket). A stock with no priced peers now shows no peer spread instead of 0ppt.
- Fixed: CSV rows with a blank `last` now fall back to `close`; text signals such as `"True"` now count in the mover trigger.
- Fixed: news clusters order articles by actual time, not by timestamp text, so mixed-timezone feeds report the true earliest article.
- Fixed: the fact-checker reads a single string source ID correctly, blocks sources dated after the bundle's `as_of`, flags causal claims whose sources have no evidence level, and rejects timestamps without a timezone offset.
- Added: `session_clock.py`, an offline market clock (pre-open / open / lunch / closed / weekend / holiday) with a Sydney daylight-saving fallback for Python installs without timezone data. The market calendar moved from YAML to `market-calendars.json` so it needs no extra library.
- Added: `evidence_score.py`, which computes the 0–8 driver score from `source-priority.md`.
- Added: a read-only Longbridge tool allowlist in `.codex/config.toml`, with a test.
- Added: an optional Claude Code multi-agent mode. `/parallel` fans out one `market-pack-builder` per market and one `catalyst-investigator` per contested name, audits the draft with an independent `desk-verifier`, and keeps house-style drafting in one context. Subagents exchange data-contract packs rather than prose. Codex ignores `agents/` and runs the same workflows sequentially; a test keeps every other skill free of agent references so the Codex build cannot come to depend on them.
- Added: Claude Code CLI support alongside Codex. `.claude-plugin/marketplace.json`, `plugins/apac-equity-desk/.claude-plugin/plugin.json`, a `CLAUDE.md` that imports the shared `AGENTS.md`, eight slash commands, and a `.claude/settings.json` permission boundary mirrored from the Codex allowlist. Skills, references, scripts and tests are shared; `tests/test_claude_code_plugin.py` checks the two builds do not drift.
