# Select tools for the question

Apply this procedure on every desk request, including a directly invoked skill.
Reuse the current task's plan for an unchanged follow-up; refresh affected needs
when the question, inputs, session cutoff or tool availability changes. The lead
owns the plan; supporting workflows reuse it and add only their assigned needs.

## 1. Define the answer and its evidence needs

For research, apply `research-planning.md` and `research-modules.md` first:
understand the investor question, decompose it into subquestions, and assign the
necessary specialist analysis before choosing retrieval or calculation tools.
Development and edit-only requests keep their existing scope.

Use `intent-routing.md` to choose one primary workflow. Resolve the subject,
listing, session, deliverable and explicit source/length constraints. Identify
what must be established to answer the question, then select the capabilities
below. A conceptual explanation or text-only edit may need no external tool;
record that reason and answer within scope. Typos and short prompts do not reduce
research depth. Ask only for an essential ambiguity that context cannot resolve.

| Question or material | Capabilities to consider |
| --- | --- |
| Why is a stock moving? | market-observation, primary-source, public-discovery; peer and timing checks within the same workflow |
| Morning or close note | market-observation, session-calendar, primary-source, public-discovery |
| Results, filing changes, takeover terms | fundamental-analysis, filing-analysis or deal calculations as the question requires; primary-source; document-tables or document-text when supplied; deterministic-calculation for derived numbers |
| Consensus changes | expectations-analysis, workbook-cells and deterministic-calculation on two dated comparable snapshots; discovery cannot reconstruct missing consensus |
| Empirical test | public-dataset or supplied observations, statistical-design, then regression or bayesian-estimation only if the model and data fit |
| DCF or full initiation | investment-artifact owner plus relevant APAC evidence needs |
| Workbook, slide deck or document deliverable | workbook-cells, presentation-artifact or document-artifact as appropriate |
| Code or skill development | code-navigation, api-documentation, instruction-editing; development-review when useful |
| Check or tighten a supplied note | existing evidence and source-verifier or desk-editor; editing alone does not start fresh research |

## 2. Discover what can actually perform each need

`tool-capabilities.json` is the ordered capability catalog, not an installed-tool
inventory. Discover relevant tools in the current host, inspect their returned
schemas, and read applicable skills before using them. Reuse that discovery
within the task. Installed/configured does not mean callable; a skill does not
prove its Python dependencies or data entitlements exist.

Establish eligibility for the particular input and question: listing/market
coverage, timestamp/session, units, file access, OCR/layout support, runtime
dependencies and user source constraints. A familiar provider with poor coverage
is ineligible for that need. Bind each candidate to an actual discovered tool,
installed skill or executable path. A successful past session is not a present
connection check. Attempt only tools selected for useful work.

Prefer source authority and task fit first, then coverage/freshness and extraction
fidelity, then reproducibility, latency and cost. Catalog order breaks ties among
eligible options. Explicit user preferences reorder eligible candidates; they do
not repair missing coverage or make an unauthorized transfer permissible. Keep
fresh supplied Bloomberg observations first and preserve field-level provenance.
Use `integrations.md` for provider and source ranking, and `research-addons.md`
for document, statistics and development details.

## 3. Make a small, checkable plan

Record each need, selected binding, eligibility evidence, fallback and completion
check in the private evidence/development pack. Keep distinct needs separate:
a financial PDF may require both table extraction and verification against the
original page. No tool count or mandatory second extractor establishes quality.

A question can use multiple tools, including complementary tools for the same
capability. Represent each required role as a separate need with a unique ID:
for example `extract-table` selects Docling while `verify-original-page` selects
the original PDF reader. Execute both when both roles are needed. The helper
selects one candidate per need, not one tool per question; `alternatives` are
substitutes for that particular role, not a place to hide required collaborators.
There is no fixed cap on needs, tools or specialist modules. Reuse results and
add follow-up needs when findings warrant them. Two readers of one document
still share one underlying source; tool multiplicity is not source independence.

For competing candidates, a failure, sensitive local input or numerical/modeling
work, use `scripts/tool_selection.py` when local execution is available:

```sh
python scripts/tool_selection.py /absolute/path/to/tool-request.json
```

Run relative to the plugin directory or resolve the script from this reference.
The input contract is `tool_request/v1`:

```json
{
  "schema": "tool_request/v1",
  "primary_workflow": "earnings-review",
  "needs": [{
    "id": "reported-results-table",
    "capability": "document-tables",
    "required": true,
    "local_only": true,
    "candidates": {
      "docling": {
        "state": "callable",
        "eligible": true,
        "binding": "replace with the discovered conversion tool name",
        "execution": "local",
        "effect": "read",
        "evidence": "replace with observed file access, schema and format support"
      }
    }
  }]
}
```

Replace example bindings/evidence with observed facts. Candidate state is
`callable`, `unverified`, `unavailable` or `failed`; omitted candidates are
undiscovered, never presumed available. Set `eligible` from the task-specific
checks above. `allowed_candidates` restricts sources; `preferred_candidate`
expresses a user preference within that boundary. `local_only` is true for
private documents unless transfer to the selected remote service is authorized.
`effect` is `read` or, for an authorized local artifact/code change, `local_write`.
External writes and brokerage/account mutations are outside this planner.

For one obvious choice, or a host without local execution, apply the same gates
directly and retain the concise plan. The helper selects among supplied eligible
candidates; it neither interprets the user's prose nor independently verifies
eligibility. Its `planned` status never means the research is complete.

## 4. Execute, inspect, and adapt

Call the selected tool and inspect the actual result against the need's completion
check. Preserve original source, locator, timestamp, method and material conflicts.
For numbers, check signs, units, period, table headers and footnotes against the
original. A scraper, converter and model using the same document remain one source.
For code, inspect the relevant symbols and callers, then run appropriate checks.

When a tool fails or its output lacks the required coverage/fidelity, mark that
candidate failed/ineligible for this need and select an eligible fallback. Retry
once only when a specific transient problem or corrected input justifies it;
then switch method or state the gap. Keep useful results already obtained.
Never silently downgrade table extraction to flattened text, current quotes to
undated search snippets, or empirical estimates to assumptions. An equivalent
tool outside the catalog may be used after the same checks; record its binding
and why the catalog options are inadequate, and flag the catalog gap for later
maintenance. Do not install packages or purchase access during routine research.

## 5. Check answer coverage before returning it

The lead reconciles every required need with a returned result or an explicit
material gap, not merely a planned call. Apply the source-verifier and desk-editor
passes for research drafts, plus existing readiness/calculation checks where
their schemas apply. Test chronology, competing explanations and counterevidence.
A failed requirement limits the affected claim, not automatically the whole answer.
Revisit the plan if a new finding could materially change the conclusion.

Keep routing details in the private pack. Explain only material limitations in
the answer unless the user asks which tools were used. Preserve format-specific
presentation, including Japan EOD. Stop when required claims are supported or
explicitly unresolved and further work is unlikely to change the answer.

## Release checks

`tool-selection-evals.json` exercises task-specific choices, privacy/source
constraints and unavailable-tool fallbacks through the actual helper. The existing
`routing-evals.json` remains the semantic workflow acceptance set. These offline
checks do not measure an LLM's routing accuracy or prove future source quality.
Before claiming improved semantic accuracy, replay representative prompts with
recorded model/version, available tools, selected route, actual calls, unmet needs
and human-reviewed answer quality; compare against the same baseline environment.
