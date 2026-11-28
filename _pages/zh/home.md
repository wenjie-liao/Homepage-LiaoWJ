---
layout: about
title: 廖文杰 · 学术主页
description: 廖文杰，西南交通大学土木工程学院副研究员。研究聚焦人工智能驱动的结构设计与优化，包括建筑结构生成式设计和结构抗震韧性。
permalink: /zh/
lang: zh
translation_key: home
subtitle: 西南交通大学 · 土木工程学院 · 副研究员
profile:
  align: right
  image: wenjie-liao.png
  image_circular: false
  more_info: >
    <p><span class="profile-name-zh" lang="zh-CN">廖文杰</span> · <span class="profile-name-en" lang="en">Wenjie Liao</span></p>
selected_papers: false
social: false
announcements:
  enabled: false
latest_posts:
  enabled: false
---

<div class="research-intro">
  <p class="eyebrow">人工智能 × 结构工程</p>
  <h2>面向结构设计与优化的生成式人工智能。</h2>
  <p class="lead">我研究人工智能如何生成和改进工程结构，聚焦建筑结构设计与抗震韧性。</p>
</div>

我是西南交通大学土木工程学院副研究员，2022年获得清华大学博士学位，随后在清华大学从事博士后研究至2024年。我的研究聚焦人工智能驱动的结构设计与优化，包括建筑结构生成式设计和结构抗震韧性。

<div class="site-actions">
  <a class="action-primary" href="{{ '/zh/research/' | relative_url }}">了解我的研究</a>
  <a class="action-secondary" href="mailto:liaowj@swjtu.edu.cn">邮件联系</a>
</div>
<div class="profile-links">
  <a href="https://faculty.swjtu.edu.cn/liaowj/" lang="zh-CN">中文主页</a>
  <a href="https://scholar.google.com/citations?user=aE1me5sAAAAJ&amp;hl=zh-CN" lang="en">Google Scholar</a>
  <a href="https://github.com/wenjie-liao">GitHub</a>
  <a href="https://orcid.org/0000-0002-9309-0054">ORCID</a>
</div>

<section class="home-research" aria-labelledby="research-heading">
  <div class="section-heading"><h2 id="research-heading">研究方向</h2><a href="{{ '/zh/research/' | relative_url }}">查看研究</a></div>
  <div class="theme-grid">
  {% assign themes = site.pages | where: 'research_theme', true | where: 'lang', 'zh' | sort: 'importance' %}
  {% for theme in themes %}
    <a class="theme-card" href="{{ theme.url | relative_url }}">
      <img src="{{ theme.img | relative_url }}" alt="{{ theme.img_alt }}" width="560" height="300" loading="lazy">
      <div class="theme-card-body"><h3>{{ theme.title }}</h3><p>{{ theme.description }}</p><span class="text-link">了解这一方向</span></div>
    </a>
  {% endfor %}
  </div>
</section>

<section class="platform-feature" aria-labelledby="platform-heading">
  <div><p class="eyebrow">从研究到工程应用</p><h2 id="platform-heading">AI-structure Copilot</h2><p>我的研究参与支持了建筑结构智能设计平台的开发，将智能设计方法与工程实践相连接。</p></div>
  <a class="action-secondary" href="{{ '/zh/software/' | relative_url }}">了解软件平台</a>
</section>

<section class="home-contact"><h2>交流与合作</h2><p>欢迎就人工智能与结构工程开展研究交流和学术合作，请<a href="mailto:liaowj@swjtu.edu.cn">与我联系</a>。</p></section>
