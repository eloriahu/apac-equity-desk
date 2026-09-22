# Research interchange contracts

APAC Equity Desk consumes these JSON-compatible packs by schema. AI Toolbox may
produce them, but the desk must not import its source tree, assume its local
path or require it at runtime. Unknown fields should be preserved when a pack
is handed onward.

## `idea_funnel/v1`

Required top-level fields:

- `schema: idea_funnel/v1`
- `schemaVersion: 1`
- offset `as_of`
- `question` and nonempty `scope`
- nonempty `sources` and `claims`
- `causal_chain`, `causal_gate`, `bottlenecks`, `screen_profiles`,
  `candidates`, `ranking` and `quality`

Every causal link uses `supported`, `disputed`, `unsupported` or `unknown`, has
`required` (default `true`) and retains source IDs and counterevidence.
`causal_gate` contains `state: pass|blocked`, `blocking_link_ids` and `rule`;
any required link not `supported` blocks all ranking. Every candidate has a
stable ID, entity name, primary symbol, exchange, supply-chain position,
evidence-backed exposure, screen results, valuation/expectations context,
catalysts/falsifiers, `rankable`, `rankability_reasons` and a disposition of
`advance`, `watch` or `reject`. Rejections keep a reason.

Screen profiles contain sector/profile-specific rules and thresholds. Each
rule result is `pass`, `fail`, `insufficient` or `not_applicable`; no universal
quality threshold is implied. Ranking rows retain `rank`, `candidate_id`,
`score` and `evidence_coverage`. Only `rankable: true` candidates may receive a
rank. `quality.status` is `ready`, `limited` or `blocked` and carries missing
inputs, conflicts, warnings and checks.

The score orders research attention. It is not a recommendation, probability
or substitute for the causal-chain evidence.

## `research_review/v1`

Required top-level fields:

- `schema: research_review/v1`
- `schemaVersion: 1`
- offset `as_of`
- `entity`
- nonempty `sources` and `claims`
- `researchability`, `management_ledger`, `thesis_drift`, `number_audit`,
  `publication_gate` and `quality`

`researchability.grade` is `A`, `B` or `C` and
`maximum_supported_confidence` is `high`, `medium` or `low`. This grades the
evidence environment, not the company.

Management-ledger rows retain the original dated commitment and its source,
measurement window, outcome and status: `delivered`, `partial`, `missed`,
`pending`, `withdrawn` or `unclear`. A measured outcome uses separate
`measurement.source_ids`; qualitative or partial assessments carry their own
source IDs and rationale. The original promise cannot verify its own outcome.

Thesis changes use `fact`, `price`, `wording` or `no_change`; `primary_class`
uses the same values. `comparison_status` is `complete` or
`limited_no_baseline`; `substantive_state` is `facts_changed`,
`valuation_changed` or `unchanged`. Each change preserves the prior and current
value; changed facts retain source IDs in the current value. The review-level
`effect_on_conclusion` records direction, rationale and source IDs for the
supported effect on the thesis.

Number-audit rows identify the claim/field, value, unit, currency, period,
basis, source and status `pass`, `fail` or `unverifiable`. The publication gate
is `pass`, `blocked` or `not_run`; a critical failed or unverifiable number used
in a key conclusion blocks publication. `quality.status` is `ready`, `limited`
or `blocked`.

## Consumption rules

- Each source has `id`, `origin` and `independence_group`; each claim has `id`,
  `statement`, `source_ids` and optional `status`/`type`. Use the shared registry
  across all routes and agents. Reposts, syndicated stories and calculations
  derived from one underlying item remain one independence group.
- Validate schema and version before use; an unknown major version is a gap.
- Preserve provider/source IDs, timestamps, currencies, periods and bases.
- Do not upgrade `limited` or `blocked` because prose sounds convincing.
- Apply this desk's independent source ranking and semantic claim review.
- Deterministic checks prove matching/calculation, not economic causation.
- Keep collection/calculation separate from APAC interpretation and writing.
