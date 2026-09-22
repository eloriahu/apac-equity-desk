---
description: Automatically route a natural-language APAC equity question to the minimum useful workflows and agent mode, then run it end to end.
argument-hint: [short request, e.g. Japan wrap]
---

Run the APAC equity desk workflow for this request:

$ARGUMENTS

Read `${CLAUDE_PLUGIN_ROOT}/skills/desk/SKILL.md` and follow it. It routes the
request to one of the sibling skills and lists the review passes included by
default. If the request is empty, ask for the task and the market, security or
event in one short question.

This command and the `desk` skill share a name on purpose: both do the same
semantic routing. The user does not need to name skills or agents.
