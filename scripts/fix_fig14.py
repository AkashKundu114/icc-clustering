import os
import pandas as pd
from pathlib import Path

# 1. Update run_exp3_1_benchmark_matrix.py
p_script = Path("experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py")
with open(p_script, "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('"Li et al. (2019)"', '"Core-Halo Cons."')
text = text.replace('"ICC-v2 (VSSG+Anchor)"', '"ICC-v2 (BGSS+Anchor)"')

old_title = 'd_title = f"({chr(97 + i)}) {dname.upper()} (N={meta_n}, D={meta_d}, K={meta_k})"'
new_title = 'disp_name = "PBMC68K-REDUCED" if dname == "zheng68k" else dname.upper()\n            d_title = f"({chr(97 + i)}) {disp_name} (N={meta_n}, D={meta_d}, K={meta_k})"'
text = text.replace(old_title, new_title)

with open(p_script, "w", encoding="utf-8") as f:
    f.write(text)
print("Updated run_exp3_1_benchmark_matrix.py successfully.")

# 2. Re-run plot_fig14_13datasets
import sys
sys.path.insert(0, str(Path.cwd()))
from experiments.exp3_real_world_benchmarks.src.run_exp3_1_benchmark_matrix import plot_fig14_13datasets

csv_path = "experiments/exp3_real_world_benchmarks/data/exp3_1_benchmark_matrix_v2.csv"
df = pd.read_csv(csv_path)

out_fig = "experiments/exp3_real_world_benchmarks/figures/fig14_benchmark_matrix_13datasets.png"
plot_fig14_13datasets(df, metric="ari", save_path=out_fig)
print(f"Generated {out_fig}")

# 3. Copy to manuscript, paper, and springer_manuscript
import shutil
targets = [
    "springer_manuscript/figures/fig14_benchmark_matrix_13datasets.png",
    "paper/figures/fig14_benchmark_matrix_13datasets.png",
    "manuscript/figures/fig14_benchmark_matrix_13datasets.png",
]
for t in targets:
    shutil.copyfile(out_fig, t)
    print(f"Copied to {t}")
