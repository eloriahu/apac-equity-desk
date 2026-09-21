---
name: topic-radar
description: Find timely APAC equity topics from requests such as what is moving, sector radar, find me a topic, or what should I write about, ranking observed sector moves before investigating causes.
---

# Topic Radar

Use this when the user needs a timely subject for a market update or colour note.

1. Resolve the market, session and observation window. If no market is named, use the market already established in the task; otherwise ask for one.
2. Collect a broad, representative read-only quote set with sector, benchmark, volume-normal and timestamp fields. Collect fresh timestamped news separately. Do not select only names that support a pre-existing story.
3. Normalize the pack to `../../references/data-contract.md`, then run `../../scripts/pack_readiness.py --mode topic-radar`. Stop for a blocking result; disclose a limited result.
4. Run `../../scripts/topic_radar.py`. Treat its score as an attention queue, not significance, conviction or a trading signal.
5. Present the top three topics with the observed move, benchmark-relative move, breadth, volume context, leading names, data gaps and a one-line research question.
6. For the selected topic, apply `../market-color/SKILL.md` and `../catalyst-analysis/SKILL.md`. Fresh news is a lead to test, never proof that it caused the move.

If no sector clears two useful signals, say the tape is diffuse and list the strongest observation without manufacturing a theme. Every output states its as-of time and remains `DRAFT — HUMAN APPROVAL REQUIRED`.
