---
concept_id: "knowledge-distillation"
title: "Knowledge Distillation"
origin: "Hinton, Vinyals & Dean (2015)"
field: "Statistics"
modern_adaptation: "distilling repair skills into reusable plugins"
source_url: "https://en.wikipedia.org/wiki/Knowledge_distillation"
relevance: 4
---

## One line
A large teacher model's softened output distribution trains a smaller student to match it, transferring "dark knowledge" about class similarities that one-hot labels throw away.

## The problem
Big models are expensive to deploy, but training small models from scratch on hard labels underperforms badly. The teacher's full output distribution carries information the labels don't: a "5% cat, 90% dog" output says cats are more similar to dogs than to cars. The question was how to make that implicit knowledge trainable — and the same question arises in harness work, where an expensive successful *process* (a full debugging session, a costly search) needs to become a cheap reusable *component*.

## How it works
Given teacher logits `zᵢ`, soften with temperature `T`: `pᵢ = exp(zᵢ/T) / Σⱼ exp(zⱼ/T)`. Higher `T` spreads probability mass, exposing the teacher's beliefs about similarity structure. The student minimizes `L = α·CE(student_T, teacher_T) + (1−α)·CE(student, hard labels)` — matching soft targets plus the ground truth. Hinton et al. (2015) showed a distilled shallow network approaching deep-network performance on MNIST, and the idea scaled to production model compression (e.g., DistilBERT, 2019). Variants distill intermediate features, attention maps, and even self-distill within one architecture.

## Key results
"Distilling the Knowledge in a Neural Network" (Hinton, Vinyals & Dean, arXiv 2015) launched model compression as a mainstream practice. It reframed the goal: the student isn't learning the *data*, it's learning the teacher's *function*, including the teacher's uncertainty. The temperature parameter turned out to be the key dial — too low and the student gets one-hot-like targets and learns nothing extra; too high and everything is uniform noise.

## How it maps to modern harness work
The harness analog is **compiling knowledge into executable form**. AgentBug-Smith distills repair skills from mined real-world bug fixes so agents fix harness bugs faster; PluginRSI's 75-plugin library is distilled reusable behavior, each plugin a chunk of "dark knowledge" compiled from many successful trajectories into an executable unit. The mapping: the teacher is the expensive full process (a frontier model's repair trace, a full search episode); the soft targets are the detailed statistics of *how* it succeeded (which fixes worked on which bug classes); the student is the small reusable component that behaves correctly on its covered cases. The temperature analog is how much of the teacher's nuance — edge cases, rare failure modes — survives compilation. Just as low-temperature distillation loses information, compressing a rich repair trajectory into a plugin loses context, which is exactly why distilled skills are narrow specialists rather than generalists.

## Limits and open questions
Distillation transfers behavior, not understanding: the student inherits the teacher's biases and blind spots, and can be *confidently wrong* where the teacher was merely uncertain. In harness land, a distilled plugin is frozen at the knowledge available when it was made — if the environment or tool APIs shift, the plugin silently goes stale, and no amount of matching old soft targets will fix it. The open question is versioning: how do distilled components get *updated* when the teacher process would now do something different? That staleness problem is the same one adaptive decomposition attacks by keeping structure live (split/fuse) instead of frozen. A promising direction is distillation with a refresh loop — re-distilling from fresh teacher traces on a schedule — but nobody has characterized how often that loop must run to stay ahead of drift.
