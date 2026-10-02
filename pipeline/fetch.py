"""Fetch public data (INSPIRE, arXiv, GitHub) into data/cache/.

Run weekly by CI and on demand locally:  python pipeline/fetch.py
Also appends one row per day to data/metrics.csv so citation and star counts
build up a history over time.
"""

import csv
import datetime as dt
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CACHE = DATA / "cache"
INSPIRE = "https://inspirehep.net/api/literature"
UA = {"User-Agent": "MeighenBergerS.github.io site builder (https://github.com/MeighenBergerS)"}

# Collaboration papers carry hundreds of authors; only keep author lists below this.
AUTHOR_LIST_MAX = 30

LIGHT_FIELDS = [
    "control_number", "texkeys", "titles", "arxiv_eprints", "dois", "publication_info",
    "document_type", "author_count", "collaborations", "citation_count",
    "citation_count_without_self_citations", "earliest_date", "refereed",
]


def get(url, accept=None):
    headers = dict(UA)
    if accept:
        headers["Accept"] = accept
    if "api.github.com" in url and os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as r:
                return r.read().decode("utf-8")
        except Exception as exc:  # network hiccups and rate limits: back off and retry
            if attempt == 3 or getattr(exc, "code", None) == 404:
                raise
            print(f"  retry {url[:80]}... ({exc})", file=sys.stderr)
            time.sleep(5 * (attempt + 1))


def inspire_query(q, fields=None, fmt=None):
    params = {"q": q, "size": 500, "sort": "mostrecent"}
    if fields:
        params["fields"] = ",".join(fields)
    if fmt:
        params["format"] = fmt
    return get(f"{INSPIRE}?{urllib.parse.urlencode(params)}")


def fetch_inspire(bai, curated_keys):
    print("INSPIRE: all records")
    records = json.loads(inspire_query(f"a {bai}", LIGHT_FIELDS))["hits"]["hits"]
    records = {r["metadata"]["control_number"]: r["metadata"] for r in records}

    print(f"INSPIRE: author lists for papers with <= {AUTHOR_LIST_MAX} authors")
    small = json.loads(inspire_query(f"a {bai} and ac 1->{AUTHOR_LIST_MAX}", ["control_number", "authors.full_name"]))
    for r in small["hits"]["hits"]:
        m = r["metadata"]
        records[m["control_number"]]["authors"] = [a["full_name"] for a in m.get("authors", [])]

    # BibTeX for everything the CV may cite: small-author papers plus curated keys.
    keys = {k for m in records.values() if m.get("author_count", 999) <= AUTHOR_LIST_MAX for k in m["texkeys"][:1]}
    keys |= {k for k in curated_keys if any(k in m["texkeys"] for m in records.values())}
    print(f"INSPIRE: BibTeX for {len(keys)} records")
    bib = inspire_query(" or ".join(f"texkeys:{k}" for k in sorted(keys)), fmt="bibtex")

    out = sorted(records.values(), key=lambda m: m.get("earliest_date", ""), reverse=True)
    (CACHE / "inspire.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    (CACHE / "inspire.bib").write_text(bib)
    return out


def fetch_arxiv():
    """Recent arXiv listings, to catch preprints INSPIRE has not indexed yet."""
    print("arXiv: author listing")
    q = urllib.parse.urlencode({"search_query": 'au:"Meighen-Berger"', "sortBy": "submittedDate",
                                "sortOrder": "descending", "max_results": 50})
    root = ET.fromstring(get(f"https://export.arxiv.org/api/query?{q}"))
    ns = {"a": "http://www.w3.org/2005/Atom"}
    entries = []
    for e in root.findall("a:entry", ns):
        arxiv_id = e.find("a:id", ns).text.rsplit("/abs/", 1)[-1].split("v")[0]
        entries.append({
            "id": arxiv_id,
            "title": " ".join(e.find("a:title", ns).text.split()),
            "published": e.find("a:published", ns).text[:10],
            "authors": [a.find("a:name", ns).text for a in e.findall("a:author", ns)],
        })
        if len(entries[-1]["authors"]) > AUTHOR_LIST_MAX:
            entries[-1]["authors"] = entries[-1]["authors"][:3] + ["et al."]
    (CACHE / "arxiv.json").write_text(json.dumps(entries, indent=1, ensure_ascii=False) + "\n")
    return entries


def fetch_github(software):
    out = {}
    for s in software:
        repo = s.get("repo")
        if not repo:
            continue
        print(f"GitHub: {repo}")
        try:
            r = json.loads(get(f"https://api.github.com/repos/{repo}", "application/vnd.github+json"))
        except Exception as exc:
            print(f"  skipped ({exc})", file=sys.stderr)
            continue
        info = {k: r.get(k) for k in ("stargazers_count", "forks_count", "pushed_at", "html_url", "description")}
        try:
            rel = json.loads(get(f"https://api.github.com/repos/{repo}/releases/latest", "application/vnd.github+json"))
            info["latest_release"] = {"tag": rel.get("tag_name"), "date": (rel.get("published_at") or "")[:10]}
        except Exception:
            info["latest_release"] = None
        out[repo] = info
    (CACHE / "github.json").write_text(json.dumps(out, indent=1) + "\n")
    return out


def h_index(counts):
    counts = sorted(counts, reverse=True)
    return sum(1 for i, c in enumerate(counts, 1) if c >= i)


def snapshot(records, curated_keys, github):
    """Append today's numbers to data/metrics.csv (one row per day)."""
    path = DATA / "metrics.csv"
    cites = [m.get("citation_count", 0) for m in records]
    main = [m.get("citation_count", 0) for m in records if set(m["texkeys"]) & curated_keys]
    row = {
        "date": dt.date.today().isoformat(),
        "records": len(records),
        "citations": sum(cites),
        "h_index": h_index(cites),
        "citations_main": sum(main),
        "h_index_main": h_index(main),
        "stars": sum(g.get("stargazers_count") or 0 for g in github.values()),
    }
    rows = list(csv.DictReader(path.open())) if path.exists() else []
    rows = [r for r in rows if r["date"] != row["date"]] + [row]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(row))
        w.writeheader()
        w.writerows(rows)
    print(f"metrics: {row}")


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    profile = yaml.safe_load((DATA / "profile.yml").read_text())
    curated = set(yaml.safe_load((DATA / "papers.yml").read_text())["papers"])
    software = yaml.safe_load((DATA / "software.yml").read_text())["software"]

    records = fetch_inspire(profile["ids"]["inspire_bai"], curated)
    fetch_arxiv()
    github = fetch_github(software)
    snapshot(records, curated, github)


if __name__ == "__main__":
    main()
