from pathlib import Path

p = Path("scripts/make_stability_outputs.py")
text = p.read_text(encoding="utf-8")
lines = text.splitlines()

print("--- Lines 240-265 ---")
for i in range(240, 266):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}")

print("\n--- Lines 420-448 ---")
for i in range(420, 448):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}")
