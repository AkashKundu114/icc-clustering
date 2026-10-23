import sys
import time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import kneighbors_graph
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from icc.consensus_v2 import InvariantCoreConsensusV2
from icc.baselines.consensus import run_standard_consensus

DATASETS = [
    "colon", "leukemia", "srbct", "cns", "lymphoma", "ovarian",
    "indian_pines", "isolet", "har", "newsgroups20", "usps", "waveform", "yale_b"
]

SEEDS = [42, 101, 202, 303, 404, 505, 606, 707, 808, 909]

def compute_laplacian_score(X, n_neighbors=5):
    N, D = X.shape
    W = kneighbors_graph(X, n_neighbors=min(n_neighbors, N - 1), mode="connectivity", include_self=False)
    W = 0.5 * (W + W.T)
    d = np.array(W.sum(axis=1)).flatten()
    L = np.diag(d) - W.toarray()
    scores = np.zeros(D)
    ones = np.ones(N)
    d_sum = np.sum(d)
    if d_sum < 1e-12:
        return np.zeros(D)
    for j in range(D):
        f = X[:, j]
        f_tilde = f - (np.dot(f, d) / d_sum) * ones
        denom = np.dot(f_tilde * d, f_tilde)
        if denom < 1e-12:
            scores[j] = np.inf
        else:
            numer = np.dot(f_tilde, np.dot(L, f_tilde))
            scores[j] = numer / denom
    return scores

def run_sparse_kmeans(X, k, s=None, max_iter=8, random_state=42):
    N, D = X.shape
    if s is None:
        s = 1.1 + 0.5 * (np.sqrt(D) - 1.1)
    s = max(1.1, min(s, np.sqrt(D) * 0.9))
    w = np.ones(D) / np.sqrt(D)
    labels = KMeans(n_clusters=k, n_init=3, random_state=random_state).fit_predict(X)
    for it in range(max_iter):
        a = np.zeros(D)
        for c in range(k):
            members = X[labels == c]
            if len(members) > 0:
                mean_c = members.mean(axis=0)
                a += len(members) * (mean_c ** 2)
        if np.all(a <= 1e-12):
            break
        low, high = 0.0, np.max(a)
        best_delta = 0.0
        for _ in range(25):
            delta = (low + high) / 2.0
            soft = np.maximum(0.0, a - delta)
            norm2 = np.linalg.norm(soft)
            if norm2 < 1e-12:
                high = delta
                continue
            l1_over_l2 = np.sum(soft) / norm2
            if l1_over_l2 > s:
                low = delta
            else:
                high = delta
                best_delta = delta
        soft = np.maximum(0.0, a - best_delta)
        norm2 = np.linalg.norm(soft)
        w = soft / (norm2 + 1e-12)
        X_w = X * np.sqrt(w)
        new_labels = KMeans(n_clusters=k, n_init=1, random_state=random_state).fit_predict(X_w)
        if np.array_equal(new_labels, labels):
            break
        labels = new_labels
    return labels

def main():
    out_dir = Path("results/phase2")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_csv = out_dir / "fair_baselines.csv"

    records = []

    for dname in DATASETS:
        p_npz = Path(f"experiments/exp3_real_world_benchmarks/data/cache/{dname}.npz")
        data = np.load(p_npz)
        X, y = data["X"].astype(np.float64), data["y"]
        N, D = X.shape
        K = len(np.unique(y))
        print(f"Dataset {dname.upper()}: N={N}, D={D}, K={K}")

        n_top = max(2, int(np.ceil(0.15 * D)))
        var_indices = np.argsort(X.var(axis=0))[-n_top:]
        X_var = X[:, var_indices]

        n_comp = min(N - 1, D, 50)
        svd = TruncatedSVD(n_components=n_comp, random_state=42)
        X_pca = svd.fit_transform(X)

        if D > 5000 and N > 500:
            sub_feats = np.argsort(X.var(axis=0))[-3000:]
            lap_scores_sub = compute_laplacian_score(X[:, sub_feats])
            lap_indices = sub_feats[np.argsort(lap_scores_sub)[:n_top]]
        else:
            lap_scores = compute_laplacian_score(X)
            lap_indices = np.argsort(lap_scores)[:n_top]
        X_lap = X[:, lap_indices]

        for s_idx, seed in enumerate(SEEDS):
            t0 = time.perf_counter()
            pred_km_all = KMeans(n_clusters=K, n_init=5, random_state=seed).fit_predict(X)
            t_km_all = time.perf_counter() - t0
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "model": "K-Means_All", "seed": seed, "ari": adjusted_rand_score(y, pred_km_all), "nmi": normalized_mutual_info_score(y, pred_km_all), "runtime_s": t_km_all})

            t0 = time.perf_counter()
            pred_km_var = KMeans(n_clusters=K, n_init=5, random_state=seed).fit_predict(X_var)
            t_km_var = time.perf_counter() - t0
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "model": "K-Means_VarFilt", "seed": seed, "ari": adjusted_rand_score(y, pred_km_var), "nmi": normalized_mutual_info_score(y, pred_km_var), "runtime_s": t_km_var})

            t0 = time.perf_counter()
            pred_km_pca = KMeans(n_clusters=K, n_init=5, random_state=seed).fit_predict(X_pca)
            t_km_pca = time.perf_counter() - t0
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "model": "K-Means_PCA", "seed": seed, "ari": adjusted_rand_score(y, pred_km_pca), "nmi": normalized_mutual_info_score(y, pred_km_pca), "runtime_s": t_km_pca})

            t0 = time.perf_counter()
            pred_km_lap = KMeans(n_clusters=K, n_init=5, random_state=seed).fit_predict(X_lap)
            t_km_lap = time.perf_counter() - t0
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "model": "K-Means_LapScore", "seed": seed, "ari": adjusted_rand_score(y, pred_km_lap), "nmi": normalized_mutual_info_score(y, pred_km_lap), "runtime_s": t_km_lap})

            t0 = time.perf_counter()
            pred_sparse_km = run_sparse_kmeans(X, K, random_state=seed)
            t_sparse_km = time.perf_counter() - t0
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "model": "SparseKMeans", "seed": seed, "ari": adjusted_rand_score(y, pred_sparse_km), "nmi": normalized_mutual_info_score(y, pred_sparse_km), "runtime_s": t_sparse_km})

            t0 = time.perf_counter()
            pred_std_all, t_std_all, _ = run_standard_consensus(X, K, seed=seed)
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "model": "StdCons_All", "seed": seed, "ari": adjusted_rand_score(y, pred_std_all), "nmi": normalized_mutual_info_score(y, pred_std_all), "runtime_s": t_std_all})

            t0 = time.perf_counter()
            pred_std_var, t_std_var, _ = run_standard_consensus(X_var, K, seed=seed)
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "model": "StdCons_VarFilt", "seed": seed, "ari": adjusted_rand_score(y, pred_std_var), "nmi": normalized_mutual_info_score(y, pred_std_var), "runtime_s": t_std_var})

            t0 = time.perf_counter()
            pred_std_pca, t_std_pca, _ = run_standard_consensus(X_pca, K, seed=seed)
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "model": "StdCons_PCA", "seed": seed, "ari": adjusted_rand_score(y, pred_std_pca), "nmi": normalized_mutual_info_score(y, pred_std_pca), "runtime_s": t_std_pca})

            t0 = time.perf_counter()
            icc = InvariantCoreConsensusV2(n_clusters=K, random_state=seed)
            pred_icc = icc.fit_predict(X)
            t_icc = time.perf_counter() - t0
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "model": "ICC_v2", "seed": seed, "ari": adjusted_rand_score(y, pred_icc), "nmi": normalized_mutual_info_score(y, pred_icc), "runtime_s": t_icc})

    df = pd.DataFrame(records)
    df.to_csv(out_csv, index=False)
    print(f"Saved {len(df)} fair baseline records to {out_csv}")

if __name__ == "__main__":
    main()
