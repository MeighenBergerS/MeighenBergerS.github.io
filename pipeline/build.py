"""Build the website (_site/) and the CV sources (build/cv/) from data/.

    python pipeline/build.py            # public site + public CV sources
    python pipeline/build.py --private  # additionally build/cv-private/ with
                                        # phone, nationality and references

Reads data/*.yml (hand-written) and data/cache/* (written by fetch.py).
Also writes build/review.md: papers and preprints that need your attention.
"""

import argparse
import csv
import datetime as dt
import html
import json
import re
import shutil
from pathlib import Path

import jinja2
import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CACHE = DATA / "cache"
SITE = ROOT / "_site"
BUILD = ROOT / "build"
SELF = "Meighen-Berger"
SMALL_AUTHOR_LIST = 10  # "small-author-list works": fewer than this many authors
REVIEW_MAX_AUTHORS = 30  # unlisted papers below this author count are flagged for review


def load(name):
    return yaml.safe_load((DATA / name).read_text(encoding="utf-8"))


# ---------------------------------------------------------------- light markup
# Text in the YAML files uses **bold**, *italic* and [text](url); these two
# functions render that to HTML and to LaTeX.

LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
BOLD = re.compile(r"\*\*(.+?)\*\*")
ITAL = re.compile(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])")


def to_html(text):
    if text is None:
        return ""
    s = html.escape(str(text), quote=False)
    s = LINK.sub(r'<a href="\2">\1</a>', s)
    s = BOLD.sub(r"<strong>\1</strong>", s)
    s = ITAL.sub(r"<em>\1</em>", s)
    return s


TEX_ESCAPE = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
              "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\^{}",
              "\\": r"\textbackslash{}", "–": "--", "—": "---"}


# Greek letters typed directly (e.g. "pγ") become math in LaTeX; pdflatex has no text glyphs.
GREEK = dict(zip("αβγδεζηθικλμνξπρστυφχψωΓΔΘΛΞΠΣΦΨΩ",
                 [rf"$\{n}$" for n in ("alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi "
                                        "pi rho sigma tau upsilon phi chi psi omega Gamma Delta Theta Lambda Xi Pi "
                                        "Sigma Phi Psi Omega").split()]))
TEX_ESCAPE.update(GREEK)
MATH = re.compile(r"(?<!\\)\$(?!\s)(.+?)(?<!\s)\$")  # inline $...$ math, passed through untouched


def tex_escape(s):
    return "".join(TEX_ESCAPE.get(c, c) for c in str(s))


def to_tex(text):
    if text is None:
        return ""
    links = []

    def stash(m):  # protect URLs from escaping
        links.append(m.group(2))
        return f"\x00{len(links) - 1}\x00{m.group(1)}\x01"

    maths = []

    def stash_math(m):  # protect $...$ from escaping and from the * markup
        maths.append(m.group(0))
        return f"\x02{len(maths) - 1}\x03"

    s = MATH.sub(stash_math, str(text))
    s = LINK.sub(stash, s)
    s = tex_escape(s)
    s = re.sub(r"\x00(\d+)\x00(.*?)\x01", lambda m: rf"\href{{{links[int(m.group(1))]}}}{{{m.group(2)}}}", s)
    s = BOLD.sub(r"\\textbf{\1}", s)
    s = ITAL.sub(r"\\textit{\1}", s)
    s = re.sub(r"\x02(\d+)\x03", lambda m: maths[int(m.group(1))], s)
    return s  # straight quotes are left to csquotes (\MakeOuterQuote)


SMALL_WORDS = {"a", "an", "the", "and", "or", "of", "in", "on", "for", "with", "from", "to", "at", "by", "via", "vs"}


def title_case(title):
    """Sentence-case INSPIRE titles -> Title Case (keeps acronyms, handles hyphens)."""
    out, start = [], True
    for word in title.split(" "):
        if not start and word.lower() in SMALL_WORDS:
            out.append(word.lower())
        else:
            out.append("-".join(w[:1].upper() + w[1:] if w[:1].islower() else w for w in word.split("-")))
        start = word.endswith(":")
    return " ".join(out)


# ---------------------------------------------------------------- papers

def split_bib(text):
    """Return {key: raw entry} for a BibTeX string."""
    out = {}
    for m in re.finditer(r"^@\w+\{\s*([^,\s]+)\s*,.*?^\}", text, re.S | re.M):
        out[m.group(1)] = m.group(0)
    return out


def bib_field(entry, field):
    m = re.search(rf"\b{field}\s*=\s*[{{\"](.+?)[}}\"]\s*,?\s*$", entry, re.M | re.I)
    return m.group(1).strip("{}") if m else None


def short_name(full):
    """'Meighen-Berger, Stephan A.' -> 'S. A. Meighen-Berger'."""
    if "," not in full:
        return full
    last, first = [p.strip() for p in full.split(",", 1)]
    initials = " ".join(p[0] + "." for p in re.split(r"[\s.]+", first) if p)
    return f"{initials} {last}".strip()


JOURNAL_PRETTY = {"Phys.Rev.D": "Phys. Rev. D", "Phys.Rev.Lett.": "Phys. Rev. Lett.",
                  "Phys.Lett.B": "Phys. Lett. B", "Comput.Phys.Commun.": "Comput. Phys. Commun.",
                  "Astropart.Phys.": "Astropart. Phys.", "Eur.Phys.J.C": "Eur. Phys. J. C",
                  "Nature Astron.": "Nature Astron."}


def venue(pub_info):
    """'Phys. Lett. B, 2020' style, for prose."""
    for p in pub_info or []:
        if p.get("journal_title"):
            j = JOURNAL_PRETTY.get(p["journal_title"], p["journal_title"])
            return f"{j}, {p['year']}" if p.get("year") else j
    return None


def journal_ref(pub_info):
    for p in pub_info or []:
        if p.get("journal_title"):
            parts = [JOURNAL_PRETTY.get(p["journal_title"], p["journal_title"])]
            if p.get("journal_volume"):
                parts.append(p["journal_volume"])
            ref = " ".join(parts)
            if p.get("year"):
                ref += f" ({p['year']})"
            page = p.get("artid") or p.get("page_start")
            if page:
                ref += f" {page}"
            return ref
    return None


def paper_from_inspire(m):
    doc = m.get("document_type", [])
    authors = m.get("authors")
    collab = [c["value"] for c in m.get("collaborations", [])]
    arxiv = (m.get("arxiv_eprints") or [{}])[0].get("value")
    doi = (m.get("dois") or [{}])[0].get("value")
    jref = journal_ref(m.get("publication_info"))
    if "conference paper" in doc:
        status = "proc"
    elif jref:
        status = "pub"
    elif "thesis" in doc:
        status = "thesis"
    else:
        status = "sub"
    return {
        "key": m["texkeys"][0],
        "texkeys": m["texkeys"],
        "recid": m["control_number"],
        "title": m["titles"][0]["title"],
        "authors": [short_name(a) for a in authors] if authors else None,
        "author_count": m.get("author_count", 0),
        "collaborations": collab,
        "date": m.get("earliest_date", ""),
        "year": int(m.get("earliest_date", "0")[:4] or 0),
        "journal": jref,
        "venue": venue(m.get("publication_info")),
        "arxiv": arxiv,
        "doi": doi,
        "citations": m.get("citation_count", 0),
        "refereed": m.get("refereed"),
        "doc_type": doc[0] if doc else "",
        "status": status,
        "url": f"https://inspirehep.net/literature/{m['control_number']}",
    }


def paper_from_bib(key, entry):
    authors = [short_name(a.strip()) for a in (bib_field(entry, "author") or "").split(" and ") if a.strip()]
    year = bib_field(entry, "year") or "0"
    journal = bib_field(entry, "journal")
    arxiv, doi = bib_field(entry, "eprint"), bib_field(entry, "doi")
    return {
        "key": key, "texkeys": [key], "recid": None,
        "title": bib_field(entry, "title"),
        "authors": authors if len(authors) <= REVIEW_MAX_AUTHORS else None,
        "author_count": len(authors), "collaborations": [],
        "date": year, "year": int(year), "journal": f"{journal} ({year})" if journal else None,
        "venue": f"{journal}, {year}" if journal else None,
        "arxiv": arxiv, "doi": doi, "citations": None, "refereed": bool(journal),
        "doc_type": "article", "status": "pub" if journal else "sub",
        "url": f"https://doi.org/{doi}" if doi else (f"https://arxiv.org/abs/{arxiv}" if arxiv else None),
    }


def load_papers():
    notes = load("papers.yml")
    curated, hidden = notes["papers"], set(notes.get("hidden") or [])
    records = json.loads((CACHE / "inspire.json").read_text(encoding="utf-8"))
    papers = [paper_from_inspire(m) for m in records]

    bib = split_bib((CACHE / "inspire.bib").read_text(encoding="utf-8"))
    extra_bib = split_bib((DATA / "papers_extra.bib").read_text(encoding="utf-8"))
    bib.update(extra_bib)

    by_key = {k: p for p in papers for k in p["texkeys"]}
    for key, entry in extra_bib.items():
        if key not in by_key:
            p = paper_from_bib(key, entry)
            papers.append(p)
            by_key[key] = p

    missing = []
    for key, note in curated.items():
        p = by_key.get(key)
        if p is None:
            missing.append(key)
            continue
        note = note or {}
        p.update({k: v for k, v in note.items() if k != "status"})
        p["key"] = key
        p["curated"] = True
        if note.get("status"):
            p["status"] = note["status"]
    for p in papers:
        if p.get("curated"):
            p["role_tags"], p["contribution"] = contribution(p)

    exp = notes.get("experiments") or {}
    for p in papers:
        p.setdefault("curated", False)
        p.setdefault("themes", [])
        p["hidden"] = bool(set(p["texkeys"]) & hidden)
        p["small"] = 0 < p["author_count"] < SMALL_AUTHOR_LIST
        p["experiment"] = experiment_of(p, exp)
    papers.sort(key=lambda p: p["date"], reverse=True)
    return papers, bib, missing, exp.get("order", [])


ROLE_LABELS = {"idea": "Developed the idea", "mentored": "Mentored student"}


def contribution(p):
    """Standard role tags plus free-text details -> (tags, one-line statement)."""
    unknown = set(p.get("roles") or []) - set(ROLE_LABELS) - {"wrote"}
    if unknown:
        raise SystemExit(f"{p['key']}: unknown role(s) {sorted(unknown)}; use wrote, idea, mentored")
    tags = []
    for r in ("wrote", "idea", "mentored"):  # fixed order
        if r in (p.get("roles") or []):
            tags.append((r, ("Wrote" if p["author_count"] == 1 else "Co-wrote") + " the paper"
                         if r == "wrote" else ROLE_LABELS[r]))
    if "idea" in (p.get("roles") or []) and p.get("details"):
        print(f"note: {p['key']}: `details` ignored because `idea` is set")
        p["details"] = None
    parts = [label for _, label in tags] + ([p["details"].rstrip(".")] if p.get("details") else [])
    text = ", ".join(parts[:1] + [x[0].lower() + x[1:] for x in parts[1:]])
    return tags, text


def experiment_of(p, exp):
    """The experiment a collaboration paper belongs to, or None for non-experimental papers."""
    for k in p["texkeys"]:
        if k in (exp.get("assign") or {}):
            return exp["assign"][k]
    aliases = exp.get("aliases") or {}
    tags = {aliases.get(c, c) for c in p["collaborations"]}
    return next((e for e in exp.get("order", []) if e in tags), None)


def slug(name):
    return re.sub(r"[^a-z0-9]+", "", name.lower())


def make_cv_bib(papers, bib):
    """papers.bib for the CV: curated papers, with contribution and keywords injected."""
    out = []
    for p in papers:
        if not p["curated"]:
            continue
        entry = next((bib[k] for k in p["texkeys"] if k in bib), None)
        if entry is None:
            continue
        # Use the curated key so the CV can cite it by the name in papers.yml.
        entry = re.sub(r"^(@\w+\{)\s*[^,\s]+", lambda m: m.group(1) + p["key"], entry, count=1)
        addendum = ""
        if p.get("contribution"):
            addendum += "Contribution: " + to_tex(p["contribution"])
        keyword = f"exp-{slug(p['experiment'])}" if p["experiment"] else p["status"]
        fields = [f'keywords = "{keyword}"']
        if addendum:
            fields.append(f'addendum = "\\newline {addendum}"')
        body = entry.rstrip().rstrip("}").rstrip().rstrip(",")
        out.append(body + ",\n    " + ",\n    ".join(fields) + "\n}\n")
    return "\n".join(out)


# ---------------------------------------------------------------- stats

NUMBER_WORDS = ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]


def words(n):
    return NUMBER_WORDS[n] if n < len(NUMBER_WORDS) else str(n)


def h_index(counts):
    counts = sorted((c or 0 for c in counts), reverse=True)
    return sum(1 for i, c in enumerate(counts, 1) if c >= i)


def compute_stats(papers, talks, teaching, software, github):
    inspire = [p for p in papers if p["recid"]]
    curated = [p for p in papers if p["curated"]]
    sup = {lvl: sum(1 for s in teaching["students"] if s["level"] == lvl) for lvl in ("phd", "masters", "junior")}
    return {
        "records": len(inspire),
        "refereed": sum(1 for p in inspire if p["refereed"]),
        "conference": sum(1 for p in inspire if p["doc_type"] == "conference paper"),
        "curated": len(curated),
        "small": sum(1 for p in inspire if p["small"] and p["status"] != "thesis"),
        "citations": sum(p["citations"] or 0 for p in inspire),
        "h_index": h_index(p["citations"] for p in inspire),
        "citations_main": sum(p["citations"] or 0 for p in curated),
        "h_index_main": h_index(p["citations"] for p in curated),
        "invited_talks": sum(1 for t in talks["talks"] if t["kind"] in ("invited", "seminar")),
        "contributed_talks": sum(1 for t in talks["talks"] if t["kind"] in ("contributed", "poster")),
        "software": len(software),
        "stars": sum((github.get(s.get("repo")) or {}).get("stargazers_count") or 0 for s in software),
        "supervision": {**sup, **{f"{k}_words": words(v) for k, v in sup.items()}},
    }


def render_string(text, ctx):
    """Fill {{ stats.* }} placeholders inside YAML text."""
    return jinja2.Template(text).render(**ctx) if text and "{{" in text else text


def review_report(papers, missing):
    lines = ["# Needs review", ""]
    todo = [p for p in papers if p["recid"] and not p["curated"] and not p["hidden"] and not p["experiment"]
            and p["author_count"] <= REVIEW_MAX_AUTHORS and p["status"] != "thesis"]
    untagged = [p for p in papers if not p["experiment"] and not p["hidden"] and p["author_count"] > REVIEW_MAX_AUTHORS]
    if todo:
        lines += ["Papers on INSPIRE that are neither in `data/papers.yml` (`papers`) nor `hidden`:", ""]
        lines += [f"- [ ] `{p['key']}` ({p['date']}, {p['author_count']} authors) {p['title']} <{p['url']}>" for p in todo]
        lines.append("")
    if untagged:
        lines += ["Large-author papers with no experiment (add them to `experiments.assign` in `data/papers.yml`):", ""]
        lines += [f"- [ ] `{p['key']}` ({p['date']}, {p['author_count']} authors) {p['title']} <{p['url']}>" for p in untagged]
        lines.append("")
    arxiv = json.loads((CACHE / "arxiv.json").read_text(encoding="utf-8"))
    known = {p["arxiv"] for p in papers if p["arxiv"]}
    fresh = [e for e in arxiv if e["id"] not in known]
    if fresh:
        lines += ["Preprints on arXiv not (yet) on INSPIRE:", ""]
        lines += [f"- [ ] arXiv:{e['id']} ({e['published']}) {e['title']}" for e in fresh]
        lines.append("")
    if missing:
        lines += ["Keys in `data/papers.yml` with no matching record:", ""]
        lines += [f"- [ ] `{k}`" for k in missing]
        lines.append("")
    return "\n".join(lines) if len(lines) > 2 else ""


# ---------------------------------------------------------------- charts

def pubs_per_year(papers):
    """Counts per year for the publications chart: three disjoint groups."""
    rows = {}
    for p in papers:
        if not p["recid"] and not p["curated"] or p["status"] == "thesis" or not p["year"] or p["hidden"]:
            continue
        group = "collab" if p["experiment"] else ("main" if p["curated"] else "small")
        rows.setdefault(p["year"], {"main": 0, "small": 0, "collab": 0})[group] += 1
    years = range(min(rows), max(rows) + 1)
    return [{"year": y, **rows.get(y, {"main": 0, "small": 0, "collab": 0})} for y in years]


def metrics_history():
    path = DATA / "metrics.csv"
    return list(csv.DictReader(path.open())) if path.exists() else []


# ---------------------------------------------------------------- render

def fmt_month(value):
    if not value:
        return "Present"
    d = dt.date.fromisoformat(f"{value}-01") if len(str(value)) == 7 else value
    return d.strftime("%b %Y") if hasattr(d, "strftime") else str(value)


def fmt_month_tex(value):
    return fmt_month(value).replace("Present", "Current").replace(" ", r".\ ", 1) if value else "Current"


def site_env():
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(ROOT / "templates" / "site"),
                             autoescape=jinja2.select_autoescape(["html"]),
                             trim_blocks=True, lstrip_blocks=True)
    env.filters["md"] = lambda s: jinja2.utils.markupsafe.Markup(to_html(s))
    env.filters["month"] = fmt_month
    env.filters["json"] = lambda v: jinja2.utils.markupsafe.Markup(json.dumps(v))
    env.tests["self"] = lambda name: SELF in name
    env.tests["contains"] = lambda seq, item: item in (seq or [])
    return env


def cv_env():
    # LaTeX-friendly delimiters: <% block %>, << variable >>, <# comment #>
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(ROOT / "templates" / "cv"),
                             block_start_string="<%", block_end_string="%>",
                             variable_start_string="<<", variable_end_string=">>",
                             comment_start_string="<#", comment_end_string="#>",
                             trim_blocks=True, lstrip_blocks=True, autoescape=False)
    env.filters["tex"] = to_tex
    env.filters["titlecase"] = title_case
    env.filters["month"] = fmt_month_tex
    return env


def build_site(ctx):
    if SITE.exists():
        shutil.rmtree(SITE)
    shutil.copytree(ROOT / "static", SITE)
    env = site_env()
    pages = ["index", "research", "publications", "software", "talks", "cv"]
    for page in pages:
        out = env.get_template(f"{page}.html.j2").render(page=page, **ctx)
        (SITE / f"{page}.html").write_text(out, encoding="utf-8")
    (SITE / ".nojekyll").write_text("")
    print(f"site: {len(pages)} pages -> {SITE.relative_to(ROOT)}/")


def build_cv(ctx, out_dir, private=None):
    if out_dir.exists():
        shutil.rmtree(out_dir)
    (out_dir / "sections").mkdir(parents=True)
    shutil.copy(ROOT / "cv" / "simplecv.sty", out_dir)
    env = cv_env()
    cctx = dict(ctx, private=private)
    for tpl in sorted((ROOT / "templates" / "cv").rglob("*.tex.j2")):
        rel = tpl.relative_to(ROOT / "templates" / "cv")
        if tpl.name == "references.tex.j2" and not private:
            continue
        out = out_dir / str(rel)[: -len(".j2")]
        out.write_text(env.get_template(str(rel)).render(**cctx), encoding="utf-8")
    (out_dir / "papers.bib").write_text(ctx["cv_bib"], encoding="utf-8")
    print(f"cv: sources -> {out_dir.relative_to(ROOT)}/ (compile with latexmk -pdf main.tex)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--private", action="store_true", help="also build the private CV")
    args = ap.parse_args()

    profile, cvdata, talks = load("profile.yml"), load("cv.yml"), load("talks.yml")
    teaching, software, research = load("teaching.yml"), load("software.yml"), load("research.yml")
    github = json.loads((CACHE / "github.json").read_text()) if (CACHE / "github.json").exists() else {}
    papers, bib, missing, exp_order = load_papers()
    talks["talks"].sort(key=lambda t: str(t.get("date") or t["year"]), reverse=True)
    stats = compute_stats(papers, talks, teaching, software["software"], github)

    # Fill computed numbers into prose.
    tctx = {"stats": stats}
    cvdata["highlights"] = [render_string(h, tctx) for h in cvdata["highlights"]]
    teaching["summary"] = render_string(teaching["summary"], tctx)

    by_key = {p["key"]: p for p in papers}
    for s in software["software"]:
        s["github"] = github.get(s.get("repo"), {})
        s["paper_obj"] = by_key.get(s.get("paper"))
    for h in profile.get("highlights") or []:
        h["paper_obj"] = by_key.get(h["paper"])
    for t in research["themes"]:
        t["papers"] = [p for p in papers if t["id"] in p["themes"]]
        for h in t.get("highlights", []):
            h["paper_obj"] = by_key.get(h["paper"])

    today = dt.date.today()
    ctx = {
        "profile": profile, "cv": cvdata, "talks": talks, "teaching": teaching,
        "software": software, "research": research, "stats": stats,
        "papers": papers, "by_key": by_key,
        "curated": [p for p in papers if p["curated"] and not p["experiment"]],
        "experiments": [
            {"name": e, "slug": slug(e),
             "papers": [p for p in papers if p["experiment"] == e and not p["hidden"]],
             "curated": [p for p in papers if p["experiment"] == e and p["curated"]]}
            for e in exp_order if any(p["experiment"] == e for p in papers)],
        "selected": [p for p in papers if p.get("selected")],
        "chart_pubs": pubs_per_year(papers), "metrics": metrics_history(),
        "updated": today.isoformat(), "year": today.year,
        "cv_bib": make_cv_bib(papers, bib),
    }

    build_site(ctx)
    build_cv(ctx, BUILD / "cv")
    if args.private:
        private_path = ROOT / "private" / "private.yml"
        if not private_path.exists():
            raise SystemExit("private/private.yml not found (see private/private.yml.example)")
        build_cv(ctx, BUILD / "cv-private", yaml.safe_load(private_path.read_text(encoding="utf-8")))

    report = review_report(papers, missing)
    (BUILD / "review.md").write_text(report)
    if report:
        print(f"review: {report.count('- [ ]')} item(s) need attention -> build/review.md")


if __name__ == "__main__":
    main()
