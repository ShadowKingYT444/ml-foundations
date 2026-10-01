---
concept_id: "evolutionary-strategies"
title: "Evolutionary Strategies & Genetic Algorithms"
origin: "Holland 1975; Rechenberg & Schwefel 1970s"
field: "Search"
modern_adaptation: "PluginRSI / DGM / mixture-of-branches"
source_url: "https://en.wikipedia.org/wiki/Genetic_algorithm"
relevance: 5
---

## One line
Keep a *population* of candidate solutions, let the fittest reproduce with random *mutations* (and crossover), and repeat — a gradient-free optimizer that works on any representation, from bit strings to neural weights to plugin code.

## The problem
Gradient methods need differentiable objectives; many real problems — combinatorial design, program synthesis, architectures — have no gradient at all. Hill climbing from a single point gets trapped in local optima and can't hedge its bets. Holland's (1975) *Adaptation in Natural and Artificial Systems* asked whether the *process* of natural selection could be formalized as a general search algorithm, and Rechenberg and Schwefel were independently evolving aerodynamic shapes in 1970s Berlin with what became evolution strategies (ES).

## How it works
A genetic algorithm maintains a population of individuals (each a candidate solution, e.g. a bit string). Each generation: (1) **evaluate** fitness for all; (2) **select** parents with probability proportional to fitness — fitness-proportionate (roulette-wheel) selection, or tournament selection in modern practice; (3) **crossover** recombines two parents' representations; (4) **mutate** perturbs the offspring slightly. The schema theorem (Holland) gives the intuition for why this works: selection exponentially amplifies above-average *building blocks* (schemas), while mutation and crossover explore new combinations. Evolution strategies drop crossover and work directly on real-valued vectors with adaptive step sizes (the famous 1/5 success rule, then CMA-ES's covariance adaptation). The key property: it's a *population* method, so diversity is intrinsic and there's no single point of failure.

## Key results
Holland's schema theorem (1975) and the building-block hypothesis gave GA its theoretical folklore. CMA-ES (Hansen & Ostermeier, 2001) became the gold standard for black-box continuous optimization. The famous empirical revival: Salimans et al. (2017) showed ES — basically Gaussian perturbations plus fitness-weighted averaging — could train deep RL policies competitively with gradient methods, proving evolution scales to millions of parameters.

## How it maps to modern harness work
Recursive self-improvement systems are evolutionary algorithms where the genome is *harness code* and the mutator is an LLM. Three modern instantiations:

- **PluginRSI**: the *unit of selection* is the plugin, not the whole harness. A library of ~75 plugins evolves: useful plugins reproduce (get reused/composed), useless ones die out. This is the building-block hypothesis made literal — selection accumulates knowledge in *modular* units, so the population's total knowledge grows even as individual agents come and go.
- **DGM (Darwin Gödel Machine)**: the whole agent codebase is the individual; the LLM proposes code edits (mutations), keeps the ones that improve benchmark scores (selection), and archives the lineage. Self-modifying code as an evolutionary process.
- **Mixture of self-improving branches**: a *population of two* harness lineages, each evolving against the data subset it "owns" — speciation by niche, with a router (not crossover) combining them at deploy time.

What changed versus classical GA: the mutation operator went from random bit flips to an *intelligent* proposer (the LLM writes directed edits), which is both the superpower (far fewer wasted evaluations) and the failure mode (the mutator's biases become the search's blind spots).

## Limits and open questions
LLM-guided mutation is not random: it inherits the model's priors, so "diversity" must be enforced rather than assumed. Fitness evaluation is noisy and expensive (full rollouts), making selection unreliable — a lucky evaluation can fix a bad mutation in the population. And there's no crossover analog worthy of the name: merging two harness lineages' code is still an unsolved composition problem. Open questions: what is the right unit of selection — plugin, file, whole repo? Can we get the building-block accumulation of PluginRSI without a human fixing the plugin interfaces in advance? And does intelligent mutation converge prematurely in exactly the way random mutation was designed to avoid?
