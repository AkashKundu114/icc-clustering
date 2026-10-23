import numpy as np

from icc import ICC
from icc.metrics import evaluate_all


def main():
    print("=" * 60)
    print("ICC-v2 Quickstart Example (Synthetic Benchmark)")
    print("=" * 60)

    # 1. Generate synthetic high-dimensional data (N=150, D=300, K=3)
    rng = np.random.default_rng(42)
    X = rng.standard_normal((150, 300))
    # Plant distinct signals in 15 features
    y_true = np.array([0] * 50 + [1] * 50 + [2] * 50)
    X[:50, :15] += 2.5
    X[50:100, :15] -= 2.5

    # 2. Fit the ICC-v2 estimator
    model = ICC(
        n_clusters=3,
        n_base_models=25,
        n_anchors=30,
        subspace_rate=0.30,
        core_quantile=0.50,
        random_state=42,
    )
    labels = model.fit_predict(X)

    # 3. Evaluate clustering metrics
    scores = evaluate_all(y_true, labels)
    print("\nTraining Metrics:")
    print(f"  Adjusted Rand Index (ARI):    {scores['ari']:.4f}")
    print(f"  Normalized Mutual Info (NMI): {scores['nmi']:.4f}")

    # 4. Out-of-sample inductive assignment
    X_new = rng.standard_normal((5, 300))
    X_new[:, :15] += 2.5
    pred_new = model.predict(X_new)
    print(f"\nInductive Predictions for Query Instances: {pred_new.tolist()}")

    # 5. Low-dimensional spectral coordinates
    emb = model.transform()
    print(f"Spectral Embedding Coordinates Shape:     {emb.shape}")
    print("=" * 60)

if __name__ == "__main__":
    main()
