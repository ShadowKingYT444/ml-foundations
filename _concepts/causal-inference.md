---
concept_id: "causal-inference"
title: "Causal Inference & Counterfactuals"
origin: "Donald Rubin (potential outcomes, 1974) and Judea Pearl (do-calculus, 1995)"
field: "Statistics"
modern_adaptation: "diagnosing which harness component caused a failure"
source_url: "https://en.wikipedia.org/wiki/Causal_inference"
relevance: 3
---

## One line
Causal inference is the toolkit for distinguishing "X and Y move together" from "changing X *would change* Y" — using counterfactuals and interventions rather than raw correlation.

## The problem
Correlation lies constantly. Hospitals that treat more patients have higher death rates — because sicker patients go to bigger hospitals, not because treatment kills. Standard statistics answers "what is P(Y | X)?" (given we *observe* X), but decisions need "what is P(Y | do(X))?" — what happens if we *intervene* and set X. Pearl's ladder of causation makes this precise: association (seeing), intervention (doing), and counterfactuals (imagining what would have happened) are three distinct levels, and no amount of level-1 data answers level-2 or level-3 questions without extra assumptions.

## How it works
Two frameworks dominate. **Rubin's potential-outcomes model (1974):** each unit has two potential outcomes, Y(1) if treated and Y(0) if not; the causal effect is Y(1) − Y(0). The fundamental problem: you only ever observe one of them — the other is the *counterfactual*. Randomized experiments solve this by making treatment independent of the potential outcomes, so group averages estimate the average causal effect. **Pearl's structural causal models (1995):** represent assumptions as a directed acyclic graph, define interventions via the *do-operator* do(X = x) (surgically set X, severing its incoming edges), and derive rules — the *backdoor criterion*, the *front-door criterion* — for when a causal effect is identifiable from observational data. The slogan: correlation needs no model, causation always does; the graph is where your assumptions live, in public, where they can be attacked.

## Key results
- **Rubin (1974, 1978):** the potential-outcomes framework and the "fundamental problem of causal inference."
- **Pearl (1995):** the do-calculus — complete rules for identifying causal effects from graphs.
- **Hernán & Robins and the applied literature (2000s):** causal inference becomes standard practice in epidemiology, economics (Angrist & Pischke), and tech experimentation.

## How it maps to modern harness work
Harness diagnosis is a causal question wearing a debugging costume. A task failed and the trace shows component C did something odd — but did C *cause* the failure, or would the task have failed anyway (an unobserved confounder, like a bad prompt upstream)? Video-RSI's key trick is exactly counterfactual reasoning: rather than just revising from the trace, the agent *revisits the training videos* to test competing hypotheses about *why* the failure happened — i.e. it gathers the interventional evidence needed to move from "the harness correlated with failure" to "this design choice caused it." The general template for harness work: ablations and component swaps are *interventions* (do(component = variant)), golden-trace comparisons are attempts at the counterfactual ("what would the outcome have been with the correct component?"), and the do-operator is the right mental model for a disciplined "change one thing and re-run" methodology instead of the usual change-five-things-and-pray loop.

## Limits and open questions
Real causal inference leans on assumptions — no unmeasured confounding, correct graph structure — that are nearly impossible to verify inside a stochastic LLM pipeline where every component is a black box and "the same input" never produces the same output. Counterfactuals for LLM agents are especially slippery: re-running with one component swapped doesn't hold everything else fixed, because downstream LLM calls are sampled, not deterministic. And the biggest gap: nobody has a causal *graph* of a modern agent harness — we don't even know which components influence which outcomes, which is precisely the knowledge causal methods require as input. So the honest version of this idea for harness work is a discipline (intervene cleanly, distrust correlations, demand counterfactual evidence before "fixing" a component), not a theorem you can apply off the shelf.
