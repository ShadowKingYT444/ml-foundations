---
concept_id: "multi-armed-bandits"
title: "Multi-Armed Bandits: UCB & Thompson Sampling"
origin: "Thompson 1933; Lai & Robbins 1985; Auer, Cesa-Bianchi & Fischer 2002 (UCB1)"
field: "Reinforcement Learning"
modern_adaptation: "per-component search budgets (adaptive decomposition)"
source_url: "https://en.wikipedia.org/wiki/Multi-armed_bandit"
relevance: 5
---

## One line
When you must repeatedly choose between uncertain options, the optimal strategy isn't to always pick the current winner — it's to add an *exploration bonus* to each option proportional to your uncertainty about it, so under-tried options get their fair shot.

## The problem
The explore–exploit dilemma: a gambler facing slot machines with unknown payout rates must decide each round whether to pull the best-known lever (exploit) or try a poorly-understood one (explore). Pure exploitation locks onto the first lucky arm; pure exploration never cashes in. Robbins (1952) formalized the problem, and the right objective is *regret* — how much reward you lose versus an oracle that always pulled the best arm. The question is which simple rule achieves provably small regret.

## How it works
Two classical solutions. **UCB1** (Auer et al. 2002) keeps, for each arm `i`, the empirical mean reward `Qᵢ` after `nᵢ` pulls out of `t` total, and plays the arm maximizing `Qᵢ + √(2 ln t / nᵢ)`. The second term is the exploration bonus: it shrinks as the arm is tried more, and grows (slowly, via `ln t`) for arms left behind — so every arm is eventually tried, but good arms dominate. **Thompson sampling** (Thompson 1933, revived ~2010) is Bayesian: maintain a posterior over each arm's mean, sample one value from each posterior, and play the argmax. Uncertainty automatically becomes exploration because wide posteriors produce occasional high samples. Both achieve `O(√(KT log T))` or `O(log T)`-style regret: the gap to the oracle grows *sublinearly*, meaning per-round regret vanishes.

## Key results
Lai & Robbins (1985) proved the logarithmic regret lower bound — no strategy can do asymptotically better — and gave an asymptotically optimal rule. UCB1 (2002) gave a simple finite-time bound matching it up to constants. Thompson sampling's finite-time optimality was proven around 2012 (Agrawal & Goyal), and it remains the empirical champion in industry (ad placement, recommendation).

## How it maps to modern harness work
Adaptive decomposition is, at its core, a bandit problem: the agent discovers a decomposition of the harness into components, and each component is an *arm* competing for a finite search budget. The mapping:

- **Arms** → harness components (a tool definition, a prompt module, a workflow stage).
- **Pulling an arm** → spending search budget on that component (proposing and evaluating edits to it).
- **Reward** → measured improvement in end-to-end task success attributable to that component.
- **UCB's exploration bonus** → the reason to keep spending budget on a *failing* component rather than pouring everything into the already-working one: the failing component's uncertainty is high, and splitting it (adaptive decomposition's signature move) is exactly what a bandit algorithm does when an arm's variance refuses to shrink — it *refines the arm*.

Thompson sampling's view is arguably even closer to the user's mechanism: maintain a belief over each component's "improvability," sample, and allocate budget to the sampled winner. Fusion is the reverse operation — merging arms whose posteriors have collapsed to the same value — and the revert-to-monolith rule is the bandit deciding the decomposition itself was a bad model.

## Limits and open questions
Classical regret bounds assume *stationary* arms with independent rewards; harness components are neither — editing one component changes the reward distribution of others (non-stationarity), and "reward" is a noisy, expensive, hard-to-attribute rollout metric. Worse, adaptive decomposition changes the *set of arms* mid-game (split/fuse), which standard bandit theory doesn't cover. Open questions: is there a regret bound for bandits with splitting arms? Can component-level credit assignment be made clean enough that `Qᵢ` means something? And what's the right prior — should a brand-new component inherit optimism (try it!) or skepticism (prove it)?
