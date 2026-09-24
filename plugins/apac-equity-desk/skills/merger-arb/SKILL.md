---
name: merger-arb
description: Analyze announced APAC takeovers, mergers, privatizations and tender offers for arbitrage research, covering consideration, hedges, net spread, break downside, closing conditions and scenario probabilities. Not acquisition accretion/dilution modeling.
---

# Merger Arbitrage

Read [research standards](../../references/event-driven/research-standards.md) and the relevant
[jurisdiction sources](../../references/event-driven/jurisdictions.md).

1. Verify status: rumor, preliminary proposal, signed agreement/firm offer,
   conditional, unconditional, effective/settled, lapsed, withdrawn or terminated.
   Confirm security, share class and ADR/foreign-holder eligibility.
2. Extract definitive terms and amendments: cash, exchange ratio, fixed/floating
   structure, collars, election/proration, dividends/adjustments, CVRs, competing
   bids, acceptance/voting conditions, financing, regulatory/court steps, long-stop
   date, extension and termination rights, fee triggers and recipients. Cite
   pages/sections; omission from a press release means unknown. A break fee paid
   to a company is not automatically a cash payment to its shareholders.
3. Align target/acquirer/FX observations by timestamp, session, currency, unit and
   corporate actions. Check borrow availability, dividends and funding assumptions.
4. Read [calculation conventions](../../references/event-driven/calculations.md). Use the bundled
   calculator for supported cash/fixed-ratio deals, saving input/output in the
   research workspace. Show gross spread, costed P&L, capital denominator and day
   count separately. Never disguise a missing cost as a known zero. Model collars,
   floating ratios, CVRs, proration and cross-currency structures separately.
5. Model close, delayed close and break; add recut or rival bid where material.
   Estimate break value independently using unaffected price/date, market/sector
   changes, fundamentals and lost optionality. Stress both legs in stock-deal breaks.
6. For each remaining condition identify evidence, decision-maker, next milestone
   and timing. Financing commitment is not cash received; one clearance is not all
   approvals. Do not multiply correlated marginal probabilities as if independent.
7. Label analyst probabilities and their rationale/ranges. Distinguish them from
   two-state break-even thresholds and price-implied proxies. Spreads alone do not
   identify true completion probabilities. Avoid fixed universal probability gates.

Explain what must happen to earn the spread, the strongest contrary view, dominant
risk, falsifier and next dated test. Lead with net economics and break loss, not
the largest annualized percentage. Expected close, contractual deadline and cash
settlement are different dates. No precise expected return without probability inputs.

If terms/prices are unavailable, finish the supported terms/risk analysis and mark
calculations unavailable. A quote does not establish an executable short. For
explicit portfolio sizing or hedge-design requests, follow the desk handoff
in `../../references/integrations.md`; provide the verified scenario evidence.
Contractual exchange-ratio arithmetic is deal research, not personalized hedge
advice. Do not use generic Kelly outputs as NAV allocations.
