"""
Experiment 1 (Part B & C): Multi-Classifier Pseudo-Label Inductive Generalization Test.

Evaluates whether training downstream inductive classifiers on certified Invariant Core
pseudo-labels achieves higher out-of-sample generalization accuracy on held-out noisy test data
than training on all (100%) uncalibrated pseudo-labels.

Downstream Classifiers Evaluated:
1. SVM (Support Vector Machine with Linear Kernel)
2. RandomForest (RandomForestClassifier with 100 estimators)
3. MLP (Multi-Layer Perceptron neural network, hidden layers (100, 50), max_iter=500)
4. KNN (K-Nearest Neighbors with k=5)
"""

import time
from pathlib import Path
import numpy as np
import pandas as pd
import scipy.linalg as sla
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier

import sys
src_dir = Path(__file__).resolve().parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

root_dir = Path(__file__).resolve().parents[3]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from exp0_core import build_dataset, run_clusterer, pairwise_coassoc
from icc_v1 import InvariantCoreConsensus
from src.icc.metrics import evaluate_all


def align_labels_hungarian(y_true, y_pred):
    """Aligns unsupervised cluster labels to ground truth using the Hungarian algorithm."""
    classes = np.unique(y_true)
    clusters = np.unique(y_pred)
    cost_matrix = np.zeros((len(classes), len(clusters)))
    for i, c in enumerate(classes):
        for j, cl in enumerate(clusters):
            cost_matrix[i, j] = -np.sum((y_true == c) & (y_pred == cl))
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    mapping = {clusters[j]: classes[i] for i, j in zip(row_ind, col_ind)}
    return np.array([mapping.get(p, p) for p in y_pred])


class DualRidgeClassifier:
    """High-Dimensional Dual Ridge / Kernel Linear SVM equivalent fallback."""
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

        Y = np.zeros((n, k))
        for idx, c in enumerate(self.classes_):
            Y[y == c, idx] = 1.0

        K = X @ X.T + self.alpha * np.eye(n)
        self.dual_weights = sla.solve(K, Y, assume_a='pos')
        return self

    def predict(self, X_test):
        K_test = X_test @ self.X_train.T
        scores = K_test @ self.dual_weights
        pred_idx = np.argmax(scores, axis=1)
        return self.classes_[pred_idx]


def get_classifier_instances(seed=42):
    """Instantiates the 4 benchmark downstream classifiers with fixed reproducible configurations."""
    return {
        "SVM": SVC(kernel="linear", random_state=seed),
        "RF": RandomForestClassifier(n_estimators=100, random_state=seed, n_jobs=-1),
        "MLP": MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=seed),
        "KNN": KNeighborsClassifier(n_neighbors=5),
    }


def extract_core_subset(X_train, pseudo_train_aligned, core_mask, stability, noise_frac, k_clusters, min_per_cluster=2):
    """
    Extracts high-confidence core instances while guaranteeing representation across all clusters.
    """
    valid = True
    for c in range(k_clusters):
        c_core = core_mask & (pseudo_train_aligned == c)
        if np.sum(c_core) < min_per_cluster:
            valid = False
            break
    if valid:
        return X_train[core_mask], pseudo_train_aligned[core_mask]

    # Stratified fallback by sample stability
    quality = stability * (1.0 - noise_frac)
    selected_indices = []
    for c in range(k_clusters):
        c_indices = np.where(pseudo_train_aligned == c)[0]
        if len(c_indices) == 0:
            continue
        c_sorted = c_indices[np.argsort(quality[c_indices])]
        take = max(min_per_cluster, len(c_sorted) // 2)
        selected_indices.extend(c_sorted[-take:])
    selected_indices = np.array(selected_indices)
    return X_train[selected_indices], pseudo_train_aligned[selected_indices]


def run_pseudolabel_generalization(
    noise_dims=None,
    n_trials=5,
    n_total=300,
    train_ratio=0.8,
    k_clusters=3,
    noise_kind="scaled",
    output_csv=None,
):
    """
    Executes the multi-classifier pseudo-label generalization sweep.
    Sweeps D_noise in {0, 50, 200, 500, 1000, 3000, 5000} across [SVM, RF, MLP, KNN].
    """
    if noise_dims is None:
        noise_dims = [0, 50, 200, 500, 1000, 3000, 5000]

    exp_dir = Path(__file__).resolve().parent.parent
    data_dir = exp_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    if output_csv is None:
        output_csv = data_dir / "exp1_multiclassifier_results.csv"

    print("=================================================================")
    print(" RUNNING MULTI-CLASSIFIER PSEUDO-LABEL GENERALIZATION TEST")
    print(f" Target Noise: {noise_kind.upper()} | D_noise: {noise_dims}")
    print(f" Classifiers: [SVM, RF, MLP, KNN] | Trials: {n_trials}")
    print(f" N={n_total} (Train={int(n_total*train_ratio)}, Test={n_total - int(n_total*train_ratio)})")
    print("=================================================================")

    records = []
    summary_svm = []
    t_start = time.time()

    for d_noise in noise_dims:
        t0 = time.time()
        print(f"\n--> Evaluating D_noise = {d_noise:<5} (Total D = {d_noise + 2})")

        acc_svm_all = []
        acc_svm_core = []
        ari_svm_all = []
        ari_svm_core = []

        for trial in range(n_trials):
            trial_seed = trial * 37 + 11
            X, y_true = build_dataset(
                d_noise=d_noise, noise_kind=noise_kind, noise_seed=trial_seed,
                n_per_cluster=n_total // k_clusters, k=k_clusters
            )

            # Split Train (80%) / Test (20%)
            n_samples = X.shape[0]
            rng = np.random.default_rng(trial_seed)
            perm = rng.permutation(n_samples)
            n_train = int(n_samples * train_ratio)
            train_idx, test_idx = perm[:n_train], perm[n_train:]

            X_train, y_train_true = X[train_idx], y_true[train_idx]
            X_test, y_test_true = X[test_idx], y_true[test_idx]

            # 1. Unsupervised Clustering on Train Split ONLY
            icc = InvariantCoreConsensus(
                n_clusters=k_clusters, n_base_models=20, n_anchors=50,
                subspace_rate=0.25, beta=2.0, base_clusterer="kmeans",
                random_state=trial
            )
            pseudo_train = icc.fit_predict(X_train)
            core_mask = icc.core_mask_
            pseudo_train_aligned = align_labels_hungarian(y_train_true, pseudo_train)

            # 2. Extract Certified Core Pseudo-labels
            X_core, y_core = extract_core_subset(
                X_train, pseudo_train_aligned, core_mask,
                icc.stability_, icc.noise_fraction_, k_clusters
            )

            # 3. Train each downstream classifier on ALL vs CORE-ONLY
            clfs_all = get_classifier_instances(seed=trial_seed)
            clfs_core = get_classifier_instances(seed=trial_seed)

            for cname in ["SVM", "RF", "MLP", "KNN"]:
                # --- Train on ALL Pseudo-labels (100%) ---
                clf_all = clfs_all[cname]
                try:
                    clf_all.fit(X_train, pseudo_train_aligned)
                    preds_all = clf_all.predict(X_test)
                except Exception:
                    # Fallback to DualRidge if solver issue
                    dual = DualRidgeClassifier(alpha=1.0).fit(X_train, pseudo_train_aligned)
                    preds_all = dual.predict(X_test)

                scores_all = evaluate_all(y_test_true, preds_all)
                acc_all = float(np.mean(preds_all == y_test_true))

                # --- Train on CORE-ONLY Pseudo-labels ---
                clf_core = clfs_core[cname]
                try:
                    clf_core.fit(X_core, y_core)
                    preds_core = clf_core.predict(X_test)
                except Exception:
                    dual = DualRidgeClassifier(alpha=1.0).fit(X_core, y_core)
                    preds_core = dual.predict(X_test)

                scores_core = evaluate_all(y_test_true, preds_core)
                acc_core = float(np.mean(preds_core == y_test_true))

                records.append({
                    "classifier": cname,
                    "d_noise": d_noise,
                    "trial": trial,
                    "training_set": "ALL",
                    "test_ari": scores_all["ari"],
                    "test_nmi": scores_all["nmi"],
                    "test_accuracy": acc_all,
                })

                records.append({
                    "classifier": cname,
                    "d_noise": d_noise,
                    "trial": trial,
                    "training_set": "CORE",
                    "test_ari": scores_core["ari"],
                    "test_nmi": scores_core["nmi"],
                    "test_accuracy": acc_core,
                })

                if cname == "SVM":
                    acc_svm_all.append(acc_all)
                    acc_svm_core.append(acc_core)
                    ari_svm_all.append(scores_all["ari"])
                    ari_svm_core.append(scores_core["ari"])

        m_acc_all = float(np.mean(acc_svm_all))
        m_acc_core = float(np.mean(acc_svm_core))
        m_ari_all = float(np.mean(ari_svm_all))
        m_ari_core = float(np.mean(ari_svm_core))

        summary_svm.append({
            "d_noise": d_noise,
            "test_acc_full_pseudo": m_acc_all,
            "test_acc_core_pseudo": m_acc_core,
            "test_ari_full_pseudo": m_ari_all,
            "test_ari_core_pseudo": m_ari_core,
            "core_advantage_acc": m_acc_core - m_acc_all,
            "core_advantage_ari": m_ari_core - m_ari_all,
        })

        print(f"  [D_noise={d_noise:5d} in {time.time()-t0:.2f}s] SVM Out-of-Sample Test Acc -> All: {m_acc_all:.3f} | "
              f"Core: {m_acc_core:.3f} (Delta: {m_acc_core - m_acc_all:+.3f})")

    # Save primary multi-classifier results
    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False)
    print(f"\n[+] Saved multi-classifier results to {output_csv} ({len(df)} evaluations)")

    # Save backward-compatible SVM summary CSV
    df_svm = pd.DataFrame(summary_svm)
    svm_csv = data_dir / "exp1_pseudolabel_results.csv"
    df_svm.to_csv(svm_csv, index=False)
    print(f"[+] Saved SVM pseudo-label summary to {svm_csv}")

    return df


if __name__ == "__main__":
    run_pseudolabel_generalization()
