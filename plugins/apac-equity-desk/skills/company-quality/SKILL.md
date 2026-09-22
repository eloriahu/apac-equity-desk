---
name: company-quality
description: Evaluate an APAC listed company's sector-aware operating quality or dividend/income durability. Use for quality screens, cash-conversion questions, balance-sheet resilience, dividend safety, payout sustainability or income research; exclude personal portfolio sizing.
---

# Company Quality and Income

Resolve the company, sector, fiscal basis, horizon and whether the user wants
operating quality, income durability or both. Read the fundamental contract in
`../../references/data-contract.md`, the idea funnel contract in
`../../references/research-contracts.md` and `../../references/source-priority.md`.

Choose and disclose a sector/profile screen. Do not apply industrial-company
ROE, leverage, interest-cover or free-cash-flow thresholds unchanged to banks,
insurers, REITs, property developers, commodity producers, regulated utilities
or early-stage growth companies. Each rule must report `pass`, `fail`,
`insufficient` or `not_applicable`, with the tested period, basis and threshold.

For operating quality, test the supported subset of returns on capital, margin
structure, cash conversion, reinvestment, working capital, leverage, dilution,
cyclicality, customer/supplier concentration and accounting quality. Explain
what drives the result rather than collapsing it into one score.

For income durability, distinguish the current yield from sustainable
distribution capacity. Test payout basis, free cash flow or sector-appropriate
coverage, balance-sheet headroom, refinancing, capex/reinvestment needs,
cyclicality, policy/regulatory constraints, dilution and management's stated
capital-allocation priorities. Run downside conditions that could force a cut;
do not call a high historical yield safe by default.

Consume `fundamental_pack/v1` and, where a screen produced it,
`idea_funnel/v1` by schema from AI Toolbox. Preserve source and calculation
lineage; a missing denominator produces `insufficient`, not a guessed value.

Return the sector/profile used, the rule-by-rule evidence, the quality or
income conclusion, counterevidence, sensitivity and next evidence. Run
source-verifier and desk-editor. This is company research, not a personalized
income recommendation; do not size a position or use personal holdings.
