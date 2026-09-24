# Calculator conventions

Run Python 3.10+ from the plugin root:

```sh
python scripts/merger_arb.py examples/event-driven/cash-deal.json
python scripts/merger_arb.py input.json --output dated-result.json
```

No network or third-party Python packages. Output creation refuses to overwrite an
existing snapshot. Supply `merger_arb/v1` JSON as shown in the examples. Unknown
numeric/model fields are rejected; provenance can go in `sources` and `notes`.

All monetary inputs use **one currency, per target share**, except acquirer price
and dividend which are per acquirer share. Ratios are acquirer shares per target.
Rates are decimals (0.05 = 5%); days are positive integer calendar days to cash
settlement or exit. `as_of` records the observation cutoff; `sources` should preserve
quote timestamps, terms documents and assumption rationale. The calculator checks
arithmetic input validity, not source accuracy/freshness or legal applicability.

Inputs explicitly include cash, ratio, target/acquirer price, hedge ratio, positive
`capital_base`, `financed_amount`, funding/borrow/rebate rates and round-trip
transaction cost. Zero is an explicit assumption, not a substitute for unknown data.
Each scenario requires name, close/break, days, acquirer exit, cash adjustment,
target/acquirer dividends and additional cost. Break scenarios also require target
exit. Probabilities are either omitted everywhere or supplied everywhere and sum to 1.

Let T/A be opening target/acquirer prices, C cash, r contractual ratio, h shares
shorted, A1 terminal acquirer price, K capital denominator and d calendar days:

```text
Indicative consideration = C + r*A
Gross spread = C + r*A - T
Close price P&L = C + cash_adjustment + r*A1 - T + h*(A-A1)
Break price P&L = target_exit - T + h*(A-A1)
Dividend cash flow = target_dividend - h*acquirer_dividend
Funding cost = financed_amount * funding_rate * d/365
Borrow cost = h*A * borrow_rate * d/365
Rebate income = h*A * rebate_rate * d/365
Net P&L = price P&L + dividends - funding - borrow + rebate - transaction - additional
Holding return = Net P&L / K
Simple annualized = Holding return * 365/d
Compounded annualized = (1 + Holding return)^(365/d) - 1
```

For fixed mixed consideration the full hedge is **h = r**, with no second
cash/stock weighting. A partial hedge leaves `(r-h)` acquirer exposure on close;
on break both securities matter. Static opening-notional borrow/rebate is an
approximation; path-dependent costs, changing margin and recall risk need separate
analysis. `capital_base` must include the analyst's chosen capital/margin basis;
short proceeds do not automatically reduce funded capital. Financing costs and
opportunity-cost hurdles are distinct. Rates/capital stay constant within a scenario.

Target dividends and contractual offer-price reductions are separate: a dividend
of 1 and offer adjustment of -1 cancel before tax. Additional costs may represent
explicit tax/slippage/other costs. Do not count the same cost twice. All terminal
values are ex-dividend; intermediate receipts are aggregated without reinvestment.
Annualization is a convention, not a cash-flow IRR or guaranteed repeatable return.

Expected P&L uses user probabilities and signed net outcomes. Never annualize the
weighted expected return using an average resolution date; durations can differ.
For exactly one close and one break, the script reports `-break_pnl/(close_pnl-break_pnl)`
as the undiscounted net-P&L break-even threshold, even with different scenario costs.
It is not a true completion probability. Out-of-range results remain visible, not
clipped. When both payoffs are equal the threshold is undefined. Losses below -100%
of supplied K make compounded annualization undefined and are left null.

Unsupported: collars, floating ratios, elections/proration, CVRs, FX risk, options,
dynamic hedges, path-dependent financing and automatic sizing. Build explicit
payoff/cash-flow models for these; do not relabel them as supported structures.

The calculator returns a structured research draft. It does not use the market
colour/earnings pack-readiness schema. Assess deal-term and quote freshness before
building the input, and apply source-verifier/desk-editor to the resulting memo.
