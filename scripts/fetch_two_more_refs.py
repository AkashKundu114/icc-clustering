import urllib.request, urllib.parse, json

headers = {'User-Agent': 'AntigravityRefVerifier/2.0 (mailto:akashkundu1152@gmail.com)'}

q_params = urllib.parse.urlencode({
    'query.bibliographic': 'ensemble clustering anchor graph',
    'filter': 'from-pub-date:2024-01-01',
    'rows': 10
})
url = f'https://api.crossref.org/works?{q_params}'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

items = data.get('message', {}).get('items', [])
print(f"Found {len(items)} items:")
for item in items:
    t = item.get('title', [''])[0]
    doi = item.get('DOI', '')
    venue = item.get('container-title', [''])[0]
    year = item.get('issued', {}).get('date-parts', [[None]])[0][0]
    authors = ' and '.join([f"{a.get('given', '')} {a.get('family', '')}".strip() for a in item.get('author', [])[:3]])
    print(f"[{year}] {t} | {venue} | DOI: {doi} | {authors}")
