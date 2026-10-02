---
name: design-build
description: Rules for the Python pipeline (fetch, build, news drafts) and the CI workflow. Load when editing anything in pipeline/ or .github/workflows/.
---

# Build

B1. Three scripts, one job each: `fetch.py` talks to the APIs, `build.py`
    renders from local files only, `news_drafts.py` creates drafts and PRs.
B2. `build.py` never touches the network, so a build is reproducible from the repo.
B3. Bad data fails the build with one line naming the file, the key and the fix.
    Do: `SystemExit("x.md: image img/news/x.png not found in static/")`.
    Not: a traceback, or a silently skipped entry.
B4. Something that needs a human, rather than a fix, goes in `build/review.md`,
    which CI turns into the "Publications needing review" issue.
B5. Dependencies stay minimal: the standard library, `jinja2` and `pyyaml`.
    A CI-only tool is installed in its CI step, not in `requirements.txt`.
B6. Named thresholds are module constants with a comment (`SMALL_AUTHOR_LIST`).
B7. A step that may fail without harming the site (news drafts) uses
    `continue-on-error`. Fetching, building and deploying never do.
B8. No AI model runs in CI. Writing text happens locally, with the user.
