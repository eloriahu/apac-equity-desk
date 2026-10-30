# Specialist research modules

This is the analysis layer between a desk workflow and its retrieval/calculation
tools. The lead chooses modules by the question they answer, then reads the actual
installed skill and executes its scoped assignment. These skills are optional
external integrations, not code vendored into APAC Equity Desk. Installed skills
and their underlying data/runtime availability are separate checks.

The capability IDs below connect to `tool-capabilities.json`. Skill locations
come from the current host catalog, never a hard-coded machine path. Resolve an
external script relative to that installed plugin, not this desk's scripts.

| Capability / question | Preferred installed specialist | Required inputs and bounded output |
| --- | --- | --- |
| `fundamental-analysis`: what drives earnings, operating economics, cash conversion or valuation? | `fundamental-tools:fundamental-research` | Dated issuer sources and usable financial periods -> scoped `fundamental_pack/v1`. Default support for ordinary earnings reviews and company fundamentals; include valuation only when requested or necessary and supported. |
| `expectations-analysis`: what changed in estimates or the analyst model? | `fundamental-tools:expectations-bridge` | Two dated comparable snapshots -> `expectations_bridge/v1`. One actual/consensus pair is an earnings surprise, not an estimate revision. |
| `filing-analysis`: what was newly disclosed or changed? | `fundamental-tools:filing-change-radar` | Two comparable dated filings with original locators -> `filing_change/v1`. Review flagged changes for economic meaning; extraction similarity does not establish materiality. |
| `ownership-analysis`: who holds it, or which investor categories traded? | `fundamental-tools:ownership-flow-review` | Dated disclosed holdings or jurisdiction-specific trading data -> `ownership_flow/v1`. Keep beneficial ownership, nominees and net trading separate. |
| `candidate-analysis`: which listed names benefit, lose or control the bottleneck? | `fundamental-tools:equity-idea-generation` | Verified event/theme and traceable universe/exposure links -> `idea_funnel/v1`. Establish the observation first and retain unrankable names; ordinary price colour does not trigger a funnel. |
| `research-audit`: did management deliver, did the thesis change, or are key numbers reliable? | `fundamental-tools:research-quality-review` | Select only the needed ledger, baseline comparison or number audit -> `research_review/v1`. No thesis-drift verdict without a prior thesis. Routine source verification remains included in every research draft. |
| `consensus-analysis`: is there a shared Street thesis, and where could it fail? | `fundamental-tools:consensus-challenge` | Dated accessible house views, coverage universe and primary tests -> `consensus_challenge/v1`. A ratings majority is not a shared causal thesis. |
| `market-normalization`: are the supplied observations comparable and current? | `finance-tools:market-data` | Bloomberg exports/screens or eligible fallback observations -> normalized market rows, capture times, adjustments and field lineage under `data-contract.md`. Current facts still require source timestamps. |
| `quantitative-design`: does a historical claim survive an empirical test? | `quant-tools:quant-research` | Hypothesis, point-in-time universe/series, horizon and benchmark -> scoped reproducible design/calculations. Use `statistical-research` for suitable statistical-analysis, statsmodels or PyMC work, with dependencies checked. |
| `source-investigation`: which primary evidence resolves a research question? | `research-tools:browser-research` | Specific evidence question and permitted source scope -> claim-linked original sources with timestamps/locators. Select ordinary retrieval or dynamic browsing according to the actual page. |
| `investment-artifact`: build a full initiation, model, comps or DCF workbook | `public-equity-investing:public-equity-investing` | Verified APAC evidence and requested deliverable -> that plugin owns one final artifact; the desk supplies evidence and interpretation. Preserve its own input contract. |

For fundamental packs read `data-contract.md`; for the bridge/audit/funnel packs
read `research-contracts.md` and the selected specialist's own contract. Map
fields explicitly; do not assume every plugin accepts the same JSON schema.

If a preferred specialist is absent or cannot perform the assignment, use the
corresponding desk analysis with traceable original inputs and working local
calculations. Preserve the required comparison and source standards. A fallback
cannot manufacture a missing baseline, consensus entitlement or statistical fit.
A missing investment-artifact owner retains the boundary in `integrations.md`.

These are supported mappings, not a claim that every installed plugin is wired
into every question. A newly discovered specialist can support a scoped need
after reading its instructions and checking fit, access, inputs and output. Note
that choice in the plan. Explicit-invocation-only skills remain user shortcuts.

## Worked compositions

- **“Review these results.”** Earnings-review leads; fundamental-analysis
  normalizes and explains the result; the desk calculates comparable surprises.
  Add another module only for a material subquestion, then verify/edit once.
- **“Earnings beat, why is the stock down?”** Market-color leads; establish the
  actual reaction and timing, then use scoped fundamental analysis and guidance
  checks to test explanations. An expectations bridge requires two snapshots.
- **“What changed in the annual report and estimates?”** Filing-change leads
  with filing-analysis and expectations-analysis. Run the independent comparisons
  on their own dated baselines before reconciling whether they support one story.
- **“Who benefits from these results?”** Explain the result, then use
  candidate-analysis for evidence-linked exposures. Do not assume every supplier
  benefits from the same headline.
- **“Tighten this earnings note only.”** Desk-editor leads; preserve supplied
  facts and scope. The word earnings does not start a fundamental research run.
