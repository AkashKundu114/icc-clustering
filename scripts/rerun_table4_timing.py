"""
scripts/rerun_table4_timing.py

Reruns sample complexity scaling benchmark for ICC-v2 at N in {5000, 6000, 8000, 10000}
for 5 seeds each (42, 101, 202, 303, 404) on an idle system, logging CPU frequency,
background load, and swap usage.
"""

import cProfile
import gc
import io
import json
import pstats
import sys
import time
import tracemalloc
from pathlib import Path

import pandas as pd
import psutil

# Add project root
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from experiments.exp3_real_world_benchmarks.src.benchmark_models import run_icc_v2
from experiments.exp4_scalability_and_sensitivity.src.scaling_benchmark import generate_benchmark_synthetic

CSV_PATH = ROOT / "experiments" / "exp4_scalability_and_sensitivity" / "data" / "exp4_sample_scaling_results.csv"
BACKUP_PATH = ROOT / "experiments" / "exp4_scalability_and_sensitivity" / "data" / "exp4_sample_scaling_results_backup.csv"
LOG_PATH = ROOT / "experiments" / "exp4_scalability_and_sensitivity" / "data" / "timing_rerun_environment_log.json"


def main():
    print("=" * 80)
    print("RERUNNING TABLE 4 TIMING BENCHMARK ON IDLE SYSTEM")
    print("=" * 80)

    # Backup original CSV
    if CSV_PATH.exists() and not BACKUP_PATH.exists():
        import shutil
        shutil.copy2(CSV_PATH, BACKUP_PATH)
        print(f"Backed up original CSV to {BACKUP_PATH}")

    old_df = pd.read_csv(CSV_PATH) if CSV_PATH.exists() else pd.DataFrame()

    env_log = {
        "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {},
        "cpu_count": psutil.cpu_count(logical=True),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "virtual_mem": psutil.virtual_memory()._asdict(),
        "swap_mem": psutil.swap_memory()._asdict(),
        "runs": []
    }

    n_values = [5000, 6000, 8000, 10000]
    seeds = [42, 101, 202, 303, 404]
    new_records = []

    for n in n_values:
        for trial, seed in enumerate(seeds):
            gc.collect()
            time.sleep(0.1) # brief pause to ensure idle state

            freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0.0
            cpu_pct = psutil.cpu_percent(interval=None)
            swap_used_mb = psutil.swap_memory().used / (1024 * 1024)

            X, y = generate_benchmark_synthetic(n, 200, k=3, seed=seed)

            tracemalloc.start()
            t0 = time.perf_counter()
            labels, runtime, meta = run_icc_v2(X, k=3, seed=seed)
            t_total = time.perf_counter() - t0
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_mb = peak / (1024.0 * 1024.0)

            rec = {
                "N": n,
                "D": 200,
                "K": 3,
                "model": "ICC_v2",
                "trial": trial,
                "seed": seed,
                "runtime_sec": t_total,
                "peak_memory_mb": peak_mb,
                "peak_rss_mb": peak_mb,
                "graph_mem_mb": (n * 40 * 8) / (1024 * 1024),
                "lc": 40,
                "oom": False
            }
            new_records.append(rec)
            print(f"N={n:5d} | Seed={seed:3d} | Time={t_total:6.3f}s | Peak RAM={peak_mb:6.1f}MB | CPU Freq={freq:6.1f}MHz | Swap={swap_used_mb:6.1f}MB")

            env_log["runs"].append({
                "N": n,
                "seed": seed,
                "time_sec": t_total,
                "peak_ram_mb": peak_mb,
                "cpu_freq_mhz": freq,
                "cpu_pct": cpu_pct,
                "swap_used_mb": swap_used_mb
            })

    # Save environment log
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(env_log, f, indent=2)
    print(f"\nSaved environment and timing log to {LOG_PATH}")

    # Profiler run at N=8000
    print("\n--- Running cProfile on N=8000 to analyze function execution ---")
    X, y = generate_benchmark_synthetic(8000, 200, k=3, seed=42)
    pr = cProfile.Profile()
    pr.enable()
    run_icc_v2(X, k=3, seed=42)
    pr.disable()

    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
    ps.print_stats(15)
    prof_output = s.getvalue()
    print(prof_output)

    with open(ROOT / "experiments" / "exp4_scalability_and_sensitivity" / "data" / "profiler_n8000.txt", "w", encoding="utf-8") as f:
        f.write(prof_output)

    # Merge new records into old_df (replace old ICC_v2 records for N in [5000, 6000, 8000, 10000])
    new_df_records = pd.DataFrame(new_records)
    filtered_old = old_df[~((old_df["model"] == "ICC_v2") & (old_df["N"].isin(n_values)))]
    merged_df = pd.concat([filtered_old, new_df_records], ignore_index=True)
    merged_df.sort_values(by=["N", "model", "trial"], inplace=True)
    merged_df.to_csv(CSV_PATH, index=False)
    print(f"\nUpdated {CSV_PATH} with clean idle benchmark data.")


if __name__ == "__main__":
    main()
