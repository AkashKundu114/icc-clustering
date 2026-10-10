"""
Experiment 2 Engine: Component-Wise Ablation of Invariant Core Consensus.

Systematically evaluates 6 ablation variants to isolate the individual
and compound contributions of:
1. Variance-Guided Subspace Gating (SSG)
2. Feature-Reliability Noise Calibration (w_il = exp(-beta * q_il))
3. Invariant Core Anchor Selection (U_core via 2D (C, R) filtering)
"""

from pathlib import Path
import numpy as np
import scipy.linalg as sla
from scipy.spatial.distance import cdist

# Import core helpers from root src package
import sys
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.icc.core import run_clusterer, adjusted_rand_score


def normalized_mutual_info(y_true, y_pred):
    """Vectorized Normalized Mutual Information (NMI) in [0, 1]."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    n = len(y_true)
    classes, c_idx = np.unique(y_true, return_inverse=True)
    clusters, cl_idx = np.unique(y_pred, return_inverse=True)
    contingency = np.zeros((len(classes), len(clusters)), dtype=float)
    np.add.at(contingency, (c_idx, cl_idx), 1.0)
    p_ij = contingency / n
    p_i = p_ij.sum(axis=1)
    p_j = p_ij.sum(axis=0)

    h_u = -np.sum(p_i * np.log(p_i + 1e-12))
    h_v = -np.sum(p_j * np.log(p_j + 1e-12))

    denom = p_i[:, None] * p_j[None, :]
    mask = p_ij > 0
    mi = np.sum(p_ij[mask] * np.log(p_ij[mask] / (denom[mask] + 1e-12)))

    if h_u + h_v == 0:
        return 1.0
    return float(2.0 * mi / (h_u + h_v))


def run_icc_variant(
    X,
    k=3,
    use_subspaces=True,
    use_noise_calibration=True,
    use_core_anchors=True,
    n_base_models=20,
    n_anchors=60,
    subspace_rate=0.25,
    beta=2.0,
    seed=42
):
    """
    Executes a specific ablation variant of Invariant Core Consensus.
    """
    N, D = X.shape
    rng = np.random.default_rng(seed)

    # 1. Candidate Anchor Seeding (Random projection + k-means++)
    d_proj = min(30, D)
    proj_matrix = rng.normal(size=(D, d_proj)) / np.sqrt(d_proj)
    X_proj = X @ proj_matrix

    anchor_indices = [rng.choice(N)]
    for _ in range(1, min(n_anchors, N)):
        dist_sq = np.min(cdist(X_proj, X_proj[anchor_indices], metric='sqeuclidean'), axis=1)
        dist_sq[anchor_indices] = 0.0
        prob = dist_sq / (dist_sq.sum() + 1e-12)
        anchor_indices.append(rng.choice(N, p=prob))

    anchor_indices = np.array(anchor_indices, dtype=int)
    anchors = X[anchor_indices]  # (L, D)
    L = len(anchor_indices)

    # 2. Base Model Training (Subspaces vs Full Space)
    var_features = np.var(X, axis=0)
    p_features = var_features / (np.sum(var_features) + 1e-12)
    n_active = max(2, int(D * subspace_rate)) if use_subspaces else D

    gates = []
    partitions = []
    anchor_partitions = []

    for m in range(n_base_models):
        seed_m = seed + m * 37
        if use_subspaces and D > 2:
            active_idx = rng.choice(D, size=n_active, replace=False, p=p_features)
            gate = np.zeros(D, dtype=float)
            gate[active_idx] = 1.0
            X_sub = X[:, active_idx]
            anchors_sub = anchors[:, active_idx]
        else:
            gate = np.ones(D, dtype=float)
            X_sub = X
            anchors_sub = anchors

        gates.append(gate)
        lab = run_clusterer("kmeans", X_sub, k, seed=seed_m)
        partitions.append(lab)

        # Map anchors to clusters
        centroids = np.array([X_sub[lab == c].mean(axis=0) if np.any(lab == c) else X_sub[c] for c in range(k)])
        anchor_lab = np.argmin(cdist(anchors_sub, centroids, metric='sqeuclidean'), axis=1)
        anchor_partitions.append(anchor_lab)

    gates = np.array(gates)

    # 3. Construct Anchor Bipartite Matrix (Calibrated vs Uncalibrated)
    B_num = np.zeros((N, L), dtype=float)
    B_den = np.zeros((N, L), dtype=float) + 1e-8
    total_dist_sq = cdist(X, anchors, metric='sqeuclidean') + 1e-12

    for m in range(n_base_models):
        p_m = partitions[m]
        p_anc_m = anchor_partitions[m]
        H_m = (p_m[:, None] == p_anc_m[None, :]).astype(float)

        if use_noise_calibration and use_subspaces and D > 2:
            noise_gate = 1.0 - gates[m]
            noise_dist_sq = cdist(X * noise_gate, anchors * noise_gate, metric='sqeuclidean')
            q_m = noise_dist_sq / total_dist_sq
            w_m = np.exp(-beta * q_m)
        else:
            # Uniform unweighted voting
            w_m = 1.0

        B_num += w_m * H_m
        B_den += w_m

    B_star = B_num / B_den

    # 4. Core Anchor Certification (Filtered vs Unfiltered)
    if use_core_anchors:
        C = 1.0 - 4.0 * np.mean((B_star - 0.5)**2, axis=1)
        mean_noise_gate = np.mean(1.0 - gates, axis=0) if use_subspaces else np.zeros(D)
        R = np.sum(X**2 * mean_noise_gate, axis=1) / (np.sum(X**2, axis=1) + 1e-12)

        tau_R = np.quantile(R, 0.70)
        tau_C = np.quantile(C[R <= tau_R], 0.50) if np.any(R <= tau_R) else np.median(C)
        is_core = (C >= tau_C) & (R <= tau_R)

        core_anchor_mask = is_core[anchor_indices]
        core_anchors = np.where(core_anchor_mask)[0]

        if len(core_anchors) < k:
            core_anchors = np.argsort(C[anchor_indices] * (1.0 - R[anchor_indices]))[-k:]
    else:
        # Use all candidate anchors without filtering
        core_anchors = np.arange(L)

    L_c = len(core_anchors)

    # 5. Reduced Spectral Graph Decomposition
    B_core = B_star[:, core_anchors]
    row_sums = B_core.sum(axis=1, keepdims=True)
    row_sums[row_sums < 1e-12] = 1.0
    B_norm = B_core / row_sums

    W_core = B_norm.T @ B_norm  # (L_c x L_c)
    d_vec = W_core.sum(axis=1)
    d_inv_sqrt = 1.0 / np.sqrt(np.fmax(d_vec, 1e-12))
    L_sym = np.eye(L_c) - (d_inv_sqrt[:, None] * W_core * d_inv_sqrt[None, :])

    evals, evecs = sla.eigh(L_sym)
    V_core = evecs[:, :k]

    U_emb = B_norm @ V_core
    emb_norm = np.linalg.norm(U_emb, axis=1, keepdims=True)
    emb_norm[emb_norm < 1e-12] = 1.0
    U_emb /= emb_norm

    final_labels = run_clusterer("kmeans", U_emb, k, seed=seed)
    return final_labels, L_c
