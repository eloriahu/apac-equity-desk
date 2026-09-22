---
name: parallel-company-research
description: Orchestrate a full functional-agent deep dive on an APAC listed company only for explicitly parallel work or a genuinely broad, deep or substantive company report. Do not use for a simple one-name question or narrow conflict/high-consequence check; those stay in the normal workflow or a one-wave micro-team.
---

# Parallel Company Research

Read `../../references/intent-routing.md`, `../../references/agent-team.md` and
`../company-fundamentals/SKILL.md`. This is an execution mode, not a larger
permission boundary. The desk head owns scope, hand-offs, reconciliation and
the final response; it does not duplicate the agents' research.

Use the functional roles in `../../agents/` or matching project agents:

1. **Wave 1:** `filings-accounting-analyst`, `business-kpi-analyst` and
   `industry-chain-analyst` work independently.
2. **Wave 2:** after Wave 1, dispatch `expectations-valuation-analyst` with the
   normalized facts and `management-governance-analyst` with the primary-source
   record. Use `bear-case-analyst` here when the thesis is contested or the
   deliverable needs explicit independent challenge.
3. Reconcile source, period, currency, basis and definition conflicts without
   averaging conclusions or changing figures.
4. Dispatch `chief-editor` with the original request and full packs.
5. Dispatch `desk-verifier` with only the draft and evidence packs. One editor
   revision may follow; carry remaining issues to the user.

Respect actual capacity. With three worker slots, dispatch at most three agents
per wave. If fewer slots are available, split the same roles into smaller
waves. Do not create a role merely to fill capacity, and do not run this skill
when `intent-routing.md` says a single/composed workflow is sufficient.

Give every role the same claim/source-ID registry with `origin` and
`independence_group`. Agent agreement never upgrades evidence confidence by
itself. Workers must not spawn workers or invoke another orchestration skill.

The final synthesis must distinguish business quality from investment merit at
the current price, name the decision hinge, identify what is priced in and
retain falsifiers. When the requested deliverable is a full initiation,
DCF/comps workbook or three-statement model, route automatically to Public
Equity Investing when available and hand it the verified APAC packs. If it is
unavailable, state the boundary. Portfolio artifacts require an explicit
portfolio request and remain outside this desk.

All agents are read-only. No account access, position sizing, execution,
publication or sending without explicit human approval.
