---
concept_id: "credit-assignment"
title: "The Credit Assignment Problem"
origin: "Marvin Minsky, 1961 ('Steps toward artificial intelligence')"
field: "Reinforcement Learning"
modern_adaptation: "per-component evaluation in adaptive decomposition"
source_url: "https://en.wikipedia.org/wiki/Credit_assignment_problem"
relevance: 5
---

## One line
When a system succeeds or fails, credit assignment is the problem of deciding *which* internal decision — which action, which component, which weight — deserves the praise or blame.

## The problem
Minsky named it in 1961: in any system with many interacting parts, the outcome tells you almost nothing about which part caused it. A chess program loses — was the opening book bad, the evaluation function misweighted, or was one search-depth parameter off? If you can't attribute outcomes to components, you can't improve components; you're reduced to tweaking the whole thing and praying. The problem splits two ways: **temporal** credit assignment (which *past* action in a long sequence caused the final reward?) and **structural** credit assignment (which *part* of the system caused the outcome?). Reinforcement learning spent decades on the temporal side — TD learning, eligibility traces, advantage estimation — while the structural side was mostly handled by backprop (differentiable systems) or ignored (discrete systems).

## How it works
The classic formalization comes from RL. An agent takes actions a₁…aₜ and gets reward R at the end; temporal credit assignment asks how much each aᵢ contributed. The core tool is the *value function*: V(s) estimates expected future reward from state s, so the *advantage* A(s,a) = Q(s,a) − V(s) measures how much better this action was than average — a principled per-action credit signal. For structural credit assignment in neural networks, backpropagation solves it exactly for differentiable architectures: the gradient ∂loss/∂wᵢ tells each weight its marginal contribution. But for *discrete, modular* systems — a planner calling a retriever calling a code executor — there is no gradient. You're stuck with ablations, counterfactual rollouts, or reward shaping, all of which are expensive and confounded by interactions between parts.

## Key results
- **Minsky (1961):** named the problem; framed learning as needing per-component feedback.
- **Sutton (1988):** TD(λ) learning — a unified way to propagate credit backward through time with eligibility traces.
- **Williams (1992):** REINFORCE — the policy-gradient estimator, which assigns credit via likelihood-ratio weighting of sampled trajectories (unbiased but famously high-variance).
- **Schulman et al. (2015):** generalized advantage estimation — practical variance reduction for temporal credit.

## How it maps to modern harness work
Adaptive decomposition lives or dies on **structural credit assignment at the component level**. The split/fuse loop needs to answer: *which component caused this failure?* Today's harness optimizers mostly evaluate the *whole harness* on dev tasks and keep or reject entire revisions — that's no credit assignment at all, and it confounds everything: a genuinely improved retriever can be masked by a bad prompt template upstream, and a harmful change can ride along with a lucky one. The RL analogs transfer concretely: the harness outcome is the terminal reward; each component's contribution is the advantage to estimate. Practical versions include per-component ablations (remove/replace component, measure delta — the harness equivalent of a counterfactual rollout), blame-weighted search budgets (spend more mutations on components with high estimated disadvantage), and fault-localization traces (which component first diverged from a golden trace). SelfSearch's whole-repo edits and VACE's whole-harness gating are both held back precisely because their credit signal is whole-system.

## Limits and open questions
Component interactions make marginal credit ill-defined: component A looks bad only because component B feeds it malformed input — blame A and you "fix" the wrong thing. This is the classic *blame assignment* pathology, and RL never solved it for non-differentiable modular systems either. Counterfactual ablation is O(n) rollouts per revision (n components), which is brutal when each rollout costs LLM calls. The open question: can we learn a cheap *proxy* credit model (e.g. a judge model predicting component-level blame from traces) that correlates well enough with true ablation deltas to steer search? If yes, that unlocks per-component budgets; if no, adaptive decomposition is stuck with whole-harness evaluation and inherits all its confounding.
