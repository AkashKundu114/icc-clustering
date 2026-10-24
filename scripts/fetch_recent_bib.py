import json
import urllib.parse
import urllib.request

queries = [
    "ensemble clustering",
    "consensus clustering",
    "anchor graph clustering bipartite",
    "high-dimensional subspace clustering",
    "unsupervised feature selection clustering",
    "out-of-sample clustering inductive extension",
    "conformal prediction clustering"
]

all_papers = []
seen_dois = set()

# High-quality target journals / publishers
preferred_venues = [
    "IEEE Transactions on Pattern Analysis and Machine Intelligence",
    "IEEE Transactions on Knowledge and Data Engineering",
    "IEEE Transactions on Neural Networks and Learning Systems",
    "IEEE Transactions on Cybernetics",
    "Pattern Recognition",
    "Information Sciences",
    "Data Mining and Knowledge Discovery",
    "Neural Networks",
    "Knowledge-Based Systems",
    "Neurocomputing",
    "Expert Systems with Applications",
    "Bioinformatics",
    "Briefings in Bioinformatics",
    "Machine Learning",
    "ACM Transactions on Knowledge Discovery from Data"
]

for q in queries:
    url = f"https://api.crossref.org/works?query={urllib.parse.quote(q)}&filter=from-pub-date:2024-01-01,type:journal-article&rows=25"
    req = urllib.request.Request(url, headers={'User-Agent': 'AcademicResearcher/1.0 (mailto:kalyan.biltu@gmail.com)'})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data['message']['items']
            for item in items:
                doi = item.get('DOI', '')
                if doi in seen_dois:
                    continue
                seen_dois.add(doi)
                year = item.get('issued', {}).get('date-parts', [[None]])[0][0]
                if year not in (2024, 2025, 2026):
                    continue
                title = item.get('title', [''])[0]
                container = item.get('container-title', [''])[0]
                authors = item.get('author', [])
                if not authors or not title or not container:
                    continue
                author_str = ' and '.join([f"{a.get('family', '')}, {a.get('given', '')}" for a in authors if 'family' in a])
                all_papers.append({
                    'doi': doi,
                    'year': year,
                    'title': title,
                    'journal': container,
                    'authors': author_str,
                    'volume': item.get('volume', ''),
                    'issue': item.get('issue', ''),
                    'page': item.get('page', '')
                })
    except Exception as e:
        print(f"Error querying {q}: {e}")

print(f"Total collected recent papers: {len(all_papers)}")

with open("results/recent_papers.json", "w", encoding="utf-8") as f:
    json.dump(all_papers, f, indent=2)
print("Saved to results/recent_papers.json")

