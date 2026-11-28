---
lang: en
translation_key: research
layout: page
title: Research
permalink: /research/
description: Generative design, intelligent optimization, and seismic resilience of engineering structures.
nav: true
nav_order: 1
---

My research connects generative AI with structural engineering, from learning design representations and generating structural layouts to optimizing engineering decisions and improving seismic performance. The three themes below bring together the methods, applications, and publications behind this work.

<div class="research-list">
{% assign themes = site.projects | sort: 'importance' %}
{% for theme in themes %}
  <article class="research-row">
    <a href="{{ theme.url | relative_url }}"><img src="{{ theme.img | relative_url }}" alt="{{ theme.img_alt }}" width="560" height="300" loading="lazy"></a>
    <div><p class="eyebrow">{{ theme.label }}</p><h2><a href="{{ theme.url | relative_url }}">{{ theme.title }}</a></h2><p>{{ theme.description }}</p><a class="text-link" href="{{ theme.url | relative_url }}">Read about this research</a></div>
  </article>
{% endfor %}
</div>
