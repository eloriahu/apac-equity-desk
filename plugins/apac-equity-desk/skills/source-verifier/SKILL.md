---
name: source-verifier
description: Audit APAC finance claims and citations from requests such as check this, including timestamps, source support, numerical conflicts and causal wording.
---

# Source Verifier

Read `../../references/desk-defaults.md` for short-request routing, context/date defaults and the included review stages. The user does not need to repeat these instructions or request each pass.

Read `../../references/source-priority.md` and the fact-check schema in `data-contract.md`. Decompose the draft into atomic factual and causal claims. For each claim verify the cited source actually supports it, source level, publication/event time, primary-versus-repost status, units/currency/session and whether subsequent information superseded it.

Run `../../scripts/fact_check.py` on a structured claim bundle. For live claims, attach the quote/observation time as source `observed_at` and a claim-specific `max_age_minutes`; do not apply an arbitrary freshness limit to filings or structural background. Repeated numeric claims should share a `fact_key` and carry `unit`, `currency` and `session` where relevant. Escalate: uncited facts, causal statements resting only on Level 4 material, contradictory numeric values, stale live data, non-overlapping timestamps, unattributed estimates and circular sourcing. Return `pass`, `revise` or `block`, with minimal corrections. Verification does not authorize publication.
