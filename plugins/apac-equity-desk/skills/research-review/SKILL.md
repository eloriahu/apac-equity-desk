---
name: research-review
description: Review the reliability and evolution of APAC equity research. Use for thesis drift, what actually changed, researchability or confidence grading, numerical audit, claim support and publication-readiness questions.
---

# Research Review

Read `../../references/source-priority.md` and the `research_review/v1` section
of `../../references/research-contracts.md`. Work only from reports, thesis snapshots
or packs supplied in the current task or at an explicit path. Never imply
hidden cross-task memory.

## Researchability

Grade the name `A`, `B` or `C` based on primary-source coverage, reporting
history, segment/KPI disclosure, estimate/peer coverage and unresolved
conflicts. Set `maximum_supported_confidence` to `high`, `medium` or `low`.
This is an evidence ceiling, not a company-quality score. Name the missing
evidence that creates the ceiling.

## Thesis drift

Compare the prior and current thesis proposition by proposition. If the current
task or an explicit path does not supply a prior thesis/report, ask one concise
question for the baseline and stop the drift comparison. Classify each change
as:

- `fact` — new operating, financial, competitive, regulatory or governance evidence;
- `price` — valuation or expected return changed because market price/estimates changed;
- `wording` — rhetoric or emphasis changed without a corresponding fact;
- `no_change` — neither evidence nor conclusion changed materially.

Set `primary_class` using the dominant supported change. Do not label a thesis
stronger merely because the newer prose sounds more confident. Preserve
contradictory history and explicit falsifiers.

## Numerical and publication audit

Check every critical figure: price, shares, market capitalization, revenue,
earnings, net debt/cash, valuation inputs and target/scenario outputs. For each
row record basis, period, currency, unit, source and `pass`, `fail` or
`unverifiable`. Sample secondary figures only after critical coverage is
complete. A critical failure or unverifiable number used in a key conclusion
blocks the publication gate.

Accept `research_review/v1` from AI Toolbox by schema, without a source-code
dependency. Reperform semantic claim/source review under the desk's rules; a
deterministic audit proves arithmetic and matching, not interpretation.

Return the researchability ceiling, thesis-change table, number-audit summary,
publication gate (`pass`, `blocked` or `not_run`) and remediation list. For a
ledger update, hand the supported thesis delta to `../signal-ledger/SKILL.md`;
do not silently overwrite history. Apply the source-verifier and desk-editor
passes and retain human approval.
