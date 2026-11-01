"""
Integration test for dataset loading, preprocessing, consensus clustering, and metric computation.
"""

import numpy as np

from icc.consensus import InvariantCoreConsensusV2
from icc.data.preprocessing import build_dataset
from icc.evaluation.metrics import evaluate_all


def test_full_clustering_pipeline():
    # 1. Dataset generation
    X, y_true = build_dataset(
        n_per_cluster=30,
        k=3,
        signal_dim=2,
        noise_dim=50,
        seed=42,
    )
    assert X.shape == (90, 52)
    assert len(y_true) == 90

    # 2. Consensus model fit & prediction
    model = InvariantCoreConsensusV2(
        n_clusters=3,
        n_base_models=15,
        n_anchors=30,
        random_state=42,
    )
    labels = model.fit_predict(X)

    # 3. Validation
    assert len(labels) == 90
    assert len(np.unique(labels)) == 3

    # 4. Evaluation metrics
    metrics = evaluate_all(y_true, labels)
    assert "ari" in metrics
    assert "nmi" in metrics
    assert "ami" in metrics
    assert metrics["ari"] > 0.5  # High recovery on clear clusters
