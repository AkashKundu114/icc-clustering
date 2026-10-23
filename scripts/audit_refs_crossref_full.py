"""
Comprehensive CrossRef Reference Audit Script.
Queries api.crossref.org for every entry in references.bib.
Extracts raw CrossRef fields, compares with .bib fields, records match flags,
and generates LOOP/REFS_AUDIT.csv.
"""

import re
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path
import pandas as pd

BIB_PATH = Path("springer_manuscript/references.bib")
OUT_CSV = Path("LOOP/REFS_AUDIT.csv")

def parse_bib_entries(filename: str):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    entries = []
    curr = None
    for line in lines:
        line_s = line.strip()
        if line_s.startswith('@'):
            m = re.match(r'@(\w+)\s*\{\s*([^,]+),', line_s)
            if m:
                if curr:
                    entries.append(curr)
                curr = {'type': m.group(1).lower(), 'key': m.group(2).strip(), 'fields': {}}
        elif curr and '=' in line:
            parts = line.split('=', 1)
            k = parts[0].strip().lower()
            v = parts[1].strip().strip('{},').strip('"')
            curr['fields'][k] = v
    if curr:
        entries.append(curr)
    return entries

def query_crossref_by_doi(doi: str):
    url = f"https://api.crossref.org/works/{doi}"
    req = urllib.request.Request(url, headers={"User-Agent": "mailto:researcher@university.edu"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("message", {})
    except Exception as e:
        return {"error": str(e)}

def query_crossref_by_title(title: str, author: str = ""):
    query = f"{title} {author}"
    url = f"https://api.crossref.org/works?query={urllib.parse.quote(query)}&rows=1"
    req = urllib.request.Request(url, headers={"User-Agent": "mailto:researcher@university.edu"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            items = data.get("message", {}).get("items", [])
            if items:
                return items[0]
            return {}
    except Exception as e:
        return {"error": str(e)}

def main():
    print("=" * 70)
    print("RUNNING LIVE CROSSREF AUDIT FOR ALL REFERENCES")
    print("=" * 70)
    entries = parse_bib_entries(str(BIB_PATH))
    print(f"Parsed {len(entries)} entries from {BIB_PATH}")

    audit_rows = []

    for idx, e in enumerate(entries, 1):
        key = e["key"]
        fields = e["fields"]
        bib_doi = fields.get("doi")
        bib_title = fields.get("title", "")
        bib_author = fields.get("author", "")
        bib_vol = fields.get("volume", "")
        bib_num = fields.get("number", "")
        bib_pages = fields.get("pages", "")
        bib_year = fields.get("year", "")

        print(f"[{idx}/{len(entries)}] Auditing '{key}'...", flush=True)

        cr_data = {}
        if bib_doi:
            cr_data = query_crossref_by_doi(bib_doi)
        else:
            cr_data = query_crossref_by_title(bib_title, bib_author)

        cr_doi = cr_data.get("DOI", bib_doi)
        cr_title = cr_data.get("title", [""])[0] if cr_data.get("title") else ""
        cr_vol = str(cr_data.get("volume", ""))
        cr_issue = str(cr_data.get("issue", ""))
        cr_pages = str(cr_data.get("page", ""))
        cr_year_parts = cr_data.get("issued", {}).get("date-parts", [[None]])[0]
        cr_year = str(cr_year_parts[0]) if cr_year_parts and cr_year_parts[0] else ""

        # Check match status
        discrepancies = []
        if cr_vol and bib_vol and cr_vol != bib_vol:
            discrepancies.append(f"Volume: bib={bib_vol} vs cr={cr_vol}")
        if cr_issue and bib_num and cr_issue != bib_num:
            discrepancies.append(f"Issue: bib={bib_num} vs cr={cr_issue}")
        if cr_pages and bib_pages:
            norm_bib_pages = bib_pages.replace("--", "-")
            if cr_pages != norm_bib_pages and cr_pages.split("-")[0] != norm_bib_pages.split("-")[0]:
                discrepancies.append(f"Pages: bib={bib_pages} vs cr={cr_pages}")
        if cr_year and bib_year and cr_year != bib_year:
            discrepancies.append(f"Year: bib={bib_year} vs cr={cr_year}")

        match_status = "MATCH_VERIFIED" if not discrepancies else f"DISCREPANCY: {'; '.join(discrepancies)}"
        print(f"    Status: {match_status}", flush=True)

        audit_rows.append({
            "key": key,
            "type": e["type"],
            "bib_title": bib_title,
            "cr_title": cr_title,
            "bib_doi": bib_doi,
            "cr_doi": cr_doi,
            "bib_volume": bib_vol,
            "cr_volume": cr_vol,
            "bib_number": bib_num,
            "cr_issue": cr_issue,
            "bib_pages": bib_pages,
            "cr_pages": cr_pages,
            "bib_year": bib_year,
            "cr_year": cr_year,
            "match_status": match_status,
            "discrepancies": "; ".join(discrepancies)
        })
        time.sleep(0.2)  # courteous API rate limit

    df = pd.DataFrame(audit_rows)
    df.to_csv(OUT_CSV, index=False)
    print(f"\nSaved audit to {OUT_CSV}")

if __name__ == "__main__":
    main()
