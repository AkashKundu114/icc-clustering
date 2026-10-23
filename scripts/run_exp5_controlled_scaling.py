"""
Exp 5 Controlled Scaling Benchmark for Pass E.
Evaluates both configurations:
  Config A (Default Exp 4): M=25, L=40, K=5, D=100
  Config B (Optimized Exp 5): M=15, L=60, K=5, D=100
Across N in {1e4, 1e5, 1e6} on synthetic Gaussian benchmark data (seeds 0, 1, 2).
Measures runtime and peak memory, fits scaling exponent with 95% CI.
"""

import time
import json
import tracemalloc
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import linregress

import sys
_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from icc.consensus_v2 import InvariantCoreConsensusV2
from experiments.exp5_extreme_scale.src.extreme_scale_benchmark import generate_synthetic_data

OUT_DIR = Path("results/passE")
OUT_DIR.mkdir(parents=True, exist_ok=True)

N_VALS = [10000, 100000, 1000000]
SEEDS = [0, 1, 2]

def run_scaling():
    records = []
    print("=" * 70)
    print("RUNNING EXP 5 CONTROLLED SCALING ACROSS N in {10k, 100k, 1M}")
    print("=" * 70)

    configs = [
        {"name": "Default_Exp4", "M": 25, "L": 40},
        {"name": "Optimized_Exp5", "M": 15, "L": 60}
    ]

    for N in N_VALS:
        for seed in SEEDS:
            print(f"\nGenerating data for N={N:,}, seed={seed}...")
            X, y = generate_synthetic_data(N=N, D=100, K=5, seed=seed)

            for cfg in configs:
                cname = cfg["name"]
                M = cfg["M"]
                L = cfg["L"]
                print(f"  Running {cname} (M={M}, L={L}) on N={N:,} seed={seed}...", flush=True)

                tracemalloc.start()
                t0 = time.perf_counter()
                model = InvariantCoreConsensusV2(
                    n_clusters=5, n_base_models=M, n_anchors=L, random_state=seed
                )
                pred = model.fit_predict(X)
                elap = time.perf_counter() - t0
                _, peak_mem = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                from sklearn.metrics import adjusted_rand_score
                ari = adjusted_rand_score(y, pred)
                mem_mb = peak_mem / (1024 * 1024)
                print(f"    -> Time: {elap:.2f}s | Peak RAM: {mem_mb:.1f} MB | ARI: {ari:.4f}")

                records.append({
                    "config": cname, "N": N, "D": 100, "K": 5, "M": M, "L": L,
                    "seed": seed, "time_s": elap, "peak_ram_mb": mem_mb, "ari": ari
                })

    df = pd.DataFrame(records)
    out_csv = OUT_DIR / "exp5_controlled_scaling.csv"
    df.to_csv(out_csv, index=False)
    print(f"\nSaved scaling results to {out_csv}")

    # Compute scaling exponents
    stats = {}
    for cname in ["Default_Exp4", "Optimized_Exp5"]:
        sub = df[df["config"] == cname]
        log_n = np.log10(sub["N"].values)
        log_t = np.log10(sub["time_s"].values)
        res = linregress(log_n, log_t)
        beta = res.slope
        se = res.stderr
        stats[cname] = {
            "beta": float(beta),
            "stderr": float(se),
            "ci_95": [float(beta - 1.96 * se), float(beta + 1.96 * se)],
            "r2": float(res.rvalue ** 2),
            "mean_time_1M": float(sub[sub["N"] == 1000000]["time_s"].mean()),
            "std_time_1M": float(sub[sub["N"] == 1000000]["time_s"].std()),
            "mean_ram_1M": float(sub[sub["N"] == 1000000]["peak_ram_mb"].mean()),
        }
        print(f"\n[{cname}] Scaling exponent beta = {beta:.4f} +/- {1.96*se:.4f} (95% CI: [{beta-1.96*se:.4f}, {beta+1.96*se:.4f}])")
        print(f"  Mean Time at N=1M: {stats[cname]['mean_time_1M']:.2f} +/- {stats[cname]['std_time_1M']:.2f} s")
        print(f"  Mean RAM at N=1M: {stats[cname]['mean_ram_1M']:.1f} MB")

    with open(OUT_DIR / "exp5_scaling_stats.json", "w", encoding="utf-8") as fp:
        json.dump(stats, fp, indent=2)
    print(f"Saved stats to {OUT_DIR / 'exp5_scaling_stats.json'}")

if __name__ == "__main__":
    run_scaling()
