"""
Experiment 1 (Part C): Multi-Classifier Inductive Generalization Audit.

Evaluates unsupervised pseudo-label denoising across diverse downstream inductive classifiers:
1. SVM (Linear Support Vector Classifier)
2. RF (RandomForestClassifier, n_estimators=100)
3. MLP (Multi-Layer Perceptron, hidden_layer_sizes=(100, 50), max_iter=500)
4. KNN (K-Nearest Neighbors, n_neighbors=5)
"""

import sys
from pathlib import Path

src_dir = Path(__file__).resolve().parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from exp1_pseudolabel_generalization import (
    run_pseudolabel_generalization,
    get_classifier_instances,
    align_labels_hungarian,
    extract_core_subset,
)


def run_multiclassifier_generalization(
    noise_dims=None,
    n_trials=5,
    n_total=300,
    train_ratio=0.8,
    k_clusters=3,
    noise_kind="scaled",
    output_csv=None,
):
    """Entry point forwarding to unified multi-classifier implementation."""
    return run_pseudolabel_generalization(
        noise_dims=noise_dims,
        n_trials=n_trials,
        n_total=n_total,
        train_ratio=train_ratio,
        k_clusters=k_clusters,
        noise_kind=noise_kind,
        output_csv=output_csv,
    )


if __name__ == "__main__":
    run_multiclassifier_generalization(
        noise_dims=[0, 50, 200, 500, 1000, 3000, 5000],
        n_trials=5,
    )
