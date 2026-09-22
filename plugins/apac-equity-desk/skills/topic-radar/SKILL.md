---
name: topic-radar
description: Find timely APAC equity topics from requests such as what is moving, sector radar, find me a topic, or what should I write about, ranking observed sector moves before investigating causes.
---

# Topic Radar

Use this when the user needs a timely subject for a market update or colour note.

1. Resolve the market, session and observation window. APAC means China, Hong Kong, Japan, Korea, Taiwan, Australia, New Zealand, India and Southeast Asia to the extent the supplied/configured sources cover them. If no market is named and none is established, default to the supported APAC region rather than HK alone.
2. Read `../../references/integrations.md`. Prefer a user-supplied Bloomberg export or screenshot. Accept screenshots as first-class inputs, transcribe only visible values, and preserve the screen's timestamp separately from upload time. Use OpenBB only for missing, stale or absent market fields. Collect fresh timestamped news separately. Do not select only names that support a pre-existing story.
3. Normalize the pack to `../../references/data-contract.md`, set `expected_market_timestamp` from `../../scripts/session_clock.py`, then run `../../scripts/pack_readiness.py --mode topic-radar`. A live quote older than the market's latest tradable time or a capture window wider than the declared tolerance blocks the draft. Stop for a blocking result; disclose a limited result.
4. Run `../../scripts/topic_radar.py`. Treat its score as an attention queue, not significance, conviction or a trading signal.
5. Present the top three topics with the observed move, benchmark-relative move, breadth, volume context, leading names, data gaps and a driver assessment. A label such as `AI`, `risk-on` or `policy hopes` is incomplete without a dated trigger and transmission mechanism. If no driver is supported, state `No single catalyst is confirmed`, rank the plausible factors and give a one-line research question.
6. For the selected topic, apply `../market-color/SKILL.md` and `../catalyst-analysis/SKILL.md`. Fresh news is a lead to test, never proof that it caused the move.

If no sector clears two useful signals, say the tape is diffuse and list the strongest observation without manufacturing a theme. Every output states its as-of time and remains `DRAFT — HUMAN APPROVAL REQUIRED`.
