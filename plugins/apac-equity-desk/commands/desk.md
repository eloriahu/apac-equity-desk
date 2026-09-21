---
description: Route a short APAC desk request (Japan morning, HK wrap, CATL colour, ideas from this, check this, tighten this) to the right workflow and run it end to end.
argument-hint: [short request, e.g. Japan wrap]
---

Run the APAC equity desk workflow for this request:

$ARGUMENTS

Read `${CLAUDE_PLUGIN_ROOT}/skills/desk/SKILL.md` and follow it. It routes the
request to one of the sibling skills and lists the review passes included by
default. If the request is empty, ask for the task and the market, security or
event in one short question.

This command and the `desk` skill share a name on purpose: both do the same
routing, and this is the explicit way to ask for it.
