---
name: morning-brief
description: Research and write an APAC morning note from requests such as Japan morning or HK morning. Investigate overnight and local developments, test their company and sector implications, and identify the day's decisive catalysts. Use a short snippet only when requested; label pre-open or retrospective data honestly.
---

# Morning Brief

Read `../../references/desk-defaults.md` for short-request routing, context/date defaults and the included review stages. The user does not need to repeat these instructions or request each pass.

Read `../../references/morning-research.md` for the investigation and completion criteria, `../../references/house-style.md` (voice and morning format), `../../references/prose-quality.md`, `../../references/source-priority.md` and the morning-note contract in `../../references/data-contract.md`.

Resolve the country, session, date and as-of time with `../../scripts/session_clock.py`, not from memory of the timetable. Verify holidays against an exchange calendar when material. Establish what changed since the previous local close, including intervening holidays/weekends. For a historical recap, use only evidence available by the requested morning cutoff.

An ordinary morning request authorizes active research with available read-only sources. Begin with broad discovery, then pursue the material questions raised by what you find. Open original disclosures, investigate company/sector exceptions, compare competing explanations and revisit the lead when evidence changes it. Reading the workflow, summarizing the supplied headlines or filling the narrative fields does not complete the research. A short prompt or one lead workflow does not limit research depth. Respect explicit source and time limits.

Default to a developed country note, roughly 500–900 words when the evidence warrants it, without a fixed paragraph count. Let significance and remaining uncertainty determine the research effort and emphasis. A requested flash, snippet or word limit controls presentation; it does not excuse unsupported claims. Preserve clear desk shorthand.

When the market is open, lead with the local tape and say whether a move is versus prior close or since opening. Include named heavyweight offsets and counterintuitive moves where supported. For rates, distinguish an intraday high from the session close. Attribute dated central-bank expectations and survey results; a policy base case is not an announced decision.

Explain each material move you choose to include. An overnight handover such as "AI stocks led" must say why that theme moved, the dated trigger, and how the mechanism reaches the local leaders. Local sector leadership also needs a confirmed or plausible driver and a peer-relative fit. When no common driver is supported, say so and give the ranked alternatives rather than substituting labels such as `risk-on`, `rotation` or `profit-taking` for analysis.

When pre-open, use a PRE-OPEN header and expectations instead of observed opening performance. Include the relevant upcoming catalysts, their local times when verified, and what outcomes would challenge the morning view. Keep this selective; do not manufacture a long watchlist.

Prefer a user-supplied Bloomberg export or screenshot for the opening tape. Consult `../../references/integrations.md` and use OpenBB only for missing, stale or absent market fields. Keep every claim tied to an evidence pack, distinguish missing data from flat markets and retain contradictions.

Maintain the working evidence pack and research questions described in `morning-research.md`; derive the `format: desk-morning` narrative pack from that work. Its optional `local_context`, `research_focus` and `watch` fields preserve deeper findings in `../../scripts/render_morning_brief.py`. The renderer and pack-readiness helper check structure, not research sufficiency.

Run source-verifier and desk-editor before delivery. When either exposes a material research gap, the morning lead resumes targeted collection if an accessible source could resolve it, then revises and rechecks the affected claims. The editor itself remains an editor. Finish when the material questions have supported answers or specific, honestly bounded unresolved outcomes; do not stop just because a pass ran. Never send, publish or execute trades; the result remains a draft for human review.
