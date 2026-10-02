# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The personal academic website and CV of Stephan A. Meighen-Berger, deployed to
GitHub Pages. One set of data files gives both:

```
data/*.yml, data/news/  +  data/cache/ (INSPIRE, arXiv, GitHub)
    -> pipeline/build.py -> _site/ (website), build/cv/ (LaTeX CV), build/review.md
```

## Commands

```sh
pip install -r requirements.txt
python pipeline/fetch.py              # refresh data/cache (network; CI does this weekly)
python pipeline/build.py              # -> _site/, build/cv/, build/review.md
python pipeline/build.py --drafts     # include draft news posts (local preview only)
python pipeline/build.py --private    # also build/cv-private/ from private/private.yml
python -m http.server -d _site        # preview at http://localhost:8000
cd build/cv && latexmk -pdf main.tex  # CV PDF (full TeX Live with biber)
python pipeline/news_drafts.py        # create news drafts for new papers and releases
```

There are no tests. A passing `build.py` is the check.

## Layout

- `data/`: everything hand-written. Each file explains its fields in its header comment.
- `data/cache/`, `data/metrics.csv`: written by `fetch.py` in CI.
- `data/news/`: one Markdown file per news item. `drafts/` holds the source material for drafts.
- `templates/site/`, `templates/cv/`: Jinja templates for the site and the LaTeX CV.
- `static/`: CSS, JS and images, copied into `_site/`.
- `docs/news-style.md`: the news-post style guide.
- `private/`: git-ignored personal data, never published.
- `.github/workflows/site.yml`: fetch, news-draft PRs, build, CV, review issue, deploy.

## Conventions

- Design rules live in `.claude/skills/`. The index is `design-principles`; the
  change protocol and the learning rules are in `design-governance`. Load the
  relevant skill before touching data, templates, the pipeline or docs. A
  conflict with a rule is flagged in chat as **Design warning**, a rule change
  as **Design change**, and both are logged in `design-principles/decisions.md`.
  Never change a rule silently.
- Every text on the site or in the CV follows `design-prose`.
- Skills, hooks, subagents (`.claude/agents/`), `.claude/settings.json` and this
  file change only after the user explicitly approves that change. Never
  silently, never bundled with other work, never through Bash.
- Commits and PRs follow `workflow-commits` and `workflow-pull-requests`.
  Never add Claude as an author, co-author or signer (`workflow-ai-disclosure`).
  These rules apply from 2026-10-02. Never rewrite earlier commits to follow them.
