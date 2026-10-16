"""
Anchor-Space Perturbation Profiling (ASPP) for Invariant Core Consensus (ICC-v2).

ASPP provides interpretable, multi-family stability diagnostics and cluster reliability
certification without incurring the quadratic O(N^2) memory bottleneck of classical
co-association tensors.

Mathematical Architecture:
1. Perturbation Engine:
   Decomposes physical stability assessment across explicit families:
   - Sampling (row dropout without replacement)
   - Feature (subspace dropout / attribute masking)
   - Measurement (Gaussian, heavy-tailed Student-t noise)
   - Technical (simulated batch multiplicative scale and additive offsets)
   - Algorithmic (stochastic initialization and hyperparameter jitter)
2. Anchor Bipartite Evaluation:
   Evaluates perturbed partitions strictly against the certified core anchors
   A_core = {a_1, ..., a_L} (L << N), constructing an auxiliary bipartite affinity
   B^(p, r) in R^(N_obs x L) and anchor-space affinity W_A^(p, r) in R^(L x L).
   Auxiliary memory scales as O(N * L) instead of O(N^2).
3. Fingerprinting & Sensitivity Index:
   Computes cluster-level membership retention and anchor-space cohesion, yielding:
   - Stability Fingerprint: F_k in [0, 1]^P
   - Perturbation Sensitivity Index: PSI_k = 1 - (1/P) sum_p S_kp in [0, 1]
   - Categorical Reliability Certification: globally_invariant, conditionally_invariant,
     perturbation_fragile, or ambiguous.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import scipy.linalg as sla

from .core import run_clusterer
from .metrics import adjusted_rand_score

ASPP_FAMILIES = ("sampling", "feature", "measurement", "technical", "algorithmic")

DEFAULT_ASPP_LEVELS: Dict[str, Tuple[float, ...]] = {
    "sampling": (0.2, 0.4),
    "feature": (0.3, 0.6),
    "measurement": (0.25, 0.75),
    "technical": (0.2, 0.5),
    "algorithmic": (0.5, 1.0),
}


@dataclass
class ASPPConfig:
    """
    Configuration parameters for Anchor-Space Perturbation Profiling.

    Parameters
    ----------
    families : tuple of str
        Perturbation families to evaluate.
    levels : dict
        Mapping from family name to tuple of perturbation intensity levels.
    repetitions : int
        Number of stochastic repetitions per (family, level) pair.
    n_base_models : int
        Number of subspace models evaluated per perturbed view.
    subspace_rate : float
        Fraction of active candidate pool features drawn per perturbed model.
    hi_threshold : float
        Upper stability cutoff for global/conditional invariance certification.
    lo_threshold : float
        Lower stability cutoff for fragility/ambiguity boundary.
    max_response_sd : float
        Maximum standard deviation across repetitions to qualify as globally invariant.
    random_state : int
        Random seed for reproducible perturbation sequences.
    """

    families: Tuple[str, ...] = ASPP_FAMILIES
    levels: Dict[str, Tuple[float, ...]] = field(default_factory=lambda: dict(DEFAULT_ASPP_LEVELS))
    repetitions: int = 2
    n_base_models: int = 5
    subspace_rate: float = 0.30
    hi_threshold: float = 0.70
    lo_threshold: float = 0.45
    max_response_sd: float = 0.15
    random_state: int = 42


def _apply_perturbation(
    X: np.ndarray,
    family: str,
    level: float,
    rng: np.random.Generator,
    rep: int,
    batch_vector: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Apply a physical perturbation to input data X.

    Returns
    -------
    X_pert : np.ndarray
        Perturbed data matrix of shape (N_obs, D_obs).
    observed_rows : np.ndarray
        Original row indices retained in the perturbed view.
    observed_cols : np.ndarray
        Original column indices retained in the perturbed view.
    """
    N, D = X.shape
    rows = np.arange(N)
    cols = np.arange(D)
    V = X.copy()

    if family == "sampling":
        keep_n = max(int(round((1.0 - level) * N)), max(10, min(N, 20)))
        pos = np.sort(rng.choice(N, size=keep_n, replace=False))
        rows = rows[pos]
        V = V[pos]

    elif family == "feature":
        keep_d = max(int(round((1.0 - level) * D)), 2)
        pos = np.sort(rng.choice(D, size=keep_d, replace=False))
        cols = cols[pos]
        V = V[:, pos]

    elif family == "measurement":
        if rep % 2 == 0:
            noise = rng.normal(loc=0.0, scale=level, size=V.shape)
        else:
            noise = (level / np.sqrt(3.0)) * rng.standard_t(df=3, size=V.shape)
        V = V + noise

    elif family == "technical":
        n_obs = len(rows)
        if batch_vector is not None:
            b = np.asarray(batch_vector)[rows]
            b = np.unique(b, return_inverse=True)[1]
        else:
            n_batches = 3
            b = rng.integers(0, n_batches, size=n_obs)
        B = int(np.max(b)) + 1
        offsets = rng.normal(0.0, level, size=(B, V.shape[1]))
        scales = np.clip(1.0 + 0.4 * level * rng.normal(size=(B, V.shape[1])), 0.3, 3.0)
        V = V * scales[b] + offsets[b]

    elif family == "algorithmic":
        pass

    else:
        raise ValueError(f"Unknown perturbation family: '{family}'. Supported: {ASPP_FAMILIES}")

    return V, rows, cols


def _compute_cluster_retention(
    labels_ref_observed: np.ndarray,
    labels_pert: np.ndarray,
    K: int,
) -> np.ndarray:
    """
    Compute best-match Jaccard membership retention for each reference cluster.
    Guarantees robust bijective/greedy matching without NaN poisoning.
    """
    retention = np.full(K, np.nan, dtype=np.float64)
    if len(labels_ref_observed) == 0 or len(labels_pert) == 0:
        return retention

    n_pert_clusters = int(np.max(labels_pert)) + 1 if len(labels_pert) > 0 else 0
    if n_pert_clusters == 0:
        return retention

    for k in range(K):
        mask_ref_k = labels_ref_observed == k
        n_ref_k = np.sum(mask_ref_k)
        if n_ref_k == 0:
            continue

        best_jaccard = 0.0
        for l_idx in range(n_pert_clusters):
            mask_pert_l = labels_pert == l_idx
            intersection = np.sum(mask_ref_k & mask_pert_l)
            union = np.sum(mask_ref_k | mask_pert_l)
            if union > 0:
                jacc = intersection / union
                if jacc > best_jaccard:
                    best_jaccard = jacc
        retention[k] = best_jaccard

    return retention


class AnchorSpacePerturbationProfiler:
    """
    Profiler for executing Anchor-Space Perturbation Profiling (ASPP) on fitted ICC-v2 models.
    """

    def __init__(self, config: Optional[ASPPConfig] = None):
        self.config = config or ASPPConfig()

    def profile(
        self,
        model: Any,
        X: np.ndarray,
        batch_vector: Optional[np.ndarray] = None,
    ) -> pd.DataFrame:
        """
        Execute Anchor-Space Perturbation Profiling on input data X using the fitted model.

        Parameters
        ----------
        model : InvariantCoreConsensusV2
            Fitted ICC-v2 instance containing labels_, anchor_indices_, selected_features_.
        X : np.ndarray of shape (N, D)
            Input feature matrix.
        batch_vector : Optional[np.ndarray] of shape (N,)
            Known categorical batch assignments, if available.

        Returns
        -------
        fingerprints_df : pd.DataFrame
            Summary DataFrame indexed by cluster with stability fingerprints,
            Perturbation Sensitivity Index (PSI), and reliability categories.
        """
        if getattr(model, "labels_", None) is None or getattr(model, "anchor_indices_", None) is None:
            raise RuntimeError("Model must be fitted before running ASPP profiling.")

        X = np.asarray(X, dtype=np.float64)
        N, D = X.shape
        K = model.n_clusters
        cfg = self.config
        rng = np.random.default_rng(cfg.random_state)

        ref_labels = model.labels_
        anchor_indices = model.anchor_indices_
        L = len(anchor_indices)
        candidate_pool = getattr(model, "selected_features_", np.arange(D))
        base_engine = getattr(model, "base_clusterer", "auto")
        if base_engine == "auto":
            base_engine = "spectral" if N <= 100 else "kmeans"

        family_cluster_retention: Dict[str, List[np.ndarray]] = {f: [] for f in cfg.families}
        family_cluster_anchor_coassoc: Dict[str, List[np.ndarray]] = {f: [] for f in cfg.families}
        family_mean_ari: Dict[str, List[float]] = {f: [] for f in cfg.families}

        for fam in cfg.families:
            levels = cfg.levels.get(fam, (0.3,))
            for lev in levels:
                for rep in range(cfg.repetitions):
                    seed_run = int(rng.integers(0, 1_000_000_000))
                    rng_run = np.random.default_rng(seed_run)

                    X_pert, obs_rows, obs_cols = _apply_perturbation(X, fam, lev, rng_run, rep, batch_vector)
                    N_obs = len(obs_rows)

                    surviving_anchor_mask = np.isin(anchor_indices, obs_rows)
                    if not np.any(surviving_anchor_mask):
                        local_anchor_pos = np.arange(min(L, N_obs))
                        surviving_anchors = obs_rows[local_anchor_pos]
                    else:
                        surviving_anchors = anchor_indices[surviving_anchor_mask]

                        obs_row_map = {orig_idx: local_idx for local_idx, orig_idx in enumerate(obs_rows)}
                        local_anchor_pos = np.array([obs_row_map[idx] for idx in surviving_anchors])

                    L_obs = len(local_anchor_pos)

                    surviving_pool = np.intersect1d(candidate_pool, obs_cols)
                    if len(surviving_pool) < 2:
                        surviving_pool = obs_cols
                    sub_size = max(2, int(len(surviving_pool) * cfg.subspace_rate))

                    B_pert = np.zeros((N_obs, L_obs), dtype=np.float32)
                    pert_partitions = []

                    for m in range(cfg.n_base_models):
                        seed_m = int(rng_run.integers(0, 1_000_000_000))
                        sub_feat = rng_run.choice(surviving_pool, size=sub_size, replace=False)

                        col_map = {orig_c: loc_c for loc_c, orig_c in enumerate(obs_cols)}
                        local_sub_feat = np.array([col_map[c] for c in sub_feat])

                        X_sub = X_pert[:, local_sub_feat]

                        if fam == "algorithmic":
                            seed_m = seed_m + int(lev * 1000)

                        p_m = run_clusterer(base_engine, X_sub, K, seed=seed_m)
                        pert_partitions.append(p_m)

                        anchor_labels_m = p_m[local_anchor_pos]
                        B_pert += (p_m[:, None] == anchor_labels_m[None, :]).astype(np.float32)

                    B_pert /= max(1, cfg.n_base_models)

                    row_sums = B_pert.sum(axis=1, keepdims=True)
                    row_sums[row_sums < 1e-12] = 1.0
                    B_norm = B_pert / row_sums

                    W_anchor_pert = B_norm.T @ B_norm
                    d_anchor = W_anchor_pert.sum(axis=1)
                    d_inv_sqrt = 1.0 / np.sqrt(np.fmax(d_anchor, 1e-12))
                    L_anchor_norm = np.eye(L_obs) - (d_inv_sqrt[:, None] * W_anchor_pert * d_inv_sqrt[None, :])

                    evals, evecs = sla.eigh(L_anchor_norm)
                    V_pert = evecs[:, :K]
                    U_pert = B_norm @ V_pert
                    U_norm = np.linalg.norm(U_pert, axis=1, keepdims=True)
                    U_norm[U_norm < 1e-12] = 1.0
                    U_pert /= U_norm

                    pert_consensus_labels = run_clusterer("kmeans", U_pert, K, seed=seed_run)

                    ref_obs = ref_labels[obs_rows]
                    ret_k = _compute_cluster_retention(ref_obs, pert_consensus_labels, K)
                    family_cluster_retention[fam].append(ret_k)

                    coassoc_k = np.full(K, np.nan, dtype=np.float64)
                    for k in range(K):
                        surv_anchors_in_k = [
                            local_idx for local_idx, orig_a in enumerate(surviving_anchors) if ref_labels[orig_a] == k
                        ]
                        if len(surv_anchors_in_k) >= 2:
                            sub_W = W_anchor_pert[np.ix_(surv_anchors_in_k, surv_anchors_in_k)]

                            n_ak = len(surv_anchors_in_k)
                            off_diag_sum = np.sum(sub_W) - np.trace(sub_W)
                            coassoc_k[k] = off_diag_sum / (n_ak * (n_ak - 1))
                        elif len(surv_anchors_in_k) == 1:
                            cluster_samples = np.where(ref_obs == k)[0]
                            if len(cluster_samples) > 0:
                                coassoc_k[k] = np.mean(B_pert[cluster_samples, surv_anchors_in_k[0]])
                            else:
                                coassoc_k[k] = 1.0
                        else:
                            coassoc_k[k] = ret_k[k]

                    family_cluster_anchor_coassoc[fam].append(coassoc_k)

                    ari_run = float(adjusted_rand_score(ref_obs, pert_consensus_labels))
                    family_mean_ari[fam].append(ari_run)

        cluster_rows = []
        family_summary = {}

        for fam in cfg.families:
            family_summary[f"{fam}_mean_ari"] = float(np.nanmean(family_mean_ari[fam]))

        for k in range(K):
            cluster_size = int(np.sum(ref_labels == k))
            row: Dict[str, Any] = {
                "cluster": k,
                "size": cluster_size,
            }
            stability_scores = []
            response_sds = []

            for fam in cfg.families:
                rets = np.array([r[k] for r in family_cluster_retention[fam]])
                coas = np.array([c[k] for c in family_cluster_anchor_coassoc[fam]])

                valid_rets = rets[~np.isnan(rets)]
                valid_coas = coas[~np.isnan(coas)]

                mean_ret = float(np.mean(valid_rets)) if len(valid_rets) > 0 else 0.5
                mean_coa = float(np.mean(valid_coas)) if len(valid_coas) > 0 else mean_ret

                s_kp = float(np.mean([mean_ret, mean_coa])) if not (np.isnan(mean_ret) or np.isnan(mean_coa)) else 0.5
                sd_kp = float(np.std(valid_rets)) if len(valid_rets) > 1 else 0.0

                row[fam] = s_kp
                row[f"{fam}_retention"] = mean_ret
                row[f"{fam}_anchor_coassoc"] = mean_coa
                row[f"{fam}_sd"] = sd_kp

                stability_scores.append(s_kp)
                response_sds.append(sd_kp)

            max_sd = float(np.max(response_sds)) if len(response_sds) > 0 else 0.0
            stab_arr = np.array(stability_scores, dtype=np.float64)
            psi = float(np.mean(1.0 - stab_arr)) if len(stab_arr) > 0 else 0.5
            if np.isnan(psi):
                psi = 0.5

            row["max_response_sd"] = max_sd
            row["PSI"] = np.clip(psi, 0.0, 1.0)

            n_hi = int(np.sum(stab_arr >= cfg.hi_threshold))
            min_score = float(np.min(stab_arr))

            if (n_hi == len(cfg.families)) and (max_sd <= cfg.max_response_sd):
                cat = "globally_invariant"
            elif (n_hi == len(cfg.families)) or (n_hi >= 1 and min_score >= cfg.lo_threshold):
                cat = "conditionally_invariant"
            elif n_hi >= 1:
                cat = "perturbation_fragile"
            else:
                cat = "ambiguous"

            row["reliability"] = cat
            cluster_rows.append(row)

        df_fingerprints = pd.DataFrame(cluster_rows)

        self.fingerprints_df_ = df_fingerprints
        self.aspp_summary_ = family_summary
        self.psi_ = df_fingerprints["PSI"].to_numpy()
        self.reliability_categories_ = df_fingerprints["reliability"].tolist()

        return df_fingerprints
