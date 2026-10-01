---
concept_id: "pac-learning"
title: "PAC Learning & Generalization Bounds"
origin: "Leslie Valiant, 1984 ('A theory of the learnable')"
field: "Learning Theory"
modern_adaptation: "Harness Evolution as Learning (theory)"
source_url: "https://en.wikipedia.org/wiki/Probably_approximately_correct_learning"
relevance: 4
---

## One line
PAC learning gives a mathematical framework for asking: *how many training examples do I need before a learned hypothesis is, with high probability, approximately correct?*

## The problem
Before Valiant, learning was a zoo of algorithms with no common way to say what was *learnable*. A learner could fit training data perfectly and still fail in the real world, and there was no rigorous language for separating "the data was insufficient" from "the algorithm is broken" from "the hypothesis class can't express the truth." PAC learning made these distinctions quantitative: it defines learnability as the existence of an algorithm that, given enough samples, outputs a hypothesis that is probably (probability ≥ 1 − δ) approximately correct (error ≤ ε).

## How it works
The framework has four ingredients:

- A **hypothesis class** H (e.g. linear classifiers, a fixed set of harness designs).
- An unknown target concept and an unknown data distribution D.
- An algorithm that receives m i.i.d. samples from D.
- Two knobs: **accuracy** ε (how much error we tolerate) and **confidence** δ (how much risk of a bad sample we tolerate).

A class H is *PAC-learnable* if some algorithm, for every ε, δ, finds h ∈ H with true error ≤ ε with probability ≥ 1 − δ, using a number of samples m that grows polynomially in 1/ε and 1/δ.

The core bound, for a finite hypothesis class H and a *consistent* learner (one that fits all training data): with probability ≥ 1 − δ,

    true error(h) ≤ (log|H| + log(1/δ)) / m

In words: generalization error shrinks with more data (1/m) but grows with the log of the hypothesis class size — a bigger search space demands more samples. For infinite classes, the right measure of capacity is the **VC dimension** (Vapnik and Chervonenkis, 1971), and the agnostic bound replaces log|H| with VC(H), paying a 1/ε² rate instead of 1/ε.

## Key results
- **Valiant (1984):** the PAC model itself; showed that simple classes (conjunctions, k-CNF, decision lists) are efficiently learnable.
- **Vapnik–Chervonenkis (1971):** VC dimension characterizes uniform convergence — finite VC dimension is necessary and sufficient for PAC learnability.
- **Occam bounds (Blumer et al., 1987):** the finite-class bound above, formalizing "compression implies generalization."

## How it maps to modern harness work
The 2026 paper *Harness Evolution as Learning* explicitly imports this vocabulary: it decomposes harness-evolution error into **approximation error** (the best harness in the fixed design class can't express the ideal), **generalization error** (the evolved harness overfits the development tasks), and **optimization error** (the search never found the good harness). The PAC mapping is direct: the "hypothesis class" is the set of harness structures the search can reach, the "samples" are the dev tasks used to select harnesses, and ε/δ are the performance-tolerance and confidence you want on unseen tasks. This immediately suggests questions no one in harness land asks rigorously: given a search space of size ~2^n harness variants, how many held-out tasks do you need before your winning harness is probably approximately good? If your dev set has 50 tasks and your harness search space is enormous, PAC says your "generalization" claim is vacuous — which is exactly the regime most recursive self-improvement work lives in today.

## Limits and open questions
PAC assumes a fixed hypothesis class and a fixed distribution, but harness evolution *changes* the class (new tools, new decompositions appear mid-search), breaking the standard analysis. Worse, real agent tasks are adversarial and non-stationary, not i.i.d. draws from D. An honest PAC-style bound for evolved harnesses would need to handle expanding hypothesis classes and distribution shift — the paper gestures at this but the full theory is unwritten. I'm also not confident any published harness benchmark has enough held-out tasks to make the bounds nontrivial.
