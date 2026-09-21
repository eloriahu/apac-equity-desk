---
description: Run a multi-market or multi-name APAC request with researcher subagents in parallel, then verify and draft centrally. Claude Code only.
argument-hint: [request spanning several markets or names, e.g. APAC wrap]
---

Run this request in parallel mode:

$ARGUMENTS

Read `${CLAUDE_PLUGIN_ROOT}/skills/parallel-desk/SKILL.md` and follow it.

Dispatch every gatherer in one message so they run concurrently. Draft and edit
in this context, not in a subagent, and send `desk-verifier` the draft and the
packs only.

If the request covers a single market or a single name, say so and run the
ordinary workflow instead — fan-out costs more and returns the same note.
