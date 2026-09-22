---
name: parallel-desk
description: Run broad, deep or explicitly parallel APAC market research with functional agents, independent verification and a chief editor. Activate automatically only for multi-market or multi-company work that clears the desk complexity threshold, or when the user explicitly asks for parallel/multi-agent work; keep simple requests lean.
---

# Parallel Desk

Read `../../references/desk-defaults.md` and
`../../references/intent-routing.md` first. Everything there still applies:
the same house formats, the same session and date handling, the same
human-approval banner. This skill changes who does each stage, not what the desk
produces.

You are the desk head in this mode. You brief the team, move packs between
them, reconcile across markets and present the result. You do not research,
calculate or draft.

Read `../../references/agent-team.md`. In a Codex checkout, use the matching
project agents in `.codex/agents/`. From an installed plugin, create subagents
with the role instructions in this skill and the table below; do not assume a
subagent can see plugin files or prior conversation unless you include the
needed paths and material. Claude Code uses the matching agents in `../../agents/`.

## The team

| Agent | One per | Does |
| --- | --- | --- |
| `market-data-analyst` | market | Quotes, then the Python helpers: indices, breadth, sectors, movers, relative moves, flows. Checks the data for problems. |
| `country-researcher` | market | Policy, macro, FX and rates, overnight context, corporate headlines. |
| `catalyst-investigator` | contested name | Timeline, ranked competing explanations, what would falsify the lead. |
| `chief-editor` | request | Drafts the house-style note from the packs; revises against the verifier. |
| `desk-verifier` | draft | Audits the draft against the packs without knowing how it was reached. |

A subagent sees nothing of this conversation. Whatever it needs — market,
session date, the user's constraints, the packs — must be in its prompt.
Attach or describe every user-supplied Bloomberg export or screenshot in the
market-data brief. The data analyst must prefer it and request OpenBB fallback
only for missing, stale or absent fields; downstream agents receive the full
lineage and conflicts.

## The run

**1. Scope.** Resolve the markets or names, the session dates and the user's
explicit constraints. Keep the user's request word for word; the chief-editor
gets it verbatim.

**2. First wave — capacity-aware.** For every market dispatch a
`market-data-analyst` and a `country-researcher`. Dispatch no more workers than
the environment permits (at most three workers alongside the desk head in a
four-slot environment); batch the rest into later first-wave groups and wait
for every result before continuing.

**3. Second wave — capacity-aware.** Read the mover lists from the data packs.
Dispatch a `catalyst-investigator` for each name whose move stands out from its
sector and index, and for any name the user asked about. Give each one the
security, the session, the move and peer figures from the data pack, and any
related headline from the country pack. Batch to available slots. Skip this
wave when nothing stands out.

**4. Reconcile.** The packs arrive independently, so cross-market facts are
yours: A/H and ADR read-through, one commodity or FX move explaining several
markets, and places two packs disagree. Write short reconciliation notes. When
sources conflict keep both observations, prefer the higher-ranked and more
recent primary source, and say why. Do not alter a figure in any pack.

**5. Draft.** Dispatch `chief-editor` with the user's request word for word,
every pack in full, and your reconciliation notes.

**6. Verify.** Dispatch `desk-verifier` with the draft and the packs and nothing
else. Do not tell it which explanation anyone preferred or how the draft was
built; that isolation is what makes the audit worth running.

**7. Revise — one round.** On `revise` or `block`, dispatch `chief-editor` again
with the draft, the packs and the verifier's findings. Do not patch sentences
yourself. One round only: anything still open after it goes to the user as an
open finding rather than into another loop.

**8. Present.** Return the note with its draft banner, the review notes, any
finding the editor declined and any finding still open. Verification is not
approval to publish.

## What must survive every hand-off

Numbers degrading between contexts is how this mode fails. Guard against it:

- Pass packs in full and unedited. Never summarize a pack before handing it on.
- Figures come from the helpers via the data analyst, and travel as returned.
  Nobody downstream rounds, restates or re-derives one.
- Source URLs and timestamps stay attached to their claims.
- Every role uses the same claim/source-ID registry and independence groups.
  Repeated agent agreement does not raise confidence when the source is shared.
- Every `GAPS`, `UNRESOLVED` and `DATA QUALITY` entry reaches the final review
  notes. A problem an agent found and the desk dropped is worse than not running
  the team at all.
- If an agent fails or returns nothing, retry it once. If it fails again, say so
  in the note. Never draft around a missing market.

No worker may dispatch another worker or invoke an orchestration skill. Only
the desk head controls the acyclic sequence of roles.

## Cost and automatic threshold

Each agent is its own context. A three-market wrap is six agents in the first
wave, a handful of investigators, an editor and a verifier — roughly a dozen
contexts against one for the ordinary workflow. That buys independent gathering,
a data check, an isolated audit and a revision pass. It is for notes that
matter, not for every request. Use it when explicitly requested or when the
automatic threshold in `intent-routing.md` is met. A `quick`, `brief` or `flash`
constraint stays in the ordinary workflow.

## Boundaries

Everything in `AGENTS.md` binds every agent: read-only research, no account or
order mutation, no publication without explicit human approval at that moment,
and nothing represented as personalized investment advice.
