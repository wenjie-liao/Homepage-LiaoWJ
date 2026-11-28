---
layout: page
title: 研究方向
permalink: /zh/research/
description: 生成式人工智能、结构智能优化，以及工程结构的抗震性能与韧性。
lang: zh
translation_key: research
nav: true
nav_order: 1
---

我的研究将人工智能与结构工程相结合，贯通设计表达、结构方案生成、工程决策优化和抗震性能提升。以下三个方向汇集了相关方法、应用与研究论文。

<div class="research-list">
{% assign themes = site.pages | where: 'research_theme', true | where: 'lang', 'zh' | sort: 'importance' %}
{% for theme in themes %}
  <article class="research-row">
    <a href="{{ theme.url | relative_url }}"><img src="{{ theme.img | relative_url }}" alt="{{ theme.img_alt }}" width="560" height="300" loading="lazy"></a>
    <div><p class="eyebrow">{{ theme.label }}</p><h2><a href="{{ theme.url | relative_url }}">{{ theme.title }}</a></h2><p>{{ theme.description }}</p><a class="text-link" href="{{ theme.url | relative_url }}">了解这一研究方向</a></div>
  </article>
{% endfor %}
</div>
