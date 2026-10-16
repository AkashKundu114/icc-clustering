"""
Experiment 1: Downstream Inductive Generalization Test.
Tests whether training on an Invariant Core (40-60% of samples) achieves higher
out-of-sample generalization accuracy on held-out noisy test data than training
on 100% of the training set.

Evaluates:
1. Full Train (100% of noisy training samples)
2. Random Subset (50% control)
3. Li et al. (2019) Label-Space Determinacy Core (50%)
4. ICC-v1 Feature-Calibrated Invariant Core (50%)
"""

import time
from pathlib import Path
import numpy as np
import pandas as pd
import scipy.linalg as sla
from scipy.spatial.distance import cdist
# Import synthetic generator from exp0_core
import sys
root_dir = Path(__file__).resolve().parents[3]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
src_dir = Path(__file__).resolve().parent / "experiment_0_suite" / "src"
sys.path.insert(0, str(src_dir))
from exp0_core import build_dataset, run_clusterer, pairwise_coassoc
from icc.metrics import evaluate_all, adjusted_rand_score


# ==============================================================================
# INDUCTIVE CLASSIFIERS (DUAL KERNEL RIDGE & LOGISTIC REGRESSION)
# ==============================================================================

class DualRidgeClassifier:
    """
    High-Dimensional Dual Ridge / Kernel Linear SVM equivalent.
    In D >> N regimes, inverts an (N x N) Gram matrix in O(N^3) rather than (D x D) in O(D^3).
    """
    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.X_train = None
        self.dual_weights = None
        self.classes_ = None

    def fit(self, X, y):
        self.classes_ = np.unique(y)
        k = len(self.classes_)
        n = X.shape[0]
        self.X_train = X

        # One-hot encode targets
        Y = np.zeros((n, k))
        for idx, c in enumerate(self.classes_):
            Y[y == c, idx] = 1.0

        # Dual Gram matrix: K = X X^T
        K = X @ X.T + self.alpha * np.eye(n)
        # Solve (K + alpha I) A = Y
        self.dual_weights = sla.solve(K, Y, assume_a='pos')
        return self

    def predict(self, X_test):
        # K_test = X_test @ X_train^T
        K_test = X_test @ self.X_train.T
        scores = K_test @ self.dual_weights
        pred_idx = np.argmax(scores, axis=1)
        return self.classes_[pred_idx]


class NearestCentroidClassifier:
    """Nearest Centroid classifier for high-dimensional prototype generalization."""
    def __init__(self):
        self.centroids = {}
        self.classes_ = None

    def fit(self, X, y):
        self.classes_ = np.unique(y)
        for c in self.classes_:
            self.centroids[c] = X[y == c].mean(axis=0)
        return self

    def predict(self, X_test):
        centers = np.array([self.centroids[c] for c in self.classes_])
        dists = cdist(X_test, centers, metric='sqeuclidean')
        pred_idx = np.argmin(dists, axis=1)
        return self.classes_[pred_idx]


# ==============================================================================
# SAMPLE FILTERING ENGINES (DETERMINACY vs ICC CALIBRATED)
# ==============================================================================

def select_li2019_core(X_train, k=3, m_runs=15, keep_fraction=0.5):
    """
    Selects top core samples using Li et al. (2019) label-space determinacy:
    Det(i) = 1/N sum_j [1 - 4(S_ij - 0.5)^2]
    """
    n = X_train.shape[0]
    labelings = []
    for s in range(m_runs):
        lab = run_clusterer("kmeans", X_train, k, seed=s)
        labelings.append(lab)

    S = pairwise_coassoc(labelings)
    # Co-association determinacy
    det = 1.0 - 4.0 * np.mean((S - 0.5) ** 2, axis=1)
    n_keep = int(n * keep_fraction)
    core_idx = np.argsort(det)[-n_keep:]
    return core_idx, det


def select_icc_calibrated_core(X_train, k=3, m_runs=15, keep_fraction=0.5, beta=2.0):
    """
    Selects top core samples using ICC-v1 reliability-calibrated determinacy:
    Scores points by Stability penalized by Residual Noise Fraction:
    Score(i) = C_i * (1 - R_i)
    """
    n, d = X_train.shape
    labelings = []
    subspace_gates = []

    # Run random subspace clusterers
    rng = np.random.default_rng(42)
    for s in range(m_runs):
        # Feature gate with variance prior
        var = np.var(X_train, axis=0)
        p = var / (np.sum(var) + 1e-12)
        # Select active subspace
        n_active = max(2, int(d * 0.2))
        active_dims = rng.choice(d, size=n_active, replace=False, p=p)
        gate = np.zeros(d)
        gate[active_dims] = 1.0
        subspace_gates.append(gate)

        lab = run_clusterer("kmeans", X_train * gate, k, seed=s)
        labelings.append(lab)

    # 1. Consensus determinacy C_i
    S = pairwise_coassoc(labelings)
    C = 1.0 - 4.0 * np.mean((S - 0.5) ** 2, axis=1)

    # 2. Residual noise fraction R_i
    mean_gate = np.mean(subspace_gates, axis=0)
    noise_gate = 1.0 - mean_gate
    R = np.sum(X_train**2 * noise_gate, axis=1) / (np.sum(X_train**2, axis=1) + 1e-12)

    # 3. ICC Score: high stability, low noise dependency
    icc_score = C * np.exp(-beta * R)
    n_keep = int(n * keep_fraction)
    core_idx = np.argsort(icc_score)[-n_keep:]
    return core_idx, icc_score


# ==============================================================================
# MAIN EXPERIMENT EXECUTION
# ==============================================================================

def run_generalization_experiment(
    n_total=400,
    train_ratio=0.8,
    k_clusters=3,
    noise_dims=[0, 50, 200, 1000, 3000, 5000],
    n_repeats=20,
    noise_kind="scaled"  # heteroscedastic noise triggers strong noise traps
):
    print("=================================================================")
    print(" RUNNING INDUCTIVE GENERALIZATION TEST")
    print(f" N={n_total} (Train={int(n_total*train_ratio)}, Test={n_total - int(n_total*train_ratio)}), K={k_clusters}")
    print(f" Testing across {len(noise_dims)} noise dimensions, {n_repeats} independent splits")
    print("=================================================================")

    results = []

    for d_noise in noise_dims:
        t0 = time.time()
        print(f"\n--> Evaluating D_noise = {d_noise} (Total D = {d_noise + 2})")

        acc_full_list = []
        acc_full_list = []
        acc_random_list = []
        acc_li_list = []
        acc_icc_list = []
        
        icc_metrics_list = []
        full_metrics_list = []
        li_metrics_list = []

        for split_seed in range(n_repeats):
            # 1. Generate full dataset
            X, y = build_dataset(
                d_noise=d_noise, noise_kind=noise_kind, noise_seed=split_seed,
                n_per_cluster=n_total // k_clusters, k=k_clusters
            )

            # 2. Split into 80% Train, 20% Test strictly out-of-sample
            n_samples = X.shape[0]
            rng = np.random.default_rng(split_seed + 100)
            perm = rng.permutation(n_samples)
            n_train = int(n_samples * train_ratio)
            train_idx, test_idx = perm[:n_train], perm[n_train:]

            X_train, y_train = X[train_idx], y[train_idx]
            X_test, y_test = X[test_idx], y[test_idx]

            # 3. Core Selection Strategies on Train Split
            # Strategy A: 100% Full Training Set
            clf_full = DualRidgeClassifier(alpha=1.0).fit(X_train, y_train)
            pred_full = clf_full.predict(X_test)
            acc_full = np.mean(pred_full == y_test)
            full_metrics_list.append(evaluate_all(y_test, pred_full))

            # Strategy B: Random 50% Subsample Control
            n_half = n_train // 2
            rand_sub = rng.choice(n_train, size=n_half, replace=False)
            clf_rand = DualRidgeClassifier(alpha=1.0).fit(X_train[rand_sub], y_train[rand_sub])
            pred_rand = clf_rand.predict(X_test)
            acc_rand = np.mean(pred_rand == y_test)

            # Strategy C: Li et al. (2019) Stability Determinacy Core (50%)
            li_core_idx, _ = select_li2019_core(X_train, k=k_clusters, keep_fraction=0.5)
            clf_li = DualRidgeClassifier(alpha=1.0).fit(X_train[li_core_idx], y_train[li_core_idx])
            pred_li = clf_li.predict(X_test)
            acc_li = np.mean(pred_li == y_test)
            li_metrics_list.append(evaluate_all(y_test, pred_li))

            # Strategy D: ICC-v1 Feature-Calibrated Invariant Core (50%)
            icc_core_idx, _ = select_icc_calibrated_core(X_train, k=k_clusters, keep_fraction=0.5)
            clf_icc = DualRidgeClassifier(alpha=1.0).fit(X_train[icc_core_idx], y_train[icc_core_idx])
            pred_icc = clf_icc.predict(X_test)
            acc_icc = np.mean(pred_icc == y_test)
            icc_metrics_list.append(evaluate_all(y_test, pred_icc))

            acc_full_list.append(acc_full)
            acc_random_list.append(acc_rand)
            acc_li_list.append(acc_li)
            acc_icc_list.append(acc_icc)

        mean_full = float(np.mean(acc_full_list))
        mean_rand = float(np.mean(acc_random_list))
        mean_li = float(np.mean(acc_li_list))
        mean_icc = float(np.mean(acc_icc_list))

        test_ari = float(np.mean([m["ari"] for m in icc_metrics_list]))
        test_nmi = float(np.mean([m["nmi"] for m in icc_metrics_list]))
        test_ami = float(np.mean([m["ami"] for m in icc_metrics_list]))
        test_v_measure = float(np.mean([m["v_measure"] for m in icc_metrics_list]))
        test_fm_index = float(np.mean([m["fm_index"] for m in icc_metrics_list]))

        results.append(dict(
            d_noise=d_noise,
            mean_full_100=mean_full,
            mean_random_50=mean_rand,
            mean_li2019_50=mean_li,
            mean_icc_50=mean_icc,
            icc_advantage_over_full=mean_icc - mean_full,
            icc_advantage_over_li=mean_icc - mean_li,
            test_ari=test_ari,
            test_nmi=test_nmi,
            test_ami=test_ami,
            test_v_measure=test_v_measure,
            test_fm_index=test_fm_index,
            full_test_ari=float(np.mean([m["ari"] for m in full_metrics_list])),
            full_test_nmi=float(np.mean([m["nmi"] for m in full_metrics_list])),
            full_test_ami=float(np.mean([m["ami"] for m in full_metrics_list])),
            li_test_ari=float(np.mean([m["ari"] for m in li_metrics_list])),
            li_test_nmi=float(np.mean([m["nmi"] for m in li_metrics_list])),
            li_test_ami=float(np.mean([m["ami"] for m in li_metrics_list])),
        ))

        print(f"  [D_noise={d_noise:5d}] Test Acc -> Full: {mean_full:.3f} | ICC: {mean_icc:.3f} (Adv: {mean_icc - mean_full:+.3f}) | "
              f"Test ARI: {test_ari:.3f}, NMI: {test_nmi:.3f}, AMI: {test_ami:.3f}")

    df = pd.DataFrame(results)
    out_dir = Path(__file__).resolve().parent / "experiment_0_suite" / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / "exp1_generalization_results.csv", index=False)
    print(f"\nSaved generalization data to {out_dir / 'exp1_generalization_results.csv'}")

    # Also save to experiments/exp1_generalization/data if that exists
    exp1_data_dir = Path(__file__).resolve().parent.parent / "data"
    if exp1_data_dir.exists():
        df.to_csv(exp1_data_dir / "exp1_generalization_results.csv", index=False)

    # Plot Inductive Generalization Curves
    plot_generalization(df)
    return df


def plot_generalization(df):
    fig_dir = Path(__file__).resolve().parent / "experiment_0_suite" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.0, 5.8), dpi=300)

    # Subplot 1: Out-of-sample Test Accuracy across Strategies
    ax1.plot(df["d_noise"], df["mean_full_100"], marker="o", color="#1f77b4",
             linewidth=2.0, markersize=7, label="Full Training Set (100% samples)")
    ax1.plot(df["d_noise"], df["mean_random_50"], marker="s", color="#7f7f7f",
             linewidth=1.8, linestyle="--", markersize=6, label="Random Subsample (50% control)")
    ax1.plot(df["d_noise"], df["mean_li2019_50"], marker="^", color="#ff7f0e",
             linewidth=2.0, markersize=7, label="Li et al. 2019 Determinacy Core (50%)")
    ax1.plot(df["d_noise"], df["mean_icc_50"], marker="d", color="#2ca02c",
             linewidth=2.5, markersize=8, label="ICC-v1 Calibrated Core (50%) [Ours]")

    ax1.set_title("Out-of-Sample Generalization on Held-Out Test Set (20%)", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Noise dimensions ($D_{noise}$)", fontsize=11)
    ax1.set_ylabel("Test Accuracy on Raw Held-Out Data", fontsize=11)
    ax1.set_xscale("symlog", linthresh=10)
    ax1.set_ylim(0.25, 1.05)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="lower left", fontsize=10)

    # Subplot 2: Pruning Generalization Advantage (ICC Core vs Full 100%)
    advantage = df["icc_advantage_over_full"] * 100
    bars = ax2.bar(range(len(df)), advantage, color="#2ca02c", alpha=0.85, width=0.55)
    ax2.axhline(0, color="black", linestyle="--", linewidth=1.0)

    # Add labels on bars
    for idx, rect in enumerate(bars):
        h = rect.get_height()
        va = "bottom" if h >= 0 else "top"
        ax2.annotate(f"{h:+.1f}%", xy=(rect.get_x() + rect.get_width() / 2, h),
                     xytext=(0, 3 if h >= 0 else -10), textcoords="offset points",
                     ha="center", va=va, fontsize=9, fontweight="bold")

    ax2.set_xticks(range(len(df)))
    ax2.set_xticklabels([str(d) for d in df["d_noise"]], fontsize=10)
    ax2.set_title("Generalization Advantage of Training on 50% Core vs 100% Full", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Noise dimensions ($D_{noise}$)", fontsize=11)
    ax2.set_ylabel("Absolute Test Accuracy Gain (% points)", fontsize=11)
    ax2.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    out_path = fig_dir / "fig9_inductive_generalization.png"
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Saved publication figure -> {out_path}")

    # Supplementary Figure 9: Test NMI & AMI Inductive Generalization
    if "test_nmi" in df.columns:
        fig_supp, (sax1, sax2) = plt.subplots(1, 2, figsize=(15.0, 5.8), dpi=300)
        sax1.plot(df["d_noise"], df["full_test_nmi"], marker="o", color="#1f77b4",
                  linewidth=2.0, markersize=7, label="Full Training Set (100%)")
        sax1.plot(df["d_noise"], df["li_test_nmi"], marker="^", color="#ff7f0e",
                  linewidth=2.0, markersize=7, label="Li et al. (2019) Core (50%)")
        sax1.plot(df["d_noise"], df["test_nmi"], marker="d", color="#2ca02c",
                  linewidth=2.5, markersize=8, label="ICC-v1 Core (50%) [Ours]")

        sax1.set_title("Held-Out Test NMI Across Noise Dimensions", fontsize=12, fontweight="bold")
        sax1.set_xlabel("Noise dimensions ($D_{noise}$)", fontsize=11)
        sax1.set_ylabel("Normalized Mutual Information (NMI)", fontsize=11)
        sax1.set_xscale("symlog", linthresh=10)
        sax1.set_ylim(-0.05, 1.05)
        sax1.grid(True, alpha=0.3)
        sax1.legend(loc="lower left", fontsize=10)

        sax2.plot(df["d_noise"], df["full_test_ami"], marker="o", color="#1f77b4",
                  linewidth=2.0, markersize=7, label="Full Training Set (100%)")
        sax2.plot(df["d_noise"], df["li_test_ami"], marker="^", color="#ff7f0e",
                  linewidth=2.0, markersize=7, label="Li et al. (2019) Core (50%)")
        sax2.plot(df["d_noise"], df["test_ami"], marker="d", color="#2ca02c",
                  linewidth=2.5, markersize=8, label="ICC-v1 Core (50%) [Ours]")

        sax2.set_title("Held-Out Test AMI Across Noise Dimensions", fontsize=12, fontweight="bold")
        sax2.set_xlabel("Noise dimensions ($D_{noise}$)", fontsize=11)
        sax2.set_ylabel("Adjusted Mutual Information (AMI)", fontsize=11)
        sax2.set_xscale("symlog", linthresh=10)
        sax2.set_ylim(-0.05, 1.05)
        sax2.grid(True, alpha=0.3)
        sax2.legend(loc="lower left", fontsize=10)

        plt.tight_layout()
        supp_path = fig_dir / "fig9_supp_nmi_inductive_generalization.png"
        plt.savefig(supp_path, dpi=300)
        plt.close()
        print(f"Saved supplementary figure -> {supp_path}")


if __name__ == "__main__":
    run_generalization_experiment()
