# MeighenBergerS.github.io

My website and CV, built from `data/` by `pipeline/build.py` and deployed by
`.github/workflows/site.yml` on every push and every Monday.

```bash
pip install -r requirements.txt
python pipeline/build.py           # -> _site/ and build/cv/  (--drafts, --private)
python -m http.server -d _site     # http://localhost:8000
```

- Edit content in `data/*.yml`. Each file explains its fields at the top.
  Paper metadata comes from INSPIRE, never by hand.
- News: CI opens a PR with a draft for each new paper or release. Finish it
  with `gh pr checkout <n>`, then `/news-post` in Claude Code.
- Open items land in the issue "Publications needing review".
- `private/` (phone, references) is git-ignored. `--private` builds the full CV locally.

## Development with AI assistance

This repo is developed with Claude Code. Its rules live in `CLAUDE.md` and
`.claude/skills/`. I review and commit every change.
