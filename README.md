# Wenjie Liao · 廖文杰的学术主页

面向中文与国际同行的中英双语个人学术网站，基于 [al-folio](https://github.com/alshedivat/al-folio) v1，使用 Jekyll 构建、GitHub Pages 托管。

- 源码仓库：[wenjie-liao/homepage](https://github.com/wenjie-liao/homepage)
- 预期发布地址：[https://wenjie-liao.github.io/homepage/](https://wenjie-liao.github.io/homepage/)（部署完成后可访问）
- 本地目录：`E:\Gitcodes\Homepage-LiaoWJ`；当前开发分支：`init`
- 已有首页、研究方向与三个研究专题、23 篇论文、软件与模型、Teaching／教学、学术经历和联系页面；支持全站中英文切换、手机布局和深浅色切换。
- 英文页面保留原有路径 `/`，中文页面使用 `/zh/` 镜像；部署到当前项目站后分别为 `/homepage/` 和 `/homepage/zh/`。切换语言会进入当前页面的对应译版。
- 论文条目由本人提供的 23 篇原文核对整理，展示作者、单位、原创中英文简介、代表方法图和 DOI。三个主题分别收录 18、5、6 篇，允许交叉归类。
- Teaching 按本科生和研究生分组，依据本地材料整理 4 门课程、共 33 个主题，课程数据统一存放在 `_data/teaching.json`；不提供教材、课件或作业下载。
- 基础信息和头像来自学校公开主页。首页外链保留中文主页、GitHub 和 ORCID；原英文 University profile 入口已移除。研究总览图片已从 Research 页面移除。

## 本机预览

本机已在相邻的 `paper-search` 项目下配置便携 Ruby。预览脚本会优先使用系统 Bundler，其次自动查找该便携环境；需要 Python 3 提供本地 HTTP 服务。

```powershell
Set-Location E:\Gitcodes\Homepage-LiaoWJ
powershell -ExecutionPolicy Bypass -File .\scripts\preview.ps1 -Rebuild
```

打开 [http://127.0.0.1:4173/](http://127.0.0.1:4173/)，按 `Ctrl+C` 停止服务。修改源文件后重新运行带 `-Rebuild` 的命令；省略该参数会复用已有构建。端口被占用时可加 `-Port 4174`。

如果便携环境的位置改变，可以显式指定：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\preview.ps1 -Rebuild -RubyRunner "E:\Gitcodes\paper-search\tools\ruby-runtime\run-ruby.ps1"
```

其他电脑安装 Ruby 3.3 和 Bundler 后，在仓库根目录运行：

```sh
bundle install
bundle exec jekyll serve --host 127.0.0.1 --port 4000
```

该方式使用 [http://127.0.0.1:4000/](http://127.0.0.1:4000/)，并自动重建内容修改。修改 `_config.yml` 后需重启服务。Node.js 仅用于可选的格式化工具，不是网站构建的必需依赖。

## 内容在哪里修改

| 内容                     | 文件或目录                                           |
| ------------------------ | ---------------------------------------------------- |
| 首页简介与研究入口       | `_pages/about.md`                                    |
| 研究方向总览             | `_pages/research.md`                                 |
| 三个研究专题             | `_projects/`                                         |
| 论文事实与展示             | `_data/publications.json`、`_pages/publications.md` |
| 论文方法图                 | `assets/img/publications/`                           |
| 教学双语内容与展示         | `_data/teaching.json`、`_pages/teaching.md`、`_includes/teaching-list.html` |
| 中文页面正文               | `_pages/zh/`，通过 `translation_key` 对应英文页面 |
| 软件、代码与模型         | `_pages/software.md`                                 |
| 学术经历（About）        | `_pages/cv.md`，网页地址为 `/about/`                 |
| 联系方式                 | `_pages/contact.md`、`_data/socials.yml`             |
| 头像和研究图片           | `assets/img/`                                        |
| 网站标题、导航与功能开关 | `_config.yml`                                        |
| 自定义配色与排版         | `_sass/_personal.scss`                               |

`_data/publications.json` 是论文网页的唯一事实源，Publications 与研究专题共同读取；`_bibliography/papers.bib` 仅为引用导出副本。年份按正式期刊卷期记录，只有已核实的 `online_date` 才显示上线日期；未知月日时的 `YYYY-01-01` 仅为排序占位。列表按 `sort_key` 降序排列，先按正式期刊年、再按已核实的上线日期（缺省时用 `date`）排序。具体维护方法见 [内容维护指南](docs/CONTENT-GUIDE-ZH.md)。

论文全文和教学材料分别保存在本地 `assets/papers/`、`assets/teaching/`，两个目录均由 Git 忽略、Jekyll 构建排除及打包脚本排除。教学材料中的 PPT、PPTX、PDF、DOCX、HTML 和 GIF 均不进入公开仓库或网站，页面只展示原创课程简介与大纲。论文页面使用方法图和 DOI 链接，不提供本地全文下载。

双语页面分别设置 `lang: en` 或 `lang: zh`，同一内容的两种语言使用相同的 `translation_key`。论文中文题目、简介和图注统一使用 `_data/publications.json` 中的 `title_zh`、`summary_zh`、`figure_caption_zh`；英文正式题名及作者单位保留以便核对。中文使用系统黑体类字体回退，英文采用系统通用无衬线字体，相关设置位于 `_sass/_personal.scss`。

## 发布到 GitHub Pages

仓库已经创建，无需重新套用模板。当前 `init` 分支用于初始化和检查；工作流在 `init` 上构建验证，在 `main`（或 `master`）上构建并发布。

1. 检查本地修改，提交并推送 `init` 分支。
2. 在仓库 **Settings → Pages → Build and deployment** 中，将 **Source** 设为 **GitHub Actions**。
3. 将 `init` 的修改通过 Pull Request 合并到 `main`。推送到 `main` 后会自动触发 **Build and deploy personal website** 工作流。
4. 等待 Actions 中的 `build`、`deploy` 均成功，再打开部署记录中的网址。

也可以在包含本项目工作流的 `main` 分支上手动运行工作流。PR 和 `init` 分支只检查、不发布。若首次部署先于 Pages 配置而失败，完成配置后重新运行即可。

工作流会自动读取 Pages 地址，并生成被 Git 忽略的 `_config.pages.yml`。本仓库默认使用 `/homepage` 路径前缀，通常不必手动修改 `_config.yml` 中的 `url` 或 `baseurl`。构建产物通过 GitHub Actions 发布，无需建立 `gh-pages` 分支。

完整步骤和故障排查见 [发布指南](docs/QUICKSTART-ZH.md)。本地构建通过不代表远程部署已完成。

## 构建与检查

在装有 Ruby/Bundler 的环境中运行：

```sh
bundle exec jekyll build
bundle exec ruby scripts/check-site.rb
```

本机使用便携环境时：

```powershell
$rubyRunner = 'E:\Gitcodes\paper-search\tools\ruby-runtime\run-ruby.ps1'
& $rubyRunner bundle exec jekyll build
& $rubyRunner ruby scripts/check-site.rb
```

GitHub Actions 还会按正式地址的 `/homepage` 前缀检查内部链接。`Gemfile.lock` 固定 Ruby 依赖版本，应随源码提交；`_site/`、`_config.pages.yml`、`node_modules/`、本地 Ruby 环境和 `output/` 无需提交；`assets/papers/` 中的论文全文和 `assets/teaching/` 中的教材、课件和作业不得提交。

从默认本地配置完成构建后，可运行 `python scripts/package.py` 生成源码 ZIP 和离线预览 ZIP，输出位于被 Git 忽略的 `output/`。

## 资料与许可

- [内容维护指南](docs/CONTENT-GUIDE-ZH.md)
- [发布指南](docs/QUICKSTART-ZH.md)
- [内容与素材来源](docs/SOURCES.md)
- [验证记录](docs/VALIDATION.md)

al-folio 模板采用 MIT 许可证，原始许可证见 [LICENSE](LICENSE)。个人内容及照片的权利归原权利人所有。
