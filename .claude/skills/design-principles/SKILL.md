---
name: design-principles
description: Index of the design rules for this website and CV repo. Load before editing data, templates, the pipeline, docs or skills, to find the skill that applies.
---

# Website design principles

Goal: one set of data files gives the website and the CV, both always current,
with as little hand-typing as possible. The audience of the site is a physics
faculty search committee and interested non-specialists.

| Skill | Covers | IDs |
| --- | --- | --- |
| `design-governance` | how rules change, approval, learning | P, L |
| `design-architecture` | data flow, one source of truth, private data | A |
| `design-build` | pipeline code, failures, CI | B |
| `design-prose` | every text on the site and in the CV | W |
| `design-docs` | README, `docs/`, comments in the data files | G |
| `news-post` | writing one news post from a draft | |
| `workflow-commits` | splitting and writing commits | C |
| `workflow-pull-requests` | scoping and describing PRs | PR |
| `workflow-ai-disclosure` | no AI authorship, one note in the README | AI |
| `repo-audit` | monthly best-practice audit, untracked report | RA |

Rules describe the target state. Existing content that breaks one is migration
debt. Fix it when you touch it, and don't warn about it otherwise. Past commits
are never rewritten to follow a rule.

A conflict with a rule, or any change to one, follows `design-governance`.
The log is `decisions.md` in this folder.
