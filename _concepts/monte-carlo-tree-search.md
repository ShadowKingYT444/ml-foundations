---
concept_id: "monte-carlo-tree-search"
title: "Monte Carlo Tree Search"
origin: "Rémi Coulom (2006); UCT by Kocsis & Szepesvári (2006)"
field: "Search"
modern_adaptation: "search over harness revision trajectories"
source_url: "https://en.wikipedia.org/wiki/Monte_Carlo_tree_search"
relevance: 4
---

## One line
MCTS grows a search tree by repeatedly selecting promising branches with an exploration bonus, expanding them, estimating their value with random rollouts, and backpropagating the results.

## The problem
Classical game search (minimax with heuristics) collapsed on Go: the branching factor is ~250 and no reliable evaluation function existed, so exhaustive or shallow heuristic search was hopeless. The question was how to allocate a fixed simulation budget across a huge tree so that effort concentrates where uncertainty is highest — a problem identical to searching the space of possible harness edits, where each candidate revision is expensive to evaluate.

## How it works
Each iteration runs four phases. **Selection**: walk down from the root, at each node choosing the child that maximizes the UCT score `x̄_j + C_p·√(2·ln(n) / n_j)`, where `x̄_j` is the child's mean reward, `n_j` its visit count, `n` the parent's visit count, and `C_p` an exploration constant. **Expansion**: add one or more child nodes for an unexplored move. **Simulation**: play a rollout (often random, sometimes guided) from the new node to a terminal state and observe the reward. **Backpropagation**: update visit counts and mean rewards along the path back to the root. The UCT rule is imported from multi-armed bandits (UCB1, Auer et al. 2002): the first term exploits, the second explores rarely-visited children, and the balance provably concentrates visits on the best moves.

## Key results
Kocsis & Szepesvári (2006) showed UCT converges to optimal action selection with high probability. The landmark win came a decade later: AlphaGo (Silver et al., *Nature*, 2016) fused MCTS with deep policy and value networks and defeated Lee Sedol — the first superhuman Go program, ending a problem the field had considered decades away. The lesson was architectural: search plus learned priors beats either alone.

## How it maps to modern harness work
Harness optimizers that explore sequences of edits — GEPA-style proposal loops, SelfSearch's generational lineages — are doing tree search over *program space*: nodes are harness versions, edges are edits. The **simulation/rollout** analog is evaluating a candidate harness on a task batch; the observed reward (pass rate minus inference cost) plays the role of the playout score, and backpropagation is the credit flowing back to the edit decisions that produced it. UCT's selection rule is the principled answer to the budget question every harness optimizer faces: how much effort goes to refining a promising harness versus trying a structurally different one. SelfSearch's parallel lineages are essentially parallel tree descents without explicit UCT bookkeeping. The modern twist: classical MCTS uses random rollouts, but harness search replaces them with a *learned rollout policy* — an LLM proposing edits — exactly mirroring AlphaGo's move from random playouts to a policy network.

## Limits and open questions
MCTS needs many simulations to converge, and each harness "simulation" costs real inference dollars, not CPU cycles — naive UCT with random edits burns budget on nonsense. The branching factor is effectively infinite (any edit is legal), so without a strong proposal prior the tree never concentrates. Rewards are also noisy and task-dependent, violating the stationary-reward assumption behind UCB theory. Open question: what is the right depth-versus-breadth budget split when a single rollout costs dollars? Nobody has a principled answer yet; current optimizers use fixed heuristics (a few lineages, a few generations) rather than anything like an exploration bonus.
