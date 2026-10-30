"""
scripts/run_clean_scaling_benchmark.py

Reruns sample scalability benchmark under clean idle single-process conditions:
- N in {500, 1000, 2000, 5000, 8000, 10000}
- Seeds in {42, 101, 202, 303, 404}
- Fixed dimensions: D=200, K=3, M=25, L=40
- Discarded warm-up run per N reported separately to results/scaling_warmup.csv
- Pre- and post-run system telemetry (CPU freq, CPU load/percent, swap memory) logged to results/scaling_env.csv
- Main pass: Pure untraced timing (time.perf_counter) measuring end-to-end execution
- Separate pass: Traced memory (tracemalloc) measuring peak process RAM
- Outputs:
    - results/scaling_warmup.csv
    - results/scaling_env.csv
    - results/scaling_runs.csv
    - results/scalability_untraced_raw.csv
    - experiments/exp4_scalability_and_sensitivity/data/exp4_sample_scaling_results.csv
"""

import gc
import os
import sys
import time
import tracemalloc
from pathlib import Path
import numpy as np
import pandas as pd
import psutil

# Ensure repository root is on sys.path
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
D_FIXED = 200
K_FIXED = 3


def get_telemetry():
    freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0.0
    cpu_pct = psutil.cpu_percent(interval=None)
    swap = psutil.swap_memory()
    loadavg = os.getloadavg() if hasattr(os, "getloadavg") else None
    return {
        "timestamp": time.time(),
        "cpu_freq_mhz": freq,
        "cpu_percent": cpu_pct,
        "swap_used_mb": swap.used / (1024.0 * 1024.0),
        "swap_percent": swap.percent,
        "load_avg": str(loadavg) if loadavg is not None else "N/A",
    }


def main():
    print("=" * 80)
    print("ITEM 1C: CLEAN CONTROLLED SCALING BENCHMARK")
    print(f"Sample Sizes N: {N_VALS}")
    print(f"Fixed Dimension D={D_FIXED}, Clusters K={K_FIXED}, Seeds={SEEDS}")
    print("=" * 80)

    env_records = []
    warmup_records = []
    timing_records = []
    run_counter = 0

    results_dir = ROOT / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------
    # PASS 1: Untraced Timing Benchmark
    # -------------------------------------------------------------
    print("\n>>> PASS 1: Pure Untraced Timing (time.perf_counter)")

    for n in N_VALS:
        print(f"\n--- Benchmark N = {n} ---")
        
        # 1. Warm-up Run (discarded, recorded separately)
        X_warm, y_warm = generate_benchmark_synthetic(n, D_FIXED, k=K_FIXED, seed=9999)
        for mname, mfn in MODELS.items():
            gc.collect()
            time.sleep(0.05)
            pre = get_telemetry()
            t0 = time.perf_counter()
            pred, _, _ = mfn(X_warm, K_FIXED, seed=9999)
            elapsed_warm = time.perf_counter() - t0
            post = get_telemetry()
            warmup_records.append({
                "N": n,
                "model": mname,
                "warmup_time_sec": elapsed_warm,
                "pre_cpu_freq_mhz": pre["cpu_freq_mhz"],
                "post_cpu_freq_mhz": post["cpu_freq_mhz"],
                "pre_cpu_pct": pre["cpu_percent"],
                "post_cpu_pct": post["cpu_percent"],
                "pre_swap_mb": pre["swap_used_mb"],
                "post_swap_mb": post["swap_used_mb"],
            })
            print(f"  [Warmup] N={n:5d} | {mname:<18} | Time={elapsed_warm:6.3f}s")

        # 2. Measured Runs across 5 canonical seeds
        for seed in SEEDS:
            X, y = generate_benchmark_synthetic(n, D_FIXED, k=K_FIXED, seed=seed)
            for mname, mfn in MODELS.items():
                run_counter += 1
                gc.collect()
                time.sleep(0.05)

                pre = get_telemetry()
                env_records.append({
                    "run_id": run_counter,
                    "phase": "pre",
                    "timing_mode": "untraced",
                    "N": n,
                    "model": mname,
                    "seed": seed,
                    **pre
                })

                t0 = time.perf_counter()
                pred, _, _ = mfn(X, K_FIXED, seed=seed)
                elapsed = time.perf_counter() - t0

                post = get_telemetry()
                env_records.append({
                    "run_id": run_counter,
                    "phase": "post",
                    "timing_mode": "untraced",
                    "N": n,
                    "model": mname,
                    "seed": seed,
                    **post
                })

                timing_records.append({
                    "run_id": run_counter,
                    "N": n,
                    "D": D_FIXED,
                    "K": K_FIXED,
                    "model": mname,
                    "seed": seed,
                    "runtime_sec": elapsed,
                    "cpu_freq_mhz": (pre["cpu_freq_mhz"] + post["cpu_freq_mhz"]) / 2.0,
                    "cpu_percent": (pre["cpu_percent"] + post["cpu_percent"]) / 2.0,
                    "swap_used_mb": post["swap_used_mb"],
                })
                print(f"  [Measured] N={n:5d} | Seed={seed:3d} | {mname:<18} | Time={elapsed:6.3f}s")

    timing_df = pd.DataFrame(timing_records)
    warmup_df = pd.DataFrame(warmup_records)
    env_df = pd.DataFrame(env_records)

    warmup_df.to_csv(results_dir / "scaling_warmup.csv", index=False)
    env_df.to_csv(results_dir / "scaling_env.csv", index=False)
    print(f"\n[+] Saved warm-up records to {results_dir / 'scaling_warmup.csv'}")
    print(f"[+] Saved telemetry records to {results_dir / 'scaling_env.csv'}")

    # -------------------------------------------------------------
    # PASS 2: Traced Peak Memory Benchmark (tracemalloc)
    # -------------------------------------------------------------
    print("\n>>> PASS 2: Traced Peak Memory (tracemalloc)")
    mem_records = []
    for n in N_VALS:
        print(f"\n--- Memory Tracing N = {n} ---")
        for seed in SEEDS:
            X, y = generate_benchmark_synthetic(n, D_FIXED, k=K_FIXED, seed=seed)
            for mname, mfn in MODELS.items():
                run_counter += 1
                gc.collect()
                time.sleep(0.05)

                pre = get_telemetry()
                env_records.append({
                    "run_id": run_counter,
                    "phase": "pre",
                    "timing_mode": "traced_memory",
                    "N": n,
                    "model": mname,
                    "seed": seed,
                    **pre
                })

                tracemalloc.start()
                pred, _, _ = mfn(X, K_FIXED, seed=seed)
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                post = get_telemetry()
                env_records.append({
                    "run_id": run_counter,
                    "phase": "post",
                    "timing_mode": "traced_memory",
                    "N": n,
                    "model": mname,
                    "seed": seed,
                    **post
                })

                peak_mb = peak / (1024.0 * 1024.0)
                mem_records.append({
                    "N": n,
                    "model": mname,
                    "seed": seed,
                    "peak_memory_mb": peak_mb,
                })
                print(f"  [RAM] N={n:5d} | Seed={seed:3d} | {mname:<18} | Peak RAM={peak_mb:6.2f} MB")

    mem_df = pd.DataFrame(mem_records)
    env_df = pd.DataFrame(env_records)
    env_df.to_csv(results_dir / "scaling_env.csv", index=False)

    # Merge timing and memory records
    merged_raw = pd.merge(timing_df, mem_df, on=["N", "model", "seed"])
    merged_raw.to_csv(results_dir / "scaling_runs.csv", index=False)
    merged_raw.to_csv(results_dir / "scalability_untraced_raw.csv", index=False)
    print(f"\n[+] Saved merged raw runs to {results_dir / 'scaling_runs.csv'}")
    print(f"[+] Saved raw untraced backup to {results_dir / 'scalability_untraced_raw.csv'}")

    # Summary table
    summary = merged_raw.groupby(["N", "model"]).agg(
        runtime_sec=("runtime_sec", "mean"),
        time_std=("runtime_sec", "std"),
        peak_memory_mb=("peak_memory_mb", "mean"),
        mem_std=("peak_memory_mb", "std"),
    ).reset_index()

    # Save to experiments data
    exp_csv = ROOT / "experiments" / "exp4_scalability_and_sensitivity" / "data" / "exp4_sample_scaling_results.csv"
    summary.to_csv(exp_csv, index=False)
    print(f"[+] Saved aggregated summary to {exp_csv}")

    print("\n" + "=" * 80)
    print("AGGREGATED RESULTS SUMMARY:")
    print("=" * 80)
    for model_name in ["Standard_Consensus", "ICC_v2"]:
        sub = summary[summary["model"] == model_name]
        print(f"\nModel: {model_name}")
        for _, row in sub.iterrows():
            print(f"  N={int(row['N']):5d}: Runtime = {row['runtime_sec']:.3f} +/- {row['time_std']:.3f} s | RAM = {row['peak_memory_mb']:.2f} +/- {row['mem_std']:.2f} MB")


if __name__ == "__main__":
    main()
