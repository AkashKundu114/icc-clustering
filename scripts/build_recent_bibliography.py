import json

with open('results/recent_papers.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

keywords = [
    'cluster', 'consensus', 'ensemble', 'subspace', 'anchor', 
    'bipartite', 'feature selection', 'out-of-sample', 'conformal', 
    'spectral', 'graph', 'high-dimensional', 'rough set', 'contrastive'
]

selected = []
seen_titles = set()

for p in papers:
    t = p['title'].lower()
    j = p['journal'].lower()
    if t in seen_titles:
        continue
    if any(k in t for k in keywords) and p['year'] in (2024, 2025, 2026):
        # Exclude irrelevant domains like power systems, agriculture, etc.
        irrelevant = ['power system', 'agriculture', 'traffic', 'wind', 'battery', 'solar', 'cricket', 'concrete']
        if any(irr in t or irr in j for irr in irrelevant):
            continue
        seen_titles.add(t)
        selected.append(p)

print(f"Filtered {len(selected)} high-quality recent papers (2024-2026)")

# Sort by venue prominence and year
def venue_rank(p):
    j = p['journal'].lower()
    if 'ieee transactions' in j:
        return 0
    if 'pattern recognition' in j or 'information sciences' in j:
        return 1
    if 'knowledge-based systems' in j or 'neural networks' in j or 'expert systems' in j:
        return 2
    if 'neurocomputing' in j or 'information fusion' in j or 'applied intelligence' in j:
        return 3
    return 4

selected.sort(key=lambda p: (venue_rank(p), -p['year']))

print("\nTop 30 papers:")
for i, p in enumerate(selected[:30]):
    first_author = p['authors'].split(' and ')[0]
    print(f"{i+1:2d}. [{p['year']}] {first_author}: {p['title'][:65]}... ({p['journal']})")
