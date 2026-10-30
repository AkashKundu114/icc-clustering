"""
scripts/update_title_everywhere.py

Updates historical manuscript titles across docs/, AGENTS.md, and submission files
to the unified canonical title:
"Cluster Stability and Feature-Gated Bipartite Ensemble Learning for High-Dimensional Noisy Data: An Empirical Analysis"
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CANONICAL_TITLE = "Cluster Stability and Feature-Gated Bipartite Ensemble Learning for High-Dimensional Noisy Data: An Empirical Analysis"

OLD_TITLES = [
    "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination",
    "When Do Feature Gating and Anchor Consensus Help High-Dimensional Clustering? An Empirical and Geometric Analysis",
    "Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes",
    "Stable but Wrong: Why Consensus Clustering Can Fail in High Dimensions, and What Helps",
]

TARGET_DIRS = ["docs", "paper", "submission"]
TARGET_FILES = ["AGENTS.md", "README.md", "CITATION.cff"]

def main():
    updated_count = 0
    
    # 1. Target individual root files
    for fname in TARGET_FILES:
        p = ROOT / fname
        if p.exists():
            text = p.read_text(encoding="utf-8")
            orig = text
            for old in OLD_TITLES:
                text = text.replace(old, CANONICAL_TITLE)
            if text != orig:
                p.write_text(text, encoding="utf-8")
                print(f"[+] Updated {p}")
                updated_count += 1

    # 2. Target directories
    for dname in TARGET_DIRS:
        dpath = ROOT / dname
        if not dpath.exists():
            continue
        for root, _, files in os.walk(dpath):
            if ".git" in root or "__pycache__" in root:
                continue
            for f in files:
                if f.endswith((".md", ".tex", ".txt", ".json")):
                    # Skip main.tex since it's already set and carefully verified
                    p = Path(root) / f
                    if p.name in ["main.tex", "sn-article.tex"]:
                        continue
                    try:
                        text = p.read_text(encoding="utf-8")
                        orig = text
                        for old in OLD_TITLES:
                            text = text.replace(old, CANONICAL_TITLE)
                        if text != orig:
                            p.write_text(text, encoding="utf-8")
                            print(f"[+] Updated {p}")
                            updated_count += 1
                    except Exception as e:
                        pass

    print(f"[+] Done. Updated {updated_count} files with canonical title.")

if __name__ == "__main__":
    main()
