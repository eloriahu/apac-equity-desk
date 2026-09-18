# Short requests and desk defaults

A short request supplies the task and subject. These defaults supply the workflow.
Do not ask the user to repeat the house style, source hierarchy, peer comparison,
fact checking or editing instructions.

## Request routes

| User says | Workflow | Default result |
| --- | --- | --- |
| Japan morning; HK morning; morning snippet | morning-brief | Three short paragraphs: opening tape, overnight context, sectors |
| Japan wrap; HK close; China EOD | apac-market-wrap | Developed country close ending with Corporate Headlines |
| APAC wrap | apac-market-wrap | Regional digest for completed sessions, with coverage gaps |
| CATL colour; why is CATL moving?; Taiwan lenses | market-color | Move versus peers, competing explanations, fundamental hook, mixed evidence, implications, watch |
| Dig deeper; challenge the catalyst | catalyst-analysis | Evidence-ranked explanations, contradictions and invalidation |
| Ideas from this; trade ideas on this event | event-trade-ideas | Up to three research scenarios with mechanism, horizon, confirmation and invalidation |
| Check this | source-verifier | Audit the supplied note and evidence |
| Tighten this | desk-editor | Edit the supplied draft, preserving the selected house format and evidence |

"Taiwan lenses" is a colour request only in an established desk-research context
or with an explicit desk invocation. Do not intercept unrelated uses of "wrap",
"morning", "check" or "ideas". The user can invoke `$desk Japan wrap` to make
the intended route explicit. These are natural-language instructions, not a
shell command, keyword-parser API or background subscription.

## Resolve context without a questionnaire

- Read the user's explicit subject, date, format, length and data-source constraints first; these override defaults.
- Reuse the market, named event or draft from the current task when "this", "update" or "wrap" has an unambiguous referent. Do not assume access to other tasks, yesterday's private notes or a cross-task memory store.
- If the essential market/security/event is missing and cannot be resolved from context, ask one short question. Do not ask optional style or checklist questions.
- A morning request defaults to the requested market's current local trading day. Check the market clock/calendar. If pre-open, label PRE-OPEN and use expectations; if already closed, label it a retrospective morning recap rather than a live opening note. On a holiday, identify the closure instead of inventing a session.
- A wrap with no date defaults to the latest completed session for that market; display the date, especially on holidays or before today's close. If the user explicitly requests today's wrap while trading continues, return a clearly labelled interim note and do not use the closed-session renderer. Do not create a later run unless separately requested.
- Colour defaults to the latest available market observation, with its actual timestamp and delayed/live status. Resolve security identity and listing; use prior context for an already-established A/H focus. Do not guess ambiguous numeric tickers.
- "Ideas from this" needs an identifiable event and evidence. Use the current task's material and verify the event before developing scenarios. Do not choose an unrelated macro story just to fill three ideas.
- Refresh time-sensitive prices and event status before an update or close wrap. Earlier task notes are leads, not fresh evidence. Respect an explicit "use only this pack" constraint and label the supplied cutoff.

## Run the whole routine

For morning, wrap, colour and catalyst analysis:

1. Resolve market/session/subject and get the material data from available approved read-only sources. Longbridge is preferred where supported; optional integrations must actually be configured. Public primary-source research may supplement news when available, not masquerade as an entitled quote feed.
2. Build or refresh the evidence pack before drafting. Compare peers, benchmarks, related listings and cross-assets where relevant; investigate rather than assume causation.
3. Use the appropriate format and voice from `house-style.md`.
4. Apply the sibling source-verifier instructions to the claims and citations. Use the fact-check helper on structured claims where appropriate; it does not prove semantic support.
5. Apply the sibling desk-editor instructions. Remove or qualify unsupported claims; if the conclusion cannot be supported, return a limited draft or concise evidence-gap request.
6. Return the finished draft and only material unresolved gaps. The user does not need to request each review pass or receive a narration of every checklist item.

For event-trade-ideas, verify the event and assess catalysts first, then create
at most three researched scenarios and perform the same verification/editing
passes. Zero supported ideas is an acceptable result.

For an explicit source audit or edit-only request, respect that narrow scope.
The editor does not collect new data or append a trade-idea section.

Read the relevant sibling SKILL.md files and perform these stages in the same
task. This sequence does not require delegation or another task. Keep the
draft banner and human publication approval. Never mutate brokerage accounts
or execute trades.

## Default output sizes and scope

- Morning: 150–250 words, three short paragraphs.
- Country wrap: roughly 500–900 words with useful sector/name detail.
- Regional wrap: a compact country-by-country digest; expand only when requested.
- Developed colour: 180–350 words; an explicitly requested flash is 90–180 words.
- Ideas: up to three, each with an explicit invalidation.
- Editor: retain the existing format and length unless the user asks to shorten.

These are guides, not padding targets. Data gaps do not justify made-up content.
A short prompt does not activate scheduling, continuous monitoring, new provider
connections, or publication.
