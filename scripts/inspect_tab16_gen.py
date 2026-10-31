from pathlib import Path

p = Path("scripts/make_stability_outputs.py")
text = p.read_text(encoding="utf-8")
lines = text.splitlines()

for i in range(150, 230):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}")
