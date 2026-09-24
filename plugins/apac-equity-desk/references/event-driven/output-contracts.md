# Research outputs

## Memo

Lead with the research stance and reason. Include as-of, security, jurisdiction,
stage, terms/sources, aligned quotes, gross spread, hedge, costed scenarios,
remaining conditions, milestones, downside/probability rationale, counterargument,
falsifier, next action and material gaps. Keep screens short; expand deep dives.

## Watchlist files

Use `event_watchlist/v1` with `as_of`, `universe`, `coverage_limitations`, `deals`.
Each deal: `deal_id`, `target`, `acquirer`, `security`, `jurisdictions`, `status`,
`terms`, `quotes`, `conditions`, `milestones`, `scenarios`, `research_stance`,
`thesis_state`, `falsifiers`, `missing_inputs`, `sources`.
Quotes carry provider, observation timestamp/timezone, currency and unit. Sources
carry id, URL/file, document/retrieval dates and page/section. Facts reference source
ids; assumptions also carry rationale. Use null/unknown for gaps. Stable deal IDs
include issuer/security identity and announcement date.

Write dated files to the user's research workspace, not installed plugin folders;
preserve old versions. This is an output convention, not a live database. The
calculator uses its own smaller `merger_arb/v1` input, not the watchlist format.
Updates: field | previous | current | source | implication.
Calendar: deal | milestone | date/window | timezone | certainty | source.
