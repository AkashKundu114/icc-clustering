"""
src/icc/confirmatory/runner.py
Confirmatory Experiment Execution Engine for DMKD Gate G2.

Executes all pre-registered algorithms across 30 deterministic seeds:
- Enforces strict label quarantine (models operate solely on unlabeled X).
- Fingerprints all predictions with SHA-256 before unsealing the label vault.
- Implements paired experimental designs for Family 1 and Family 2 hypotheses.
"""

import hashlib
import json
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Ensure root is in sys.path
_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from icc.baselines.classical import run_kmeans, run_ward, run_spectral
from icc.baselines.consensus import run_standard_consensus, run_li_et_al_2019, run_icc_v2
from icc.baselines.sparse_kmeans import run_sparse_kmeans
from icc.baselines.anchor import run_fcag, run_fastmvc
from icc.confirmatory.vault import LabelQuarantineVault, fingerprint_predictions

# Master seed sequence (S = 30 independent seeds)
MASTER_SEED = 20261101
sq = np.random.SeedSequence(MASTER_SEED)
CONFIRMATORY_SEEDS = [int(s.generate_state(1)[0] % 100000) for s in sq.spawn(30)]


def run_kmeans_varfilt(X: np.ndarray, k: int, seed: int, top_frac: float = 0.20):
    """K-Means with top 20% variance feature filter (label-blind)."""
    variances = np.var(X, axis=0)
    n_keep = max(int(X.shape[1] * top_frac), 50)
    top_idx = np.argsort(variances)[-n_keep:]
    X_sub = X[:, top_idx]
    return run_kmeans(X_sub, k=k, seed=seed)


def run_kmeans_pca(X: np.ndarray, k: int, seed: int, n_components: int = 30):
    """K-Means on top PCA components (label-blind)."""
    n_comp = min(n_components, X.shape[0] - 1, X.shape[1])
    pca = PCA(n_components=n_comp, random_state=seed)
    X_pca = pca.fit_transform(X)
    return run_kmeans(X_pca, k=k, seed=seed)


def run_matched_random_gating(X: np.ndarray, k: int, seed: int):
    """
    Bipartite consensus with budget-matched random feature gating (Control for H2a).
    Matches feature count using random subspace selection.
    """
    from icc.consensus_v2 import InvariantCoreConsensusV2
    model = InvariantCoreConsensusV2(
        n_clusters=k,
        n_anchors=min(40, X.shape[0]),
        pool_mode="random",  # Budget-matched random subspace gating
        random_state=seed,
    )
    t0 = time.perf_counter()
    model.fit(X)
    runtime = time.perf_counter() - t0
    labels = model.labels_
    return labels, runtime, {"model": "Matched_Random", "gating": "random"}


def run_dense_gac(X: np.ndarray, k: int, seed: int):
    """
    GAC feature gating under dense consensus matrix (Ablation for H2b).
    """
    from icc.consensus_v2 import InvariantCoreConsensusV2
    model = InvariantCoreConsensusV2(
        n_clusters=k,
        n_anchors=X.shape[0],  # All samples as anchors -> dense consensus graph
        core_quantile=0.0,
        random_state=seed,
    )
    t0 = time.perf_counter()
    model.fit(X)
    runtime = time.perf_counter() - t0
    labels = model.labels_
    return labels, runtime, {"model": "Dense_GAC", "anchors": "dense"}


def run_knockout4_random_landmarks(X: np.ndarray, k: int, seed: int):
    """
    Bipartite consensus with uniform random landmark anchors instead of core anchors (H3 TOST).
    """
    from icc.consensus_v2 import InvariantCoreConsensusV2
    model = InvariantCoreConsensusV2(
        n_clusters=k,
        n_anchors=min(40, X.shape[0]),
        core_quantile=0.0,  # All samples eligible -> uniform random landmark sampling
        random_state=seed,
    )
    t0 = time.perf_counter()
    model.fit(X)
    runtime = time.perf_counter() - t0
    labels = model.labels_
    return labels, runtime, {"model": "Knockout_4", "anchor_method": "uniform_random"}


def execute_confirmatory_cohort(
    cohort_id: str,
    unlabeled_npz_path: Path,
    vault_dir: Path,
    output_dir: Path,
    seeds: Optional[List[int]] = None,
) -> pd.DataFrame:
    """
    Executes the full confirmatory model grid on a single cohort across seeds.
    """
    if seeds is None:
        seeds = CONFIRMATORY_SEEDS

    unlabeled_npz_path = Path(unlabeled_npz_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    preds_dir = output_dir / "predictions" / cohort_id
    preds_dir.mkdir(parents=True, exist_ok=True)

    data = np.load(unlabeled_npz_path)
    X = data["X"]
    K = int(data["n_clusters"])
    sample_accessions = data["sample_accessions"].tolist()
    N, D = X.shape

    vault = LabelQuarantineVault(cohort_id, vault_dir)
    vault_fp = vault.get_fingerprint()
    print(f"=== Starting Confirmatory Execution for {cohort_id} (N={N}, D={D}, K={K}) ===")
    print(f"Vault fingerprint: {vault_fp[:16]}... Seeds: {len(seeds)}")

    # Model dispatch table
    model_dispatch: Dict[str, Callable] = {
        # Primary Framework
        "Full_GAC": lambda s: run_icc_v2(X, k=K, seed=s),
        # Family 1 Baseline Comparators (8 Models)
        "StdCons_All": lambda s: run_standard_consensus(X, k=K, seed=s),
        "K-Means_All": lambda s: run_kmeans(X, k=K, seed=s),
        "K-Means_VarFilt": lambda s: run_kmeans_varfilt(X, k=K, seed=s),
        "K-Means_PCA": lambda s: run_kmeans_pca(X, k=K, seed=s),
        "SparseKMeans": lambda s: run_sparse_kmeans(X, k=K, seed=s),
        "FCAG": lambda s: run_fcag(X, k=K, seed=s),
        "FastMVC-Surrogate": lambda s: run_fastmvc(X, k=K, seed=s),
        "Li_et_al_2019": lambda s: run_li_et_al_2019(X, k=K, seed=s),
        # Family 2 Ablation Controls
        "Matched_Random": lambda s: run_matched_random_gating(X, k=K, seed=s),
        "Dense_GAC": lambda s: run_dense_gac(X, k=K, seed=s),
        "Knockout_4": lambda s: run_knockout4_random_landmarks(X, k=K, seed=s),
    }

    # Step 1: Execute all models with ZERO label access and fingerprint predictions
    predictions_map: Dict[str, np.ndarray] = {}
    run_records: List[Dict[str, Any]] = []

    for model_name, runner_fn in model_dispatch.items():
        for seed_idx, seed in enumerate(seeds):
            run_key = f"{cohort_id}__{model_name}__seed{seed}"
            t0 = time.perf_counter()
            try:
                pred_labels, runtime, meta = runner_fn(seed)
                status = "OK"
                pred_labels = np.asarray(pred_labels, dtype=np.int64)
            except Exception as e:
                print(f"[!] Error in {model_name} (seed {seed}): {e}")
                pred_labels = np.zeros(N, dtype=np.int64)
                runtime = time.perf_counter() - t0
                status = f"FAILED: {e}"
                meta = {}

            pred_fp = fingerprint_predictions(pred_labels)
            pred_file = preds_dir / f"{model_name}_seed_{seed}.npy"
            np.save(pred_file, pred_labels)

            predictions_map[run_key] = pred_labels
            run_records.append({
                "cohort_id": cohort_id,
                "model_name": model_name,
                "trial_idx": seed_idx,
                "seed": seed,
                "runtime_sec": round(float(runtime), 4),
                "status": status,
                "pred_fingerprint": pred_fp,
                "run_key": run_key,
            })

    print(f"[RUNNER] Completed {len(predictions_map)} runs. Unsealing label vault for evaluation...")

    # Step 2: Unseal label vault and compute evaluation metrics
    evaluated_metrics = vault.unseal_and_evaluate(predictions_map)

    # Step 3: Merge metrics with execution records
    final_rows: List[Dict[str, Any]] = []
    for r in run_records:
        k = r["run_key"]
        scores = evaluated_metrics.get(k, {})
        row = {
            "cohort_id": r["cohort_id"],
            "model_name": r["model_name"],
            "trial_idx": r["trial_idx"],
            "seed": r["seed"],
            "ari": scores.get("ari", np.nan),
            "nmi": scores.get("nmi", np.nan),
            "ami": scores.get("ami", np.nan),
            "v_measure": scores.get("v_measure", np.nan),
            "fm_index": scores.get("fm_index", np.nan),
            "runtime_sec": r["runtime_sec"],
            "status": r["status"],
            "pred_fingerprint": r["pred_fingerprint"],
        }
        final_rows.append(row)

    df_out = pd.DataFrame(final_rows)
    csv_out = output_dir / f"{cohort_id}_raw_results.csv"
    df_out.to_csv(csv_out, index=False)
    print(f"[DONE] Saved {len(df_out)} trial records to {csv_out}")

    # Generate within-cohort median and mean summaries
    summary = df_out.groupby("model_name")[["ari", "nmi", "ami", "runtime_sec"]].agg(["median", "mean", "std"])
    summary_out = output_dir / f"{cohort_id}_summary.csv"
    summary.to_csv(summary_out)
    print(f"[SUMMARY] Saved cohort summary to {summary_out}")

    return df_out
