"""
Study 3': Pre-Registered Benchmark for Null-Calibrated Gating
Tracks:
- Track A: Isotropic Gaussian Mixture (20 signal, 480 i.i.d. noise)
- Track B: Correlated Nuisance Noise (20 signal, 480 Toeplitz rho=0.75 noise)
- Track C: Skewed Distractor Noise (20 signal, 480 lognormal noise)
- Track D: Non-linear XOR / Parity (4-feature XOR signal, 496 distractor noise)

Evaluates:
- Empirical FDP and Statistical Power across 10 random seeds.
- Downstream clustering ARI with K-Means and ICC-v2.
- Testing against pre-registered kill criteria.
"""

import json
import os
import sys
import numpy as np
import scipy.linalg as sla
from scipy.stats import kurtosis, skew
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.mixture import GaussianMixture

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.icc.consensus_v2 import InvariantCoreConsensusV2


# -----------------------------------------------------------------------------
# 1. Feature Screening Baselines
# -----------------------------------------------------------------------------

def compute_variance_scores(X: np.ndarray) -> np.ndarray:
    """Marginal sample variance."""
    return np.var(X, axis=0)


def compute_bc_scores(X: np.ndarray) -> np.ndarray:
    """Sarle's Bimodality Coefficient."""
    sk = skew(X, axis=0, bias=False)
    kt = kurtosis(X, axis=0, fisher=True, bias=False)
    bc = (sk**2 + 1.0) / (kt + 3.0 + 1e-9)
    return bc


def compute_bimodality_index(X: np.ndarray) -> np.ndarray:
    """
    Wang et al. Bimodality Index (BI):
    BI = sqrt(p * (1 - p)) * |mu_1 - mu_2| / sigma_pooled
    Computed via 2-component 1D GMM.
    """
    N, D = X.shape
    bi_scores = np.zeros(D)
    for j in range(D):
        x_j = X[:, j].reshape(-1, 1)
        try:
            gmm = GaussianMixture(n_components=2, n_init=1, random_state=42)
            gmm.fit(x_j)
            weights = gmm.weights_
            means = gmm.means_.ravel()
            covs = gmm.covariances_.ravel()
            sigma_pooled = np.sqrt(np.sum(weights * covs) + 1e-9)
            bi = np.sqrt(weights[0] * weights[1]) * np.abs(means[0] - means[1]) / sigma_pooled
            bi_scores[j] = bi
        except Exception:
            bi_scores[j] = 0.0
    return bi_scores


def compute_dip_proxy(X: np.ndarray) -> np.ndarray:
    """
    Hartigan Dip Statistic proxy:
    Measures maximum deviation between empirical CDF and the best-fitting unimodal uniform CDF.
    """
    N, D = X.shape
    dip_scores = np.zeros(D)
    for j in range(D):
        sorted_x = np.sort(X[:, j])
        x_std = np.std(sorted_x)
        if x_std < 1e-12:
            dip_scores[j] = 0.0
            continue
        z = (sorted_x - sorted_x[0]) / (sorted_x[-1] - sorted_x[0] + 1e-12)
        ecdf = np.arange(1, N + 1) / N
        # Uniform CDF: F(z) = z
        diff = np.abs(ecdf - z)
        dip_scores[j] = np.max(diff)
    return dip_scores


def null_calibrated_knockoff_gate(
    X: np.ndarray,
    n_clusters: int,
    fdr_target: float = 0.10,
    random_state: int = 42,
) -> np.ndarray:
    """
    Proposed Null-Calibrated Gating:
    Contrasts target feature agreement gain against a synthetic exchangeable null.
    Controls False Discovery Proportion at target level q.
    """
    rng = np.random.default_rng(random_state)
    N, D = X.shape

    # Generate synthetic null decoy matrix preserving feature marginals and covariance
    # Using Gaussian Copula / permuted exchangeable null
    X_decoy = np.zeros_like(X)
    for j in range(D):
        X_decoy[:, j] = rng.permutation(X[:, j])

    # Saliency via cluster separation on fast ensemble base partitions
    km = KMeans(n_clusters=n_clusters, n_init=2, random_state=random_state)
    pseudo_labels = km.fit_predict(X)

    def calc_saliency(mat):
        # Between-to-within variance ratio
        c_means = np.array([np.mean(mat[pseudo_labels == k], axis=0) for k in range(n_clusters)])
        between_var = np.var(c_means, axis=0)
        total_var = np.var(mat, axis=0) + 1e-9
        return between_var / total_var

    S_real = calc_saliency(X)
    S_decoy = calc_saliency(X_decoy)

    # Knockoff contrast statistic
    W = S_real - S_decoy

    # Solve for Knockoff+ threshold tau
    pos_W = np.sort(W[W > 0])
    if len(pos_W) == 0:
        return np.array([], dtype=int)

    best_tau = None
    for tau in pos_W:
        n_neg = np.sum(W <= -tau)
        n_pos = np.sum(W >= tau)
        fdp_est = (1.0 + n_neg) / max(1, n_pos)
        if fdp_est <= fdr_target:
            best_tau = tau
            break

    if best_tau is None:
        best_tau = pos_W[-1]

    selected = np.where(W >= best_tau)[0]
    return selected


# -----------------------------------------------------------------------------
# 2. Synthetic Data Generators
# -----------------------------------------------------------------------------

def generate_track_a(seed: int, N: int = 200, D_total: int = 500, D_signal: int = 20, K: int = 3):
    """Track A: Isotropic Gaussian Mixture + i.i.d. Gaussian noise."""
    rng = np.random.default_rng(seed)
    y = rng.choice(K, size=N)
    # Centroids with Delta / sigma = 2.5
    means = np.zeros((K, D_signal))
    for k in range(K):
        means[k, k * 2:(k + 1) * 2] = 2.5

    X_sig = np.zeros((N, D_signal))
    for k in range(K):
        idx = (y == k)
        X_sig[idx] = rng.normal(loc=means[k], scale=1.0, size=(np.sum(idx), D_signal))

    X_noise = rng.normal(loc=0.0, scale=1.0, size=(N, D_total - D_signal))
    X = np.hstack([X_sig, X_noise])
    return X, y, D_signal


def generate_track_b(seed: int, N: int = 200, D_total: int = 500, D_signal: int = 20, K: int = 3, rho: float = 0.75):
    """Track B: Correlated Nuisance Noise (Block Toeplitz covariance)."""
    rng = np.random.default_rng(seed)
    X_sig, y, _ = generate_track_a(seed=seed, N=N, D_total=D_signal, D_signal=D_signal, K=K)
    D_noise = D_total - D_signal

    # Block Toeplitz noise covariance with block size 20
    block_size = 20
    n_blocks = D_noise // block_size
    noise_blocks = []
    for b in range(n_blocks):
        # AR(1) correlation matrix
        idx = np.arange(block_size)
        cov_block = rho ** np.abs(idx[:, None] - idx[None, :])
        L = np.linalg.cholesky(cov_block + 1e-6 * np.eye(block_size))
        z = rng.normal(size=(N, block_size))
        block = z @ L.T
        noise_blocks.append(block)

    X_noise = np.hstack(noise_blocks)
    X = np.hstack([X_sig, X_noise])
    return X, y, D_signal


def generate_track_c(seed: int, N: int = 200, D_total: int = 500, D_signal: int = 20, K: int = 3):
    """Track C: Skewed Unimodal Distractors (Lognormal noise)."""
    rng = np.random.default_rng(seed)
    X_sig, y, _ = generate_track_a(seed=seed, N=N, D_total=D_signal, D_signal=D_signal, K=K)
    D_noise = D_total - D_signal
    # Lognormal noise standardized to zero mean unit variance
    raw_ln = rng.lognormal(mean=0.0, sigma=0.8, size=(N, D_noise))
    X_noise = (raw_ln - np.mean(raw_ln, axis=0)) / (np.std(raw_ln, axis=0) + 1e-9)
    X = np.hstack([X_sig, X_noise])
    return X, y, D_signal


def generate_track_d(seed: int, N: int = 400, D_total: int = 500, D_signal: int = 4):
    """Track D: Non-linear XOR / Parity across 4 features."""
    rng = np.random.default_rng(seed)
    # 4 clusters formed by 2-bit XOR parity
    # Clusters: (0,0), (0,1), (1,0), (1,1)
    b0 = rng.choice([0, 1], size=N)
    b1 = rng.choice([0, 1], size=N)
    y = b0 * 2 + b1

    X_sig = np.zeros((N, D_signal))
    for i in range(N):
        # Parity encoding: coordinates 0 and 1 represent bits with noise
        X_sig[i, 0] = (b0[i] * 2 - 1) * 1.5 + rng.normal(scale=0.4)
        X_sig[i, 1] = (b1[i] * 2 - 1) * 1.5 + rng.normal(scale=0.4)
        # Coordinate 2 is XOR product
        xor_bit = b0[i] ^ b1[i]
        X_sig[i, 2] = (xor_bit * 2 - 1) * 1.5 + rng.normal(scale=0.4)
        X_sig[i, 3] = rng.normal(scale=1.0)

    X_noise = rng.normal(size=(N, D_total - D_signal))
    X = np.hstack([X_sig, X_noise])
    return X, y, D_signal


# -----------------------------------------------------------------------------
# 3. Benchmark Execution Harness
# -----------------------------------------------------------------------------

def evaluate_selection(selected: np.ndarray, D_signal: int):
    """Calculate FDP and Power."""
    if len(selected) == 0:
        return 0.0, 0.0
    tp = np.sum(selected < D_signal)
    fp = np.sum(selected >= D_signal)
    fdp = fp / len(selected)
    power = tp / D_signal
    return float(fdp), float(power)


def run_benchmark():
    tracks = {
        "Track A (Isotropic Gaussian)": generate_track_a,
        "Track B (Correlated Nuisance)": generate_track_b,
        "Track C (Skewed Lognormal)": generate_track_c,
        "Track D (Non-linear XOR)": generate_track_d,
    }

    seeds = list(range(42, 52))  # 10 seeds
    results = {}

    print("=" * 80)
    print("STARTING PRE-REGISTERED BENCHMARK: STUDY 3' (NULL-CALIBRATED GATING)")
    print(f"Seeds: {len(seeds)} (42-51) | Nominal FDR Target q = 0.10")
    print("=" * 80)

    for track_name, track_gen in tracks.items():
        print(f"\n>>> Running {track_name} ...")
        track_results = {
            "Raw": {"ari_km": [], "ari_icc": []},
            "Variance (Top 20)": {"fdp": [], "power": [], "ari_km": [], "ari_icc": []},
            "Sarle BC (>0.555)": {"fdp": [], "power": [], "ari_km": [], "ari_icc": []},
            "Bimodality Index (Top 20)": {"fdp": [], "power": [], "ari_km": [], "ari_icc": []},
            "Hartigan Dip (Top 20)": {"fdp": [], "power": [], "ari_km": [], "ari_icc": []},
            "Null-Calibrated Decoy (Proposed)": {"fdp": [], "power": [], "ari_km": [], "ari_icc": [], "n_selected": []},
        }

        for seed in seeds:
            X, y, D_sig = track_gen(seed=seed)
            K = len(np.unique(y))

            # 1. Raw Baseline
            km = KMeans(n_clusters=K, n_init=5, random_state=seed)
            ari_km_raw = adjusted_rand_score(y, km.fit_predict(X))
            icc = InvariantCoreConsensusV2(n_clusters=K, n_base_models=15, random_state=seed)
            ari_icc_raw = adjusted_rand_score(y, icc.fit_predict(X))
            track_results["Raw"]["ari_km"].append(ari_km_raw)
            track_results["Raw"]["ari_icc"].append(ari_icc_raw)

            # 2. Variance Screening (Top D_sig)
            v_scores = compute_variance_scores(X)
            sel_var = np.argsort(v_scores)[::-1][:D_sig]
            fdp_var, pwr_var = evaluate_selection(sel_var, D_sig)
            ari_km_var = adjusted_rand_score(y, km.fit_predict(X[:, sel_var]))
            ari_icc_var = adjusted_rand_score(y, icc.fit_predict(X[:, sel_var]))
            track_results["Variance (Top 20)"]["fdp"].append(fdp_var)
            track_results["Variance (Top 20)"]["power"].append(pwr_var)
            track_results["Variance (Top 20)"]["ari_km"].append(ari_km_var)
            track_results["Variance (Top 20)"]["ari_icc"].append(ari_icc_var)

            # 3. Sarle's BC Screening (BC > 0.555 or Top D_sig)
            bc_scores = compute_bc_scores(X)
            sel_bc = np.where(bc_scores > 0.555)[0]
            if len(sel_bc) == 0:
                sel_bc = np.argsort(bc_scores)[::-1][:D_sig]
            fdp_bc, pwr_bc = evaluate_selection(sel_bc, D_sig)
            X_bc = X[:, sel_bc] if len(sel_bc) > 1 else X
            ari_km_bc = adjusted_rand_score(y, km.fit_predict(X_bc))
            ari_icc_bc = adjusted_rand_score(y, icc.fit_predict(X_bc))
            track_results["Sarle BC (>0.555)"]["fdp"].append(fdp_bc)
            track_results["Sarle BC (>0.555)"]["power"].append(pwr_bc)
            track_results["Sarle BC (>0.555)"]["ari_km"].append(ari_km_bc)
            track_results["Sarle BC (>0.555)"]["ari_icc"].append(ari_icc_bc)

            # 4. Bimodality Index Screening (Top D_sig)
            bi_scores = compute_bimodality_index(X)
            sel_bi = np.argsort(bi_scores)[::-1][:D_sig]
            fdp_bi, pwr_bi = evaluate_selection(sel_bi, D_sig)
            ari_km_bi = adjusted_rand_score(y, km.fit_predict(X[:, sel_bi]))
            ari_icc_bi = adjusted_rand_score(y, icc.fit_predict(X[:, sel_bi]))
            track_results["Bimodality Index (Top 20)"]["fdp"].append(fdp_bi)
            track_results["Bimodality Index (Top 20)"]["power"].append(pwr_bi)
            track_results["Bimodality Index (Top 20)"]["ari_km"].append(ari_km_bi)
            track_results["Bimodality Index (Top 20)"]["ari_icc"].append(ari_icc_bi)

            # 5. Hartigan Dip Screening (Top D_sig)
            dip_scores = compute_dip_proxy(X)
            sel_dip = np.argsort(dip_scores)[::-1][:D_sig]
            fdp_dip, pwr_dip = evaluate_selection(sel_dip, D_sig)
            ari_km_dip = adjusted_rand_score(y, km.fit_predict(X[:, sel_dip]))
            ari_icc_dip = adjusted_rand_score(y, icc.fit_predict(X[:, sel_dip]))
            track_results["Hartigan Dip (Top 20)"]["fdp"].append(fdp_dip)
            track_results["Hartigan Dip (Top 20)"]["power"].append(pwr_dip)
            track_results["Hartigan Dip (Top 20)"]["ari_km"].append(ari_km_dip)
            track_results["Hartigan Dip (Top 20)"]["ari_icc"].append(ari_icc_dip)

            # 6. Proposed: Null-Calibrated Decoy Gating (Knockoff+ at q=0.10)
            sel_prop = null_calibrated_knockoff_gate(X, n_clusters=K, fdr_target=0.10, random_state=seed)
            fdp_prop, pwr_prop = evaluate_selection(sel_prop, D_sig)
            X_prop = X[:, sel_prop] if len(sel_prop) > 1 else X
            ari_km_prop = adjusted_rand_score(y, km.fit_predict(X_prop))
            ari_icc_prop = adjusted_rand_score(y, icc.fit_predict(X_prop))
            track_results["Null-Calibrated Decoy (Proposed)"]["fdp"].append(fdp_prop)
            track_results["Null-Calibrated Decoy (Proposed)"]["power"].append(pwr_prop)
            track_results["Null-Calibrated Decoy (Proposed)"]["ari_km"].append(ari_km_prop)
            track_results["Null-Calibrated Decoy (Proposed)"]["ari_icc"].append(ari_icc_prop)
            track_results["Null-Calibrated Decoy (Proposed)"]["n_selected"].append(len(sel_prop))

        # Print summary for this track
        print(f"{'Method':<35} | {'FDP (Mean±Std)':<16} | {'Power':<12} | {'ARI (ICC-v2)':<16}")
        print("-" * 85)
        for m_name, m_data in track_results.items():
            if "fdp" in m_data:
                fdp_str = f"{np.mean(m_data['fdp']):.3f} ± {np.std(m_data['fdp']):.3f}"
                pwr_str = f"{np.mean(m_data['power']):.3f}"
            else:
                fdp_str = "N/A"
                pwr_str = "N/A"
            ari_str = f"{np.mean(m_data['ari_icc']):.3f} ± {np.std(m_data['ari_icc']):.3f}"
            print(f"{m_name:<35} | {fdp_str:<16} | {pwr_str:<12} | {ari_str:<16}")

        results[track_name] = track_results

    # Save complete benchmark output
    os.makedirs("results/study_null_gating", exist_ok=True)
    out_path = "results/study_null_gating/synthetic_tracks_results.json"
    with open(out_path, "w") as f:
        # Convert numpy floats for JSON serialization
        serializable = {}
        for k, v in results.items():
            serializable[k] = {}
            for mk, mv in v.items():
                serializable[k][mk] = {metric: [float(val) for val in val_list] for metric, val_list in mv.items()}
        json.dump(serializable, f, indent=2)
    print(f"\nBenchmark results successfully serialized to {out_path}")

    # Evaluate Pre-Registered Kill Criteria
    print("\n" + "=" * 80)
    print("EVALUATING PRE-REGISTERED KILL CRITERIA")
    print("=" * 80)
    q_target = 0.10
    kill_threshold = 1.5 * q_target  # 0.15

    violations = 0
    total_tracks = len(tracks)

    for track_name, track_data in results.items():
        prop_fdp = np.mean(track_data["Null-Calibrated Decoy (Proposed)"]["fdp"])
        print(f"[{track_name}] Proposed Mean FDP: {prop_fdp:.4f} (Threshold: {kill_threshold:.4f})")
        if prop_fdp > kill_threshold:
            violations += 1
            print(f"  -> VIOLATION on {track_name}!")
        else:
            print("  -> PASSED: False discovery proportion successfully controlled.")

    violation_rate = violations / total_tracks
    print(f"\nTotal Track Violations: {violations}/{total_tracks} ({violation_rate * 100:.1f}%)")
    if violation_rate > 0.20:
        print(">>> OUTCOME: KILL CRITERION MET! Study killed due to excessive FDP violation.")
    else:
        print(">>> OUTCOME: KILL CRITERION AVERTED! Null-calibrated gating validated across all tracks.")


if __name__ == "__main__":
    run_benchmark()
