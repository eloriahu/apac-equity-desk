---
name: deal-radar
description: Discover newly announced APAC deals and amendments from a defined source universe; deduplicate evidence and expose coverage gaps. Use for new deals today, takeover radar or recent transaction announcements. Use special-situations for investment candidate ranking.
---

# Deal Radar

Read [research standards](../../references/event-driven/research-standards.md),
[toolkit contracts and examples](../../references/event-driven/toolkit.md), and
[market data integrations](../../references/integrations.md).

1. Establish markets, event types and publication window. Default to the current APAC session when clear; report countries and sources actually checked. Read the jurisdiction source directory. Search official exchange, company and regulator announcements with available browser/search tools; use secondary news to find primary documents. No universal live-feed connection is bundled.
2. Record canonical deal/security IDs, stage, headline, source URL, publication and observation timestamps, extracted terms and verification status. Treat rumors and preliminary proposals separately from firm offers. A secondary report cannot become primary evidence through repetition.
3. Normalize records into `deal_radar/v1` and run the radar helper. A cutoff excludes both future publication and future observation. Retain amendments and conflicting observations; exact duplicate records are removed. The latest verified official record leads, with all supporting records retained.
4. Review conflicting concurrent terms against the source documents. Present new deals, material amendments, unresolved reports and coverage gaps with links. A document verification flag is an analyst assertion; the helper cannot authenticate it.
5. Use merger-arb only when economics are requested, or special-situations when the user asks to rank candidates. No attractiveness ranking from headlines or gross spread alone.

Use the `radar` example and helper described in the toolkit. Preserve the input
and output beside the source pack. Run source-verifier and desk-editor for the
reader-facing research draft; retain `DRAFT — HUMAN APPROVAL REQUIRED`.
