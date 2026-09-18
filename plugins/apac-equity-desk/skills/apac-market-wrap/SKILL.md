---
name: apac-market-wrap
description: Build a structured data pack and concise end-of-day wrap for major APAC equity markets, especially China, Hong Kong, Japan, Korea, Australia and Singapore. Use for close recaps, regional wraps and country-by-country session summaries.
---

# Apac Market Wrap

Write prose only after the close pack is complete. Read `../../references/house-style.md`, `source-priority.md`, `data-contract.md` and `market-calendars.yaml`.

## Scope and timing

Confirm the requested date, closed sessions and cutoff time. Never call a still-open market “closed”. Label holidays, partial sessions, delayed data and non-overlapping FX/commodity timestamps. Longbridge is the primary read-only source where coverage/entitlements permit; approved fallbacks may fill gaps. Singapore live quotes require a fallback because Longbridge Developers does not currently supply them.

Read `../../references/integrations.md` when the primary source is unavailable or a fallback must be chosen.

## Build one pack per market

For each in-scope closed market collect:

- headline indices with close and percent move
- advancers/decliners/unchanged, up/down volume, percent above 20DMA and new highs/lows when available
- three best and worst sectors; breadth within the sector if possible
- top index contributors/detractors and material movers, with volume/turnover context
- turnover and market-specific foreign/Stock Connect flow where available
- session catalysts: macro, policy, earnings, corporate and sector
- relevant FX, rates and commodities with aligned as-of times

Use `market_snapshot.py`, `breadth.py`, `movers.py`, `relative_moves.py`, `news_cluster.py` and `ah_premium.py` to calculate and structure the pack. A missing field must appear in `data_gaps`; do not replace it with narrative guesswork.

## Synthesize the regional story

Identify the dominant regime and dispersion rather than listing tapes. Compare what the market expected at the open with what changed during the session. Keep country-specific causes local unless evidence supports a regional transmission channel. Distinguish index-level moves from the median stock and note when a few heavyweights distort the headline index.

Write only markets with a complete enough pack. Use `../../scripts/render_market_wrap.py` for the first draft, then fact-check and apply the desk-editor review. Target 450–800 words, but shorten on low-information days. End with tomorrow's scheduled catalysts/live questions and a concise data-gap note. Keep the draft banner and require human approval before publication.
