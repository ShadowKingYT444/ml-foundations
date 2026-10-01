---
concept_id: "successive-halving"
title: "Successive Halving & Hyperband"
origin: "Jamieson & Talwalkar, AISTATS 2016"
field: "Search"
modern_adaptation: "budget allocation across harness candidates"
source_url: "https://arxiv.org/abs/1502.07943"
relevance: 4
---

## One line
Successive halving spends a fixed evaluation budget efficiently by giving many candidates a little budget, killing the worst, and repeatedly doubling down on survivors — Hyperband extends it by hedging over how many candidates to start with.

## The problem
Model selection is expensive: you have `n` candidate configurations and each full evaluation costs a lot. Random search wastes most of its budget fully evaluating losers. The question was how to *identify the best arm* with a fixed total budget — spending just enough on each candidate to tell whether it deserves more, and formalizing the tradeoff between trying many candidates cheaply versus few candidates thoroughly.

## How it works
**Successive halving** runs in rounds with a halving factor `η` (typically 3). Start with `n` candidates and a small per-candidate budget `r`. Evaluate all, keep the top `n/η`, and multiply their budget by `η`. Repeat until one candidate remains. The total budget is fixed, and the schedule is geometric: each round spends the same total as the last, concentrated on fewer, better candidates. Intuition: bad configurations reveal themselves quickly — you don't need a full training run to know a learning rate is hopeless — so early rounds are cheap filters and late rounds are expensive confirmations. **Hyperband** (Li, Jamieson et al., 2016) observes that the algorithm is sensitive to the initial choice of `(n, r)`: many-cheap vs few-expensive is itself a bet. So it runs multiple *brackets*, each a successive-halving run with a different starting tradeoff, hedging across them. Jamieson & Talwalkar (2016, "Non-stochastic Best Arm Identification and Hyperparameter Optimization") proved the halving schedule is near-optimal for identifying the best arm under a budget; Hyperband showed order-of-magnitude speedups over random search on real hyperparameter problems.

## Key results
The 2016 paper gave the first rigorous analysis: successive halving identifies an ε-optimal configuration with exponentially less budget than uniform allocation, under mild assumptions about how performance improves with budget. Hyperband's empirical results (2016–2018) made it the default budget-aware tuner in AutoML — it demonstrated that *how you allocate evaluation budget matters more than how you sample candidates*, a finding that reshaped hyperparameter optimization practice.

## How it maps to modern harness work
This is the exact machinery behind **independent search budgets** — the core of adaptive decomposition. The analogs: **arms** → candidate harness components or per-subproblem strategies; **budget** → evaluation rollouts, LLM calls, wall-clock time; **halving rounds** → evaluate each component on a few probe tasks, kill the ones that fail, double the budget of survivors. When a harness system gives each subproblem its own search budget and starves failing components while feeding working ones, it is running successive halving over the decomposition. The Hyperband lesson also transfers: the *initial* split of budget across components is itself a bet, so a principled system should hedge — try several budget-allocation brackets rather than committing to one decomposition up front. Practically, this is why "failing components recursively split" needs a halving rule: a split is only worth it if the child components can be evaluated cheaply enough to survive early rounds, and components that cannot beat their siblings on few probes should be fused back or killed rather than given full evaluations.

## Limits and open questions
Successive halving assumes performance at small budget *predicts* performance at large budget — in harness work this often fails: a component that looks bad on 3 probe tasks may be the one that needed 30 to show its structure (early-stopping bias). It also assumes arms are independent, but harness components interact — killing a "loser" can remove the component its sibling depended on. Open questions: how to design *predictive* cheap evaluations (what is the harness analog of a learning curve?); how to handle non-transitive component interactions in the kill rule; and whether the halving factor should itself adapt (failing fast when signal is strong, persisting when it is noisy).
