"""
scripts/search_literature.py

Searches CrossRef, arXiv, and OpenAlex for relevant 2024-2026 literature across topics (a)-(h),
resolves the candidate leads given in the revision protocol, and writes results/lit_candidates.csv.
"""

import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_CSV = ROOT / "results" / "lit_candidates.csv"

CANDIDATES = []

def query_crossref(query, rows=5, filter_year=True):
    print(f"Querying CrossRef: {query[:60]}...")
    url = f"https://api.crossref.org/works?query={urllib.parse.quote(query)}&rows={rows}"
    if filter_year:
        url += "&filter=from-pub-date:2024-01-01"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ICCv2-Revision/1.0 (mailto:akashkundu1152@gmail.com)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            items = data.get("message", {}).get("items", [])
            results = []
            for item in items:
                title = item.get("title", [""])[0] if item.get("title") else ""
                doi = item.get("DOI", "")
                year = None
                date_parts = item.get("issued", {}).get("date-parts", [[None]])
                if date_parts and date_parts[0] and date_parts[0][0]:
                    year = date_parts[0][0]
                container = item.get("container-title", [""])[0] if item.get("container-title") else ""
                volume = item.get("volume", "")
                page = item.get("page", item.get("article-number", ""))
                authors = []
                for a in item.get("author", []):
                    fam = a.get("family", "")
                    giv = a.get("given", "")
                    if fam:
                        authors.append(f"{fam}, {giv}" if giv else fam)
                url_link = item.get("URL", f"https://doi.org/{doi}")
                results.append({
                    "title": title,
                    "doi": doi,
                    "year": year,
                    "venue": container,
                    "volume": volume,
                    "pages": page,
                    "authors": "; ".join(authors),
                    "url": url_link,
                    "source": "CrossRef"
                })
            return results
    except Exception as e:
        print(f"  CrossRef error: {e}")
        return []

def query_arxiv(query, max_results=5):
    print(f"Querying arXiv: {query[:60]}...")
    url = f"http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(query)}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ICCv2-Revision/1.0 (mailto:akashkundu1152@gmail.com)"}
    )
    try:
        import xml.etree.ElementTree as ET
        with urllib.request.urlopen(req, timeout=12) as resp:
            tree = ET.fromstring(resp.read().decode("utf-8"))
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            results = []
            for entry in tree.findall("atom:entry", ns):
                title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
                published = entry.find("atom:published", ns).text[:4]
                arxiv_id = entry.find("atom:id", ns).text.split("/abs/")[-1]
                authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
                summary = entry.find("atom:summary", ns).text.strip().replace("\n", " ")
                results.append({
                    "title": title,
                    "doi": f"arXiv:{arxiv_id}",
                    "year": published,
                    "venue": "arXiv preprint",
                    "volume": "",
                    "pages": "",
                    "authors": "; ".join(authors),
                    "url": f"https://arxiv.org/abs/{arxiv_id}",
                    "source": "arXiv",
                    "abstract": summary[:300]
                })
            return results
    except Exception as e:
        print(f"  arXiv error: {e}")
        return []

if __name__ == "__main__":
    print("Starting literature search...")
    # 1. Investigate the 12 candidate leads
    leads = [
        "Fast Clustering with Anchor Guidance",
        "CoHiRF",
        "Interpreting the Curse of Dimensionality from Distance Concentration",
        "Dynamic Anchor-Based Ensemble Clustering via Hypergraph Reconstruction",
        "RANGE ensemble clustering",
        "A Structured Bipartite Graph Learning method for ensemble clustering",
        "Anchor-based fast spectral ensemble clustering",
        "Efficient Co-Clustering via Bipartite Graph Factorization",
        "Fast Co-clustering via Anchor-guided Label Spreading",
        "Normalized cut co-clustering with out-of-sample extension",
        "A comprehensive survey on deep clustering: taxonomy, challenges, and future directions",
        "Comprehensive analysis of clustering algorithms: exploring limitations and innovative solutions"
    ]
    
    found_leads = []
    for lead in leads:
        res = query_crossref(lead, rows=3, filter_year=False)
        if res:
            found_leads.extend(res)
        time.sleep(0.5)

    print(f"Found {len(found_leads)} candidate entries from leads.")
