---
concept_id: "actor-critic"
title: "Actor-Critic Methods"
origin: "Barto, Sutton & Anderson, 1983"
field: "Reinforcement Learning"
modern_adaptation: "proposer-critic harness revision loops"
source_url: "https://en.wikipedia.org/wiki/Actor%E2%80%93critic_method"
relevance: 4
---

## One line
Actor-critic methods split learning into two roles: an *actor* that proposes actions and a *critic* that estimates how good states are, so the actor can learn from low-variance value estimates instead of noisy full returns.

## The problem
REINFORCE's gradient uses the total return of a whole trajectory, which is unbiased but extremely noisy — one lucky or unlucky rollout swings the update. Waiting for full episodes also delays learning. The question was whether you could get a learning signal *mid-trajectory* that is less noisy than Monte Carlo returns, without waiting for the episode to end.

## How it works
The **actor** is a parameterized policy `πθ(a|s)` that selects actions. The **critic** learns a value function `Vw(s)` estimating expected future return from a state. The key object is the **temporal-difference error**:

`δt = rt + γ Vw(st+1) − Vw(st)`

which measures how much better reality turned out than the critic predicted. The actor updates with `∇θ log πθ(at|st) · δt` — it reinforces actions that *surprised the critic upward*. Because `δt` is computed from a single transition plus the critic's estimate, it has far lower variance than a full-trajectory return. This is **bootstrapping**: the critic updates from its own predictions rather than waiting for ground truth, trading some bias (early critics are wrong) for much faster, lower-variance learning. Barto, Sutton and Anderson's 1983 "neuronlike adaptive elements" paper introduced the two-element architecture; the modern A2C/A3C family (Mnih et al., 2016) scaled it with parallel workers and entropy regularization.

## Key results
The 1983 paper showed an actor-critic could solve difficult control tasks (a simulated pole-balancer and related problems) with function approximation. The policy gradient theorem (Sutton et al., 2000) put the method on rigorous footing by proving the actor's update direction is a true gradient when the critic matches the policy's value function. A3C (2016) demonstrated that asynchronous actor-critic agents could beat prior state of the art across Atari games with dramatically less wall-clock time, cementing the pattern that *a learned evaluator beats raw returns for steering a proposer*.

## How it maps to modern harness work
Nearly every modern harness-revision loop is an actor-critic in disguise. The **actor** is the proposer LLM: SelfSearch's *improver* that edits the agent's repository, GEPA's candidate generator, or any loop that drafts a new harness version. The **critic** is whatever judges the proposal — a second LLM-as-judge, a benchmark score, or a value estimate of "how good is this harness state." The critic's value estimate corresponds to the *expected future task performance of the current harness*, and the TD-error analog is *measured improvement minus expected improvement*: proposals that beat the critic's expectation get reinforced. Why bootstrapping helps here: evaluating a harness fully (running every benchmark) is expensive, exactly like waiting for episode end — a critic that can judge a *partial* signal (a few probe tasks, a static review) gives cheap, low-variance steering. The known failure mode carries over too: if the critic is miscalibrated (a judge that likes verbose harnesses, a benchmark that leaks), the actor optimizes the critic's bias instead of real performance — the harness equivalent of reward hacking.

## Limits and open questions
Classical actor-critic theory needs the critic to be *compatible* with the actor (Sutton et al.'s compatible-function-approximation condition); LLM judges satisfy nothing like that, so the "gradient" modern loops follow is heuristic, not a true gradient. Bootstrapping compounds critic error over revisions — a slightly wrong judge steers ten generations off a cliff. Open questions: can we learn critics that are calibrated enough for multi-generation harness evolution; how to combine expensive ground-truth evaluations with cheap judge estimates (a principled schedule, not vibes); and whether the actor and critic should share a model (as in Video-RSI's Solver/Editor split) or be kept separate to avoid collapse.
