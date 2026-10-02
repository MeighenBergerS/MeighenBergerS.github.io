---
name: design-architecture
description: Data flow, single source of truth and private data in the website and CV repo. Load when adding a data file, a field, a page, a CV section, or deciding where new content lives.
---

# Architecture

A1. Data flows one way: `data/*.yml`, `data/news/` + `data/cache/` (from
    `fetch.py`) -> `pipeline/build.py` -> `_site/`, `build/cv/`, `build/review.md`.
A2. One source of truth. A fact is written once in `data/` and both the site
    and the CV read it. Never type it into a template.
A3. Paper metadata (authors, journal, citations, arXiv) comes from INSPIRE.
    `papers.yml` holds only what no API knows. A paper without INSPIRE goes in `papers_extra.bib`.
A4. A count in prose ("12 invited talks") is a `{{ stats.* }}` placeholder
    computed in `compute_stats`, never a typed number.
A5. Group by content, one file per kind (`talks.yml`, `teaching.yml`, ...).
    A new field is documented in the comment block at the top of its file.
A6. Templates hold layout only. The site templates live in `templates/site/`,
    the CV in `templates/cv/`, one LaTeX section per file in `sections/`.
A7. Private data (phone, nationality, references) lives only in `private/`,
    which is git-ignored. Only `--private` reads it, and its output is never published.
A8. `data/cache/` and `data/metrics.csv` are written by CI. Edit them by hand only to fix a fetch.
A9. Drafts (`draft: true`, `data/news/drafts/`) never reach the live site.
