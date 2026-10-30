# Plan the analysis before selecting tools

For a research request, the lead owns this procedure before `tool-selection.md`.
Read it even when the user directly invokes a focused skill. Supporting modules
receive a scoped assignment and reuse the plan; they do not restart this router.
Development and edit-only work retain their own scope.

## Understand the question

Infer the requested answer from the question, current task and supplied material.
Resolve issuer/listing, period, cutoff and deliverable. Distinguish a reported
result, its quality, changing expectations, the market reaction and implications:
these are different questions even when the user puts them in one sentence.
Choose one lead under `intent-routing.md`, then state the subquestions that must
be answered. One lead owns synthesis; multiple skills and tools can contribute
to the same question. A short or misspelled prompt is still an ordinary request.

Example: “Review these earnings” normally asks what happened, why, whether it is
repeatable, how it compares with expectations/guidance, and what changes next.
“Only calculate the EPS beat” asks for one comparable calculation. “Good results,
why did it fall?” makes the price reaction the main question and earnings analysis
its support. Do not decide the conclusion from those descriptions alone.

## Build a scoped analysis plan

Read `research-modules.md`. Choose the modules whose outputs answer those
subquestions, using installed specialist skills automatically when their inputs
and runtimes are available. The user does not need to name the plugin or approve
ordinary read-only analysis. Discover and read each selected installed SKILL.md;
listing its name in the plan is not invoking it.

Keep a compact private decision record, not a transcript of deliberation:

```yaml
lead: earnings-review
objective: assess the result and what it changes
questions:
  - What drove the reported earnings change?
  - How much is recurring and supported by cash flow?
  - What changed versus pre-result expectations and guidance?
assignments:
  - capability: fundamental-analysis
    purpose: normalize the reported periods and explain profit/cash drivers
    inputs: official results, comparable history, source registry
    output: scoped fundamental_pack/v1 with comparisons and limitations
  - capability: expectations-analysis
    activate_when: dated estimate revisions are material to the answer
    inputs: two comparable dated consensus/model snapshots
    output: expectations_bridge/v1, or a specific unavailable-baseline gap
```

Each assignment needs a purpose, minimum inputs, expected output and completion
check. Sequence dependencies: retrieve/normalize facts before calculating;
establish the event before tracing beneficiaries; obtain two snapshots before
claiming revisions. Independent evidence lanes may run together only under the
existing agent policy. For agent-team execution, map assignments to the roles
and handoff protocol in `agent-assignments.md`; check capacity and prerequisite
results before dispatch. Modules alone do not require agents or separate chats.

Give a supporting skill the narrow assignment, with the user's original question
as context. Ask it to return its evidence/calculation output to the lead, without
starting another router, full report, downstream artifact or agent team. Honor
the skill's invocation policy and requirements. Reuse the source/claim registry,
entity identity and period definitions across all modules. Add every substantive
module needed for a distinct material subquestion; there is no fixed count cap.
Use existing results where they suffice. Agent concurrency is a separate runtime
constraint and does not limit the total tools or modules in the research plan.

## Earnings default

For an ordinary earnings review, use `fundamental-tools:fundamental-research`
automatically when available. Limit the assignment to the reported-period
analysis needed here; statement normalization does not require a DCF. Keep the
desk's `earnings_surprise.py` and earnings readiness check as separate steps.

The lead investigates these questions with the available evidence:

1. Normalize actuals and comparable periods: currency, scale, basis, fiscal
   period, reported/adjusted reconciliation and source IDs.
2. Explain revenue, segments, margins and profit changes. Check identified
   one-offs, cash conversion, working capital and balance-sheet items when they
   could alter the interpretation; unavailable cash data stays a stated gap.
3. Compare actuals with the dated pre-result consensus and guidance on the same
   basis. Separate missing consensus from an in-line result.
4. Assess forward implications. Add `expectations-analysis` for dated revisions,
   `filing-analysis` for changed disclosures requiring two documents, or
   `research-audit` for management promises, thesis drift or critical-number
   reliability when those questions matter. Each requires its own baseline.
5. Add market/peer context for a requested or material reaction explanation.
   Use `candidate-analysis` for an actual beneficiary/candidate question, and
   the investment-artifact owner only for a requested full model/DCF deliverable.

A quick review compresses the answer and focuses the checks; it does not turn
missing evidence into facts. An explicitly EPS-only calculation stays narrow.
When the specialist is unavailable, the lead performs supported normalization
and calculations from original sources and reports the reduced scope.

## Let findings change the plan

After each material result, ask whether it answers the subquestion and whether a
new finding changes what is needed. A profit beat alongside weak cash conversion
calls for a scoped receivables/working-capital follow-up. A beat alongside weaker
guidance calls for a forward comparison. A share-price decline alone does not
establish estimate cuts or a new market expectation.

Add or revise an assignment only for a concrete unanswered question that could
change the answer. If a required input is missing, first use an accessible,
permitted source or the current task. Otherwise limit the affected conclusion
or ask for the essential baseline. Repeated calls and extra modules cannot
substitute for missing data. Keep unaffected analysis moving.

## Synthesize one answer

Use `tool-selection.md` to bind the planned modules and their lower-level needs
to actual tools, runtimes and fallbacks. Returned material must satisfy the
relevant contracts before helpers consume it. Preserve facts, management claims,
consensus, derived values and assumptions as distinct evidence types.

The lead integrates the outputs into one answer to the original question. It
must not concatenate module reports or let each module write a competing view.
Account for every required subquestion with evidence or a material limitation;
then perform source verification and desk editing. Neither an installed skill,
a completed checklist nor agreement among modules establishes the conclusion.

The planning cases in `routing-evals.json` specify expected decompositions and
conditional modules. They are semantic acceptance criteria, not a keyword
classifier or evidence of measured model accuracy.
