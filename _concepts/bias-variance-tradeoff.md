---
concept_id: "bias-variance-tradeoff"
title: "The Bias-Variance Tradeoff"
origin: "Geman, Bienenstock & Doursat, 1992 ('Neural networks and the bias/variance dilemma')"
field: "Statistics"
modern_adaptation: "split/fuse decisions in adaptive decomposition"
source_url: "https://en.wikipedia.org/wiki/Bias%E2%80%93variance_tradeoff"
relevance: 4
---

## One line
Expected prediction error decomposes into three parts — bias (how wrong your model's average answer is), variance (how much it flinches with different data), and irreducible noise — and shrinking one usually grows the other.

## The problem
Early neural-network work was puzzling: bigger models fit training data beautifully and then collapsed on new data, while small models were stable but mediocre everywhere. People lacked a language for *why* adding capacity helps one failure mode and hurts another. The bias–variance decomposition gives it: for squared error, expected error over random training sets equals

    E[error] = bias² + variance + irreducible noise

where **bias²** = (average prediction − truth)² measures systematic error from a too-rigid model, **variance** = E[(prediction − average prediction)²] measures sensitivity to the particular data sampled, and the noise term is baked into the problem and no model can remove.

## How it works
Picture fitting a curve through noisy points. A straight-line fit has high bias (it can't bend) but low variance (two different datasets give nearly the same line). A high-degree polynomial fit has low bias (it can wiggle to the truth) but high variance (two datasets give wildly different wiggles). The textbook U-curve: as model complexity rises, bias falls and variance rises, and total error is minimized at the sweet spot in the middle. Regularization, early stopping, bagging (variance reduction), and ensembles all make sense as tools that move you along this curve.

## Key results
- **Geman et al. (1992):** the formal decomposition for neural networks, linking it to statistical estimation theory.
- **Breiman (1996):** bagging provably reduces variance without much bias cost — the mechanism behind random forests.
- **Belkin et al. (2019):** the *double-descent* curve showed the classic U can turn back down past the interpolation point in overparameterized models — the tradeoff is real but the classical picture is incomplete for modern deep learning.

## How it maps to modern harness work
This is the missing vocabulary for **split/fuse** decisions in adaptive decomposition. Consider a harness component that handles, say, file I/O. As one monolithic component it has *high bias* (one design must serve every sub-case: CSV parsing, error retries, large files) but *low variance* (it was evolved against the whole task set, lots of data). Split it into three specialized subcomponents and each gets *lower bias* (each can specialize) but *higher variance* (each is now tuned on a third of the failure data — a lucky or unlucky sample can make it brittle). Fusing does the reverse: you pool data and share evidence (variance down) but force one design to cover heterogeneous cases (bias up). So the split/fuse question is literally a bias–variance question: split when a component's error looks *systematic* (fails the same way on many inputs → bias), fuse when error looks *brittle* (works except on a few sampled cases → variance). The classic diagnostics transfer too: error on many tasks but consistent patterns → split; error only on rare tasks → maybe don't touch it.

## Limits and open questions
The clean decomposition holds for squared error with a fixed model class and i.i.d. data — none of which an evolving harness has. Harness "error" isn't a clean scalar; a component's failure is entangled with upstream and downstream components (a correct component fed garbage fails), so component-level bias/variance is confounded by system composition. Also, in harness search we rarely have *enough* failure cases per component for variance estimates to be meaningful — the analog of "more data" (run more tasks) is expensive in LLM-evaluation dollars. A genuinely useful version would need a notion of per-component error attribution first, which circles back to the credit assignment problem.
