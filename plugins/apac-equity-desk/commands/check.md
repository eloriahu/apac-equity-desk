---
description: Audit an APAC desk draft's claims, citations, timestamps, units and numerical consistency, and return pass, revise or block.
argument-hint: [optional: the draft to check]
---

Check the facts and sources in:

$ARGUMENTS

Read `${CLAUDE_PLUGIN_ROOT}/skills/source-verifier/SKILL.md` and follow it.
If the argument is empty, use the draft already in this conversation. Keep the
scope to verification: do not rewrite the note or add new sections. Verification
does not authorize publication.
