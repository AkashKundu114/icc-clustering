"""
Inductive out-of-sample evaluation on Leukemia microarray gene expression.

Demonstrates out-of-sample generalization of ICC-v2 on real-world cancer genomics data:
1. Loads the Golub et al. Leukemia dataset (N=72 patients, D=7,129 gene probes, K=2 subtypes: ALL vs AML).
2. Performs an 80/20 train/test split.
3. Fits ICC-v2 solely on the 80% training partition.
4. Evaluates training partition recovery (ARI).
5. Projects the remaining 20% held-out test patients in closed form using geometry-calibrated
   anchor centroids, demonstrating robust inductive generalization without model refitting.

Usage:
    python examples/leukemia_inductive.py
"""

import numpy as np

from icc import ICC
from icc.datasets.registry import load_dataset
from icc.metrics import evaluate_all


def main():
    print("=" * 60)
    print("ICC-v2 Leukemia Inductive Out-of-Sample Evaluation")
    print("=" * 60)

    # 1. Load benchmark dataset
    X, y, meta = load_dataset("leukemia")
    print(f"Loaded {meta.get('display_name', 'leukemia')}: N={X.shape[0]}, D={X.shape[1]}, K={len(np.unique(y))}")

    # 2. Train-test split (80% train, 20% held-out out-of-sample)
    rng = np.random.default_rng(42)
    n_samples = X.shape[0]
    indices = rng.permutation(n_samples)
    split = int(0.80 * n_samples)
    train_idx, test_idx = indices[:split], indices[split:]

    X_train, y_train = X[train_idx], y[train_idx]
    X_test, y_test = X[test_idx], y[test_idx]

    # 3. Fit estimator on training partition
    model = ICC(
        n_clusters=2,
        n_base_models=25,
        n_anchors=40,
        subspace_rate=0.25,
        core_quantile=0.50,
        random_state=42,
    )
    train_preds = model.fit_predict(X_train)
    train_ari = evaluate_all(y_train, train_preds)["ari"]
    print(f"Train Partition Adjusted Rand Index (ARI): {train_ari:.4f}")

    # 4. Out-of-sample inductive projection
    test_preds = model.predict(X_test)
    test_ari = evaluate_all(y_test, test_preds)["ari"]
    print(f"Held-Out Out-of-Sample (20%) Test ARI:     {test_ari:.4f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
