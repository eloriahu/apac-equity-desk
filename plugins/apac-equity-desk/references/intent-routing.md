# Automatic intent routing

The user supplies the question; the desk chooses the minimum sufficient
workflow. Slash commands remain shortcuts, not prerequisites. Route by meaning,
not by literal keyword matching.

## Classify before acting

Make a short internal assessment across five dimensions:

1. **Observation or question** — price/volume move, news/event, results,
   business fundamentals, management, thesis change, quality/income, theme or
   editing/audit.
2. **Research horizon** — current session, event window, coming quarters or
   multi-year structural work.
3. **Requested deliverable** — explanation, desk note, calendar, review,
   company comparison, candidate funnel or full investment artifact.
4. **Evidence availability** — supplied pack; primary sources available;
   partial coverage; material conflict; or no decision-grade evidence.
5. **Complexity and consequence** — number of entities/markets, depth,
   calculation sensitivity, disputed evidence, requested independence and
   whether the output is intended for circulation or a material decision.

Keep this routing record internal unless explaining a material limitation:

```yaml
primary_workflow: market-color
required_enrichers: [source-verifier, desk-editor]
optional_followups: [idea-funnel]
execution_mode: composed
reason: one-name move requires several evidence lanes but not separate agents
stop_conditions:
  - move and relative comparison established
  - candidate drivers tested against timing and counterevidence
  - no additional lane could change the conclusion
```

`execution_mode` is `single`, `composed` or `agent-team`.

## Minimum-sufficient routing

- **Single** — one narrow workflow answers the request. Examples: check a
  supplied note, update a supplied ledger, or review one clearly defined
  management commitment.
- **Composed** — one lead workflow needs two or more evidence lanes, but one
  context can reconcile them. This is the default for a one-company move,
  ordinary earnings review and most company research.
- **Agent team** — use when the user explicitly requests parallel work, or the
  deliverable is broad/deep enough to benefit from independent functional
  research, or material evidence conflict/high numerical consequence requires
  independent challenge. Multiple available skills alone does not qualify.

For ordinary composition, cap the work at one primary workflow and three
substantive enrichers, excluding the routine verifier/editor passes. If a
fourth lane looks useful, decide which existing lane it replaces or escalate
under the criteria below. Do not turn every answer into a full initiation.

## Canonical composite: “XXX stock is up, why?”

Use `market-color` and perform these lanes as one investigation:

1. establish the current or requested-session move, volume and comparison with
   benchmark, sector, peers and related listings;
2. check fresh company disclosures and established company-specific news;
3. check policy, regulation, macro and input-price events with a plausible
   timing/mechanism link;
4. test whether peers, customers, suppliers or the industry moved together;
5. treat positioning, technicals and sentiment as contributing evidence, with
   social chatter kept at Level 4;
6. connect the best-supported driver to a concise revenue, cost, cash-flow or
   valuation fundamental hook;
7. state implications and dated watch points only where the evidence makes
   them useful.

This route does **not** automatically trigger a full financial review, a stock
screen or idea generation. Activate `idea-funnel` only when the user asks who
benefits/loses, asks for ideas or candidates, or an evidence-supported
cross-market chain is central to answering the question. Separate observed
explanation from downstream research scenarios.

If evidence does not discriminate, preserve the unresolved outcome. Never add
more workflows merely to manufacture certainty.

## Automatic team threshold

Use a team when any one strong condition or two moderate conditions apply.

Strong conditions:

- the user explicitly asks for multi-agent, parallel, exhaustive or independent work;
- a full multi-market/multi-company deep dive or decision-ready initiation is requested;
- material source conflict or a high-consequence numerical conclusion needs an independent challenge.

Moderate conditions:

- more than one market or more than three companies need primary-source work;
- the request spans at least four independent research lanes;
- it requires both detailed historical reconstruction and forward valuation;
- evidence volume cannot be reconciled reliably in one context;
- a client-ready deep report requires independent verification beyond the routine desk pass.

Use the task's actual agent capacity. With a four-slot environment, the desk
head plus at most three workers run at once. Batch additional roles into later
waves; never dispatch more workers than available slots. A simple one-name
question stays lean even though agents exist.

Choose the specialized orchestrator:

- market/country wrap or multi-name move investigation -> `parallel-desk`;
- full company/fundamental research -> `parallel-company-research`;
- complex results or reporting-season comparison -> `parallel-earnings`.

## Stop and hand off

Stop collecting when the stated question is answered, critical claims are
supported or explicitly unresolved, and another lane is unlikely to change the
conclusion. Put attractive but unnecessary work under optional follow-ups; do
not execute it silently.

APAC Equity Desk owns regional evidence, interpretation and desk writing. When
the user explicitly invokes Public Equity Investing for a full initiation,
three-statement model, DCF/comps workbook, portfolio artifact, sizing or hedge
design, pass the verified APAC evidence pack to that plugin and let it own the
hero artifact. The desk never gives personalized sizing or trades.
