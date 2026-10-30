---
name: earnings-review
description: Review APAC company earnings from requests such as earnings review, results colour, actual versus consensus, or what changed after results, with surprise calculations and evidence gates.
---

# Earnings Review

Before choosing tools, apply `../../references/tool-selection.md`, including
when this skill is invoked directly. Reuse the lead’s plan in supporting work.

Read `../../references/integrations.md` for market/consensus source policy and
`../../references/research-addons.md` when retrieving or converting filings,
presentations and workbooks. Verify extracted figures in their originals.

Read `../../references/research-planning.md` and its earnings default before
collecting data. Automatically use the installed
`fundamental-tools:fundamental-research` skill for scoped period normalization,
segment/margin drivers and earnings/cash quality. Read that skill, prepare its
inputs and execute its relevant helpers; naming it is not completion. Consume
`fundamental_pack/v1` under `../../references/data-contract.md`, mapping relevant
actuals and comparisons into the desk’s earnings rows rather than passing the
whole pack to an incompatible helper. If unavailable, perform the supported
analysis locally and retain the gap. An explicitly EPS-only request stays narrow.

Add the expectations, filing-change, management/audit or beneficiary modules in
`../../references/research-modules.md` only when needed for a material subquestion,
and require their actual baselines. Revise the plan when results reveal a new
issue, such as weak cash conversion beneath an earnings beat. Preserve module
readiness and explain which limitations affect this review; absent DCF inputs
do not require inventing a valuation for a statement-only assignment.

Resolve the company, listing, reporting period, currency, accounting basis and as-of time. Prefer the company filing and presentation for actuals, and attribute every consensus figure to its provider and retrieval time.

Build rows for revenue, operating profit, net income, EPS, margins, segment results and guidance as available. Run `../../scripts/earnings_surprise.py`; do not calculate surprises mentally. Reject mixed units, currencies, GAAP/non-GAAP bases or periods rather than comparing them. Run `../../scripts/pack_readiness.py --mode earnings` before drafting.

Write: headline result; actual versus consensus; segment and margin drivers; guidance and management language; estimate/valuation implications; peer and supply-chain read-through; next dated watch points. Separate reported facts, management guidance, consensus, analyst inference and market reaction. Use `../source-verifier/SKILL.md` and `../desk-editor/SKILL.md`, and keep the draft approval banner.
