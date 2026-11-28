# Content and asset provenance

Personal-profile sources were checked on 2026-11-27. Publication metadata and method figures were reviewed against 23 locally supplied papers on 2026-11-28. Teaching summaries were checked against the four locally supplied course folders (44 source files) on 2026-11-28. Future changes should be checked against the relevant source and confirmed with Wenjie Liao.

| Content | Source |
| --- | --- |
| English name, affiliation, research interests, appointments, education, academic service, AIstructure association | [University English profile](https://faculty.swjtu.edu.cn/liaowj/en/index.htm) |
| Chinese name and institutional identity | [University profile](https://faculty.swjtu.edu.cn/liaowj/) |
| Email | [University publication record](https://faculty.swjtu.edu.cn/liaowj/en/lwcg/856572/content/25765.htm) and [published paper](https://journals.sagepub.com/doi/10.1177/13694332251353614) |
| GitHub account and research code | [GitHub profile](https://github.com/wenjie-liao) and [StructGAN-Hybrid paper](https://doi.org/10.1002/eqe.3862) |
| ORCID | [StructGAN-Hybrid paper](https://doi.org/10.1002/eqe.3862) and [data enhancement paper](https://journals.sagepub.com/doi/10.1177/13694332251353614) |
| Portrait | [University portrait asset](https://faculty.swjtu.edu.cn/_resources/group1/M00/00/4D/wKi3F2bOyP-AdWR-AAFT5guPlMw859.png) |
| Research overview | [University research image](https://faculty.swjtu.edu.cn/_resources/group1/M00/00/59/wKi3FmiySTqAOitXAAMj9tvfg78542.png) |
| Publication titles, complete author lists, affiliation mappings, journals, years and DOIs | The 23 papers supplied by Wenjie Liao; first pages and author-affiliation footnotes were checked |
| Research summaries and theme assignments | Original editorial summaries and classifications based on the supplied papers |
| Representative method figures | Figures extracted from the supplied papers, with their original figure numbers and DOI attribution displayed on the site |
| Four courses and 33 outline topics, grouped into two undergraduate and two graduate courses | Locally supplied materials in `assets/teaching/`: PDF and presentation covers and outlines, assignment themes, and embedded slide data in interactive HTML lessons |
| Chinese paper titles, summaries, and figure captions | Original editorial translations based on the same verified publication records; English published titles are preserved |

The site uses “Associate Research Professor”, following the university biography and employment section. The research statement was updated at the author's request on 2026-11-28 to focus on AI-driven structural design and optimization, including generative design of building structures and structural seismic resilience.

## Publication records and dates

`_data/publications.json` is the single source of publication facts rendered by Publications and the research-theme pages. `_bibliography/papers.bib` is an exported citation copy, not a separate source for the web pages. The collection contains 23 distinct supplied papers. Current theme counts are 18 for generative design, 5 for structural optimization, and 6 for seismic performance and resilience; papers can belong to multiple themes. These counts describe this collection, not a claim about the author's complete publication record.

Publication years follow the formal journal issue printed in the supplied paper. They can differ from the filename, copyright year, DOI year, and online publication year. In particular, two Engineering Structures papers belong to 2027 volumes. `online_date` is displayed only when explicitly verified. A January 1 value with year-only precision is a sorting placeholder and is not displayed as an exact publication date. An acceptance date is not treated as an online publication date. The list is sorted by `sort_key` in descending order. This key concatenates the formal journal year, a hyphen, and the verified `online_date` when available, otherwise `date`. For example, `2027-2026-10-09` belongs to the 2027 journal-year group and uses 2026-10-09 within that group. The key is internal and is updated whenever its source year or date changes.

## Images and local source material

Representative paper figures are stored in `assets/img/publications/`. They illustrate the published methods; the accompanying English and Chinese descriptions are newly written. The three SVG research diagrams are original conceptual illustrations for this site, not measured results or trained-model outputs. The university research overview PNG remains a sourced asset used by the current social-sharing configuration; the Research overview section has been removed from the Research page.

The full papers and course slides remain local in the repository-relative `assets/papers/` and `assets/teaching/` directories. Git ignores both directories, Jekyll excludes them from the built site, and the packaging script excludes them from both source and preview archives. All teaching-source formats, including PPT, PPTX, PDF, DOCX, HTML, and GIF, are excluded. Extracted text, page renders, temporary conversions, and review notes in `output/` are also private working materials. The website exposes publication metadata, summaries, selected figures, and DOI links, without publishing the supplied full texts. New images and attachments require a review of their visible contents and metadata before publication.

## Teaching and other profile content

Teaching reads the shared bilingual `_data/teaching.json` and presents four courses:

| Level | Course | Outline topics |
| --- | --- | --- |
| Undergraduate | Seismic Design of Building Structures / 建筑结构抗震设计 | 8 |
| Undergraduate | Big Data Applications and Analytics in Intelligent Construction / 智能建造大数据应用与分析 | 12 |
| Graduate | Fundamentals of Artificial Intelligence in Civil Engineering / 土木工程人工智能基础 | 5 |
| Graduate | Intelligent Design of Engineering Structures / 工程结构智能设计 | 8 |

English course names are faithful translations, not independently verified official catalog titles. Course summaries and topic descriptions are newly written in both languages. Topic counts describe the available outlines, not the number of class meetings. The teaching page provides no downloads or links to original slides, interactive lessons, textbooks, assignments, or answer keys. Credits, semesters, and assessment arrangements are not stated.

Course codes follow the supplied course-information materials. Detailed reconciliation notes and source files remain local; the public teaching page contains course summaries and topic outlines only.

## Bilingual presentation and profile links

The English site keeps its original routes beginning at `/`; Chinese pages mirror them under `/zh/`. Both versions are built as static pages. Each page declares `lang: en` or `lang: zh`, and paired pages share a `translation_key` so that the language switch links to the corresponding page. Chinese page sources are in `_pages/zh/`; the same publication and teaching records serve both languages. The publication fields `title_zh`, `summary_zh`, and `figure_caption_zh` contain editorial translations, with the English published title retained for identification.

Homepage external links are the university Chinese profile, Google Scholar, GitHub, and ORCID. The English university profile remains a provenance source for previously checked biography facts. Typography uses local system CJK sans-serif fallbacks for Chinese and common system sans-serif fonts for English.

Citation counts, patent totals, awards, current student names, and admission quotas have not been added. A future CV may be published separately when Wenjie Liao supplies and approves it for public use, after reviewing its contents and metadata for private information.

## Public repository scope

Public academic identity, institutional contact information, publications, and approved profile links are retained. Private contact details, credentials, local usernames and machine paths, original teaching materials, unpublished documents, and review notes do not belong in the public source. Source and build privacy checks support this boundary; they do not replace manual review. Ignore rules do not remove Git history, and a local history scan does not establish removal from remote copies, forks, or caches.

## Template

Template: [al-folio](https://github.com/alshedivat/al-folio), commit `e5f84cc8da64bc31d05a0733f0b832d9d77c084d`. Runtime: `al_folio_core 1.0.15`. The original MIT license is preserved in `LICENSE`.

The Sass entry `assets/css/main.scss` retains the core imports and appends the site-specific `personal` module. Its reviewed fingerprint is recorded in `.al-folio-overrides.yml`. The local publication component reads the shared JSON data for consistent rendering across pages.
