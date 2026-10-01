---
concept_id: "meta-learning"
title: "Meta-Learning (MAML)"
origin: "Finn, Abbeel & Levine, ICML 2017"
field: "Optimization"
modern_adaptation: "Learning Meta-Skills for Agent Harness Design"
source_url: "https://en.wikipedia.org/wiki/Meta_learning_(computer_science)"
relevance: 4
---

## One line
MAML learns an *initialization* of a model's parameters such that a few gradient steps on a new task produce good performance — it optimizes for fast adaptability rather than for any single task.

## The problem
Standard training optimizes parameters for one fixed task distribution; give the model a genuinely new task and it needs massive data to adapt. Humans do the opposite: we learn *how to learn* new skills from a handful of examples. The question was how to make "learning to learn" a concrete optimization problem: can you train parameters so that the *gradient steps themselves* become an effective few-shot learner?

## How it works
MAML has an **inner loop** and an **outer loop**. Given a task `Ti` with loss `LTi`, the inner loop takes one (or a few) gradient steps from shared initialization `θ`:

`θi' = θ − α ∇θ LTi(fθ)`

The outer loop then asks: how good is the *adapted* model? It minimizes the post-adaptation loss summed over tasks:

`min_θ Σ_Ti LTi(f_{θi'})`

The meta-gradient flows *through* the inner update (a gradient of a gradient), which is expensive; first-order approximations like FOMAML and **Reptile** (Nichol, Achiam & Schulman, 2018) drop the second-order terms and work surprisingly well. Intuition: `θ` is positioned at a point in parameter space from which every task's optimum is a short walk away — a "consensus initialization" that is maximally *close* to many task solutions at once. Finn et al. showed this simple scheme achieving landmark few-shot results on Omniglot and Mini-ImageNet classification and on few-shot reinforcement learning, competitive with far more elaborate architectures.

## Key results
The ICML 2017 paper demonstrated that a single meta-learned initialization could adapt to new image-classification tasks and new RL environments with a handful of gradient steps, matching or beating specialized meta-learning architectures of the time. Follow-ups showed the idea was *model-agnostic* (it applies to any gradient-trained model, hence the name) and that even first-order approximations retain most of the benefit — the structure of the two-loop optimization mattered more than exact meta-gradients.

## How it maps to modern harness work
The **meta-skills** paper (arXiv 2609.38143) is MAML with the parameter vector replaced by *harness-building knowledge*. The **inner loop** is per-task adaptation: the Builder assembles a fresh task-specific harness for the Target using the current meta-skills, then observes execution feedback — the analog of taking gradient steps on one task. The **outer loop** is meta-skill learning: the Builder updates its reusable *when / what / how-to-use* skills across many tasks, exactly like MAML updating `θ` to minimize post-adaptation loss. What changed: the "parameters" are natural-language procedural knowledge rather than weights, and the "gradient step" is an LLM reflecting on feedback rather than backprop. But the structural insight transfers wholesale — the paper's headline finding (a +12.02pp Builder-enactment gap: knowledge helps most when compiled into executable support, not delivered as advice) is the MAML lesson in harness form: meta-learning works when the outer loop produces something the inner loop can *act on in a few steps*, not a description of the solution.

## Limits and open questions
MAML assumes tasks come from a coherent distribution; when tasks are wildly heterogeneous, no single initialization is close to all optima, and meta-training can produce an initialization that is mediocre everywhere. The harness analog: meta-skills learned on coding tasks may actively hurt on embodied tasks. Also, MAML's inner loop is a *fixed* few gradient steps — but an LLM's "inner adaptation" (prompting, editing) has no fixed step budget or convergence guarantee. Open questions: what is the right *unit* of a meta-skill so it transfers without negative interference; how to detect when the task distribution has shifted enough that meta-skills need re-learning; and whether the outer loop can itself be automated (meta-meta-learning) rather than hand-scheduled.
