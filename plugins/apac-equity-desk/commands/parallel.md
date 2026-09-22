---
description: Force the appropriate functional APAC research team for a market, company or earnings request, with independent verification and a chief editor.
argument-hint: [any desk request, e.g. APAC wrap or Japan wrap]
---

Run this request with the full agent team:

$ARGUMENTS

Read `${CLAUDE_PLUGIN_ROOT}/skills/desk/SKILL.md`, then select
`parallel-desk`, `parallel-company-research` or `parallel-earnings` from the
request. Explicit `/parallel` overrides the normal lean-mode threshold.

You are the desk head: brief the agents, pass packs between them in full,
reconcile and present the result. Respect actual capacity, keep the role graph
acyclic and never allow workers to dispatch workers. Give `chief-editor` the
request above word for word and `desk-verifier` only the draft and evidence.
