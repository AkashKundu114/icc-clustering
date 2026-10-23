"""
Unified Pass E Experiment Runner.
Executes canonical seeds 0-9 across:
  1. 2x2 Factorial Ablation on 6 High-D datasets
  2. Fair Feature-Matched Baselines on 6 High-D datasets
  3. Direct Inductive Extension on held-out test splits + Prediction Agreement
  4. 13-Dataset Omnibus Benchmark Matrix across 11 candidate models
Saves all outputs into results/passE/ with complete config hashes.
"""

import sys
import time
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Tuple

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedShuffleSplit

# Ensure project root is available
_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from icc.datasets.registry import load_dataset
from icc.consensus_v2 import InvariantCoreConsensusV2
from icc.baselines.consensus import run_standard_consensus, run_icc_v1, run_li_et_al_2019
from icc.baselines.classical import run_single_kmeans, run_single_ward, run_single_spectral, run_single_fcm
from icc.baselines.anchor import run_fcag, run_fastmvc
from icc.baselines.deep import run_dec
from experiments.exp2_ablation.src.ablation_engine import extract_vssg_candidate_features

CANONICAL_SEEDS = list(range(10))
HIGH_D_DATASETS = ["cns", "colon", "leukemia", "ovarian", "prostate", "srbct"]
INDUCTIVE_DATASETS = ["cns", "colon", "leukemia", "ovarian", "srbct", "isolet"]
OMNIBUS_DATASETS = [
    "cns", "colon", "indian_pines", "isolet", "leukemia",
    "madelon", "newsgroups20", "ovarian", "prostate", "sonar",
    "srbct", "yale_b", "zheng68k"
]

OUT_DIR = Path("results/passE")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def get_config_hashes() -> Dict[str, str]:
    configs = {
        "ICC_v2": {
            "n_base_models": 25, "n_anchors": 40, "core_quantile": 0.5,
            "subspace_rate": 0.3, "pool_mode": "legacy", "pool_frac": 0.15
        },
        "Standard_Consensus": {"n_base_models": 25, "base_clusterer": "kmeans"},
        "Core_Halo_Consensus": {"n_base_models": 25, "core_quantile": 0.5},
        "ICC_v1": {"n_base_models": 25, "n_anchors": 40},
        "K-Means": {"n_init": 10, "algorithm": "lloyd"},
        "Ward": {"linkage": "ward"},
        "Spectral": {"n_neighbors": 10, "assign_labels": "kmeans"},
        "FCM": {"m": 2.0, "max_iter": 150},
        "DEC": {"pretrain_epochs": 200, "finetune_epochs": 100, "latent_dim": 10},
        "FCAG": {"n_anchors": 40},
        "FastMVC": {"n_anchors": 40}
    }
    hashes = {}
    for k, v in configs.items():
        hashes[k] = hashlib.sha256(json.dumps(v, sort_keys=True).encode()).hexdigest()[:12]
    return hashes


# ==============================================================================
# STAGE 1: 2x2 High-D Factorial Ablation
# ==============================================================================
def run_stage1_ablation():
    print("=" * 70)
    print("STAGE 1: 2x2 Factorial Ablation on 6 High-D Datasets (Seeds 0-9)")
    print("=" * 70)
    out_file = OUT_DIR / "ablation_2x2_seeds0_9.csv"
    if out_file.exists():
        df = pd.read_csv(out_file)
        if len(df) == 6 * 7 * 10:  # 420 records
            print(f"  [OK] Stage 1 already complete with {len(df)} records.")
            return df

    records = []
    for name in HIGH_D_DATASETS:
        X, y, _ = load_dataset(name)
        N, D = X.shape
        K = len(np.unique(y))
        vssg_idx = extract_vssg_candidate_features(X, k=K)
        X_bgss = X[:, vssg_idx]
        print(f"  {name.upper()} (N={N}, D={D}, active_D={len(vssg_idx)}, K={K})")

        for seed in CANONICAL_SEEDS:
            # Ambient K-Means
            km_amb = KMeans(n_clusters=K, n_init=10, random_state=seed).fit_predict(X)
            records.append({"dataset": name, "variant": "Ambient_KMeans", "seed": seed, "ari": adjusted_rand_score(y, km_amb)})

            # V0: Ambient Std Consensus
            p_v0, _, _ = run_standard_consensus(X, K, n_base_models=25, seed=seed)
            records.append({"dataset": name, "variant": "Ambient_StdConsensus", "seed": seed, "ari": adjusted_rand_score(y, p_v0)})

            # V1: BGSS K-Means
            km_bgss = KMeans(n_clusters=K, n_init=10, random_state=seed).fit_predict(X_bgss)
            records.append({"dataset": name, "variant": "BGSS_KMeans", "seed": seed, "ari": adjusted_rand_score(y, km_bgss)})

            # V2: BGSS Std Consensus
            p_v2, _, _ = run_standard_consensus(X_bgss, K, n_base_models=25, seed=seed)
            records.append({"dataset": name, "variant": "BGSS_StdConsensus", "seed": seed, "ari": adjusted_rand_score(y, p_v2)})

            # V3: Ambient Anchor Consensus (ICC-v1)
            p_v3, _, _ = run_icc_v1(X, K, n_base_models=25, n_anchors=min(40, N), seed=seed)
            records.append({"dataset": name, "variant": "Ambient_AnchorConsensus", "seed": seed, "ari": adjusted_rand_score(y, p_v3)})

            # V4: BGSS + Random Anchors
            m_v4 = InvariantCoreConsensusV2(
                n_clusters=K, n_base_models=25, n_anchors=min(40, N),
                subspace_rate=0.30, core_quantile=0.0, random_state=seed
            )
            p_v4 = m_v4.fit_predict(X)
            records.append({"dataset": name, "variant": "BGSS_RandomAnchors", "seed": seed, "ari": adjusted_rand_score(y, p_v4)})

            # V5: Full ICC-v2 (BGSS + Certified Core Anchors)
            m_v5 = InvariantCoreConsensusV2(
                n_clusters=K, n_base_models=25, n_anchors=min(40, N),
                subspace_rate=0.30, core_quantile=0.50, random_state=seed
            )
            p_v5 = m_v5.fit_predict(X)
            records.append({"dataset": name, "variant": "Full_ICC_v2", "seed": seed, "ari": adjusted_rand_score(y, p_v5)})

    df = pd.DataFrame(records)
    df.to_csv(out_file, index=False)
    print(f"  [OK] Saved {len(df)} records to {out_file}")
    return df


# ==============================================================================
# STAGE 2: Fair Feature-Matched Baselines
# ==============================================================================
def compute_laplacian_score(X: np.ndarray, n_neighbors: int = 5) -> np.ndarray:
    N, D = X.shape
    from sklearn.neighbors import kneighbors_graph
    W = kneighbors_graph(X, n_neighbors=min(n_neighbors, N - 1), mode='connectivity', include_self=False).toarray()
    W = np.maximum(W, W.T)
    d = W.sum(axis=1)
    D_mat = np.diag(d)
    L = D_mat - W
    scores = np.zeros(D)
    for j in range(D):
        fj = X[:, j]
        denom = np.var(fj)
        if denom < 1e-12:
            scores[j] = 1e9
            continue
        scores[j] = (fj.T @ L @ fj) / ((fj - fj.mean()).T @ D_mat @ (fj - fj.mean()) + 1e-12)
    return scores


def run_sparse_kmeans(X: np.ndarray, k: int, random_state: int = 42, max_iter: int = 6) -> np.ndarray:
    N, D = X.shape
    labels = KMeans(n_clusters=k, n_init=1, random_state=random_state).fit_predict(X)
    w = np.ones(D) / np.sqrt(D)
    s = np.sqrt(D) * 1.1
    for _ in range(max_iter):
        a = np.zeros(D)
        for c in range(k):
            members = (labels == c)
            if members.sum() > 1:
                diff = X[members] - X[members].mean(axis=0)
                a += (diff ** 2).sum(axis=0)
        soft = np.maximum(0, a - np.percentile(a, 50))
        norm2 = np.linalg.norm(soft)
        if norm2 < 1e-12:
            break
        w = soft / (norm2 + 1e-12)
        X_w = X * np.sqrt(w)
        new_labels = KMeans(n_clusters=k, n_init=1, random_state=random_state).fit_predict(X_w)
        if np.array_equal(new_labels, labels):
            break
        labels = new_labels
    return labels


def run_stage2_fair_baselines():
    print("=" * 70)
    print("STAGE 2: Fair Feature-Matched Baselines on 6 High-D Datasets (Seeds 0-9)")
    print("=" * 70)
    out_file = OUT_DIR / "fair_baselines_seeds0_9.csv"
    if out_file.exists():
        df = pd.read_csv(out_file)
        if len(df) == 6 * 9 * 10:  # 540 records
            print(f"  [OK] Stage 2 already complete with {len(df)} records.")
            return df

    records = []
    for dname in HIGH_D_DATASETS:
        X, y, _ = load_dataset(dname)
        N, D = X.shape
        K = len(np.unique(y))
        print(f"  {dname.upper()}: N={N}, D={D}, K={K}")

        n_top = max(2, int(np.ceil(0.15 * D)))
        var_indices = np.argsort(X.var(axis=0))[-n_top:]
        X_var = X[:, var_indices]

        n_comp = min(N - 1, D, 50)
        svd = TruncatedSVD(n_components=n_comp, random_state=42)
        X_pca = svd.fit_transform(X)

        lap_scores = compute_laplacian_score(X)
        lap_indices = np.argsort(lap_scores)[:n_top]
        X_lap = X[:, lap_indices]

        for seed in CANONICAL_SEEDS:
            # K-Means All
            pred_km_all = KMeans(n_clusters=K, n_init=10, random_state=seed).fit_predict(X)
            records.append({"dataset": dname, "model": "K-Means_All", "seed": seed, "ari": adjusted_rand_score(y, pred_km_all)})

            # K-Means VarFilt
            pred_km_var = KMeans(n_clusters=K, n_init=10, random_state=seed).fit_predict(X_var)
            records.append({"dataset": dname, "model": "K-Means_VarFilt", "seed": seed, "ari": adjusted_rand_score(y, pred_km_var)})

            # K-Means PCA
            pred_km_pca = KMeans(n_clusters=K, n_init=10, random_state=seed).fit_predict(X_pca)
            records.append({"dataset": dname, "model": "K-Means_PCA", "seed": seed, "ari": adjusted_rand_score(y, pred_km_pca)})

            # K-Means LapScore
            pred_km_lap = KMeans(n_clusters=K, n_init=10, random_state=seed).fit_predict(X_lap)
            records.append({"dataset": dname, "model": "K-Means_LapScore", "seed": seed, "ari": adjusted_rand_score(y, pred_km_lap)})

            # Sparse K-Means
            pred_sparse_km = run_sparse_kmeans(X, K, random_state=seed)
            records.append({"dataset": dname, "model": "SparseKMeans", "seed": seed, "ari": adjusted_rand_score(y, pred_sparse_km)})

            # StdCons All
            pred_std_all, _, _ = run_standard_consensus(X, K, n_base_models=25, seed=seed)
            records.append({"dataset": dname, "model": "StdCons_All", "seed": seed, "ari": adjusted_rand_score(y, pred_std_all)})

            # StdCons VarFilt
            pred_std_var, _, _ = run_standard_consensus(X_var, K, n_base_models=25, seed=seed)
            records.append({"dataset": dname, "model": "StdCons_VarFilt", "seed": seed, "ari": adjusted_rand_score(y, pred_std_var)})

            # StdCons PCA
            pred_std_pca, _, _ = run_standard_consensus(X_pca, K, n_base_models=25, seed=seed)
            records.append({"dataset": dname, "model": "StdCons_PCA", "seed": seed, "ari": adjusted_rand_score(y, pred_std_pca)})

            # ICC-v2
            icc = InvariantCoreConsensusV2(n_clusters=K, random_state=seed)
            pred_icc = icc.fit_predict(X)
            records.append({"dataset": dname, "model": "ICC_v2", "seed": seed, "ari": adjusted_rand_score(y, pred_icc)})

    df = pd.DataFrame(records)
    df.to_csv(out_file, index=False)
    print(f"  [OK] Saved {len(df)} records to {out_file}")
    return df


# ==============================================================================
# STAGE 3: Direct Inductive Extension & Prediction Agreement
# ==============================================================================
def run_stage3_inductive():
    print("=" * 70)
    print("STAGE 3: Direct Inductive Extension & Per-Split Agreement (Seeds 0-9)")
    print("=" * 70)
    out_file = OUT_DIR / "inductive_direct_seeds0_9.csv"
    aggr_file = OUT_DIR / "inductive_agreement.json"

    records = []
    agreement_records = {}

    for dname in INDUCTIVE_DATASETS:
        X, y, _ = load_dataset(dname)
        N, D = X.shape
        K = len(np.unique(y))
        print(f"  {dname.upper()}: N={N}, D={D}, K={K}")

        agreements = []

        for seed in CANONICAL_SEEDS:
            try:
                sss = StratifiedShuffleSplit(n_splits=1, test_size=0.20, random_state=seed)
                train_idx, test_idx = next(sss.split(X, y))
            except ValueError:
                rng = np.random.default_rng(seed)
                perm = rng.permutation(N)
                split_pt = int(0.80 * N)
                train_idx, test_idx = perm[:split_pt], perm[split_pt:]

            X_tr, y_tr = X[train_idx], y[train_idx]
            X_te, y_te = X[test_idx], y[test_idx]

            # Fit ICC-v2 on train split
            icc = InvariantCoreConsensusV2(n_clusters=K, random_state=seed)
            y_tr_pred = icc.fit_predict(X_tr)

            # 1. Nystrom Subspace Projection
            pred_icc_sub = icc.predict(X_te, subspace=True)
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "seed": seed, "method": "ICC_v2_NystromSubspace", "ari": adjusted_rand_score(y_te, pred_icc_sub)})

            # 2. Stability-Weighted Centroid Full Projection (Eq. 6)
            pred_icc_full = icc.predict(X_te, subspace=False)
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "seed": seed, "method": "ICC_v2_CentroidFull", "ari": adjusted_rand_score(y_te, pred_icc_full)})

            # 3. Unweighted Nearest Centroid (Eq. 7)
            nc = NearestCentroid()
            nc.fit(X_tr, y_tr_pred)
            pred_nc = nc.predict(X_te)
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "seed": seed, "method": "ICC_v2_Pseudo_NearestCentroid", "ari": adjusted_rand_score(y_te, pred_nc)})

            # Measure per-split prediction agreement between weighted and unweighted assignment
            agree = float(np.mean(pred_icc_full == pred_nc))
            agreements.append(agree)

            # 4. Random Forest on pseudo-labels
            rf = RandomForestClassifier(n_estimators=100, random_state=seed)
            rf.fit(X_tr, y_tr_pred)
            pred_rf = rf.predict(X_te)
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "seed": seed, "method": "ICC_v2_Pseudo_RandomForest", "ari": adjusted_rand_score(y_te, pred_rf)})

            # 5. Ambient K-Means direct
            km = KMeans(n_clusters=K, n_init=10, random_state=seed)
            km.fit(X_tr)
            pred_km = km.predict(X_te)
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "seed": seed, "method": "KMeans_Direct", "ari": adjusted_rand_score(y_te, pred_km)})

        agreement_records[dname] = {
            "mean_agreement": float(np.mean(agreements)),
            "min_agreement": float(np.min(agreements)),
            "max_agreement": float(np.max(agreements)),
            "agreements_per_seed": agreements
        }
        print(f"    Agreement (Weighted vs Unweighted): {np.mean(agreements):.1%} (min: {np.min(agreements):.1%}, max: {np.max(agreements):.1%})")

    df = pd.DataFrame(records)
    df.to_csv(out_file, index=False)
    with open(aggr_file, "w", encoding="utf-8") as fp:
        json.dump(agreement_records, fp, indent=2)

    print(f"  [OK] Saved {len(df)} records to {out_file}")
    print(f"  [OK] Saved agreement records to {aggr_file}")
    return df, agreement_records


def run_icc_v2_wrapper(X: np.ndarray, k: int, seed: int = 42) -> Tuple[np.ndarray, float, Any]:
    t0 = time.perf_counter()
    model = InvariantCoreConsensusV2(
        n_clusters=k,
        n_base_models=25,
        n_anchors=min(40, len(X)),
        random_state=seed,
    )
    pred = model.fit_predict(X)
    elap = time.perf_counter() - t0
    return pred, elap, None


# ==============================================================================
# STAGE 4: 13-Dataset Omnibus Benchmark Matrix (Seeds 0-9)
# ==============================================================================
def run_stage4_omnibus():
    print("=" * 70)
    print("STAGE 4: 13-Dataset Omnibus Benchmark Matrix (Seeds 0-9)")
    print("=" * 70)
    out_file = OUT_DIR / "benchmark_matrix_seeds0_9.csv"

    existing_records = []
    if out_file.exists():
        existing_records = pd.read_csv(out_file).to_dict(orient="records")
        done_keys = set((r['dataset'], r['model'], r['seed']) for r in existing_records)
        print(f"  Found {len(existing_records)} existing records.")
        if len(existing_records) == 13 * 11 * 10:
            print("  [OK] Stage 4 already fully complete.")
            return pd.DataFrame(existing_records)
    else:
        done_keys = set()

    records = list(existing_records)

    models_dict = {
        "K-Means": run_single_kmeans,
        "Ward": run_single_ward,
        "Spectral": run_single_spectral,
        "FCM": run_single_fcm,
        "Standard_Consensus": run_standard_consensus,
        "Core_Halo_Consensus": run_li_et_al_2019,
        "ICC_v1": run_icc_v1,
        "ICC_v2": run_icc_v2_wrapper,
        "DEC": run_dec,
        "FCAG": run_fcag,
        "FastMVC": run_fastmvc
    }

    for dname in OMNIBUS_DATASETS:
        X, y, _ = load_dataset(dname)
        N, D = X.shape
        K = len(np.unique(y))
        print(f"\nProcessing {dname.upper()} (N={N}, D={D}, K={K})...")

        for mname, mfunc in models_dict.items():
            # Optimization for Ward linkage: deterministic across seeds
            if mname == "Ward" and all((dname, mname, s) not in done_keys for s in CANONICAL_SEEDS):
                t0 = time.perf_counter()
                try:
                    pred, elap, _ = mfunc(X, K)
                    score_ari = adjusted_rand_score(y, pred)
                    score_nmi = normalized_mutual_info_score(y, pred)
                except Exception as e:
                    print(f"    [Error] {mname} on {dname}: {e}")
                    score_ari, score_nmi, elap = 0.0, 0.0, time.perf_counter() - t0

                for s in CANONICAL_SEEDS:
                    rec = {
                        "dataset": dname, "N": N, "D": D, "K": K,
                        "model": mname, "seed": s,
                        "ari": score_ari, "nmi": score_nmi,
                        "elapsed_sec": elap
                    }
                    records.append(rec)
                    done_keys.add((dname, mname, s))
                pd.DataFrame(records).to_csv(out_file, index=False)
                continue

            for seed in CANONICAL_SEEDS:
                if (dname, mname, seed) in done_keys:
                    continue

                t0 = time.perf_counter()
                try:
                    pred, elap, _ = mfunc(X, K, seed=seed)
                    score_ari = adjusted_rand_score(y, pred)
                    score_nmi = normalized_mutual_info_score(y, pred)
                except Exception as e:
                    print(f"    [Error] {mname} on {dname} seed {seed}: {e}")
                    score_ari = 0.0
                    score_nmi = 0.0
                    elap = time.perf_counter() - t0

                rec = {
                    "dataset": dname, "N": N, "D": D, "K": K,
                    "model": mname, "seed": seed,
                    "ari": score_ari, "nmi": score_nmi,
                    "elapsed_sec": elap
                }
                records.append(rec)
                done_keys.add((dname, mname, seed))

            # Checkpoint after each model completes
            pd.DataFrame(records).to_csv(out_file, index=False)
            print(f"    [OK] {mname} on {dname} complete ({len(records)}/{13*11*10} total records saved).", flush=True)

        # Checkpoint after each dataset
        pd.DataFrame(records).to_csv(out_file, index=False)

    df = pd.DataFrame(records)
    df.to_csv(out_file, index=False)
    print(f"\n  [OK] Saved all {len(df)} records to {out_file}")
    return df


def main():
    print("STARTING PASS E EXPERIMENTAL SUITE")
    hashes = get_config_hashes()
    with open(OUT_DIR / "config_hashes.json", "w", encoding="utf-8") as fp:
        json.dump(hashes, fp, indent=2)
    print(f"Saved config hashes to {OUT_DIR / 'config_hashes.json'}")

    run_stage1_ablation()
    run_stage2_fair_baselines()
    run_stage3_inductive()
    run_stage4_omnibus()
    print("\nALL PASS E EXPERIMENTAL RUNS COMPLETE!")


if __name__ == "__main__":
    main()
