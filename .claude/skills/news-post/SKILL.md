---
name: news-post
description: Write a plain-English news post for a new paper or software release on this website, filling in a draft created by pipeline/news_drafts.py (or starting one from a paper key). Use when the user runs /news-post or asks to write or finish a news post.
---

# Write a news post

Fill in a draft news post in `data/news/`. Drafts are created weekly by CI
(`pipeline/news_drafts.py --open-prs`), one pull request each, or locally with
`python pipeline/news_drafts.py`.

## 1. Find the draft

- List `data/news/*.md` files whose front matter has `draft: true`. If there are
  several, ask the user which one. If there are none and the user named a paper (INSPIRE
  texkey or arXiv id), run `python pipeline/news_drafts.py` or create the draft by hand
  using an existing post as the model.
- Read the matching `data/news/drafts/<slug>/source.md` (abstract, introduction,
  conclusion, figure list).

## 2. Read the rules

Read `docs/news-style.md` in full and follow it. The essentials:
- 3–4 sentences (about 60–100 words), one paragraph: question → what we did → what we
  found (one number) → why it matters, the caveat, or your part. No separate post page
  exists; the summary is the whole post.
- First person: "we" with co-authors, "I" only for single-author work. Credit
  collaborators and students by name when their full names are in the source material.
- No em dashes, no colons joining clauses, no semicolon chains, American spelling.
  Greek letters as inline math (`$\nu_\tau$`).
- Never write "my student" or "my PhD student". Name students with their role in
  parentheses, for example "Ho Man Yim (PhD candidate)".
- Use only facts from the source material. Never invent numbers, comparisons, or
  claims of experimental adoption.

## 3. Ask the user (briefly, in one message)

- What was their part, if the source does not make it obvious, and whether a student
  should be credited.
- If the paper is not yet in `data/papers.yml`: its contribution tags
  (`wrote`, `idea`, `mentored`, plus `details` only when there is no `idea` tag) and
  theme (`neutrino`, `bsm`, `tools`, `side`). Add the entry to `data/papers.yml`.

## 4. Pick the figure

Look at each `fig-N.png` in the draft folder (use the Read tool on the images). Prefer
a sketch or overview figure that explains the idea without the paper; dense multi-panel
result plots are a last resort. Propose one and say why. After the user agrees, copy it
to `static/img/news/<slug>.png` (convert to `.jpg` with quality 88 if it is larger than
about 180 KB) and set `image` and `image_alt` (chart type, what is plotted, takeaway). Software
posts may keep the logo already set.

## 5. Write and finish

- Replace the TODO title with a plain-English headline under about 12 words (not the
  paper title) and the TODO body with the post.
- Remove `draft: true`. Delete `data/news/drafts/<slug>/`.
- Run `python3 pipeline/build.py`. It fails if the image path is wrong. Show the user
  the finished post text and word count.
- Do not commit or push unless the user asks. When they do, commit on the current
  branch (the PR branch) with a message like `News: <headline>`.
