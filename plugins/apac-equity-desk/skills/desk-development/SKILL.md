---
name: desk-development
description: Build, fix or extend APAC Equity Desk skills, research pipelines, calculators and dashboards. Use for desk software development and integration requests; market research and investment conclusions stay with the research workflows.
---

# Desk Development

Work in the user's actual desk source project. Read its AGENTS.md and inspect
the current files and working changes before editing. Resolve the requested
behavior from the task; make a concrete, tested local change within that scope.
Research-only controls still exclude brokerage/account mutations. Do not apply
the financial draft banner to code or maintenance status messages.

Use `../../references/research-addons.md` to discover optional capabilities.
These are development aids, not prerequisites or evidence for an investment
conclusion:

| Development need | Integration |
| --- | --- |
| Current API or library syntax | Context7: resolve the library, then query its docs for the installed/target version. Use repository documentation or official docs if unavailable. Send the technical question without proprietary research or credentials. |
| Skill or agent instruction changes | Read Matt Pocock's installed `writing-for-agents` reference; keep triggers precise and disclose detail only where needed. |
| A requested specification | Matt Pocock `to-spec` is an optional explicit invocation. Keep the resulting spec local unless the user has authorized creating an issue. |
| A requested development handoff or retrospective | Matt Pocock `handoff` or `retro`, respecting explicit-only invocation policies. Identify the author/path because gstack also has a `retro` skill. |
| Project tracker setup | `setup-matt-pocock-skills` only when that setup is requested; it is not a dependency of ordinary research or coding. |
| Scope, engineering plan or code review | Relevant installed gstack planning or `review` skill, only when its review adds value to this change. |
| A reproducible bug or user-interface problem | gstack `investigate`, `qa-only`, `qa` or `design-review` as appropriate to the requested inspection or fix. |

Read the selected installed skill before following its process. Preserve its
invocation policy: explicit-only skills remain user shortcuts, not silently
invoked subroutines. When they are not explicitly invoked, complete ordinary
planning and context preservation directly. Do not run the entire gstack suite
or paid benchmarks merely because it is installed.

Keep optional source and modeling dependencies outside the deterministic core.
For a requested environment setup, use an isolated environment and record exact
versions; routine research must remain usable without these additions. Add
fixture-based checks for new adapters and calculations using synthetic or
redistributable inputs. Check changed routing against realistic requests,
including unavailable tools and directly invoked focused skills. Run the
repository's relevant checks and summarize observed results and remaining limits.

Shipping, merging, deploying, publishing, tracker changes and schedules need
their own user-authorized scope. The existence of gstack `ship` or
`land-and-deploy` does not initiate those actions. A local plugin update can be
completed when the user's integration request covers it; report which host
copies were updated and whether a new session is needed to load them.
