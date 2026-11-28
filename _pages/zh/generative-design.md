---
layout: page
title: 生成式人工智能结构设计
permalink: /zh/research/generative-design/
description: 将建筑需求与工程约束转化为建筑结构布置和面板堆石坝分区方案的生成式方法。
lang: zh
translation_key: generative-design
importance: 1
research_theme: true
label: 方案生成
img: /assets/img/generative-design.svg
img_alt: 建筑平面与结构布置生成的概念示意图
---

我研究连接建筑设计意图与结构工程要求的生成式方法，涵盖剪力墙与梁的布置、构件尺寸、隔震方案及混凝土面板堆石坝分区，并进一步拓展到独立住宅的建筑与结构顺序协同设计。

这些方法将生成对抗网络、图神经网络和扩散模型，与图纸表达、设计条件及物理约束相结合。相关工作包括文本与图像融合、构件掩膜、墙梁协同生成、物理与规则引导学习，以及扩散过程中的力学反馈，推动设计生成与可解释评价、工程软件相衔接。

## 研究重点

- **设计表达：** 图纸语义、特征掩膜、图结构与文本图像融合。
- **工程约束引导：** 融合物理模型、设计规则与闭环力学反馈。
- **设计流程集成：** 从 CAD 图纸和生成方案，连接到结构模型与设计评价。

## 相关论文

{% include publication-list.html theme='generative-design' %}

[全部研究方向]({{ '/zh/research/' | relative_url }}) · [全部论文]({{ '/zh/publications/' | relative_url }})
