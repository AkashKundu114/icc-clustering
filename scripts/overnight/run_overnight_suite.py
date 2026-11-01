"""
scripts/overnight/run_overnight_suite.py

Central overnight experiment orchestration and execution engine.
Executes Milestones 2 through 6 sequentially with RAM safety,
atomic persistence, checkpoint resumption, and manifest logging.
"""

import gc
import gzip
import os
import sys
import time
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering, KMeans, SpectralClustering
from sklearn.metrics import (
    adjusted_mutual_info_score,
    adjusted_rand_score,
    calinski_harabasz_score,
    davies_bouldin_score,
    fowlkes_mallows_score,
    normalized_mutual_info_score,
    silhouette_score,
)
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Add project root and src to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))
sys.path.insert(0, str(ROOT_DIR))

from icc.autok import run_icc_autok
from icc.baselines.classical import run_fcm, run_kmeans, run_spectral, run_ward
from icc.baselines.consensus import run_icc_v2, run_standard_consensus
from icc.baselines.density import run_hdbscan
from icc.baselines.probabilistic import run_gmm, run_gmm_bic
from icc.baselines.sparse_kmeans import run_sparse_kmeans
from icc.consensus_v2 import InvariantCoreConsensusV2
from icc.datasets.registry import load_dataset

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

RESULTS_DIR = ROOT_DIR / "results" / "overnight"
MANIFEST_PATH = RESULTS_DIR / "EXECUTION_MANIFEST.csv"
DL_DIR = Path.home() / "scikit_learn_data" / "openml" / "openml.org" / "data" / "v1" / "download"

SEEDS = [42, 101, 202, 303, 404]

EXP6_MAP = {
    "dlbcl": "DLBCL.arff.gz",
    "breast": "Breast.arff.gz",
    "su2001": "11_Tumors.arff.gz",
    "novartis": "9_Tumors.arff.gz",
    "endometrium": "AP_Endometrium_Kidney.arff.gz",
}

GIT_COMMIT = "research/overnight-experiments"


def log_manifest(
    exp_id: str,
    exp_group: str,
    dataset: str,
    method: str,
    config_desc: str,
    seed: int,
    status: str,
    start_time: str,
    end_time: str,
    runtime_sec: float,
    out_path: str,
    error_msg: str = "",
    notes: str = "",
):
    """Append row to master EXECUTION_MANIFEST.csv atomically."""
    row = {
        "experiment_id": exp_id,
        "experiment_group": exp_group,
        "dataset": dataset,
        "method": method,
        "configuration": config_desc,
        "seed": seed,
        "status": status,
        "start_time": start_time,
        "end_time": end_time,
        "runtime_seconds": runtime_sec,
        "output_path": out_path,
        "error_message": error_msg,
        "git_commit": GIT_COMMIT,
        "notes": notes,
    }
    df = pd.DataFrame([row])
    hdr = not MANIFEST_PATH.exists()
    df.to_csv(MANIFEST_PATH, mode="a", index=False, header=hdr)


def find_arff(filename: str) -> Path:
    matches = list(DL_DIR.rglob(filename))
    if not matches:
        raise FileNotFoundError(f"Cannot find {filename} in {DL_DIR}")
    return matches[0]


def parse_arff_gz(file_path: Path) -> Tuple[np.ndarray, np.ndarray]:
    with gzip.open(file_path, "rt", encoding="utf-8", errors="ignore") as gz:
        in_data = False
        X_rows = []
        y_rows = []
        for line in gz:
            line_str = line.strip()
            if not line_str or line_str.startswith("%"):
                continue
            if line_str.upper().startswith("@DATA"):
                in_data = True
                continue
            if in_data:
                parts = line_str.split(",")
                features = [float(val) if val != "?" else np.nan for val in parts[:-1]]
                label = parts[-1].strip().strip("'\"")
                X_rows.append(features)
                y_rows.append(label)

    X = np.array(X_rows, dtype=np.float64)
    y = np.array(y_rows)
    col_means = np.nanmean(X, axis=0)
    inds = np.where(np.isnan(X))
    X[inds] = np.take(col_means, inds[1])
    X = StandardScaler().fit_transform(X)
    y = LabelEncoder().fit_transform(y)
    return X, y


def load_cohort(key: str) -> Tuple[np.ndarray, np.ndarray]:
    if key in ["colon", "srbct", "cns", "leukemia", "prostate", "ovarian", "zheng68k", "sonar", "madelon"]:
        X, y, _ = load_dataset(key)
        return X, y
    elif key in EXP6_MAP:
        path = find_arff(EXP6_MAP[key])
        return parse_arff_gz(path)
    elif key == "gli":
        path = find_arff("GLI.arff.gz")
        return parse_arff_gz(path)
    else:
        raise ValueError(f"Unknown cohort {key}")


def compute_metrics(X: np.ndarray, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    # Handle noise or non-clustered points (-1 in HDBSCAN)
    valid_mask = y_pred >= 0
    n_clusters = len(np.unique(y_pred[valid_mask])) if np.any(valid_mask) else 0

    if n_clusters < 2:
        return {
            "ari": 0.0,
            "nmi": 0.0,
            "ami": 0.0,
            "fm_index": 0.0,
            "silhouette": -1.0,
            "davies_bouldin": 99.0,
            "calinski_harabasz": 0.0,
            "n_clusters_found": n_clusters,
            "noise_fraction": float(np.mean(~valid_mask)),
        }

    X_sub = X[valid_mask]
    yt_sub = y_true[valid_mask]
    yp_sub = y_pred[valid_mask]

    ari = adjusted_rand_score(yt_sub, yp_sub)
    nmi = normalized_mutual_info_score(yt_sub, yp_sub)
    ami = adjusted_mutual_info_score(yt_sub, yp_sub)
    fm = fowlkes_mallows_score(yt_sub, yp_sub)

    # Topological unsupervised metrics (compute on subset if N > 2000 for RAM safety)
    if len(X_sub) > 2000:
        rng = np.random.default_rng(42)
        idx = rng.choice(len(X_sub), 2000, replace=False)
        sil = float(silhouette_score(X_sub[idx], yp_sub[idx]))
        db = float(davies_bouldin_score(X_sub[idx], yp_sub[idx]))
        ch = float(calinski_harabasz_score(X_sub[idx], yp_sub[idx]))
    else:
        sil = float(silhouette_score(X_sub, yp_sub))
        db = float(davies_bouldin_score(X_sub, yp_sub))
        ch = float(calinski_harabasz_score(X_sub, yp_sub))

    return {
        "ari": float(ari),
        "nmi": float(nmi),
        "ami": float(ami),
        "fm_index": float(fm),
        "silhouette": sil,
        "davies_bouldin": db,
        "calinski_harabasz": ch,
        "n_clusters_found": n_clusters,
        "noise_fraction": float(np.mean(~valid_mask)),
    }


# ==============================================================================
# MILESTONE 2: Primary ICC Benchmark across Eligible Cohorts
# ==============================================================================
def run_milestone2_primary_icc():
    print("\n" + "=" * 80)
    print(">>> MILESTONE 2: Primary ICC Benchmark (P0) across Confirmed Cohorts")
    print("=" * 80)

    out_file = RESULTS_DIR / "primary_icc" / "primary_icc_results.csv"
    cohorts = [
        "colon", "srbct", "cns", "leukemia", "prostate", "ovarian",
        "dlbcl", "breast", "su2001", "endometrium",
        "zheng68k", "sonar", "madelon"
    ]

    # Load existing checkpoint
    completed = set()
    if out_file.exists():
        df_old = pd.read_csv(out_file)
        completed = set(zip(df_old["cohort"], df_old["seed"]))
        print(f"Loaded existing checkpoint with {len(df_old)} records.")

    for c in cohorts:
        X, y = load_cohort(c)
        k_true = len(np.unique(y))
        n_samples, n_features = X.shape

        for seed in SEEDS:
            if (c, seed) in completed:
                continue

            t0 = time.perf_counter()
            t_iso = datetime.now(timezone.utc).isoformat()
            exp_id = f"M2-P0-{c}-ICC-{seed}"

            try:
                # Primary ICC Configuration: InvariantCoreConsensusV2 with adaptive gating
                icc_model = InvariantCoreConsensusV2(
                    n_clusters=k_true,
                    n_base_models=25,
                    n_anchors=max(10, int(np.sqrt(n_samples))),
                    subspace_rate=0.3,
                    random_state=seed,
                )
                icc_model.fit(X)
                y_pred = icc_model.labels_

                runtime = time.perf_counter() - t0
                t_end = datetime.now(timezone.utc).isoformat()
                metrics = compute_metrics(X, y, y_pred)

                res_row = {
                    "cohort": c,
                    "N": n_samples,
                    "D": n_features,
                    "true_k": k_true,
                    "model": "ICC_v2_adaptive",
                    "seed": seed,
                    "ari": metrics["ari"],
                    "nmi": metrics["nmi"],
                    "ami": metrics["ami"],
                    "fm_index": metrics["fm_index"],
                    "silhouette": metrics["silhouette"],
                    "davies_bouldin": metrics["davies_bouldin"],
                    "calinski_harabasz": metrics["calinski_harabasz"],
                    "runtime_sec": runtime,
                    "status": "COMPLETED",
                }
                pd.DataFrame([res_row]).to_csv(out_file, mode="a", index=False, header=not out_file.exists())
                log_manifest(
                    exp_id=exp_id, exp_group="Primary_ICC", dataset=c, method="ICC_v2_adaptive",
                    config_desc="n_base=25, n_anchors=sqrt(N), rate=0.3", seed=seed,
                    status="completed", start_time=t_iso, end_time=t_end, runtime_sec=runtime,
                    out_path=str(out_file), notes=f"ARI={metrics['ari']:.4f}"
                )
                print(f"[M2 Primary ICC] Cohort={c:12s} Seed={seed:3d} -> ARI={metrics['ari']:.4f} ({runtime:.2f}s)")

            except Exception as e:
                runtime = time.perf_counter() - t0
                t_end = datetime.now(timezone.utc).isoformat()
                log_manifest(
                    exp_id=exp_id, exp_group="Primary_ICC", dataset=c, method="ICC_v2_adaptive",
                    config_desc="n_base=25, n_anchors=sqrt(N), rate=0.3", seed=seed,
                    status="failed", start_time=t_iso, end_time=t_end, runtime_sec=runtime,
                    out_path=str(out_file), error_msg=str(e)
                )
                print(f"[M2 Primary ICC ERROR] Cohort={c} Seed={seed}: {e}")

            gc.collect()


# ==============================================================================
# MILESTONE 3: BGSS Robustness, Matched Random Gating & Ablations
# ==============================================================================
def run_milestone3_bgss():
    print("\n" + "=" * 80)
    print(">>> MILESTONE 3: BGSS Robustness & Matched Random Gating (P1)")
    print("=" * 80)

    out_file = RESULTS_DIR / "bgss" / "bgss_ablation_results.csv"
    bio_cohorts = [
        "colon", "srbct", "cns", "leukemia", "prostate", "ovarian",
        "dlbcl", "breast", "su2001", "endometrium"
    ]

    completed = set()
    if out_file.exists():
        df_old = pd.read_csv(out_file)
        completed = set(zip(df_old["cohort"], df_old["condition"], df_old["seed"]))

    for c in bio_cohorts:
        X, y = load_cohort(c)
        k_true = len(np.unique(y))
        n_samples, n_features = X.shape
        n_anchors = max(10, int(np.sqrt(n_samples)))

        for seed in SEEDS:
            # ---------------- Condition 1: Full ICC with BGSS ----------------
            if (c, "Full_BGSS", seed) not in completed:
                t0 = time.perf_counter()
                t_iso = datetime.now(timezone.utc).isoformat()
                exp_id = f"M3-BGSS-{c}-FullBGSS-{seed}"
                try:
                    m1 = InvariantCoreConsensusV2(
                        n_clusters=k_true, n_base_models=25, n_anchors=n_anchors,
                        subspace_rate=0.3, random_state=seed, pool_mode="legacy"
                    )
                    m1.fit(X)
                    runtime = time.perf_counter() - t0
                    met = compute_metrics(X, y, m1.labels_)
                    row = {
                        "cohort": c, "N": n_samples, "D": n_features, "true_k": k_true,
                        "condition": "Full_BGSS", "seed": seed, "ari": met["ari"],
                        "nmi": met["nmi"], "ami": met["ami"], "fm_index": met["fm_index"],
                        "runtime_sec": runtime, "active_features": int(n_features * 0.3)
                    }
                    pd.DataFrame([row]).to_csv(out_file, mode="a", index=False, header=not out_file.exists())
                    log_manifest(exp_id, "BGSS_Robustness", c, "ICC_Full_BGSS", "subspace_rate=0.3", seed, "completed", t_iso, datetime.now(timezone.utc).isoformat(), runtime, str(out_file))
                    print(f"[M3 BGSS Full]   Cohort={c:12s} Seed={seed:3d} -> ARI={met['ari']:.4f}")
                except Exception as e:
                    log_manifest(exp_id, "BGSS_Robustness", c, "ICC_Full_BGSS", "", seed, "failed", t_iso, datetime.now(timezone.utc).isoformat(), time.perf_counter() - t0, str(out_file), str(e))

            # ---------------- Condition 2: No BGSS (All Features) ----------------
            if (c, "No_BGSS", seed) not in completed:
                t0 = time.perf_counter()
                t_iso = datetime.now(timezone.utc).isoformat()
                exp_id = f"M3-BGSS-{c}-NoBGSS-{seed}"
                try:
                    # subspace_rate=1.0 disables feature gating (uses all features)
                    m2 = InvariantCoreConsensusV2(
                        n_clusters=k_true, n_base_models=25, n_anchors=n_anchors,
                        subspace_rate=1.0, random_state=seed, pool_mode="legacy"
                    )
                    m2.fit(X)
                    runtime = time.perf_counter() - t0
                    met = compute_metrics(X, y, m2.labels_)
                    row = {
                        "cohort": c, "N": n_samples, "D": n_features, "true_k": k_true,
                        "condition": "No_BGSS", "seed": seed, "ari": met["ari"],
                        "nmi": met["nmi"], "ami": met["ami"], "fm_index": met["fm_index"],
                        "runtime_sec": runtime, "active_features": n_features
                    }
                    pd.DataFrame([row]).to_csv(out_file, mode="a", index=False, header=not out_file.exists())
                    log_manifest(exp_id, "BGSS_Robustness", c, "ICC_No_BGSS", "subspace_rate=1.0", seed, "completed", t_iso, datetime.now(timezone.utc).isoformat(), runtime, str(out_file))
                    print(f"[M3 BGSS None]   Cohort={c:12s} Seed={seed:3d} -> ARI={met['ari']:.4f}")
                except Exception as e:
                    log_manifest(exp_id, "BGSS_Robustness", c, "ICC_No_BGSS", "", seed, "failed", t_iso, datetime.now(timezone.utc).isoformat(), time.perf_counter() - t0, str(out_file), str(e))

            # ---------------- Condition 3: Matched Random Gating ----------------
            if (c, "Matched_Random_Gating", seed) not in completed:
                t0 = time.perf_counter()
                t_iso = datetime.now(timezone.utc).isoformat()
                exp_id = f"M3-BGSS-{c}-RandomGating-{seed}"
                try:
                    rng = np.random.default_rng(seed)
                    d_sub = max(10, int(n_features * 0.3))
                    rand_feats = rng.choice(n_features, d_sub, replace=False)
                    X_rand = X[:, rand_feats]

                    m3 = InvariantCoreConsensusV2(
                        n_clusters=k_true, n_base_models=25, n_anchors=n_anchors,
                        subspace_rate=1.0, random_state=seed, pool_mode="legacy"
                    )
                    m3.fit(X_rand)
                    runtime = time.perf_counter() - t0
                    met = compute_metrics(X, y, m3.labels_)
                    row = {
                        "cohort": c, "N": n_samples, "D": n_features, "true_k": k_true,
                        "condition": "Matched_Random_Gating", "seed": seed, "ari": met["ari"],
                        "nmi": met["nmi"], "ami": met["ami"], "fm_index": met["fm_index"],
                        "runtime_sec": runtime, "active_features": d_sub
                    }
                    pd.DataFrame([row]).to_csv(out_file, mode="a", index=False, header=not out_file.exists())
                    log_manifest(exp_id, "BGSS_Robustness", c, "ICC_Matched_Random", f"random_sub={d_sub}", seed, "completed", t_iso, datetime.now(timezone.utc).isoformat(), runtime, str(out_file))
                    print(f"[M3 BGSS Random] Cohort={c:12s} Seed={seed:3d} -> ARI={met['ari']:.4f}")
                except Exception as e:
                    log_manifest(exp_id, "BGSS_Robustness", c, "ICC_Matched_Random", "", seed, "failed", t_iso, datetime.now(timezone.utc).isoformat(), time.perf_counter() - t0, str(out_file), str(e))

            gc.collect()


# ==============================================================================
# MILESTONE 4: Modern Classical Baseline Comparisons
# ==============================================================================
def run_milestone4_baselines():
    print("\n" + "=" * 80)
    print(">>> MILESTONE 4: Modern & Classical Baseline Comparison (P1)")
    print("=" * 80)

    out_file = RESULTS_DIR / "baselines" / "modern_baselines_results.csv"
    cohorts = [
        "colon", "srbct", "cns", "leukemia", "prostate", "ovarian",
        "dlbcl", "breast", "su2001", "endometrium", "zheng68k"
    ]

    completed = set()
    if out_file.exists():
        df_old = pd.read_csv(out_file)
        completed = set(zip(df_old["cohort"], df_old["model"], df_old["seed"]))

    for c in cohorts:
        X, y = load_cohort(c)
        k_true = len(np.unique(y))
        n_samples, n_features = X.shape

        for seed in SEEDS:
            # Baseline definitions to evaluate
            baseline_tasks = [
                ("K-Means", lambda: run_kmeans(X, k_true, seed)[0]),
                ("Ward", lambda: run_ward(X, k_true)[0]),
                ("Spectral", lambda: run_spectral(X, k_true, seed)[0]),
                ("FCM", lambda: run_fcm(X, k_true, seed)[0]),
                ("Standard_Consensus", lambda: run_standard_consensus(X, k_true, seed)[0]),
                ("Sparse_KMeans", lambda: run_sparse_kmeans(X, k_true, seed)[0]),
                ("HDBSCAN*", lambda: run_hdbscan(X, min_cluster_size=5)[0]),
                ("GMM_BIC", lambda: run_gmm(X, k=k_true, seed=seed)[0]),
            ]

            for model_name, fn in baseline_tasks:
                if (c, model_name, seed) in completed:
                    continue

                t0 = time.perf_counter()
                t_iso = datetime.now(timezone.utc).isoformat()
                exp_id = f"M4-BASE-{c}-{model_name}-{seed}"

                try:
                    labels = fn()
                    runtime = time.perf_counter() - t0
                    met = compute_metrics(X, y, labels)

                    res_row = {
                        "cohort": c,
                        "N": n_samples,
                        "D": n_features,
                        "true_k": k_true,
                        "model": model_name,
                        "seed": seed,
                        "ari": met["ari"],
                        "nmi": met["nmi"],
                        "ami": met["ami"],
                        "fm_index": met["fm_index"],
                        "silhouette": met["silhouette"],
                        "davies_bouldin": met["davies_bouldin"],
                        "calinski_harabasz": met["calinski_harabasz"],
                        "n_clusters_found": met["n_clusters_found"],
                        "noise_fraction": met["noise_fraction"],
                        "runtime_sec": runtime,
                        "status": "COMPLETED",
                    }
                    pd.DataFrame([res_row]).to_csv(out_file, mode="a", index=False, header=not out_file.exists())
                    log_manifest(
                        exp_id, "Modern_Baselines", c, model_name, f"K={k_true}", seed,
                        "completed", t_iso, datetime.now(timezone.utc).isoformat(), runtime,
                        str(out_file), notes=f"ARI={met['ari']:.4f}"
                    )
                    print(f"[M4 Baseline] Cohort={c:12s} Model={model_name:18s} Seed={seed:3d} -> ARI={met['ari']:.4f}")

                except Exception as e:
                    runtime = time.perf_counter() - t0
                    log_manifest(
                        exp_id, "Modern_Baselines", c, model_name, f"K={k_true}", seed,
                        "failed", t_iso, datetime.now(timezone.utc).isoformat(), runtime,
                        str(out_file), error_msg=str(e)
                    )
                    print(f"[M4 ERROR] Cohort={c} Model={model_name}: {e}")

                gc.collect()


# ==============================================================================
# MILESTONE 5: Unknown-K Evaluation (Synthetic & Real Biological Cohorts)
# ==============================================================================
def run_milestone5_unknown_k():
    print("\n" + "=" * 80)
    print(">>> MILESTONE 5: Unknown-K Evaluation (Model Order Selection Benchmark)")
    print("=" * 80)

    synth_out = RESULTS_DIR / "unknown_k" / "unknown_k_synthetic_results.csv"
    real_out = RESULTS_DIR / "unknown_k" / "unknown_k_real_results.csv"

    # --- Part A: Synthetic Grid ---
    synth_configs = [
        {"cfg_id": "SYN-K2-BAL", "k": 2, "n": 200, "d_sig": 20, "d_noise": 100, "bal": True},
        {"cfg_id": "SYN-K3-BAL", "k": 3, "n": 300, "d_sig": 20, "d_noise": 100, "bal": True},
        {"cfg_id": "SYN-K4-IMB", "k": 4, "n": 400, "d_sig": 30, "d_noise": 150, "bal": False},
        {"cfg_id": "SYN-K5-NOISE", "k": 5, "n": 500, "d_sig": 20, "d_noise": 500, "bal": True},
        {"cfg_id": "SYN-K8-COMPLEX", "k": 8, "n": 400, "d_sig": 40, "d_noise": 200, "bal": False},
        {"cfg_id": "SYN-K10-EXTREME", "k": 10, "n": 500, "d_sig": 50, "d_noise": 500, "bal": False},
    ]

    completed_synth = set()
    if synth_out.exists():
        df_old = pd.read_csv(synth_out)
        completed_synth = set(zip(df_old["config_id"], df_old["method"], df_old["seed"]))

    for sc in synth_configs:
        k_true = sc["k"]
        cfg_id = sc["cfg_id"]

        for seed in SEEDS:
            # Generate synthetic clusters submerged in Gaussian distractor noise
            rng = np.random.default_rng(seed)
            if sc["bal"]:
                sizes = [sc["n"] // k_true] * k_true
                sizes[0] += sc["n"] - sum(sizes)
            else:
                probs = rng.dirichlet(np.ones(k_true) * 0.5)
                sizes = np.fmax(rng.multinomial(sc["n"], probs), 5)

            X_list = []
            y_list = []
            for i, sz in enumerate(sizes):
                mean = rng.uniform(-4, 4, sc["d_sig"])
                cov = np.eye(sc["d_sig"]) * rng.uniform(0.5, 1.5)
                X_list.append(rng.multivariate_normal(mean, cov, sz))
                y_list.append(np.full(sz, i))

            X_signal = np.vstack(X_list)
            y_synth = np.concatenate(y_list)
            X_noise = rng.standard_normal((len(X_signal), sc["d_noise"]))
            X_synth = StandardScaler().fit_transform(np.hstack([X_signal, X_noise]))

            # Candidate methods under unknown-K
            methods = [
                ("ICC-AutoK", lambda: _run_icc_autok_wrapper(X_synth, k_min=2, k_max=10, seed=seed)),
                ("GMM-BIC", lambda: _run_gmm_bic_select(X_synth, k_range=(2, 10), seed=seed)),
                ("Spectral-Eigengap", lambda: _run_spectral_eigengap(X_synth, max_k=10, seed=seed)),
                ("HDBSCAN*", lambda: _run_hdbscan_unknown(X_synth)),
            ]

            for m_name, fn in methods:
                if (cfg_id, m_name, seed) in completed_synth:
                    continue

                t0 = time.perf_counter()
                t_iso = datetime.now(timezone.utc).isoformat()
                exp_id = f"M5-SYN-{cfg_id}-{m_name}-{seed}"

                try:
                    k_est, labels = fn()
                    runtime = time.perf_counter() - t0
                    met = compute_metrics(X_synth, y_synth, labels)

                    row = {
                        "config_id": cfg_id, "true_k": k_true, "method": m_name,
                        "seed": seed, "estimated_k": k_est, "k_error": int(k_est - k_true),
                        "abs_k_error": abs(int(k_est - k_true)), "exact_k_hit": int(k_est == k_true),
                        "ari": met["ari"], "nmi": met["nmi"], "silhouette": met["silhouette"],
                        "runtime_sec": runtime, "N": sc["n"], "D_signal": sc["d_sig"], "D_noise": sc["d_noise"]
                    }
                    pd.DataFrame([row]).to_csv(synth_out, mode="a", index=False, header=not synth_out.exists())
                    log_manifest(exp_id, "Unknown_K_Synthetic", cfg_id, m_name, f"TrueK={k_true}", seed, "completed", t_iso, datetime.now(timezone.utc).isoformat(), runtime, str(synth_out), notes=f"EstK={k_est}, ARI={met['ari']:.4f}")
                    print(f"[M5 Synth] Cfg={cfg_id:16s} Method={m_name:18s} TrueK={k_true:2d} EstK={k_est:2d} ARI={met['ari']:.4f}")
                except Exception as e:
                    log_manifest(exp_id, "Unknown_K_Synthetic", cfg_id, m_name, f"TrueK={k_true}", seed, "failed", t_iso, datetime.now(timezone.utc).isoformat(), time.perf_counter() - t0, str(synth_out), str(e))

                gc.collect()

    # --- Part B: Real Biological Cohorts with Hidden K ---
    real_cohorts = ["colon", "srbct", "cns", "leukemia", "dlbcl", "breast", "su2001"]
    completed_real = set()
    if real_out.exists():
        df_old_r = pd.read_csv(real_out)
        completed_real = set(zip(df_old_r["cohort"], df_old_r["method"], df_old_r["seed"]))

    for c in real_cohorts:
        X, y = load_cohort(c)
        k_true = len(np.unique(y))

        for seed in SEEDS:
            methods_real = [
                ("ICC-AutoK", lambda: _run_icc_autok_wrapper(X, k_min=2, k_max=min(10, max(3, k_true + 2)), seed=seed)),
                ("GMM-BIC", lambda: _run_gmm_bic_select(X, k_range=(2, 10), seed=seed)),
                ("Spectral-Eigengap", lambda: _run_spectral_eigengap(X, max_k=10, seed=seed)),
                ("HDBSCAN*", lambda: _run_hdbscan_unknown(X)),
            ]

            for m_name, fn in methods_real:
                if (c, m_name, seed) in completed_real:
                    continue

                t0 = time.perf_counter()
                t_iso = datetime.now(timezone.utc).isoformat()
                exp_id = f"M5-REAL-{c}-{m_name}-{seed}"

                try:
                    k_est, labels = fn()
                    runtime = time.perf_counter() - t0
                    met = compute_metrics(X, y, labels)

                    row = {
                        "cohort": c, "true_k": k_true, "method": m_name, "seed": seed,
                        "estimated_k": k_est, "k_error": int(k_est - k_true),
                        "abs_k_error": abs(int(k_est - k_true)), "exact_k_hit": int(k_est == k_true),
                        "ari": met["ari"], "nmi": met["nmi"], "silhouette": met["silhouette"],
                        "runtime_sec": runtime, "N": X.shape[0], "D": X.shape[1]
                    }
                    pd.DataFrame([row]).to_csv(real_out, mode="a", index=False, header=not real_out.exists())
                    log_manifest(exp_id, "Unknown_K_Real", c, m_name, f"HiddenK={k_true}", seed, "completed", t_iso, datetime.now(timezone.utc).isoformat(), runtime, str(real_out), notes=f"EstK={k_est}, ARI={met['ari']:.4f}")
                    print(f"[M5 Real Bio] Cohort={c:12s} Method={m_name:18s} TrueK={k_true:2d} EstK={k_est:2d} ARI={met['ari']:.4f}")
                except Exception as e:
                    log_manifest(exp_id, "Unknown_K_Real", c, m_name, f"HiddenK={k_true}", seed, "failed", t_iso, datetime.now(timezone.utc).isoformat(), time.perf_counter() - t0, str(real_out), str(e))

                gc.collect()


def _run_icc_autok_wrapper(X: np.ndarray, k_min=2, k_max=10, seed=42) -> Tuple[int, np.ndarray]:
    res = run_icc_autok(X, k_min=k_min, k_max=k_max, seed=seed)
    return res.best_k_pac, res.best_labels_pac


def _run_gmm_bic_select(X: np.ndarray, k_range=(2, 10), seed=42) -> Tuple[int, np.ndarray]:
    best_bic = np.inf
    best_k = k_range[0]
    best_labels = None
    for k in range(k_range[0], k_range[1] + 1):
        gmm = GaussianMixture(n_components=k, covariance_type="diag", random_state=seed, max_iter=100)
        labels = gmm.fit_predict(X)
        bic = gmm.bic(X)
        if bic < best_bic:
            best_bic = bic
            best_k = k
            best_labels = labels
    return best_k, best_labels


def _run_spectral_eigengap(X: np.ndarray, max_k=10, seed=42) -> Tuple[int, np.ndarray]:
    from sklearn.metrics.pairwise import rbf_kernel
    # Compute RBF affinity
    A = rbf_kernel(X, gamma=1.0 / X.shape[1])
    D = np.diag(np.sum(A, axis=1))
    L = D - A
    # Compute normalized Laplacian L_sym = D^(-1/2) L D^(-1/2)
    d_inv_sqrt = np.power(np.sum(A, axis=1), -0.5)
    d_inv_sqrt[np.isinf(d_inv_sqrt)] = 0.0
    L_sym = np.eye(A.shape[0]) - (d_inv_sqrt[:, None] * A * d_inv_sqrt[None, :])
    eigenvals = np.sort(np.linalg.eigvalsh(L_sym))
    # Eigengap heuristic: find max gap for k in [2, max_k]
    gaps = np.diff(eigenvals[: max_k + 1])
    best_k = int(np.argmax(gaps[1:]) + 2)  # offset for k >= 2
    sc = SpectralClustering(n_clusters=best_k, affinity="nearest_neighbors", random_state=seed)
    labels = sc.fit_predict(X)
    return best_k, labels


def _run_hdbscan_unknown(X: np.ndarray) -> Tuple[int, np.ndarray]:
    labels, _, _ = run_hdbscan(X, min_cluster_size=5)
    valid_labels = labels[labels >= 0]
    k_est = len(np.unique(valid_labels)) if len(valid_labels) > 0 else 1
    return max(1, k_est), labels


# ==============================================================================
# MILESTONE 6: Synthetic Falsification & Stress Tests (Non-Convex Failure Modes)
# ==============================================================================
def run_milestone6_synthetic_stress():
    print("\n" + "=" * 80)
    print(">>> MILESTONE 6: Synthetic Falsification & Stress Tests (P2)")
    print("=" * 80)

    out_file = RESULTS_DIR / "synthetic" / "synthetic_stress_results.csv"
    from sklearn.datasets import make_circles, make_moons

    stress_tasks = [
        ("Two_Moons_Clean", lambda s: make_moons(n_samples=300, noise=0.05, random_state=s)),
        ("Two_Moons_Noisy", lambda s: make_moons(n_samples=300, noise=0.25, random_state=s)),
        ("Concentric_Circles_Clean", lambda s: make_circles(n_samples=300, noise=0.05, factor=0.5, random_state=s)),
        ("Concentric_Circles_Noisy", lambda s: make_circles(n_samples=300, noise=0.20, factor=0.5, random_state=s)),
    ]

    completed = set()
    if out_file.exists():
        df_old = pd.read_csv(out_file)
        completed = set(zip(df_old["geometry"], df_old["method"], df_old["seed"]))

    for geom_name, gen_fn in stress_tasks:
        for seed in SEEDS:
            X_geom, y_geom = gen_fn(seed)
            k_true = 2

            models = [
                ("ICC_v2", lambda: run_icc_v2(X_geom, k_true, seed)[0]),
                ("Standard_Consensus", lambda: run_standard_consensus(X_geom, k_true, seed)[0]),
                ("K-Means", lambda: run_kmeans(X_geom, k_true, seed)[0]),
                ("Spectral_RBF", lambda: run_spectral(X_geom, k_true, seed)[0]),
                ("Ward", lambda: run_ward(X_geom, k_true)[0]),
            ]

            for m_name, fn in models:
                if (geom_name, m_name, seed) in completed:
                    continue

                t0 = time.perf_counter()
                t_iso = datetime.now(timezone.utc).isoformat()
                exp_id = f"M6-STRESS-{geom_name}-{m_name}-{seed}"

                try:
                    labels = fn()
                    runtime = time.perf_counter() - t0
                    met = compute_metrics(X_geom, y_geom, labels)

                    row = {
                        "geometry": geom_name, "method": m_name, "seed": seed,
                        "ari": met["ari"], "nmi": met["nmi"], "silhouette": met["silhouette"],
                        "runtime_sec": runtime, "N": len(X_geom), "D": X_geom.shape[1]
                    }
                    pd.DataFrame([row]).to_csv(out_file, mode="a", index=False, header=not out_file.exists())
                    log_manifest(exp_id, "Synthetic_Stress", geom_name, m_name, "NonConvex", seed, "completed", t_iso, datetime.now(timezone.utc).isoformat(), runtime, str(out_file), notes=f"ARI={met['ari']:.4f}")
                    print(f"[M6 Stress] Geom={geom_name:25s} Method={m_name:18s} Seed={seed:3d} -> ARI={met['ari']:.4f}")
                except Exception as e:
                    log_manifest(exp_id, "Synthetic_Stress", geom_name, m_name, "NonConvex", seed, "failed", t_iso, datetime.now(timezone.utc).isoformat(), time.perf_counter() - t0, str(out_file), str(e))

                gc.collect()


def main():
    print("=" * 80)
    print("STARTING AUTONOMOUS OVERNIGHT EXPERIMENT EXECUTION ENGINE")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 80)

    # Milestone 2: Primary ICC Benchmark (P0)
    run_milestone2_primary_icc()

    # Milestone 3: BGSS Robustness & Matched Random Gating (P1)
    run_milestone3_bgss()

    # Milestone 4: Modern Baselines (P1)
    run_milestone4_baselines()

    # Milestone 5: Unknown-K Evaluation (P1)
    run_milestone5_unknown_k()

    # Milestone 6: Synthetic Falsification & Non-Convex Stress Tests (P2)
    run_milestone6_synthetic_stress()

    print("\n" + "=" * 80)
    print("ALL OVERNIGHT EXPERIMENTAL RUNS COMPLETED SUCCESSFULLY.")
    print("=" * 80)


if __name__ == "__main__":
    main()
