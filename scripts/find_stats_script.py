from pathlib import Path

for p in Path("scripts").glob("*.py"):
    t = p.read_text(encoding="utf-8")
    if "N13" in t or "table06" in t or "5.62" in t or "5.15" in t:
        print(f"Match in {p}")
