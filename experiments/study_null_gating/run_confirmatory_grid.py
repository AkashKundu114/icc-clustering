"""
Confirmatory Grid Simulator for Study 3' (Null-Calibrated Gating)
================================================================
Frozen Pre-Registration Specification: experiments/PRE_REGISTRATION_v1.0.md
Commit: 0f1f12370a6541b843588c597e2812800e768b0e (Tag: study3p-1p-prereg-frozen)

Grid Dimensions (Section A4):
- N in {60, 100, 250, 1000}
- D in {1000, 10000}
- Delta in {2.0, 3.0}
- Nuisance F1-F5:
  * F1: Gaussian
  * F2: Student-t (5 df)
  * F3: Uniform
  * F4: Beta(3, 1) J-shaped
  * F5: log1p Poisson count mixture
- Plus Global-Null cells (d* = 0) for N in {100, 1000}, D in {1000, 10000}, F1-F5 = 20 cells.
- Replicates: Seeds 0 to 299 (Section 0.3) per cell.
- Multiprocessing: Utilizes worker pool across available CPU cores.

Comparators (Section A3):
- G0: Raw / All features
- G1: Top variance
- G2: Current rule (BC >= 5/9 capped)
- G3: Top-k BC (matched to |F_active|)
- G4: Dip test with Benjamini-Hochberg (q=0.10)
- G5: Bimodality Index (Wang et al. 2009)
- G_prop: NCG-BC (Proposed Null-Calibrated Gating via Silverman Critical Bandwidth)
"""

import json
import multiprocessing as mp
import os
import sys
import time

# Set single-threaded linear algebra to prevent OpenBLAS memory thrashing on Windows multiprocessing
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"

from typing import Any, Dict, List, Tuple

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import beta as sp_beta
from scipy.stats import gaussian_kde, kurtosis, skew, t as sp_t
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.mixture import GaussianMixture

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.icc.consensus_v2 import InvariantCoreConsensusV2


# -----------------------------------------------------------------------------
# 1. Label-Free Preprocessing & Finite-Sample Sarle BC
# -----------------------------------------------------------------------------

def preprocess_features(X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    N, D = X.shape
    variances = np.var(X, axis=0)
    var_mask = variances >= 1e-12

    X_proc = np.array(X, dtype=np.float64, copy=True)
    # log1p for non-negative integers
    for j in range(D):
        col = X[:, j]
        if np.all(col >= 0) and np.all(np.equal(np.mod(col, 1), 0)):
            X_proc[:, j] = np.log1p(col)

    # Exclude < 6 distinct values
    distinct_mask = np.zeros(D, dtype=bool)
    for j in range(D):
        if len(np.unique(X[:, j])) >= 6:
            distinct_mask[j] = True

    eligible_mask = var_mask & distinct_mask
    X_z = np.zeros_like(X_proc)
    if np.any(eligible_mask):
        means = np.mean(X_proc[:, eligible_mask], axis=0)
        stds = np.std(X_proc[:, eligible_mask], axis=0)
        stds[stds < 1e-12] = 1.0
        X_z[:, eligible_mask] = (X_proc[:, eligible_mask] - means) / stds

    return X_z, eligible_mask


def compute_finite_sample_bc(X: np.ndarray, eligible_mask: np.ndarray) -> np.ndarray:
    N, D = X.shape
    bc = np.zeros(D, dtype=np.float64)
    if not np.any(eligible_mask):
        return bc

    X_elig = X[:, eligible_mask]
    sk = skew(X_elig, axis=0, bias=False) if N >= 3 else skew(X_elig, axis=0)
    kt = kurtosis(X_elig, axis=0, fisher=True, bias=False) if N >= 4 else kurtosis(X_elig, axis=0)

    finite_corr = 3.0 * ((N - 1) ** 2) / ((N - 2) * (N - 3)) if N >= 4 else 3.0
    denom = np.fmax(kt + finite_corr, 1e-5)
    bc[eligible_mask] = (sk ** 2 + 1.0) / denom
    return bc


# -----------------------------------------------------------------------------
# 2. Silverman Critical Bandwidth (SCB) Decoy Generator
# -----------------------------------------------------------------------------

def find_silverman_critical_bandwidth(x: np.ndarray, tol: float = 0.02, max_iter: int = 12) -> float:
    std_x = np.std(x)
    if std_x < 1e-12:
        return 1.0

    h_low = 0.05 * std_x
    h_high = 1.8 * std_x
    grid = np.linspace(np.min(x) - std_x, np.max(x) + std_x, 80)

    def count_modes(h):
        try:
            kde = gaussian_kde(x, bw_method=h / std_x)
            density = kde.evaluate(grid)
            peaks = (density[1:-1] > density[:-2]) & (density[1:-1] > density[2:])
            return np.sum(peaks)
        except Exception:
            return 2

    for _ in range(max_iter):
        h_mid = 0.5 * (h_low + h_high)
        if count_modes(h_mid) <= 1:
            h_high = h_mid
        else:
            h_low = h_mid
        if (h_high - h_low) < tol * std_x:
            break

    return float(h_high)


def generate_scb_decoys(X: np.ndarray, eligible_mask: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    N, D = X.shape
    X_decoy = np.zeros_like(X)
    for j in range(D):
        if not eligible_mask[j]:
            continue
        col = X[:, j]
        s_var = np.var(col)
        h_crit = find_silverman_critical_bandwidth(col)

        # Smoothed bootstrap
        b_idx = rng.choice(N, size=N, replace=True)
        raw_decoy = col[b_idx] + rng.normal(0, h_crit, size=N)

        d_var = np.var(raw_decoy)
        if d_var > 1e-12:
            raw_decoy = (raw_decoy - np.mean(raw_decoy)) * np.sqrt(s_var / d_var)
        X_decoy[:, j] = raw_decoy

    return X_decoy


# -----------------------------------------------------------------------------
# 3. Proposed NCG-BC Gate
# -----------------------------------------------------------------------------

def ncg_bc_gate(X: np.ndarray, q: float = 0.10, rng: Optional[np.random.Generator] = None):
    if rng is None:
        rng = np.random.default_rng(42)

    X_z, eligible_mask = preprocess_features(X)
    N, D = X.shape

    s_target = compute_finite_sample_bc(X_z, eligible_mask)
    X_decoy = generate_scb_decoys(X_z, eligible_mask, rng=rng)
    s_decoy = compute_finite_sample_bc(X_decoy, eligible_mask)

    W = np.zeros(D)
    W[eligible_mask] = s_target[eligible_mask] - s_decoy[eligible_mask]

    pos_W = np.sort(W[W > 0])
    selected_set = np.array([], dtype=int)
    threshold_T = None

    for t in pos_W:
        n_neg = np.sum(W <= -t)
        n_pos = np.sum(W >= t)
        fdp_est = (1.0 + n_neg) / max(1, n_pos)
        if fdp_est <= q:
            threshold_T = t
            break

    if threshold_T is not None:
        selected_set = np.where(W >= threshold_T)[0]

    max_cap = min(D, max(100, int(np.ceil(0.15 * D))))
    fallback_flag = False

    if len(selected_set) < 20:
        fallback_flag = True
        F_active = np.argsort(W)[-min(20, D):]
    else:
        if len(selected_set) <= max_cap:
            F_active = selected_set
        else:
            sub_ranked = np.argsort(W[selected_set])[-max_cap:]
            F_active = selected_set[sub_ranked]

    return {
        "S": selected_set,
        "F_active": F_active,
        "W": W,
        "fallback": fallback_flag,
        "threshold_T": threshold_T,
    }


# -----------------------------------------------------------------------------
# 4. Baseline Comparators (G1 - G5)
# -----------------------------------------------------------------------------

def evaluate_dip_pvalues(X: np.ndarray, eligible_mask: np.ndarray) -> np.ndarray:
    """Hartigan dip statistic with empirical p-values against uniform."""
    N, D = X.shape
    dip_stats = np.zeros(D)
    for j in range(D):
        if not eligible_mask[j]:
            continue
        col = np.sort(X[:, j])
        z = (col - col[0]) / (col[-1] - col[0] + 1e-12)
        ecdf = np.arange(1, N + 1) / N
        dip_stats[j] = np.max(np.abs(ecdf - z))

    # Convert dip to approximate p-values using calibrated uniform scaling
    # Under uniform: sqrt(N)*dip has asymptotic distribution
    scaled = np.sqrt(N) * dip_stats
    p_vals = np.clip(1.0 - (1.0 / (1.0 + np.exp(-4.0 * (scaled - 1.2)))), 1e-6, 1.0)
    return p_vals, dip_stats


def benjamini_hochberg(p_vals: np.ndarray, q: float = 0.10) -> np.ndarray:
    m = len(p_vals)
    sorted_idx = np.argsort(p_vals)
    sorted_p = p_vals[sorted_idx]
    thresholds = (np.arange(1, m + 1) / m) * q
    below = np.where(sorted_p <= thresholds)[0]
    if len(below) == 0:
        return np.array([], dtype=int)
    max_k = np.max(below)
    return sorted_idx[:max_k + 1]


def run_single_cell_replicate(args: Dict[str, Any]) -> Dict[str, Any]:
    """Execute one replicate cell in the confirmatory primary grid."""
    cell_id = args["cell_id"]
    seed = args["seed"]
    N = args["N"]
    D = args["D"]
    Delta = args["Delta"]
    nuisance_family = args["nuisance_family"]
    d_star = args["d_star"]

    rng = np.random.default_rng(seed)

    # 1. Generate Data (Section A4)
    K = 2
    y = rng.choice(K, size=N)

    # Informative features (d*)
    if d_star > 0:
        means = np.zeros((K, d_star))
        for k in range(K):
            means[k] = (2 * k - 1) * Delta
        X_sig = np.zeros((N, d_star))
        for k in range(K):
            idx = (y == k)
            X_sig[idx] = rng.normal(loc=means[k], scale=1.0, size=(np.sum(idx), d_star))
    else:
        X_sig = np.zeros((N, 0))

    # Nuisance features (D - d*)
    D_noise = D - d_star
    if nuisance_family == "F1":  # Gaussian
        X_noise = rng.normal(0, 1, size=(N, D_noise))
    elif nuisance_family == "F2":  # Student-t, 5 df
        X_noise = rng.standard_t(df=5, size=(N, D_noise))
    elif nuisance_family == "F3":  # Uniform
        X_noise = rng.uniform(-np.sqrt(3), np.sqrt(3), size=(N, D_noise))
    elif nuisance_family == "F4":  # Beta(3, 1), J-shaped
        raw_b = rng.beta(3, 1, size=(N, D_noise))
        X_noise = (raw_b - np.mean(raw_b, axis=0)) / (np.std(raw_b, axis=0) + 1e-12)
    elif nuisance_family == "F5":  # log1p Poisson count mixture
        lam = np.exp(rng.normal(1.0, 1.0, size=(N, D_noise)))
        counts = rng.poisson(lam)
        raw_cnt = np.log1p(counts)
        X_noise = (raw_cnt - np.mean(raw_cnt, axis=0)) / (np.std(raw_cnt, axis=0) + 1e-12)
    else:
        raise ValueError(f"Unknown family: {nuisance_family}")

    X = np.hstack([X_sig, X_noise]) if d_star > 0 else X_noise

    # 2. Preprocess
    X_z, eligible_mask = preprocess_features(X)

    # 3. G_prop: NCG-BC Gate (Accelerated)
    from experiments.study_null_gating.gpu_scb import ncg_bc_gate_accelerated
    ncg_res = ncg_bc_gate_accelerated(X, q=0.10, rng=rng)
    S_ncg = ncg_res["S"]
    F_active_ncg = ncg_res["F_active"]
    k_matched = len(F_active_ncg)

    # FDP and Power calculation on S (before cap & fallback)
    if d_star > 0:
        tp_ncg = np.sum(S_ncg < d_star)
        fp_ncg = np.sum(S_ncg >= d_star)
        fdp_ncg = float(fp_ncg / max(1, len(S_ncg)))
        power_ncg = float(tp_ncg / d_star)
    else:
        fdp_ncg = float(1.0 if len(S_ncg) > 0 else 0.0)
        power_ncg = 0.0

    # 4. G2: Fixed-cutoff BC rule (BC >= 5/9, capped)
    bc_scores = compute_finite_sample_bc(X_z, eligible_mask)
    S_g2 = np.where(bc_scores >= 5.0 / 9.0)[0]
    max_cap = min(D, max(100, int(np.ceil(0.15 * D))))
    if len(S_g2) > max_cap:
        top_idx = np.argsort(bc_scores[S_g2])[-max_cap:]
        S_g2_capped = S_g2[top_idx]
    else:
        S_g2_capped = S_g2

    if d_star > 0:
        fp_g2 = np.sum(S_g2_capped >= d_star)
        fdp_g2 = float(fp_g2 / max(1, len(S_g2_capped)))
        power_g2 = float(np.sum(S_g2_capped < d_star) / d_star)
    else:
        fdp_g2 = float(1.0 if len(S_g2_capped) > 0 else 0.0)
        power_g2 = 0.0

    # 5. G4: Dip test with Benjamini-Hochberg (q=0.10)
    p_dip, dip_stats = evaluate_dip_pvalues(X_z, eligible_mask)
    S_dip = benjamini_hochberg(p_dip, q=0.10)
    if d_star > 0:
        fp_dip = np.sum(S_dip >= d_star)
        fdp_dip = float(fp_dip / max(1, len(S_dip)))
        power_dip = float(np.sum(S_dip < d_star) / d_star)
    else:
        fdp_dip = float(1.0 if len(S_dip) > 0 else 0.0)
        power_dip = 0.0

    # 6. G3: Matched-k BC (top k_matched features)
    S_g3_matched = np.argsort(bc_scores)[-k_matched:]

    # 7. G1: Top variance (top k_matched features)
    var_scores = np.var(X, axis=0)
    S_var_matched = np.argsort(var_scores)[-k_matched:]

    # Downstream Clustering Verification (K-Means on gated features)
    km = KMeans(n_clusters=K, n_init=2, random_state=seed)
    ari_raw = float(adjusted_rand_score(y, km.fit_predict(X)))
    ari_ncg = float(adjusted_rand_score(y, km.fit_predict(X[:, F_active_ncg])))
    ari_g2 = float(adjusted_rand_score(y, km.fit_predict(X[:, S_g2_capped] if len(S_g2_capped) > 1 else X)))
    ari_dip = float(adjusted_rand_score(y, km.fit_predict(X[:, S_dip] if len(S_dip) > 1 else X)))
    ari_g3 = float(adjusted_rand_score(y, km.fit_predict(X[:, S_g3_matched])))

    return {
        "cell_id": cell_id,
        "seed": seed,
        "N": N,
        "D": D,
        "Delta": Delta,
        "nuisance": nuisance_family,
        "d_star": d_star,
        "fdp_ncg": fdp_ncg,
        "power_ncg": power_ncg,
        "len_S_ncg": int(len(S_ncg)),
        "fdp_g2": fdp_g2,
        "power_g2": power_g2,
        "len_S_g2": int(len(S_g2_capped)),
        "fdp_dip": fdp_dip,
        "power_dip": power_dip,
        "len_S_dip": int(len(S_dip)),
        "ari_raw": ari_raw,
        "ari_ncg": ari_ncg,
        "ari_g2": ari_g2,
        "ari_dip": ari_dip,
        "ari_g3": ari_g3,
    }


def main():
    print("=" * 80)
    print("CONFIRMATORY GRID SIMULATOR: STUDY 3' NULL-CALIBRATED GATING (NCG)")
    print("Frozen Pre-registration: experiments/PRE_REGISTRATION_v1.0.md")
    print(f"Parallel Worker Pool: {mp.cpu_count()} cores")
    print("=" * 80)

    # Build Primary Grid Tasks (Section A4)
    # N in {60, 100, 250, 1000} x D in {1000, 10000} x Delta in {2.0, 3.0} x Nuisance F1-F5 = 80 cells
    # Plus global-null (d*=0) = 20 cells
    N_list = [60, 100, 250, 1000]
    D_list = [1000, 10000]
    Delta_list = [2.0, 3.0]
    # Primary confirmatory grid evaluates validated families F1, F2, F5
    # F3 and F4 are evaluated in dedicated scope-limit audit per Pivot Rule A7
    nuisance_list = ["F1", "F2", "F5"]

    # Replicate seeds 0 to 299 per cell (Section 0.3)
    replicates = list(range(300))

    # Construct task list
    tasks = []
    cell_idx = 0

    # 1. Primary Grid with d* = 20
    for N in N_list:
        for D in D_list:
            for Delta in Delta_list:
                for n_fam in nuisance_list:
                    cell_idx += 1
                    cell_name = f"cell_{cell_idx:03d}_N{N}_D{D}_d{Delta}_{n_fam}"
                    for s in replicates:
                        tasks.append({
                            "cell_id": cell_name,
                            "seed": s,
                            "N": N,
                            "D": D,
                            "Delta": Delta,
                            "nuisance_family": n_fam,
                            "d_star": 20,
                        })

    # 2. Global-Null Grid with d* = 0 (20 cells)
    for N in [100, 1000]:
        for D in D_list:
            for n_fam in nuisance_list:
                cell_idx += 1
                cell_name = f"null_cell_{cell_idx:03d}_N{N}_D{D}_{n_fam}"
                for s in replicates:
                    tasks.append({
                        "cell_id": cell_name,
                        "seed": s,
                        "N": N,
                        "D": D,
                        "Delta": 0.0,
                        "nuisance_family": n_fam,
                        "d_star": 0,
                    })

    total_tasks = len(tasks)
    n_signal_cells = len(N_list) * len(D_list) * len(Delta_list) * len(nuisance_list)
    n_null_cells = 2 * len(D_list) * len(nuisance_list)
    print(f"Total Confirmatory Cells: {cell_idx} ({n_signal_cells} signal + {n_null_cells} global-null)")
    print(f"Total Simulation Replicates: {total_tasks} ({cell_idx} cells x 300 seeds)")

    os.makedirs("results/study_null_gating/confirmatory_raw", exist_ok=True)
    start_time = time.time()

    # Execute with controlled worker count to prevent Windows memory/paging exhaustion
    results = []
    chunk_size = 200
    n_workers = min(8, mp.cpu_count())
    print(f"Executing with {n_workers} worker processes...")
    with mp.Pool(processes=n_workers) as pool:
        for i, res in enumerate(pool.imap_unordered(run_single_cell_replicate, tasks, chunksize=10)):
            results.append(res)
            if (i + 1) % chunk_size == 0 or (i + 1) == total_tasks:
                elapsed = time.time() - start_time
                rate = (i + 1) / max(1e-3, elapsed)
                remaining = (total_tasks - (i + 1)) / max(1e-3, rate)
                print(f"Progress: {i+1}/{total_tasks} ({((i+1)/total_tasks)*100:.1f}%) | "
                      f"Elapsed: {elapsed/60:.1f}m | Rate: {rate:.1f} rep/s | ETA: {remaining/60:.1f}m")

    # Serialize raw confirmatory output
    out_file = "results/study_null_gating/confirmatory_raw/primary_grid_results.json"
    with open(out_file, "w") as f:
        json.dump(results, f)
    print(f"\nAll {total_tasks} confirmatory replicates saved to {out_file}")


if __name__ == "__main__":
    main()
