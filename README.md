# APAC Equity Desk

For minipanda's happy friends.

`apac-equity-desk` is a plugin and reference repository for sell-side APAC equity market colour, close wraps, catalyst work and event-driven idea generation. It installs into both the **Codex CLI** and the **Claude Code CLI** from one set of skills, references and helpers. Regional requests cover North Asia, Australia/New Zealand, India and Southeast Asia to the extent the supplied or configured sources support each exchange.

The system separates collection from judgment:

1. User-supplied Bloomberg exports or screenshots are the preferred market-data input.
2. OpenBB fills only missing, stale or absent market fields; official sources remain authoritative for reported facts and events.
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
| What is moving in HK? | Ranked sector topics with breadth, relative move, volume and leaders |
| Review these results | Actual versus consensus, guidance, read-through and watch points |
| What matters next week? | Sourced APAC event and catalyst calendar |
| Map the read-through | Evidence-linked cross-market transmission paths |
| Update this thesis | Explicit signal-ledger change and preserved history |
| Multi-agent Japan wrap | Full Codex or Claude Code agent team with an independent audit |
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
short arguments, for example `/wrap Japan, 300 words`. `/parallel` runs any
request with the full agent team.

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

### 6. Find a timely topic before writing

Scan a broad market universe for sector moves that are large, benchmark-relative, broad and volume-supported. Fresh news improves the research queue but does not become a causal claim. The shortlist gives you observed metrics, leading names, evidence gaps and the next question to investigate.

> What is moving in HK, and what should I write about?

The radar is on-demand. For timely capture, connect a read-only quote/news source and run the supplied approval-gated automation design during market hours. It writes local evidence packs; external publication is disabled by default.

### 7. Run a request with the full agent team

For a note that matters, Codex or Claude Code can run the desk as a team of five
roles instead of one context:

| Agent | One per | Job |
| --- | --- | --- |
| `market-data-analyst` | market | Collects quotes, runs the Python helpers for indices, breadth, sectors, movers and flows, and checks the data for problems |
| `country-researcher` | market | Policy, macro, FX and rates, overnight context and corporate headlines |
| `catalyst-investigator` | contested name | Timeline, ranked competing explanations and what would falsify the lead |
| `chief-editor` | request | Drafts the house-style note from the packs and revises it against the verifier |
| `desk-verifier` | draft | Audits the draft against the packs without being told how it was reached |

> Multi-agent APAC wrap

The data analysts and country researchers run together, one pair per market.
The catalyst investigators run next, because the mover lists decide which names
need them. The chief editor drafts, the verifier audits, and the editor gets one
revision round against the findings. Anything still open after that round comes
back to you as an open finding.

Three rules protect the numbers across hand-offs: the data analyst never does
arithmetic (every derived figure comes from the helpers), packs travel in full
and nobody downstream rounds or re-derives a figure, and the editor receives
your request word for word.

A three-market wrap runs roughly a dozen agent contexts against one for the
ordinary workflow, so the team runs only when you ask for it. It works for a
single market too. Codex uses project-scoped roles in `.codex/agents/` when the
repository is open and can follow the installed `parallel-desk` orchestration
contract elsewhere. Claude Code uses the packaged `agents/` role files.

### 8. Check a draft's facts and sources

Review claims for citation support, timestamps, units, numerical conflicts and unsupported causal language. Reposts of one story should not become multiple independent confirmations.

> Check this

### 9. Tighten a note before sending it

Give a completed draft a senior editorial pass: sharpen the lead, remove repetition, challenge weak explanations and preserve uncertainty. Supply the evidence with the draft; the editor does not collect missing data.

> Tighten this to 120 words

### A typical desk day

Start with “What is moving in Japan?”, turn the selected sector into colour, ask “Japan wrap” near the close, and finish with “What matters tomorrow?”. Verification and editing are included. Follow up with “Challenge the catalyst”, “Map the read-through”, “Ideas from this”, or “Update this thesis” when a topic deserves deeper work.

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
.codex/agents/                      Codex project agent team (five roles)
.claude-plugin/marketplace.json     Claude Code marketplace manifest
.agents/plugins/marketplace.json    Codex marketplace manifest
config/providers.example.toml       Optional provider settings
plugins/apac-equity-desk/
  .claude-plugin/plugin.json        Claude Code plugin manifest
  .codex-plugin/plugin.json         Codex plugin manifest
  skills/                           Short-request entrypoint + thirteen workflows
  commands/                         Claude Code slash commands for each workflow
  agents/                           Claude Code agent team (five subagents)
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

To update an installed copy:

```text
/plugin marketplace update apac-equity-desk
```

### Either CLI

Attach a Bloomberg CSV/XLSX/BQL export or screenshot with the request. The desk preserves its displayed/export timestamp and uses OpenBB only when configured and needed. This is version 1.1.0: an on-demand APAC research desk with Bloomberg-first ingestion, screenshot support, field-level fallback lineage, session-aware freshness gates, topic discovery, earnings, event research, signal tracking, deterministic helpers and optional multi-agent mode. Market calendars and symbol mappings are starter data and need verification for the chosen provider and trading date.

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

The scripts consume normalized JSON/CSV rather than credentials. Bloomberg screenshots are transcribed from visible values, structured exports are normalized directly, and OpenBB fallback fields retain lineage. See the plugin's `references/data-contract.md` for schemas and `references/integrations.md` for provider boundaries.

## Safety boundary

This repository is research-only. It does not package a brokerage connector and must not submit, replace, cancel or stage orders; alter positions, alerts or watchlists; or publish/send a draft without the user's explicit approval at that moment. Bloomberg artifacts remain local and must not be committed or redistributed. OpenBB/provider credentials stay in local provider settings or environment variables.

## Changelog

**1.1.0**

- Changed: Bloomberg exports and screenshots are the preferred market-data input across every workflow; the plugin no longer packages a brokerage connector.
- Added: field-level OpenBB fallback lineage and conflicts, plus distinct task, ingestion and provider timestamps.
- Added: session-aware freshness and capture-skew gates, including correct lunch-break handling.

**1.0.0**

- Added: `topic-radar`, which ranks observed sector moves using magnitude, benchmark-relative performance, breadth, volume and fresh-news availability while leaving causal status unassessed.
- Added: readiness gates, prior/current pack deltas, earnings-surprise calculations, event calendars, evidence-linked cross-market maps, sector playbooks and an explicit signal ledger with no hidden memory.
- Added: Codex-native project agents and an installed-plugin orchestration contract for the same five-role team used by Claude Code.
- Added: a portable scheduled sector-radar workflow that writes local evidence packs and keeps optional external publication disabled and approval-gated.
- Added: synthetic regression tests for every new primitive and safety invariant.

**0.6.0**

- Added: claim-level freshness checks. Live facts can now declare `max_age_minutes`; the verifier uses source `observed_at` (falling back to `published_at`) and blocks evidence that is too old for the stated as-of time.
- Added: repeated numeric facts now fail verification when their units, currencies or sessions disagree, even when the numeric values happen to match.
- Fixed: base release versions are synchronized across the Python project, lock file, Codex manifest, Claude manifest and Claude marketplace, while preserving Codex's local cachebuster suffix; a regression test prevents drift.

**0.5.0**

- Changed: `/parallel` now runs the desk as a full five-agent team. New `market-data-analyst` (numbers and a data-quality check, always through the Python helpers) and `chief-editor` (house-style drafting and revision). `market-pack-builder` is renamed `country-researcher` and now covers session context only, since the numbers moved to the data analyst.
- Added: a revision round. The `desk-verifier`'s findings go back to the `chief-editor` once; anything still open is returned to the user instead of looping.
- Changed: the team can be run for a single market when asked for. Ordinary short requests still stay in one context.

**0.4.0**

- Added: Claude Code CLI support alongside Codex. `.claude-plugin/marketplace.json`, `plugins/apac-equity-desk/.claude-plugin/plugin.json`, a `CLAUDE.md` that imports the shared `AGENTS.md`, eight slash commands, and a `.claude/settings.json` permission boundary mirrored from the Codex allowlist. Skills, references, scripts and tests are shared; `tests/test_claude_code_plugin.py` checks the two builds do not drift.
- Added: the original Claude Code multi-agent mode. Version 1.0.0 extends the same role contract to Codex.
- Note: installed copies only pick up changes when this version string moves. `claude plugin update` and `codex plugin add` both compare versions, not content.

**0.3.0**

- Fixed: peer medians now exclude the stock itself. Before, a stock was compared against a basket that included it, which understated relative moves (by half in a two-stock basket). A stock with no priced peers now shows no peer spread instead of 0ppt.
- Fixed: CSV rows with a blank `last` now fall back to `close`; text signals such as `"True"` now count in the mover trigger.
- Fixed: news clusters order articles by actual time, not by timestamp text, so mixed-timezone feeds report the true earliest article.
- Fixed: the fact-checker reads a single string source ID correctly, blocks sources dated after the bundle's `as_of`, flags causal claims whose sources have no evidence level, and rejects timestamps without a timezone offset.
- Added: `session_clock.py`, an offline market clock (pre-open / open / lunch / closed / weekend / holiday) with a Sydney daylight-saving fallback for Python installs without timezone data. The market calendar moved from YAML to `market-calendars.json` so it needs no extra library.
- Added: `evidence_score.py`, which computes the 0–8 driver score from `source-priority.md`.
- Added at the time: a read-only provider boundary; version 1.1.0 removes the brokerage connector entirely.
