---
concept_id: "online-learning-regret"
title: "Online Learning & Regret Minimization"
origin: "Nick Littlestone & Manfred Warmuth (weighted majority, 1989–1994); Yoav Freund & Robert Schapire (Hedge, 1997)"
field: "Learning Theory"
modern_adaptation: "sequential harness revision with guarantees"
source_url: "https://en.wikipedia.org/wiki/Online_machine_learning"
relevance: 3
---

## One line
Online learning studies learners that see data one round at a time and must perform well *as they go* — measured by **regret**: how much worse they did than the best fixed strategy in hindsight.

## The problem
Classical learning assumes you get a dataset, train, then deploy. But many systems face a stream: a spam filter sees emails one by one, a portfolio allocator rebalances daily, and there's no "training phase" — every round counts. Worse, the data may be adversarial: assume nothing about the future, and still guarantee you won't do much worse than the best single strategy you *could* have committed to. Regret makes this precise. Over T rounds, if your algorithm accumulates total loss L_alg and the best fixed expert in hindsight accumulates L_best, your **regret** is L_alg − L_best. An algorithm is *no-regret* if regret grows sublinearly in T — i.e. your per-round disadvantage versus the best expert vanishes as T grows.

## How it works
The canonical algorithm is **Hedge** (a.k.a. exponential weights / multiplicative weights). You maintain a weight wᵢ for each of N experts (candidate strategies). Each round: play the weighted mixture of experts, observe losses ℓᵢ, and update weights multiplicatively:

    wᵢ ← wᵢ · exp(−η · ℓᵢ)

Experts that keep losing get exponentially downweighted; η controls how aggressively you shift. The guarantee: with η tuned to √(log N / T), total regret is O(√(T log N)) — sublinear, so per-round regret → 0, *with no assumptions about the loss sequence at all*, even adversarial ones. The log N dependence is the magic: you can compete with exponentially many experts at the cost of only logarithmic extra regret.

## Key results
- **Littlestone & Warmuth (1989–1994):** the weighted majority algorithm; the first clean mistake-bound and regret analyses.
- **Freund & Schapire (1997):** Hedge and the decision-theoretic framework — regret O(√(T log N)).
- **Auer et al. (2002):** EXP3 — no-regret learning with bandit feedback, the foundation of adversarial bandits.

## How it maps to modern harness work
Iterative self-improvement is an online learning problem wearing different clothes: each "round" is a harness revision, each "expert" is a candidate harness design (or a mutation operator), and the "loss" is the harness's measured error on that round's tasks. The regret framing asks the question nobody in harness land asks: *is my revision process doing almost as well as the best fixed harness I could have picked in hindsight?* If your search has linear regret — it keeps proposing bad revisions forever — no amount of compute saves you. Hedge suggests a concrete design: keep a population of harness variants with weights, sample revisions proportional to weight, and downweight variants exponentially by their measured loss. That's a principled alternative to the greedy keep-or-reject loops (SelfSearch, VACE) that dominate today: greedy search has no regret guarantees and can get stuck; exponential weights provably can't do much worse than the best variant in the pool. The bandit variant (EXP3) is the honest model, since you only ever evaluate the harness you actually tried.

## Limits and open questions
The guarantees need a *fixed* expert set and bounded losses — but harness revision *invents* new experts (new components, new tools) every round, which breaks the standard analysis; the "sleeping experts" extensions only partly cover this. Losses in harness eval are also noisy and expensive, and regret bounds assume you observe the loss every round — with LLM-eval noise, you'd need the high-probability versions of these bounds, which are looser. The deepest gap: regret compares you to the best *fixed* expert in hindsight, but self-improvement's whole point is that the best strategy *changes* as the harness evolves — the right comparator is a moving target, and the theory for that ("dynamic regret") is much less developed. Still, even as an aspiration, no-regret is a sharper design goal than "the number went up this round."