---
concept_id: "simulated-annealing"
title: "Simulated Annealing"
origin: "Kirkpatrick, Gelatt & Vecchi 1983; Černý 1985"
field: "Optimization"
modern_adaptation: "acceptance rules for harness revisions"
source_url: "https://en.wikipedia.org/wiki/Simulated_annealing"
relevance: 3
---

## One line
To escape local optima, sometimes *accept a worse solution* — with probability that decays over time — so early search explores broadly and late search settles, mimicking the slow cooling of a metal into a low-energy crystal.

## The problem
Greedy hill climbing ("only accept improvements") gets permanently trapped in the first local optimum it finds. For combinatorial problems like chip placement or the traveling salesman, the landscape is riddled with local optima, and pure greed is hopeless. Kirkpatrick, Gelatt, and Vecchi (1983) — physicists at IBM — noticed the analogy to statistical mechanics: a metal cooled slowly reaches a near-perfect crystal (global energy minimum), while quenched metal freezes defects in place. The question was whether *temperature* could be a controllable parameter of search.

## How it works
From the current solution, propose a random neighbor. If it's better, accept it. If it's worse by `ΔE`, accept it with the **Metropolis criterion**: probability `exp(−ΔE / T)`, where `T` is the temperature. At high `T`, almost everything is accepted (random walk, broad exploration); as `T → 0` on a *cooling schedule* (e.g. geometric `T ← αT` with `α` near 1), the search freezes into greedy descent. The deep result (Geman & Geman 1984; Hajek 1988): with a logarithmic cooling schedule, simulated annealing converges *in probability* to the global optimum — one of the few global-convergence guarantees in non-convex optimization, bought at the price of impractically slow cooling. In practice, geometric schedules are the standard compromise.

## Key results
The 1983 *Science* paper launched a thousand applications: VLSI placement, scheduling, protein folding approximations. The Geman–Geman and Hajek theorems established that the *stationary distribution* of the Markov chain at fixed `T` is the Boltzmann distribution `∝ exp(−E/T)`, so slow cooling tracks the global minimum. The practical lesson: the *schedule* is everything — the theory's logarithmic schedule is too slow for any real problem, so every application is an artful compromise.

## How it maps to modern harness work
Every harness optimizer faces the acceptance question: a proposed revision scores *worse* on the dev set — keep it or revert? Current systems mostly implement the `T = 0` extreme: greedy acceptance with rollback (VACE's validation gate, DGM's archive-and-revert). Simulated annealing suggests the missing middle:

- **Energy** → negative task score (or a cost-penalized objective, like LongHarness Bench's accuracy-per-dollar).
- **Temperature** → an explicit exploration budget that *decays over the run*: early revisions are accepted liberally (even regressions) to escape the initial harness's local optimum; late revisions face a strict gate.
- **Metropolis criterion** → a principled alternative to today's binary gates: accept a locally-worse revision with probability `exp(−Δscore / T)`, so small regressions sometimes survive to enable later breakthroughs — exactly the "locally improving but globally regressive" tension that rollback mechanisms currently resolve by pure veto.

What changed: the "neighborhood" is now LLM-proposed edits rather than random perturbations, and the objective is a noisy rollout estimate rather than an exact energy. The Self-Healing Harness finding — 211 of 383 replay-decided rejections were locally improving but globally regressive — is precisely the phenomenon a temperature schedule is designed to manage.

## Limits and open questions
The global-convergence theorem needs the logarithmic schedule nobody can afford, and it assumes exact energy evaluations — harness scores are noisy, so `ΔE` itself is uncertain and the Metropolis criterion misfires. Worse, "temperature" has no natural units in harness space: what does it mean to cool a code-editing process? Open questions: can we define temperature operationally (e.g. the LLM proposer's sampling temperature, or a decaying tolerance for dev-set regressions)? Is there an analog of the Boltzmann stationary distribution for populations of harness lineages? And empirically: does any real harness optimizer benefit from non-greedy acceptance, or is the landscape such that regressions are never worth it?
