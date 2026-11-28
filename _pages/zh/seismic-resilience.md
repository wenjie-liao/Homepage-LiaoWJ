---
layout: page
title: 抗震性能与韧性
permalink: /zh/research/seismic-resilience/
description: 建筑结构的减隔震、智能加固设计、自适应振动控制、响应识别与不确定性评估。
lang: zh
translation_key: seismic-resilience
importance: 3
research_theme: true
label: 结构性能
img: /assets/img/seismic-resilience.svg
img_alt: 地震作用下建筑结构的概念示意图
---

我研究结构体系、减隔震措施与可靠的响应信息如何共同提升抗震性能，内容涵盖高层建筑牺牲耗能伸臂体系、智能隔震设计，以及钢筋混凝土框架的屈曲约束支撑加固。

这些研究将物理机制与学习方法相结合：利用可更换耗能构件控制结构损伤，以物理与规则引导的生成式模型支持隔震设计，并将生成式搜索与加固优化耦合。通过卷积神经网络识别环境振动，选择经优化的线性二次型调节器参数，实现自适应振动控制。时频响应识别及加速度传感器不确定性研究，则关注用于理解结构行为的测量与评估信息的质量。

## 研究重点

- **减隔震措施：** 牺牲耗能、隔震支座与支撑加固。
- **智能加固设计：** 生成候选布置，并与结构优化相结合。
- **自适应振动控制：** 基于卷积神经网络的振动识别，以及经优化的线性二次型调节器参数选择。
- **响应与不确定性：** 基于深度迁移学习的响应识别，以及传感器对损伤评估的影响。

## 相关论文

{% include publication-list.html theme='seismic-resilience' %}

[全部研究方向]({{ '/zh/research/' | relative_url }}) · [全部论文]({{ '/zh/publications/' | relative_url }})
