"""
Real-data benchmark evaluation reproduction engine.

Evaluates and compares GAC (ICC-v2) against Standard K-Means on real-world
biomedical datasets (Leukemia, SRBCT, Colon, Lymphoma) across specified random seeds,
computing Adjusted Rand Index (ARI) and Normalized Mutual Information (NMI).

Usage:
    python scripts/reproduce_benchmarks.py
    python scripts/reproduce_benchmarks.py --datasets leukemia srbct --seeds 0 1 2 3 4
    python scripts/reproduce_benchmarks.py --output results/benchmarks_reproduced.csv
"""

import argparse
import os
import time
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

from icc import ICC
from icc.datasets.registry import load_dataset

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results"

BENCHMARK_CONFIGS = {
    "leukemia": {"K": 2, "name": "Leukemia", "domain": "Genomics"},
    "srbct": {"K": 4, "name": "SRBCT", "domain": "Genomics"},
    "colon": {"K": 2, "name": "Colon", "domain": "Genomics"},
    "lymphoma": {"K": 2, "name": "Lymphoma", "domain": "Genomics"},
}


def load_target_dataset(dataset_key: str) -> Tuple[np.ndarray, np.ndarray, Dict]:
    """
    Load benchmark dataset, with dedicated fallback for lymphoma cache if needed.
    """
    key = dataset_key.lower().strip()
    if key == "lymphoma":
        cache_paths = [
            ROOT / "data" / "cache" / "lymphoma.npz",
            ROOT / "experiments" / "exp3_real_world_benchmarks" / "data" / "cache" / "lymphoma.npz",
        ]
        for p in cache_paths:
            if p.exists():
                data = np.load(p)
                X = np.asarray(data["X"], dtype=np.float64)
                y = np.asarray(data["y"])
                metadata = {
                    "name": "lymphoma",
                    "N": int(X.shape[0]),
                    "D": int(X.shape[1]),
                    "K": int(len(np.unique(y))),
                    "d_over_n": round(float(X.shape[1] / X.shape[0]), 2),
                }
                return X, y, metadata

    return load_dataset(key)


def run_benchmark_evaluations(
    datasets: List[str],
    seeds: List[int],
    n_init: int = 10,
    output_csv: Path = RESULTS_DIR / "benchmarks_reproduced.csv",
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Run evaluation across specified datasets and seeds.
    """
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"

    records = []
    print("=" * 85)
    print("ICC-v2 Real-Data Benchmark Reproduction Suite")
    print("=" * 85)
    print(f"Target Datasets: {', '.join([BENCHMARK_CONFIGS.get(d, {}).get('name', d) for d in datasets])}")
    print(f"Random Seeds:    {seeds}")
    print("Models Compared: Standard K-Means vs. GAC Pipeline (ICC-v2)")
    print("-" * 85)

    for d in datasets:
        d_key = d.lower().strip()
        disp_name = BENCHMARK_CONFIGS.get(d_key, {}).get("name", d_key)
        try:
            X, y, meta = load_target_dataset(d_key)
        except Exception as exc:
            print(f"[!] Warning: Could not load dataset '{d}': {exc}")
            continue

        K = BENCHMARK_CONFIGS.get(d_key, {}).get("K", len(np.unique(y)))
        N, D = X.shape
        print(f"\n[*] Evaluating Dataset: {disp_name} (N={N}, D={D}, K={K})...")

        for s in seeds:
            # 1. Standard K-Means
            t0 = time.perf_counter()
            km = KMeans(n_clusters=K, random_state=s, n_init=n_init)
            km_preds = km.fit_predict(X)
            km_time = time.perf_counter() - t0
            km_ari = float(adjusted_rand_score(y, km_preds))
            km_nmi = float(normalized_mutual_info_score(y, km_preds))

            records.append({
                "Dataset": disp_name,
                "Seed": s,
                "Method": "Standard K-Means",
                "ARI": km_ari,
                "NMI": km_nmi,
                "Time_s": km_time,
            })

            # 2. GAC (ICC-v2)
            t0 = time.perf_counter()
            gac = ICC(n_clusters=K, random_state=s)
            gac_preds = gac.fit_predict(X)
            gac_time = time.perf_counter() - t0
            gac_ari = float(adjusted_rand_score(y, gac_preds))
            gac_nmi = float(normalized_mutual_info_score(y, gac_preds))

            records.append({
                "Dataset": disp_name,
                "Seed": s,
                "Method": "GAC (ICC-v2)",
                "ARI": gac_ari,
                "NMI": gac_nmi,
                "Time_s": gac_time,
            })

            delta_ari = gac_ari - km_ari
            delta_sign = "+" if delta_ari >= 0 else ""
            print(
                f"  Seed {s:2d} | KM: ARI={km_ari:+.4f}, NMI={km_nmi:.4f} | "
                f"GAC: ARI={gac_ari:+.4f}, NMI={gac_nmi:.4f} | Delta ARI={delta_sign}{delta_ari:.4f}"
            )

    df_runs = pd.DataFrame(records)

    # Compute Summary Aggregation
    summary_rows = []
    if not df_runs.empty:
        for d in df_runs["Dataset"].unique():
            for m in ["Standard K-Means", "GAC (ICC-v2)"]:
                sub = df_runs[(df_runs["Dataset"] == d) & (df_runs["Method"] == m)]
                if not sub.empty:
                    summary_rows.append({
                        "Dataset": d,
                        "Method": m,
                        "Mean ARI": float(sub["ARI"].mean()),
                        "Std ARI": float(sub["ARI"].std()) if len(sub) > 1 else 0.0,
                        "Mean NMI": float(sub["NMI"].mean()),
                        "Std NMI": float(sub["NMI"].std()) if len(sub) > 1 else 0.0,
                        "Mean Time (s)": float(sub["Time_s"].mean()),
                    })

    df_summary = pd.DataFrame(summary_rows)

    # Format Summary Table
    print("\n" + "=" * 85)
    print("Aggregate Benchmark Summary (Mean +/- Std Across Seeds)")
    print("=" * 85)

    disp_summary = []
    for _, row in df_summary.iterrows():
        disp_summary.append({
            "Dataset": row["Dataset"],
            "Method": row["Method"],
            "ARI (Mean +/- Std)": f"{row['Mean ARI']:+.3f} +/- {row['Std ARI']:.3f}",
            "NMI (Mean +/- Std)": f"{row['Mean NMI']:.3f} +/- {row['Std NMI']:.3f}",
            "Mean Runtime (s)": f"{row['Mean Time (s)']:.2f}s",
        })

    df_disp = pd.DataFrame(disp_summary)
    print("\n" + df_disp.to_string(index=False) + "\n")

    if output_csv:
        output_csv = Path(output_csv)
        output_csv.parent.mkdir(parents=True, exist_ok=True)
        df_runs.to_csv(output_csv, index=False)
        print(f"[*] Per-seed evaluation records saved to: {output_csv}")

    print("=" * 85 + "\n")
    return df_runs, df_summary


def main():
    parser = argparse.ArgumentParser(description="ICC-v2 Real-Data Benchmark Reproduction Engine")
    parser.add_argument(
        "--datasets",
        nargs="+",
        default=["leukemia", "srbct", "colon", "lymphoma"],
        help="Datasets to evaluate (default: leukemia srbct colon lymphoma)",
    )
    parser.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        default=[0, 1, 2],
        help="Random seeds to evaluate (default: 0 1 2)",
    )
    parser.add_argument(
        "--n-init",
        type=int,
        default=10,
        help="Number of K-Means initializations (default: 10)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results/benchmarks_reproduced.csv",
        help="Output CSV path for per-seed evaluation records",
    )
    args = parser.parse_args()

    run_benchmark_evaluations(
        datasets=args.datasets,
        seeds=args.seeds,
        n_init=args.n_init,
        output_csv=ROOT / args.output,
    )


if __name__ == "__main__":
    main()
