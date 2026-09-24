---
name: desk
description: Automatically route short or composite APAC equity questions to the minimum useful research workflows and, only when warranted, a functional multi-agent team. Use for market moves, company research, earnings, idea discovery, merger arbitrage, special situations, deal updates, morning notes, wraps, catalysts, verification and editing.
---

# APAC Desk

Read `../../references/desk-defaults.md` and `../../references/intent-routing.md`.
The user should need only a natural-language question and a market, security,
company, event or theme. Do not make the user choose skills, slash commands or
agents. Apply explicit overrides first.

For every workflow that consumes market, consensus, estimate, calendar or
cross-asset data, read `../../references/integrations.md`. Prefer the user's
Bloomberg export or screenshot, use OpenBB only for missing, stale or absent
market fields, and preserve task time, provider time and field lineage. Official
filings and regulator/exchange/government releases remain authoritative for
reported facts and events.

Classify the request before selecting a route. Record internally:
`primary_workflow`, `required_enrichers`, `optional_followups`,
`execution_mode`, `reason` and `stop_conditions`. Answer the stated question
first. Add an enricher only when its result could change the conclusion.

Select exactly one primary route and any justified sibling enrichers:

- Morning -> `../morning-brief/SKILL.md`
- Country/regional close -> `../apac-market-wrap/SKILL.md`
- Stock/sector colour or why-it-moved -> `../market-color/SKILL.md`
- Deeper catalyst work -> `../catalyst-analysis/SKILL.md`
- Event research ideas -> `../event-trade-ideas/SKILL.md`
- Announced takeover, privatization, tender terms or merger-arbitrage spread -> `../merger-arb/SKILL.md`
- Event-driven strategy, announced-deal screen or special-situation candidates -> `../special-situations/SKILL.md`
- Deal watchlist update, merger status or dated transaction comparison -> `../deal-monitor/SKILL.md`
- Topic discovery / what is moving -> `../topic-radar/SKILL.md`
- Earnings/results -> `../earnings-review/SKILL.md`
- Compare two company filings or ask what is newly disclosed -> `../filing-change/SKILL.md`
- Dated consensus/model revision or expectations drift -> `../expectations-change/SKILL.md`
- Disclosed holders, foreign/institutional flow or positioning -> `../ownership-flow/SKILL.md`
- Company fundamentals, valuation or model change -> `../company-fundamentals/SKILL.md`
- Sector-aware company quality or dividend/income durability -> `../company-quality/SKILL.md`
- Management quality, capital allocation or promise-versus-delivery -> `../management-review/SKILL.md`
- Thesis drift, researchability or numerical research audit -> `../research-review/SKILL.md`
- Critique a mainstream sell-side thesis or find consensus blind spots -> `../consensus-challenge/SKILL.md`
- Theme-to-names, bottleneck discovery or candidate funnel -> `../idea-funnel/SKILL.md`
- Upcoming catalysts -> `../event-radar/SKILL.md`
- Cross-market transmission -> `../cross-market-map/SKILL.md`
- Thesis tracking -> `../signal-ledger/SKILL.md`
- Broad/deep/high-risk or explicitly parallel market work -> `../parallel-desk/SKILL.md`
- Broad/deep company research -> `../parallel-company-research/SKILL.md`
- Broad/deep earnings analysis -> `../parallel-earnings/SKILL.md`
- Claim/source check -> `../source-verifier/SKILL.md`
- Editing -> `../desk-editor/SKILL.md`

Execute the selected workflow or lean composition. For research drafts, verification and editing are
included: read the source-verifier and desk-editor instructions and complete
their passes in this task before returning the draft. Do not ask whether to
perform those routine stages. A check-only or edit-only request stays narrow.

For takeover news, route by the requested answer: why the stock moved remains
market-color; deal economics and conditions use merger-arb; finding discrete
corporate-event opportunities uses special-situations. Generic ideas from a
policy or industry event remain event-trade-ideas, and a general catalyst calendar
remains event-radar. These specialist routes are bundled here and do not require
the separate Event Driven Desk plugin. Apply this desk's APAC scope and draft controls.

For `XXX stock is up, why?`, use market-color as the lead. Its normal workflow
already includes tape/relative move, company/news, regulation/policy,
peer/industry and sentiment/chatter triage, a concise fundamental hook and
useful implications. Do not launch full fundamentals, idea generation or a
team merely because those subjects are adjacent.

Resolve dates/session cutoffs from the request and current market calendar;
use task context for "this" or "update". Ask one concise question only if an
essential subject cannot be inferred. Do not invent live data, imply unavailable
connections or assume access to other tasks. Retain material gaps and the
human-approval draft banner. Do not place orders, change accounts, publish,
schedule runs or create new tasks through this shorthand.
