---
lang: en
translation_key: generative-design
layout: page
title: Generative AI structural design
description: Generative models that turn architectural requirements and engineering constraints into structural layouts for buildings and dams.
permalink: /research/generative-design/
importance: 1
label: Design generation
img: /assets/img/generative-design.svg
img_alt: Conceptual illustration of generative ai structural design
---

I develop generative methods that connect architectural intent with structural engineering requirements. This work spans shear wall and beam layouts, component sizing, base-isolation schemes, and zoning of concrete-faced rockfill dams. It also extends to sequential architectural and structural design of detached houses.

The methods combine generative adversarial networks, graph neural networks, and diffusion models with representations of drawings, design conditions, and physical constraints. Key contributions include text-image fusion, component masks, joint wall-beam generation, physics- and rule-guided learning, and mechanical feedback during diffusion. Together, these studies connect design generation with interpretable evaluation and engineering software.

## Research focus

- **Design representations:** drawing semantics, feature masks, graphs, and text-image fusion.
- **Engineering-guided generation:** physical models, design rules, and closed-loop mechanical feedback.
- **Integrated workflows:** from CAD drawings and generated layouts to structural models and design evaluation.

## Related publications

{% include publication-list.html theme='generative-design' %}

[All research themes]({{ '/research/' | relative_url }}) · [All publications]({{ '/publications/' | relative_url }})
