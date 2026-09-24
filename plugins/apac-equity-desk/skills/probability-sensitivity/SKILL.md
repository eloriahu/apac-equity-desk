---
name: probability-sensitivity
description: Stress merger completion probability, break value and settlement timing using explicit costed scenarios. Use for probability sensitivity, break-even probability, downside grids or testing assumptions; do not infer true probabilities from the spread.
---

# Probability Sensitivity

Read [research standards](../../references/event-driven/research-standards.md),
[toolkit contracts and examples](../../references/event-driven/toolkit.md), and
[market data integrations](../../references/integrations.md).

1. Assemble a verified cash or fixed-ratio merger_arb/v1 input with exactly one close and one break scenario. Review consideration, both legs, dividends, costs, financing and the capital denominator before using it. Read calculation conventions.
2. Set probability, independent break-price and close-day grids from the user's assumptions or clearly labeled research ranges. Cite evidence supporting the range; never manufacture a calibrated model from a current quote. Show the baseline before changes.
3. Run the sensitivity helper. Close probability and its complement sum to one. Close timing changes financing/borrow costs; break timing and acquirer exits remain fixed at the declared baseline. To stress those variables, run separately labeled base inputs.
4. Explain positive/negative EV regions, cost-adjusted break-even thresholds and which input drives the result. Thresholds outside [0,1] remain visible. The threshold is an algebraic indifference point, not a completion forecast.
5. Do not annualize EV using average scenario duration. For multiple closing states, recuts or dependent milestones, construct explicit joint scenarios with merger-arb or deal-models rather than silently collapsing outcomes. Output the grid, assumptions, strongest contrary evidence and next milestone that could change them.

Use the `sensitivity` example and helper described in the toolkit. Preserve the input
and output beside the source pack. Run source-verifier and desk-editor for the
reader-facing research draft; retain `DRAFT — HUMAN APPROVAL REQUIRED`.
