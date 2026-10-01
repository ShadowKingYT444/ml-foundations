---
concept_id: "boosting"
title: "Boosting (AdaBoost / Gradient Boosting)"
origin: "Freund & Schapire (1997)"
field: "Learning Theory"
modern_adaptation: "component fusion in adaptive decomposition"
source_url: "https://en.wikipedia.org/wiki/Boosting_(machine_learning)"
relevance: 4
---

## One line
Build a strong predictor by sequentially training weak learners on reweighted data that emphasizes the current ensemble's mistakes, then combining them by weighted vote.

## The problem
It's far easier to find many rules that are slightly better than chance than to find one great rule. Schapire (1990) asked whether weak learnability could be converted into strong learnability — and the practical question was how to combine the weak rules without them just echoing each other. The harness analog: it's easier to evolve components that each handle one slice of the task space than to evolve one monolithic harness that handles everything.

## How it works
AdaBoost: start with uniform weights `D₁(i) = 1/m`. At round `t`, train a weak learner `h_t` on the weighted data, measure its weighted error `ε_t`, set its vote weight `α_t = ½·ln((1−ε_t)/ε_t)`, and reweight: `D_{t+1}(i) ∝ D_t(i)·exp(−α_t·y_i·h_t(x_i))` — misclassified points get exponentially upweighted, correctly classified ones downweighted. Final classifier: `H(x) = sign(Σ_t α_t·h_t(x))`. Friedman, Hastie & Tibshirani (2000) showed this is coordinate descent on exponential loss `Σ exp(−y·H(x))`; Friedman (2001) generalized it to gradient boosting, where each new learner fits the *residuals* (negative gradient) of the ensemble — the idea XGBoost (Chen & Guestrin, 2016) industrialized for tabular data.

## Key results
Schapire (1990) proved weak learnability implies strong learnability. Freund & Schapire (1997) gave the practical AdaBoost with the training-error bound `Π_t 2√(ε_t(1−ε_t))`: error drops exponentially fast as long as each weak learner beats chance. The work earned the 2003 Gödel Prize, and gradient boosting dominated tabular ML competitions for two decades. The core theoretical insight: reweighting forces *diversity* — each new learner must succeed where the ensemble currently fails.

## How it maps to modern harness work
Fusing working harness components is the structural analog of boosting. Each component is a "weak learner" — competent on some subproblem slice, useless elsewhere — and the fused harness is the ensemble. The reweighting mechanism maps to *budget allocation*: components that fail get more search budget (split and re-evolved), like misclassified points getting upweighted; components that work get fused and their budgets consolidated. The diversity requirement is the crux, and it has a direct empirical echo: the Scaffold paper (2609.34924) warns that fusion/voting only helps with *cross-family* diversity — a majority of same-family workers failed 23 of 55 tasks, so voting among near-identical agents adds nothing. Boosting theory says the same thing formally: if the weak learners err identically, the exponential-loss bound collapses and the ensemble is no better than its parts.

## Limits and open questions
Boosting overfits noisy labels — late rounds fit noise, not signal — and the harness analog is fusing components around spurious task quirks, producing a fused harness that is brittle outside the training tasks. Worse, boosting theory assumes a *fixed* weak-learner class while only the data weights change; in adaptive decomposition both the components *and* the decomposition change, which breaks the clean analysis. The open question is a fusion rule with boosting-style guarantees for *evolving* components: under what diversity condition does fusing two independently-evolved harness components provably help? No such theorem exists yet, and writing one is a genuine research target — it would be the theoretical backbone of the fuse step in adaptive decomposition.
