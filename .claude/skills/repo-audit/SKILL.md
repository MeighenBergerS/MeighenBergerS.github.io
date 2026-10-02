---
name: repo-audit
description: The Repo Audit, a monthly comparison of the website repo with current best practices, run only after the user approves. Load when a session start says it is due, or when the user asks for /repo-audit.
---

# Repo Audit

Untracked, in `.audit/`: reports `YYYY-MM-DD.md` and `state.json`.

RA1. Ask first, in 1-3 short sentences, e.g.: "The Repo Audit compares the
     website with current best practices for the site, CI and skills. It reads
     the web and the repo, changes nothing, and writes an untracked report. Run it now?"
RA2. Declined: set `snooze_until` in `state.json` to today + 7 days. Nothing else.
RA3. Approved:
     1. Run `python pipeline/build.py` and note whether it passed and what it printed.
     2. Check every internal link and image in `_site/` resolves, with a short
        script in the scratchpad, and note the broken ones.
     3. Hand both results and the latest earlier report to the `repo-auditor` subagent.
     4. Write its report to `.audit/<today>.md`, set `last_run` to today, and drop `snooze_until`.
     5. In chat, at most ~10 lines: the counts, the top findings, and each
        proposal as **Design change proposed**.
RA4. The audit changes nothing outside `.audit/`. Adopting a proposal follows `design-governance`.
