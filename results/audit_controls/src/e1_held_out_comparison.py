"""
E1 & E3b Extended Audit: Pre-Registered Held-Out Dataset Comparison Protocol.

This script implements the formal pre-registered held-out evaluation requested
by the research audit:
1. FIXED SEARCH BUDGET:
   Grid of candidate pool sizes: F = [0.02, 0.05, 0.10, 0.15, 0.25, 0.40] of features.
   Selection criteria evaluated without labels:
   - Silhouette coefficient of consensus partition in U_emb
   - Mean sample stability (from closed-form quadratic determinacy)
2. FIXED DATASET PARTITION:
   - Development / Tuning Suite (n = 8 datasets):
     ['colon', 'srbct', 'cns', 'leukemia', 'prostate', 'ovarian', 'madelon', 'sonar']
   - Held-Out Test Suite (n = 13 datasets, zero label-peeking / zero hyperparameter tuning):
     ['breast_cancer_genomic', 'gisette', 'glioma', 'har', 'indian_pines', 'isolet',
      'lung_cancer', 'lymphoma', 'newsgroups20', 'usps', 'waveform', 'yale_b', 'zheng68k']
3. COMPARATIVE METHODS:
   - ICC-v2 (Fixed 15% Default)
   - ICC-v2 (Selected by Silhouette in U_emb)
   - ICC-v2 (Selected by Mean Stability)
   - ICC-v2 (Grid Average over Search Budget)
   - ICC-v2 (Oracle Best Fraction - Label-Peeking Upper Bound)
   - ICC-v1 (Full Bipartite Consensus, no feature filtering)
   - Standard Consensus (EAC with 25 random subspaces)
   - Li et al. (2019) Core-Halo Consensus
   - Ward Hierarchical Agglomerative
   - Spectral Clustering
   - K-Means
4. STATISTICAL VALIDATION:
   - Friedman omnibus test across models
   - Pairwise Wilcoxon signed-rank tests with Holm-Bonferroni correction
   - Stratified analysis by high-D biological regime (D/N > 5)
"""

import os
import sys
import time
import glob
import pathlib
import warnings
from typing import Dict, List, Tuple, Any

import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, wilcoxon
from sklearn.metrics import adjusted_rand_score as ari, silhouette_score

warnings.filterwarnings("ignore")

# Ensure repository root is on sys.path
REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.icc.core import run_clusterer, pairwise_coassoc
from src.icc.consensus import InvariantCoreConsensus as ICCv1
from src.icc.consensus_v2 import InvariantCoreConsensusV2 as ICCv2

CACHE_DIR = REPO_ROOT / "experiments" / "exp3_real_world_benchmarks" / "data" / "cache"
OUTPUT_DIR = REPO_ROOT / "experiments" / "audit_controls" / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Pre-Registered Protocol Constants
# -----------------------------------------------------------------------------
POOL_GRID = [0.02, 0.05, 0.10, 0.15, 0.25, 0.40]
SEEDS = [42, 101, 202, 303, 404]

DEV_DATASETS = [
    "colon", "srbct", "cns", "leukemia",
    "prostate", "ovarian", "madelon", "sonar",
]

HELD_OUT_DATASETS = [
    "breast_cancer_genomic", "gisette", "glioma", "har",
    "indian_pines", "isolet", "lung_cancer", "lymphoma",
    "newsgroups20", "usps", "waveform", "yale_b", "zheng68k",
]


def load_dataset(name: str) -> Tuple[np.ndarray, np.ndarray, int]:
    """Load cached dataset (.npz) and return X, y, and cluster count K."""
    path = CACHE_DIR / f"{name}.npz"
    if not path.exists():
        raise FileNotFoundError(f"Missing cached dataset: {path}")
    data = np.load(path, allow_pickle=False)
    X = data["X"].astype(np.float64)
    y = data["y"].astype(int)
    K = len(np.unique(y))
    return X, y, K


def safe_silhouette(X_emb: np.ndarray, labels: np.ndarray) -> float:
    """Compute silhouette score safely, returning -1.0 if degenerate."""
    n_unique = len(np.unique(labels))
    if n_unique < 2 or n_unique >= len(labels):
        return -1.0
    try:
        # Sample if N > 2000 for efficiency
        if len(labels) > 2000:
            rng = np.random.default_rng(0)
            idx = rng.choice(len(labels), size=2000, replace=False)
            return float(silhouette_score(X_emb[idx], labels[idx]))
        return float(silhouette_score(X_emb, labels))
    except Exception:
        return -1.0


def evaluate_icc_grid(
    X: np.ndarray, y: np.ndarray, K: int, seed: int, pool_grid: List[float]
) -> Dict[str, Any]:
    """
    Fit ICC-v2 across the pre-registered search budget pool_grid.
    Returns evaluated trial metrics for each candidate size.
    """
    records = []
    for frac in pool_grid:
        m = ICCv2(
            n_clusters=K,
            n_base_models=25,
            n_anchors=min(30, len(y)),
            pool_mode="bc_frac",
            pool_frac=frac,
            random_state=seed,
        )
        preds = m.fit_predict(X)
        score_ari = ari(y, preds)
        score_sil = safe_silhouette(m.U_emb_, preds)
        score_stab = float(np.mean(m.stability_)) if m.stability_ is not None else 0.0

        records.append({
            "frac": frac,
            "ari": score_ari,
            "sil": score_sil,
            "stab": score_stab,
        })

    df_grid = pd.DataFrame(records)

    # 1. Fixed 15% default
    fixed15_row = df_grid[df_grid["frac"] == 0.15].iloc[0]
    ari_fixed15 = fixed15_row["ari"]

    # 2. Selected by silhouette in U_emb (label-free)
    best_sil_idx = df_grid["sil"].idxmax()
    ari_sel_sil = df_grid.loc[best_sil_idx, "ari"]
    frac_sel_sil = df_grid.loc[best_sil_idx, "frac"]

    # 3. Selected by mean sample stability (label-free)
    best_stab_idx = df_grid["stab"].idxmax()
    ari_sel_stab = df_grid.loc[best_stab_idx, "ari"]
    frac_sel_stab = df_grid.loc[best_stab_idx, "frac"]

    # 4. Grid mean across candidate search budget
    ari_grid_mean = df_grid["ari"].mean()

    # 5. Oracle best fraction (label-peeking diagnostic ceiling)
    best_oracle_idx = df_grid["ari"].idxmax()
    ari_oracle = df_grid.loc[best_oracle_idx, "ari"]
    frac_oracle = df_grid.loc[best_oracle_idx, "frac"]

    return {
        "ICC_v2_fixed15": ari_fixed15,
        "ICC_v2_sel_sil": ari_sel_sil,
        "ICC_v2_sel_stab": ari_sel_stab,
        "ICC_v2_grid_mean": ari_grid_mean,
        "ICC_v2_oracle": ari_oracle,
        "frac_sel_sil": frac_sel_sil,
        "frac_sel_stab": frac_sel_stab,
        "frac_oracle": frac_oracle,
    }


def evaluate_baselines(X: np.ndarray, y: np.ndarray, K: int, seed: int) -> Dict[str, float]:
    """Evaluate standard non-gated and single-model baselines."""
    N, D = X.shape
    out = {}

    # K-Means
    km_labels = run_clusterer("kmeans", X, K, seed=seed)
    out["K-Means"] = ari(y, km_labels)

    # Ward
    ward_labels = run_clusterer("ward", X, K, seed=seed)
    out["Ward"] = ari(y, ward_labels)

    # Spectral
    spec_labels = run_clusterer("spectral", X, K, seed=seed)
    out["Spectral"] = ari(y, spec_labels)

    # Standard Consensus (EAC, 25 random subspaces)
    rng = np.random.default_rng(seed)
    sub_d = max(2, int(0.3 * D))
    partitions = [
        run_clusterer("kmeans", X[:, rng.choice(D, size=sub_d, replace=False)], K, seed=int(rng.integers(1e6)))
        for _ in range(25)
    ]
    S = pairwise_coassoc(partitions)
    from sklearn.cluster import SpectralClustering
    sc = SpectralClustering(n_clusters=K, affinity="precomputed", random_state=seed, assign_labels="kmeans")
    std_cons_labels = sc.fit_predict(S)
    out["Standard_Consensus"] = ari(y, std_cons_labels)

    # Li et al. (2019) Consensus
    P_li = [run_clusterer("kmeans", X, K, seed=int(rng.integers(1e6))) for _ in range(25)]
    S_li = pairwise_coassoc(P_li)
    sc_li = SpectralClustering(n_clusters=K, affinity="precomputed", random_state=seed, assign_labels="kmeans")
    li_labels = sc_li.fit_predict(S_li)
    out["Li_et_al_2019"] = ari(y, li_labels)

    # ICC-v1 (Anchor-Only Consensus, 100% features)
    m_v1 = ICCv1(n_clusters=K, n_base_models=25, n_anchors=min(30, N), random_state=seed)
    v1_labels = m_v1.fit_predict(X)
    out["ICC_v1"] = ari(y, v1_labels)

    return out


def run_evaluation_suite(dataset_list: List[str], suite_name: str) -> pd.DataFrame:
    """Execute complete trial sweep across pre-specified dataset list."""
    print("=" * 80)
    print(f"RUNNING PROTOCOL ON: {suite_name.upper()} ({len(dataset_list)} DATASETS x {len(SEEDS)} SEEDS)")
    print("=" * 80)

    rows = []
    for dname in dataset_list:
        X, y, K = load_dataset(dname)
        N, D = X.shape
        high_d = (D / N) > 5.0
        print(f"\n[Dataset: {dname:<22}] N={N:5d}, D={D:6d}, K={K:2d} | High-D Bio: {high_d}")

        for s in SEEDS:
            t0 = time.perf_counter()
            # 1. ICC-v2 pool grid sweep
            icc_results = evaluate_icc_grid(X, y, K, seed=s, pool_grid=POOL_GRID)

            # 2. Baseline models
            base_results = evaluate_baselines(X, y, K, seed=s)

            elapsed = time.perf_counter() - t0
            record = {
                "suite": suite_name,
                "dataset": dname,
                "N": N,
                "D": D,
                "K": K,
                "high_d": high_d,
                "seed": s,
                "runtime_s": round(elapsed, 2),
                **icc_results,
                **base_results,
            }
            rows.append(record)

    df = pd.DataFrame(rows)
    return df


def compute_holms_wilcoxon(df_summary: pd.DataFrame, reference_col: str, candidate_cols: List[str]) -> pd.DataFrame:
    """Perform pairwise Wilcoxon signed-rank test against reference with Holm correction."""
    tests = []
    for col in candidate_cols:
        if col == reference_col:
            continue
        diff = df_summary[reference_col] - df_summary[col]
        # Ignore zero differences
        non_zero = diff[diff != 0]
        if len(non_zero) < 5:
            p_val = 1.0
            stat = 0.0
        else:
            try:
                stat, p_val = wilcoxon(df_summary[reference_col], df_summary[col])
            except Exception:
                stat, p_val = 0.0, 1.0

        tests.append({
            "comparison": f"{reference_col} vs {col}",
            "mean_ref": df_summary[reference_col].mean(),
            "mean_other": df_summary[col].mean(),
            "mean_diff": (df_summary[reference_col] - df_summary[col]).mean(),
            "stat": stat,
            "raw_p": p_val,
        })

    df_tests = pd.DataFrame(tests).sort_values("raw_p")
    # Holm-Bonferroni step-down correction
    m = len(df_tests)
    df_tests["holm_alpha"] = [0.05 / (m - i) for i in range(m)]
    df_tests["significant"] = df_tests["raw_p"] < df_tests["holm_alpha"]
    return df_tests


def main():
    print("=" * 80)
    print("INDEPENDENT AUDIT: PRE-REGISTERED HELD-OUT DATASET COMPARISON")
    print(f"Candidate Search Grid: {POOL_GRID}")
    print(f"Development Suite (n = {len(DEV_DATASETS)}): {DEV_DATASETS}")
    print(f"Held-Out Suite (n = {len(HELD_OUT_DATASETS)}): {HELD_OUT_DATASETS}")
    print("=" * 80)

    # 1. Run Development Suite
    df_dev = run_evaluation_suite(DEV_DATASETS, "development")

    # 2. Run Held-Out Suite
    df_held = run_evaluation_suite(HELD_OUT_DATASETS, "held_out")

    # Combine and save full trial dataset
    df_trials = pd.concat([df_dev, df_held], ignore_index=True)
    trials_csv = OUTPUT_DIR / "e1_held_out_trials.csv"
    df_trials.to_csv(trials_csv, index=False)
    print(f"\n[+] Saved trial records ({len(df_trials)} rows) to: {trials_csv}")

    # Summary by dataset (mean over 5 seeds)
    core_models = [
        "ICC_v2_fixed15",
        "ICC_v2_sel_sil",
        "ICC_v2_sel_stab",
        "ICC_v2_grid_mean",
        "ICC_v2_oracle",
        "ICC_v1",
        "Standard_Consensus",
        "Li_et_al_2019",
        "Ward",
        "Spectral",
        "K-Means",
    ]

    summary_df = df_trials.groupby(["suite", "dataset", "high_d"])[core_models].mean().round(4).reset_index()
    summary_csv = OUTPUT_DIR / "e1_held_out_summary.csv"
    summary_df.to_csv(summary_csv, index=False)
    print(f"[+] Saved summary matrix to: {summary_csv}")

    # -------------------------------------------------------------------------
    # Analysis 1: Development Suite Evaluation
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PHASE 1: DEVELOPMENT SUITE RESULTS (n = 8 Datasets)")
    print("=" * 80)
    dev_summary = summary_df[summary_df["suite"] == "development"].set_index("dataset")
    print(dev_summary[core_models].round(3).to_string())
    print("\n--- Development Suite Mean ARI by Method ---")
    dev_means = dev_summary[core_models].mean().sort_values(ascending=False)
    for m, val in dev_means.items():
        print(f"  {m:<20}: {val:.4f}")

    # -------------------------------------------------------------------------
    # Analysis 2: Held-Out Suite Evaluation
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PHASE 2: HELD-OUT TEST SUITE RESULTS (n = 13 Datasets, Strictly Unseen)")
    print("=" * 80)
    held_summary = summary_df[summary_df["suite"] == "held_out"].set_index("dataset")
    print(held_summary[core_models].round(3).to_string())
    print("\n--- Held-Out Suite Mean ARI by Method ---")
    held_means = held_summary[core_models].mean().sort_values(ascending=False)
    for m, val in held_means.items():
        print(f"  {m:<20}: {val:.4f}")

    print("\n--- Held-Out Suite Mean Ranks (1 = Best) ---")
    ranks_df = held_summary[core_models].rank(axis=1, ascending=False)
    mean_ranks = ranks_df.mean().sort_values()
    for m, val in mean_ranks.items():
        print(f"  {m:<20}: {val:.2f}")

    # -------------------------------------------------------------------------
    # Analysis 3: Stratified High-D Biological Regime (D/N > 5)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PHASE 3: STRATIFIED SUBGROUP ANALYSIS (D/N > 5 High-D Biological Regimes)")
    print("=" * 80)
    high_d_summary = summary_df[summary_df["high_d"]].set_index("dataset")
    print(f"Identified {len(high_d_summary)} High-D Biological Datasets:")
    print(high_d_summary[core_models].round(3).to_string())
    print("\n--- High-D Biological Subgroup Mean ARI ---")
    high_d_means = high_d_summary[core_models].mean().sort_values(ascending=False)
    for m, val in high_d_means.items():
        print(f"  {m:<20}: {val:.4f}")

    # -------------------------------------------------------------------------
    # Analysis 4: Pre-Specified Statistical Tests
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PHASE 4: STATISTICAL HYPOTHESIS TESTING (Held-Out Suite, n = 13)")
    print("=" * 80)

    # Omnibus Friedman Test
    test_models = [
        "ICC_v2_fixed15",
        "ICC_v2_sel_sil",
        "ICC_v1",
        "Standard_Consensus",
        "Li_et_al_2019",
        "Ward",
        "Spectral",
        "K-Means",
    ]
    friedman_matrix = [held_summary[m].values for m in test_models]
    stat_f, p_f = friedmanchisquare(*friedman_matrix)
    print(f"Omnibus Friedman Test across {len(test_models)} models: chi2 = {stat_f:.3f}, p = {p_f:.4f}")

    # Pairwise Wilcoxon tests against fixed 15% default with Holm correction
    print("\n--- Pairwise Wilcoxon Tests vs ICC_v2_fixed15 (Holm-Bonferroni Corrected) ---")
    df_tests = compute_holms_wilcoxon(held_summary, "ICC_v2_fixed15", test_models)
    print(df_tests[["comparison", "mean_ref", "mean_other", "mean_diff", "raw_p", "holm_alpha", "significant"]].to_string(index=False))

    stats_csv = OUTPUT_DIR / "e1_held_out_stats.csv"
    df_tests.to_csv(stats_csv, index=False)
    print(f"\n[+] Saved statistical tests to: {stats_csv}")


if __name__ == "__main__":
    main()
