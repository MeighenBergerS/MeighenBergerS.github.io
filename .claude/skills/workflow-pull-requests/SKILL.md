---
name: workflow-pull-requests
description: When and how to use pull requests in this repo. Load before opening, updating, describing or merging a PR.
---

# Pull requests

PR1. Small edits (a talk, a typo) go straight to `main`. A change to the layout,
     the pipeline or CI goes through a PR, so the build runs before deploy.
PR2. CI opens one PR per news draft. Finish it on its branch with `/news-post`.
PR3. The title follows C2. The body says what changes and why, and how to
     check it (`python pipeline/build.py`, then the page to look at).
PR4. Review your own diff first. No unrelated changes ride along.
PR5. List any design rule changed or excepted.
PR6. No AI attribution in the title, the body or the commits (`workflow-ai-disclosure`).
PR7. Open, push or merge only when the user asks.
