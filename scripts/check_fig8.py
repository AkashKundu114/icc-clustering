import json
from pathlib import Path

# 1. stats.json
stats_path = Path("results/stats.json")
if stats_path.exists():
    data = json.loads(stats_path.read_text(encoding="utf-8"))
    print("stats.json N13 ranks:")
    for k, v in data.get("N13", {}).get("ranks", {}).items():
        print(f"  {k:20s}: {v:.2f}")

# 2. table06_omnibus_benchmark_ari.tex
t06_path = Path("paper/gen/table06_omnibus_benchmark_ari.tex")
if t06_path.exists():
    print("\ntable06_omnibus_benchmark_ari.tex bottom rows:")
    for line in t06_path.read_text(encoding="utf-8").splitlines()[-15:]:
        print(" ", line)

# 3. Fig. 8 in main.tex
with open("springer_manuscript/main.tex", "r", encoding="utf-8") as f:
    text = f.read()

import re
m = re.search(r"\\begin\{figure\*?\}.*?fig08.*?\\end\{figure\*?\}", text, re.DOTALL)
if m:
    print("\nFig. 8 block in main.tex:")
    print(m.group(0))
else:
    # search by critical difference
    m2 = re.search(r"\\begin\{figure\*?\}.*?[Cc]ritical [Dd]ifference.*?\\end\{figure\*?\}", text, re.DOTALL)
    if m2:
        print("\nFig. 8 (by CD) block in main.tex:")
        print(m2.group(0))
