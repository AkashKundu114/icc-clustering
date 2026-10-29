"""
Fix remaining 'certified' occurrences across all manuscript files:
1. paper/main.tex line 616
2. springer_manuscript/main.tex line 70 and line 616
"""

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Line 70
    c1_old = "certified invariant anchors (stars)"
    c1_new = "high-determinacy landmark anchors (stars)"
    if c1_old in content:
        content = content.replace(c1_old, c1_new)
        print(f"[{filepath}] Replaced '{c1_old}' -> '{c1_new}'")

    # Line 616
    c2_old = "certified core anchors (V5: $0.225 \\pm 0.318$)"
    c2_new = "high-determinacy core anchors (V5: $0.225 \\pm 0.318$)"
    if c2_old in content:
        content = content.replace(c2_old, c2_new)
        print(f"[{filepath}] Replaced '{c2_old}' -> '{c2_new}'")

    c3_old = "(or certified core subsets)"
    c3_new = "(or high-determinacy core subsets)"
    if c3_old in content:
        content = content.replace(c3_old, c3_new)
        print(f"[{filepath}] Replaced '{c3_old}' -> '{c3_new}'")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    for path in ['paper/main.tex', 'springer_manuscript/main.tex']:
        clean_file(path)
