"""
scripts/run_untraced_scalability.py

Executes Item 2 protocol:
1. Untraced timing: pure execution time using time.perf_counter() (no tracemalloc/cProfile)
   across N in {500, 1000, 2000, 5000, 8000, 10000} for 5 canonical seeds (42, 101, 202, 303, 404)
   for both GAC (ICC_v2) and Dense (Standard_Consensus), plus Li_et_al_2019 and ICC_v1.
2. Traced memory: separate run with tracemalloc to record peak process RAM.
3. System logs: records CPU frequency, CPU percent, virtual memory, and swap memory before each run.
4. Saves raw results to results/scalability_untraced_raw.csv and summary to
   experiments/exp4_scalability_and_sensitivity/data/exp4_sample_scaling_results.csv.
"""

import gc
import json
import os
import sys
import time
import tracemalloc
from pathlib import Path
import numpy as np
import pandas as pd
import psutil

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.exp4_scalability_and_sensitivity.src.scaling_benchmark import generate_benchmark_synthetic
from experiments.exp3_real_world_benchmarks.src.benchmark_models import (
    run_standard_consensus,
    run_li_et_al_2019,
    run_icc_v1,
    run_icc_v2,
)

MODELS = {
    "Standard_Consensus": run_standard_consensus,
    "Li_et_al_2019": run_li_et_al_2019,
    "ICC_v1": run_icc_v1,
    "ICC_v2": run_icc_v2,
}

N_VALS = [500, 1000, 2000, 5000, 8000, 10000]
SEEDS = [42, 101, 202, 303, 404]

def main():
    print("=" * 80)
    print("RUNNING ITEM 2: SCALABILITY & RESOURCE BENCHMARK")
    print("=" * 80)

    env_log = {
        "cpu_count": psutil.cpu_count(logical=True),
        "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {},
        "virtual_mem": psutil.virtual_memory()._asdict(),
        "swap_mem": psutil.swap_memory()._asdict(),
        "runs": [],
    }

    raw_records = []

    # PASS 1: Untraced Timing (pure time.perf_counter)
    print("\n--- PASS 1: Pure Untraced Execution Timing ---")
    for N in N_VALS:
        for seed in SEEDS:
            X, y = generate_benchmark_synthetic(N, 200, k=3, seed=seed)
            for mname, mfn in MODELS.items():
                gc.collect()
                time.sleep(0.05)

                freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0.0
                cpu_pct = psutil.cpu_percent(interval=None)
                swap_mb = psutil.swap_memory().used / (1024 * 1024)

                t0 = time.perf_counter()
                pred, _, _ = mfn(X, 3, seed=seed)
                untraced_time = time.perf_counter() - t0

                rec = {
                    "N": N,
                    "D": 200,
                    "K": 3,
                    "model": mname,
                    "seed": seed,
                    "untraced_time_sec": untraced_time,
                    "cpu_freq_mhz": freq,
                    "cpu_percent": cpu_pct,
                    "swap_used_mb": swap_mb,
                }
                raw_records.append(rec)
                env_log["runs"].append(rec)
                print(f"  [Untraced] N={N:5d} | Model={mname:<18} | Seed={seed:3d} | Time={untraced_time:6.3f}s")

    raw_df = pd.DataFrame(raw_records)

    # PASS 2: Traced Memory (separate pass)
    print("\n--- PASS 2: Traced Peak Memory (tracemalloc) ---")
    mem_records = []
    for N in N_VALS:
        for seed in SEEDS:
            X, y = generate_benchmark_synthetic(N, 200, k=3, seed=seed)
            for mname, mfn in MODELS.items():
                gc.collect()
                time.sleep(0.05)

                tracemalloc.start()
                pred, _, _ = mfn(X, 3, seed=seed)
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                peak_mb = peak / (1024.0 * 1024.0)
                mem_records.append({
                    "N": N,
                    "model": mname,
                    "seed": seed,
                    "peak_memory_mb": peak_mb,
                })
                print(f"  [Memory]   N={N:5d} | Model={mname:<18} | Seed={seed:3d} | Peak RAM={peak_mb:6.1f}MB")

    mem_df = pd.DataFrame(mem_records)

    # Merge untraced timing and traced memory
    merged = pd.merge(raw_df, mem_df, on=["N", "model", "seed"])

    # Save full raw runs
    raw_path = ROOT / "results" / "scalability_untraced_raw.csv"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(raw_path, index=False)
    print(f"\n[+] Saved full raw runs to {raw_path}")

    # Save environment log
    log_path = ROOT / "results" / "timing_rerun_environment_log.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(env_log, f, indent=2)
    print(f"[+] Saved environment log to {log_path}")

    # Aggregate by N and model
    summary = merged.groupby(["N", "model"]).agg(
        runtime_sec=("untraced_time_sec", "mean"),
        time_std=("untraced_time_sec", "std"),
        peak_memory_mb=("peak_memory_mb", "mean"),
        mem_std=("peak_memory_mb", "std"),
    ).reset_index()

    # Save to experiments data
    exp_csv = ROOT / "experiments" / "exp4_scalability_and_sensitivity" / "data" / "exp4_sample_scaling_results.csv"
    summary.to_csv(exp_csv, index=False)
    print(f"[+] Saved aggregated summary to {exp_csv}")
    print("\nSummary Table:")
    print(summary)

if __name__ == "__main__":
    main()
