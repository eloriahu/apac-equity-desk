---
name: filing-change
description: Explain what changed between two dated APAC company filings, including risk-factor, operating, guidance and governance disclosures. Use for compare annual reports, what is new in this filing, or disclosure-change questions; verify page-level source evidence before interpreting significance.
---

# Filing Change

Before choosing tools, apply `../../references/tool-selection.md`, including
when this skill is invoked directly. Reuse the lead’s plan in supporting work.

Use the `filing-analysis` module in
`../../references/research-modules.md`: read and execute the installed
`fundamental-tools:filing-change-radar` skill for the scoped evidence/calculation
assignment when available. Reuse its returned pack; a missing skill or runtime
uses the documented fallback with the same evidence requirements.

For document retrieval or conversion, read `../../references/research-addons.md`
and select available Firecrawl, local MarkItDown or existing document tools.

Identify the issuer, comparable filing type and two official dated versions. Retrieve from company, exchange or regulator sources under permitted terms; a configured disclosure tool may help locate documents, but is not assumed. If AI Toolbox is available, consume `filing_change/v1`; otherwise compare supplied filings manually using the same fields in `../../references/research-contracts.md`. Page-level text differences and numeric flags are review leads, not conclusions.

Read every potentially important change in context, checking nearby tables and whether extraction/OCR or pagination explains it. Classify the change as new fact, changed forecast/commitment, risk wording, clarification, or formatting; say what is unresolved. Connect only supported changes to the current thesis or model. Verify dates, numbers and citations, then apply the desk edit. Keep `DRAFT — HUMAN APPROVAL REQUIRED`.
