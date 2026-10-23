"""
Compute 30-seed 2x2 Factorial Ablation for Pass F:
Variants:
- Ambient_KMeans (V1)
- Ambient_StdConsensus (V2)
- BGSS_KMeans (V3)
- BGSS_StdConsensus (V4)
- BGSS_RandomAnchors (V4_Anchor)
- Full_ICC_v2 (V5)
Datasets: cns, colon, leukemia, ovarian, prostate, srbct
Seeds: 0-29 (30 seeds)
"""

import sys
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from scipy.stats import wilcoxon

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from icc.datasets.registry import load_dataset
from icc.consensus_v2 import InvariantCoreConsensusV2
from icc.baselines.consensus import run_standard_consensus, run_icc_v1
from experiments.exp2_ablation.src.ablation_engine import extract_vssg_candidate_features

OUT_DIR = Path("results/passF")
OUT_DIR.mkdir(parents=True, exist_ok=True)

HIGH_D_DATASETS = ["cns", "colon", "leukemia", "ovarian", "prostate", "srbct"]
SEEDS = list(range(30))

def main():
    out_file = OUT_DIR / "ablation_30seeds_passF.csv"
    existing_records = []
    done_keys = set()
    if out_file.exists():
        existing_records = pd.read_csv(out_file).to_dict(orient="records")
        done_keys = set((r['dataset'], r['variant'], r['seed']) for r in existing_records)
        print(f"Found {len(existing_records)} existing records in {out_file}")

    # Load seeds 0-9 from passE if not already present
    if not existing_records and Path("results/passE/ablation_2x2_seeds0_9.csv").exists():
        df_e = pd.read_csv("results/passE/ablation_2x2_seeds0_9.csv")
        existing_records = df_e.to_dict(orient="records")
        done_keys = set((r['dataset'], r['variant'], r['seed']) for r in existing_records)
        print(f"Loaded {len(existing_records)} seeds 0-9 records from Pass E")

    records = list(existing_records)

    for dname in HIGH_D_DATASETS:
        X, y, _ = load_dataset(dname)
        N, D = X.shape
        K = len(np.unique(y))
        vssg_idx = extract_vssg_candidate_features(X, k=K)
        X_bgss = X[:, vssg_idx]

        for seed in range(10, 30):
            # Ambient K-Means
            if (dname, "Ambient_KMeans", seed) not in done_keys:
                km_amb = KMeans(n_clusters=K, n_init=10, random_state=seed).fit_predict(X)
                records.append({"dataset": dname, "variant": "Ambient_KMeans", "seed": seed, "ari": adjusted_rand_score(y, km_amb)})

            # Ambient Std Consensus (V2)
            if (dname, "Ambient_StdConsensus", seed) not in done_keys:
                p_v0, _, _ = run_standard_consensus(X, K, n_base_models=25, seed=seed)
                records.append({"dataset": dname, "variant": "Ambient_StdConsensus", "seed": seed, "ari": adjusted_rand_score(y, p_v0)})

            # BGSS K-Means (V3)
            if (dname, "BGSS_KMeans", seed) not in done_keys:
                km_bgss = KMeans(n_clusters=K, n_init=10, random_state=seed).fit_predict(X_bgss)
                records.append({"dataset": dname, "variant": "BGSS_KMeans", "seed": seed, "ari": adjusted_rand_score(y, km_bgss)})

            # BGSS Std Consensus (V4)
            if (dname, "BGSS_StdConsensus", seed) not in done_keys:
                p_v2, _, _ = run_standard_consensus(X_bgss, K, n_base_models=25, seed=seed)
                records.append({"dataset": dname, "variant": "BGSS_StdConsensus", "seed": seed, "ari": adjusted_rand_score(y, p_v2)})

            # Ambient Anchor Consensus (ICC-v1)
            if (dname, "Ambient_AnchorConsensus", seed) not in done_keys:
                p_v3, _, _ = run_icc_v1(X, K, n_base_models=25, n_anchors=min(40, N), seed=seed)
                records.append({"dataset": dname, "variant": "Ambient_AnchorConsensus", "seed": seed, "ari": adjusted_rand_score(y, p_v3)})

            # BGSS + Random Anchors (V4_Anchor)
            if (dname, "BGSS_RandomAnchors", seed) not in done_keys:
                m_v4 = InvariantCoreConsensusV2(
                    n_clusters=K, n_base_models=25, n_anchors=min(40, N),
                    subspace_rate=0.30, core_quantile=0.0, random_state=seed
                )
                p_v4 = m_v4.fit_predict(X)
                records.append({"dataset": dname, "variant": "BGSS_RandomAnchors", "seed": seed, "ari": adjusted_rand_score(y, p_v4)})

            # Full ICC-v2 (V5)
            if (dname, "Full_ICC_v2", seed) not in done_keys:
                m_v5 = InvariantCoreConsensusV2(
                    n_clusters=K, n_base_models=25, n_anchors=min(40, N),
                    subspace_rate=0.30, core_quantile=0.50, random_state=seed
                )
                p_v5 = m_v5.fit_predict(X)
                records.append({"dataset": dname, "variant": "Full_ICC_v2", "seed": seed, "ari": adjusted_rand_score(y, p_v5)})

        pd.DataFrame(records).to_csv(out_file, index=False)
        print(f"Processed {dname.upper()}: total records {len(records)}")

    df = pd.DataFrame(records)
    df.to_csv(out_file, index=False)
    print(f"\n[OK] Saved {len(df)} 30-seed ablation records to {out_file}")

    # Summary
    grouped = df.groupby(["variant", "dataset"])["ari"].mean().unstack()
    print("\nMean ARI per variant per dataset (30 seeds):")
    print(grouped.round(3).to_string())

    mean_per_variant = grouped.mean(axis=1)
    print("\nOverall High-D Subgroup Mean ARI (30 seeds):")
    print(mean_per_variant.round(3).to_string())

    # V5 vs V4 dataset bootstrap
    # V5: Full_ICC_v2, V4: BGSS_RandomAnchors
    v5_means = grouped.loc["Full_ICC_v2"]
    v4_means = grouped.loc["BGSS_RandomAnchors"]
    diffs = v5_means - v4_means
    print("\nPer-dataset difference (V5 - V4):")
    print(diffs.round(3))

    rng = np.random.default_rng(42)
    boot_diffs = [np.mean(rng.choice(diffs.values, size=len(diffs), replace=True)) for _ in range(2000)]
    ci_low = float(np.percentile(boot_diffs, 2.5))
    ci_high = float(np.percentile(boot_diffs, 97.5))
    w_stat, w_p = wilcoxon(diffs.values)

    print(f"\nV5 vs V4: Mean Diff = {diffs.mean():+.4f}, 95% CI = [{ci_low:+.4f}, {ci_high:+.4f}], Wilcoxon W = {w_stat}, p = {w_p:.4f}")

    with open(OUT_DIR / "ablation_stats_passF.json", "w", encoding="utf-8") as fp:
        json.dump({
            "means": mean_per_variant.to_dict(),
            "v5_vs_v4": {
                "mean_diff": float(diffs.mean()),
                "ci_95": [ci_low, ci_high],
                "wilcoxon_w": float(w_stat),
                "wilcoxon_p": float(w_p)
            }
        }, fp, indent=2)

if __name__ == "__main__":
    main()
