"""
scripts/run_phase3_experiments.py

Implements and executes Phase 3 experiments as specified in results/PLAN.md:
  8a. CoHiRF benchmark on all 13 datasets (30 seeds for 6 D/N>20; 10 seeds for other 7)
  8b. Anchor selection comparison (Random V4, Certified V5, KMeans Anchors, Balanced Anchors)
  8c. Feature gating comparison (BGSS vs CoHiRF Random Subspace Gating)
  8d. Distance concentration under metric variations (Euclidean, Chebyshev, Cosine)
  8e. Large-K anchor scaling (L = max(40, 10K))
  8f. Hyperparameter sensitivity grid (M x L)

All results are written to raw CSVs in results/.
"""

import sys
import os
import time
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from scipy.stats import kurtosis, skew
from icc.datasets.registry import load_dataset
from icc.baselines.cohirf import CoHiRF
from icc.consensus_v2 import InvariantCoreConsensusV2

def compute_bimodality(X: np.ndarray) -> np.ndarray:
    N, D = X.shape
    kurt = kurtosis(X, axis=0, bias=False) if N >= 4 else kurtosis(X, axis=0)
    sk = skew(X, axis=0, bias=False) if N >= 3 else skew(X, axis=0)
    finite_corr = 3.0 * (N - 1)**2 / ((N - 2) * (N - 3)) if N > 3 else 3.0
    denom = np.maximum(kurt + finite_corr, 1e-5)
    return (sk**2 + 1.0) / denom

HIGH_D_DATASETS = ["colon", "srbct", "cns", "leukemia", "prostate", "ovarian"]
OTHER_DATASETS = ["sonar", "madelon", "isolet", "indian_pines", "yale_b", "zheng68k", "newsgroups20"]
ALL_DATASETS = HIGH_D_DATASETS + OTHER_DATASETS

SEEDS_30 = list(range(30))  # 0 to 29 (30 seeds matching Pass F main benchmark)
SEEDS_10 = list(range(10))  # 0 to 9 (10 seeds matching Pass F main benchmark)

def _eval_cohirf_seed(dname, s, X, y, K):
    t0 = time.perf_counter()
    model = CoHiRF(n_clusters=K, repetitions=25, n_features_subspace=0.15, consensus_threshold=0.80, random_state=s)
    pred = model.fit_predict(X)
    elapsed = time.perf_counter() - t0
    ari = float(adjusted_rand_score(y, pred))
    nmi = float(normalized_mutual_info_score(y, pred))
    print(f"    {dname} Seed {s}: ARI = {ari:.4f}, NMI = {nmi:.4f}, Time = {elapsed:.2f}s", flush=True)
    return {
        "dataset": dname,
        "model": "CoHiRF",
        "seed": s,
        "ari": ari,
        "nmi": nmi,
        "runtime_sec": elapsed,
        "N": X.shape[0],
        "D": X.shape[1],
        "K": K
    }

def run_exp8a_cohirf():
    print("=" * 60)
    print("Executing Exp 8a: CoHiRF Benchmark on 13 Datasets")
    print("=" * 60)
    out_csv = ROOT / "results" / "exp3_cohirf_benchmark.csv"
    
    existing_keys = set()
    records = []
    if out_csv.exists():
        try:
            df_prev = pd.read_csv(out_csv)
            records = df_prev.to_dict("records")
            existing_keys = {(r["dataset"], int(r["seed"])) for r in records}
            print(f"Loaded {len(records)} existing CoHiRF runs from {out_csv}.")
        except Exception:
            pass

    for dname in ALL_DATASETS:
        seeds = SEEDS_30 if dname in HIGH_D_DATASETS else SEEDS_10
        needed_seeds = [s for s in seeds if (dname, s) not in existing_keys]
        if not needed_seeds:
            print(f"Skipping {dname} (all {len(seeds)} seeds already completed).", flush=True)
            continue

        print(f"Loading {dname}...", flush=True)
        X, y, meta = load_dataset(dname)
        K = int(meta["K"]) if isinstance(meta, dict) else int(meta.K)
        print(f"  {dname}: N={X.shape[0]}, D={X.shape[1]}, K={K}, Seeds={len(needed_seeds)} needed", flush=True)

        if dname == "newsgroups20" and len(needed_seeds) > 1:
            from joblib import Parallel, delayed
            results = Parallel(n_jobs=3, backend="loky")(
                delayed(_eval_cohirf_seed)(dname, s, X, y, K) for s in needed_seeds
            )
            for rec in results:
                records.append(rec)
            pd.DataFrame(records).to_csv(out_csv, index=False)
        else:
            for s in needed_seeds:
                rec = _eval_cohirf_seed(dname, s, X, y, K)
                records.append(rec)
                pd.DataFrame(records).to_csv(out_csv, index=False)

    df = pd.DataFrame(records)
    df.to_csv(out_csv, index=False)
    print(f"Exp 8a complete. Saved {len(df)} runs to {out_csv}.", flush=True)
    return df

def run_exp8b_anchor_selection():
    print("=" * 60)
    print("Executing Exp 8b: Anchor Selection Test on 6 High-D Cohorts")
    print("=" * 60)
    out_csv = ROOT / "results" / "exp8b_anchor_selection.csv"
    records = []

    for dname in HIGH_D_DATASETS:
        print(f"Loading {dname}...")
        X, y, meta = load_dataset(dname)
        K = int(meta["K"]) if isinstance(meta, dict) else int(meta.K)

        for s in SEEDS_30:
            # 1. Variant V5: Certified core anchors (default ICC-v2)
            icc_v5 = InvariantCoreConsensusV2(n_clusters=K, n_base_models=25, n_anchors=40, pool_frac=0.15, core_quantile=0.5, random_seed=s)
            pred_v5 = icc_v5.fit_predict(X)
            ari_v5 = float(adjusted_rand_score(y, pred_v5))

            # 2. Variant V4: Random anchors from full dataset (core_quantile=0.0)
            icc_v4 = InvariantCoreConsensusV2(n_clusters=K, n_base_models=25, n_anchors=40, pool_frac=0.15, core_quantile=0.0, random_seed=s)
            pred_v4 = icc_v4.fit_predict(X)
            ari_v4 = float(adjusted_rand_score(y, pred_v4))

            # 3. Variant V_kmeans: KMeans centroids as anchors
            # Feature gating top 15% features
            D = X.shape[1]
            pool_size = max(2, int(np.floor(0.15 * D)))
            bcs = compute_bimodality(X)
            active_feats = np.argsort(bcs)[-pool_size:]
            X_active = X[:, active_feats]

            # Base ensemble partitions
            rng = np.random.RandomState(s)
            M = 25
            sub_dim = max(1, int(np.floor(0.50 * pool_size)))
            P_stack = np.empty((M, X.shape[0]), dtype=np.int32)
            for m in range(M):
                sub_f = rng.choice(pool_size, size=sub_dim, replace=False)
                km = KMeans(n_clusters=K, n_init=1, random_state=rng.randint(0, 1000000))
                P_stack[m] = km.fit_predict(X_active[:, sub_f])

            # Run KMeans with k=40 on X_active to identify 40 prototype centroids as anchors
            L = min(40, X.shape[0])
            km_anchors = KMeans(n_clusters=L, n_init=1, random_state=s)
            km_anchors.fit(X_active)
            # Find nearest instance to each centroid
            centroids = km_anchors.cluster_centers_
            dists = cdist(centroids, X_active)
            anchor_indices_km = np.argmin(dists, axis=1)

            # Build bipartite co-association B against KMeans anchors
            B_km = np.zeros((X.shape[0], L), dtype=np.float64)
            for m in range(M):
                P_anchors = P_stack[m, anchor_indices_km]
                B_km += (P_stack[m, :, None] == P_anchors[None, :])
            B_km /= float(M)

            # Solve Transfer-Cut / Bipartite Spectral Embedding
            row_sum = np.sum(B_km, axis=1, keepdims=True)
            row_sum[row_sum == 0] = 1.0
            B_norm = B_km / row_sum
            W_anchor = B_norm.T @ B_norm
            d_A = np.sum(W_anchor, axis=1)
            d_A[d_A == 0] = 1.0
            D_A_inv_sqrt = np.diag(1.0 / np.sqrt(d_A))
            L_A = np.eye(L) - D_A_inv_sqrt @ W_anchor @ D_A_inv_sqrt
            evals, evecs = np.linalg.eigh(L_A)
            idx_sorted = np.argsort(evals)
            V = evecs[:, idx_sorted[:K]]
            U = B_norm @ V
            final_km = KMeans(n_clusters=K, n_init=5, random_state=s)
            pred_kmeans_anchors = final_km.fit_predict(U)
            ari_kmeans_anchors = float(adjusted_rand_score(y, pred_kmeans_anchors))

            # 4. Variant V_balanced: Stratified / balanced quantile anchors across determinacy
            # Compute point determinacy
            # S^2 average
            P_match = (P_stack[:, :, None] == P_stack[:, None, :]).astype(np.float32)
            S_full = np.mean(P_match, axis=0)
            det = np.mean(S_full ** 2, axis=1)
            # Stratify into L quantiles and pick 1 per quantile
            sorted_idx = np.argsort(det)
            bins = np.array_split(sorted_idx, L)
            anchor_indices_balanced = np.array([b[len(b) // 2] for b in bins])

            B_bal = np.zeros((X.shape[0], L), dtype=np.float64)
            for m in range(M):
                P_anchors = P_stack[m, anchor_indices_balanced]
                B_bal += (P_stack[m, :, None] == P_anchors[None, :])
            B_bal /= float(M)
            row_sum = np.sum(B_bal, axis=1, keepdims=True)
            row_sum[row_sum == 0] = 1.0
            B_norm = B_bal / row_sum
            W_anchor = B_norm.T @ B_norm
            d_A = np.sum(W_anchor, axis=1)
            d_A[d_A == 0] = 1.0
            D_A_inv_sqrt = np.diag(1.0 / np.sqrt(d_A))
            L_A = np.eye(L) - D_A_inv_sqrt @ W_anchor @ D_A_inv_sqrt
            evals, evecs = np.linalg.eigh(L_A)
            idx_sorted = np.argsort(evals)
            V = evecs[:, idx_sorted[:K]]
            U = B_norm @ V
            final_km = KMeans(n_clusters=K, n_init=5, random_state=s)
            pred_balanced_anchors = final_km.fit_predict(U)
            ari_balanced_anchors = float(adjusted_rand_score(y, pred_balanced_anchors))

            records.append({
                "dataset": dname,
                "seed": s,
                "ari_v5_certified": ari_v5,
                "ari_v4_random": ari_v4,
                "ari_kmeans_anchors": ari_kmeans_anchors,
                "ari_balanced_anchors": ari_balanced_anchors,
                "diff_v5_v4": ari_v5 - ari_v4,
                "diff_v5_kmeans": ari_v5 - ari_kmeans_anchors,
                "diff_v5_balanced": ari_v5 - ari_balanced_anchors
            })
            print(f"  {dname} Seed {s}: V5={ari_v5:.4f}, V4={ari_v4:.4f}, KMeansA={ari_kmeans_anchors:.4f}, BalA={ari_balanced_anchors:.4f}")

    df = pd.DataFrame(records)
    df.to_csv(out_csv, index=False)
    print(f"Exp 8b complete. Saved to {out_csv}.")
    return df

def run_exp8c_feature_gating():
    print("=" * 60)
    print("Executing Exp 8c: Feature Gating (BGSS vs CoHiRF Random Subspace Gating)")
    print("=" * 60)
    out_csv = ROOT / "results" / "exp8c_feature_gating.csv"
    records = []

    for dname in HIGH_D_DATASETS:
        print(f"Loading {dname}...")
        X, y, meta = load_dataset(dname)
        K = int(meta["K"]) if isinstance(meta, dict) else int(meta.K)
        D = X.shape[1]
        pool_size = max(2, int(np.floor(0.15 * D)))

        for s in SEEDS_30:
            # 1. BGSS feature gating (V5)
            icc_bgss = InvariantCoreConsensusV2(n_clusters=K, n_base_models=25, n_anchors=40, pool_frac=0.15, core_quantile=0.5, random_seed=s)
            pred_bgss = icc_bgss.fit_predict(X)
            ari_bgss = float(adjusted_rand_score(y, pred_bgss))

            # 2. Random feature gating (same pool_size)
            rng = np.random.RandomState(s)
            rand_feats = rng.choice(D, size=pool_size, replace=False)
            X_rand = X[:, rand_feats]

            # Fit ICC-v2 on X_rand without further feature filtering (pool_frac=1.0)
            icc_rand = InvariantCoreConsensusV2(n_clusters=K, n_base_models=25, n_anchors=40, pool_frac=1.0, core_quantile=0.5, random_seed=s)
            pred_rand = icc_rand.fit_predict(X_rand)
            ari_rand = float(adjusted_rand_score(y, pred_rand))

            records.append({
                "dataset": dname,
                "seed": s,
                "ari_bgss": ari_bgss,
                "ari_random_gating": ari_rand,
                "diff_bgss_minus_random": ari_bgss - ari_rand
            })
            print(f"  {dname} Seed {s}: BGSS={ari_bgss:.4f}, RandomGating={ari_rand:.4f}, Diff={ari_bgss - ari_rand:+.4f}")

    df = pd.DataFrame(records)
    df.to_csv(out_csv, index=False)
    print(f"Exp 8c complete. Saved to {out_csv}.")
    return df

def run_exp8d_distance_metrics():
    print("=" * 60)
    print("Executing Exp 8d: Distance Concentration Simulation (Euclidean, Chebyshev, Cosine)")
    print("=" * 60)
    out_csv = ROOT / "results" / "exp8d_distance_metrics.csv"
    from sklearn.cluster import AgglomerativeClustering, SpectralClustering

    N = 200
    K = 2
    d_noises = [0, 50, 100, 200, 500, 1000, 2000]
    metrics = ["euclidean", "chebyshev", "cosine"]
    seeds = [42, 101, 202, 303, 404]

    records = []
    for d_noise in d_noises:
        for metric in metrics:
            aris_km = []
            aris_agg = []
            aris_spec = []
            for s in seeds:
                rng = np.random.RandomState(s)
                # 2 informative signal dimensions with separation
                X_signal = np.vstack([
                    rng.normal(loc=[-2.0, 0.0], scale=1.0, size=(N // 2, 2)),
                    rng.normal(loc=[+2.0, 0.0], scale=1.0, size=(N // 2, 2))
                ])
                y_true = np.array([0] * (N // 2) + [1] * (N // 2))

                if d_noise > 0:
                    X_noise = rng.normal(loc=0.0, scale=1.0, size=(N, d_noise))
                    X_full = np.hstack([X_signal, X_noise])
                else:
                    X_full = X_signal

                # 1. K-Means (Euclidean coordinate mapping)
                km = KMeans(n_clusters=K, n_init=5, random_state=s)
                p_km = km.fit_predict(X_full)
                aris_km.append(adjusted_rand_score(y_true, p_km))

                # 2. Agglomerative (with specific metric)
                if metric == "cosine":
                    # Normalize for cosine or compute distance
                    D_mat = cdist(X_full, X_full, metric="cosine")
                    agg = AgglomerativeClustering(n_clusters=K, metric="precomputed", linkage="average")
                    p_agg = agg.fit_predict(D_mat)
                elif metric == "chebyshev":
                    D_mat = cdist(X_full, X_full, metric="chebyshev")
                    agg = AgglomerativeClustering(n_clusters=K, metric="precomputed", linkage="complete")
                    p_agg = agg.fit_predict(D_mat)
                else:
                    agg = AgglomerativeClustering(n_clusters=K, metric="euclidean", linkage="ward")
                    p_agg = agg.fit_predict(X_full)
                aris_agg.append(adjusted_rand_score(y_true, p_agg))

                # 3. Spectral (affinity from metric)
                D_mat = cdist(X_full, X_full, metric=metric)
                gamma = 1.0 / np.median(D_mat) if np.median(D_mat) > 0 else 1.0
                aff = np.exp(-gamma * (D_mat ** 2))
                spec = SpectralClustering(n_clusters=K, affinity="precomputed", random_state=s)
                p_spec = spec.fit_predict(aff)
                aris_spec.append(adjusted_rand_score(y_true, p_spec))

            mean_km = float(np.mean(aris_km))
            mean_agg = float(np.mean(aris_agg))
            mean_spec = float(np.mean(aris_spec))
            records.append({
                "D_noise": d_noise,
                "metric": metric,
                "ari_kmeans": mean_km,
                "ari_agglomerative": mean_agg,
                "ari_spectral": mean_spec
            })
            print(f"  D_noise={d_noise:4d}, Metric={metric:10s} -> KM={mean_km:.4f}, Agg={mean_agg:.4f}, Spec={mean_spec:.4f}")

    df = pd.DataFrame(records)
    df.to_csv(out_csv, index=False)
    print(f"Exp 8d complete. Saved to {out_csv}.")
    return df

def run_exp8e_large_k_anchor_budget():
    print("=" * 60)
    print("Executing Exp 8e: Large-K Anchor Budget Scaling (L = max(40, 10K))")
    print("=" * 60)
    out_csv = ROOT / "results" / "exp8e_large_k_anchor_budget.csv"
    large_k_datasets = ["isolet", "newsgroups20", "indian_pines", "yale_b"]
    records = []

    for dname in large_k_datasets:
        print(f"Loading {dname}...")
        X, y, meta = load_dataset(dname)
        K = int(meta["K"]) if isinstance(meta, dict) else int(meta.K)
        L_scaled = max(40, 10 * K)
        print(f"  {dname}: N={X.shape[0]}, D={X.shape[1]}, K={K} -> Scaled L={L_scaled} (Default L=40)")

        for s in SEEDS_10:
            # Run with default L=40
            icc_def = InvariantCoreConsensusV2(n_clusters=K, n_base_models=25, n_anchors=40, pool_frac=0.15, core_quantile=0.5, random_seed=s)
            pred_def = icc_def.fit_predict(X)
            ari_def = float(adjusted_rand_score(y, pred_def))

            # Run with scaled L = 10*K
            icc_scaled = InvariantCoreConsensusV2(n_clusters=K, n_base_models=25, n_anchors=L_scaled, pool_frac=0.15, core_quantile=0.5, random_seed=s)
            pred_scaled = icc_scaled.fit_predict(X)
            ari_scaled = float(adjusted_rand_score(y, pred_scaled))

            records.append({
                "dataset": dname,
                "seed": s,
                "K": K,
                "L_default": 40,
                "L_scaled": L_scaled,
                "ari_default": ari_def,
                "ari_scaled": ari_scaled,
                "diff_scaled_minus_default": ari_scaled - ari_def
            })
            print(f"  {dname} Seed {s}: L=40 -> ARI={ari_def:.4f}; L={L_scaled} -> ARI={ari_scaled:.4f}; Diff={ari_scaled - ari_def:+.4f}")

    df = pd.DataFrame(records)
    df.to_csv(out_csv, index=False)
    print(f"Exp 8e complete. Saved to {out_csv}.")
    return df

def run_exp8f_sensitivity_grid():
    print("=" * 60)
    print("Executing Exp 8f: Sensitivity Grid (M in {5,10,15,25,50} x L in {20,40,60,80})")
    print("=" * 60)
    out_csv = ROOT / "results" / "exp8f_sensitivity_grid.csv"
    M_values = [5, 10, 15, 25, 50]
    L_values = [20, 40, 60, 80]
    records = []

    for dname in HIGH_D_DATASETS:
        print(f"Loading {dname}...")
        X, y, meta = load_dataset(dname)
        K = int(meta["K"]) if isinstance(meta, dict) else int(meta.K)

        for M in M_values:
            for L in L_values:
                aris = []
                for s in SEEDS_10:
                    icc = InvariantCoreConsensusV2(n_clusters=K, n_base_models=M, n_anchors=L, pool_frac=0.15, core_quantile=0.5, random_seed=s)
                    pred = icc.fit_predict(X)
                    aris.append(adjusted_rand_score(y, pred))
                mean_ari = float(np.mean(aris))
                std_ari = float(np.std(aris))
                records.append({
                    "dataset": dname,
                    "M": M,
                    "L": L,
                    "mean_ari": mean_ari,
                    "std_ari": std_ari
                })
                print(f"  {dname} M={M:2d}, L={L:2d} -> ARI = {mean_ari:.4f} +/- {std_ari:.4f}")

    df = pd.DataFrame(records)
    df.to_csv(out_csv, index=False)
    print(f"Exp 8f complete. Saved to {out_csv}.")
    return df

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--exp8a", action="store_true")
    parser.add_argument("--exp8b", action="store_true")
    parser.add_argument("--exp8c", action="store_true")
    parser.add_argument("--exp8d", action="store_true")
    parser.add_argument("--exp8e", action="store_true")
    parser.add_argument("--exp8f", action="store_true")
    args = parser.parse_args()

    if args.all or not any([args.exp8a, args.exp8b, args.exp8c, args.exp8d, args.exp8e, args.exp8f]):
        run_exp8a_cohirf()
        run_exp8b_anchor_selection()
        run_exp8c_feature_gating()
        run_exp8d_distance_metrics()
        run_exp8e_large_k_anchor_budget()
        run_exp8f_sensitivity_grid()
    else:
        if args.exp8a: run_exp8a_cohirf()
        if args.exp8b: run_exp8b_anchor_selection()
        if args.exp8c: run_exp8c_feature_gating()
        if args.exp8d: run_exp8d_distance_metrics()
        if args.exp8e: run_exp8e_large_k_anchor_budget()
        if args.exp8f: run_exp8f_sensitivity_grid()
