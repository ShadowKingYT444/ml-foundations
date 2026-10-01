---
concept_id: "population-based-training"
title: "Population-Based Training"
origin: "Jaderberg et al., DeepMind, 2017"
field: "Optimization"
modern_adaptation: "co-evolving harnesses and hyperparameters"
source_url: "https://arxiv.org/abs/1711.09846"
relevance: 4
---

## One line
PBT trains a *population* of models in parallel and periodically lets underperformers copy the weights and hyperparameters of winners (exploit) and then randomly perturb them (explore) — evolution of hyperparameters wrapped around gradient-based learning.

## The problem
Hyperparameter tuning was a painful outer loop: grid search, random search, or Bayesian optimization all required training many models *from scratch* to completion, and the best hyperparameters often change *during* training (a learning rate that is good at step 1k is not the one you want at step 100k). The question was whether you could adapt hyperparameters *online*, mid-training, without restarts — and whether evolution and gradient descent could be combined instead of treated as rival paradigms.

## How it works
Maintain a population of agents, each with its own weights `θ` and hyperparameters `h` (learning rate, entropy bonus, etc.). Everyone trains asynchronously on the real objective. Periodically, each member is evaluated; the protocol is **exploit then explore**: if a member is underperforming, it *copies* the weights and hyperparameters of a randomly selected better member (exploit), then *perturbs* the hyperparameters — e.g. multiply the learning rate by 1.2 or 0.8 — while keeping the copied weights (explore). Intuition: weights carry the accumulated knowledge, so copying them avoids restarting from scratch; hyperparameters carry the *strategy*, so perturbing them lets the population discover schedules no human would hand-design. Because evaluation and copying are asynchronous, there is no synchronization barrier — the population is a continuously evolving ecosystem. Jaderberg et al. (arXiv:1711.09846, 2017) showed PBT beating hand-tuned baselines on Atari, DeepMind Lab, and machine translation, often discovering non-monotonic learning-rate schedules.

## Key results
The 2017 paper's headline was practical: PBT matched or exceeded heavily hand-tuned results while removing the human from the hyperparameter loop, and it found hyperparameter *schedules* (not just fixed values) that improved final performance. Conceptually it bridged two communities — it is gradient descent inside, evolution outside — and inspired a family of population methods (PBT variants, Population-Based Bandits, and later uses in RLHF and LLM training runs).

## How it maps to modern harness work
Harness evolution is PBT with the population members being *harness candidates* instead of neural nets. The analogs: **weights** → the current harness structure/code (the accumulated knowledge worth preserving); **hyperparameters** → everything around it — search budgets, mutation rates, which components to evolve; **exploit** → periodically kill losing harness lineages and seed new ones from winners (as in mixture-of-branches methods that keep the best branch heads); **explore** → perturb the copied harness (mutate its structure, split a component, change a budget). This is the machinery behind co-evolutionary systems: VACE's alternating model/harness updates and SafeCoEvo's two-timescale populations are both exploit-and-explore ecosystems, just with structured populations rather than flat ones. The deepest PBT lesson for harness work is *never restart from scratch*: the winning move is copying the winner's state and perturbing the strategy, which is exactly why versioned harness lineages with rollback (Self-Evolving Coding Agents) outperform generate-from-scratch search.

## Limits and open questions
PBT's exploit step assumes performance is *transitive and comparable* — but harness performance is noisy and task-dependent, so "better" is often an artifact of which probe tasks you sampled. Copying can also collapse diversity: the whole population converges to one lineage and exploration dies (a known PBT failure). In harness settings the "hyperparameter" space (structure mutations) is discrete and unbounded, unlike PBT's small continuous hyperparameter vectors, so the perturb step needs real design. Open questions: how to maintain *useful* diversity in a harness population (when is a weird lineage worth keeping?); how often to run the exploit step relative to evaluation cost; and whether exploit-and-explore should operate at the component level (per-subproblem populations) rather than whole-harness level.
