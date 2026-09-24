# Short requests and desk defaults

A short request supplies the task and subject. These defaults supply the workflow.
Do not ask the user to repeat the house style, source hierarchy, peer comparison,
fact checking or editing instructions. Read `intent-routing.md` and choose the
minimum sufficient workflow automatically; slash commands are optional.

## Request routes

| User says | Workflow | Default result |
| --- | --- | --- |
| Japan morning; HK morning; morning snippet | morning-brief | Three short paragraphs: opening tape, overnight context, sectors |
| Japan wrap; HK close; China EOD | apac-market-wrap | Developed country close ending with Corporate Headlines |
| APAC wrap | apac-market-wrap | Regional digest for completed sessions, with coverage gaps |
| CATL colour; why is CATL moving?; Taiwan lenses | market-color | Move versus peers, competing explanations, fundamental hook, mixed evidence, implications, watch |
| Dig deeper; challenge the catalyst | catalyst-analysis | Evidence-ranked explanations, contradictions and invalidation |
| Ideas from this; trade ideas on this event | event-trade-ideas | Up to three research scenarios with mechanism, horizon, confirmation and invalidation |
| Analyze this takeover; merger spread; privatization terms; tender downside | merger-arb | Verified terms, costed close/delay/break scenarios, conditions and milestones |
| Screen announced deals; find special situations; event-driven strategy | special-situations | Sourced APAC corporate-event candidates, eligibility, economics and falsifiers |
| Update this deal watchlist; what changed in the merger? | deal-monitor | Dated terms/status/quote comparison and research-thesis changes |
| What is moving?; sector radar; find me a topic; what should I write about? | topic-radar | Ranked observed sectors/themes, leaders, breadth, volume, gaps and research questions |
| Earnings review; results colour; actual versus consensus | earnings-review | Verified result versus consensus, drivers, guidance and read-through |
| Is this a quality company?; dividend durability; income screen | company-quality | Sector-aware quality or distribution durability with insufficient/not-applicable outcomes |
| Assess management; did management deliver?; capital allocation review | management-review | Promise-versus-delivery ledger, capital allocation, incentives and governance |
| Has the thesis changed?; audit this research; is this name researchable? | research-review | Researchability grade, fact/price/wording drift, number audit and publication gate |
| Challenge the Street's view; what is the consensus missing? | consensus-challenge | House-by-house thesis map, strongest consensus defense, source-backed weak links and falsifiers |
| Who benefits/loses?; find candidates; bottleneck scan; screen this theme; idea funnel | idea-funnel | Causal chain, bottlenecks, traceable universe screen, ranked candidates and exclusions |
| Catalysts this week; event calendar; what matters next? | event-radar | Sourced chronological event watchlist with confirmed/provisional timing |
| Cross-market read-through; trace the exposure; transmission map | cross-market-map | Evidence-linked paths across sectors, securities, commodities and FX |
| Track this thesis; update the signal; what changed? | signal-ledger | Explicit strengthened/weakened/falsified/unchanged ledger update |
| Update this; what changed since the last pack? | current workflow + pack-delta | Refreshed facts and a material delta from the supplied/current-task prior pack |
| Multi-agent; parallel; use the agent team; /parallel | specialized parallel workflow | Functional research waves with independent verification |
| Check this | source-verifier | Audit the supplied note and evidence |
| Tighten this | desk-editor | Edit the supplied draft, preserving the selected house format and evidence |

"Taiwan lenses" is a colour request only in an established desk-research context
or with an explicit desk invocation. Do not intercept unrelated uses of "wrap",
"morning", "check" or "ideas". The user can invoke `$desk Japan wrap` to make
the intended route explicit. These are natural-language instructions, not a
shell command, keyword-parser API or background subscription.

Routes may compose. Use one primary workflow, add only enrichers that could
change its answer, and keep optional follow-ups unexecuted. A one-stock
why-it-moved question remains market-color; do not run full fundamentals, an
idea funnel or a team merely because those capabilities are related.

## Resolve context without a questionnaire

- Read the user's explicit subject, date, format, length and data-source constraints first; these override defaults.
- Reuse the market, named event or draft from the current task when "this", "update" or "wrap" has an unambiguous referent. Do not assume access to other tasks, yesterday's private notes or a cross-task memory store.
- If the essential market/security/event is missing and cannot be resolved from context, ask one short question. Do not ask optional style or checklist questions.
- A morning request defaults to the requested market's current local trading day. Run `scripts/session_clock.py` and verify holidays against an exchange calendar when material. If pre-open, label PRE-OPEN and use expectations; if already closed, label it a retrospective morning recap rather than a live opening note. On a holiday, identify the closure instead of inventing a session.
- A wrap with no date defaults to the latest completed session for that market; display the date, especially on holidays or before today's close. If the user explicitly requests today's wrap while trading continues, return a clearly labelled interim note and do not use the closed-session renderer. Do not create a later run unless separately requested.
- Colour defaults to the latest available market observation, with its actual timestamp and delayed/live status. Resolve security identity and listing; use prior context for an already-established A/H focus. Do not guess ambiguous numeric tickers.
- "Ideas from this" needs an identifiable event and evidence. Use the current task's material and verify the event before developing scenarios. Do not choose an unrelated macro story just to fill three ideas.
- "Who benefits?", "find ideas" or a theme/bottleneck screen routes to idea-funnel. Plain implications stay within the lead workflow unless candidate discovery is central.
- Management, quality and research-review requests default to the named company and current evidence. Thesis drift needs a supplied/current-task baseline.
- A full company or earnings team is automatic only under `intent-routing.md`; broad/deep/high-consequence work may escalate, while quick/simple work stays lean.
- Refresh time-sensitive prices and event status before an update or close wrap. Earlier task notes are leads, not fresh evidence. Respect an explicit "use only this pack" constraint and label the supplied cutoff.

## Run the whole routine

For morning, wrap, colour, catalyst analysis and composed research:

1. Resolve market/session/subject and apply the source router in `integrations.md`: user-supplied Bloomberg export or screenshot first, OpenBB for missing/stale/absent market fields, and official primary sources for reported facts. Public research may supplement news, not masquerade as a timestamped quote feed.
2. Build or refresh the evidence pack before drafting. Compare peers, benchmarks, related listings and cross-assets where relevant; investigate rather than assume causation.
3. Run `scripts/pack_readiness.py` for topic-radar, morning, wrap, colour or earnings packs. A blocking result stops prose; a limited result must be disclosed.
4. For an update with a supplied or current-task prior pack, run `scripts/pack_delta.py` and lead with material changes. Never claim access to another task's pack.
5. Use the appropriate format and voice from `house-style.md`.
6. Apply the sibling source-verifier instructions to the claims and citations. Use the fact-check helper on structured claims where appropriate; it does not prove semantic support.
7. Apply the sibling desk-editor instructions. Remove or qualify unsupported claims; if the conclusion cannot be supported, return a limited draft or concise evidence-gap request.
8. Return the finished draft and only material unresolved gaps. The user does not need to request each review pass or receive a narration of every checklist item.

For event-trade-ideas, verify the event and assess catalysts first, then create
at most three researched scenarios and perform the same verification/editing
passes. Zero supported ideas is an acceptable result.

For merger-arb, special-situations and deal-monitor, use the event-driven
references and `merger_arb/v1` calculation input where applicable. These deal
inputs are not market-colour/earnings packs; do not feed them into pack-readiness
or pack-delta under an unrelated schema. Verify terms, aligned quotes and costs,
compare dated deal snapshots, then perform the same verification/editing passes.
Research watchlist files are local artifacts, not brokerage watchlist mutations.

For company-quality, management-review, research-review and idea-funnel, accept
the matching AI Toolbox schema pack when available. Consume it by schema, not
by importing or assuming a repository path. Preserve this desk's source
ranking, verification, APAC conventions and draft controls.

When team escalation is warranted, select parallel-desk,
parallel-company-research or parallel-earnings; use functional roles in
capacity-aware waves and keep the verifier independent.

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
