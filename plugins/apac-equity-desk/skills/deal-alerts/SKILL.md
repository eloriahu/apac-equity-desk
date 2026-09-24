---
name: deal-alerts
description: Evaluate local research alerts for deal status, terms, spread changes, deadlines and stale data with persisted duplicate suppression. Use for deal alert rules or material-change notifications; no brokerage alert mutation or automatic messaging.
---

# Deal Alerts

Read [research standards](../../references/event-driven/research-standards.md),
[toolkit contracts and examples](../../references/event-driven/toolkit.md), and
[market data integrations](../../references/integrations.md).

1. Establish a deal ID, prior/current dated research snapshots and explicit thresholds: spread widening in basis points of target price, deadline window and stale-data hours. Thresholds are user choices, not universal investment rules. Store rule versions alongside the input.
2. Run the alerts helper on deal_alerts/v1. A missing prior snapshot establishes a baseline and cannot produce change claims. A missing price is a data-gap alert, not a zero spread. Status, normalized terms, consideration and deadline changes retain before/after evidence in the research pack.
3. Persist next_state and current snapshot together in the user's research workspace after successful evaluation. Serialize evaluations per deal. Reuse the state on retries; deliver only newly emitted events. Persistent conditions rearm after clearing. Changes are measured against the supplied previous observation, so choose and disclose polling cadence.
4. Closed/settled, withdrawn, terminated and lapsed statuses suppress deadline, freshness and missing-price alerts. Review every material alert with original sources before writing its implication; an alert is not a trade instruction.
5. This helper neither schedules nor sends. If the user explicitly requests an ongoing monitor, use the host's supported automation tool after resolving watchlist, cadence/timezone and sources. Notify only on meaningful changes, failures or required action; stay quiet when unchanged. Keep state local and never mutate brokerage alerts/watchlists. External messaging needs the user's explicit instruction.
6. Present triggered change, supporting timestamp/source, research consequence and next verification step. Report stale/inaccessible feeds as gaps; do not label silence as no new disclosures.

Use the `alerts` example and helper described in the toolkit. Preserve the input
and output beside the source pack. Run source-verifier and desk-editor for the
reader-facing research draft; retain `DRAFT — HUMAN APPROVAL REQUIRED`.
