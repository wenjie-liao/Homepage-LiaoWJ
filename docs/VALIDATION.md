# Validation · 2026-11-27

- Jekyll 4.4.1 build passed using the pinned al-folio core 1.0.15.
- Personal-site root deployment and `/personal-site` project deployment both passed: 10 HTML pages, 235 local references.
- No unresolved Liquid expressions or sample Einstein profile text in the built HTML.
- Prettier passed after formatting.
- al-folio upgrade audit: 0 blocking and 0 non-blocking findings. The main Sass entry override is acknowledged.
- An isolated temporary site with synthetic BibTeX records verified publication rendering, selected-publication filtering, abstracts, code links, and BibTeX display. Those records are not in the personal site or deliverable archives.
- Browser checks verified home/research/publications navigation, a 390 px mobile viewport, the mobile navigation menu, and light/dark mode. No horizontal overflow was observed in the checked mobile page.
- GitHub Pages URL configuration passed personal-site, project-site, and custom-domain cases.

The source has been prepared for the existing `wenjie-liao/homepage` repository on the `init` branch. Its remote default branch is `main`. The workflow checks `init` and pull requests, and publishes pushes or manual runs on `main`/`master`.

Migration checks in `E:\Gitcodes\Homepage-LiaoWJ` on 2026-11-27:

- Copied 40 editable source files; the existing `.git` metadata was unchanged during the copy, with the `init` branch and origin retained.
- The relocated `scripts/preview.ps1 -Rebuild` found the sibling portable Ruby runtime and successfully built the site. The HTTP preview returned 200 with the expected profile content.
- The local root build passed 10 HTML pages and 235 local references.
- The production build using generated `url: https://wenjie-liao.github.io` and `baseurl: /homepage` passed 10 HTML pages and 225 local references.
- Git ignored `_site/`, `_site_project/`, and `_config.pages.yml` as intended.

No remote GitHub Actions run or public deployment has been verified. Local browser checks do not establish overseas network performance.


## Publication and teaching update · 2026-11-28

- Active working directory: `E:\Gitcodes\Homepage-LiaoWJ`.
- Read all 23 supplied papers and independently cross-checked titles, author order, affiliations, DOI, and journal years. Each record has an original English summary and one visually inspected method-figure crop with attribution.
- Publications contains 23 unique records; research listings contain 18 generative-design, 7 structural-optimization, and 5 seismic-resilience records, with intentional cross-listing.
- Journal year grouping and within-year chronological sort keys were verified. Two supplied Engineering Structures articles carry 2027 issue years; only explicit online dates are displayed.
- Research overview removed; platform spelling unified as AI-structure Copilot. Teaching includes the verified GS30106003 graduate course and eight topics from local source slides; no unverified semester or credit information is presented.
- Local build: 11 HTML pages and 446 local references passed. Production build at `/homepage`: 11 HTML pages and 435 local references passed.
- Git ignores all 23 paper PDFs; none were tracked or present in local Git history. Original source directories are excluded from Jekyll and ZIP packaging. Private teaching slides also remain local.
- Browser QA checked desktop and 390px mobile layout, author-affiliation disclosure, mobile navigation, dark mode, theme membership, and Teaching. Checked layouts had no horizontal overflow.
- Local preview uses port 4174 because an older preview still serves port 4173.
- No commit, push, or remote deployment was performed during this update.


## Bilingual teaching update · 2026-11-28

- Reviewed 44 local teaching materials across four courses: two undergraduate and two graduate. Course data contains 33 bilingual topics, supported by the supplied PDFs, slides, interactive HTML lessons, and assignment documents. Public pages contain original summaries and outlines only.
- Added `/assets/teaching/` to Git ignore rules, Jekyll exclusions, and both source/preview archive exclusions. Existing private paper and legacy slide exclusions remain active.
- Implemented 11 matching Chinese pages under `/zh/` with static language switches, locale-specific navigation, `lang`, and `hreflang`. All 23 publications have Chinese titles, summaries, and figure captions; official English titles and author records are retained.
- Homepage and footer profile links are Chinese faculty homepage, GitHub, and ORCID. Removed the English faculty-profile link from generated pages.
- Chinese name text uses a CJK sans-serif font stack; English name/location use the site's standard Latin font stack. The Chinese homepage includes the location in Chinese.
- Root build passed 22 HTML pages and 958 internal references. Production `/homepage` build passed 22 pages and 892 internal references. Checks cover exact language counterparts, required bilingual pages, publication membership, course coverage, private directory exclusion, and private source-link exclusion.
- Browser checks verified English/Chinese home and course switching, 23 Chinese publication entries, course-outline disclosure, the 640px navigation fix, 390px mobile layout, and 1024px desktop navigation. Checked layouts had no horizontal overflow.
- No commit, push, or remote deployment was performed.
