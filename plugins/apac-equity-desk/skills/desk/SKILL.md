---
name: desk
description: Run APAC equity desk workflows from short requests including morning, wrap, colour, topic radar, earnings, event calendar, cross-market mapping, thesis updates, multi-agent mode, verification and editing. Use in a finance desk context or when explicitly invoked.
---

# APAC Desk

Read `../../references/desk-defaults.md`. The user should need only a task and
a market/security/event, not a detailed prompt. Apply explicit overrides first.

For every workflow that consumes market, consensus, estimate, calendar or
cross-asset data, read `../../references/integrations.md`. Prefer the user's
Bloomberg export or screenshot, use OpenBB only for missing, stale or absent
market fields, and preserve task time, provider time and field lineage. Official
filings and regulator/exchange/government releases remain authoritative for
reported facts and events.

Select the route and read its sibling skill:

- Morning -> `../morning-brief/SKILL.md`
- Country/regional close -> `../apac-market-wrap/SKILL.md`
- Stock/sector colour or why-it-moved -> `../market-color/SKILL.md`
- Deeper catalyst work -> `../catalyst-analysis/SKILL.md`
- Event research ideas -> `../event-trade-ideas/SKILL.md`
- Topic discovery / what is moving -> `../topic-radar/SKILL.md`
- Earnings/results -> `../earnings-review/SKILL.md`
- Company fundamentals, valuation or model change -> `../company-fundamentals/SKILL.md`
- Upcoming catalysts -> `../event-radar/SKILL.md`
- Cross-market transmission -> `../cross-market-map/SKILL.md`
- Thesis tracking -> `../signal-ledger/SKILL.md`
- Explicit multi-agent/parallel mode -> `../parallel-desk/SKILL.md`
- Claim/source check -> `../source-verifier/SKILL.md`
- Editing -> `../desk-editor/SKILL.md`

Execute the selected workflow. For research drafts, verification and editing are
included: read the source-verifier and desk-editor instructions and complete
their passes in this task before returning the draft. Do not ask whether to
perform those routine stages. A check-only or edit-only request stays narrow.

Resolve dates/session cutoffs from the request and current market calendar;
use task context for "this" or "update". Ask one concise question only if an
essential subject cannot be inferred. Do not invent live data, imply unavailable
connections or assume access to other tasks. Retain material gaps and the
human-approval draft banner. Do not place orders, change accounts, publish,
schedule runs or create new tasks through this shorthand.
