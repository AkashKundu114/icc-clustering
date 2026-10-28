import json
import re
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parent.parent

# 1. Load verified 2024-2026 references
with open(ROOT / "results" / "verified_2024_2026.json", "r", encoding="utf-8") as f:
    v1 = json.load(f)

with open(ROOT / "results" / "extra_verified.json", "r", encoding="utf-8") as f:
    v2 = json.load(f)

# Filter out chen2024inductive (mismatched query)
v_all = [e for e in v1 if e.get("key") != "chen2024inductive"] + v2

# Add the two high-tier verified PR/Neurocomputing papers
v_all.append({
    "key": "li2026rfag",
    "title": "RFAG: Random forest clustering based on anchor graph",
    "authors": "Jinyu Li and Congyu Wang and Mingjing Du",
    "venue": "Pattern Recognition",
    "volume": "172",
    "pages": "112997",
    "year": "2026",
    "doi": "10.1016/j.patcog.2025.112997",
    "section": "Sec 2.2",
    "why": "Random forest clustering based on anchor graph"
})
v_all.append({
    "key": "lei2024anchor",
    "title": "Anchor graph-based multiview spectral clustering",
    "authors": "Yu Lei and Zuoyuan Niu and Qianqian Wang",
    "venue": "Neurocomputing",
    "volume": "576",
    "pages": "127579",
    "year": "2024",
    "doi": "10.1016/j.neucom.2024.127579",
    "section": "Sec 2.2",
    "why": "Anchor graph-based multiview spectral clustering"
})

print(f"Total new 2024-2026 entries to add: {len(v_all)}")

# Save updated refs_map.csv
with open(ROOT / "results" / "refs_map.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["bibkey", "section", "sentence", "why"])
    writer.writeheader()
    for e in v_all:
        writer.writerow({
            "bibkey": e["key"],
            "section": e.get("section", "Sec 2.2"),
            "sentence": e.get("why", ""),
            "why": e.get("why", "")
        })

print("Updated results/refs_map.csv with all verified references.")

# Read existing references.bib
with open(ROOT / "paper" / "references.bib", "r", encoding="utf-8") as f:
    orig_bib = f.read()

# Build BibTeX entries for verified recent papers
new_bib_entries = []
seen_keys = set()

# Parse existing keys
existing_keys = set(re.findall(r"@\w+\s*\{\s*([^,]+)\s*,", orig_bib))

for e in v_all:
    key = e["key"]
    if key in existing_keys or key in seen_keys:
        continue
    seen_keys.add(key)
    
    venue = e.get("venue", "")
    is_proc = "Proceedings" in venue or "Conference" in venue or "Symposium" in venue or "ICASSP" in venue or "ICDMW" in venue
    is_arxiv = "arxiv" in venue.lower() or "arxiv" in e.get("doi", "").lower()
    
    entry_type = "article"
    if is_arxiv:
        entry_type = "article"
    elif is_proc:
        entry_type = "inproceedings"
    
    lines = [f"@{entry_type}{{{key},"]
    lines.append(f"  author    = {{{e['authors']}}},")
    lines.append(f"  title     = {{{e['title']}}},")
    
    if entry_type == "inproceedings":
        lines.append(f"  booktitle = {{{venue}}},")
    else:
        lines.append(f"  journal   = {{{venue}}},")
        
    if e.get("volume"):
        lines.append(f"  volume    = {{{e['volume']}}},")
    if e.get("number"):
        lines.append(f"  number    = {{{e['number']}}},")
    if e.get("pages"):
        lines.append(f"  pages     = {{{e['pages']}}},")
        
    lines.append(f"  year      = {{{e['year']}}},")
    
    if e.get("doi"):
        lines.append(f"  doi       = {{{e['doi']}}}")
    else:
        lines[-1] = lines[-1].rstrip(",")
        
    lines.append("}\n")
    new_bib_entries.append("\n".join(lines))

full_new_bib = orig_bib.rstrip() + "\n\n" + "\n".join(new_bib_entries)

with open(ROOT / "paper" / "references.bib", "w", encoding="utf-8") as f:
    f.write(full_new_bib)

with open(ROOT / "springer_manuscript" / "references.bib", "w", encoding="utf-8") as f:
    f.write(full_new_bib)

print(f"Added {len(new_bib_entries)} new entries to references.bib.")
