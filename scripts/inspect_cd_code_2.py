from pathlib import Path

p = Path("experiments/exp3_real_world_benchmarks/src/run_exp3_4_statistical_significance.py")
text = p.read_text(encoding="utf-8")
lines = text.splitlines()

for i in range(235, 305):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}")
