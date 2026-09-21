---
name: company-fundamentals
description: Review an APAC listed company's business quality, reported financials, expectations, valuation, catalysts, risks and falsifiers from requests such as fundamental review, initiate on this name, valuation check, or what changed in the model.
---

# APAC Company Fundamentals

Resolve the issuer, primary listing, reporting currency, fiscal calendar, accounting basis and investor question. Read `../../references/integrations.md`, `../../references/source-priority.md` and the `fundamental_pack/v1` section of `../../references/data-contract.md` before collecting evidence.

## Evidence pack

Prefer user-supplied Bloomberg/model exports and official company, exchange or regulator filings. When installed, `fundamental-tools` may provide country adapters, transparent metrics and valuation scenarios; consume its `fundamental_pack/v1` output rather than importing its repository. If it is unavailable, assemble the same fields from supplied or public evidence and declare the reduced capability.

For Japan prefer J-Quants/JPX, for Korea OpenDART/FSS, for Taiwan TWSE/MOPS, and for US-listed APAC issuers SEC filings. FinanceToolkit is a calculation layer, FinanceDatabase is identity metadata, and AKShare is a labeled fallback. None outranks an official filing.

Run the desk source-verifier on material claims and preserve reported, provider-standardized, consensus, management-guidance, derived and assumed values separately. Never silently mix currencies, scales, periods, consolidated/standalone accounts or reported/adjusted bases.

## Analysis

Address only the sections supported by the question and evidence:

- business and segment economics;
- revenue, margin and earnings progression;
- cash conversion, reinvestment, balance-sheet capacity and capital allocation;
- reported results versus guidance/consensus and what changed;
- peer-relative and scenario valuation with current market-data as-of time;
- the decision hinge, variant perception and what appears priced in;
- dated catalysts, material risks, contradictory evidence and explicit falsifiers.

State whether the pack is `ready`, `limited` or `blocked`. Do not produce a target price or confident recommendation when current price, diluted shares, net debt, comparable history or valuation assumptions are materially unsupported. Sensitivities are derived scenarios, not facts.

When the explicitly invoked Public Equity Investing plugin owns a larger artifact—initiating coverage, a DCF/comps workbook, model update or thesis tracker—use this APAC pack as its evidence handoff and let that specialist own the hero deliverable. Retain this desk's source hierarchy, APAC conventions and draft controls.

## Output

Lead with the investment-relevant answer, then the supporting financial/valuation bridge, debates and watch items. Include source IDs beside material facts, the data cut-off, unresolved conflicts and next required evidence. Run `../source-verifier/SKILL.md` and `../desk-editor/SKILL.md`; keep `DRAFT — HUMAN APPROVAL REQUIRED` on research intended for circulation.
