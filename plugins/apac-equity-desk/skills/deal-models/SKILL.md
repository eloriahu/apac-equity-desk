---
name: deal-models
description: Model contractual merger consideration with fixed-value collars, stock, cash, CVRs, partial-tender proration and explicit FX scenarios. Use for complex deal payoffs; acquisition accretion/dilution and full company models use the existing investing handoff.
---

# Deal Models

Read [research standards](../../references/event-driven/research-standards.md),
[toolkit contracts and examples](../../references/event-driven/toolkit.md), and
[market data integrations](../../references/integrations.md).

1. Read definitive terms and amendments with page/section evidence. Classify fixed ratio versus fixed value; establish ratio measurement window, floor/ceiling, inclusive boundaries, contractual ratio rounding, settlement dates and currencies. Do not generalize one collar convention to every transaction.
2. Use merger_arb.py for costed fixed-ratio trading P&L. Use the models helper for supported consideration components and present values. These are separate economic outputs: NPV is not hedged P&L or annualized strategy return.
3. Build mutually exclusive parent scenarios with probabilities totaling one. Components may include cash, stock, a fixed-value collar, a CVR or proration. Every component needs days from valuation, base-currency-per-component-currency FX and source locator. Provide dated as_of, target entry price, discount rate and present-value costs explicitly.
4. Keep collar reference VWAP distinct from settlement stock price. Supply below-floor and above-ceiling ratios from the contract, including rounding. CVR probabilities are conditional on their parent scenario and payments are discounted to their own dates. Use joint scenarios for mutually exclusive or dependent milestones; no automatic independence assumption.
5. Proration values the accepted fraction and residual position separately. If acceptance and residual realization occur on different dates, use separate cash/stock components. FX is scenario-based; no hedge is inferred.
6. Report component values, scenario NPV, expected NPV, contract gaps and sensitivity. Fractional-share rounding, special election waterfalls, taxes, dynamic hedging and contract-specific caps beyond this schema require a separately reviewed extension.

Use the `models` example and helper described in the toolkit. Preserve the input
and output beside the source pack. Run source-verifier and desk-editor for the
reader-facing research draft; retain `DRAFT — HUMAN APPROVAL REQUIRED`.
