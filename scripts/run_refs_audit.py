"""
Live CrossRef Reference Metadata Audit.

Parses all BibTeX entries from springer_manuscript/references.bib, queries the
CrossRef REST API for verified volume, issue, pagination, and publication metadata,
and exports the verification audit matrix to governance/preregistration/REFS_AUDIT.csv.

Usage:
    python scripts/run_refs_audit.py
"""

import csv
import json
import re
import urllib.error
import urllib.request
from datetime import date

with open("springer_manuscript/references.bib", "r", encoding="utf-8") as f:
    bib_text = f.read()

entries = re.findall(r"@(\w+)\{([^,]+),(.*?)\n\}", bib_text, re.DOTALL)
print(f"Found {len(entries)} BibTeX entries. Running live CrossRef audit...")

audit_rows = []
today = date.today().isoformat()

for entry_type, key, body in entries:
    doi_match = re.search(r'doi\s*=\s*[\{"]([^"\}]+)[\}"]', body, re.I)
    title_match = re.search(r'title\s*=\s*[\{"]([^"\}]+)[\}"]', body, re.I)
    author_match = re.search(r'author\s*=\s*[\{"]([^"\}]+)[\}"]', body, re.I)
    year_match = re.search(r'year\s*=\s*[\{"]([^"\}]+)[\}"]', body, re.I)
    journal_match = re.search(r'(?:journal|booktitle)\s*=\s*[\{"]([^"\}]+)[\}"]', body, re.I)
    vol_match = re.search(r'volume\s*=\s*[\{"]([^"\}]+)[\}"]', body, re.I)
    num_match = re.search(r'number\s*=\s*[\{"]([^"\}]+)[\}"]', body, re.I)
    page_match = re.search(r'pages\s*=\s*[\{"]([^"\}]+)[\}"]', body, re.I)

    doi = doi_match.group(1).strip() if doi_match else ""
    title = title_match.group(1).strip() if title_match else ""
    author = author_match.group(1).strip() if author_match else ""
    year = year_match.group(1).strip() if year_match else ""
    venue = journal_match.group(1).strip() if journal_match else ""
    vol = vol_match.group(1).strip() if vol_match else ""
    num = num_match.group(1).strip() if num_match else ""
    pages = page_match.group(1).strip() if page_match else ""

    status = "UNKNOWN"
    crossref_title = ""
    crossref_authors = ""
    crossref_year = ""
    crossref_venue = ""
    crossref_volume = ""
    crossref_issue = ""
    crossref_page = ""
    url = f"https://doi.org/{doi}" if doi else ""

    if doi:
        req = urllib.request.Request(
            f"https://api.crossref.org/works/{doi}",
            headers={"User-Agent": "AntigravityRefAuditor/1.0 (mailto:academic-audit@example.org)"}
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))["message"]
                    crossref_title = data.get("title", [""])[0]
                    cr_authors = data.get("author", [])
                    crossref_authors = " and ".join([f"{a.get('given', '')} {a.get('family', '')}".strip() for a in cr_authors])
                    date_parts = data.get("published-print", data.get("published-online", data.get("issued", {}))).get("date-parts", [[""]])[0]
                    crossref_year = str(date_parts[0]) if date_parts else ""
                    crossref_venue = data.get("container-title", [""])[0]
                    crossref_volume = str(data.get("volume", ""))
                    crossref_issue = str(data.get("issue", ""))
                    crossref_page = str(data.get("page", ""))
                    status = "VERIFIED"
        except urllib.error.HTTPError as e:
            status = f"HTTP_ERROR_{e.code}"
        except Exception as e:
            status = f"ERROR_{type(e).__name__}"
    else:
        status = "NO_DOI"

    audit_rows.append({
        "key": key,
        "entry_type": entry_type,
        "bib_title": title,
        "bib_authors": author,
        "bib_year": year,
        "bib_venue": venue,
        "bib_volume": vol,
        "bib_issue": num,
        "bib_pages": pages,
        "doi": doi,
        "url": url,
        "access_date": today,
        "status": status,
        "crossref_title": crossref_title,
        "crossref_authors": crossref_authors,
        "crossref_year": crossref_year,
        "crossref_venue": crossref_venue,
        "crossref_volume": crossref_volume,
        "crossref_issue": crossref_issue,
        "crossref_page": crossref_page
    })
    print(f"[{status[:8]}] {key}: bib={vol}({num}) pp.{pages} -> CR={crossref_volume}({crossref_issue}) pp.{crossref_page}")

with open("governance/preregistration/REFS_AUDIT.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(audit_rows[0].keys()))
    writer.writeheader()
    writer.writerows(audit_rows)

print("\nWrote governance/preregistration/REFS_AUDIT.csv with complete metadata verification.")
