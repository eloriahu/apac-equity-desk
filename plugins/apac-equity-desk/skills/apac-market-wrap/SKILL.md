---
name: apac-market-wrap
description: Run a complete country close or regional APAC wrap from short requests such as Japan wrap, HK close or China EOD, including fresh session data, house-style drafting, source checks and editing.
---

# Apac Market Wrap

Read `../../references/desk-defaults.md` for short-request routing, context/date defaults and the included review stages. The user does not need to repeat these instructions or request each pass.

Build the structured data pack before prose. Read `../../references/house-style.md`, `../../references/source-priority.md`, `../../references/data-contract.md` and `../../references/market-calendars.json`. Default to the house's developed country narrative when a country is requested; use a regional digest only when requested.

## Scope and timing

Resolve the date, closed sessions and cutoff time using the shared defaults. Confirm each market's status with Longbridge `market_status`/`trading_days` when available, otherwise run `../../scripts/session_clock.py --markets CN,HK` (it knows holidays only when a verified holidays file is supplied); do not turn this into a mandatory confirmation question. Never call a still-open market “closed”. Label holidays, partial sessions, delayed data and non-overlapping FX/commodity timestamps. Longbridge is the primary read-only source where coverage/entitlements permit; approved fallbacks may fill gaps. Singapore live quotes require a fallback because Longbridge Developers does not currently supply them.

Read `../../references/integrations.md` when the primary source is unavailable or a fallback must be chosen.

## Build one pack per market

For each in-scope closed market collect:

- headline indices with close and percent move
- advancers/decliners/unchanged, up/down volume, percent above 20DMA and new highs/lows when available
- sector leaders, laggards and useful exceptions; retain enough named stock moves to explain the session rather than limiting the note to three sectors
- top index contributors/detractors and material movers, with volume/turnover context
- turnover and market-specific foreign/Stock Connect flow where available
- session catalysts: macro, policy, earnings, corporate and sector
- relevant FX, rates and commodities with aligned as-of times

Use `market_snapshot.py`, `breadth.py`, `movers.py`, `relative_moves.py`, `news_cluster.py` and `ah_premium.py` to calculate and structure the pack. A missing field must appear in `data_gaps`; do not replace it with narrative guesswork.

## Synthesize the regional story

Identify the dominant regime and dispersion rather than listing tapes. Compare what the market expected at the open with what changed during the session. Keep country-specific causes local unless evidence supports a regional transmission channel. Distinguish index-level moves from the median stock and note when a few heavyweights distort the headline index.

## Write the country narrative

Lead with index divergence and heavyweight concentration, followed by local policy/official remarks, FX and the yield curve, macro actual versus consensus, weak sectors and outperformers. Preserve detailed stock-move lists and explain exceptions. Only include paragraphs supported by that session's data. Keep breadth/flow calculations in the pack; surface them when explanatory rather than as mandatory labels.

End with Corporate Headlines, using concise company-led bullets. A supplied humorous aside can appear just before them, but never replaces factual analysis. Do not force a Tomorrow section or invent jokes.

Build `format: desk-narrative` with closed-session market blocks and use `../../scripts/render_market_wrap.py`. Put sources beside the relevant paragraphs and record missing inputs in separate review notes. Rough guide: 500–900 words per developed country wrap, adjustable to the day's information and the user's request. Fact-check and apply desk-editor before returning the draft.

The legacy `regional-summary` format remains available for explicit multi-market digest requests. Neither format authorizes publication or trading actions.
