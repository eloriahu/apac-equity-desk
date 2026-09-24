---
name: historical-testing
description: Replay a supplied point-in-time event-driven trade sample with daily portfolio NAV, transaction costs, locked capital, failed deals and chronological segments. Use for historical merger-arb testing and backtests; not a live performance claim or automated strategy optimizer.
---

# Historical Testing

Read [research standards](../../references/event-driven/research-standards.md),
[toolkit contracts and examples](../../references/event-driven/toolkit.md), and
[market data integrations](../../references/integrations.md).

1. Define the hypothesis, eligible universe, selection/sizing rules, benchmark and sample window before results. Freeze the policy before the sample; define train, validation and test boundaries. If tuning after inspection, version the policy and obtain a fresh holdout. Record all variants tried.
2. Assemble archived source availability, signal and execution times, execution prices, settlement dates and session marks. Include failed, withdrawn, delisted and unresolved deals plus an explicit exclusion register. Avoid constructing the universe from surviving tickers or completed deals. Preserve as-known terms rather than restated final consideration.
3. Run event_backtest.py on event_backtest/v1. The bundled engine supports fully funded long-only, one-currency positions with explicit fees/slippage and idle-cash interest. It reserves entry capital, distinguishes execution prices from session marks, releases cash on the supplied settlement/exit date and rejects missing marks, excess concentration or capital reuse. It does not simulate short legs, leverage, broker margin or borrow availability.
4. A supplied trade list is a replay, not proof of unbiased selection. Audit entry allocations and eligibility against the archived rule using only information available then. Later outcome labels must not influence sizing. Marks/distributions must form a consistent economic-value series; do not double count dividends in both settlement values and marks.
5. Report the NAV curve, benchmark-relative outcome, observed drawdown, costs, outcome coverage, unresolved positions and chronological segment results. Holdings carry across segment boundaries. Segment summaries are not fitted-model validation. Document sample, liquidity, taxes, missing-market and survivorship limitations; never call synthetic fixture results a track record.
6. Stress costs, settlement delays and downside on separately labeled runs when data supports it. Do not optimize parameters on the final test interval. State what is still needed for a stock-hedged strategy backtest.

Use the `backtest` example and helper described in the toolkit. Preserve the input
and output beside the source pack. Run source-verifier and desk-editor for the
reader-facing research draft; retain `DRAFT — HUMAN APPROVAL REQUIRED`.
