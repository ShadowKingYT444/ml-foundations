---
concept_id: "bayesian-optimization"
title: "Bayesian Optimization"
origin: "Mockus 1970s; Jones, Schonlau & Welch 1998 (EGO)"
field: "Optimization"
modern_adaptation: "surrogate-guided harness search (GEPA-style proposers)"
source_url: "https://en.wikipedia.org/wiki/Bayesian_optimization"
relevance: 4
---

## One line
When evaluating the objective is expensive, fit a cheap probabilistic *surrogate* to past evaluations and use an *acquisition function* to decide where to sample next — balancing exploration of uncertain regions against exploitation of known-good ones.

## The problem
Grid search and random search waste the budget on hopeless configurations when each evaluation costs hours (hyperparameter tuning, hardware design, A/B tests on live traffic). The classical question: how do you choose the *next* evaluation point using everything you've learned, when you can't afford many? Bayesian optimization's answer is to never touch the expensive function directly for decisions — instead maintain a model of *what you believe* about it, including uncertainty, and optimize that instead.

## How it works
A Gaussian process (GP) prior is placed over the objective `f`: after observing `(xᵢ, f(xᵢ))`, the posterior gives a mean `μ(x)` and variance `σ²(x)` at every candidate point — a prediction *plus* calibrated uncertainty. An *acquisition function* then scores each candidate: Expected Improvement `EI(x) = E[max(f(x) − f_best, 0)]` rewards points likely to beat the incumbent, while Upper Confidence Bound `UCB(x) = μ(x) + βσ(x)` adds an explicit exploration bonus `βσ`. Maximize the acquisition function (cheap), evaluate the real function there (expensive), update the GP, repeat. The Jones–Schonlau–Welch (1998) "Efficient Global Optimization" paper made EI+GP the standard recipe; Srinivas et al. (2010) later proved sublinear regret bounds for GP-UCB under smoothness assumptions.

## Key results
Landmark results: EGO (1998) brought BO into engineering practice; GP-UCB regret bounds (2010) gave the first rigorous explore-exploit guarantees; and BO became the backbone of hyperparameter tuning (Spearmint, 2012) and neural architecture search warm-ups. Empirically, BO routinely beats random search by an order of magnitude in sample efficiency on expensive black-box functions with dozens of dimensions — and fails gracefully beyond that, which is why scaling BO is its own research field.

## How it maps to modern harness work
In harness optimization (e.g. GEPA-style proposers), the "expensive evaluation" is a full agent rollout on a benchmark suite, and the classical BO loop is adapted with LLMs filling both roles:

- **Surrogate** → often an *LLM judge* or learned reward model that predicts a harness candidate's quality without running it, or even just the proposer's implicit prior over "what good harnesses look like." Unlike a GP, it provides no calibrated `σ(x)` — uncertainty is vibes, not variance.
- **Acquisition function** → the proposal strategy: generating candidates that are both promising (mutations of the current best) and diverse (exploring unexplored structural families). Some systems make this explicit by asking the LLM to propose candidates *different* from past failures.
- **Objective** → task success rate / cost on the dev set; the incumbent is the best harness found so far.

What changed: the surrogate went from a mathematically principled posterior to a language model's gut feeling, and the search space went from a continuous box to *program space*. The discipline BO offers — *quantified* uncertainty driving *principled* exploration — is exactly what current LLM-driven search lacks, which is why some of the strongest recent systems reintroduce it (e.g. explicit coverage/vote rules deciding which data a branch "owns").

## Limits and open questions
GP surrogates assume smooth, low-dimensional objectives; harness space is discrete, high-dimensional, and violently non-smooth (one token can flip behavior). LLM-judge surrogates hallucinate confidence and correlate poorly with real rollout outcomes on out-of-distribution harness structures. Open questions: can we build a *calibrated* surrogate for program space — e.g. train a small model on (harness, score) pairs with proper uncertainty? And can acquisition functions be expressed in language ("propose the candidate that maximizes information gain about the failure boundary") and actually honored by the proposer?
