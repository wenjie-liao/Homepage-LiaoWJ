# Wenjie Liao · 廖文杰的学术主页

中英双语个人学术网站，介绍人工智能驱动的结构设计与优化研究，包括建筑结构生成式设计和结构抗震韧性。网站基于 [al-folio](https://github.com/alshedivat/al-folio) v1 和 Jekyll，通过 GitHub Actions 发布到 GitHub Pages。

- 公开源码：[wenjie-liao/homepage](https://github.com/wenjie-liao/homepage)
- 网站地址：[英文首页](https://wenjie-liao.github.io/homepage/) · [中文首页](https://wenjie-liao.github.io/homepage/zh/)；部署状态以仓库 Actions 记录为准。
- 内容包括首页、三个研究专题、23 篇论文、软件与模型、4 门课程与 33 个教学主题、学术经历及联系方式。
- 支持对应页面的中英文切换、移动端布局和深浅色切换。首页学术入口包括学校中文主页、Google Scholar、GitHub 和 ORCID。

## 本地预览

在本仓库根目录操作，使用 Ruby 3.3、Bundler 和锁定的依赖：

```sh
bundle install
bundle exec jekyll serve --host 127.0.0.1 --port 4000
```

打开 [http://127.0.0.1:4000/](http://127.0.0.1:4000/)。正文修改会自动重建；修改 `_config.yml` 后需重启服务。

Windows 也可使用预览脚本，需要 Python 3 和可用的 Bundler：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\preview.ps1 -Rebuild
```

默认地址是 [http://127.0.0.1:4173/](http://127.0.0.1:4173/)，可用 `-Port 4174` 更换端口，按 `Ctrl+C` 停止。修改源文件后再次运行带 `-Rebuild` 的命令；省略该参数会复用已有构建。使用便携 Ruby 时，以 `-RubyRunner "<Ruby 启动脚本路径>"` 显式指定本机脚本，路径只在本地使用。Node.js 仅用于可选的格式化工具。

## 内容维护

| 内容 | 文件或目录 |
| --- | --- |
| 中英文首页简介 | `_pages/zh/home.md`、`_pages/about.md` |
| 研究总览与专题 | `_pages/research.md`、`_projects/`、`_pages/zh/` |
| 论文数据与方法图 | `_data/publications.json`、`assets/img/publications/` |
| 教学双语内容 | `_data/teaching.json` |
| 软件与模型 | `_pages/software.md`、`_pages/zh/software.md` |
| 学术经历 | `_pages/cv.md`、`_pages/zh/about.md` |
| 联系方式与学术链接 | `_pages/contact.md`、`_pages/zh/contact.md`、`_data/socials.yml` |
| 网站配置与样式 | `_config.yml`、`_sass/_personal.scss`、`_sass/_bilingual.scss` |

英文页面从 `/` 开始，中文页面位于 `/zh/`。同一页面的两个版本共享 `translation_key`，分别设置 `lang: en` 和 `lang: zh`；内部链接通过 `relative_url` 适配项目站前缀。

论文页面与研究专题共同读取 `_data/publications.json`，`_bibliography/papers.bib` 为引用导出副本。三个专题当前分别收录 18、5、6 篇，可交叉归类。论文年份采用正式期刊卷期年份，按 `sort_key` 降序排列。教学页面共同读取 4 门课程、33 个主题的双语数据。详见 [内容维护指南](docs/CONTENT-GUIDE-ZH.md)。

## 检查与打包

从仓库根目录运行，隐私检查需要 Python 3：

```sh
python scripts/check-privacy.py
bundle exec jekyll build
bundle exec ruby scripts/check-site.rb
python scripts/check-privacy.py --site _site
```

隐私检查默认扫描当前跟踪文件和暂存变更；构建检查覆盖双语页面、内部链接、论文与课程展示。新克隆应启用仓库的提交前检查：

```sh
git config core.hooksPath .githooks
```

在类 Unix 环境中，如脚本不可执行，运行 `chmod +x .githooks/pre-commit`。该钩子在本地提交前运行隐私检查。GitHub Actions 也在构建前和上传产物前检查隐私，并按正式站点前缀验证链接；CI 只能阻止后续部署，无法撤回已推送到公开仓库的内容。

从默认本地配置完成构建后，运行 `python scripts/package.py` 可在 `output/` 生成源码和离线预览 ZIP。源码包仅收录通过检查的 Git 跟踪文件，新增的公开文件须先审核并加入 Git；隐私检查脚本自身未被跟踪时，打包会拒绝执行。打包脚本还会检查实际构建产物。`Gemfile.lock` 应随源码提交；本地依赖、缓存、生成配置、构建目录和压缩包不提交。

## 公开范围与隐私

本仓库为 public。公开内容限于已确认的学术简介、任职与教育经历、研究成果、课程概述、学术账号、机构联系方式和获准使用的图片。个人电话、私人邮箱、家庭地址、证件、账号凭据、个人电脑路径及未公开材料不得写入源码、文档、提交说明或图片元数据。

论文全文放在本地 `assets/papers/`，教材、课件和作业放在 `assets/teaching/`；旧课件目录 `assets/teach/` 同样受保护。私有笔记可放在被忽略的 `private/`，核验产物保存在 `output/`。这些内容由 Git 忽略、Jekyll 排除及打包规则共同保护。不要用 `git add -f` 绕过规则，或将私有材料移到公开资源目录。网页仅提供论文元数据、原创简介、方法图与 DOI，以及课程简介和大纲。

`.gitignore` 不会删除已跟踪文件或旧提交。需要检查本地可达历史时另行运行：

```sh
python scripts/check-privacy.py --history
```

历史检查可能报告先前提交中的旧记录，修改当前文件不会清除它们。自动扫描不能代替人工审阅，也不能证明远程副本、克隆、分叉或缓存已清除；若曾提交凭据，应立即撤销或轮换，并单独处理受影响的历史。公开提交应使用 GitHub 提供的隐私邮箱或明确用于公开的工作邮箱。

## 发布到 GitHub Pages

本仓库已有发布工作流，无需重新初始化：

1. 在仓库 **Settings → Pages → Build and deployment** 中将 **Source** 设为 **GitHub Actions**。
2. 审阅修改并完成本地检查，通过 Pull Request 合并到 `main`，或按仓库协作规则更新部署分支。
3. 等待 **Build and deploy personal website** 的 `build`、`deploy` 均成功，检查中英文页面。

工作流发布 `main`／`master` 上的推送和手动运行；Pull Request、`init` 分支以及其他分支的手动运行仅检查。发布地址由工作流生成的 `_config.pages.yml` 配置，项目站默认前缀为 `/homepage`，无需另建 `gh-pages` 分支。详见 [发布指南](docs/QUICKSTART-ZH.md)。

## 资料与许可

- [内容维护指南](docs/CONTENT-GUIDE-ZH.md)
- [发布指南](docs/QUICKSTART-ZH.md)
- [Google、Bing、百度收录操作步骤](docs/SEARCH-ENGINES-ZH.md)
- [内容与素材来源](docs/SOURCES.md)
- [验证说明与记录](docs/VALIDATION.md)

al-folio 模板采用 MIT 许可证，见 [LICENSE](LICENSE)。个人内容及照片的权利归原权利人所有。
