---
concept_id: "expectation-maximization"
title: "Expectation-Maximization"
origin: "Dempster, Laird & Rubin 1977"
field: "Statistics"
modern_adaptation: "VACE-style alternating co-evolution"
source_url: "https://en.wikipedia.org/wiki/Expectation%E2%80%93maximization"
relevance: 4
---

## One line
EM fits models with hidden variables by alternating between *guessing* the hidden structure given current parameters (E-step) and *improving* the parameters given those guesses (M-step), with a theorem guaranteeing the likelihood never goes down.

## The problem
Maximum-likelihood estimation breaks when some variables are unobserved: you can't maximize `log p(x | θ)` if the observed data `x` depends on latents `z` you never see. Naive approaches — ignoring the latents, or jointly optimizing `θ` and `z` at once — get stuck or overfit, because the two quantities *condition on each other*: the best parameters depend on the latent assignments, and the best latent assignments depend on the parameters. EM's contribution was to turn this chicken-and-egg problem into a monotone coordinate ascent with a real guarantee.

## How it works
The E-step computes the expected complete-data log-likelihood `Q(θ | θᵗ) = E_{z|x,θᵗ}[log p(x, z | θ)]` — i.e. it fills in the latents with a *distribution*, not a single guess, using the current parameters `θᵗ`. The M-step then sets `θᵗ⁺¹ = argmax_θ Q(θ | θᵗ)`. The elegant part is the proof: by Jensen's inequality, the log-likelihood decomposes into `Q` plus a KL-divergence term that is minimized exactly when the E-step uses the true posterior — so maximizing `Q` guarantees `log p(x | θᵗ⁺¹) ≥ log p(x | θᵗ)`. Monotone ascent to a local optimum is assured. The classic worked example is a Gaussian mixture: the E-step computes soft cluster responsibilities for each point, the M-step recomputes each cluster's mean/covariance as a weighted average.

## Key results
The Dempster–Laird–Rubin (1977) paper proved the monotone-likelihood theorem and unified a zoo of earlier iterative algorithms (k-means, Baum–Welch for HMMs) as special cases. EM remains the canonical way to fit mixture models, HMMs, and topic models; variational EM extends it to intractable posteriors. Its main theoretical caveat is also famous: the guarantee is *local* — EM can and does converge to poor local optima depending on initialization.

## How it maps to modern harness work
VACE (Validation-Gated Alternating Co-Evolution, 2026) adapts EM's alternating structure to the problem of jointly improving an *agent model* and its *harness*. The mapping:

- **E-step analog** → *harness revision*: given the current agent weights, analyze trajectories, diagnose which harness components (prompts, tools, workflow) are the bottleneck, and propose structural edits — this is "estimating the hidden structure" that makes the current parameters perform best.
- **M-step analog** → *RL weight update*: given the revised harness, run agentic reinforcement learning to re-optimize the model weights — the "maximization" conditioned on the latent structure.
- **The EM guarantee** → deliberately weakened: VACE only accepts a new harness after *checkpoint-specific validation*, i.e. it must beat the old harness when the current weights are plugged in. This is a pragmatic stand-in for EM's monotone ascent.

What changed: real EM's guarantee rests on the E-step computing an exact posterior and the M-step solving a well-posed maximization. VACE's "E-step" is an LLM writing harness code — approximate, stochastic, with no Jensen's inequality to lean on — so the validation gate substitutes a *measured* improvement for a *proven* one.

## Limits and open questions
When the "M-step" is an LLM edit rather than an argmax, nothing guarantees monotonicity; validation on a finite checkpoint can accept noise as signal. Worse, the two phases can chase each other's tail: the harness adapts to the current weights' quirks, and the weights then adapt to the new harness's quirks. Open questions: can we formalize a divergence measure for the harness-as-latent that restores some convergence statement? And how do you set the validation gate tight enough to prevent regressions without rejecting the risky-but-good structural changes — the classic gate benefit was 4.6–7.0pp, but that number itself is data-dependent.
