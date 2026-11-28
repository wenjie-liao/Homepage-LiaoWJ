---
lang: en
translation_key: structural-optimization
layout: page
title: Intelligent structural optimization
description: Learning and optimization methods that improve structural layouts, member sizes, retrofit schemes, and engineering decisions.
permalink: /research/structural-optimization/
importance: 2
label: Design optimization
img: /assets/img/structural-optimization.svg
img_alt: Conceptual illustration of intelligent structural optimization
---

I study how learning algorithms and structural analysis can improve engineering designs under performance and resource constraints. Applications include photovoltaic support member sizing and buckling-restrained brace retrofit design.

This research connects reinforcement learning, generative models, and numerical optimization with engineering evaluation. A deep Q-network learns transferable cross-section design policies; generative retrofit methods identify promising brace locations before optimization. Complementary work embeds expert experience in design evaluation and uses structural optimization to improve the training data available to generative models.

## Research focus

- **Learning design policies:** reinforcement learning for discrete member sizing and cross-structure generalization.
- **Performance-driven search:** retrofit configurations, material use, and mechanical compliance.
- **Evaluation and data quality:** expert-informed decision-making and optimization-enhanced design datasets.

## Related publications

{% include publication-list.html theme='structural-optimization' %}

[All research themes]({{ '/research/' | relative_url }}) · [All publications]({{ '/publications/' | relative_url }})
