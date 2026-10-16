"""
Runner script for Experiment 3: Real-World High-Dimensional Benchmarks.
Executes 8 clustering algorithms across 4 diverse datasets over 10 independent trials.
"""

import os
import sys
from pathlib import Path
import time
import numpy as np
import pandas as pd

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from experiments.exp3_real_world_benchmarks.src.dataset_loader import load_benchmark_dataset, DATASET_CONFIGS
from experiments.exp3_real_world_benchmarks.src.benchmark_models import MODELS
from icc.core import adjusted_rand_score, normalized_mutual_info_score

OUTPUT_CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "exp3_benchmark_results.csv")
SEEDS = [42, 101, 202, 303, 404, 505, 606, 707, 808, 909]


def run_all_benchmarks(n_trials=10):
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    records = []
    
    print("=" * 80)
    print("STARTING EXPERIMENT 3: REAL-WORLD HIGH-DIMENSIONAL BENCHMARKS")
    print(f"Datasets: {list(DATASET_CONFIGS.keys())}")
    print(f"Models ({len(MODELS)}): {list(MODELS.keys())}")
    print(f"Trials per model: {n_trials}")
    print("=" * 80)
    
    start_total = time.perf_counter()
    
    for dname in DATASET_CONFIGS:
        print(f"\n---> Loading Dataset: {dname.upper()}")
        X, y, meta = load_benchmark_dataset(dname)
        N, D, K = meta["N"], meta["D"], meta["K"]
        print(f"     N={N}, D={D}, K={K}, D/N={D/N:.2f}")
        
        for mname, model_fn in MODELS.items():
            t_start_model = time.perf_counter()
            ari_list = []
            nmi_list = []
            time_list = []
            
            for trial_idx in range(n_trials):
                seed = SEEDS[trial_idx % len(SEEDS)]
                pred, elapsed_sec, lc = model_fn(X, K, seed=seed)
                
                ari = adjusted_rand_score(y, pred)
                nmi = normalized_mutual_info_score(y, pred)
                
                ari_list.append(ari)
                nmi_list.append(nmi)
                time_list.append(elapsed_sec)
                
                records.append({
                    "dataset": dname,
                    "N": N,
                    "D": D,
                    "K": K,
                    "model": mname,
                    "trial": trial_idx,
                    "seed": seed,
                    "ari": ari,
                    "nmi": nmi,
                    "elapsed_sec": elapsed_sec,
                    "lc": lc
                })
                
            model_duration = time.perf_counter() - t_start_model
            print(f"     {mname:<20}: Mean ARI={np.mean(ari_list):.4f} +/- {np.std(ari_list):.4f} | Mean NMI={np.mean(nmi_list):.4f} +/- {np.std(nmi_list):.4f} ({model_duration:.2f}s)")
            
    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_CSV, index=False)
    print("\n" + "=" * 80)
    print(f"[+] All benchmark trials completed in {time.perf_counter() - start_total:.2f}s")
    print(f"[+] Results saved to: {OUTPUT_CSV}")
    print("=" * 80)
    
    # Print formatted markdown summary table
    print("\n### Summary of Mean Performance across 10 Trials:")
    summary = df.groupby(["dataset", "model"]).agg({
        "ari": ["mean", "std"],
        "nmi": ["mean", "std"],
        "elapsed_sec": "mean"
    }).reset_index()
    print(summary.to_string())
    
    return df


if __name__ == "__main__":
    run_all_benchmarks(n_trials=10)
