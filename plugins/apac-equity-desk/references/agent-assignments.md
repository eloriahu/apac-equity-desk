# Research-agent assignments and handoffs

The desk head turns `research-planning.md` into scoped worker assignments. Use
the existing roles below; the question determines which roles are needed. Each
worker can use multiple relevant modules and tools. A role is a responsibility,
not a one-tool restriction, and a specialist skill is not a separate agent.

## Role to module map

Read `research-modules.md` and the selected installed skills before executing
them. These are candidate assignments, not a requirement to run every module.

| Role | Assignment and useful modules | Boundary |
| --- | --- | --- |
| `market-data-analyst` | market-normalization, session checks and deterministic market calculations | Own timestamped observations and field lineage; no causal conclusion. |
| `country-researcher` | source-investigation for local policy, macro and corporate developments | Return sourced context; reuse the data analyst's figures. |
| `catalyst-investigator` | source-investigation, scoped fundamental-analysis when needed to test the mechanism | Start from observed moves and chronology; compare competing explanations. |
| `filings-accounting-analyst` | fundamental-analysis and filing-analysis for reported periods, reconciliations and cash quality | Own the normalized financial pack and calculations; no unrequested valuation. |
| `business-kpi-analyst` | scoped fundamental-analysis for segment/KPI drivers and guidance | Research operating evidence; reuse the filings analyst's normalized numbers when available. |
| `industry-chain-analyst` | source-investigation and candidate-analysis for peers, exposures and bottlenecks | Ranking only when assigned; test each economic link. |
| `expectations-valuation-analyst` | expectations-analysis and scoped valuation calculations | Depend on normalized actuals and dated market/estimate inputs; full artifacts retain their specialist owner. |
| `management-governance-analyst` | research-audit for commitments, outcomes and capital allocation | Require original promises and separately sourced outcomes. |
| `bear-case-analyst` | targeted falsification; research-audit or consensus-analysis when that is the assigned question | Receive question and evidence without the preferred conclusion; unsupported criticism is not a finding. |
| `chief-editor` | desk-editor and the selected house format | Draft from returned packs; ask the lead for missing research rather than inventing it. |
| `desk-verifier` | source-verifier, structural checks and scoped research-audit where useful | Fresh independent context, draft plus full evidence only; return findings rather than rewriting. |

## A complete brief

The head supplies each researcher with:

- a unique task ID, role and one concrete research question;
- the original user request, relevant issuer/listing, period, cutoff and scope;
- the resolved plugin root, role-file path and selected skill/reference paths;
- the assigned evidence-need IDs, module scope and expected output contract;
- accessible original inputs and completed dependency packs in full;
- the shared source/claim registry and an ID prefix for any new entries;
- tool availability known to the head, source restrictions and completion checks.

Verify that paths and inputs are accessible to the worker. Provide full content
when paths cannot be shared. A worker does not inherit hidden context, other
chats, credentials or the parent's callable connectors. The worker inspects its
own tools and reports missing access honestly.

The editor receives the original request, full packs and reconciliation notes.
The verifier receives only the draft, full evidence and neutral format/scope
metadata embedded in that evidence. Exclude the team's preferred explanation,
drafting discussion and prior verdict. Use a fresh verifier context; reusing a
researcher or editor as the verifier does not provide independent review.

## Execution and access

Workers invoke the relevant installed skills and helpers for their assignments;
they do not start another router, agent team or full report. Keep one owner for
each calculation/evidence need and share its returned result. Separate readers
may challenge that result, but do not count repeated sources as independent.

Keep the declared read-only tool permissions. If an assigned MCP is unavailable
to a worker, return a `TOOL_REQUEST` containing the exact read-only need, intended
source, safe arguments or schema, expected result and the reason access is
missing. The head can execute that scoped request using its own available tools
and return the unedited result with provenance. This is access brokering, not a
second investigation. Never widen permissions or assume a connection to avoid a
gap; a missing source entitlement remains a gap.

Workers return their packs in the conversation and do not edit shared files.
Use helper stdin/stdout where supported. If a helper requires an input filename,
the head may materialize the supplied structured input in the task workspace,
then give the worker that path; use stdout for the result. Local input preparation
does not authorize source edits, account access, publishing or package installs.

## Handoff status

Keep each role's domain output, adding this compact envelope:

```yaml
task_id: earnings-financials
role: filings-accounting-analyst
status: complete  # complete | limited | blocked
covered_need_ids: [reported-actuals, cash-quality]
modules_used: [fundamental-tools:fundamental-research]
tools_used: []  # actual returned calls/helpers, not planned capabilities
source_ids: []
checks_performed: []
gaps: []
tool_requests: []
followup_questions: []
```

`complete` means the assigned checks ran with returned evidence. `limited`
means useful findings coexist with a material gap. `blocked` means the assigned
answer cannot be supported. A planned tool call or empty result is not completion.
Preserve module readiness even if a missing field is irrelevant to this narrow
assignment; explain which conclusions the gap affects. New findings can propose
follow-up questions, but only the head assigns more work.

The head merges new source IDs deterministically, preserves original values and
independence groups, resolves duplicates without discarding conflicts, and tracks
every required need to a result or material gap. A failed prerequisite blocks
only dependent claims; independent work can continue.

## Capacity and fallback

Check actual native agent capacity, including workers already running. With four
total slots, reserve one for the head and use at most three concurrent workers.
Queue additional roles; available concurrency is not a total role/tool limit.
Wait for required inputs before dispatching dependent work. Reuse a researcher
for a follow-up in its own role, but preserve fresh-context independent review.

Use the host's native subagent API. In Codex, load the project role definition
when supported; otherwise give a native worker the resolved installed role
instructions and complete brief. In Claude Code, use the corresponding plugin
agent. Inherit the user's current model settings unless explicitly overridden.
If native agents are unavailable, state that the assignments will run sequentially
in the current context; do not label that execution an independent agent team.

Retry a failed worker once only when a concrete correction can help. Otherwise
return a limited/blocked handoff and continue independent assignments. Drafting,
verification and one editorial revision follow `agent-team.md`; unresolved
critical findings remain visible and cannot be hidden by a polished final answer.
