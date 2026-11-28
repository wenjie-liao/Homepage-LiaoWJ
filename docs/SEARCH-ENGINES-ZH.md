# Google、Bing、百度搜索收录操作步骤

目标是让搜索引擎发现并收录公开学术主页。站长平台验证、提交网址、搜索结果收录是三个不同阶段；验证成功或提交成功不等于已经收录。本指南按 2026-11-28 核查的官方说明编写，登录后的按钮和配额以各平台实际显示为准。

## 1. 本站要用的网址

| 用途 | 地址 |
| --- | --- |
| 英文首页、Google/Bing 项目属性 | `https://wenjie-liao.github.io/homepage/` |
| 中文首页 | `https://wenjie-liao.github.io/homepage/zh/` |
| 站点地图 | `https://wenjie-liao.github.io/homepage/sitemap.xml` |
| 主机根目录 | `https://wenjie-liao.github.io/` |

不要提交 GitHub 源码仓库网址、分支页面或本地预览地址。本次检查正式英文首页和 sitemap 均返回 HTTP 200，根目录 `/robots.txt` 返回 404；这是当时的响应，不能代表搜索引擎已经完成抓取。

网站已有静态页面、规范链接（canonical）、中英文对应链接（hreflang）及 Jekyll 自动生成的 sitemap。本分支增加三家平台的 HTML 验证配置、首页中英文摘要、404 的 `noindex` 和 sitemap 排除，以及部署前 SEO 检查。配置为空时不输出验证标签。

## 2. 先取得验证标识，再部署

在下面的平台步骤中选择 HTML 标签验证后，平台会给出类似代码：

```html
<meta name="google-site-verification" content="平台为你生成的标识">
```

只复制 `content` 引号内的值，填入仓库根目录 `_config.yml` 已有的配置段，不要复制整段 HTML，也不要把示例文字作为真实标识：

```yaml
search_engine_verification:
  google: ""
  bing: ""
  baidu: ""
```

| 平台标签 | 填入配置项 |
| --- | --- |
| `google-site-verification` | `search_engine_verification.google` |
| `msvalidate.01` | `search_engine_verification.bing` |
| `baidu-site-verification` | `search_engine_verification.baidu` |

未使用的平台保留空字符串。Bing 从 Google 导入时通常不需要单独填写 `bing`。这些标识本来就要出现在公开网页中供平台读取，可以提交到公开仓库；登录密码、OAuth 凭据和 API 推送 token 不属于这些标识，不能填入或提交。

本项目统一通过 `_includes/search-engine-metadata.html` 输出标签。不要再同时开启主题自身的 `enable_google_verification`／`enable_bing_verification`，以免生成重复标签。百度配置只影响本项目页面，不能替代主机根站点的验证，见第 5 节。

完成填写后：

1. 在当前功能分支审阅变更，运行源码检查和生产路径构建。
2. 提交并推送功能分支，创建以 `main` 为目标的 Pull Request。
3. 等待 PR 检查通过，合并到 `main`。
4. 等待 **Build and deploy personal website** 工作流的 `build` 和 `deploy` 成功。仅推送功能分支不会更新正式网站。
5. 打开正式首页，使用“查看网页源代码”，搜索对应的 meta 名称并确认其值正确，然后回平台点击验证。

验证成功后继续保留标签，平台可能再次检查所有权。[Google 所有权验证说明](https://support.google.com/webmasters/answer/9008080?hl=en)

## 3. Google Search Console

1. 打开 [Google Search Console](https://search.google.com/search-console)，登录自己的 Google 账号。
2. 在资源选择器中选择“添加资源”，选择 **网址前缀 / URL prefix**。
3. 填入 `https://wenjie-liao.github.io/homepage/`，保留 HTTPS 和末尾斜杠。这个属性包含 `/homepage/zh/`，无需为了中文首页再建属性。当前 GitHub 提供的域名没有可由你修改的 DNS，使用网址前缀验证。[属性范围与验证方式](https://support.google.com/webmasters/answer/34592?hl=en)
4. 选择 **HTML 标记 / HTML tag**，复制 `content` 值到 `search_engine_verification.google`。
5. 按第 2 节部署，确认正式首页源代码有 `google-site-verification`，回到 Search Console 点击“验证”。
6. 验证后进入 **站点地图 / Sitemaps**，提交 `https://wenjie-liao.github.io/homepage/sitemap.xml`。若输入框前已固定显示完整项目网址，只填 `sitemap.xml`；检查最终拼接地址没有重复的 `/homepage/`。[站点地图操作说明](https://support.google.com/webmasters/answer/7451001?hl=en)
7. 在顶部“网址检查”依次检查英文首页和中文首页，运行“测试实际网址”，根据检测结果处理抓取问题，再点“请求编入索引”。其他内容由 sitemap 引导发现即可。[网址检查工具](https://support.google.com/webmasters/answer/9012289/)
8. 后续查看站点地图处理状态、网页索引报告和这两个 URL 的索引状态。对同一网址反复请求不会加速抓取；Google 不保证固定收录日期。[请求重新抓取说明](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl)

## 4. Bing Webmaster Tools

推荐在 Google 验证后导入：

1. 打开 [Bing Webmaster Tools](https://www.bing.com/webmasters/)，登录自己的账号。
2. 选择 **从 Google Search Console 导入 / Import from Google Search Console**。
3. 按页面提示授权读取 GSC 站点信息，选中 `https://wenjie-liao.github.io/homepage/`。导入可验证网站并带入 sitemap；完成后核对属性和 sitemap 地址。[Bing 添加、导入与验证说明](https://www.bing.com/webmasters/help/add-and-verify-site-12184f8b)
4. 进入 **Sitemaps**；若列表没有上述 sitemap，选择提交并填写其完整网址。[Bing sitemap 帮助](https://www2.bing.com/webmasters/help/sitemaps-3b5cf6ed)
5. 在 **URL Inspection** 检查英文和中文首页，查看索引结果及 Live URL 检测。按后台提供的请求索引入口操作；也可在 **URL Submission / Submit URLs** 每行填写一个首页网址后提交。[网址检查](https://www.bing.com/webmasters/help/url-inspection-55a30305)、[URL 提交](https://www.bing.com/webmasters/help/URL-Submission-62f2860b)

如果不希望关联 Google 账号，可手工添加同一项目网址，选择 HTML meta 验证。将 `<meta name="msvalidate.01" content="…">` 的 `content` 值填入 `search_engine_verification.bing`，部署并验证。Bing 支持网站子路径属性。[Bing 站点范围说明](https://www.bing.com/webmasters/help/add-and-verify-site-12184f8b)

本主页首次提交用 sitemap 和手工网址提交即可，不需要配置 API key 或自动推送服务。

## 5. 百度搜索资源平台

百度需先解决“验证的是哪一个首页”。官方要求文件验证位于域名根目录、HTML 标签位于被验证站点首页的 `<head>`。尚未确认当前登录表单是否接受 `/homepage/` 作为独立站点；不要把 Google/Bing 的子路径支持套用到百度。[官方验证说明](https://ziyuan.baidu.com/college/courseinfo?id=267&page=21)

### 添加和验证

1. 打开 [百度搜索资源平台](https://ziyuan.baidu.com/)，登录后进入 **用户中心 → 站点管理 → 添加网站**。
2. 使用实际网站的 HTTPS 协议，按表单要求填写网址。
3. 如果平台接受 `https://wenjie-liao.github.io/homepage/` 且要求验证该首页，选 HTML 标签验证，将 `content` 值填入 `search_engine_verification.baidu`，按第 2 节部署，再回平台验证。
4. 如果平台只接受域名 `https://wenjie-liao.github.io/`，则必须在这个根站点完成验证。仅修改当前项目的 `/homepage/` 首页不够。

对第 4 种情况，可按以下步骤准备根站点；这是条件方案，本次没有创建或修改另一个仓库：

1. 查看自己是否已有 `wenjie-liao.github.io` 用户站点仓库；有则使用现有仓库和部署方式，没有则创建同名仓库。用户站点的仓库命名规则见 [GitHub Pages 官方说明](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)。
2. 对新建的简单静态根站点，可在根目录添加 `index.html`，展示公开姓名和指向 `/homepage/` 的链接；进入 Settings → Pages，使用 `main` 分支的 `/(root)` 发布。已有站点沿用其发布设置。
3. 若选 HTML 标签验证，把百度给出的标签放入这个根首页的 `<head>`；若选文件验证，把下载文件按原文件名和内容放入根站点发布目录。
4. 等待发布成功，确认百度给出的验证地址可直接访问。例如域名根文件应位于 `https://wenjie-liao.github.io/baidu_verify_….html`，而不是 `/homepage/baidu_verify_….html`。实际扩展名以下载文件为准。
5. 回百度点击验证，成功后保留验证内容。原有学术主页继续在 `/homepage/` 发布；根站点可以链接到它，无需迁移当前仓库。

根站点验证位置与项目目录不匹配的判断，是依据百度验证位置要求和 GitHub Pages 部署结构作出的推论。实际添加网址规则和验证失败原因以平台反馈为准。

### 提交公开页面

验证成功后，进入 **搜索服务 → 资源提交 → 普通收录**。先使用可用的手动提交入口，每行一个正式网址，例如：

```text
https://wenjie-liao.github.io/homepage/
https://wenjie-liao.github.io/homepage/zh/
https://wenjie-liao.github.io/homepage/research/
https://wenjie-liao.github.io/homepage/zh/research/
https://wenjie-liao.github.io/homepage/publications/
https://wenjie-liao.github.io/homepage/zh/publications/
```

如果该站点后台显示可用的 Sitemap 入口及配额，再提交 `https://wenjie-liao.github.io/homepage/sitemap.xml`。本站生成的是直接列出页面的 `<urlset>`。不要假定新站一定拥有 Sitemap 或快速抓取权限；配额和入口以登录后实际显示为准。[普通收录指南](https://ziyuan.baidu.com/college/articleinfo?id=3329)、[Sitemap 配额说明](https://ziyuan.baidu.com/college/articleinfo?id=3134)

提交后查看“索引量”“抓取诊断”“抓取异常”。百度明确说明提交不保证收录，不能把工具显示“提交成功”当作已能搜索到。[普通收录说明](https://ziyuan.baidu.com/linksubmit/index)

## 6. robots.txt 与公开范围

爬虫读取的是 `https://wenjie-liao.github.io/robots.txt`。Jekyll 在本项目生成的 `/homepage/robots.txt` 不能作为主机根规则生效；可以直接向站长平台提交 sitemap，不必为此迁移网站。[Google robots 位置规范](https://developers.google.com/crawling/docs/robots-txt/create-robots-txt)、[百度 robots 手册](https://ziyuan.baidu.com/college/courseinfo?id=267&page=10)

若后续管理根站点，可在根站点放置以下文件；有现有 robots 时先检查其用途再合并规则：

```text
User-agent: *
Allow: /
Sitemap: https://wenjie-liao.github.io/homepage/sitemap.xml
```

本次根 robots 返回 404，不等于禁止抓取。robots 也不负责保护私人信息；论文原文、课件、私有笔记和凭据仍通过 Git 忽略、构建排除及打包检查保持不公开。公开工作邮箱可以保留。不要把 API 推送 URL 中的 token 放进 sitemap、配置、文档或日志。

## 7. 构建与上线核验

仓库根目录使用 Ruby/Bundler 和 Python 运行。PowerShell 示例：

```powershell
$env:GITHUB_REPOSITORY = 'wenjie-liao/homepage'
python scripts/check-privacy.py
bundle exec ruby scripts/pages-config.rb
bundle exec jekyll build --config '_config.yml,_config.pages.yml' --destination _site_project
bundle exec ruby scripts/check-site.rb _site_project /homepage
python scripts/check-seo.py _site_project https://wenjie-liao.github.io/homepage/
python scripts/check-privacy.py --site _site_project
```

`check-seo.py` 检查 sitemap、canonical、双语对应链接、摘要、404 的 noindex，以及验证标签是否重复或为空；它不会替你登录平台，也不能验证平台是否已接受标识。GitHub Actions 在上传网站产物前执行同一检查。

上线后分别确认：正式中英文首页和 sitemap 可以访问；源代码中的验证标识为自己的值；平台显示所有权验证通过；sitemap 被读取；URL 检查报告实际收录情况。`site:wenjie-liao.github.io/homepage` 以及“廖文杰 人工智能 结构设计”等检索可作辅助观察，不能代替站长后台的索引诊断。
