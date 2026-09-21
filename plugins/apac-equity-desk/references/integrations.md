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

## Adding an adapter

Keep credentials in environment variables or the provider's authenticated connector. Add a small read-only collector outside the core calculation helpers, normalize its output, and add fixture-based tests. Never add order-routing capabilities to this plugin.
