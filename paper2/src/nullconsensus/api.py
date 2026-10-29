"""
Top-level Scikit-Learn Compatible Estimator for nullconsensus.
"""

import numpy as np
from sklearn.base import BaseEstimator, ClusterMixin
from sklearn.cluster import KMeans
from typing import Optional, Dict, Any

from nullconsensus.methods.nullgate import NullGateFeatureSelector
from nullconsensus.methods.hurdlegate import HurdleGateFeatureSelector

class NullConsensus(BaseEstimator, ClusterMixin):
    """
    Permutation-Null Calibrated Consensus Clustering (NullConsensus).
    
    Parameters:
        n_clusters: Target number of clusters (K).
        n_base_models: Number of base partitions in the ensemble (M). Default: 25.
        n_anchors: Number of landmark anchors (L). Default: 40.
        subspace_fraction: Fraction of features sampled per base model (alpha). Default: 0.15.
        mode: Feature gating mode ('permutation_null', 'hurdle', 'uniform'). Default: 'permutation_null'.
        temperature: Softmax temperature for saliency-weighted subspace sampling. Default: 1.0.
        n_null_permutations: Number of permutation shuffles per feature. Default: 10.
        random_state: Random seed for deterministic reproducibility.
    """
    def __init__(
        self,
        n_clusters: int = 3,
        n_base_models: int = 25,
        n_anchors: int = 40,
        subspace_fraction: float = 0.15,
        mode: str = "permutation_null",
        temperature: float = 1.0,
        n_null_permutations: int = 10,
        random_state: int = 42
    ):
        self.n_clusters = n_clusters
        self.n_base_models = n_base_models
        self.n_anchors = n_anchors
        self.subspace_fraction = subspace_fraction
        self.mode = mode
        self.temperature = temperature
        self.n_null_permutations = n_null_permutations
        self.random_state = random_state
        
        # Fitted attributes
        self.labels_: Optional[np.ndarray] = None
        self.centroids_: Optional[np.ndarray] = None
        self.active_features_: Optional[np.ndarray] = None
        self.feature_weights_: Optional[np.ndarray] = None

    def fit(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> "NullConsensus":
        X = np.asarray(X, dtype=float)
        N, D = X.shape
        rng = np.random.default_rng(self.random_state)
        
        # 1. Feature Saliency Weighting
        if self.mode == "permutation_null":
            selector = NullGateFeatureSelector(
                n_permutations=self.n_null_permutations,
                random_state=self.random_state
            )
            selector.fit(X, temperature=self.temperature)
            sampling_probs = selector.sampling_probs_
            self.feature_weights_ = selector.saliency_scores_
        elif self.mode == "hurdle":
            selector = HurdleGateFeatureSelector(random_state=self.random_state)
            selector.fit(X, temperature=self.temperature)
            sampling_probs = selector.sampling_probs_
            self.feature_weights_ = selector.hurdle_scores_
        else: # uniform
            sampling_probs = np.ones(D) / D
            self.feature_weights_ = np.ones(D)
            
        # Top active features pool
        n_pool = max(2, int(np.ceil(self.subspace_fraction * D)))
        self.active_features_ = np.argsort(-self.feature_weights_)[:n_pool]
        
        # 2. Select L Landmark Anchors
        L = min(self.n_anchors, N)
        anchor_idx = rng.choice(N, size=L, replace=False)
        
        # 3. Generate Base Ensemble Partitions
        n_sub = max(2, int(np.ceil(self.subspace_fraction * D)))
        # Rectangular bipartite co-association matrix B: N x L
        B = np.zeros((N, L), dtype=float)
        
        for m in range(self.n_base_models):
            sub_seed = rng.integers(0, 1000000)
            # Soft saliency-weighted sampling
            sub_feats = rng.choice(D, size=n_sub, replace=False, p=sampling_probs)
            X_sub = X[:, sub_feats]
            
            # Base clustering
            km = KMeans(n_clusters=self.n_clusters, n_init=1, random_state=sub_seed)
            base_labels = km.fit_predict(X_sub)
            
            # Co-association with landmark anchors
            anchor_labels = base_labels[anchor_idx]
            # Outer equality matrix: N x L
            match_matrix = (base_labels[:, None] == anchor_labels[None, :]).astype(float)
            B += match_matrix / self.n_base_models

        # 4. Bipartite Transfer-Cut Spectral Embedding
        # Node degrees
        dx = np.sum(B, axis=1) # N
        dy = np.sum(B, axis=0) # L
        dx[dx < 1e-12] = 1e-12
        dy[dy < 1e-12] = 1e-12
        
        Dx_inv_sqrt = np.diag(1.0 / np.sqrt(dx))
        Dy_inv = np.diag(1.0 / dy)
        
        # SVD of normalized bipartite matrix: S = Dx^(-1/2) * B * Dy^(-1/2)
        Dy_inv_sqrt = np.diag(1.0 / np.sqrt(dy))
        S = Dx_inv_sqrt @ B @ Dy_inv_sqrt
        
        # SVD
        try:
            U, s, Vt = np.linalg.svd(S, full_matrices=False)
            k_eff = min(self.n_clusters, U.shape[1])
            embeddings = U[:, :k_eff]
            # Normalize embedding rows
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            norms[norms < 1e-12] = 1e-12
            embeddings = embeddings / norms
        except Exception:
            embeddings = B[:, :min(self.n_clusters, L)]

        # Final consensus clustering on spectral embedding
        final_km = KMeans(n_clusters=self.n_clusters, n_init=10, random_state=self.random_state)
        self.labels_ = final_km.fit_predict(embeddings)
        
        # 5. Compute Active Subspace Centroids for Inductive Inference
        self.centroids_ = np.zeros((self.n_clusters, len(self.active_features_)))
        for k in range(self.n_clusters):
            mask = (self.labels_ == k)
            if np.any(mask):
                self.centroids_[k] = np.mean(X[mask][:, self.active_features_], axis=0)
            else:
                self.centroids_[k] = np.mean(X[:, self.active_features_], axis=0)
                
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Projects out-of-sample query instances to nearest active centroids in O(K * |F_active|) time.
        """
        X = np.asarray(X, dtype=float)
        X_active = X[:, self.active_features_]
        
        # Distance to centroids: (N_query, K)
        # ||x - c||^2 = ||x||^2 - 2 x c^T + ||c||^2
        dists = np.zeros((len(X), self.n_clusters))
        for k in range(self.n_clusters):
            dists[:, k] = np.sum((X_active - self.centroids_[k]) ** 2, axis=1)
            
        return np.argmin(dists, axis=1)

    def fit_predict(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> np.ndarray:
        self.fit(X, y)
        return self.labels_
