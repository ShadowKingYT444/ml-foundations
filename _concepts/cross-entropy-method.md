---
concept_id: "cross-entropy-method"
title: "The Cross-Entropy Method"
origin: "Reuven Rubinstein (1997)"
field: "Optimization"
modern_adaptation: "distribution-based harness design search"
source_url: "https://en.wikipedia.org/wiki/Cross-entropy_method"
relevance: 3
---

## One line
CEM keeps a parametric distribution over candidate designs, samples from it, keeps the elite samples, and refits the distribution to those elites — iterating until the distribution concentrates on good designs.

## The problem
Black-box optimization with no gradients and discrete choices: random search wastes samples on dead regions, while greedy hill-climbing gets stuck. The question is how to use the *history* of evaluated candidates to focus future sampling without assuming differentiability — which is exactly the situation in harness design, where the choices (which tools, which decomposition, which prompts) are discrete and the objective is only observable by running the agent.

## How it works
Initialize parameters `θ₀` of a distribution family (e.g., mean and covariance of a Gaussian, or per-choice probabilities of a categorical). Then repeat: **sample** `N` candidates `xᵢ ~ p_θ`; **score** each with the black-box objective `f(xᵢ)`; **select** the top `ρ`-fraction as elites; **refit** `θ ← argmax_θ Σ_elites log p_θ(xᵢ)`, i.e., maximum-likelihood on the elites. The refit step minimizes the cross-entropy between `p_θ` and the empirical elite distribution — hence the name. Intuition: repeatedly ask "what do the winners look like?" and become more like them. Variance shrinkage is often added to force convergence. Over iterations the distribution collapses onto a high-performing region.

## Key results
Introduced by Rubinstein (1997) for rare-event simulation, then generalized to optimization; it became a standard derivative-free optimizer for continuous control and planning. A prominent modern use: PETS (Chua et al., 2018) uses CEM inside model-predictive control to plan action sequences with learned dynamics models. Convergence results exist under smoothness assumptions, though in practice the method is valued for simplicity and robustness rather than tight theory.

## How it maps to modern harness work
Distribution-based harness design search is CEM with harnesses as the samples: maintain a distribution over harness *patterns* (which components to include, which tools to expose, what budget each gets), sample concrete harnesses, evaluate them on tasks, keep the winners, and refit the distribution toward them. The **elite-refit loop** is the mechanism for "iteratively concentrating search around winning harness patterns": early rounds explore broadly, later rounds tighten around architectures that pass the gates. This is the natural alternative to gradient-style prompt optimization (TextGrad) when the search space is discrete structure rather than continuous text. The analogs are direct: samples = candidate harness variants, the objective `f` = task success rate minus cost, and the refit distribution = a learned prior over good harness structure. PluginRSI's bandit over its 75-plugin library is spiritually adjacent — keep what works, drop what doesn't — but a full CEM would additionally *refit a generative model* of good configurations instead of just tracking per-arm means.

## Limits and open questions
The parametric family may not contain any good design — CEM can only concentrate, not invent outside its family (model bias). It is sample-hungry in high dimensions, and a harness has many discrete choices; elites can also collapse diversity prematurely, converging to a local optimum while a better architecture sits one mutation away. The open question is representational: what parametric family is expressive enough for *program-like* harness structures yet sample-efficient enough to refit from a few dozen expensive evaluations? Mixture models over component libraries are one direction; learned generative priors over code are another, essentially untested at this scale.
