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

Choose exactly one lead route. Required enrichers form a one-way support graph
from that lead; an enricher must not launch another workflow or its own agents.
The desk head alone may add, remove or sequence support work. This prevents
nested fan-out, duplicated research and circular hand-offs.

## Minimum-sufficient routing

- **Single** — one narrow workflow answers the request. Examples: check a
  supplied note, update a supplied ledger, or review one clearly defined
  management commitment.
- **Composed** — one lead workflow needs two or more evidence lanes, but one
  context can reconcile them. This is the default for a one-company move,
  ordinary earnings review and most company research.
- **Agent team** — use when the user explicitly requests parallel work or the
  deliverable is broad/deep enough to benefit from independent functional
  research. For a narrow but materially conflicted or numerically sensitive
  question, prefer a two- or three-agent micro-team in one wave rather than the
  full research team. Multiple available skills alone does not qualify.

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
screen or idea generation. Activate `idea-funnel` only when the user asks
`who benefits/loses`, asks for ideas or candidates, or an evidence-supported
cross-market chain is central to answering the question. Separate observed
explanation from downstream research scenarios.

If evidence does not discriminate, preserve the unresolved outcome. Never add
more workflows merely to manufacture certainty.

## Automatic agent threshold

Use any agents only when one strong condition or two moderate conditions apply.
Then choose the smallest team that resolves the need:

- **One-wave micro-team (two or three workers):** a narrow request has material
  source conflict, a high-consequence numerical conclusion or a clear need for
  independent challenge. This is not a full research team.
- **Full team:** the user explicitly requests parallel/full-team work, or the
  deliverable is genuinely broad/deep: multi-market, multi-company, a
  substantive research report or a full company/results deep dive.

Strong conditions:

- the user explicitly asks for multi-agent, parallel, exhaustive or independent work;
- a genuinely broad multi-market/multi-company deep dive or substantive report is requested;
- material source conflict or a high-consequence numerical conclusion needs an
  independent challenge; use only a micro-team when the underlying request is narrow.

Moderate conditions:

- more than one market or more than three companies need primary-source work;
- the request spans at least four independent research lanes;
- it requires both detailed historical reconstruction and forward valuation;
- evidence volume cannot be reconciled reliably in one context;
- a client-ready deep report requires independent verification beyond the routine desk pass.

Two moderate conditions permit agent escalation, but do not by themselves
justify every role. Use a full team only when the requested scope is also
genuinely broad or deep; otherwise use the one-wave micro-team.

Use the task's actual agent capacity. With a four-slot environment, the desk
head plus at most three workers run at once. Batch additional roles into later
waves; never dispatch more workers than available slots. A simple one-name
question stays lean even though agents exist.

`Quick`, `brief`, `flash` or an equivalent user constraint forbids a full team.
An explicit `parallel`, `multi-agent` or `independent team` request forces the
appropriate team unless doing so would violate a stronger safety boundary.
Agents never spawn other agents. Give all agents one shared claim/source-ID
registry so duplicated syndication is not mistaken for independent evidence;
agreement between agents does not raise confidence unless their underlying
sources are genuinely independent.

Choose the specialized orchestrator:

- market/country wrap or multi-name move investigation -> `parallel-desk`;
- full company/fundamental research -> `parallel-company-research`;
- complex results or reporting-season comparison -> `parallel-earnings`.

## Route examples

The machine-readable acceptance cases in `routing-evals.json` preserve these
decisions for release checks. They are an evaluation contract for the semantic
router, not a keyword-matching runtime.

- `TSMC is up 6%, why?` -> market-color, composed evidence lanes, no team.
- `CATL is up; who benefits?` -> market-color leads; cross-market/idea-funnel
  supports only after the observed move is explained.
- `Find AI power bottlenecks and APAC names` -> idea-funnel leads.
- `Has my short thesis changed?` -> research-review only when the current task
  or explicit path supplies the baseline; otherwise ask for it.
- `Quick earnings take` -> earnings-review, never a full team.
- `Parallel deep dive on these five companies` -> parallel-company-research.
- `Full initiation and DCF` -> Public Equity Investing owns the artifact
  automatically when available; AI Toolbox supplies calculations and the desk
  supplies verified APAC evidence. If unavailable, state the boundary.

## Stop and hand off

Stop collecting when the stated question is answered, critical claims are
supported or explicitly unresolved, and another lane is unlikely to change the
conclusion. Put attractive but unnecessary work under optional follow-ups; do
not execute it silently.

APAC Equity Desk owns regional evidence, interpretation and desk writing. When
the requested deliverable is a full initiation, three-statement model or
DCF/comps workbook, route it automatically to Public Equity Investing when
that plugin is available and pass the verified APAC evidence pack. If it is
unavailable, state the capability boundary rather than imitating the full
artifact. Portfolio sizing or hedge design routes only when the user explicitly
asks for portfolio work. The desk never gives personalized sizing or trades.

For thesis-drift questions, require a prior thesis/report from the current task
or an explicit path. If no baseline exists, ask one concise question for it
rather than inventing a comparison. For an ambiguous ticker/listing, ask one
concise identity question before collecting data.
