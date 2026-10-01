---
concept_id: "policy-gradient"
title: "Policy Gradients (REINFORCE)"
origin: "Ronald J. Williams, 1992"
field: "Reinforcement Learning"
modern_adaptation: "RLHarness / agentic RL"
source_url: "https://en.wikipedia.org/wiki/Policy_gradient"
relevance: 4
---

## One line
Policy gradients optimize a parameterized policy directly by following the gradient of expected reward, using the log-derivative trick to turn a non-differentiable sampling objective into a usable gradient estimate.

## The problem
Before 1992, reinforcement learning mostly meant learning *value functions* — estimate how good each state is, then act greedily. That works for small discrete action spaces, but it breaks down when actions are continuous, structured, or when the policy needs to be stochastic (games, robotics, any partial observability). Worse, you often cannot differentiate through the environment at all: the reward is a black-box signal (win/lose, task success), and the trajectory distribution depends on the policy itself. The question was how to get a gradient through a sampler you cannot differentiate.

## How it works
REINFORCE's trick is the **log-derivative identity**: since ∇π = π ∇ log π, the gradient of expected return J(θ) = E_τ∼πθ[R(τ)] can be written without ever differentiating the environment:

`∇θ J(θ) = E_τ∼πθ[ R(τ) · Σt ∇θ log πθ(at | st) ]`

Intuition: run the policy, collect full trajectories, and nudge each action's log-probability up in proportion to the total reward that followed. Actions that preceded high reward get reinforced; actions that preceded failure get suppressed. The update is Monte Carlo — it needs only sampled trajectories and the final return, so it works for *any* reward function, differentiable or not. The price is **variance**: the estimator multiplies a high-variance total return by a gradient, so learning is noisy. The fix is a **baseline**: subtract any quantity `b` that is independent of the actions taken — `E[b · ∇θ log π] = 0`, so the estimate stays unbiased — and a good baseline (e.g., average return, or a state-dependent value) can cut variance dramatically.

## Key results
Williams' 1992 paper ("Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning", *Machine Learning* 8:229–256) established REINFORCE as the canonical unbiased gradient estimator for stochastic policies. The policy gradient theorem (2000) made the theory clean and spawned actor-critic methods. REINFORCE with baselines remained the workhorse behind landmark empirical wins — from early neural game players to the RL stage of modern LLM training (RLHF pipelines are, at their core, policy-gradient updates on non-differentiable human-preference rewards).

## How it maps to modern harness work
Agentic RL — e.g. **RLHarness**-style systems that fine-tune an agent's policy or its harness parameters against task success — is REINFORCE lifted into the harness setting. The analogs: the **policy** is the agent's decision process (or the harness's routing logic); the **trajectory** is a full multi-step rollout with tool calls; the **return** is a 0/1 task-success signal, exactly the non-differentiable black-box reward REINFORCE was built for. What changed: the "actions" are natural-language tool calls and the horizon is long, so the variance problem Williams flagged becomes extreme — success is sparse and credit must propagate across dozens of steps. That is why modern systems rediscover baselines: per-task difficulty normalization, group-relative scoring (compare rollouts of the *same* task, as in GRPO-style objectives), and learned reward models are all baseline machinery doing variance reduction. If you want to adapt foundational ideas to harness engineering, the first question is always the REINFORCE question: *what is your unbiased gradient signal, and what baseline are you subtracting?*

## Limits and open questions
REINFORCE is unbiased but can be so noisy it is practically unusable without a strong baseline — and in harness settings, a good state-dependent baseline is hard to learn because the "state" is a whole conversation history. The theory also assumes a stationary environment, while a harness that is itself being edited makes the environment non-stationary (the policy's past data goes stale). Open questions: how to do credit assignment across long tool-use trajectories without drowning in variance; whether language-model critics can serve as low-variance surrogate returns without injecting their own bias; and how often to refresh the policy when the harness underneath it keeps changing.
