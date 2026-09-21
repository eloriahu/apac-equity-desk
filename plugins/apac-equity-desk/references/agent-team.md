# Multi-agent desk contract

Codex and Claude Code use the same five roles: market data, country context, catalyst investigation, chief editing and independent verification. Project-scoped Codex role files live in `.codex/agents/`; Claude Code role files live in `plugins/apac-equity-desk/agents/`. When installed outside the repository, `skills/parallel-desk/SKILL.md` carries the complete orchestration contract and Codex can create purpose-briefed subagents without relying on project files.

Only an explicit request for multi-agent, parallel, agent-team or `/parallel` mode activates the team. Ordinary desk prompts use one context.

The desk head must pass the original request verbatim, pass evidence packs in full, keep sources and timestamps attached, and preserve every gap. Market-data and country-context work run concurrently per market; catalyst work follows the mover list; the editor drafts; the verifier receives only the draft and evidence; one editor revision follows. No agent may publish, trade, mutate a brokerage account, or read personal account data.

User-supplied Bloomberg exports and screenshots travel with the market-data brief. OpenBB may fill only missing, stale or absent market fields, and its field-level lineage and conflicts must survive every hand-off.
