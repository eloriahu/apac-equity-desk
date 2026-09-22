---
name: idea-funnel
description: Discover and rank APAC equity candidates from a theme, structural trend, event or bottleneck. Use automatically for questions such as who benefits, who loses, find ideas, screen this theme, bottleneck scan or turn this trend into listed-company candidates; do not activate for a simple why-it-moved question unless candidate discovery is central.
---

# APAC Idea Funnel

Start from the user's question, not a stock list. Read
`../../references/intent-routing.md`, `../../references/source-priority.md`,
`../../references/integrations.md` and the `idea_funnel/v1` section of
`../../references/research-contracts.md`.

## Establish the causal chain

Write the hypothesized chain as separately testable links:

`structural trend or event -> incremental demand/cost change -> constrained or advantaged activity -> earnings sensitivity -> listed exposure -> possible repricing catalyst`

For each link use `supported`, `disputed`, `unsupported` or `unknown`, mark
whether it is required, attach source IDs and record counterevidence. Any
required link that is not supported blocks ranking through `causal_gate` and
must appear in `blocking_link_ids`. A popular theme is not evidence that the
listed company earns from it.

## Find the scarce or decisive node

Test bottlenecks and beneficiary mechanisms using supplier concentration,
capacity/utilisation, expansion lead time, qualification time, substitution,
regulation, pricing power and demand-versus-capacity growth. Also test how the
bottleneck could disappear. Distinguish physical scarcity from temporary
inventory, narrative scarcity and simple share-price correlation.

## Build and narrow the universe

Map direct and second-order exposures across relevant APAC listings, related
ADRs and global peers where they establish the economics. Retain an audit trail
for every candidate:

- entity name, primary symbol, exchange, liquidity caveat and supply-chain position;
- revenue/profit exposure and business purity, with evidence rather than labels;
- expected earnings sensitivity, operating leverage and balance-sheet constraints;
- sector-appropriate quality screen and any `insufficient` or `not_applicable` tests;
- what expectations/valuation appear to embed, with market-data timestamp;
- dated catalyst, confirmation, falsifier and strongest counterevidence;
- `rankable`, `rankability_reasons` and disposition `advance`, `watch` or
  `reject`, including the rejection reason.

Do not hard-code one ROE, margin, leverage or dividend threshold across banks,
insurers, property, cyclicals, commodity producers and technology companies.
Select a declared sector/profile rule set and preserve its thresholds in the
pack.

For a structural-growth or category-leader question, also test industry
penetration/stage, market-share direction, pricing power, quarterly financial
progression, dated high-frequency operating indicators, announced supply and
overcapacity risk, and the growth required by the current valuation. Treat
shipments, monthly revenue, tenders, utilisation or channel data as supporting
indicators with explicit methodology—not as substitutes for reported earnings.

When AI Toolbox is available, consume `idea_funnel/v1` by schema; never import
or assume its repository path. Recheck material claims under this desk's source
hierarchy. A `limited` or `blocked` pack constrains the output regardless of its
ranking score, and a candidate with `rankable: false` cannot appear in a ranked
top list.

## Output

Lead with the causal chain and whether it survives. Then show the bottleneck or
other decisive economic node, the narrowed candidate table, ranked ideas and
exclusions. Ranking rows must retain `candidate_id`, score, evidence coverage
and rank; explain score drivers rather than presenting the score as truth.

Separate direct beneficiaries, second-order read-through and speculative
watchlist names. For every advanced candidate state what is priced in, why the
variant view could matter, the horizon, next evidence and invalidation. Zero
advanced ideas is a valid result.

Use `../source-verifier/SKILL.md` and `../desk-editor/SKILL.md`. Keep the human
approval banner. No sizing, personalized portfolio advice, execution or orders.
