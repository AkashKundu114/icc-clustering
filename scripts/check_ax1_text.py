from pathlib import Path

p = Path("scripts/make_stability_outputs.py")
text = p.read_text(encoding="utf-8")
lines = text.splitlines()

for i, l in enumerate(lines):
    if "ax1.text" in l or "ax1.annotate" in l:
        print(f"{i+1}: {l}")
        for j in range(1, 10):
            if i+j < len(lines):
                print(f"  {lines[i+j]}")
                if ")" in lines[i+j]:
                    break
