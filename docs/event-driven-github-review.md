# GitHub review for APAC event-driven research

Reviewed 2026-09-24 using repository metadata and actual skill/calculator files.
This is a targeted shortlist, not an exhaustive audit. No third-party installers
or broker integrations were run. Code and instructions in this plugin are original;
the repositories below informed the evaluation and feature choices.

| Repository | Fit and reviewed material | Decision |
| --- | --- | --- |
| [tmcga/alpha-stack](https://github.com/tmcga/alpha-stack) | Dedicated [merger-arb skill](https://github.com/tmcga/alpha-stack/blob/eefe76525242e7484f966afe6147ddfeba9e4ffb/skills/merger-arb/SKILL.md), [calculator](https://github.com/tmcga/alpha-stack/blob/eefe76525242e7484f966afe6147ddfeba9e4ffb/tools/merger_arb.py), Kelly helper. MIT; last push returned by GitHub: 2026-05-13. | Closest topical match. Use as a checklist reference; do not install unchanged as the numerical foundation. |
| [Geeksfino/finskills](https://github.com/Geeksfino/finskills) | [Event detector](https://github.com/Geeksfino/finskills/blob/main/US-market/event-driven-detector/SKILL.md) and [framework](https://github.com/Geeksfino/finskills/blob/main/US-market/event-driven-detector/references/event-framework.md). Apache-2.0; last push 2026-03-05. | Useful event taxonomy and screen structure. Correct sign convention, generic sizing and unsupported empirical claims before reuse. |
| [yennanliu/InvestSkill](https://github.com/yennanliu/InvestSkill) | [Catalyst calendar](https://github.com/yennanliu/InvestSkill/blob/main/plugins/us-stock-analysis/skills/catalyst-calendar/SKILL.md). MIT; last push 2026-09-24. | Optional calendar reference. Considerable overlap with existing APAC event-radar. Not a merger-arb engine. |
| [Keon6/Merger-Arbitrage](https://github.com/Keon6/Merger-Arbitrage) | Repository/README and metadata; prediction-model project, last push 2019-04-24. GitHub metadata returned no license. | Research lead only. No ready agent/plugin verified, and reuse rights were not established. |
| Existing local anthropics-financial-services | Read investment-banking merger-model and deal-tracker skills. | Acquisition accretion/dilution and advisory pipeline tracking differ from trade-level merger arbitrage. Optional acquirer/diligence support. |
| Existing local EdgarTools | Read README, package metadata and MIT license; supports SEC filings, proxy and ownership data. | Useful US source-access building block already present in upstreams; no need to duplicate it. No live adapter was wired in this version. |

## Material review findings

**Alpha Stack mixed hedge.** Its skill weights the exchange ratio again by the
stock share of total consideration. When the contractual ratio already specifies
acquirer shares per target share, this under-hedges. Example: 20 cash + 0.5 acquirer
shares at 100 is worth 70; a full fixed-ratio hedge is 0.5 shares, not 0.3571.
The new calculator tests hedge cancellation across terminal acquirer prices.

**Alpha Stack model scope.** Its CLI supports cash or stock, not a combined cash
plus stock input. CVR expected value is added without a separate payment-time
discount in that helper. Downside defaults to 80% of current and probabilities are
clipped to [0,1], obscuring inconsistent scenarios. Its collar CLI clamps deal
value while its prose describes a different fixed-value-inside/ratio-outside
payoff. Neither convention is safe to apply to an arbitrary contract without terms.

**Alpha Stack sizing.** Binary Kelly `p - q/b` is expressed as the fraction at risk
when the loss unit is one. Presenting that directly as allocated NAV for a deal
with a fractional downside requires a separate return-scale conversion and limits.
The skill also imposes universal portfolio gates and regulatory probability
adjustments without deal-specific calibration. These defaults were not adopted.

**Finskills sign convention.** Its framework defines downside as current minus
unaffected price (a positive loss magnitude) but then adds the probability-weighted
downside in EV. With current 98, offer 100, break 80 and completion probability
90%, the signed gross EV is 0, not +3.6. This becomes a regression test locally.

**Evidence and portability.** Generic return/impact ranges and automatic allocation
bands in these skills are not empirical evidence. InvestSkill's sampled calendar
frontmatter omits a `name`, and its unavailable-data fallback permits labeled
training-data estimates; our skill instead leaves live quotes unavailable.
Claude-oriented commands, relative tool paths and related-skill dependencies need
adaptation for a standalone Codex package. Repository activity/stars do not validate
strategy performance. This review did not establish profitable live performance.

## Integration decision

Bundle merger-arb, special-situations and deal-monitor inside APAC Equity Desk,
with the existing desk router owning entry and source-verifier/desk-editor owning
review. Preserve the Bloomberg/OpenBB field policy, APAC scope and draft controls.
Use the original offline calculator and existing filing/data tools when available.
A separate Event Driven Desk installation is not needed. Complex structures
remain explicit custom-model work; monitoring needs an explicitly requested scheduler.
