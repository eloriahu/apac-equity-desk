---
name: expectations-change
description: Explain APAC company consensus or analyst-model revisions across two dated snapshots. Use for what changed in expectations, estimates after results, consensus drift, or what is priced in; distinguish revisions from earnings surprise and stock reaction.
---

# Expectations Change

Before choosing tools, apply `../../references/tool-selection.md`, including
when this skill is invoked directly. Reuse the lead’s plan in supporting work.

Use the `expectations-analysis` module in
`../../references/research-modules.md`: read and execute the installed
`fundamental-tools:expectations-bridge` skill for the scoped evidence/calculation
assignment when available. Reuse its returned pack; a missing skill or runtime
uses the documented fallback with the same evidence requirements.

Acquire two dated snapshots for the same issuer and listing, preferring the user's Bloomberg/model exports. Check provider, contributor population, fiscal period, reported/adjusted basis, currency, units and statistic. If available, consume AI Toolbox `expectations_bridge/v1`; otherwise calculate and document a like-for-like bridge under `../../references/research-contracts.md`. Treat new, dropped or unmatched estimates as coverage changes, not zero-value revisions.

Explain what actually changed and when, then compare separately with company guidance, reported results and the market's move. Do not infer market expectations from price action alone. A full spreadsheet model or comps/DCF artifact belongs to Public Equity Investing when available. Run source verification and desk editing; preserve the draft approval banner.
