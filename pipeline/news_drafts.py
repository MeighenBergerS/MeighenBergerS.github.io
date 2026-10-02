"""Create draft news posts for new papers and software releases.

    python pipeline/news_drafts.py            # write drafts locally (no git)
    python pipeline/news_drafts.py --open-prs # CI: one branch + pull request per draft

A draft is data/news/<slug>.md with `draft: true` and the metadata filled in, plus
data/news/drafts/<slug>/ with source.md (abstract, introduction, conclusion) and up
to six candidate figures from the arXiv source. The text itself is written locally
with Claude Code (`/news-post`, see .claude/skills/news-post/SKILL.md) following
docs/news-style.md. Nothing here calls an AI model.

Needs: pyyaml, jinja2, pypdfium2, pillow (figure rendering is skipped without them).
"""

import argparse
import datetime as dt
import io
import json
import re
import subprocess
import sys
import tarfile
import time
import urllib.request
import gzip
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402

ROOT = build.ROOT
NEWS = ROOT / "data" / "news"
DRAFTS = NEWS / "drafts"
WINDOW_DAYS = 120          # only papers/releases newer than this get a draft
MAX_FIGURES = 6
UA = {"User-Agent": "MeighenBergerS.github.io news drafts (https://github.com/MeighenBergerS)"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        return r.read()


def slugify(text, n=6):
    words = re.sub(r"[^a-z0-9 ]+", " ", text.lower()).split()
    stop = {"a", "an", "the", "of", "for", "with", "and", "in", "on", "to", "from", "using", "via"}
    return "-".join([w for w in words if w not in stop][:n])


def existing_posts():
    posts = []
    for f in NEWS.glob("*.md"):
        m = re.match(r"^---\n(.*?)\n---", f.read_text(encoding="utf-8"), re.S)
        posts.append(yaml.safe_load(m.group(1)) if m else {})
    return posts


# ---------------------------------------------------------------- candidates

def paper_candidates(papers, posts, today):
    covered = {p.get("paper") for p in posts}
    out = []
    for p in papers:
        if not p["recid"] or not p["arxiv"] or p["hidden"] or p["experiment"] or p["status"] == "thesis":
            continue
        if p["author_count"] > build.REVIEW_MAX_AUTHORS or set(p["texkeys"]) & covered or p["key"] in covered:
            continue
        try:
            date = dt.date.fromisoformat(str(p["date"])[:10])
        except ValueError:
            continue
        if (today - date).days <= WINDOW_DAYS:
            out.append((date, p))
    return out


def software_candidates(software, github, posts, today):
    covered = {(p.get("software"), str(p.get("version"))) for p in posts}
    out = []
    for s in software:
        if s.get("section") == "earlier":
            continue
        g = github.get(s.get("repo")) or {}
        rel = g.get("pypi") or ({"version": g["latest_release"]["tag"].lstrip("v"), "date": g["latest_release"]["date"]}
                                if g.get("latest_release") else None)
        if not rel or not rel.get("date"):
            continue
        date = dt.date.fromisoformat(rel["date"][:10])
        if (today - date).days <= WINDOW_DAYS and (s["name"], str(rel["version"])) not in covered:
            out.append((date, s, rel["version"]))
    return out


# ---------------------------------------------------------------- arXiv source

def arxiv_source(arxiv_id):
    """{name: bytes} of the files in the arXiv e-print."""
    data = get(f"https://arxiv.org/e-print/{arxiv_id}")
    time.sleep(3)  # be polite to arXiv
    try:
        with tarfile.open(fileobj=io.BytesIO(data)) as tar:
            return {m.name: tar.extractfile(m).read() for m in tar.getmembers() if m.isfile()}
    except tarfile.ReadError:
        try:
            return {"main.tex": gzip.decompress(data)}
        except OSError:
            return {}


def main_tex(files):
    texs = {n: b.decode("utf-8", "ignore") for n, b in files.items() if n.endswith(".tex")}
    for n, t in texs.items():
        if "\\begin{document}" in t:
            # inline \input / \include so sections in separate files are found
            def inline(m):
                name = m.group(1) if m.group(1).endswith(".tex") else m.group(1) + ".tex"
                return next((v for k, v in texs.items() if k.endswith(name)), "")
            return re.sub(r"\\(?:input|include)\{([^}]+)\}", inline, t)
    return next(iter(texs.values()), "")


def section(tex, names):
    for name in names:
        m = re.search(rf"\\section\*?\{{[^}}]*{name}[^}}]*\}}(.*?)(?=\\section|\\appendix|\\begin{{acknowledgments}}|\\bibliography|\\end{{document}})",
                      tex, re.S | re.I)
        if m:
            return m.group(1)
    return ""


def clean(tex, limit):
    tex = re.sub(r"(?<!\\)%.*", "", tex)
    tex = re.sub(r"\\begin\{figure\*?\}.*?\\end\{figure\*?\}", "", tex, flags=re.S)
    tex = re.sub(r"\\(cite[pt]?|ref|label|eqref)\{[^}]*\}", "", tex)
    tex = re.sub(r"\n{3,}", "\n\n", tex).strip()
    return tex[:limit]


def figures(files, tex, out_dir):
    """Render the paper's figures, in order of appearance, to PNG candidates."""
    try:
        import pypdfium2 as pdfium
        from PIL import Image
    except ImportError:
        print("  (pypdfium2/pillow missing: no figure candidates)")
        return []
    names = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", tex)
    order = []
    for n in names:
        for cand in (n, n + ".pdf", n + ".png", n + ".jpg", n + ".jpeg"):
            hit = next((k for k in files if k.endswith(cand) and "orcid" not in k.lower()), None)
            if hit and hit not in order:
                order.append(hit)
                break
    rendered = []
    for i, name in enumerate(order[:MAX_FIGURES], 1):
        try:
            data = files[name]
            if name.lower().endswith(".pdf"):
                page = pdfium.PdfDocument(data)[0]
                w, h = page.get_size()
                img = page.render(scale=1100 / max(w, h)).to_pil()
            else:
                img = Image.open(io.BytesIO(data))
                img.thumbnail((1100, 1100))
            path = out_dir / f"fig-{i}.png"
            img.convert("RGB").save(path, optimize=True)
            rendered.append((path.name, Path(name).name))
        except Exception as exc:  # a broken figure should not stop the draft
            print(f"  figure {name} skipped ({exc})")
    return rendered


# ---------------------------------------------------------------- drafts

def front_matter(meta):
    return "---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=1000) + "---\n"


def write_paper_draft(date, p):
    slug = f"{date.isoformat()}-{slugify(p['title'])}"
    out_dir = DRAFTS / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"paper draft: {slug}")
    abstract = ""
    try:
        meta = json.loads(get(f"https://inspirehep.net/api/literature/{p['recid']}?fields=abstracts.value"))
        abstract = (meta["metadata"].get("abstracts") or [{}])[0].get("value", "")
    except Exception as exc:
        print(f"  abstract unavailable ({exc})")
    files = arxiv_source(p["arxiv"])
    tex = main_tex(files)
    figs = figures(files, tex, out_dir)
    authors = ", ".join(p["authors"] or []) or f"{p['author_count']} authors"
    source = [f"# {p['title']}", "", f"- Authors: {authors}", f"- arXiv: {p['arxiv']}",
              f"- Venue: {p.get('venue') or 'preprint'}", f"- INSPIRE: {p['url']}", "",
              "## Abstract", "", abstract, "",
              "## Introduction (LaTeX, truncated)", "", clean(section(tex, ["Introduction"]), 9000), "",
              "## Conclusion (LaTeX, truncated)", "", clean(section(tex, ["Conclusion", "Summary", "Discussion", "Outlook"]), 5000), "",
              "## Figure candidates", ""]
    source += [f"- {png}: {orig}" for png, orig in figs] or ["- none found"]
    (out_dir / "source.md").write_text("\n".join(source) + "\n", encoding="utf-8")
    meta = {"date": date.isoformat(), "type": "paper", "draft": True,
            "title": f"TODO plain-English headline ({p['title']})", "paper": p["key"]}
    body = ("TODO: write the post with `/news-post` in Claude Code (see docs/news-style.md).\n"
            f"Source material and figure candidates: data/news/drafts/{slug}/\n")
    (NEWS / f"{slug}.md").write_text(front_matter(meta) + body, encoding="utf-8")
    return slug, f"New paper: {p['title']}"


def write_software_draft(date, s, version):
    slug = f"{date.isoformat()}-{slugify(s['name'])}-{slugify(str(version), 3)}"
    out_dir = DRAFTS / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"software draft: {slug}")
    notes = ""
    try:  # release notes, if the release exists on GitHub
        rel = json.loads(get(f"https://api.github.com/repos/{s['repo']}/releases/latest"))
        notes = rel.get("body") or ""
    except Exception:
        pass
    source = [f"# {s['name']} {version}", "", f"- Repository: https://github.com/{s['repo']}",
              f"- Docs: {s.get('docs', '-')}", f"- Tagline: {s.get('tagline', '')}", "",
              "## Description (software.yml)", "", s.get("description", ""), "",
              "## Release notes", "", notes or "(none found: check the CHANGELOG in the repository)", ""]
    (out_dir / "source.md").write_text("\n".join(source), encoding="utf-8")
    meta = {"date": date.isoformat(), "type": "software", "draft": True,
            "title": f"TODO plain-English headline ({s['name']} {version})", "software": s["name"],
            "version": str(version)}
    if s.get("logo"):
        meta["image"] = s["logo"]
        meta["image_alt"] = f"{s['name']} logo"
    body = ("TODO: write the post with `/news-post` in Claude Code (see docs/news-style.md).\n"
            f"Source material: data/news/drafts/{slug}/\n")
    (NEWS / f"{slug}.md").write_text(front_matter(meta) + body, encoding="utf-8")
    return slug, f"New release: {s['name']} {version}"


# ---------------------------------------------------------------- git / PRs

def sh(*cmd, check=True):
    return subprocess.run(cmd, cwd=ROOT, check=check, capture_output=True, text=True).stdout.strip()


PR_BODY = """A draft news post was created automatically for **{what}**.

The text still has to be written. To fill it in locally with Claude Code:

```bash
gh pr checkout {number}
claude            # then run: /news-post
```

`/news-post` follows `docs/news-style.md`, writes the plain-English summary, lets you pick a
figure from `data/news/drafts/{slug}/`, removes `draft: true`, and cleans up the draft folder.
Review the result, push, and merge. Close this PR to skip the post.
"""


def open_pr(slug, what, make):
    branch = f"news/{slug}"
    if sh("git", "ls-remote", "--heads", "origin", branch):
        print(f"  {branch} already exists, skipping")
        return
    sh("git", "switch", "-c", branch)
    try:
        make()
        sh("git", "add", "data/news")
        sh("git", "commit", "-m", f"News draft: {what}")
        sh("git", "push", "-u", "origin", branch)
        url = sh("gh", "pr", "create", "--base", "main", "--head", branch, "--title", f"News draft: {what}",
                 "--body", PR_BODY.format(what=what, number="<number>", slug=slug))
        number = url.rstrip("/").rsplit("/", 1)[-1]
        sh("gh", "pr", "edit", number, "--body", PR_BODY.format(what=what, number=number, slug=slug))
        print(f"  opened {url}")
    finally:
        sh("git", "switch", "main")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--open-prs", action="store_true", help="commit each draft on its own branch and open a PR")
    args = ap.parse_args()

    today = dt.date.today()
    papers, _, _, _ = build.load_papers()
    software = build.load("software.yml")["software"]
    github = json.loads((build.CACHE / "github.json").read_text()) if (build.CACHE / "github.json").exists() else {}
    posts = existing_posts()

    jobs = []
    for date, p in paper_candidates(papers, posts, today):
        slug = f"{date.isoformat()}-{slugify(p['title'])}"
        jobs.append((slug, f"New paper: {p['title']}", lambda d=date, p=p: write_paper_draft(d, p)))
    for date, s, version in software_candidates(software, github, posts, today):
        slug = f"{date.isoformat()}-{slugify(s['name'])}-{slugify(str(version), 3)}"
        jobs.append((slug, f"New release: {s['name']} {version}", lambda d=date, s=s, v=version: write_software_draft(d, s, v)))

    if not jobs:
        print("news drafts: nothing new")
    for slug, what, make in jobs:
        if args.open_prs:
            open_pr(slug, what, make)
        else:
            make()


if __name__ == "__main__":
    main()
