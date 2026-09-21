---
name: earnings-review
description: Review APAC company earnings from requests such as earnings review, results colour, actual versus consensus, or what changed after results, with surprise calculations and evidence gates.
---

# Earnings Review

Resolve the company, listing, reporting period, currency, accounting basis and as-of time. Prefer the company filing and presentation for actuals, and attribute every consensus figure to its provider and retrieval time.

Build rows for revenue, operating profit, net income, EPS, margins, segment results and guidance as available. Run `../../scripts/earnings_surprise.py`; do not calculate surprises mentally. Reject mixed units, currencies, GAAP/non-GAAP bases or periods rather than comparing them. Run `../../scripts/pack_readiness.py --mode earnings` before drafting.

Write: headline result; actual versus consensus; segment and margin drivers; guidance and management language; estimate/valuation implications; peer and supply-chain read-through; next dated watch points. Separate reported facts, management guidance, consensus, analyst inference and market reaction. Use `../source-verifier/SKILL.md` and `../desk-editor/SKILL.md`, and keep the draft approval banner.
