"""
Experiment 2 Engine: Rigorous Component-Wise Ablation of Invariant Core Consensus.

Systematically evaluates 6 modular ablation variants to isolate the individual
and compound contributions of:
1. Variance-Stabilized Subspace Gating (VSSG - Sarle's Bimodality screening)
2. Subspace Consensus Ensembling
3. Direct vs Bipartite Anchor Graph Construction
4. Statistical Determinacy Core Anchor Certification

Architectural Variants:
- V0_Standard_Consensus: Ambient dense co-association consensus (No VSSG, dense NxN co-association, average linkage).
- V1_VSSG_KMeans: Control 1: VSSG candidate feature screening followed by direct K-Means (no ensemble, no anchors).
- V2_VSSG_StdConsensus: Control 2: VSSG candidate feature screening followed by dense co-association consensus.
- V3_Anchors_Only: Invariant Core Anchor Consensus on full ambient features (No VSSG).
- V4_VSSG_Random_Anchors: VSSG candidate screening + Anchor consensus with uniformly random anchors (No core determinacy certification).
- V5_Full_ICC_v2: Full ICC-v2 (VSSG + Determinacy Core Certified Anchors + Bipartite Transfer-Cut).
"""

from pathlib import Path
from typing import Tuple, Dict, Any
import numpy as np

# Import core helpers from root src package
import sys
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.icc.core import run_clusterer, adjusted_rand_score
from src.icc.baselines.consensus import run_standard_consensus, run_icc_v1
from src.icc.consensus_v2 import InvariantCoreConsensusV2


def extract_vssg_candidate_features(X: np.ndarray, k: int, threshold: float = 5.0 / 9.0) -> np.ndarray:
    """
    Extracts candidate features passing Sarle's Bimodality Coefficient threshold (BC >= 5/9).
    Falls back to top min(D, max(2, k)) if fewer features exceed the threshold.
    """
    N, D = X.shape
    m1 = np.mean(X, axis=0)
    m2 = np.mean((X - m1) ** 2, axis=0)
    m3 = np.mean((X - m1) ** 3, axis=0)
    m4 = np.mean((X - m1) ** 4, axis=0)

    valid_mask = m2 > 1e-12
    sk = np.zeros(D, dtype=np.float64)
    kurt = np.zeros(D, dtype=np.float64)
    sk[valid_mask] = m3[valid_mask] / (m2[valid_mask] ** 1.5)
    kurt[valid_mask] = m4[valid_mask] / (m2[valid_mask] ** 2.0) - 3.0

    finite_corr = 3.0 * ((N - 1) ** 2) / ((N - 2) * (N - 3)) if N >= 4 else 3.0
    denom = kurt + finite_corr + 1e-5
    denom = np.fmax(denom, 1e-5)
    bimodal = np.zeros(D, dtype=np.float64)
    bimodal[valid_mask] = (sk[valid_mask] ** 2 + 1.0) / denom[valid_mask]

    passing_indices = np.where(bimodal >= threshold)[0]
    min_features = min(2, D)
    max_pool = min(D, max(100, int(0.15 * D)))

    if len(passing_indices) >= min_features:
        if len(passing_indices) <= max_pool:
            return passing_indices
        top_pass = np.argsort(bimodal[passing_indices])[-max_pool:]
        return passing_indices[top_pass]

    return np.argsort(bimodal)[-min(D, max(2, k)):]


def run_icc_variant(
    X: np.ndarray,
    k: int = 3,
    variant_name: str = "V5_Full_ICC_v2",
    n_base_models: int = 20,
    n_anchors: int = 40,
    subspace_rate: float = 0.30,
    seed: int = 42,
) -> Tuple[np.ndarray, int]:
    """
    Executes a specific modular ablation variant of Invariant Core Consensus.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
    k : int, default=3
    variant_name : str
        One of {'V0_Standard_Consensus', 'V1_VSSG_KMeans', 'V2_VSSG_StdConsensus',
                'V3_Anchors_Only', 'V4_VSSG_Random_Anchors', 'V5_Full_ICC_v2'}
    n_base_models : int, default=20
    n_anchors : int, default=40
    subspace_rate : float, default=0.30
    seed : int, default=42

    Returns
    -------
    labels : np.ndarray of shape (N,)
    n_core_anchors : int
    """
    N, D = X.shape

    if variant_name == "V0_Standard_Consensus":
        # Raw ambient dense consensus (no VSSG, no anchors)
        preds, _, meta = run_standard_consensus(X, k=k, n_base_models=n_base_models, seed=seed)
        return preds, N

    elif variant_name == "V1_VSSG_KMeans":
        # Control 1: VSSG candidate feature screening followed by direct K-Means
        vssg_idx = extract_vssg_candidate_features(X, k=k)
        X_sub = X[:, vssg_idx]
        preds = run_clusterer("kmeans", X_sub, k, seed=seed)
        return preds, 0

    elif variant_name == "V2_VSSG_StdConsensus":
        # Control 2: VSSG candidate feature screening followed by dense co-association consensus
        vssg_idx = extract_vssg_candidate_features(X, k=k)
        X_sub = X[:, vssg_idx]
        preds, _, meta = run_standard_consensus(X_sub, k=k, n_base_models=n_base_models, seed=seed)
        return preds, N

    elif variant_name == "V3_Anchors_Only":
        # Invariant Core Anchor Consensus on full ambient features (no VSSG)
        preds, _, meta = run_icc_v1(X, k=k, n_base_models=n_base_models, n_anchors=n_anchors, seed=seed)
        return preds, int(meta.get("n_anchors", int(meta)))

    elif variant_name == "V4_VSSG_Random_Anchors":
        # VSSG screening + Anchor bipartite consensus with uniform random anchors (no determinacy core certification)
        model = InvariantCoreConsensusV2(
            n_clusters=k,
            n_base_models=n_base_models,
            n_anchors=n_anchors,
            subspace_rate=subspace_rate,
            core_quantile=0.0,  # All points eligible as anchors
            random_state=seed,
        )
        preds = model.fit_predict(X)
        return preds, len(model.anchor_indices_)

    elif variant_name == "V5_Full_ICC_v2":
        # Full ICC-v2: VSSG + Determinacy Core Certified Anchors + Bipartite Transfer-Cut
        model = InvariantCoreConsensusV2(
            n_clusters=k,
            n_base_models=n_base_models,
            n_anchors=n_anchors,
            subspace_rate=subspace_rate,
            core_quantile=0.50,  # Certified determinacy core
            random_state=seed,
        )
        preds = model.fit_predict(X)
        return preds, len(model.core_indices_)

    else:
        raise ValueError(f"Unknown ablation variant: {variant_name}")
