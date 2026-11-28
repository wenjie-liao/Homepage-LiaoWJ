# 内容维护指南

当前网站整理了本人提供的 23 篇论文。论文事实、分类和方法图信息统一维护，Publications 与三个研究专题共享同一份数据。Teaching 根据本地教学材料整理 4 门课程（2 门本科生课程、2 门研究生课程），共 33 个主题。网站以静态页面提供完整中英文版本，英文沿用原路径，中文使用 `/zh/` 镜像。

## 文件对应关系

| 想修改的内容 | 文件或目录 |
| --- | --- |
| 姓名、全站描述、语言、主题功能 | `_config.yml` |
| 首页简介与展示顺序 | `_pages/about.md` |
| 研究主题总览 | `_pages/research.md` |
| 英文研究专题说明 | `_projects/` 中对应的 Markdown 文件 |
| 中文页面与研究专题说明 | `_pages/zh/` 中对应的 Markdown 文件 |
| 论文页面介绍与布局 | `_pages/publications.md`、`_includes/publication-list.html` |
| 论文的唯一网页事实源 | `_data/publications.json` |
| BibTeX 引用导出副本 | `_bibliography/papers.bib` |
| 论文方法图 | `assets/img/publications/` |
| 软件、平台与演示 | `_pages/software.md` |
| 课程双语内容与主题大纲 | `_data/teaching.json` |
| 教学页面与展示模板 | `_pages/teaching.md`、`_pages/zh/teaching.md`、`_includes/teaching-list.html` |
| 学术经历（网页地址 `/about/`） | `_pages/cv.md` |
| 联系与合作说明 | `_pages/contact.md` |
| 社交／学术主页链接 | `_data/socials.yml` |
| 头像和研究配图 | `assets/img/` |
| 本地核验用论文全文，不对外发布 | `assets/papers/` |
| 本地教材、课件和作业，不对外发布 | `assets/teaching/` |

页面开头两组 `---` 之间是配置，例如 `title`、`permalink`、`nav_order`。正文在第二组 `---` 后面，主要用 Markdown 编写。改变 `permalink` 会改变网页地址，需要同步更新内部链接。

## 中英文页面与语言切换

英文首页为 `/`，中文首页为 `/zh/`；例如 `/publications/` 对应 `/zh/publications/`，`/research/generative-design/` 对应 `/zh/research/generative-design/`。项目站部署时由 `relative_url` 统一添加 `/homepage` 前缀，正文不要写死本地预览域名或部署前缀。

英文页面设置 `lang: en`，中文页面设置 `lang: zh`。同一页面的两个版本必须使用相同 `translation_key`，例如首页均为 `home`，论文页均为 `publications`。导航中的语言开关根据该标识查找另一语言的对应页。新增页面时同时创建译版，核对两个 `permalink`、`translation_key` 和各自的导航顺序。中文正文维护在 `_pages/zh/`；英文研究专题仍在 `_projects/`。

两种语言共享论文与课程数据，不复制两套事实记录。中文论文显示译题，同时保留英文正式题名；作者姓名、单位和期刊名按文献原文显示。首页外链使用学校中文主页、GitHub 与 ORCID，不再添加英文 University profile 入口。

## 维护论文数据

新增或修正论文时，先编辑 `_data/publications.json`，核对原文首页和作者注脚；不要单独修改 BibTeX 来更新网页，也不要在各研究专题重复抄写论文信息。`_bibliography/papers.bib` 仅是从主数据整理的引用导出副本，需与主数据保持一致。

| 字段 | 维护要求 |
| --- | --- |
| `id` | 唯一且稳定的英文标识，供页面锚点和方法图文件名使用 |
| `title`、`journal`、`doi` | 按实际论文记录；DOI 保存标识本身，不附加网址前缀 |
| `authors` | 按原文顺序列出所有作者；每人的 `affiliations` 引用本文单位编号 |
| `affiliations` | 用 `id` 和 `text` 记录单位；ASCE 作者脚注可能包含职称和多个单位，应逐项对应 |
| `year` | 采用正式期刊卷期年份，不按本地文件名、版权年或 DOI 中的年份猜测 |
| `date`、`date_precision` | 用于排序；只知道年份时填 `YYYY-01-01` 并设 `date_precision` 为 `year`，不把占位日期显示为精确发表日 |
| `online_date` | 只填写原文已明确核实的上线日期；接受日期不能代替上线日期 |
| `sort_key` | `期刊年-排序日期`，其中排序日期优先取 `online_date`，缺省时取 `date`；修改年份或日期后同步更新 |
| `title_zh` | 忠实翻译论文题名；不覆盖 `title` 中的正式英文题名 |
| `summary`、`summary_zh` | 原创中英文研究简介；英文约 55–80 词，概括研究问题、方法与有依据的贡献，两种语言保持事实一致 |
| `themes` | 从以下三个主题中选择一项或多项 |
| `figure`、`figure_caption`、`figure_caption_zh`、`figure_number` | 共享方法图路径、中英文简短图注和原论文图号；图应优先展示工作流程、框架或核心机制 |

正式卷期年和上线年可以不同。例如，已核对的部分 Engineering Structures 论文于 2026 年上线，但归入 2027 年卷期。网页按 `sort_key` 降序排列：先按正式期刊年分组，同年内按已核实的 `online_date` 排序，无上线日期时使用 `date`。例如 `2027-2026-10-09` 表示归入 2027 年卷期、在该组内按 2026-10-09 排序。该内部排序键不显示在网页中。

当前分类如下，交叉归类不会增加独立论文总数：

| 主题标识 | 方向 | 当前篇数 |
| --- | --- | --- |
| `generative-design` | 生成式 AI 结构设计 | 18 |
| `structural-optimization` | 智能结构优化 | 5 |
| `seismic-resilience` | 抗震性能与韧性 | 6 |

## 方法图、研究图片和全文

方法图保存为 `assets/img/publications/<id>.png`，对应 JSON 中的 `/assets/img/publications/<id>.png`。保留图内标签，避免裁断箭头、坐标或关键说明；同时核对原论文图号。图下说明应为简短原创描述，页面通过 DOI 提供出版物入口。

论文全文仅留在本地 `assets/papers/`。该目录已被 `.gitignore` 忽略、`_config.yml` 排除及 `scripts/package.py` 排除。不要将全文移到其他公开资源目录、给页面添加本地全文下载链接，或用 `git add -f` 强制提交。`output/paper-review/` 中的提取文本、审校数据和页面截图也仅用于本地核验。

Research 页面不再保留独立的 Research overview 模块。其他必要的研究配图可放在 `assets/img/`。引用示例：

```liquid
![生成式结构设计方法概览]({{ '/assets/img/structural-generation-overview.jpg' | relative_url }})
```

替换图片时同步修改替代文本。研究专题按研究问题、核心方法、应用和相关成果组织；专题的论文列表依据 `themes` 自动筛选，无需手工同步。

## 教学、联系方式与简历

Teaching 的两种语言页面共同读取 `_data/teaching.json`，按 `level` 分为 `undergraduate` 和 `graduate` 两组。当前内容为：

| 类别 | 课程 | 主题数 |
| --- | --- | --- |
| 本科生 | 建筑结构抗震设计 | 8 |
| 本科生 | 智能建造大数据应用与分析 | 12 |
| 研究生 | 土木工程人工智能基础 | 5 |
| 研究生 | 工程结构智能设计 | 8 |

每门课程维护稳定的 `id`、`level`、`title`／`title_zh`、`summary`／`summary_zh` 和 `topics`。每个主题包含 `title`／`title_zh`、`description`／`description_zh`。`code` 只填写可核实的课程代码。英文课名为忠实译名；主题数量表示目前材料覆盖的大纲内容，不等同于实际课时或授课次数。后续更新以实际教学材料和本人确认的信息为准，不推测学分、授课学期或考核方式。

本地材料统一放在 `assets/teaching/`。该目录内全部 PPT、PPTX、PDF、DOCX、HTML、GIF 等文件由 Git、Jekyll 和打包脚本排除；网页不提供教材、课件、交互课件或作业下载，也不公开作业答案。课程简介和大纲采用原创概括，不复制课件全文。本地核验记录位于 `output/teaching-review/`，不作为网页内容。

公开邮箱和学术主页链接分别在 `_data/socials.yml` 与相关正文中维护。简历不属于上述论文全文限制：本人确认可公开的正式 CV 可以放入 `assets/pdf/`，再在 `_pages/cv.md` 添加实际可访问的链接；文件不存在时不添加下载按钮。

## 每次提交前

- 核对新增论文的作者顺序、单位映射、正式年份、DOI 和方法图。
- 检查总论文数与各主题筛选结果，避免把多标签数量相加当成论文总数。
- 确认 `assets/papers/`、`assets/teaching/` 和本地审校材料没有进入 Git 暂存区、构建目录或交付 ZIP。
- 构建后检查两种语言的 DOI、图片、导航和对应页面切换，以及手机宽度下的长题名、作者列表和方法图。
- 更新论文或课程数据时同步维护中英文字段，检查课程分组和大纲主题数量。

## 样式与模板更新

al-folio 核心模板由版本化 gem 提供，常规维护优先修改正文、数据和配置。升级 Gemfile 中的插件时，先保存当前可用版本，在分支上更新并构建，检查页面后再合并。本地模板覆盖可通过 `bundle exec al-folio upgrade overrides audit` 检查。

中文排版通过 `_sass/_personal.scss` 中的系统黑体类字体栈回退（如苹方、微软雅黑、Noto Sans CJK），英文使用系统通用无衬线字体。修改字体时检查头像下中文姓名、英文姓名及中英文正文，避免两种语言互相覆盖字体设置。

个人基本信息来源于[西南交通大学英文主页](https://faculty.swjtu.edu.cn/liaowj/en/index.htm)和[中文主页](https://faculty.swjtu.edu.cn/liaowj/zh_CN/index.htm)；论文信息以本人提供的原文为依据。后续内容更新以核验资料和本人确认为准。
