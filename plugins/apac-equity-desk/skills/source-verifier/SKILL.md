---
name: source-verifier
description: Audit APAC finance claims and citations from requests such as check this, including timestamps, source support, numerical conflicts and causal wording.
---

# Source Verifier

Read `../../references/desk-defaults.md` for short-request routing, context/date defaults and the included review stages. The user does not need to repeat these instructions or request each pass.

Read `../../references/source-priority.md` and the fact-check schema in
`../../references/data-contract.md`. Complete two distinct passes over material
claims; do not treat citation presence or a helper's pass as verification of truth.

## First pass: verify the facts

Decompose the draft into factual observations and causal interpretations. Compare
numbers, signs, company/listing identities, units and session cutoffs with the
actual supplied artifacts or source records. Open the sources behind material
news claims and check what they establish, first-publication/event time,
primary-versus-repost status, and corrections or subsequent developments within
the requested cutoff. Recalculate material derived figures where needed.

Cross-check decisive or disputed facts against primary evidence or genuinely
independent reporting when available. Repeated copies of one wire are one source;
do not impose a two-source quota on an unambiguous primary disclosure. Distinguish
a verified fact from an attributed report and an analyst inference. An inaccessible
source or an unresolved conflict remains a stated limitation, never a claimed check.

## Second pass: challenge the explanation

For a News Snippets digest, use `../../references/news-snippets.md`: check
headlines as well as summaries for unsupported certainty, implied causal links
and misleading selection or juxtaposition. Apply the full driver assessment
when a market explanation is claimed; a factual announcement does not require
an invented market view or peer-relative thesis. For a reported move with no
established cause, preserve its date/basis and keep uncertainty brief and clear.

Reassess the draft's lead against the verified facts, starting with the strongest
alternative explanation rather than looking only for confirmation. Check earlier
trends, fresh developments, event/quote chronology, different business exposures,
peer exceptions and evidence against the proposed transmission. If a material
question is unanswered, request targeted source checks from the research lead;
respect explicit source restrictions.

Test both whether a linkage is plausible and how much explanatory weight the
evidence supports. A direct driver, indirect sentiment effect and broader backdrop
may coexist. Retain supported minor links with proportionate wording; do not force
one cause, invent contribution percentages or equate an unproven main-driver claim
with proof of no relationship. A verified event does not settle its market impact.

This is a separate analytical pass, not a reread of the same headline, another
helper run or an automatic requirement for agents. Keep concise internal findings
for each pass: material checks and sources, any changed assessment, and remaining
limitations. Route feasible gaps back to the lead, then recheck corrected claims
and the final lead after editing. Finish when both passes support the wording or
the unresolved boundary is explicit; never report checks that were not performed.

## Supplied-data scope and mechanical checks

For supplied-data research, check `../../references/supplied-data-research.md`:
quotes must remain traceable to the input, while the explanation needs its own
evidence. Check the earlier trend against the event chronology, the catalyst's
reach across different businesses, and claims that weakness `spread` between
groups. Flag a narrow headline used as a sector-wide cause, later news assigned
to an earlier snapshot, and missing research disguised as an uncertainty label.
Check observation scope separately from causal scope: visible names cannot stand
for an unobserved sector, and two groups falling cannot establish a shared cause.
Review leads and transitions for implied links, even when a later caveat qualifies them.
Return resolvable gaps to the research lead before delivery.

Run `../../scripts/fact_check.py` on a structured claim bundle. Mark claims that describe a material move with `movement: true`, then supply `driver_status` and `mechanism` as defined in `data-contract.md`. For live claims, attach the quote/observation time as source `observed_at` and a claim-specific `max_age_minutes`; do not apply an arbitrary freshness limit to filings or structural background. Repeated numeric claims should share a `fact_key` and carry `unit`, `currency` and `session` where relevant. Escalate: uncited facts, causal statements resting only on Level 4 material, material moves with no driver assessment or mechanism, contradictory numeric values, stale live data, non-overlapping timestamps, unattributed estimates and circular sourcing. A label such as `AI strength`, `risk-on` or `rotation` does not count as a mechanism. Return `pass`, `revise` or `block`, with minimal corrections. Verification does not authorize publication.
