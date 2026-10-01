---
concept_id: "curriculum-learning"
title: "Curriculum Learning"
origin: "Bengio, Louradour, Collobert & Weston (2009)"
field: "Learning Theory"
modern_adaptation: "ordering tasks for harness evolution"
source_url: "https://en.wikipedia.org/wiki/Curriculum_learning"
relevance: 3
---

## One line
Train on easy examples first and gradually increase difficulty, so the learner builds on mastered skills instead of drowning in hard cases from the start.

## The problem
Training on the full hard distribution from scratch can stall in bad local minima or take far longer than necessary; human education strongly suggests ordering matters. But in machine learning the "right" order isn't obvious, and a wrong order can be worse than none. The same dilemma faces harness evolution: evolving a harness directly on hard multi-step tasks yields mostly total failures — zero informative gradient — while easy tasks give cheap, high-signal feedback.

## How it works
Define a difficulty measure (or have a teacher order examples), then sample from a distribution that starts concentrated on easy examples and anneals toward the full data distribution (Bengio et al., 2009). Later formalized as self-paced learning (Kumar et al., 2010), where the learner itself selects low-loss examples. The mechanism is a continuation method: early easy examples place parameters in a good basin of attraction, and later hard examples fine-tune without escaping it. Intuition: solve a smoothed version of the problem first, then sharpen. The difficulty measure is the load-bearing part of the whole idea — everything downstream depends on it being right.

## Key results
"Curriculum learning" (Bengio et al., ICML 2009) showed faster convergence and better generalization on toy vision and language tasks with hand-designed curricula. The replication history since has been mixed: benefits are real when the difficulty measure aligns with the learning dynamics, and absent or negative when it doesn't. Several studies have found *anti-curricula* (hard examples first) winning on some tasks, which sharpened the field's understanding that a curriculum is a bias, not a free lunch.

## How it maps to modern harness work
A harness optimizer that evolves first on simple tasks (short, single-tool, unambiguous success criteria) and escalates to hard ones (multi-step, adversarial, long-horizon) is running a curriculum: early tasks provide cheap, high-signal structure learning, and later tasks stress-test it. Self-evolving agents that bootstrap in easy environments before hard ones do this implicitly. The analog of "easy examples" is *tasks where the current harness already earns partial credit*, so evolution sees informative failures (which component broke) rather than total noise. This also explains a failure mode seen in practice: evolving directly on the hardest benchmark tasks produces flat zero scores and the optimizer learns nothing — the harness-space version of drowning.

## Limits and open questions
A curriculum is a bias, and a wrong one actively hurts: if easy tasks teach the wrong structure, the optimizer converges to a harness that is locally excellent and globally wrong — and then "hard" tasks just look like noise. In harness evolution, "easy" is hard to define without already knowing the solution, and easy-for-the-model may not be easy-for-the-harness-structure. The open question is who defines difficulty: a static designer curriculum risks misalignment with what the evolving harness actually needs next, while a self-paced (agent-chosen) curriculum risks gaming — the agent picking tasks that make it look good. This is the same credit-assignment tension at the heart of adaptive decomposition: local "progress" can be globally misleading, and any curriculum is only as good as its progress metric.
