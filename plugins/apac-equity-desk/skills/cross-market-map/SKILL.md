---
name: cross-market-map
description: Map an event across APAC equities from requests such as cross-market read-through, who benefits, transmission map, or trace this catalyst through suppliers, peers, commodities and FX.
---

# Cross-Market Map

Define the event node, affected fundamentals and candidate securities. Read `../../references/sector-playbooks.md`, but treat every playbook link as a question to verify, not a fact.

Build explicit nodes and directed edges. Each edge needs a mechanism, evidence source IDs, timing and a 0–1 confidence value. Run `../../scripts/transmission_map.py`; disclose cycles, unsupported edges and timing mismatches. Present only the paths supported by the evidence pack, then list plausible but unproven paths separately.

Distinguish direct revenue/cost exposure, second-order supplier/customer effects, valuation/risk-premium effects and simple price correlation. Include what would falsify each leading path. Do not present a transmission path as an instruction to trade.
