"""
Verification script for Figure 8 (Exp 4.3 Quad Panel) vs Manuscript Caption.
Reads the empirical data file experiments/exp4_scalability_and_sensitivity/data/exp4_sample_scaling_results.csv
and verifies every quantitative claim in the Figure 8 caption of springer_manuscript/main.tex:
  1. Dense consensus runtime at N=10,000: 29.96 s
  2. ICC-v2 runtime at N=10,000: 10.35 s
  3. Empirical speedup factor: 2.9x
  4. Auxiliary graph working memory: 762.8 MB (dense) vs 3.06 MB (reduced) -> 99.6% reduction
  5. Peak dynamic RAM: 2670.6 MB (dense) vs 68.8 MB (reduced) -> 97.4% reduction
"""

import sys
from pathlib import Path
import pandas as pd

def verify_fig8():
    data_path = Path("experiments/exp4_scalability_and_sensitivity/data/exp4_sample_scaling_results.csv")
    if not data_path.exists():
        print(f"FAILED: Data file {data_path} not found.")
        sys.exit(1)

    df = pd.read_csv(data_path)
    df_10k = df[df["N"] == 10000]

    exact_time = df_10k[df_10k["model"] == "Standard_Consensus"]["runtime_sec"].mean()
    exact_time_std = df_10k[df_10k["model"] == "Standard_Consensus"]["runtime_sec"].std()

    red_time = df_10k[df_10k["model"] == "ICC_v2"]["runtime_sec"].mean()
    red_time_std = df_10k[df_10k["model"] == "ICC_v2"]["runtime_sec"].std()

    speedup = exact_time / red_time

    exact_graph = df_10k[df_10k["model"] == "Standard_Consensus"]["graph_mem_mb"].iloc[0]
    red_graph = df_10k[df_10k["model"] == "ICC_v2"]["graph_mem_mb"].iloc[0]
    graph_reduc = (exact_graph - red_graph) / exact_graph * 100.0

    exact_peak = df_10k[df_10k["model"] == "Standard_Consensus"]["peak_memory_mb"].mean()
    red_peak = df_10k[df_10k["model"] == "ICC_v2"]["peak_memory_mb"].mean()
    peak_reduc = (exact_peak - red_peak) / exact_peak * 100.0

    print("--- Figure 8 Empirical Verification ---")
    print(f"Dense Runtime at N=10,000: {exact_time:.2f} s +/- {exact_time_std:.2f} s (Caption: 29.96 s)")
    assert abs(exact_time - 29.96) < 0.05, f"Dense runtime mismatch: {exact_time} vs 29.96"

    print(f"ICC-v2 Runtime at N=10,000: {red_time:.2f} s +/- {red_time_std:.2f} s (Caption: 10.35 s)")
    assert abs(red_time - 10.35) < 0.05, f"ICC-v2 runtime mismatch: {red_time} vs 10.35"

    print(f"Speedup Factor: {speedup:.1f}x ({speedup:.3f}x) (Caption: 2.9x)")
    assert abs(speedup - 2.90) < 0.05, f"Speedup mismatch: {speedup} vs 2.90"

    print(f"Dense Graph Memory: {exact_graph:.1f} MB (Caption: 762.8 MB)")
    assert abs(exact_graph - 762.8) < 0.2, f"Dense graph memory mismatch: {exact_graph} vs 762.8"

    print(f"ICC-v2 Graph Memory: {red_graph:.2f} MB (Caption: 3.06 MB)")
    assert abs(red_graph - 3.06) < 0.05, f"ICC-v2 graph memory mismatch: {red_graph} vs 3.06"

    print(f"Graph Reduction: {graph_reduc:.1f}% (Caption: 99.6%)")
    assert abs(graph_reduc - 99.6) < 0.1, f"Graph reduction mismatch: {graph_reduc} vs 99.6"

    print(f"Dense Peak Dynamic RAM: {exact_peak:.1f} MB (Caption: 2,670.6 MB)")
    assert abs(exact_peak - 2670.6) < 0.5, f"Dense peak RAM mismatch: {exact_peak} vs 2670.6"

    print(f"ICC-v2 Peak Dynamic RAM: {red_peak:.1f} MB (Caption: 68.8 MB)")
    assert abs(red_peak - 68.8) < 0.5, f"ICC-v2 peak RAM mismatch: {red_peak} vs 68.8"

    print(f"Dynamic RAM Reduction: {peak_reduc:.1f}% (Caption: 97.4%)")
    assert abs(peak_reduc - 97.4) < 0.1, f"Peak reduction mismatch: {peak_reduc} vs 97.4"

    print("\n[SUCCESS] All Figure 8 caption quantitative claims VERIFIED against empirical data store.")

if __name__ == "__main__":
    verify_fig8()
