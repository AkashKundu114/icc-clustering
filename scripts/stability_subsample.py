"""
scripts/stability_subsample.py

Pre-registered Subsample Stability and Permutation Null Benchmark
as defined in results/PLAN_STAB.md.

Protocol:
- 6 High-D cohorts: Colon, SRBCT, CNS, Leukemia, Prostate, Ovarian.
- 12 Clustering Methods:
    K-Means, Ward, Spectral, FCM, Standard Consensus, Core-Halo Consensus,
    FCAG, FastMVC, CoHiRF, Ungated AC, GAC Pipeline, DEC.
- 30 Subsamples of 80% class-stratified samples without replacement (seeds 5000..5029).
- Algorithm seed fixed to 0 for every subsample fit.
- Pairwise intersection ARI across all 435 pairs of subsamples (subsample stability).
- Accuracy: ARI against clinical true labels on each subsample.
- Permutation Null Control: independent permutation of each feature column across samples
  (seeds 6000..6029), clustered on matching 80% subsample, measuring null subsample stability.
- Resumable: saves individual fit records to results/stability/runs/*.parquet (or csv).
"""

import os
import sys
import time
import argparse
from pathlib import Path
from itertools import combinations
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score
from sklearn.model_selection import StratifiedShuffleSplit

# Ensure root in sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from icc.datasets.registry import load_dataset
from icc.baselines import (
    run_kmeans,
    run_ward,
    run_spectral,
    run_fcm,
    run_standard_consensus,
    run_li_et_al_2019,
    run_fcag,
    run_fastmvc,
    run_cohirf,
    run_icc_v1,
    run_icc_v2,
    run_dec,
)

HIGH_D_DATASETS = ["colon", "srbct", "cns", "leukemia", "prostate", "ovarian"]

MODELS = {
    "K-Means": run_kmeans,
    "Ward": run_ward,
    "Spectral": run_spectral,
    "FCM": run_fcm,
    "StdCons": run_standard_consensus,
    "CoreHalo": run_li_et_al_2019,
    "FCAG": run_fcag,
    "FastMVC": run_fastmvc,
    "CoHiRF": run_cohirf,
    "UngatedAC": run_icc_v1,
    "GAC": run_icc_v2,
    "DEC": run_dec,
}

RUNS_DIR = ROOT / "results" / "stability" / "runs"
PARTITIONS_DIR = ROOT / "results" / "stability" / "partitions"
RUNS_DIR.mkdir(parents=True, exist_ok=True)
PARTITIONS_DIR.mkdir(parents=True, exist_ok=True)


def get_stratified_subsample(y: np.ndarray, seed: int, train_size: float = 0.80) -> np.ndarray:
    """Draws class-stratified subsample indices without replacement."""
    sss = StratifiedShuffleSplit(n_splits=1, train_size=train_size, random_state=seed)
    train_idx, _ = next(sss.split(np.zeros(len(y)), y))
    return np.sort(train_idx)


def generate_permuted_null(X: np.ndarray, seed: int) -> np.ndarray:
    """Permutes each feature column independently across samples to break correlations."""
    rng = np.random.RandomState(seed)
    X_null = np.empty_like(X)
    for col in range(X.shape[1]):
        X_null[:, col] = rng.permutation(X[:, col])
    return X_null


def run_single_fit(
    dataset_name: str,
    model_name: str,
    subsample_id: int,
    mode: str, # "real" or "null"
    X_full: np.ndarray,
    y_full: np.ndarray,
    k: int,
) -> dict:
    """Executes a single subsample fit, saving partition labels and metadata."""
    run_file = RUNS_DIR / f"{dataset_name}_{model_name}_{mode}_{subsample_id}.parquet"
    if run_file.exists():
        try:
            return pd.read_parquet(run_file).to_dict(orient="records")[0]
        except Exception:
            pass

    sub_seed = 5000 + subsample_id
    null_seed = 6000 + subsample_id if mode == "null" else -1
    sub_idx = get_stratified_subsample(y_full, sub_seed, train_size=0.80)

    if mode == "real":
        X_sub = X_full[sub_idx]
    else:
        X_null = generate_permuted_null(X_full, null_seed)
        X_sub = X_null[sub_idx]

    fn = MODELS[model_name]
    t0 = time.time()
    status = "success"
    labels = None
    try:
        labels, rt, _ = fn(X_sub, k, seed=0)
        labels = np.asarray(labels, dtype=int)
    except Exception as e:
        status = f"failed: {str(e)[:100]}"
        labels = np.zeros(len(sub_idx), dtype=int)

    runtime = time.time() - t0

    acc = float(adjusted_rand_score(y_full[sub_idx], labels)) if mode == "real" and status == "success" else (0.0 if status != "success" else np.nan)

    # Save partition
    part_file = PARTITIONS_DIR / f"{dataset_name}_{model_name}_{mode}_{subsample_id}.npy"
    np.save(part_file, {"sub_idx": sub_idx, "labels": labels})

    rec = {
        "dataset": dataset_name,
        "model": model_name,
        "mode": mode,
        "subsample_id": subsample_id,
        "sub_seed": sub_seed,
        "null_seed": null_seed,
        "status": status,
        "runtime": runtime,
        "accuracy": acc,
        "n_samples": len(sub_idx),
    }
    df = pd.DataFrame([rec])
    df.to_parquet(run_file, index=False)
    return rec


def evaluate_stability(dataset_name: str, model_name: str, mode: str) -> float:
    """Computes mean pairwise ARI across all 435 pairs of subsamples on their intersection."""
    partitions = []
    for sub_id in range(30):
        part_file = PARTITIONS_DIR / f"{dataset_name}_{model_name}_{mode}_{sub_id}.npy"
        if not part_file.exists():
            return np.nan
        data = np.load(part_file, allow_pickle=True).item()
        partitions.append(data)

    pairwise_aris = []
    for i, j in combinations(range(30), 2):
        idx_i, lbl_i = partitions[i]["sub_idx"], partitions[i]["labels"]
        idx_j, lbl_j = partitions[j]["sub_idx"], partitions[j]["labels"]

        shared = np.intersect1d(idx_i, idx_j)
        if len(shared) < 2:
            continue

        # Map shared indices to local positions
        map_i = {val: pos for pos, val in enumerate(idx_i)}
        map_j = {val: pos for pos, val in enumerate(idx_j)}

        pos_i = [map_i[s] for s in shared]
        pos_j = [map_j[s] for s in shared]

        ari = float(adjusted_rand_score(lbl_i[pos_i], lbl_j[pos_j]))
        pairwise_aris.append(ari)

    return float(np.mean(pairwise_aris)) if pairwise_aris else np.nan


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default=None)
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--skip-dec", action="store_true")
    parser.add_argument("--compile-only", action="store_true")
    args = parser.parse_args()

    datasets = [args.dataset] if args.dataset else HIGH_D_DATASETS
    models = [args.model] if args.model else list(MODELS.keys())
    if args.skip_dec and "DEC" in models:
        models.remove("DEC")

    if not args.compile_only:
        print(f"[*] Starting Subsample Stability Run: {len(datasets)} datasets x {len(models)} models x 30 subsamples x 2 modes")
        total_fits = len(datasets) * len(models) * 30 * 2
        fit_idx = 0

        for d_name in datasets:
            X, y, meta = load_dataset(d_name)
            k = meta["K"]
            print(f"\n--- Dataset: {d_name.upper()} (N={len(X)}, D={X.shape[1]}, K={k}) ---")

            for m_name in models:
                t_m0 = time.time()
                for mode in ["real", "null"]:
                    for sub_id in range(30):
                        fit_idx += 1
                        rec = run_single_fit(d_name, m_name, sub_id, mode, X, y, k)
                print(f"  [{m_name:10s}] completed real & null 30 subsamples in {time.time()-t_m0:.2f}s")

    print("\n[*] Compiling Subsample Stability and Null Control Metrics...")
    summary_records = []
    
    # Load old seed stability for comparison if available
    old_summary_file = ROOT / "results" / "stability" / "real_data_stability_summary.csv"
    old_data = {}
    if old_summary_file.exists():
        old_df = pd.read_csv(old_summary_file)
        for _, row in old_df.iterrows():
            d = str(row["dataset"]).lower()
            m = str(row["model"])
            old_data[(d, m)] = {
                "seed_stab": row["Stability"],
                "seed_gap": row["Gap"],
                "seed_ari": row["ARI"],
            }

    for d_name in HIGH_D_DATASETS:
        for m_name in MODELS.keys():
            # Check if all 30 real and null exist
            real_stab = evaluate_stability(d_name, m_name, "real")
            null_stab = evaluate_stability(d_name, m_name, "null")

            # Collect real accuracies
            accs = []
            for sub_id in range(30):
                rf = RUNS_DIR / f"{d_name}_{m_name}_real_{sub_id}.parquet"
                if rf.exists():
                    try:
                        accs.append(pd.read_parquet(rf)["accuracy"].iloc[0])
                    except Exception:
                        pass
            real_acc = float(np.mean(accs)) if accs else np.nan
            gap = real_stab - real_acc if not np.isnan(real_stab) and not np.isnan(real_acc) else np.nan

            # Pre-registered Decision Rules
            # (i) Stable but Wrong: real_stab >= 0.50 and real_acc <= 0.05
            stable_but_wrong = (real_stab >= 0.50 and real_acc <= 0.05) if not np.isnan(real_stab) else False
            # (ii) Uninformative: (real_stab - null_stab) < 0.10 and real_acc <= 0.05
            uninformative = ((real_stab - null_stab) < 0.10 and real_acc <= 0.05) if not np.isnan(real_stab) and not np.isnan(null_stab) else False

            old_info = old_data.get((d_name, m_name), {})

            summary_records.append({
                "dataset": d_name,
                "model": m_name,
                "subsample_accuracy": real_acc,
                "subsample_stability": real_stab,
                "subsample_gap": gap,
                "null_stability": null_stab,
                "stab_minus_null": real_stab - null_stab if not np.isnan(real_stab) and not np.isnan(null_stab) else np.nan,
                "rule_i_stable_but_wrong": stable_but_wrong,
                "rule_ii_uninformative": uninformative,
                "seed_stability": old_info.get("seed_stab", np.nan),
                "seed_gap": old_info.get("seed_gap", np.nan),
            })

    sum_df = pd.DataFrame(summary_records)
    out_csv = ROOT / "results" / "stability" / "subsample_stability_summary.csv"
    sum_df.to_csv(out_csv, index=False)
    print(f"\n[+] Saved Subsample Stability Summary to {out_csv}")
    print(sum_df[["dataset", "model", "subsample_accuracy", "subsample_stability", "subsample_gap", "null_stability", "rule_i_stable_but_wrong"]].head(24))


if __name__ == "__main__":
    main()
