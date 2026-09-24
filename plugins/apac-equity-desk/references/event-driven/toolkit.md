# Event-driven toolkit

Version 1.6.0 adds six focused workflows to the APAC desk. All bundled helpers are
offline, Python-standard-library tools. They consume explicit normalized JSON,
preserve the full input and its SHA-256 fingerprint, return a draft result, reject
unknown fields, and refuse to overwrite an existing `--output` path. Monetary
values must be finite; timestamps require timezone offsets. Synthetic fixtures
are examples of input shape, never current deals or a historical track record.

The agent gathers current evidence with available search, browser and document
tools; these helpers do not scrape exchanges, authenticate filings or provide a
complete APAC deal database. Read [jurisdiction sources](jurisdictions.md),
[research standards](research-standards.md) and [calculation conventions](calculations.md).

## Run from the repository root

```shell
python plugins/apac-equity-desk/scripts/event_tools.py radar plugins/apac-equity-desk/examples/event-driven/radar.json
python plugins/apac-equity-desk/scripts/event_tools.py documents plugins/apac-equity-desk/examples/event-driven/documents.json
python plugins/apac-equity-desk/scripts/event_tools.py sensitivity plugins/apac-equity-desk/examples/event-driven/sensitivity.json
python plugins/apac-equity-desk/scripts/event_tools.py models plugins/apac-equity-desk/examples/event-driven/models.json
python plugins/apac-equity-desk/scripts/event_tools.py models plugins/apac-equity-desk/examples/event-driven/proration.json
python plugins/apac-equity-desk/scripts/event_backtest.py backtest plugins/apac-equity-desk/examples/event-driven/backtest.json
python plugins/apac-equity-desk/scripts/event_tools.py alerts plugins/apac-equity-desk/examples/event-driven/alerts.json
```

Append `--output path/to/new-result.json` to save a snapshot. Replace fixture
values with sourced observations and explicit assumptions. Missing numeric inputs
must be resolved or the dependent calculation left unavailable; do not fill gaps
with zero. A deliberately zero cost remains a user assumption.

## Input and output contracts

| Workflow | Input schema | Output schema | Example |
| --- | --- | --- | --- |
| New deal radar | `deal_radar/v1` | `deal_radar_result/v1` | [radar.json](../../examples/event-driven/radar.json) |
| Deal documents | `deal_documents/v1` | `deal_documents_result/v1` | [documents.json](../../examples/event-driven/documents.json) |
| Probability grid | `probability_sensitivity/v1` | `probability_sensitivity_result/v1` | [sensitivity.json](../../examples/event-driven/sensitivity.json) |
| Consideration models | `deal_models/v1` | `deal_models_result/v1` | [models.json](../../examples/event-driven/models.json), [proration.json](../../examples/event-driven/proration.json) |
| Historical replay | `event_backtest/v1` | `event_backtest_result/v1` | [backtest.json](../../examples/event-driven/backtest.json) |
| Local alerts | `deal_alerts/v1` | `deal_alerts_result/v1` | [alerts.json](../../examples/event-driven/alerts.json) |

Every field shown in each example is required unless explicitly nullable below.
The functions in [event_tools.py](../../scripts/event_tools.py) and
[event_backtest.py](../../scripts/event_backtest.py) enforce the input contracts.
Inputs and hashes support reproduction; they do not prove source authenticity.

### Radar

Declare `as_of`, `since`, actual source `coverage`, market and event-type filters.
Each record has a canonical deal ID, market, event type, status, title, source URL,
`official`/`secondary` source type, publication/observation times, boolean analyst
verification and a `terms` object (empty if unavailable). Sources published or
observed after the cutoff are excluded. Exact duplicate records are removed;
distinct coverage remains evidence, without being counted as independent proof.
The most recent verified official record leads. Concurrent conflicting official
terms/status require review. Historical snapshots require archived observation
times, not a newly collected document retroactively assigned an old timestamp.

### Documents

`before` and `after` contain document IDs, URLs, publication times and a term map.
Every term has `value`, `status` (`known`, `unknown`, `not_applicable`) and a
nonempty `locator` naming page/section or the precise gap. Known values cannot be
null; other statuses must be null. Include amount, currency, share basis and
conditions inside a structured value. Comparison reports newly observed,
not observed in the newer document, evidence-status change, value change or
unchanged. Citation movement alone is not a changed term. This is a normalized
term comparison, not PDF OCR, legal advice or a full semantic contract parser.

### Probability sensitivity

Supply a valid `base_deal` in `merger_arb/v1` with exactly one close and one break
state, and arrays `close_probabilities`, `break_prices`, `close_days`. The grid
varies those three dimensions only, up to 10,000 cells. Break timing, acquirer
exit values and other assumptions remain fixed. Each cell returns both net P&Ls,
EV, return on supplied capital and the unclipped two-state break-even threshold.
The close probability is an input. No annualized expected return is inferred.

### Consideration models

Declare deal ID, dated `as_of`, base currency, target price, nonnegative annual
effective discount rate and `cost_pv` per target share. Parent scenarios need unique
names and probabilities summing to one. Each component requires `kind`, integer
`days` from valuation (zero allowed), positive `fx_to_base` and `source_locator`.
FX means units of base currency per unit of component currency at that scenario's
cash-flow date. Cite the component's currency in the source pack; the FX factor
must be 1 for a base-currency cash flow.

| Component | Required economic inputs | Payoff before discount/FX |
| --- | --- | --- |
| `cash` | `amount` | Supplied cash payment or terminal break proceeds |
| `stock` | `ratio`, `settlement_price` | Ratio × settlement stock price |
| `fixed_value_collar` | `stock_value`, `reference_price`, `floor`, `ceiling`, `ratio_below_floor`, `ratio_above_ceiling`, `settlement_price` | Contract ratio × settlement stock price |
| `cvr` | `payment`, `payment_probability` | Payment × probability conditional on parent scenario |
| `proration` | `accepted_fraction`, `accepted_value`, `residual_value` | Accepted fraction × accepted value + remaining fraction × residual value |

For the supported fixed-value collar, reference price at/below the floor uses
the supplied lower-bound ratio; at/above the ceiling uses the supplied upper-bound
ratio; inside the interval uses stock value / reference price. Supply contractual
ratios with their rounding rather than assuming mathematically continuous limits.
This supports that convention only. Caps, elections, different collars or
fractional-share cash-in-lieu need a separately reviewed extension.

For each component: `PV = payoff × FX / (1 + rate)^(days / 365)`.
Scenario NPV is summed component PV less target price and cost PV. Expected NPV
weights scenario NPVs once. CVR probability is conditional, not another
unconditional completion probability. For dependent/exclusive milestones use
joint parent scenarios; discount each payment at its own date. For prorated
proceeds realized on different dates, use separate components. This output is
valuation NPV, not financing-adjusted or dynamically hedged trading P&L.

The distinction between reference VWAP and settlement price is illustrated by
[CoStar's 2024 transaction disclosure, Item 1.01](https://www.sec.gov/Archives/edgar/data/1057352/000119312524103937/d828310d8k.htm).
Actual contracts govern each deal; the toolkit does not hardcode this issuer's terms.

### Historical testing

The prototype replays supplied decisions; it does not discover trades. Declare
initial capital, idle-cash rate, entry/exit transaction costs in bps (including
assumed slippage), maximum per-trade fraction of pre-entry NAV, currency, policy,
coverage, chronological splits, session rows and trades. The policy has a
`frozen_at` before the first sample date, selection/sizing rules and benchmark
description. Coverage names the universe/source, survivorship limitations and
excluded deals with reasons.

Sessions have ascending distinct dates, positive total-return benchmark levels
and nonnegative marks keyed by deal ID. Every open deal requires a mark at each
supplied session, including exit. No silent forward fill is performed. Declare
the session calendar and omissions in coverage; the engine cannot detect a whole
missing market session or verify a provider's historical adjustments.

Trades contain source URL/time, signal time, execution timestamp/price, allocation,
cash-available settlement/exit date and price, and outcome. Source availability
must precede or equal the signal, which must strictly precede entry. For an
unresolved deal both exit fields are null and its final mark remains in NAV.
`completed`, `failed` and `withdrawn` require dated exits. Outcome labels are used
only for reporting, never selection or sizing. Audit supplied allocations and
signals for hindsight separately; timestamp validation cannot establish an
unbiased historical universe.

Allocation includes entry costs: shares = allocation / (execution price ×
(1 + entry cost rate)). Exit proceeds less exit costs return to cash on exit_date.
Exits process before same-day entries, meaning proceeds are assumed available
for reuse then; supply actual cash-availability dates. Idle cash accrues over
calendar days. End-session NAV is cash plus marked long positions. Same-day
entries share one pre-entry NAV concentration denominator, using prior-session
marks for existing holdings and available cash. Today's closing prices cannot
expand an intraday entry limit. Session dates and execution timestamps must use
the same local market date basis. Excess allocation
fails instead of silently adding leverage. No reinvested profit changes the
user-supplied allocation rules.

The engine supports one-currency, fully funded long-only, fractional-share
positions. No shorts, borrow, leverage, taxes, transaction settlement ledger or
market-impact model. Marks and exit values must consistently incorporate cash
distributions, with entry prices on the matching share basis. The daily NAV is
not a genuine mark-to-market ledger if the supplied series violates that
convention. These limitations must accompany results.

Train/validation/test summaries are chronological reporting segments of a frozen
policy; positions carry across boundaries. Segment returns link to total return.
Drawdown uses observed session NAV, including entry costs, and can miss intraday
losses. No fitted-model, Sharpe, CAGR or out-of-sample skill claim is manufactured
from a small replay. Bankruptcy leaves subsequent percentage returns undefined.

### Alerts and persisted state

`previous` may be null; `current` requires deal ID, timezone-aware `as_of`, status,
normalized terms object, target price, consideration and deadline. Prices and
deadline can be null. The evaluation's `as_of` cannot precede a snapshot or the
state's prior evaluation. Use canonical statuses; `completed`, `settled`,
`withdrawn`, `terminated`, `lapsed` suppress ongoing deadline/data-freshness alerts.

Rules have positive `spread_widening_bps`, `deadline_days`, `stale_hours`. Spread
is `(consideration / target_price - 1) × 10,000`; widening compares the two supplied
snapshots. It is not a net spread after financing and borrow. Terms, status,
consideration and deadline changes are emitted with their before/after values.
Source URLs/quote timestamps belong in the associated research evidence pack.

First state: matching deal ID, null `evaluated_at`, empty `active` and
`seen_changes` arrays. The helper returns deterministic event IDs and `next_state`.
Persist it together with the current snapshot before the next serialized run.
Retries using the saved state suppress duplicate changes; persistent conditions
emit only on activation and rearm after clearing. Keep the full change history
for the monitored deal; deleting it forfeits duplicate suppression.

This is evaluation only. It installs no scheduler, sends no notifications and
creates no brokerage alerts. An explicitly requested monitor uses the host's
automation service, its saved state and the specified data sources/cadence.
Stay quiet on unchanged/non-actionable runs; report meaningful changes, failures
or required user action. External delivery requires explicit user instruction.
