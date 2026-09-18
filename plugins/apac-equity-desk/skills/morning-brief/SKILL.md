---
name: morning-brief
description: Draft a short APAC country morning snippet led by the current opening tape, overnight context and sector leadership, or a pre-open brief when the market is still closed.
---

# Morning Brief

Read `../../references/house-style.md` (voice and morning format), `../../references/source-priority.md` and the morning-snippet contract in `../../references/data-contract.md`.

Resolve the country, session, date and as-of time. Default to a compact three-paragraph snippet, around 150–250 words. A Japan example is a `{JA} JAPAN MORNING` header, the live NKY/TPX divergence, overnight US/rates/commodity and policy context, then current sector leadership/drag. Preserve clear desk shorthand.

When the market is open, lead with the local tape and say whether a move is versus prior close or since opening. Include named heavyweight offsets and counterintuitive moves where supported. For rates, distinguish an intraday high from the session close. Attribute dated central-bank expectations and survey results; a policy base case is not an announced decision.

When pre-open, use a PRE-OPEN header and expectations instead of observed opening performance. An extended watchlist is available only when requested; do not force the default snippet into 10–15 bullet points.

Use Longbridge read-only tools where available; consult `../../references/integrations.md` for unsupported markets. The skills do not create new provider coverage. Keep every claim tied to an evidence pack, distinguish missing data from flat markets and retain contradictions.

Build `format: desk-morning` data and render with `../../scripts/render_morning_brief.py`. Run source-verifier and desk-editor before delivery. Never send, publish or execute trades; the result remains a draft for human review.
