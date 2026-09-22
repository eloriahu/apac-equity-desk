---
name: management-review
description: Assess management quality, governance and capital allocation for an APAC listed company. Use for questions about whether management delivered, promise-versus-outcome history, incentives, acquisitions, buybacks, dividends, succession or governance risk.
---

# Management Review

Resolve the issuer, relevant executives/board, review period and the decision
the user is trying to inform. Read `../../references/source-priority.md`,
`../../references/integrations.md` and the `research_review/v1` section of
`../../references/research-contracts.md`.

Build a promise-versus-delivery ledger from dated, attributable statements.
For each commitment record what was promised, when, the measurement window,
the actual outcome, source IDs and status: `delivered`, `partial`, `missed`,
`pending`, `withdrawn` or `unclear`. Source the measured outcome separately
from the original promise; qualitative or partial assessments need their own
sourced rationale. Do not score vague aspirations as precise commitments, and
do not use hindsight to redefine the original promise.

Assess only with available evidence:

- operating execution across favourable and difficult periods;
- capital allocation: organic reinvestment, acquisitions/disposals, leverage,
  dividends, buybacks and dilution;
- incentives, ownership, related-party issues, board independence and succession;
- disclosure consistency, restatements, changing KPI definitions and treatment
  of minority shareholders;
- evidence against the favourable interpretation.

Separate outcomes management controlled from macro, FX, commodity or policy
effects. Avoid personality judgments and investor impersonation. State what
cannot be assessed because the record is too short or disclosure is weak.

When an AI Toolbox `research_review/v1` pack is supplied, consume it by schema
and preserve its source links, researchability ceiling and quality status.
Apply the desk source hierarchy independently; do not treat the pack's score as
a fact.

Output the decision-relevant conclusion, ledger, capital-allocation assessment,
governance flags, strongest counterevidence and next evidence to watch. Run the
source-verifier and desk-editor passes. Keep the human-approval banner; never
turn the review into personalized advice or a trade instruction.
