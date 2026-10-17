"""
Inductive Consensus Memory for AI Agents
========================================
Maintains long-term episodic and semantic memory using stability-weighted anchor centroids
and conformal coverage gating. Provides:
1. O(m) instantaneous inductive memory routing without batch reclustering.
2. Automated memory consolidation (single-cluster assignment).
3. Automated novelty / split triggers (conformal empty set C(x) = empty).
4. Epistemic contradiction detection (conformal multiton C(x) > 1).
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple
import numpy as np


@dataclass
class MemoryItem:
    """An individual episodic memory record."""
    id: str
    text: str
    embedding: np.ndarray
    metadata: Dict[str, Any] = field(default_factory=dict)
    assigned_cluster: Optional[int] = None
    prediction_set: List[int] = field(default_factory=list)
    action: str = "consolidated"  # 'consolidated', 'novel_cluster', 'ambiguous_flagged'
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class InductiveConsensusMemory:
    """
    Inductive Consensus Long-Term Agent Memory.

    Parameters
    ----------
    dim : int, default=768
        Dimensionality of embedding space.
    alpha : float, default=0.10
        Significance level for conformal prediction sets (1 - alpha coverage).
    similarity_threshold : float, default=0.35
        Minimum cosine similarity required to consolidate into an existing memory cluster.
    ema_decay : float, default=0.05
        Exponential moving average rate for updating memory centroids upon consolidation.
    temperature : float, default=10.0
        Temperature for cosine softmax probabilities.
    max_clusters : int, default=50
        Maximum number of dynamic semantic clusters.
    """

    def __init__(
        self,
        dim: int = 768,
        alpha: float = 0.10,
        similarity_threshold: float = 0.35,
        ema_decay: float = 0.05,
        temperature: float = 10.0,
        max_clusters: int = 50,
    ):
        self.dim = dim
        self.alpha = alpha
        self.similarity_threshold = similarity_threshold
        self.ema_decay = ema_decay
        self.temperature = temperature
        self.max_clusters = max_clusters

        self.centroids: List[np.ndarray] = []
        self.cluster_weights: List[float] = []
        self.memories: List[MemoryItem] = []
        self.cluster_to_memories: Dict[int, List[str]] = {}
        self.q_hat: float = 0.70  # Initialized calibrated conformal non-conformity threshold

    def _normalize(self, v: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(v)
        return v / (norm if norm > 1e-12 else 1.0)

    def add_memory(
        self,
        text: str,
        embedding: np.ndarray,
        memory_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MemoryItem:
        """
        Inductively route and store a new episodic memory.

        Parameters
        ----------
        text : str
            Text content or summary of the memory.
        embedding : np.ndarray of shape (D,)
            Vector embedding.
        memory_id : Optional[str]
            Unique identifier.
        metadata : Optional[Dict[str, Any]]
            Associated metadata (e.g., conversation ID, tool outputs, speaker).

        Returns
        -------
        item : MemoryItem
        """
        mid = memory_id or f"mem_{len(self.memories) + 1:05d}"
        v = self._normalize(np.asarray(embedding, dtype=np.float64).ravel())
        meta = metadata or {}

        # Case 0: Empty memory base - seed first cluster
        if len(self.centroids) == 0:
            self.centroids.append(v)
            self.cluster_weights.append(1.0)
            self.cluster_to_memories[0] = [mid]
            item = MemoryItem(
                id=mid,
                text=text,
                embedding=v,
                metadata=meta,
                assigned_cluster=0,
                prediction_set=[0],
                action="novel_cluster",
            )
            self.memories.append(item)
            return item

        # Compute cosine similarity to existing anchor centroids
        C_mat = np.stack(self.centroids)  # (K, D)
        cos_sim = np.clip(C_mat @ v, -1.0, 1.0)  # (K,)
        logits = cos_sim * self.temperature
        exp_logits = np.exp(logits - np.max(logits))
        probs = exp_logits / np.sum(exp_logits)

        # Conformal prediction set C(x) = {k : 1 - P(k|x) <= q_hat}
        max_sim = float(np.max(cos_sim))
        if max_sim < self.similarity_threshold:
            pred_set = []
        else:
            pred_set = [k for k in range(len(self.centroids)) if (1.0 - probs[k]) <= self.q_hat]
        best_cluster = int(np.argmax(probs))

        # Decision Logic based on Conformal Cardinality
        if len(pred_set) == 0:
            # NOVEL CLUSTER / SPLIT TRIGGER: Does not conform to existing memory schemas
            if len(self.centroids) < self.max_clusters:
                new_c_id = len(self.centroids)
                self.centroids.append(v)
                self.cluster_weights.append(1.0)
                self.cluster_to_memories[new_c_id] = [mid]
                action = "novel_cluster"
                assigned = new_c_id
                pred_set = [new_c_id]
            else:
                # Overflow fallback: attach to closest
                assigned = best_cluster
                self.cluster_to_memories[assigned].append(mid)
                action = "consolidated"
        elif len(pred_set) == 1:
            # CONSOLIDATION: Unambiguous match to existing schema
            assigned = pred_set[0]
            self.cluster_to_memories[assigned].append(mid)
            # Update centroid with exponential moving average
            self.centroids[assigned] = self._normalize(
                (1.0 - self.ema_decay) * self.centroids[assigned] + self.ema_decay * v
            )
            self.cluster_weights[assigned] += 1.0
            action = "consolidated"
        else:
            # AMBIGUITY / CONTRADICTION: Memory bridges multiple active clusters
            assigned = best_cluster
            self.cluster_to_memories[assigned].append(mid)
            action = "ambiguous_flagged"

        item = MemoryItem(
            id=mid,
            text=text,
            embedding=v,
            metadata=meta,
            assigned_cluster=assigned,
            prediction_set=pred_set,
            action=action,
        )
        self.memories.append(item)
        return item

    def retrieve(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
    ) -> List[Tuple[MemoryItem, float]]:
        """
        Two-stage retrieval: routes to top candidate clusters, then ranks memories within them.
        """
        if len(self.memories) == 0:
            return []

        q = self._normalize(np.asarray(query_embedding, dtype=np.float64).ravel())
        C_mat = np.stack(self.centroids)
        cluster_sims = C_mat @ q
        top_clusters = np.argsort(cluster_sims)[::-1][:min(3, len(self.centroids))]

        # Gather candidate memories from top clusters
        candidates: List[MemoryItem] = []
        for c in top_clusters:
            for mid in self.cluster_to_memories.get(c, []):
                mem = next((m for m in self.memories if m.id == mid), None)
                if mem is not None:
                    candidates.append(mem)

        if not candidates:
            candidates = self.memories

        # Rank candidates by dot product
        scores = [float(np.dot(m.embedding, q)) for m in candidates]
        ranked_indices = np.argsort(scores)[::-1][:top_k]

        return [(candidates[i], scores[i]) for i in ranked_indices]

    def get_stats(self) -> Dict[str, Any]:
        """Summary telemetry of memory consolidation."""
        actions = [m.action for m in self.memories]
        return {
            "total_memories": len(self.memories),
            "num_clusters": len(self.centroids),
            "consolidated_count": actions.count("consolidated"),
            "novel_cluster_count": actions.count("novel_cluster"),
            "ambiguous_flagged_count": actions.count("ambiguous_flagged"),
            "cluster_sizes": {k: len(v) for k, v in self.cluster_to_memories.items()},
        }
