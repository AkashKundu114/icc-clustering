import time
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

import sys
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from icc.datasets.registry import load_dataset
from icc.core import run_clusterer
from icc.baselines.consensus import run_standard_consensus, run_icc_v1
from icc.consensus_v2 import InvariantCoreConsensusV2
from experiments.exp2_ablation.src.ablation_engine import extract_vssg_candidate_features

DATASETS = ["cns", "colon", "leukemia", "ovarian", "prostate", "srbct"]
SEEDS = list(range(10))  # Fixed seeds 0 to 9 per PREREG_B.md

def run_ablation_for_dataset(name: str):
    X, y, meta = load_dataset(name)
    N, D = X.shape
    K = meta["K"]
    print(f"\n==========================================")
    print(f"Benchmarking 2x2 Factorial on {name.upper()}: N={N}, D={D}, K={K}")
    print(f"==========================================")

    # BGSS Feature pool
    vssg_idx = extract_vssg_candidate_features(X, k=K)
    X_bgss = X[:, vssg_idx]
    print(f"BGSS active features: {len(vssg_idx)} / {D} ({len(vssg_idx)/D*100:.1f}%)")

    records = []

    for seed in SEEDS:
        # 1. Ambient K-Means (Cell 0, 0)
        t0 = time.perf_counter()
        pred_amb_km = KMeans(n_clusters=K, n_init=5, random_state=seed).fit_predict(X)
        records.append({
            "dataset": name, "N": N, "D": D, "K": K, "active_D": D,
            "variant": "Ambient_KMeans", "seed": seed,
            "ari": adjusted_rand_score(y, pred_amb_km),
            "nmi": normalized_mutual_info_score(y, pred_amb_km),
            "runtime_s": time.perf_counter() - t0
        })

        # 2. BGSS K-Means (Cell 1, 0 / V1)
        t0 = time.perf_counter()
        pred_bgss_km = KMeans(n_clusters=K, n_init=5, random_state=seed).fit_predict(X_bgss)
        records.append({
            "dataset": name, "N": N, "D": D, "K": K, "active_D": len(vssg_idx),
            "variant": "BGSS_KMeans", "seed": seed,
            "ari": adjusted_rand_score(y, pred_bgss_km),
            "nmi": normalized_mutual_info_score(y, pred_bgss_km),
            "runtime_s": time.perf_counter() - t0
        })

        # 3. Ambient Standard Consensus (Cell 0, 1 / V0)
        t0 = time.perf_counter()
        pred_amb_cons, _, _ = run_standard_consensus(X, k=K, n_base_models=25, seed=seed)
        records.append({
            "dataset": name, "N": N, "D": D, "K": K, "active_D": D,
            "variant": "Ambient_StdConsensus", "seed": seed,
            "ari": adjusted_rand_score(y, pred_amb_cons),
            "nmi": normalized_mutual_info_score(y, pred_amb_cons),
            "runtime_s": time.perf_counter() - t0
        })

        # 4. BGSS Standard Consensus (Cell 1, 1a / V2)
        t0 = time.perf_counter()
        pred_bgss_cons, _, _ = run_standard_consensus(X_bgss, k=K, n_base_models=25, seed=seed)
        records.append({
            "dataset": name, "N": N, "D": D, "K": K, "active_D": len(vssg_idx),
            "variant": "BGSS_StdConsensus", "seed": seed,
            "ari": adjusted_rand_score(y, pred_bgss_cons),
            "nmi": normalized_mutual_info_score(y, pred_bgss_cons),
            "runtime_s": time.perf_counter() - t0
        })

        # 5. Ambient Anchor Consensus (Cell 0, 1b / V3)
        t0 = time.perf_counter()
        pred_amb_anch, _, _ = run_icc_v1(X, k=K, n_base_models=25, n_anchors=min(40, N), seed=seed)
        records.append({
            "dataset": name, "N": N, "D": D, "K": K, "active_D": D,
            "variant": "Ambient_AnchorConsensus", "seed": seed,
            "ari": adjusted_rand_score(y, pred_amb_anch),
            "nmi": normalized_mutual_info_score(y, pred_amb_anch),
            "runtime_s": time.perf_counter() - t0
        })

        # 6. BGSS Random Anchors (Cell 1, 1b / V4)
        t0 = time.perf_counter()
        m_v4 = InvariantCoreConsensusV2(
            n_clusters=K, n_base_models=25, n_anchors=min(40, N),
            subspace_rate=0.30, core_quantile=0.0, random_state=seed
        )
        pred_v4 = m_v4.fit_predict(X)
        records.append({
            "dataset": name, "N": N, "D": D, "K": K, "active_D": len(vssg_idx),
            "variant": "BGSS_RandomAnchors", "seed": seed,
            "ari": adjusted_rand_score(y, pred_v4),
            "nmi": normalized_mutual_info_score(y, pred_v4),
            "runtime_s": time.perf_counter() - t0
        })

        # 7. BGSS Core Certified Anchors (Cell 1, 1c / V5 / Full ICC-v2)
        t0 = time.perf_counter()
        m_v5 = InvariantCoreConsensusV2(
            n_clusters=K, n_base_models=25, n_anchors=min(40, N),
            subspace_rate=0.30, core_quantile=0.50, random_state=seed
        )
        pred_v5 = m_v5.fit_predict(X)
        records.append({
            "dataset": name, "N": N, "D": D, "K": K, "active_D": len(vssg_idx),
            "variant": "Full_ICC_v2", "seed": seed,
            "ari": adjusted_rand_score(y, pred_v5),
            "nmi": normalized_mutual_info_score(y, pred_v5),
            "runtime_s": time.perf_counter() - t0
        })

    df = pd.DataFrame(records)
    summary = df.groupby("variant")["ari"].agg(["mean", "std", "median"])
    print("\nSummary for", name.upper())
    print(summary)
    return df

def main():
    out_dir = Path("results/exp2_ablation")
    out_dir.mkdir(parents=True, exist_ok=True)
    all_dfs = []

    for name in DATASETS:
        df_ds = run_ablation_for_dataset(name)
        all_dfs.append(df_ds)

    total_df = pd.concat(all_dfs, ignore_index=True)
    csv_path = out_dir / "exp2_real_high_d_factorial.csv"
    total_df.to_csv(csv_path, index=False)
    print(f"\n=======================================================")
    print(f"Successfully saved all 2x2 factorial runs to {csv_path}")
    print(f"Total rows: {len(total_df)}")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
