---
layout: page
title: 结构智能优化
permalink: /zh/research/structural-optimization/
description: 以学习和优化方法改进结构布置、构件尺寸、加固方案及工程决策。
lang: zh
translation_key: structural-optimization
importance: 2
research_theme: true
label: 设计优化
img: /assets/img/structural-optimization.svg
img_alt: 结构方案比较与设计评价的概念示意图
---

我研究如何结合学习算法与结构分析，在性能与资源约束下改进工程设计。应用包括光伏支架构件截面优化与屈曲约束支撑加固设计。

这些研究将强化学习、生成式模型和数值优化与工程评价相结合：通过深度 Q 网络学习可迁移的截面设计策略，利用生成式方法为支撑加固优化提供候选位置。同时，将专家经验嵌入设计评价，并通过结构优化提高生成式模型训练数据的质量。

## 研究重点

- **设计策略学习：** 面向离散构件尺寸选择与跨结构泛化的强化学习。
- **性能驱动搜索：** 加固布置、材料用量与力学约束下的优化。
- **评价与数据质量：** 融合专家经验的决策方法，以及优化增强的设计数据集。

## 相关论文

{% include publication-list.html theme='structural-optimization' %}

[全部研究方向]({{ '/zh/research/' | relative_url }}) · [全部论文]({{ '/zh/publications/' | relative_url }})
