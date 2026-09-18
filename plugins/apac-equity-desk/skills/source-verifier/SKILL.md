---
name: source-verifier
description: Audit finance claims, citations, timestamps, numerical consistency and source independence before APAC desk material is shared. Use for fact checking drafts or evidence packs.
---

# Source Verifier

Read `../../references/source-priority.md` and the fact-check schema in `data-contract.md`. Decompose the draft into atomic factual and causal claims. For each claim verify the cited source actually supports it, source level, publication/event time, primary-versus-repost status, units/currency/session and whether subsequent information superseded it.

Run `../../scripts/fact_check.py` on a structured claim bundle. Escalate: uncited facts, causal statements resting only on Level 4 material, contradictory numeric values, stale live data, non-overlapping timestamps, unattributed estimates and circular sourcing. Return `pass`, `revise` or `block`, with minimal corrections. Verification does not authorize publication.
