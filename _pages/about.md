---
lang: en
translation_key: home
layout: about
title: Home
permalink: /
subtitle: Associate Research Professor · School of Civil Engineering · Southwest Jiaotong University
profile:
  align: right
  image: wenjie-liao.png
  image_circular: false
  more_info: >
    <p><span class="profile-name-zh" lang="zh-CN">廖文杰</span> · <span class="profile-name-en" lang="en">Wenjie Liao</span></p>
    <p class="profile-location" lang="en">Chengdu, China</p>
selected_papers: false
social: false
announcements:
  enabled: false
latest_posts:
  enabled: false
---

<div class="research-intro">
  <p class="eyebrow">Artificial intelligence × structural engineering</p>
  <h2>Generative AI for structural design and optimization.</h2>
  <p class="lead">I study how artificial intelligence can generate and improve engineering structures, with a focus on building design and seismic resilience.</p>
</div>

I am a researcher at Southwest Jiaotong University. I received my PhD from Tsinghua University in 2022 and continued there as a postdoctoral researcher until 2024. My research focuses on AI-driven structural design and optimization, including generative design of building structures and structural seismic resilience.

<div class="site-actions">
  <a class="action-primary" href="{{ '/research/' | relative_url }}">Explore my research</a>
  <a class="action-secondary" href="mailto:liaowj@swjtu.edu.cn">Email me</a>
</div>
<div class="profile-links">
  <a href="https://faculty.swjtu.edu.cn/liaowj/" lang="zh-CN">中文主页</a>
  <a href="https://scholar.google.com/citations?user=aE1me5sAAAAJ&amp;hl=zh-CN" lang="en">Google Scholar</a>
  <a href="https://github.com/wenjie-liao">GitHub</a>
  <a href="https://orcid.org/0000-0002-9309-0054">ORCID</a>
</div>

<section class="home-research" aria-labelledby="research-heading">
  <div class="section-heading"><h2 id="research-heading">Research themes</h2><a href="{{ '/research/' | relative_url }}">View research</a></div>
  <div class="theme-grid">
  {% assign themes = site.projects | sort: 'importance' %}
  {% for theme in themes %}
    <a class="theme-card" href="{{ theme.url | relative_url }}">
      <img src="{{ theme.img | relative_url }}" alt="{{ theme.img_alt }}" width="560" height="300" loading="lazy">
      <div class="theme-card-body"><h3>{{ theme.title }}</h3><p>{{ theme.description }}</p><span class="text-link">Explore theme</span></div>
    </a>
  {% endfor %}
  </div>
</section>

<section class="platform-feature" aria-labelledby="platform-heading">
  <div><p class="eyebrow">From research to engineering</p><h2 id="platform-heading">AI-structure Copilot</h2><p>My research contributes to an AI-driven design platform for building structures, connecting intelligent design methods with engineering practice.</p></div>
  <a class="action-secondary" href="{{ '/software/' | relative_url }}">Explore the platform</a>
</section>

<section class="home-contact"><h2>Let's connect</h2><p>For research discussions and academic collaboration in AI and structural engineering, please <a href="mailto:liaowj@swjtu.edu.cn">get in touch</a>.</p></section>
