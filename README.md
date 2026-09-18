# APAC Equity Desk

For minipanda's happy friends.

`apac-equity-desk` is a Codex plugin and reference repository for sell-side APAC equity market colour, close wraps, catalyst work and event-driven idea generation. It is optimized for China, Hong Kong, Japan, Korea, Australia and Singapore.

The system separates collection from judgment:

1. Longbridge supplies the primary live market and company data where coverage and entitlements permit.
2. Optional AKShare, Tushare and Jin10 adapters can fill China breadth, structured fundamentals/flows and fast macro-news gaps.
3. The Python helpers normalize and calculate facts before prose is drafted.
4. `source-verifier` and `desk-editor` challenge causal claims, contradictory evidence and numerical consistency.
5. Every publishable artifact remains a draft until a human approves it. Trading tools are never used.

## What can this do for you?

Use it to turn market data and news into a draft you can review quickly. The examples below are prompts to paste into a **new Codex task after installation**, not commands to run in PowerShell. Live research needs connected, entitled data sources; you can also supply quotes, news links and an evidence pack yourself.

### 1. Explain why a stock is moving

Turn a price alert into concise trader-ready colour: the move, performance versus peers, volume context, possible catalysts and what to watch next. Separate verified disclosures from structural background and unconfirmed chatter.

> Use $market-color to investigate CATL (300750.SZ). Compare its latest move with Ganfeng and Tianqi, check the H-share where data is available, and draft 150 words of market colour. Distinguish confirmed facts from possible explanations and cite the sources.

### 2. Write the closing market wrap

Build a country or regional recap covering indices, breadth, sectors, notable movers, turnover, flows and the session's main news. Identify missing inputs before drafting.

> Use $apac-market-wrap to draft today's China and Hong Kong close wrap. Lead with what changed during the session, explain the strongest and weakest sectors, and finish with tomorrow's watch points. Include as-of times and flag unavailable data.

You can also request Japan, Korea, Australia, Singapore or the full APAC region when suitable data is connected or supplied.

### 3. Prepare for the trading day

Condense overnight markets, company disclosures and scheduled events into a selective pre-open watchlist, with the names and sectors most exposed.

> Use $morning-brief to prepare my APAC pre-open brief. Focus on overnight US tech, currencies, commodities and company announcements. Give me up to 10 watch items and explain what would confirm each read-through.

### 4. Test a catalyst before repeating it

Compare competing explanations for a move. Ask whether the news is new, whether its timing fits the price action, and whether peers support or contradict the explanation.

> Use $catalyst-analysis to assess whether this battery-sector sell-off is better explained by lithium prices, demand expectations or company news. Use the attached evidence, rank the explanations and state what remains unresolved.

### 5. Develop event-driven research ideas

Turn a verified event into a few research scenarios with a clear mechanism, time horizon, catalyst, risks and invalidation. This workflow frames ideas for discussion; it does not execute trades.

> Use $event-trade-ideas to develop up to three APAC equity research scenarios from this verified policy announcement. Explain what may already be priced in, the affected names, the earnings or valuation impact, and what would invalidate each idea. Return fewer ideas if the evidence is weak.

### 6. Check a draft's facts and sources

Review claims for citation support, timestamps, units, numerical conflicts and unsupported causal language. Reposts of one story should not become multiple independent confirmations.

> Use $source-verifier to audit the market note and source links below. Flag unsupported claims, stale data and any rumour presented as fact. Tell me which corrections are needed before I share it.

### 7. Tighten a note before sending it

Give a completed draft a senior editorial pass: sharpen the lead, remove repetition, challenge weak explanations and preserve uncertainty. Supply the evidence with the draft; the editor does not collect missing data.

> Use $desk-editor to tighten this market-colour draft to 120 words. Preserve the numbers and citations, distinguish today's trigger from background, and list any evidence gaps separately.

### A typical desk day

Start with `$morning-brief`, use `$market-color` for intraday moves, and finish with `$apac-market-wrap`. Run `$source-verifier` and `$desk-editor` on drafts before your final review. Use `$catalyst-analysis` and `$event-trade-ideas` when an event warrants deeper work.

These workflows run when requested. Installing the plugin does not create scheduled briefs, continuous monitoring or automatic distribution; those require separate setup. Every research draft stays subject to human publication approval.

## Repository layout

```text
.codex/config.toml                  Project MCP defaults
AGENTS.md                           Desk-wide operating rules
config/providers.example.toml       Optional provider settings
plugins/apac-equity-desk/
  .codex-plugin/plugin.json         Plugin manifest
  .mcp.json                         Longbridge hosted MCP connection
  skills/                           Seven desk workflows
  references/                       House style, data contract and mappings
  scripts/                          Deterministic calculation/rendering helpers
tests/                              Offline fixtures and unit tests
```

## Quick start

Install with the Codex CLI:

```sh
codex plugin marketplace add https://github.com/eloriahu/apac-equity-desk
codex plugin add apac-equity-desk@apac-equity-desk
```

Start a new Codex task after installation. Try `$market-color` with a ticker or `$apac-market-wrap` with a date and markets. Complete Longbridge OAuth when prompted. Quote coverage depends on account entitlements; the official hosted MCP emphasizes US/HK and the scaffold requires approved fallback data for uncovered markets.

To update an installed copy:

```sh
codex plugin marketplace upgrade apac-equity-desk
codex plugin add apac-equity-desk@apac-equity-desk
```

This is version 0.1.0: an initial research workflow scaffold with offline tests. Live account integration has not been validated. Optional AKShare, Tushare and Jin10 entries are configuration examples, not implemented collectors. Market calendars and symbol mappings are starter data and need verification for the chosen provider and trading date.

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
```

The scripts consume normalized JSON/CSV rather than credentials. Codex should collect live data with MCP tools, save/pipe only the required fields, and run the calculation helpers. See the plugin's `references/data-contract.md` for schemas and `references/integrations.md` for provider boundaries.

## Safety boundary

This repository is research-only. It must not submit, replace, cancel or stage orders; alter positions, alerts, watchlists or DCA/grid plans; or publish/send a draft without the user's explicit approval at that moment.

These are agent instructions, not a server-enforced tool filter. The upstream Longbridge MCP can expose trading and account-write tools. Use least-privilege credentials where supported and do not grant trading access for this desk workflow. Credentials, private client information and proprietary research must remain outside this public repository.
