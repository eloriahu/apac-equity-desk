# APAC Equity Desk

For minipanda's happy friends.

`apac-equity-desk` is a Codex plugin and reference repository for sell-side APAC equity market colour, close wraps, catalyst work and event-driven idea generation. It is optimized for China, Hong Kong, Japan, Korea, Australia and Singapore.

The system separates collection from judgment:

1. Longbridge supplies the primary live market and company data where coverage and entitlements permit.
2. Optional AKShare, Tushare and Jin10 adapters can fill China breadth, structured fundamentals/flows and fast macro-news gaps.
3. The Python helpers normalize and calculate facts before prose is drafted.
4. `source-verifier` and `desk-editor` challenge causal claims, contradictory evidence and numerical consistency.
5. Every publishable artifact remains a draft until a human approves it. Trading tools are never used.

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
