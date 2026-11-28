# 发布到 GitHub Pages

本项目是已经个性化的 al-folio 学术网站源码。GitHub Pages 工作流已准备好；是否已经上线，以仓库 Actions 中成功的部署记录和实际访问结果为准。本地构建成功不代表网站已经发布。

## 首次发布

1. 使用已经创建的 [wenjie-liao/homepage](https://github.com/wenjie-liao/homepage) 仓库。本地目录为 `E:\Gitcodes\Homepage-LiaoWJ`，当前开发分支为 `init`，远程默认分支为 `main`。
2. 检查本项目源码，提交并推送 `init` 分支，包含 `.github/workflows/deploy.yml` 等隐藏目录。`init` 的推送会触发构建和链接检查，不会发布网站。
3. 打开仓库 **Settings → Pages → Build and deployment**，将 **Source** 设为 **GitHub Actions**。本项目使用 Actions 直接发布构建产物，不使用 `gh-pages` 分支。
4. 通过 Pull Request 将 `init` 合并到 `main`。推送到 `main` 会自动构建和发布；也可以在 **Actions → Build and deploy personal website → Run workflow** 中选择包含工作流的 `main` 分支并运行。
5. 等待 `build`、`deploy` 都成功，打开部署记录中的网址。未配置自定义域名时，预期地址为 [https://wenjie-liao.github.io/homepage/](https://wenjie-liao.github.io/homepage/)。检查 Home、Research、Publications、Software、Teaching、About 和 Contact 页面；确认 23 篇论文和方法图正常展示，三个研究主题分别筛选出 18、5、6 篇（可交叉归类）。Teaching 应展示《工程结构智能设计》（GS30106003）的课程简介和八个专题，不提供课件下载。About 的地址是 `/about/`，其内容文件为 `_pages/cv.md`。

首次推送可能发生在 Pages 设置完成之前，导致读取 Pages 设置这一步失败；完成第 3 步后重新运行即可。若仓库要求环境审批，按 GitHub 页面提示完成 `github-pages` 环境审批。

默认使用 GitHub 自动提供的 `GITHUB_TOKEN`，不需要在网站文件中保存个人访问令牌。访问公开网站的读者无需 GitHub 账号。免费托管要求公开源码仓库；不要把未公开资料、密码或私密文件放进仓库。

## 地址如何配置

发布工作流会读取 GitHub Pages 的实际地址，由 `scripts/pages-config.rb` 临时生成 `_config.pages.yml`，覆盖正式网站的 `url` 和 `baseurl`。因此不用在源码中猜测用户名，也能适配个人站、项目站及以后配置的独立域名。

`_config.pages.yml` 是生成文件，不需要手工编辑或提交。PR 和 `init` 分支只检查构建，不发布；`main` 或 `master` 分支上的推送和手动工作流可以发布。其他分支上的手动工作流只做构建检查。

本仓库属于项目站，默认地址包含 `/homepage/`。将来如果改用名为 `wenjie-liao.github.io` 的仓库，默认网址才会是站点根目录；地址生成脚本也支持这种情况。

独立域名可以以后再添加：先在 GitHub Pages 设置中配置域名和 DNS，再重新运行工作流。配置过程参见 [GitHub 自定义域名文档](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages)。

## 日常更新

直接修改内容文件，提交并推送到部署分支即可。论文只在 `_data/publications.json` 维护网页事实；`_bibliography/papers.bib` 为引用导出副本。方法图位于 `assets/img/publications/`，首页位于 `_pages/about.md`，研究专题位于 `_projects/`，教学栏目位于 `_pages/teaching.md`。详细对应关系见 [内容维护指南](CONTENT-GUIDE-ZH.md)。

论文年份采用正式期刊卷期年份，已核实的 `online_date` 才展示；未知月日时的 `YYYY-01-01` 仅为排序占位。列表按 `sort_key` 降序排列，其值为 `期刊年-上线日期`，缺少 `online_date` 时改用 `date`；修改日期后需同步更新该键。更新后检查 Publications 和研究专题中的同一条论文，确认展示一致。

如果某次更新的构建失败，已成功发布的旧版本通常会继续提供服务；先在 Actions 中查看失败步骤，修复后再提交。

## 论文全文和课程课件的本地保留

论文全文和课程课件分别留在项目本地的 `assets/papers/`、`assets/teaching/`，不上传到 GitHub，也不提供网站下载。两个目录均由 Git 忽略、Jekyll 构建排除及打包脚本排除。提交前可在 `E:\Gitcodes\Homepage-LiaoWJ` 检查：

```powershell
git ls-files -- assets/papers assets/teach
```

正常结果为空，表示没有已跟踪的论文全文或课件。构建后的 `_site/assets/papers/`、`_site/assets/teaching/` 也不应存在；源码和预览 ZIP 均不应包含这些原始材料或 `output/paper-review/` 中的审校文件。不要通过移动目录或强制添加来绕过排除规则。公开的论文页面提供元数据、原创简介、方法图和 DOI 链接，教学页面提供课程简介和大纲。

## 本地构建

在装有 Ruby 3.3 和 Bundler 的环境中，从项目根目录运行：

```sh
bundle install
bundle exec jekyll serve --host 127.0.0.1 --port 4000
```

然后打开终端给出的本地地址。只生成静态页面时运行：

```sh
bundle exec jekyll build
```

Windows 可运行 `powershell -ExecutionPolicy Bypass -File .\scripts\preview.ps1 -Rebuild`，脚本会查找系统 Bundler 或相邻 `paper-search` 项目下的便携运行环境，也可通过 `-RubyRunner` 指定位置，详见 [README](../README.md)。GitHub Actions 在 Linux 上独立安装依赖，不需要上传本地运行环境、`vendor`、`node_modules` 或 `_site`。

`Gemfile.lock` 固定依赖版本，应一并提交；如果从 Windows 更新依赖，须保留 Linux 平台的锁定依赖，以便 GitHub 构建。必要时在有 Bundler 的环境中运行 `bundle lock --add-platform x86_64-linux`，再构建验证。

## 排查常见问题

| 现象                         | 检查位置                                                                                               |
| ---------------------------- | ------------------------------------------------------------------------------------------------------ |
| Actions 没有运行             | 推送分支是否为 `init`、`main` 或 `master`，`.github/workflows/deploy.yml` 是否已上传，Actions 是否启用 |
| 读取 Pages 设置时报错        | Settings → Pages 的 Source 是否为 GitHub Actions                                                       |
| 依赖安装失败                 | Actions 中 Ruby 安装日志与 `Gemfile.lock`；不要直接删除版本锁后盲目升级                                |
| 网址带项目名时图片或链接失效 | 内部链接是否使用 `relative_url`，是否绕过了部署地址生成脚本                                            |
| 已完成构建但没有上线         | 查看独立的 `deploy` 任务；PR 和 `init` 不部署，需要合并到 `main`                                       |
| 内容更新了但浏览器仍显示旧版 | 等待最新部署完成后刷新，必要时强制刷新浏览器缓存                                                       |

工作流基于 [GitHub 自定义 Pages 工作流说明](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) 和 [Ruby 安装 Action](https://github.com/ruby/setup-ruby)，核查日期：2026-11-27。

网站现有中文 `/zh/` 与英文原路径两个版本；导航中的语言切换保持当前栏目。部署时同时检查两种语言的论文页与教学页；教学源材料包含多种格式，整个 `assets/teaching/` 目录均不得进入公开仓库或构建产物。
