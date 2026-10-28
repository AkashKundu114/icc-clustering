#!/usr/bin/env python3
"""Verify BibTeX entries against CrossRef / arXiv. Reports only what the APIs return."""
import argparse, csv, re, sys, time, unicodedata, difflib, os
import xml.etree.ElementTree as ET
import requests, bibtexparser

MAILTO = "akashkundu1152@gmail.com"   # set this
HDR = {"User-Agent": f"bib-verifier/1.0 (mailto:{MAILTO})"}
ATOM = {"a": "http://www.w3.org/2005/Atom", "ax": "http://arxiv.org/schemas/atom"}
HARD = {"TITLE", "FIRST_AUTHOR", "YEAR", "VOLUME", "PAGES"}

def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", re.sub(r"[{}\\$]", "", s.lower())).split())

def sim(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()

def get(url, params=None, tries=3):
    for i in range(tries):
        try:
            r = requests.get(url, params=params, headers=HDR, timeout=30)
            if r.status_code == 200: return r
            if r.status_code == 404: return None
        except requests.RequestException:
            pass
        time.sleep(2 * (i + 1))
    return None

def cr_rec(m):
    dp = (m.get("issued", {}).get("date-parts") or [[None]])[0]
    return dict(title=(m.get("title") or [""])[0],
                authors=[a.get("family") or a.get("name", "") for a in m.get("author", [])],
                venue=(m.get("container-title") or [""])[0], year=dp[0],
                volume=m.get("volume"), issue=m.get("issue"),
                pages=m.get("page") or m.get("article-number"),
                doi=m.get("DOI"), type=m.get("type"), source="crossref")

def crossref_by_doi(doi):
    r = get(f"https://api.crossref.org/works/{doi}")
    return cr_rec(r.json()["message"]) if r else None

def crossref_by_title(title, first_author=""):
    r = get("https://api.crossref.org/works",
            {"query.bibliographic": f"{title} {first_author}".strip(), "rows": 3})
    if not r: return None
    recs = [cr_rec(i) for i in r.json()["message"]["items"]]
    return max(recs, key=lambda x: sim(title, x["title"])) if recs else None

def arxiv_rec(aid):
    aid = re.sub(r"v\d+$", "", aid or "")
    r = get("http://export.arxiv.org/api/query", {"id_list": aid})
    if not r: return None
    e = ET.fromstring(r.text).find("a:entry", ATOM)
    if e is None: return None
    title = " ".join((e.find("a:title", ATOM).text or "").split())
    if title.lower() == "error": return None
    authors = [(a.find("a:name", ATOM).text or "").split()[-1] for a in e.findall("a:author", ATOM)]
    jr, doi = e.find("ax:journal_ref", ATOM), e.find("ax:doi", ATOM)
    return dict(title=title, authors=authors, venue="arXiv",
                year=int(e.find("a:published", ATOM).text[:4]), volume=None, issue=None,
                pages=None, doi=doi.text if doi is not None else None, type="posted-content",
                journal_ref=jr.text if jr is not None else None, source="arxiv", eprint=aid)

def last_names(field):
    out = []
    for a in re.split(r"\s+and\s+", field or ""):
        a = a.strip()
        if a and a.lower() != "others":
            out.append(norm(a.split(",")[0] if "," in a else a.split()[-1]))
    return out

def pp(s):
    return re.sub(r"[–—-]+", "-", str(s or "")).replace(" ", "")

def compare(e, rec):
    f = []
    if sim(e.get("title", ""), rec["title"]) < 0.90: f.append("TITLE")
    ba, ra = last_names(e.get("author", "")), [norm(x) for x in rec["authors"]]
    if ba and ra and ba[0] != ra[0]: f.append("FIRST_AUTHOR")
    if ba and ra and "others" not in e.get("author", "").lower() and len(ba) != len(ra):
        f.append("AUTHOR_COUNT")
    if e.get("year") and rec["year"] and int(e["year"]) != int(rec["year"]): f.append("YEAR")
    if rec["volume"] and e.get("volume") and str(e["volume"]) != str(rec["volume"]): f.append("VOLUME")
    if rec["pages"] and e.get("pages") and pp(e["pages"]) != pp(rec["pages"]): f.append("PAGES")
    ven = e.get("journal") or e.get("booktitle") or ""
    if rec["venue"] and ven and sim(ven, rec["venue"]) < 0.6: f.append("VENUE")
    if rec["source"] == "arxiv" and (rec.get("doi") or rec.get("journal_ref")):
        f.append("PUBLISHED_VERSION_EXISTS")
    return f

def to_bibtex(rec, key):
    t = {"journal-article": "article", "proceedings-article": "inproceedings"}.get(rec["type"], "misc")
    au = " and ".join(rec["authors"])
    lines = [f"@{t}{{{key},", f"  title = {{{rec['title']}}},", f"  author = {{{au}}},",
             f"  year = {{{rec['year']}}},"]
    if rec["venue"] and rec["source"] == "crossref":
        lines.append(f"  {'journal' if t == 'article' else 'booktitle'} = {{{rec['venue']}}},")
    for k in ("volume", "issue", "pages"):
        if rec.get(k): lines.append(f"  {k if k != 'issue' else 'number'} = {{{rec[k]}}},")
    if rec.get("doi"): lines.append(f"  doi = {{{rec['doi']}}},")
    if rec["source"] == "arxiv":
        lines += [f"  eprint = {{{rec['eprint']}}},", "  archivePrefix = {arXiv},"]
    return "\n".join(lines) + "\n}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bib", nargs="?")
    ap.add_argument("--out", default="results/refs_report.csv")
    ap.add_argument("--manual", default="refs_manual.csv")  # key,url,verified_by,date
    ap.add_argument("--doi"); ap.add_argument("--arxiv"); ap.add_argument("--title")
    ap.add_argument("--bibtex", action="store_true"); ap.add_argument("--key", default="key")
    a = ap.parse_args()

    if a.doi or a.arxiv or a.title:
        rec = (crossref_by_doi(a.doi) if a.doi else arxiv_rec(a.arxiv) if a.arxiv
               else crossref_by_title(a.title))
        if not rec: print("NOT FOUND"); sys.exit(1)
        print(to_bibtex(rec, a.key) if a.bibtex else rec); return

    manual = {}
    if os.path.exists(a.manual):
        manual = {r["key"]: r for r in csv.DictReader(open(a.manual, encoding="utf-8"))}
    db = bibtexparser.load(open(a.bib, encoding="utf-8"))
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    rows, seen = [], {}
    for e in db.entries:
        key = e["ID"]
        doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", e.get("doi", "")).strip()
        aid = e.get("eprint", "")
        rec, how = None, ""
        if doi: rec, how = crossref_by_doi(doi), "doi"
        elif aid: rec, how = arxiv_rec(aid), "arxiv"
        elif key in manual: how = "manual"
        else:
            rec = crossref_by_title(e.get("title", ""), last_names(e.get("author", ""))[0:1] and
                                    e.get("author", "").split(",")[0]); how = "title-search"
        flags = []
        if how == "manual": status = "MANUAL"
        elif not rec: status = "NOT_FOUND"
        else:
            flags = compare(e, rec)
            status = "MISMATCH" if HARD & set(flags) else "WARN" if flags else "OK"
            if how == "title-search" and status == "OK": status = "CHECK_ID"
        dup = seen.get(norm(e.get("title", "")))
        if dup: flags.append(f"DUPLICATE_OF_{dup}")
        seen[norm(e.get("title", ""))] = key
        r = rec or {}
        rows.append(dict(key=key, how=how, status=status, flags=";".join(flags),
                         bib_title=e.get("title", ""), api_title=r.get("title", ""),
                         bib_year=e.get("year", ""), api_year=r.get("year", ""),
                         bib_vol=e.get("volume", ""), api_vol=r.get("volume", ""),
                         bib_pages=e.get("pages", ""), api_pages=r.get("pages", ""),
                         api_doi=r.get("doi", "")))
        time.sleep(0.3)
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    counts = {}
    for r in rows: counts[r["status"]] = counts.get(r["status"], 0) + 1
    print(counts)
    bad = [r["key"] for r in rows if r["status"] in ("MISMATCH", "NOT_FOUND", "CHECK_ID")]
    if bad: print("FAIL:", ", ".join(bad)); sys.exit(1)

if __name__ == "__main__":
    main()
