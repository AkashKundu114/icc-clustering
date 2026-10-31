from pathlib import Path

p = Path("scripts/make_stats.py")
text = p.read_text(encoding="utf-8")
lines = text.splitlines()

for i, l in enumerate(lines):
    if "nemenyi" in l.lower() or "friedman" in l.lower() or "cd" in l.lower():
        print(f"{i+1}: {l}")
