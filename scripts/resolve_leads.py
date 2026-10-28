"""
scripts/resolve_leads.py

Resolves metadata for the 12 specific leads using CrossRef and arXiv APIs.
"""

import json
import urllib.parse
import urllib.request

def fetch_json(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ICCv2-Revision/1.0 (mailto:akashkundu1152@gmail.com)"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def check_doi(doi):
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
    try:
        data = fetch_json(url)
        item = data.get("message", {})
        title = item.get("title", [""])[0]
        issued = item.get("issued", {}).get("date-parts", [[None]])[0]
        authors = [f"{a.get('family', '')}, {a.get('given', '')}" for a in item.get("author", [])]
        container = item.get("container-title", [""])[0]
        vol = item.get("volume", "")
        iss = item.get("issue", "")
        page = item.get("page", item.get("article-number", ""))
        print(f"=== DOI: {doi} ===")
        print(f"Title: {title}")
        print(f"Authors: {'; '.join(authors)}")
        print(f"Venue: {container} | Vol: {vol} | Issue: {iss} | Pages: {page} | Year: {issued[0]}")
        return item
    except Exception as e:
        print(f"DOI {doi} failed: {e}")
        return None

def search_crossref_title(query):
    url = f"https://api.crossref.org/works?query.title={urllib.parse.quote(query)}&rows=3"
    try:
        data = fetch_json(url)
        items = data.get("message", {}).get("items", [])
        print(f"\n--- Search: {query} ---")
        for item in items:
            title = item.get("title", [""])[0]
            doi = item.get("DOI", "")
            issued = item.get("issued", {}).get("date-parts", [[None]])[0]
            authors = [f"{a.get('family', '')}, {a.get('given', '')}" for a in item.get("author", [])]
            container = item.get("container-title", [""])[0]
            vol = item.get("volume", "")
            iss = item.get("issue", "")
            page = item.get("page", item.get("article-number", ""))
            print(f"DOI: {doi} | Year: {issued[0]} | {container} {vol}({iss}): {page}")
            print(f"Title: {title}")
            print(f"Authors: {'; '.join(authors[:4])} (total {len(authors)})")
    except Exception as e:
        print(f"Search failed for {query}: {e}")

if __name__ == "__main__":
    print("Checking specific DOIs...")
    # Lead 1: Nie TPAMI
    check_doi("10.1109/TPAMI.2023.3318603")
    
    # Lead 4: IJCAI 2025
    check_doi("10.24963/IJCAI.2025/750")

    # Lead 12: Wani PeerJ
    check_doi("10.7717/peerj-cs.2286")

    # Searches for titles
    search_crossref_title("Fast Co-clustering via Anchor-guided Label Spreading")
    search_crossref_title("A Structured Bipartite Graph Learning method for ensemble clustering")
    search_crossref_title("Anchor-based fast spectral ensemble clustering")
    search_crossref_title("Efficient Co-Clustering via Bipartite Graph Factorization")
    search_crossref_title("Normalized cut co-clustering with out-of-sample extension")
    search_crossref_title("A comprehensive survey on deep clustering: taxonomy, challenges, and future directions")
