---
name: workflow-commits
description: How to split and write git commits in this repo. Load before staging or committing anything.
---

# Commits

C1. One logical change per commit, and the build passes at each one.
    Protected files (`design-governance` P4) always get a commit of their own.
C2. Subject: imperative, lowercase, no period, ≤50 characters (72 at most),
    saying what changes.
    Do: `add Iowa seminar`, `add news post on effective areas`.
    Not: `update`, `fixed stuff`, `More data cleaning`.
C3. Add a body when the why isn't obvious: a blank line after the subject,
    wrapped at 72, covering why and what, not how.
C4. No AI attribution in the message (`workflow-ai-disclosure`).
C5. Commit only when the user asks. Stage files by name, never `git add -A`.
    Check `git diff --cached --stat` in a command of its own, read it, and only then commit.
C6. Never amend, rebase or force-push published history. Earlier commits are
    left as they are, even where they break these rules.
C7. Before committing, `python pipeline/build.py` passes. Nothing in
    `private/`, `_site/` or `build/` is staged.
