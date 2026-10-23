"""
Regenerates Figure 6 (13-dataset Benchmark Matrix Heatmap) and Figure 7 (Demšar Critical Difference Diagram)
directly from results/passE/benchmark_matrix_seeds0_9.csv.
Synchronizes generated figures across all manuscript directories.
"""

import sys
import shutil
from pathlib import Path
import pandas as pd

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from experiments.exp3_real_world_benchmarks.src.run_exp3_1_benchmark_matrix import plot_fig14_13datasets
from experiments.exp3_real_world_benchmarks.src.run_exp3_4_statistical_significance import run_sub_exp3_4

CSV_PATH = Path("results/passE/benchmark_matrix_seeds0_9.csv")


def main():
    if not CSV_PATH.exists():
        print(f"Error: {CSV_PATH} not found.")
        return

    df = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df)} records from {CSV_PATH}.")

    # 1. Regenerate Figure 6 (Benchmark Matrix 13 Datasets)
    df_fig14 = df.copy()
    # Map model names to match MODEL_ORDER in benchmark_models
    df_fig14["model"] = df_fig14["model"].replace({"Core_Halo_Consensus": "Li_et_al_2019"})

    fig14_out = Path("experiments/exp3_real_world_benchmarks/figures/fig14_benchmark_matrix_13datasets.png")
    fig14_out.parent.mkdir(parents=True, exist_ok=True)
    plot_fig14_13datasets(df_fig14, metric="ari", save_path=str(fig14_out))
    print(f"[OK] Generated {fig14_out}")

    # Copy fig14 to target dirs
    targets_fig14 = [
        Path("springer_manuscript/figures/fig14_benchmark_matrix_13datasets.png"),
        Path("paper/figures/fig14_benchmark_matrix_13datasets.png"),
        Path("manuscript/figures/fig14_benchmark_matrix_13datasets.png"),
    ]
    for t in targets_fig14:
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(fig14_out, t)
        print(f"  Copied to {t}")

    # 2. Regenerate Figure 7 (Demšar Critical Difference Diagram)
    # Temporarily save a sanitized version of the CSV for run_sub_exp3_4
    temp_csv = Path("results/passE/temp_benchmark_matrix_for_cd.csv")
    df_cd = df.copy()
    df_cd["model"] = df_cd["model"].replace({
        "Standard_Consensus": "Std Cons",
        "Core_Halo_Consensus": "Core-Halo Cons.",
        "ICC_v2": "ICC-v2 (Ours)"
    })
    df_cd.to_csv(temp_csv, index=False)

    fig17_out = Path("experiments/exp3_real_world_benchmarks/figures/fig17_critical_difference_diagram_v2.png")
    fig17_out.parent.mkdir(parents=True, exist_ok=True)

    run_sub_exp3_4(input_csv=str(temp_csv), output_csv=str(Path("results/passE/exp3_4_statistical_significance_passE.csv")))
    print(f"[OK] Generated {fig17_out}")

    if temp_csv.exists():
        temp_csv.unlink()

    # Copy fig17 to target dirs
    targets_fig17 = [
        Path("springer_manuscript/figures/fig17_critical_difference_diagram_v2.png"),
        Path("paper/figures/fig17_critical_difference_diagram_v2.png"),
        Path("manuscript/figures/fig17_critical_difference_diagram_v2.png"),
    ]
    for t in targets_fig17:
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(fig17_out, t)
        print(f"  Copied to {t}")

    print("\n[ALL DONE] Figures 6 and 7 regenerated and synchronized successfully.")


if __name__ == "__main__":
    main()
