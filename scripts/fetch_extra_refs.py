import urllib.request
import json

dois = [
    ("10.1109/tkde.2026.3734593", "tkde2026fast", "Sec 2.2", "Fast bipartite graph clustering"),
    ("10.1093/biomet/asae059", "biometrika2024bayesian", "Sec 2.3", "Bayesian clustering in high dimensions"),
    ("10.1016/j.patcog.2026.113097", "patcog2026consensus", "Sec 2.2", "Consensus-aware sparse subspace clustering"),
    ("10.1016/j.ins.2025.122349", "ins2025fast", "Sec 2.2", "Fast adaptive anchor graph co-clustering")
]

headers = {'User-Agent': 'AntigravityRefVerifier/2.0 (mailto:akashkundu1152@gmail.com)'}

results = []
for doi, key, sec, why in dois:
    url = f'https://api.crossref.org/works/{doi}'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            msg = data.get('message', {})
            title = msg.get('title', [''])[0]
            authors_list = msg.get('author', [])
            authors = ' and '.join([f"{a.get('given', '')} {a.get('family', '')}".strip() for a in authors_list[:6]])
            venue = msg.get('container-title', [''])[0]
            year = msg.get('published-print', msg.get('published-online', msg.get('issued', {}))).get('date-parts', [[None]])[0][0]
            vol = msg.get('volume', '')
            page = msg.get('page', '')
            res = {
                'key': key,
                'title': title,
                'authors': authors,
                'venue': venue,
                'year': str(year),
                'volume': str(vol),
                'pages': str(page),
                'doi': doi,
                'section': sec,
                'why': why
            }
            results.append(res)
            print(f"SUCCESS: {key} ({year}) -> {title} | {venue}")
    except Exception as e:
        print(f"FAILED {doi}: {e}")

with open("results/extra_verified.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
