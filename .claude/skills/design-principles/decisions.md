# Design decisions log

Newest first. One entry per adoption, change or exception: date, IDs, what, why.

## 2026-10-26: The private.yml template may be committed (C7)

C7 now excepts `private/private.yml.example` from "nothing in `private/` is
staged". The file is tracked on purpose as the template for `private.yml` and
documents its fields, such as `nationality` and `students`. It holds no
private data.

## 2026-10-26: Mentored students are private data (A7)

A7 now lists the names of mentored students as private data. The public site and
CV show only counts per level (`supervision` in `data/teaching.yml`) and the joint
papers. The full list moves to `private/private.yml` and appears only in the
private CV. Why: the user wants students named only in application documents
until they have their own group. News posts keep the names of student coauthors,
since they describe the papers. Earlier commits stay as they are.

## 2026-10-02: The skill tree is adopted for the website

Adapted from the sanflux skill tree, at the user's request.

Carried over in substance: `design-governance` (P, L), `workflow-commits` (C),
`workflow-pull-requests` (PR), `workflow-ai-disclosure` (AI), `repo-audit` (RA).

Changed for this repo:
- `design-architecture` (A) describes the data flow from `data/` to the site
  and the CV, rather than a package's module layers.
- `design-build` (B) replaces `design-robustness` for the pipeline scripts.
- `design-prose` (W) is new. It moves the writing rules from personal memory
  and `docs/news-style.md` into the repo (L6).
- `design-docs` (G): the README is for the owner only and stays short.
- C2: subjects become lowercase, replacing the capitalized subjects and the
  `News:` prefix used so far. C6 and AI4: the rules apply from today, and
  earlier commits, including their `Co-Authored-By` trailers, stay as they are.
- PR1: small data edits go straight to `main`. The repo has no PR template,
  so PR7 of sanflux (the template check in CI) is not carried over.
- RA: monthly instead of every 14 days, no `sp-repo-review` (not a Python
  package) and no README checklist (G1). The audit checks the built site instead.

Not carried over: `design-naming`, `design-objects`, `design-docstrings`
(no public API), `workflow-issues` (no issue forms or labels, and the only
issue is opened by CI), and the design-rule tests.
