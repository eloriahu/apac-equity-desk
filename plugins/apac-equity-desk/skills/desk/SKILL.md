---
name: desk
description: Run predefined APAC equity desk workflows from short requests such as Japan morning, Japan wrap, CATL colour, why is it moving, Taiwan lenses, ideas from this, check this or tighten this. Use in a finance desk context or when explicitly invoked.
---

# APAC Desk

Read `../../references/desk-defaults.md`. The user should need only a task and
a market/security/event, not a detailed prompt. Apply explicit overrides first.

Select the route and read its sibling skill:

- Morning -> `../morning-brief/SKILL.md`
- Country/regional close -> `../apac-market-wrap/SKILL.md`
- Stock/sector colour or why-it-moved -> `../market-color/SKILL.md`
- Deeper catalyst work -> `../catalyst-analysis/SKILL.md`
- Event research ideas -> `../event-trade-ideas/SKILL.md`
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
