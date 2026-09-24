# Integration notes

## Bloomberg user inputs — preferred market observations

Accept user-supplied Bloomberg CSV/XLSX/BQL exports and screenshots. Structured exports are preferred, but screenshots are first-class evidence when the visible rows can be read reliably. Transcribe only visible values, use numerical signs rather than colour, and leave cropped or ambiguous cells missing. Keep the source artifact local; never commit or redistribute proprietary inputs.

Record task/upload time separately from Bloomberg's visible/export timestamp. A screenshot uploaded at 13:00 is not 13:00 market data unless the screen itself supports that timestamp. Saved Bloomberg spreadsheet values may be used, but do not claim BDP/BDH/BQL formulas refreshed outside a Bloomberg-enabled environment.

## OpenBB — field-level fallback

Use OpenBB when no Bloomberg input was supplied or when supplied market fields are missing or stale. FMP is the preferred broad-exchange candidate when configured; Yahoo Finance is suitable for a controlled symbol basket and cross-checking. Provider coverage, latency and entitlements must be verified for each APAC exchange. OpenBB is a routing layer, not the underlying data owner.

Fallback values must retain provider and timestamp lineage. Fresh fallback data may replace stale live fields, but it must not silently replace fresh Bloomberg observations or official reported facts. Preserve material conflicts for review.

## Official and optional sources

Company filings and direct statements, exchange/regulator releases and official economic data remain authoritative for reported actuals and events. Optional AKShare/Tushare can support China-specific breadth or flows and Jin10 can support macro-headline timing when configured.

Adapters should output the normalized contract in `data-contract.md`, including provider, artifact/endpoint identity, task time, market timestamp, timezone, capture window and delayed/live status.

## AI Toolbox fundamental-tools

When installed, `fundamental-tools` is the reusable source and calculation layer for company fundamentals. Consume `fundamental_pack/v1`; do not import, vendor or assume the local path of the toolbox repository. Preserve this desk's source ranking and verify material claims independently.

Country preference is J-Quants/JPX for Japan, OpenDART/FSS for Korea, TWSE/MOPS for Taiwan, and SEC EDGAR for US-listed issuers or ADRs. FinanceDatabase supports identity resolution, FinanceToolkit supports transparent calculations, and AKShare is a fallback. A missing optional package or API key produces a declared gap, not an installation attempt.

The Public Equity Investing plugin complements this desk. When the requested
deliverable is an initiation, model, comps/DCF workbook or equivalent full
investment artifact and that plugin is available, route to it automatically
and provide the verified APAC evidence pack; the user does not need to name the
plugin. If it is unavailable, state the capability boundary and return only the
supported desk research. Do not duplicate the same hero artifact in two
plugins. Portfolio sizing or hedging requires an explicit portfolio request.
Unless the installed Public Equity Investing version explicitly declares one
of the toolbox schemas, hand it both the raw pack and a concise schema-neutral
brief containing issuer/listing, as-of time, sourced facts, assumptions,
conflicts, calculations and falsifiers. Treat this as an evidence handoff, not
as a claim that the receiving plugin natively validates the pack version.

## AI Toolbox idea, review and consensus packs

AI Toolbox may also produce `idea_funnel/v1`, `research_review/v1` and `consensus_challenge/v1`. Consume
the schemas documented in `research-contracts.md`; do not import the toolbox,
assume a checkout path or make it a required runtime dependency. Preserve the
shared claim/source registry, `independence_group`, quality status, rejected
candidates, incomplete comparisons, failed/unverifiable audit rows and consensus
coverage limits. Broker reports are accessed only through user entitlements or
lawful public summaries; never commit full proprietary research to fixtures.

The toolbox owns deterministic screening, comparison and audit mechanics. This
desk owns APAC interpretation, source-ranking review, routing and reader-facing
output. Agreement between separate agents or tools does not create independent
evidence when the underlying sources share an independence group.

## Bundled event-driven research

Merger arbitrage, special situations and deal monitoring are native desk skills.
They do not depend on the standalone Event Driven Desk plugin. The offline
`scripts/merger_arb.py` helper consumes `merger_arb/v1` and emits
`merger_arb_result/v1`; see `event-driven/calculations.md`. Research watchlist
snapshots use `event_watchlist/v1` from `event-driven/output-contracts.md`.
The six focused radar, document, sensitivity, consideration-model, historical-test
and alert workflows use `scripts/event_tools.py` and `scripts/event_backtest.py`.
See [toolkit contracts](event-driven/toolkit.md) for their explicit inputs and examples.
None is a live quote feed, broker integration or background scheduler.
Keep Bloomberg/OpenBB field lineage and primary-source transaction terms under
the same policy as the rest of this desk. Declared unsupported structures require
an explicit payoff model rather than being forced into a fixed exchange ratio.

## Adding an adapter

Keep credentials in environment variables or the provider's authenticated connector. Add a small read-only collector outside the core calculation helpers, normalize its output, and add fixture-based tests. Never add order-routing capabilities to this plugin.
