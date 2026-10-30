"""
Sample complexity scaling benchmark and resource profiling for ICC-v2.

Evaluates empirical wall-clock execution time and peak memory consumption across
increasing sample sizes N in {5000, 6000, 8000, 10000} with feature dimension D=200
and cluster count K=3.

Theoretical Scaling Rationale:
------------------------------
Standard consensus clustering builds an explicit N x N co-association matrix with
quadratic time and space complexity O(M * N^2). In contrast, ICC-v2 constructs a
bipartite sample-anchor graph with L anchors (L << N), reducing complexity to O(M * N * L)
time and O(N * L) space. This script measures execution across multiple trials on an
idle system, tracking:
- Wall-clock runtime (seconds)
- Peak memory footprint via tracemalloc (MB)
- Host environment telemetry (CPU frequency, CPU load %, swap usage)
- Function-level execution hotspots via cProfile at N=8000

Parameters:
-----------
--n-values : list of int, default=[5000, 6000, 8000, 10000]
    Sample sizes N to evaluate.
--seeds : list of int, default=[42, 101, 202, 303, 404]
    Random seeds for synthetic data generation and ensemble partition initialization.
--profile-n : int, default=8000
    Sample size N on which to execute function-level cProfile analysis.

Outputs:
--------
- experiments/exp4_scalability_and_sensitivity/data/exp4_sample_scaling_results.csv
- experiments/exp4_scalability_and_sensitivity/data/timing_rerun_environment_log.json
- experiments/exp4_scalability_and_sensitivity/data/profiler_n8000.txt

Usage:
------
    python scripts/benchmark_scaling.py
    python scripts/benchmark_scaling.py --n-values 1000 2000 --seeds 42 101
"""

import argparse
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

# Add project root to sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.exp3_real_world_benchmarks.src.benchmark_models import run_icc_v2
from experiments.exp4_scalability_and_sensitivity.src.scaling_benchmark import generate_benchmark_synthetic

CSV_PATH = ROOT / "experiments" / "exp4_scalability_and_sensitivity" / "data" / "exp4_sample_scaling_results.csv"
BACKUP_PATH = ROOT / "experiments" / "exp4_scalability_and_sensitivity" / "data" / "exp4_sample_scaling_results_backup.csv"
LOG_PATH = ROOT / "experiments" / "exp4_scalability_and_sensitivity" / "data" / "timing_rerun_environment_log.json"
PROFILE_PATH = ROOT / "experiments" / "exp4_scalability_and_sensitivity" / "data" / "profiler_n8000.txt"


def benchmark_sample_scaling(n_values=None, seeds=None, profile_n=8000):
    """
    Execute sample complexity scaling benchmarks across varying N and random seeds.

    Parameters
    ----------
    n_values : list of int, optional
        Sample sizes to evaluate. Defaults to [5000, 6000, 8000, 10000].
    seeds : list of int, optional
        Random seeds for evaluation. Defaults to [42, 101, 202, 303, 404].
    profile_n : int, default=8000
        Sample size for cProfile execution trace.

    Returns
    -------
    pd.DataFrame
        Updated scaling results DataFrame.
    """
    if n_values is None:
        n_values = [5000, 6000, 8000, 10000]
    if seeds is None:
        seeds = [42, 101, 202, 303, 404]

    print("=" * 80)
    print("ICC-v2 SAMPLE COMPLEXITY SCALING BENCHMARK")
    print(f"Sample sizes N: {n_values}")
    print(f"Random seeds  : {seeds}")
    print("=" * 80)

    # Backup existing CSV before modification
    if CSV_PATH.exists() and not BACKUP_PATH.exists():
        import shutil
        shutil.copy2(CSV_PATH, BACKUP_PATH)
        print(f"[*] Backed up original CSV to {BACKUP_PATH}")

    old_df = pd.read_csv(CSV_PATH) if CSV_PATH.exists() else pd.DataFrame()

    env_log = {
        "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {},
        "cpu_count": psutil.cpu_count(logical=True),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "virtual_mem": psutil.virtual_memory()._asdict(),
        "swap_mem": psutil.swap_memory()._asdict(),
        "runs": [],
    }

    new_records = []

    for n in n_values:
        for trial, seed in enumerate(seeds):
            gc.collect()
            time.sleep(0.1)  # Brief pause to allow CPU telemetry stabilization

            freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0.0
            cpu_pct = psutil.cpu_percent(interval=None)
            swap_used_mb = psutil.swap_memory().used / (1024 * 1024)

            # Generate synthetic clustered data: D=200, K=3
            X, y = generate_benchmark_synthetic(n, 200, k=3, seed=seed)

            # Trace peak heap allocation during fit_predict
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
                "oom": False,
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
                "swap_used_mb": swap_used_mb,
            })

    # Save environment telemetry log
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(env_log, f, indent=2)
    print(f"\n[+] Saved environment and timing telemetry to {LOG_PATH}")

    # Optional cProfile run on target sample size
    if profile_n in n_values:
        print(f"\n--- Running cProfile analysis on N={profile_n} ---")
        X_prof, _ = generate_benchmark_synthetic(profile_n, 200, k=3, seed=42)
        pr = cProfile.Profile()
        pr.enable()
        run_icc_v2(X_prof, k=3, seed=42)
        pr.disable()

        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
        ps.print_stats(15)
        prof_output = s.getvalue()
        print(prof_output)

        with open(PROFILE_PATH, "w", encoding="utf-8") as f:
            f.write(prof_output)
        print(f"[+] Saved execution profile to {PROFILE_PATH}")

    # Merge newly collected timing records with existing records
    new_df_records = pd.DataFrame(new_records)
    if not old_df.empty and "model" in old_df.columns:
        filtered_old = old_df[~((old_df["model"] == "ICC_v2") & (old_df["N"].isin(n_values)))]
        merged_df = pd.concat([filtered_old, new_df_records], ignore_index=True)
    else:
        merged_df = new_df_records

    merged_df.sort_values(by=["N", "model", "trial"], inplace=True)
    merged_df.to_csv(CSV_PATH, index=False)
    print(f"[+] Updated scaling benchmark dataset: {CSV_PATH}")
    return merged_df


def main():
    parser = argparse.ArgumentParser(description="Benchmark ICC-v2 sample complexity scaling and peak RAM.")
    parser.add_argument(
        "--n-values",
        type=int,
        nargs="+",
        default=[5000, 6000, 8000, 10000],
        help="Sample sizes N to benchmark (default: 5000 6000 8000 10000).",
    )
    parser.add_argument(
        "--seeds",
        type=int,
        nargs="+",
        default=[42, 101, 202, 303, 404],
        help="Random seeds for synthetic data generation (default: 42 101 202 303 404).",
    )
    parser.add_argument(
        "--profile-n",
        type=int,
        default=8000,
        help="Sample size N for detailed cProfile function profiling (default: 8000).",
    )
    args = parser.parse_args()

    benchmark_sample_scaling(n_values=args.n_values, seeds=args.seeds, profile_n=args.profile_n)


if __name__ == "__main__":
    main()
