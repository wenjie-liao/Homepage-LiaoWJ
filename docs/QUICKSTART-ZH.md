# 发布到 GitHub Pages

本项目是 [wenjie-liao/homepage](https://github.com/wenjie-liao/homepage) 公开仓库中的双语学术网站。以下命令均从本仓库根目录执行，无需固定的本机路径或重新初始化模板。线上状态以仓库 Actions 的部署记录和实际访问结果为准。

## 发布流程

1. 在 **Settings → Pages → Build and deployment** 中将 **Source** 设为 **GitHub Actions**。
2. 审阅待提交内容，完成下文的源码隐私检查、构建和产物检查；确认公开提交使用合适的作者邮箱。
3. 按仓库协作规则提交修改并合并到 `main`。推送到 `main` 或 `master` 会触发发布；也可在 **Actions → Build and deploy personal website → Run workflow** 选择相应分支。
4. 等待 `build` 和 `deploy` 均成功，再打开部署记录中的网址。

默认网站地址为 [英文首页](https://wenjie-liao.github.io/homepage/) 与 [中文首页](https://wenjie-liao.github.io/homepage/zh/)。发布后核对导航、对应页面语言切换、论文方法图和教学大纲。当前有 23 篇论文，三个主题分别收录 18、5、6 篇，可交叉归类；教学页有 4 门课程、33 个主题。About 的英文源文件是 `_pages/cv.md`，网页地址为 `/about/`。

Pull Request 和 `init` 分支只构建检查；其他分支上的手动运行也不发布。仓库无需 `gh-pages` 分支。工作流使用 GitHub 自动提供的 `GITHUB_TOKEN`，网站源码中不保存个人访问令牌。

## 地址配置

工作流读取 Pages 地址，由 `scripts/pages-config.rb` 生成被 Git 忽略的 `_config.pages.yml`，覆盖正式站点的 `url` 和 `baseurl`。本项目默认使用 `/homepage` 前缀；源码中的内部链接须使用 `relative_url`，避免写死预览域名或部署前缀。

`_config.pages.yml` 无需手工编辑或提交。若配置自定义域名，应先完成 Pages 和 DNS 设置，再重新运行工作流。配置方法见 [GitHub 自定义域名文档](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages)。

## 本地构建与检查

安装 Ruby 3.3、Bundler 和 Python 3 后运行；新克隆先启用提交前隐私检查：

```sh
bundle install
git config core.hooksPath .githooks
python scripts/check-privacy.py
bundle exec jekyll build
bundle exec ruby scripts/check-site.rb
python scripts/check-privacy.py --site _site
```

类 Unix 环境中，如提交钩子不可执行，可运行 `chmod +x .githooks/pre-commit`。本地钩子在提交前检查；CI 无法撤回已推送的公开内容。

持续预览可用 `bundle exec jekyll serve --host 127.0.0.1 --port 4000`。Windows 也可运行 `powershell -ExecutionPolicy Bypass -File .\scripts\preview.ps1 -Rebuild`，使用系统 Bundler，或通过 `-RubyRunner "<Ruby 启动脚本路径>"` 指定便携环境，详见 [README](../README.md)。GitHub Actions 在 Linux 上独立安装依赖，不需要上传本地运行环境。

`Gemfile.lock` 固定依赖版本，应随源码提交。从 Windows 更新依赖时保留 Linux 平台记录；必要时运行 `bundle lock --add-platform x86_64-linux`，再验证构建。

论文网页事实只在 `_data/publications.json` 维护，BibTeX 为引用导出副本。修改日期时同步维护 `sort_key`；教学双语内容统一维护在 `_data/teaching.json`。文件对应关系见 [内容维护指南](CONTENT-GUIDE-ZH.md)。

## 公开仓库的隐私边界

论文全文、教材、课件、作业、私有笔记和核验产物只保存在被忽略并排除发布的目录。当前跟踪情况可检查：

```sh
git ls-files -- assets/papers assets/teach assets/teaching private output
```

结果应为空。构建目录和交付 ZIP 也不得包含这些材料。不要以强制添加或移动目录的方式绕过排除规则；图片、PDF、简历等附件发布前还需人工检查正文及元数据。

默认隐私检查处理当前跟踪文件和暂存变更；`python scripts/check-privacy.py --history` 单独扫描本地可达历史。`.gitignore` 和修改当前文件均不能消除历史记录。若历史存在敏感信息，应单独处理；凭据需立即撤销或轮换。检查范围不覆盖外部克隆、分叉及缓存，不能据此承诺全网已清除。

## 常见问题

| 现象 | 检查位置 |
| --- | --- |
| Actions 没有运行 | 推送分支是否在工作流触发范围内，工作流文件是否已提交，Actions 是否启用 |
| 隐私检查失败 | 按报告中的文件与类型审阅；删除敏感内容，不在公开日志中复述原值 |
| 读取 Pages 设置时报错 | Settings → Pages 的 Source 是否为 GitHub Actions |
| 依赖安装失败 | Ruby 安装日志与 `Gemfile.lock`；保留版本锁后定位问题 |
| 项目站图片或链接失效 | 内部链接是否使用 `relative_url`，是否使用生成的部署配置构建 |
| 构建成功但没有上线 | 独立的 `deploy` 任务是否执行成功，当前是否为部署分支 |
| 浏览器仍显示旧内容 | 最新部署是否完成，必要时刷新浏览器缓存 |

工作流配置参见 [GitHub 自定义 Pages 工作流说明](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) 和 [Ruby 安装 Action](https://github.com/ruby/setup-ruby)。
