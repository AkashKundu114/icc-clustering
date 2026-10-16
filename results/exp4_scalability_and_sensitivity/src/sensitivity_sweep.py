"""
Hyperparameter Sensitivity and Stability Landscape Engine for Experiment 4.
Sweeps:
1. Ensemble size M in [5, 100]
2. Number of candidate anchors L in [10, 120]
3. Core stability quantile tau_core in [0.20, 0.90]
4. Noise calibration decay parameter beta in [0.0, 8.0]
"""

import os
import sys
from pathlib import Path
import time
import numpy as np
import pandas as pd

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.icc.core import run_clusterer, pairwise_coassoc
from src.icc.metrics import evaluate_all
from experiments.exp3_real_world_benchmarks.src.dataset_loader import load_benchmark_dataset
from experiments.exp4_scalability_and_sensitivity.src.scaling_benchmark import generate_benchmark_synthetic

SENSITIVITY_CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "exp4_sensitivity_results.csv")


def run_icc_parametric(
    X,
    k=2,
    n_base_models=25,
    n_anchors=40,
    tau_quantile=0.50,
    beta=2.0,
    seed=42
):
    """
    Parametric ICC engine for multi-axis hyperparameter sensitivity evaluation.
    """
    N, D = X.shape
    rng = np.random.default_rng(seed)
    
    # 1. Adaptive pool feature screening
    from scipy.stats import kurtosis, skew
    kurt = kurtosis(X, axis=0)
    sk = skew(X, axis=0)
    bimodal = (sk**2 + 1.0) / (kurt + 3.0 + 1e-5)
    
    top_frac = min(1.0, max(0.15, 100.0 / D))
    pool_size = max(k, int(top_frac * D))
    candidate_pool = np.argsort(bimodal)[-pool_size:]
    sub_size = max(2, int(len(candidate_pool) * 0.30))
    
    # 2. Base models on guided subspaces
    partitions = []
    base_engine = "spectral" if N <= 100 else "kmeans"
    for m in range(n_base_models):
        seed_m = int(rng.integers(0, 100000))
        sub_idx = rng.choice(candidate_pool, size=sub_size, replace=False)
        p = run_clusterer(base_engine, X[:, sub_idx], k, seed=seed_m)
        partitions.append(p)
        
    S = pairwise_coassoc(partitions)
    
    # 3. Core stability filtering via tau_quantile
    np.fill_diagonal(S, 0.0)
    sample_stability = np.sum(S**2, axis=1) / max(1, N - 1)
    np.fill_diagonal(S, 1.0)
    
    tau_stab = np.quantile(sample_stability, tau_quantile)
    core_idx = np.where(sample_stability >= tau_stab)[0]
    if len(core_idx) < k:
        core_idx = np.argsort(sample_stability)[-k:]
        
    L = min(n_anchors, len(core_idx))
    anchor_idx = rng.choice(core_idx, size=L, replace=False)
    
    # 4. Reduced Bipartite Graph
    B = S[:, anchor_idx]
    
    # Optional beta noise scaling if beta > 0
    if beta > 0:
        noise_penalty = 1.0 - (sample_stability[:, None] * sample_stability[anchor_idx][None, :])
        w_penalty = np.exp(-beta * noise_penalty)
        B = B * w_penalty
        
    row_sums = B.sum(axis=1, keepdims=True)
    row_sums[row_sums < 1e-12] = 1.0
    B_norm = B / row_sums
    
    import scipy.linalg as sla
    W_anchor = B_norm.T @ B_norm
    deg = W_anchor.sum(axis=1)
    deg_inv_sqrt = 1.0 / np.sqrt(np.fmax(deg, 1e-12))
    L_norm = np.eye(L) - (deg_inv_sqrt[:, None] * W_anchor * deg_inv_sqrt[None, :])
    
    evals, evecs = sla.eigh(L_norm)
    V_core = evecs[:, :k]
    
    U_emb = B_norm @ V_core
    emb_norm = np.linalg.norm(U_emb, axis=1, keepdims=True)
    emb_norm[emb_norm < 1e-12] = 1.0
    U_emb /= emb_norm
    
    return run_clusterer("kmeans", U_emb, k, seed=seed)


def run_all_sensitivity_sweeps(n_trials=5):
    print("=" * 80)
    print("EXPERIMENT 4C: HYPERPARAMETER SENSITIVITY & TOPOLOGICAL STABILITY")
    print("=" * 80)
    
    # We evaluate on Leukemia (extreme real-world benchmark: N=72, D=7129, K=2)
    # and a controlled high-D synthetic benchmark (N=300, D=1000, K=3)
    X_leu, y_leu, meta_leu = load_benchmark_dataset("leukemia")
    
    records = []
    
    # 1. Sweep Ensemble Size M in [5, 10, 15, 20, 25, 35, 50, 75, 100]
    m_values = [5, 10, 15, 20, 25, 35, 50, 75, 100]
    print("\n---> Sweeping Ensemble Size M in [5, 100]...")
    for M in m_values:
        for t in range(n_trials):
            seed = 42 + t * 31
            pred = run_icc_parametric(X_leu, k=2, n_base_models=M, seed=seed)
            scores = evaluate_all(y_leu, pred)
            records.append({
                "sweep_type": "ensemble_size_M",
                "param_name": "M",
                "param_value": M,
                "secondary_param": "none",
                "secondary_val": 0,
                "trial": t,
                "ari": scores["ari"],
                "nmi": scores["nmi"],
                "ami": scores["ami"],
                "v_measure": scores["v_measure"],
                "fm_index": scores["fm_index"],
            })
            
    # 2. Sweep 2D Grid: Anchors L x Core Threshold tau
    l_values = [10, 20, 30, 40, 50, 60]
    tau_values = [0.20, 0.35, 0.50, 0.65, 0.80, 0.90]
    print("\n---> Sweeping 2D Grid: Anchors L x Core Threshold tau...")
    for L in l_values:
        for tau in tau_values:
            for t in range(n_trials):
                seed = 42 + t * 31
                pred = run_icc_parametric(X_leu, k=2, n_anchors=L, tau_quantile=tau, seed=seed)
                scores = evaluate_all(y_leu, pred)
                records.append({
                    "sweep_type": "grid_L_vs_tau",
                    "param_name": "L",
                    "param_value": L,
                    "secondary_param": "tau",
                    "secondary_val": tau,
                    "trial": t,
                    "ari": scores["ari"],
                    "nmi": scores["nmi"],
                    "ami": scores["ami"],
                    "v_measure": scores["v_measure"],
                    "fm_index": scores["fm_index"],
                })
                
    # 3. Sweep 2D Grid: Ensemble Size M x Noise Decay beta
    beta_values = [0.0, 0.5, 1.0, 2.0, 4.0, 8.0]
    m_sub = [10, 25, 50]
    print("\n---> Sweeping 2D Grid: Ensemble Size M x Beta...")
    for M in m_sub:
        for beta in beta_values:
            for t in range(n_trials):
                seed = 42 + t * 31
                pred = run_icc_parametric(X_leu, k=2, n_base_models=M, beta=beta, seed=seed)
                scores = evaluate_all(y_leu, pred)
                records.append({
                    "sweep_type": "grid_M_vs_beta",
                    "param_name": "M",
                    "param_value": M,
                    "secondary_param": "beta",
                    "secondary_val": beta,
                    "trial": t,
                    "ari": scores["ari"],
                    "nmi": scores["nmi"],
                    "ami": scores["ami"],
                    "v_measure": scores["v_measure"],
                    "fm_index": scores["fm_index"],
                })
                
    df = pd.DataFrame(records)
    df.to_csv(SENSITIVITY_CSV, index=False)
    print(f"\n[+] Sensitivity results saved to: {SENSITIVITY_CSV}")
    return df


if __name__ == "__main__":
    run_all_sensitivity_sweeps()
