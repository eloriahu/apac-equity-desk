# Multi-agent desk contract

Codex and Claude Code use functional research roles. Market work uses market
data, country context and catalyst investigation. Company and earnings work can
use filings/accounting, business/KPIs, industry/supply chain,
expectations/valuation, management/governance and bear-case challenge. Chief
editing and independent verification are shared. Project-scoped Codex role
files live in `.codex/agents/`; Claude Code role files live in
`plugins/apac-equity-desk/agents/`. Installed skills carry their complete
orchestration contract so they do not depend on project files.

An explicit request for multi-agent, parallel, agent-team or `/parallel` mode
activates the appropriate team. The router may also escalate broad/deep,
multi-market/multi-company or high-consequence work under
`intent-routing.md`. Ordinary one-name questions stay single/composed. A quick,
brief or flash constraint forbids a full team. Narrow conflict checks may use a
two- or three-agent one-wave micro-team without invoking every role.

The desk head must pass the original request verbatim, pass evidence packs in
full, keep sources and timestamps attached, and preserve every gap. It selects
exactly one lead workflow and maintains an acyclic hand-off graph. Workers do
not spawn workers. Market-data and country-context work precede catalyst work;
company/earnings research runs in capacity-aware functional waves; the editor
drafts; the verifier receives only the draft and evidence; one editor revision
follows. No agent may publish, trade, mutate a brokerage account, or read
personal account data.

Never exceed the runtime's available slots. In a four-slot environment, keep
the desk head and at most three workers active, then use later waves. Omit roles
that cannot change the answer.

User-supplied Bloomberg exports and screenshots travel with the market-data brief. OpenBB may fill only missing, stale or absent market fields, and its field-level lineage and conflicts must survive every hand-off.

All roles share one claim/source-ID registry with source `origin` and
`independence_group`. Syndication and derivation remain in the same group.
Multiple agents repeating one source do not increase confidence.
