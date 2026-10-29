---
name: statistical-research
description: Test APAC equity research hypotheses with supplied or accessible historical data, event studies, regressions or Bayesian models. Use for factor-adjusted returns, flow predictiveness, significance tests and calibrated outcome estimates; ordinary price-move explanations and deterministic deal sensitivity remain their existing desk workflows.
---

# Statistical Research

Read `../../references/research-addons.md` and
`../../references/integrations.md`. Use this as the lead for an empirical
question, or bounded support to an existing historical-testing or
probability-sensitivity workflow. Keep one owner of the final research answer.

1. Define the question, outcome, observational unit, universe, horizon and
   decision cutoff. Separate description, prediction and causal inference.
   Fix the primary comparison, benchmark and validation design before examining
   results. Record exploratory variants as exploratory.
2. Inspect the data and lineage. Align local sessions, release/availability
   times, currencies, return horizons, corporate actions and total-return versus
   price-return basis. Preserve missingness and exclusions. Include failed,
   withdrawn and delisted observations where relevant. Future labels, revised
   data and overlapping outcomes must not leak into earlier predictors.
3. Read only the installed specialist skill needed for the method:
   - `database-lookup` for a named public dataset or macro series;
   - `statistical-analysis` for test selection, assumptions, effect sizes and
     uncertainty;
   - `statsmodels` for regression or time-series estimation and diagnostics;
   - `pymc` for an explicitly justified Bayesian model, priors and partial pooling.
   Choose the simplest adequate method. Check runtime availability before
   promising execution; instructions being installed is not a working library.
4. Preserve inputs, transformations, code, package versions and random seeds
   beside the local research artifact. For repeated firms, markets, clustered
   event dates or overlapping returns, account for dependence in inference and
   train/test design. Use chronological validation for prediction and keep the
   final holdout untouched by selection. Report all tested variants and any
   multiple-comparison adjustment.
5. Inspect diagnostics before interpreting estimates. Regressions need residual,
   dependence and model-fit checks. Bayesian work needs justified priors, prior
   sensitivity, sampling/convergence and posterior-predictive checks. Prediction
   needs out-of-sample evaluation and calibration where applicable. Retain weak,
   null and failed results; regression coefficients alone do not prove a catalyst
   caused a move.
6. Return the sample and cutoff, method, effect size, appropriate confidence or
   credible interval, diagnostics, validation result, economic mechanism,
   counterevidence and limits. An unsupported or inadequate sample yields a
   descriptive result or analysis plan, not a fitted confidence claim. Run
   source-verifier and desk-editor on the research draft and retain
   `DRAFT — HUMAN APPROVAL REQUIRED`.

For deal completion models, use comparable deals and point-in-time features;
distinguish model estimates, analyst scenario probabilities and break-even
thresholds. A small or biased completed-deal sample cannot establish a calibrated
completion probability. Pass only supported, labeled estimates to the existing
scenario helper; preserve the original assumption-driven sensitivity grid.

For portfolio replay, `../historical-testing/SKILL.md` continues to own execution,
capital and settlement mechanics. Statistical significance is neither a simulated
tradable return nor evidence that costs, liquidity and borrow are attainable.
