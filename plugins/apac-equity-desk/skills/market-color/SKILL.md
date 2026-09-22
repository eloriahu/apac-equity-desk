---
name: market-color
description: "Explain why an APAC stock or sector is up or down using a lean composite investigation: tape and peer-relative move, company news, regulation/policy, peers and industry, sentiment/chatter, a concise fundamental hook, implications and watch points. Use for ordinary natural-language questions such as 'XXX stock is up, why?' without requiring manual skill selection."
---

# Market Color

Read `../../references/desk-defaults.md` for short-request routing, context/date defaults and the included review stages. The user does not need to repeat these instructions or request each pass.

Produce a draft that a sell-side analyst can verify quickly. Read `../../references/source-priority.md`, `../../references/house-style.md` and the market-colour section of `../../references/data-contract.md`.

## Build the evidence pack first

Resolve the security, listing, session and as-of time. Prefer user-supplied Bloomberg exports or screenshots for prices, peers, intraday context, volume and flow fields. Use OpenBB for missing, stale or absent market fields. Use company/exchange disclosures for announcements and configured specialist sources for breadth, flows or macro timing; disclose every coverage gap and delayed observation.

Read `../../references/integrations.md` before selecting or combining sources. Preserve field-level lineage and material conflicts.

Collect only what is material, but cover each evidence lane before concluding:

- price move today and prior session; volume/turnover versus 20-day normal; VWAP/range/levels
- sector and benchmark median moves; index contribution when available
- A/H/ADR or related-listing comparison using aligned timestamps and FX
- fresh company/exchange announcements and established company-specific reporting
- relevant regulatory, policy, macro and input-price events with a plausible timing/mechanism link
- peers, customers, suppliers and specialist industry evidence that test whether the move is shared or idiosyncratic
- flow, positioning, technical and sentiment evidence as possible contributors, never substitutes for a causal mechanism
- material social chatter only as Level 4 evidence, plus any company response
- the smallest fundamental bridge needed to explain the move: revenue, cost, cash flow, balance-sheet risk or valuation/expectations

Normalize quote rows to the shared contract. Use `../../scripts/relative_moves.py`, `movers.py`, `ah_premium.py` and `news_cluster.py` for calculations rather than mental arithmetic. Collect the move, relative context, evidence-ranked explanations, flow/technical context, read-through, watch points, sources, as-of time and data gaps. Use the theme or legacy single-stock schema in the data contract; presentation need not repeat the internal field labels.

This triage is part of market-color itself. Do not require the user to invoke a
news, sentiment, fundamentals or implications skill. Do not expand the concise
fundamental bridge into a full company review unless the question actually
turns on multi-period financials or valuation and that additional work could
change the answer.

## Decide whether there is real colour

Treat a move as investigation-worthy when any two signals are present: absolute move above 3%, sector-relative move above 2ppt, volume above 1.8× normal, material index contribution, fresh announcement, large related commodity move, estimate revision, material policy headline, A/H divergence above the desk threshold, or unusual flow. User-requested names may still be analyzed below the threshold; call it below the desk trigger rather than statistically insignificant, since these thresholds are not a statistical test.

Rank proposed drivers with the evidence score in `source-priority.md`, computed with `../../scripts/evidence_score.py` so the arithmetic and bands are consistent. Separate confirmed session catalyst, plausible contributing factor, structural background already known and unconfirmed chatter. If no driver clears medium confidence, say `No single catalyst is confirmed` and describe the best-supported possibilities. Correlation, co-movement and headline timing are not proof of causation.

## Draft and challenge

Default to `format: desk-theme` for developed stock/sector commentary. Start with a punchy theme headline and verified desk tickers on separate lines. Follow with narrative paragraphs weighing fresh catalysts against valuation/positioning or rebound explanations, then the fundamental hook. Include implications only when the evidence supports a specific exposure or changes what the reader should watch; keep speculative candidates separate from the explanation of the observed move. Use short lists for mixed demand evidence, useful cross-market implications and dated Things to watch. Explain each related stock's specific exposure, not merely that it "could follow".

Do not automatically run a full idea funnel. Use `../idea-funnel/SKILL.md` only
when the user asks for ideas, beneficiaries/losers or a candidate screen, or
when an evidence-supported cross-market chain is central to the requested
answer. Do not automatically use agents for one name. Escalate only when the
criteria in `../../references/intent-routing.md` are met.

Verify each ticker/company/listing, especially pasted Bloomberg strings; flag suffix mismatches rather than silently rewriting them. Taiwan themes are in scope when evidence/data is available, but no Taiwan provider is added by this skill.

Keep source rank and causal confidence in the evidence pack and express uncertainty naturally in prose. A confirmed company response does not automatically become a confirmed price driver. Preserve counterevidence and release/comparison distortions.

Use `../../scripts/render_market_color.py` with the selected schema. Developed colour is roughly 180–350 words; use 90–180 for an explicitly requested flash. The legacy labelled single-stock layout remains available when requested. Add the draft banner.

Before returning, read and apply `../source-verifier/SKILL.md` and `../desk-editor/SKILL.md`. Run the fact-check helper on any claim bundle and perform the desk-editor questions: Why today? Why this name versus peers? What is new? What contradicts the explanation? Are all numbers aligned by session and timestamp? Never publish or send the result; the user is the final approval layer.
