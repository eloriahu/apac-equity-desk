---
name: parallel-desk
description: Run an APAC desk request with the full agent team — a market-data-analyst and a country-researcher per market, a catalyst-investigator per contested name, an independent desk-verifier and a chief-editor — for a higher-quality note at a higher token cost. Use when the user asks for multi-agent or parallel mode, the agent team, or /parallel. Claude Code only; ordinary short requests use the single-context workflows.
---

# Parallel Desk

Read `../../references/desk-defaults.md` first. Everything there still applies:
the same house formats, the same session and date handling, the same
human-approval banner. This skill changes who does each stage, not what the desk
produces.

You are the desk head in this mode. You brief the team, move packs between
them, reconcile across markets and present the result. You do not research,
calculate or draft.

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

## The run

**1. Scope.** Resolve the markets or names, the session dates and the user's
explicit constraints. Keep the user's request word for word; the chief-editor
gets it verbatim.

**2. First wave — one message.** For every market dispatch a
`market-data-analyst` and a `country-researcher`. Send all of them in a single
message or they run one after another.

**3. Second wave — one message.** Read the mover lists from the data packs.
Dispatch a `catalyst-investigator` for each name whose move stands out from its
sector and index, and for any name the user asked about. Give each one the
security, the session, the move and peer figures from the data pack, and any
related headline from the country pack. Skip this wave when nothing stands out.

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
- Every `GAPS`, `UNRESOLVED` and `DATA QUALITY` entry reaches the final review
  notes. A problem an agent found and the desk dropped is worse than not running
  the team at all.
- If an agent fails or returns nothing, retry it once. If it fails again, say so
  in the note. Never draft around a missing market.

## Cost

Each agent is its own context. A three-market wrap is six agents in the first
wave, a handful of investigators, an editor and a verifier — roughly a dozen
contexts against one for the ordinary workflow. That buys independent gathering,
a data check, an isolated audit and a revision pass. It is for notes that
matter, not for every request, which is why ordinary short requests never
trigger it.

## Boundaries

Everything in `AGENTS.md` binds every agent: read-only research, no account or
order mutation, no publication without explicit human approval at that moment,
and nothing represented as personalized investment advice.
