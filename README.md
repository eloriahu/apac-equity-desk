# APAC Equity Desk

For minipanda's happy friends.

APAC Equity Desk is a read-only research plugin for market colour, morning notes, country closes, earnings, company fundamentals, management review, merger arbitrage, special situations, idea discovery and cross-market work. Ask the question naturally: the desk selects the minimum useful workflows and only brings in an agent team when the work is genuinely broad, deep or explicitly parallel.

The plugin supports Codex and Claude Code from the same skills, references and calculation helpers. Coverage includes North Asia, Australia/New Zealand, India and Southeast Asia when the required market data and sources are supplied or connected.

## Use cases

### Start and finish the trading day

| Ask | What comes back |
| --- | --- |
| `Japan morning` | A developed researched note: local tape, overnight/domestic drivers, named exposures, counterevidence and today's catalysts |
| `HK wrap` | Index performance, breadth, sectors, movers, flows, catalysts and Corporate Headlines |
| `APAC wrap` | A regional close with country-level detail and cross-market context |
| `What matters tomorrow?` | A sourced calendar of earnings, policy, macro and company events |

Morning notes distinguish observed opening moves from pre-open expectations. Close notes will not call an open market “closed.” Missing breadth, flow or turnover data stays visible as a gap.

### Explain a stock or sector move

| Ask | What comes back |
| --- | --- |
| `Why is CATL moving?` | Tape and peer-relative move, company/news, policy, industry and sentiment triage, a fundamental hook and dated watch points |
| `CATL is up. Who benefits?` | The observed-move explanation first, followed by a separately labelled beneficiary funnel when the evidence supports it |
| `Challenge the catalyst` | A timing test, competing explanations, contradictions and falsifiers |
| `What is moving in HK?` | A ranked topic queue based on movement, breadth, relative performance and volume |
| `Optical names are rallying. Map the read-through.` | Evidence-linked paths through suppliers, peers, commodities, FX and end markets |

The desk separates confirmed disclosures, plausible factors and unconfirmed chatter. A repeated wire story still counts as one source.

### Research company fundamentals

| Ask | What comes back |
| --- | --- |
| `Fundamental review of 9988 HK` | Business quality, financial progression, cash conversion, valuation, debates and falsifiers |
| `Review these results` | Actual versus consensus, segment and margin drivers, guidance and estimate implications |
| `What changed in the model after earnings?` | A reported-to-prior bridge, changed assumptions and valuation impact |
| `Run base, upside and downside valuation scenarios` | Assumption-led scenarios with current-data and evidence limitations stated |
| `Did management deliver on its targets?` | A dated promise-versus-delivery ledger, capital-allocation record and governance flags |
| `Is the dividend durable?` | A sector-aware income review with coverage, balance-sheet and downside tests |
| `Has the thesis actually changed?` | Fact-versus-price-versus-wording drift, researchability ceiling and critical-number audit |
| `Challenge the Street's bull case on TSMC` | A house-by-house map of the shared theory, its strongest defense, source-backed weak links and tests that could falsify them |
| `What changed in TSMC's new annual report?` | Page-linked filing differences, verified in the original documents and assessed for thesis relevance |
| `How did FY27 consensus change after results?` | A like-for-like estimate bridge, with new/dropped coverage and price reaction kept separate |
| `Are foreigners buying Samsung Electronics?` | Dated investor net trading by category; disclosed ownership is a separate question |

Install `fundamental-tools` from [AI Toolbox](https://github.com/eloriahu/ai-toolbox) for shared `fundamental_pack/v1`, `filing_change/v1`, `expectations_bridge/v1` and `ownership_flow/v1` contracts, optional Docling/pykrx adapters, Taiwan FinMind flow access and transparent ratio/DCF calculations. The desk can still work from supplied filings or manually assembled packs when the toolbox or a data entitlement is absent. Flows never substitute for beneficial-ownership disclosures.

For consensus challenges, the toolbox can also provide `consensus_challenge/v1`. “Mainstream” means a documented majority of distinct major-house groups backing the same causal thesis, not simply similar ratings. If the report universe is incomplete, the desk labels the result as observed convergence. A proposed blind spot is a testable research lead, never a claim that nobody else has seen it.

When Public Equity Investing is available, the router hands it full initiations, comps/DCF workbooks, three-statement models, model updates and equivalent investment artifacts automatically based on the requested deliverable; the user does not need to name the plugin. APAC Equity Desk supplies the verified regional evidence, conventions and note-writing layer. If the specialist is unavailable, the desk states the boundary and returns only the supported research pack.

### Turn an event into research work

| Ask | What comes back |
| --- | --- |
| `Ideas from this` | Up to three event scenarios with mechanism, timing, risks and invalidation |
| `What matters next week in Korea?` | Confirmed and provisional catalysts with source dates |
| `Update this thesis` | A visible strengthened, weakened, falsified or unchanged ledger entry |
| `Check this` | An audit of citations, timestamps, units, contradictions and causal wording |
| `Tighten this to 150 words` | A senior edit that keeps the evidence and uncertainty intact |

### Research merger arbitrage and special situations

| Ask | What comes back |
| --- | --- |
| `Analyze this HK privatization's spread and break downside` | Verified consideration, costed close/delay/break scenarios, conditions and next milestones |
| `Screen announced APAC takeovers` | Sourced candidate shortlist with eligibility, downside, data gaps and exclusions |
| `Find APAC spin-offs, tenders and rights situations` | Discrete corporate events, value mechanism, timing, implementation constraints and falsifiers |
| `Update this deal watchlist` | Dated changes in terms, status, quotes, approvals, deadlines and thesis |
| `Design an event-driven strategy` | Universe, event definitions, point-in-time data requirements, costs and risk framework |
| `Run the APAC deal radar for new announcements` | Dated primary-source candidates, amendments, duplicate filtering and explicit coverage gaps |
| `Compare this scheme document with the amended offer` | Cited term changes, unknowns and implications; omissions are not assumed to repeal terms |
| `Stress close probability, break price and timing` | Costed EV grids and break-even thresholds with declared assumptions |
| `Model this collar, CVR and partial tender` | Component payoffs and discounted scenario values, including explicit FX assumptions |
| `Backtest this historical deal sample` | Portfolio NAV, locked capital, costs, benchmark/drawdown and failed/unresolved deal coverage |
| `Evaluate alerts for this deal watchlist` | Material-change and threshold events with persisted duplicate suppression |

Use `$desk` or the focused `$merger-arb`, `$special-situations` and `$deal-monitor`
skills. Claude Code has matching `/merger-arb`, `/special-situations` and
`/deal-monitor` commands. These workflows are bundled in APAC Equity Desk; a
separate Event Driven Desk installation is not needed.

The offline calculator supports cash, fixed-ratio stock and mixed consideration,
partial hedges, financing, borrow, rebates, dividends and fees. It distinguishes
gross spread from costed P&L and analyst probabilities from a break-even threshold.
See [calculation conventions](plugins/apac-equity-desk/references/event-driven/calculations.md).
The new toolkit adds `deal-radar`, `deal-documents`, `probability-sensitivity`,
`deal-models`, `historical-testing` and `deal-alerts`, with matching slash commands.
See the [toolkit guide and runnable examples](plugins/apac-equity-desk/references/event-driven/toolkit.md).
Supported complex models cover fixed-value collars, CVRs, explicit FX and tender
proration. Their output is consideration NPV; fixed-ratio trading P&L remains a
separate calculation.

Radar uses sources actually searched or supplied; no complete live APAC deal feed
is bundled. Historical testing is a fully funded long-only replay of supplied
decisions, with point-in-time checks, rather than a stock-hedged strategy simulator.
Alert rules evaluate local snapshots; ongoing monitoring requires a configured
data source, cadence and host automation. No historical performance claim or active
monitor is created by installing the plugin. Research watchlists remain local artifacts.

The [GitHub review](docs/event-driven-github-review.md) documents candidate skills
and the formula issues identified before integrating this original calculator.

### Discover ideas from themes and bottlenecks

| Ask | What comes back |
| --- | --- |
| `Find APAC beneficiaries of AI power bottlenecks` | A tested causal chain, scarce nodes, listed exposures and what could remove the bottleneck |
| `Screen this theme` | A traceable universe funnel with sector-aware rules, ranked candidates and explicit rejections |
| `Who loses from this policy change?` | Direct and second-order exposure paths, earnings sensitivity, catalysts and falsifiers |

The idea funnel can return zero names. A popular theme does not become an idea
until the economic link, listed-company exposure and expectations test survive.

These are research workflows. They do not place trades, alter accounts or publish drafts.

## How the research stack fits together

```text
Bloomberg export or screenshot / official filing / public source
                              │
                  AI Toolbox adapters and calculations
                              │
       market pack / fundamental_pack/v1 / idea_funnel/v1
       / research_review/v1 / filing_change/v1
       / expectations_bridge/v1 / ownership_flow/v1
       / consensus_challenge/v1
                              │
                        APAC Equity Desk
                evidence ranking + APAC judgment + writing
                              │
              source verification + desk-editor review
                              │
                DRAFT — HUMAN APPROVAL REQUIRED
```

Collection and judgment stay separate. A calculation library cannot silently become the source of an official reported number, and a fresh fallback quote cannot silently overwrite a fresh Bloomberg observation.

## Install

### Codex

```shell
codex plugin marketplace add https://github.com/eloriahu/apac-equity-desk
codex plugin add apac-equity-desk@apac-equity-desk
```

Start a new task and type a short request:

```text
$desk Japan morning
$desk Why is CATL moving?
$desk Fundamental review of 9988 HK
$desk Find APAC beneficiaries of AI power bottlenecks
```

Natural-language requests such as `Japan wrap`, `TSMC is up 6%, why?` or `Did management deliver?` work when the session selects the desk automatically. Slash commands are shortcuts, not a requirement.

Update an installed copy:

```shell
codex plugin marketplace upgrade apac-equity-desk
codex plugin add apac-equity-desk@apac-equity-desk
```

### Claude Code

Run these inside Claude Code:

```text
/plugin marketplace add eloriahu/apac-equity-desk
/plugin install apac-equity-desk@apac-equity-desk
```

Claude Code exposes `/desk` plus focused commands including `/morning`, `/wrap`, `/color`, `/catalyst`, `/fundamentals`, `/discover`, `/management`, `/quality`, `/research-audit`, `/company-team`, `/earnings-team`, `/check`, `/tighten` and `/parallel`.

Update an installed copy with:

```text
/plugin marketplace update apac-equity-desk
```

## Inputs and source order

The desk prefers:

1. user-supplied Bloomberg exports or screenshots for market observations;
2. company filings, investor-relations material, exchange/regulator releases and official government data for reported facts and events;
3. configured public-data fallbacks for missing or stale fields;
4. credible secondary reporting;
5. clearly labeled unconfirmed commentary.

Bloomberg task/upload time and the displayed market-data timestamp are recorded separately. Screenshots use only visible values; cropped or ambiguous cells remain missing. Bloomberg artifacts stay local and are never committed or redistributed.

For fundamentals, the preferred optional routes are J-Quants/JPX for Japan, OpenDART/FSS for Korea, TWSE/MOPS for Taiwan and SEC EDGAR for US-listed issuers or ADRs. FinanceToolkit performs calculations, FinanceDatabase helps resolve identity, and AKShare is a labeled China/HK fallback.

## What the desk checks

Every research workflow starts from a structured pack and keeps the important controls visible:

- market, session, timezone, currency and as-of time;
- stock move versus index, sector and peers;
- reported, adjusted, consensus, guidance and analyst-assumption labels;
- source IDs beside material claims;
- contradictory values or explanations;
- current-price and valuation-input status;
- what would disprove the working thesis;
- missing or stale fields that limit the conclusion.

The deterministic helpers calculate breadth, relative moves, A/H premiums, earnings surprises, evidence scores, session state, topic rankings, transmission paths and thesis-ledger updates. Narrative renderers format supplied prose but do not invent research.

## House formats

### Country close

A developed narrative covering index divergence, heavyweight concentration, policy, FX/rates, macro data, sector losers and winners, and Corporate Headlines. Typical length is 500–900 words, adjusted to the session.

### Intraday theme

A headline and ticker block followed by competing explanations, the fundamental hook, mixed evidence, implications and dated watch points. Typical length is 180–350 words.

### Morning note

Morning notes actively investigate developments since the previous local close,
follow material findings into primary sources and local company exposures, and
test the first explanation against conflicting evidence. The local tape/setup
leads, followed by the decisive overnight and domestic stories, sector/company
implications and dated tests of the view. Typical length is 500–900 words when
supported; quiet sessions need less. A requested snippet/flash uses 150–250 words
or the user's limit. Pre-open expectations are labeled as expectations.

The [morning research guide](plugins/apac-equity-desk/references/morning-research.md)
defines research completion separately from formatting and structural checks.
Available sources and explicit source/time constraints determine the supported
scope; the workflow does not add a live data feed.

House style is the default. Ask for a flash, word limit or different audience when you want to override it.

## Automatic routing and agent teams

Simple questions stay lean. `TSMC is up 6%, why?` runs one composed market-colour investigation rather than six agents. A narrow but materially conflicted conclusion may use a two- or three-agent challenge wave. Full teams are reserved for explicit parallel requests or genuinely broad/deep multi-market, multi-company, company or earnings reports.

The router selects exactly one lead workflow, caps ordinary enrichers and prevents workers from spawning more workers. With a four-slot runtime, the desk head uses at most three workers at once and batches the rest into later waves.

| Role | Job |
| --- | --- |
| `market-data-analyst` | Quotes, indices, breadth, sectors, movers, flows and data-quality checks |
| `country-researcher` | Policy, macro, FX/rates, overnight context and company headlines |
| `catalyst-investigator` | Timeline, competing explanations and falsification tests |
| `filings-accounting-analyst` | Reported facts, reconciliation, cash flow and accounting quality |
| `business-kpi-analyst` | Business mechanics, segments, KPIs, guidance and moat evidence |
| `industry-chain-analyst` | Peers, customers, suppliers, causal chains and bottlenecks |
| `expectations-valuation-analyst` | Consensus, priced-in expectations, valuation and catalysts |
| `management-governance-analyst` | Delivery record, allocation, incentives, governance and succession |
| `bear-case-analyst` | Independent contradictions, alternatives and falsifiers |
| `chief-editor` | House-style draft and one revision against the audit |
| `desk-verifier` | Independent comparison of the draft against the evidence packs |

All roles share a claim/source registry. Multiple agents repeating one syndicated source do not create independent confirmation.

## Repository layout

```text
AGENTS.md                           Desk-wide operating rules
CLAUDE.md                           Claude Code entry point
.codex/agents/                      Codex project roles
.claude-plugin/marketplace.json     Claude Code marketplace
.agents/plugins/marketplace.json    Codex marketplace
config/providers.example.toml       Optional provider settings
plugins/apac-equity-desk/
  .claude-plugin/plugin.json        Claude Code manifest
  .codex-plugin/plugin.json         Codex manifest
  skills/                           Semantic router and focused workflows
  commands/                         Claude Code slash commands
  agents/                           Packaged Claude Code roles
  references/                       Source rules, contracts and house style
  scripts/                          Deterministic calculations and renderers
tests/                              Offline synthetic fixtures and regression tests
```

## Run the checks

The test suite has no live-data requirement:

```shell
python -m unittest discover -s tests -v
```

Try the synthetic fixtures locally:

```shell
python plugins/apac-equity-desk/scripts/market_snapshot.py tests/fixtures/quotes.json
python plugins/apac-equity-desk/scripts/render_market_color.py tests/fixtures/market_color_pack.json
python plugins/apac-equity-desk/scripts/render_market_wrap.py tests/fixtures/market_wrap_pack.json
python plugins/apac-equity-desk/scripts/session_clock.py --markets JP,HK,AU
python plugins/apac-equity-desk/scripts/merger_arb.py plugins/apac-equity-desk/examples/event-driven/cash-deal.json
python plugins/apac-equity-desk/scripts/event_tools.py sensitivity plugins/apac-equity-desk/examples/event-driven/sensitivity.json
python plugins/apac-equity-desk/scripts/event_backtest.py backtest plugins/apac-equity-desk/examples/event-driven/backtest.json
python plugins/apac-equity-desk/scripts/event_tools.py alerts plugins/apac-equity-desk/examples/event-driven/alerts.json
```

All fixture names, numbers, events, URLs and dates are synthetic. They test formatting and controls, not market facts.

## Safety boundary

This repository does not package a brokerage connector. It must not submit, replace, cancel or stage orders; alter brokerage positions, alerts or watchlists; or publish/send a research draft without explicit human approval at that moment. Local research watchlist snapshots are supported.

The output is research, not personalized financial advice. Provider access, exchange coverage, rate limits and redistribution rights remain subject to each provider's terms.

## Release 1.6.0

- Integrated merger arbitrage, special situations and deal monitoring into the existing desk router.
- Added costed cash/fixed-ratio deal scenarios, synthetic examples and 15 offline calculator tests.
- Preserved APAC scope, Bloomberg/OpenBB source policy, verification/editing and research draft controls.
- Added six focused workflows: deal radar, deal documents, probability sensitivity,
  complex consideration models, historical portfolio replay and local alerts.
- Added seven synthetic toolkit examples and offline checks for source timing,
  contract math, capital constraints, failed/unresolved deals and alert state.
- Aligned Codex, Claude Code and Python package release metadata.

See [release notes](docs/releases/1.6.0.md) for capabilities and current boundaries.

## Release 1.5.0

- Added automatic mainstream sell-side thesis challenge with source-linked premise, counterevidence, price-expectations and falsifier review.
- Consumes AI Toolbox `consensus_challenge/v1` by schema, without assuming broker-report entitlements or claiming novelty from incomplete coverage.

## Release 1.4.0

- Added automatic filing-change, expectations-change and ownership-flow routes.
- Consumes three new AI Toolbox evidence bridges by schema, without importing its code.
- Preserves the difference between changed filing text, consensus revisions, investor trading flows and disclosed beneficial ownership.

## Release 1.3.0

- Added automatic semantic routing across question type, horizon, deliverable, evidence availability and complexity.
- Added idea-funnel and bottleneck discovery, management review, thesis/research audit, sector-aware quality and income review.
- Added specialized company and earnings agent teams with capacity-aware waves, shared source independence and no nested fan-out.
- Added schema-only consumption of AI Toolbox `idea_funnel/v1` and `research_review/v1` packs.
- Routes requested full initiations and financial models to Public Equity Investing automatically when available; portfolio work still requires an explicit portfolio request.

## Release 1.2.0

Reader-facing notes now enforce causal completeness: every material move needs a fresh trigger, transmission mechanism, relative-stock fit and counterevidence, or an explicit unresolved assessment with ranked alternatives. The final editorial pass also removes canned framing, decorative formatting and repetitive AI-style prose without deleting evidence or uncertainty.

- Added `company-fundamentals` and `/fundamentals`.
- Added the shared `fundamental_pack/v1` contract and loose coupling to AI Toolbox.
- Added a documented handoff to Public Equity Investing for initiations, models, comps, DCFs and thesis tracking.
- Retained Bloomberg-first market inputs, field-level OpenBB fallback, source verification, human publication approval and the no-brokerage boundary.
