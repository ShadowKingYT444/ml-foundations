---
concept_id: "gradient-descent"
title: "Gradient Descent & Backpropagation"
origin: "Cauchy 1847; Rumelhart, Hinton & Williams 1986"
field: "Optimization"
modern_adaptation: "TextGrad"
source_url: "https://en.wikipedia.org/wiki/Backpropagation"
relevance: 5
---

## One line
The gradient of a loss function points in the direction of steepest increase, so repeatedly stepping downhill — with derivatives computed efficiently by the chain rule — trains everything from 1980s neural nets to today's giant models.

## The problem
Before backprop, training a multi-layer network meant assigning "credit" for errors to hidden units nobody could observe: perturbing one weight at a time was hopelessly slow, and the perceptron learning rule (Rosenblatt 1958) only handled single layers. The question was whether deep architectures could be trained at all with finite compute. Werbos (1975) described the method in a thesis, but it was the 1986 Rumelhart–Hinton–Williams paper that showed it actually *worked* — networks discovering edge detectors and semantic structure from nothing but error signals.

## How it works
Given a differentiable loss `L(θ)` over parameters `θ`, gradient descent updates `θ ← θ − η∇L(θ)` with step size `η` (the learning rate). If `L` is locally smooth, this is guaranteed to decrease the loss for small enough `η`. Backpropagation is the *algorithm* that computes `∇L` in time linear in the network size instead of quadratic: it applies the chain rule layer by layer, propagating an error signal backward from the output. For a layer `z = Wx`, `a = σ(z)`, the gradient flows as `δ = (W_nextᵀ δ_next) ⊙ σ′(z)`, and each weight's gradient is just an outer product of the local error and the local input. The key insight is that *credit assignment is local*: every parameter only needs to know what its own output contributed, not the whole system.

## Key results
Landmark guarantees: gradient descent converges to a stationary point on smooth non-convex functions, and at an `O(1/√T)` rate to the global optimum for convex Lipschitz losses — the rate behind every convex ML textbook bound. Empirical wins: backprop trained LeNet (LeCun 1989) for digit recognition and, decades later, made ImageNet-scale CNNs, seq2seq models, and transformers possible — the entire deep-learning era is gradient descent plus scale plus data.

## How it maps to modern harness work
TextGrad (Yuksekgonul et al., 2024) lifts this whole machinery into a world with no differentiable weights. The computation graph is an LLM *system*: nodes are prompts, tool calls, and model invocations instead of layers. The analogy is exact and deliberate:

- **Loss** → a task metric or an LLM-judge score on the system's output.
- **Gradient** → *natural-language critique* of why a node's output was bad, i.e. "textual gradients" that point toward better behavior instead of a numeric direction.
- **Backprop (chain rule)** → critique propagation: feedback on the final answer is rewritten into feedback for each upstream node, preserving "which input caused which error."
- **Optimizer step** → the LLM rewrites the node's prompt, code, or tool definition to address the critique.

So TextGrad keeps the *structure* of gradient descent (forward evaluation, backward credit assignment, local parameter update) while replacing every numeric quantity with language. The power of the mapping is that decades of optimizer wisdom — mini-batching, momentum, learning-rate discipline — can be ported by analogy into prompt/harness search.

## Limits and open questions
Textual gradients have no magnitude, no direction guarantee, and no convergence theorem: an LLM critique can be wrong, and "stepping" by rewriting a prompt is a non-local jump, not an `η`-sized move. The chain rule's locality breaks when a critique of a downstream node doesn't cleanly factor through upstream nodes. Open questions: can we calibrate the *reliability* of textual gradients (e.g. self-consistency over critiques)? Is there a principled step-size analog — how aggressive should a rewrite be? And what, if anything, plays the role of second-order information for prompt optimization?
