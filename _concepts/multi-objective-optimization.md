---
concept_id: "multi-objective-optimization"
title: "Multi-Objective Optimization & Pareto Fronts"
origin: "Vilfredo Pareto (1906); NSGA-II by Deb et al. (2002)"
field: "Optimization"
modern_adaptation: "MoMHa"
source_url: "https://en.wikipedia.org/wiki/Multi-objective_optimization"
relevance: 4
---

## One line
When objectives conflict — accuracy versus cost versus safety — no single optimum exists; the right object of study is the Pareto front of non-dominated solutions.

## The problem
Single-metric optimization ("maximize accuracy") produces harnesses that are unsafe or unaffordable, and the damage is invisible to the metric. The common patch, scalarization (`0.7·accuracy − 0.3·cost`), hides the trade-off inside arbitrary weights — and worse, a weighted sum can *never* reach the non-convex regions of the trade-off surface, no matter what weights you pick. The question is how to search honestly when the answer is a set of trade-offs, not a point.

## How it works
Solution `x` **dominates** `y` if it is at least as good on every objective and strictly better on at least one. The **Pareto front** is the set of non-dominated solutions: nobody on the front can be improved on one objective without sacrificing another. True multi-objective algorithms return the whole front so a decision-maker picks the trade-off afterward. NSGA-II (Deb et al., 2002) does this with fast non-dominated sorting plus a crowding-distance term that keeps the front diverse instead of collapsing to one region. Front quality is measured by the hypervolume indicator (Zitzler, 1999): the volume of objective space dominated by the front.

## Key results
Pareto formalized the concept in his 1906 *Manuale*; the modern computational field grew from evolutionary multi-objective work in the 1990s. NSGA-II (Deb, Pratap, Agarwal & Meyarivan, *IEEE Transactions on Evolutionary Computation*, 2002) became the reference algorithm — one of the most cited papers in optimization — because elitism plus diversity maintenance made Pareto search practical. The enduring lesson: when objectives genuinely conflict, *the front is the answer*, and any single number is a political choice disguised as a technical one.

## How it maps to modern harness work
MoMHa (2609.30967) is the first harness optimizer to treat accuracy, safety, and token cost as *joint* first-class objectives — the direct MOO move against single-objective harness search (GEPA and TextGrad variants that optimize one metric). Its novelty is exactly the Pareto framing: instead of "best accuracy at any cost," it returns harnesses along the accuracy–safety–cost front, so you can see what a point of accuracy costs in dollars and in risk. Pareto dominance is the right selection operator for harness evolution in general: a harness that is safer *and* cheaper *and* more accurate dominates, full stop; anything else is a trade-off choice, not an objective fact. Single-metric harness evaluation is misleading precisely because it collapses the front to one point — usually the expensive, brittle corner — and then declares victory.

## Limits and open questions
MOO is sample-hungry: estimating a front needs many more evaluations than optimizing one scalar, and each harness evaluation costs real inference dollars. NSGA-II-style algorithms were designed for cheap function evaluations; in harness land that assumption is badly false. There is also the curse of dimensionality of objectives: with many objectives, almost everything is non-dominated ("dominance resistance") and selection pressure vanishes. The open questions are practical: can we estimate the front from few rollouts, e.g., by predicting all objectives from shared trajectory features instead of measuring each? And which objectives even belong in the front — is "maintainability of the harness" or "robustness to tool-API drift" a fourth objective nobody currently measures? Until those are on the front, optimizers will keep sacrificing them silently.
