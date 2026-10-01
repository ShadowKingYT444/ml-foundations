---
concept_id: "variational-inference"
title: "Variational Inference"
origin: "Michael Jordan and colleagues (Ghahramani, Jaakkola, Saul), late 1990s"
field: "Optimization"
modern_adaptation: "surrogate objectives for harness search"
source_url: "https://en.wikipedia.org/wiki/Variational_Bayesian_methods"
relevance: 2
---

## One line
When the exact quantity you want is intractable to compute, variational inference optimizes a tractable *lower bound* on it instead — and maximizing the bound pushes up the real thing.

## The problem
In Bayesian models you want the posterior p(z | x) — the distribution over hidden causes given observations. Bayes' rule gives p(z | x) = p(x, z) / p(x), but the denominator p(x) = ∫ p(x, z) dz is an integral over all hidden configurations, intractable for any interesting model. Exact inference was the bottleneck that kept Bayesian methods toy-sized through the 1980s. Sampling (MCMC) was the alternative, but it was slow and hard to diagnose.

## How it works
Instead of computing the true posterior, pick a tractable family of distributions q(z; φ) and find the member *closest* to the true posterior by minimizing KL(q || p(·|x)). The clever part: this minimization is equivalent to maximizing the **ELBO** (evidence lower bound),

    ELBO(φ) = E_q[log p(x, z)] − E_q[log q(z; φ)]

because log p(x) = ELBO + KL(q || p(·|x)), and log p(x) doesn't depend on φ. So maximizing the ELBO simultaneously (a) tightens the lower bound on the model evidence and (b) drives q toward the true posterior. The intractable integral is replaced by expectations under q, which you can approximate with samples. The price: the bound has a *gap* — if your q family can't express the true posterior (say you use a Gaussian for a multimodal posterior), you converge to the best approximation within the family, not the truth. Modern variational autoencoders are this idea with q parameterized by a neural network.

## Key results
- **Jordan, Ghahramani, Jaakkola & Saul (1999):** the tutorial that unified variational methods for graphical models and made them mainstream.
- **Peterson & Anderson (1987):** earlier mean-field work on Boltzmann machines — the conceptual seed.
- **Kingma & Welling (2013):** the variational autoencoder — VI with amortized, neural-network q, trained by backprop through the ELBO.

## How it maps to modern harness work
Harness search has the same structural problem VI solves: the *true objective* — expected performance of a harness on the real task distribution — is intractable (you'd need to run the harness on infinitely many tasks with human grading). So the field optimizes a **surrogate**: a small dev set, an LLM judge's score, a reward model's estimate. That's the ELBO move — maximize a tractable stand-in and hope the gap to the truth is small. The VI lens adds two useful warnings. First, the gap matters: just as a restricted q family caps how good your posterior approximation can be, a restricted surrogate (say, an LLM judge that likes verbosity) caps how good your evolved harness can be — you converge to the best harness *for the judge*, not for reality. Second, VI theory says to *monitor the gap*: in harness terms, periodically re-evaluate top candidates on the expensive true-ish objective (fresh tasks, human grades) and check whether surrogate rankings still agree. VACE's checkpoint-gated validation is a primitive version of exactly this — re-anchoring the surrogate to ground truth at each round.

## Limits and open questions
The analogy is conceptual, not mathematical — nobody has an ELBO-style bound relating "LLM-judge score" to "true harness quality," and the KL gap has no measurable counterpart when your surrogate isn't a distribution. Surrogate optimization in harness land is also *adversarial* in a way VI isn't: an evolving harness can actively exploit the judge (reward hacking), while a posterior can't exploit the ELBO. The open question is whether we can build surrogates with *certified* gaps — e.g. a judge whose disagreement with human grades is itself bounded — which would turn "optimize the surrogate" from a hope into a guarantee. Until then, this idea is a design discipline (name your surrogate, budget gap-checks) rather than a deployable technique.
