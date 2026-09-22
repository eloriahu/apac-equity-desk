---
name: morning-brief
description: Draft a short APAC morning snippet from requests such as Japan morning or HK morning. Include opening tape, overnight context, sectors and the standard verification/editing passes; label pre-open or retrospective data honestly.
---

# Morning Brief

Read `../../references/desk-defaults.md` for short-request routing, context/date defaults and the included review stages. The user does not need to repeat these instructions or request each pass.

Read `../../references/house-style.md` (voice and morning format), `../../references/prose-quality.md`, `../../references/source-priority.md` and the morning-snippet contract in `../../references/data-contract.md`.

Resolve the country, session, date and as-of time with `../../scripts/session_clock.py`, not from memory of the timetable. Verify holidays against an exchange calendar when material. Default to a compact three-paragraph snippet, around 150–250 words. A Japan example is a `{JA} JAPAN MORNING` header, the live NKY/TPX divergence, overnight US/rates/commodity and policy context, then current sector leadership/drag. Preserve clear desk shorthand.

When the market is open, lead with the local tape and say whether a move is versus prior close or since opening. Include named heavyweight offsets and counterintuitive moves where supported. For rates, distinguish an intraday high from the session close. Attribute dated central-bank expectations and survey results; a policy base case is not an announced decision.

Explain each material move you choose to include. An overnight handover such as "AI stocks led" must say why that theme moved, the dated trigger, and how the mechanism reaches the local leaders. Local sector leadership also needs a confirmed or plausible driver and a peer-relative fit. When no common driver is supported, say so and give the ranked alternatives rather than substituting labels such as `risk-on`, `rotation` or `profit-taking` for analysis.

When pre-open, use a PRE-OPEN header and expectations instead of observed opening performance. An extended watchlist is available only when requested; do not force the default snippet into 10–15 bullet points.

Prefer a user-supplied Bloomberg export or screenshot for the opening tape. Consult `../../references/integrations.md` and use OpenBB only for missing, stale or absent market fields. Keep every claim tied to an evidence pack, distinguish missing data from flat markets and retain contradictions.

Build `format: desk-morning` data and render with `../../scripts/render_morning_brief.py`. Run source-verifier and desk-editor before delivery. Never send, publish or execute trades; the result remains a draft for human review.
