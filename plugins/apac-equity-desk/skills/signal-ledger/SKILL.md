---
name: signal-ledger
description: Maintain an explicit APAC research-thesis ledger from requests such as track this thesis, update the signal, what changed, or has this idea strengthened, weakened or been falsified.
---

# Signal Ledger

Use only a ledger supplied in the current task or at an explicit file path. Never imply hidden or cross-task memory.

For each thesis retain: stable ID, statement, created/updated timestamps, horizon, supporting observations, counterevidence, confirmation conditions, invalidation conditions, status and source IDs. New evidence must be classified `strengthened`, `weakened`, `falsified` or `unchanged` with a reason.

Use `../../scripts/research_ledger.py` with an explicit `--output` path. Show the delta from the prior ledger using `../../scripts/pack_delta.py`. Do not overwrite a ledger silently, and do not delete conflicting history. A ledger records research evolution; it is not a position, alert, order or personalized recommendation.
