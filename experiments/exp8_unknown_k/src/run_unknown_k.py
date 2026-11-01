"""
Execution runner for EXP8: Genuinely Unsupervised Model Order Selection Benchmark.
Evaluates ICC-AutoK, GMM-BIC, GMM-ICL, Spectral Eigengap, and HDBSCAN* under distractor noise.
"""

import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, List

import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from sklearn.mixture import GaussianMixture
from sklearn.cluster import SpectralClustering

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from icc.autok import run_icc_autok
from icc.datasets.registry import load_dataset


def generate_synthetic_clusters(
    n_samples: int = 200,
    k: int = 3,
    d_signal: int = 20,
    d_noise: int = 100,
    balanced: bool = True,
    seed: int = 42,
) -> Tuple[np.ndarray, np.ndarray]:
    """Generate synthetic Gaussian clusters submerged in distractor dimensions."""
    rng = np.random.default_rng(seed)

    if balanced:
        sizes = [n_samples // k] * k
        sizes[0] += n_samples - sum(sizes)
    else:
        probs = rng.dirichlet(np.ones(k) * 0.5)
        sizes = rng.multinomial(n_samples, probs)
        sizes = np.fmax(sizes, 5)

    X_list = []
    y_list = []

    for c_idx, count in enumerate(sizes):
        center = rng.normal(loc=0.0, scale=3.0, size=d_signal)
        cluster_pts = rng.normal(loc=center, scale=1.0, size=(count, d_signal))
        X_list.append(cluster_pts)
        y_list.append(np.full(count, c_idx, dtype=int))

    X_signal = np.vstack(X_list)
    y = np.concatenate(y_list)

    if d_noise > 0:
        X_noise = rng.normal(loc=0.0, scale=1.0, size=(n_samples, d_noise))
        X = np.hstack([X_signal, X_noise])
    else:
        X = X_signal

    # Shuffle instances
    perm = rng.permutation(n_samples)
    return X[perm], y[perm]


def estimate_k_gmm(X: np.ndarray, k_min: int = 2, k_max: int = 8, criterion: str = "bic", seed: int = 42) -> Tuple[int, np.ndarray]:
    """Estimate K using Gaussian Mixture Model with BIC or ICL."""
    best_score = float("inf")
    best_k = k_min
    best_labels = np.zeros(len(X), dtype=int)

    for k in range(k_min, min(k_max + 1, len(X))):
        try:
            gmm = GaussianMixture(n_components=k, covariance_type="diag", random_state=seed, max_iter=100)
            gmm.fit(X)
            probs = gmm.predict_proba(X)
            bic = gmm.bic(X)

            if criterion == "icl":
                ent = -np.sum(probs * np.log(np.fmax(probs, 1e-12)))
                score = bic + 2.0 * ent
            else:
                score = bic

            if score < best_score:
                best_score = score
                best_k = k
                best_labels = gmm.predict(X)
        except Exception:
            continue

    return best_k, best_labels


def estimate_k_spectral_eigengap(X: np.ndarray, k_min: int = 2, k_max: int = 8, seed: int = 42) -> Tuple[int, np.ndarray]:
    """Estimate K via normalized Laplacian eigengap heuristic."""
    from scipy.spatial.distance import cdist

    dists = cdist(X, X, metric="sqeuclidean")
    gamma = 1.0 / (np.median(dists) + 1e-6)
    W = np.exp(-gamma * dists)
    D = np.diag(np.sum(W, axis=1))
    D_inv_sqrt = np.diag(1.0 / np.sqrt(np.fmax(np.diag(D), 1e-12)))
    L_norm = np.eye(len(X)) - D_inv_sqrt @ W @ D_inv_sqrt

    evals = np.linalg.eigvalsh(L_norm)
    evals = np.sort(evals)

    # Find maximum eigengap in [k_min, k_max]
    gaps = []
    candidates = list(range(k_min, min(k_max + 1, len(evals) - 1)))
    for k in candidates:
        gaps.append(evals[k] - evals[k - 1])

    best_k = candidates[int(np.argmax(gaps))]
    sc = SpectralClustering(n_clusters=best_k, affinity="nearest_neighbors", n_neighbors=10, random_state=seed)
    labels = sc.fit_predict(X)
    return best_k, labels


def estimate_k_hdbscan(X: np.ndarray, min_cluster_size: int = 5) -> Tuple[int, np.ndarray]:
    """Estimate K via HDBSCAN density hierarchy."""
    try:
        from sklearn.cluster import HDBSCAN

        hdb = HDBSCAN(min_cluster_size=min_cluster_size)
        labels = hdb.fit_predict(X)
        unique_clusters = set(labels) - {-1}
        k_est = max(1, len(unique_clusters))
        return k_est, labels
    except Exception:
        return 1, np.zeros(len(X), dtype=int)


def run_synthetic_benchmark(out_csv: Path, n_reps: int = 3):
    """Run synthetic model order discovery sweep across distractor scales."""
    records: List[Dict[str, Any]] = []
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    print("Running Synthetic Unknown-K Benchmark...")
    ks = [2, 3, 4, 5, 8]
    d_noises = [0, 100, 1000]

    for k_true in ks:
        for d_noise in d_noises:
            for rep in range(n_reps):
                seed = 42 + rep * 10
                X, y_true = generate_synthetic_clusters(
                    n_samples=180,
                    k=k_true,
                    d_signal=20,
                    d_noise=d_noise,
                    balanced=True,
                    seed=seed,
                )

                # 1. ICC-AutoK
                t0 = time.perf_counter()
                res = run_icc_autok(X, k_min=2, k_max=8, seed=seed)
                t_icc = time.perf_counter() - t0

                records.append({
                    "stratum": "synthetic",
                    "model": "ICC-AutoK-PAC",
                    "true_k": k_true,
                    "pred_k": res.best_k_pac,
                    "abs_k_error": abs(res.best_k_pac - k_true),
                    "exact_k_match": int(res.best_k_pac == k_true),
                    "ari_at_pred_k": float(adjusted_rand_score(y_true, res.best_labels_pac)),
                    "nmi_at_pred_k": float(normalized_mutual_info_score(y_true, res.best_labels_pac)),
                    "d_noise": d_noise,
                    "runtime_sec": t_icc,
                    "seed": seed,
                })

                records.append({
                    "stratum": "synthetic",
                    "model": "ICC-AutoK-Silhouette",
                    "true_k": k_true,
                    "pred_k": res.best_k_silhouette,
                    "abs_k_error": abs(res.best_k_silhouette - k_true),
                    "exact_k_match": int(res.best_k_silhouette == k_true),
                    "ari_at_pred_k": float(adjusted_rand_score(y_true, res.best_labels_silhouette)),
                    "nmi_at_pred_k": float(normalized_mutual_info_score(y_true, res.best_labels_silhouette)),
                    "d_noise": d_noise,
                    "runtime_sec": t_icc,
                    "seed": seed,
                })

                # 2. GMM-BIC
                t0 = time.perf_counter()
                k_bic, y_bic = estimate_k_gmm(X, k_min=2, k_max=8, criterion="bic", seed=seed)
                t_bic = time.perf_counter() - t0
                records.append({
                    "stratum": "synthetic",
                    "model": "GMM-BIC",
                    "true_k": k_true,
                    "pred_k": k_bic,
                    "abs_k_error": abs(k_bic - k_true),
                    "exact_k_match": int(k_bic == k_true),
                    "ari_at_pred_k": float(adjusted_rand_score(y_true, y_bic)),
                    "nmi_at_pred_k": float(normalized_mutual_info_score(y_true, y_bic)),
                    "d_noise": d_noise,
                    "runtime_sec": t_bic,
                    "seed": seed,
                })

                # 3. GMM-ICL
                t0 = time.perf_counter()
                k_icl, y_icl = estimate_k_gmm(X, k_min=2, k_max=8, criterion="icl", seed=seed)
                t_icl = time.perf_counter() - t0
                records.append({
                    "stratum": "synthetic",
                    "model": "GMM-ICL",
                    "true_k": k_true,
                    "pred_k": k_icl,
                    "abs_k_error": abs(k_icl - k_true),
                    "exact_k_match": int(k_icl == k_true),
                    "ari_at_pred_k": float(adjusted_rand_score(y_true, y_icl)),
                    "nmi_at_pred_k": float(normalized_mutual_info_score(y_true, y_icl)),
                    "d_noise": d_noise,
                    "runtime_sec": t_icl,
                    "seed": seed,
                })

                # 4. Spectral Eigengap
                t0 = time.perf_counter()
                k_eigen, y_eigen = estimate_k_spectral_eigengap(X, k_min=2, k_max=8, seed=seed)
                t_eigen = time.perf_counter() - t0
                records.append({
                    "stratum": "synthetic",
                    "model": "Spectral-Eigengap",
                    "true_k": k_true,
                    "pred_k": k_eigen,
                    "abs_k_error": abs(k_eigen - k_true),
                    "exact_k_match": int(k_eigen == k_true),
                    "ari_at_pred_k": float(adjusted_rand_score(y_true, y_eigen)),
                    "nmi_at_pred_k": float(normalized_mutual_info_score(y_true, y_eigen)),
                    "d_noise": d_noise,
                    "runtime_sec": t_eigen,
                    "seed": seed,
                })

                # 5. HDBSCAN
                t0 = time.perf_counter()
                k_hdb, y_hdb = estimate_k_hdbscan(X)
                t_hdb = time.perf_counter() - t0
                records.append({
                    "stratum": "synthetic",
                    "model": "HDBSCAN*",
                    "true_k": k_true,
                    "pred_k": k_hdb,
                    "abs_k_error": abs(k_hdb - k_true),
                    "exact_k_match": int(k_hdb == k_true),
                    "ari_at_pred_k": float(adjusted_rand_score(y_true, y_hdb)),
                    "nmi_at_pred_k": float(normalized_mutual_info_score(y_true, y_hdb)),
                    "d_noise": d_noise,
                    "runtime_sec": t_hdb,
                    "seed": seed,
                })

    df = pd.DataFrame(records)
    df.to_csv(out_csv, index=False)
    print(f"Saved synthetic results to {out_csv} ({len(df)} evaluations)")
    return df


def run_real_cohort_unknown_k(out_csv: Path):
    """Run unknown-K evaluation on real high-dimensional biomedical cohorts."""
    records: List[Dict[str, Any]] = []
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    cohorts = ["colon", "srbct", "cns", "leukemia", "prostate", "ovarian"]
    print("Running Real Cohort Unknown-K Benchmark...")

    for name in cohorts:
        X, y_true, meta = load_dataset(name)
        k_true = len(set(y_true))
        k_max = min(8, len(X) // 5)

        # 1. ICC-AutoK
        t0 = time.perf_counter()
        res = run_icc_autok(X, k_min=2, k_max=k_max, seed=42)
        t_icc = time.perf_counter() - t0

        records.append({
            "cohort": name,
            "N": len(X),
            "D": X.shape[1],
            "true_k": k_true,
            "model": "ICC-AutoK-PAC",
            "pred_k": res.best_k_pac,
            "abs_k_error": abs(res.best_k_pac - k_true),
            "ari_at_pred_k": float(adjusted_rand_score(y_true, res.best_labels_pac)),
            "nmi_at_pred_k": float(normalized_mutual_info_score(y_true, res.best_labels_pac)),
            "runtime_sec": t_icc,
        })

        records.append({
            "cohort": name,
            "N": len(X),
            "D": X.shape[1],
            "true_k": k_true,
            "model": "ICC-AutoK-Silhouette",
            "pred_k": res.best_k_silhouette,
            "abs_k_error": abs(res.best_k_silhouette - k_true),
            "ari_at_pred_k": float(adjusted_rand_score(y_true, res.best_labels_silhouette)),
            "nmi_at_pred_k": float(normalized_mutual_info_score(y_true, res.best_labels_silhouette)),
            "runtime_sec": t_icc,
        })

        # 2. GMM-BIC
        t0 = time.perf_counter()
        k_bic, y_bic = estimate_k_gmm(X, k_min=2, k_max=k_max, criterion="bic", seed=42)
        t_bic = time.perf_counter() - t0
        records.append({
            "cohort": name,
            "N": len(X),
            "D": X.shape[1],
            "true_k": k_true,
            "model": "GMM-BIC",
            "pred_k": k_bic,
            "abs_k_error": abs(k_bic - k_true),
            "ari_at_pred_k": float(adjusted_rand_score(y_true, y_bic)),
            "nmi_at_pred_k": float(normalized_mutual_info_score(y_true, y_bic)),
            "runtime_sec": t_bic,
        })

        # 3. Spectral Eigengap
        t0 = time.perf_counter()
        k_eigen, y_eigen = estimate_k_spectral_eigengap(X, k_min=2, k_max=k_max, seed=42)
        t_eigen = time.perf_counter() - t0
        records.append({
            "cohort": name,
            "N": len(X),
            "D": X.shape[1],
            "true_k": k_true,
            "model": "Spectral-Eigengap",
            "pred_k": k_eigen,
            "abs_k_error": abs(k_eigen - k_true),
            "ari_at_pred_k": float(adjusted_rand_score(y_true, y_eigen)),
            "nmi_at_pred_k": float(normalized_mutual_info_score(y_true, y_eigen)),
            "runtime_sec": t_eigen,
        })

    df = pd.DataFrame(records)
    df.to_csv(out_csv, index=False)
    print(f"Saved real cohort results to {out_csv}")
    return df


if __name__ == "__main__":
    syn_csv = _ROOT / "experiments" / "exp8_unknown_k" / "data" / "unknown_k_synthetic_results.csv"
    real_csv = _ROOT / "experiments" / "exp8_unknown_k" / "data" / "unknown_k_real_results.csv"

    run_synthetic_benchmark(syn_csv, n_reps=2)
    run_real_cohort_unknown_k(real_csv)
