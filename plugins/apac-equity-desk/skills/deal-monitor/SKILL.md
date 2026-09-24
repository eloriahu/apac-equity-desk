---
name: deal-monitor
description: Refresh an event-driven watchlist or compare dated merger snapshots, tracking terms, quotes, spreads, approvals, votes, deadlines and thesis changes. Use for deal updates and monitoring; recurring runs need an available scheduler.
---

# Deal Monitor

Read [research standards](../../references/event-driven/research-standards.md) and
[snapshot format](../../references/event-driven/output-contracts.md). Locate a supplied/task-local
prior snapshot. If absent, create a baseline and state that historical comparison
was unavailable. Never imply access to hidden memory.

Refresh official terms/status and market quotes separately. Compare consideration,
ratio/adjustments, timetable, conditions, financing, votes/court decisions, rival
bids, termination, quotes/borrow/FX and assumptions. Show previous value, new value,
source and implication. Write a new dated snapshot; preserve old assumptions.

Classify the thesis as strengthened, weakened, falsified or unchanged and explain
why. Price convergence alone does not prove declining deal risk. Decompose spread
changes into target, acquirer, FX, dividends/terms, costs and time when data permits;
otherwise use a bounded qualitative explanation. Rerun changed scenario inputs.

Separate announcement, expected decision, vote/acceptance cutoff, long-stop,
effective and settlement dates. Include timezone, source and confirmed/estimated/
conditional status. Do not convert a quarterly window into a precise fact.

For requests to monitor/watch/notify later, establish a current baseline and use
an available automation tool for the requested cadence and scope. A skill or JSON
file is not a scheduler. If unavailable, report a manual baseline. Notify on material
changes, completion, failure or required action; stay quiet on unchanged runs unless
periodic reports were requested. A one-off update does not authorize a recurring job.
