---
name: news-snippets
description: Research and write an APAC pre-open news digest from requests such as China news snippets, HK pre-open snippets or a before-market news roundup. Use short headline-and-paragraph items covering policy, global developments, sectors and companies. A generic morning note or morning flash stays with morning-brief.
---

# News Snippets

Before choosing tools, apply `../../references/tool-selection.md`, including
when this skill is invoked directly. Reuse the lead’s plan in supporting work.

For public-source search and extraction, read
`../../references/research-addons.md`; Firecrawl can support collection when
available while the original publisher remains the evidence source.

Read `../../references/news-snippets.md` for the writing format and selection
rules, `../../references/source-priority.md` for evidence, and the
`desk-news-snippets` section in `../../references/data-contract.md` if rendering
a structured pack. Follow the shared voice in `../../references/house-style.md`.

Resolve the market and requested date/cutoff from the task. Use
`../../scripts/session_clock.py` and an official exchange calendar when needed
to establish the previous local close and upcoming opening. Include intervening
weekend/holiday news. For a request made after opening, use a clearly labelled
retrospective pre-open cutoff and exclude later developments; do not present
the current time as pre-open. If the user requests a particular cutoff, use it.

Research material developments since the previous local close using available
read-only sources: company/exchange announcements, government and regulator
releases, established reporting, relevant global news and today's event calendar.
Use native-language primary sources where helpful. Supplied headlines are leads;
open the supporting material unless the request explicitly limits sources.
For an edit-only request, use desk-editor instead and do not add new research.

Keep an internal item/source record with event and publication times, quote time
where applicable, verification status, important figures and local relevance.
Separate fresh announcements from new reporting about old events. Follow up
material discrepancies; merge duplicated coverage. A news digest does not require
a live quote feed, an index lead, relative-performance calculations or an opening
forecast. Do not invent those to fill a morning-note template.

Write `{Market} News Snippets:` followed by standalone headline-and-paragraph
items, with brief company updates near the end. A short company-led sentence may
stand on its own. Keep item length proportional to the story; the full digest
has no inherited morning-flash word limit or fixed item quota. Cite each item
beside its claims. Preserve reported/proposed/expected distinctions in the
headline as well as the body.

Run source-verifier and desk-editor in this task with the news-snippets format
selected. Verify each material fact and any stated or implied causality; do not
turn every factual announcement into a market-move explanation. Resolve feasible
source gaps before delivery. Keep unresolved material items out of the factual
digest or accurately qualified, and describe consequential omissions in review
notes. Neither a short item nor a source link alone establishes verification.

The optional `../../scripts/render_news_snippets.py` helper preserves reviewed
item text, ordering and inline sources. It checks structure, not truth, relevance
or whether the cutoff precedes the exchange opening.

Return the draft with its market date, cutoff/timezone and pre-open status.
Retain `DRAFT — HUMAN APPROVAL REQUIRED`. Do not schedule, send, publish, or
mutate a brokerage account.
