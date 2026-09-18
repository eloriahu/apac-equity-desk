---
name: market-color
description: Investigate and draft concise, evidence-ranked intraday colour for an APAC equity or sector move. Use for “why is it moving?”, unusual price/volume, A/H divergence, or trader-ready colour; not for order execution.
---

# Market Color

Produce a draft that a sell-side analyst can verify quickly. Read `../../references/source-priority.md`, `../../references/house-style.md` and the market-colour section of `../../references/data-contract.md`.

## Build the evidence pack first

Resolve the security, listing, session and as-of time. Prefer Longbridge read-only quote, candle, trade, capital-flow, announcement and news tools where supported and entitled. Use configured AKShare/Tushare for China breadth or cross-checks and Jin10 for macro timing; disclose coverage gaps and delayed data.

If the primary source is unavailable or an adapter must be configured, read `../../references/integrations.md` before selecting a fallback.

Collect only what is material:

- price move today and prior session; volume/turnover versus 20-day normal; VWAP/range/levels
- sector and benchmark median moves; index contribution when available
- A/H/ADR or related-listing comparison using aligned timestamps and FX
- fresh company/exchange announcements, established reporting and specialist industry data
- relevant input prices, policy/macro releases and dated prior catalysts
- material social chatter only as Level 4 evidence, plus any company response

Normalize quote rows to the shared contract. Use `../../scripts/relative_moves.py`, `movers.py`, `ah_premium.py` and `news_cluster.py` for calculations rather than mental arithmetic. Do not draft until the pack has a `what`, `relative`, `catalysts`, `flow_technical`, `read_through`, `watch`, `sources`, `as_of` and `data_gaps` field.

## Decide whether there is real colour

Treat a move as investigation-worthy when any two signals are present: absolute move above 3%, sector-relative move above 2ppt, volume above 1.8× normal, material index contribution, fresh announcement, large related commodity move, estimate revision, material policy headline, A/H divergence above the desk threshold, or unusual flow. User-requested names may still be analyzed below the threshold; say the move is not statistically unusual.

Rank proposed drivers with the evidence score in `source-priority.md`. Separate confirmed session catalyst, plausible contributing factor, structural background already known and unconfirmed chatter. If no driver clears medium confidence, say `No single catalyst is confirmed` and describe the best-supported possibilities. Correlation, co-movement and headline timing are not proof of causation.

## Draft and challenge

Use `../../scripts/render_market_color.py` when the pack conforms to the contract. Keep a flash to roughly 90–180 words. Lead with the move and relative spread, then catalyst confidence, flow/technical context, read-through and the next confirming or invalidating signal. Add the draft banner.

Before returning, run the fact-check helper on any claim bundle and perform the desk-editor questions: Why today? Why this name versus peers? What is new? What contradicts the explanation? Are all numbers aligned by session and timestamp? Never publish or send the result; the user is the final approval layer.
