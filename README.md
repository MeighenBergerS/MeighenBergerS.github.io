# MeighenBergerS.github.io

Personal academic website and CV of Stephan A. Meighen-Berger, generated from one
set of data files.

```
data/*.yml  +  INSPIRE / arXiv / GitHub  ──►  pipeline/build.py  ──►  _site/        (website)
                                                                  ──►  build/cv/     (LaTeX CV, simplecv style)
                                                                  ──►  build/review.md (what needs your attention)
```

## Day-to-day

| To… | Edit |
|---|---|
| Add a talk | `data/talks.yml` |
| Annotate a new paper (contribution, themes, selected) | `data/papers.yml` |
| Add a paper that is not on INSPIRE | `data/papers_extra.bib` + `data/papers.yml` |
| Update positions, awards, education | `data/cv.yml` |
| Students, lecturing | `data/teaching.yml` |
| Software | `data/software.yml` |
| Research page text | `data/research.yml` |
| Bio, links | `data/profile.yml` |

Text fields accept light Markdown (`**bold**`, `*italic*`, `[text](url)`) and inline math
(`$\nu_\tau$`, `$p\gamma$`), rendered by KaTeX on the site and by LaTeX in the CV. Use Greek
letters rather than spelled-out names.

Paper metadata (authors, journal, citations) is never typed by hand: it comes from
INSPIRE. Counts in the prose ("12 invited talks", "two Master's students",
"84 refereed papers") are computed at build time.

## News posts

Plain-English posts for new papers and software releases live in `data/news/`
(one Markdown file each, front matter + text). Style rules: `docs/news-style.md`.

Every Monday CI checks for new papers (yours, not large-collaboration papers) and new
releases of the software in `software.yml`. For each one without a post it opens a
pull request with a **draft**: metadata filled in, `draft: true`, plus the abstract,
introduction and candidate figures from the arXiv source in `data/news/drafts/<slug>/`.
No AI model runs in CI. To write the post:

```bash
gh pr checkout <number>
claude                 # then: /news-post
```

`/news-post` (`.claude/skills/news-post/`) writes the text following the style guide,
asks for your contribution tags if the paper is new, helps pick a figure, removes the
draft flag and cleans up. Review, push, merge. Drafts never appear on the live site;
preview them locally with `python pipeline/build.py --drafts`.

To create drafts locally instead: `python pipeline/news_drafts.py`.

## Local build

```bash
pip install -r requirements.txt
python pipeline/fetch.py            # refresh data/cache (optional; CI does this weekly)
python pipeline/build.py            # -> _site/ and build/cv/
python -m http.server -d _site      # preview at http://localhost:8000
```

CV PDF: `cd build/cv && latexmk -pdf main.tex` (needs a full TeX Live with biber).

Private CV (phone, nationality, references): fill `private/private.yml` from the
example, then `python pipeline/build.py --private` and compile `build/cv-private/`.
`private/` is git-ignored; that build is never published.

## Automation

`.github/workflows/site.yml` runs on every push and every Monday:

1. fetches INSPIRE, arXiv and GitHub data and commits it, which adds a row to `data/metrics.csv` for history,
2. builds the site and compiles the CV to `cv.pdf`,
3. opens or updates a GitHub issue, **Publications needing review**, listing new papers that are not yet annotated in `data/papers.yml` (or listed under `hidden`),
4. deploys to GitHub Pages.
