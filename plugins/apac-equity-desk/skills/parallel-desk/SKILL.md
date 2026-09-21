---
name: parallel-desk
description: Run a multi-market or multi-name APAC desk request by dispatching researcher subagents in parallel, then verifying and drafting centrally. Use for a regional wrap, several countries at once, or a basket of names needing separate driver work. Claude Code only; a single-market or single-name request uses the ordinary workflow instead.
---

# Parallel Desk

Read `../../references/desk-defaults.md` first. Everything there still applies:
the same house formats, the same review passes, the same session and date
handling. This skill only changes *how the gathering is done*, never what the
desk produces.

## When this is worth it

Fan out only when the pieces are genuinely independent:

- A regional wrap, or two or more country closes in one request.
- A basket of names that each need their own driver assessment.

Do not fan out for one market or one name. The ordinary workflow is cheaper and
the result is the same. Do not fan out to split the data work from the news work
inside a single market: the mover list decides which catalysts matter, so those
two stages are sequential and a subagent boundary between them just adds a round
trip and a chance to garble numbers.

## How to run it

**1. Resolve scope in the parent.** Decide the markets or names, the session
dates and any explicit user constraints before dispatching anything. A subagent
cannot see the conversation, so whatever it needs must be in its prompt.

**2. Dispatch gatherers concurrently.** Send every subagent call in a single
message, or they run one after another and the parallelism is lost.

- One `market-pack-builder` per market. Give it the market, the session date and
  any format or length constraint that affects what to collect.
- One `catalyst-investigator` per name that needs driver work. Give it the
  security, the session, the observed move and the comparison group.

**3. Reconcile in the parent.** The packs come back independently, so
cross-market facts are your job: A/H and ADR read-through, a commodity or FX
move that explains several markets at once, and any place two packs disagree.
Preserve both observations and explain the discrepancy; prefer the
higher-ranked, more recent primary source.

**4. Draft in the parent.** Do not ask a subagent to write client-facing prose.
One context owns the house voice, and the packs are inputs to it. Use the format
from `../../references/house-style.md` that matches the request — regional
digest for a regional wrap, the developed country close per country when
countries were requested individually.

**5. Verify independently.** Dispatch `desk-verifier` with the draft and the
packs and nothing else. Do not tell it how you reached the draft or which
explanation you preferred — that is what makes the audit worth running. Act on
its blocking findings before going further.

**6. Edit in the parent.** Apply `../desk-editor/SKILL.md` yourself. Keep the
draft banner and the human publication approval.

## What must survive the fan-out

The failure mode of this mode is numbers degrading as they pass between
contexts. Guard against it:

- Subagents return packs in the `../../references/data-contract.md` shapes, not
  prose. Carry figures across as they were returned; do not re-derive or round
  them.
- Keep each source URL and timestamp attached to its claim through every hand-off.
- Carry every `GAPS` and `UNRESOLVED` entry into the draft's gap list. A gap
  that a subagent found and the parent dropped is worse than no fan-out at all.
- If a pack comes back empty or failed, say so in the note. Do not quietly draft
  around a market you have no data for.

## Cost

Each subagent is a separate context with its own token cost. Five markets is
roughly five times the gathering cost of one. That is worth it for a regional
wrap on a deadline and wasteful for anything smaller, so do not reach for this
mode by default.

## Boundaries

Everything in `AGENTS.md` applies to every subagent: read-only research, no
account or order mutation, no publication without explicit human approval at
that moment, and no representing analysis as personalized investment advice.
