"""
scripts/ref_stats.py

Computes publication vintage statistics for paper/references.bib.
Calculates the exact share of 2024-2026 citations against older foundations.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIB_PATH = ROOT / "paper" / "references.bib"

def analyze_bibliography(bib_path=BIB_PATH):
    if not bib_path.exists():
        bib_path = ROOT / "springer_manuscript" / "references.bib"
    
    with open(bib_path, "r", encoding="utf-8") as f:
        text = f.read()

    entries = re.findall(r"@(\w+)\s*\{\s*([^,]+)\s*,\s*(.*?)\n\}", text, re.DOTALL)
    
    total = len(entries)
    years = {}
    recent_count = 0
    recent_entries = []
    older_entries = []

    for entry_type, key, body in entries:
        m = re.search(r'year\s*=\s*[\{"]?(\d{4})[\}"]?', body)
        yr = int(m.group(1)) if m else 0
        years[yr] = years.get(yr, 0) + 1
        if yr in [2024, 2025, 2026]:
            recent_count += 1
            recent_entries.append((key, yr))
        else:
            older_entries.append((key, yr))

    recent_pct = (recent_count / total * 100.0) if total > 0 else 0.0

    print(f"=== Bibliography Vintage Statistics ===")
    print(f"Total References: {total}")
    print(f"2024-2026 References: {recent_count} ({recent_pct:.1f}%)")
    print(f"Earlier Classics (<2024): {len(older_entries)} ({100.0 - recent_pct:.1f}%)")
    print(f"\nYear Breakdown:")
    for yr in sorted(years.keys()):
        print(f"  {yr}: {years[yr]}")
    
    return {
        "total": total,
        "recent_count": recent_count,
        "recent_pct": recent_pct,
        "years": years,
        "recent_entries": recent_entries,
        "older_entries": older_entries
    }

if __name__ == "__main__":
    analyze_bibliography()
