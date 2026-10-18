"""
GPU-Accelerated Silverman Critical Bandwidth (SCB) and NCG-BC Gate
==================================================================
Batched parallel 1D Gaussian KDE and bisection in PyTorch.
Evaluates all D features simultaneously in chunked batched tensor operations.
Automatically detects and utilizes CUDA GPU if available, falling back gracefully
to vectorized CPU tensor operations.
"""

from typing import Dict, Any, Optional
import numpy as np
import torch


def compute_scb_bandwidths_torch(
    X_t: torch.Tensor,
    tol: float = 0.02,
    max_iter: int = 12,
    n_grid: int = 80,
    chunk_size: int = 2000,
) -> torch.Tensor:
    """
    Computes Silverman critical bandwidth for all D features in X_t (shape: [N, D]).
    Uses chunked batched 3D tensor operations to maximize throughput and keep VRAM lean.
    """
    N, D = X_t.shape
    device = X_t.device
    dtype = X_t.dtype

    # Standard deviation per feature (unbiased)
    std_x = torch.std(X_t, dim=0, unbiased=True)  # [D]
    valid_mask = std_x > 1e-12

    h_crit = torch.ones(D, device=device, dtype=dtype)
    valid_indices = torch.where(valid_mask)[0]

    if len(valid_indices) == 0:
        return h_crit

    for start_idx in range(0, len(valid_indices), chunk_size):
        idx_chunk = valid_indices[start_idx : start_idx + chunk_size]
        X_sub = X_t[:, idx_chunk]  # [N, C]
        std_sub = std_x[idx_chunk]  # [C]
        C = len(idx_chunk)

        h_low = 0.05 * std_sub  # [C]
        h_high = 1.8 * std_sub  # [C]

        min_x = torch.min(X_sub, dim=0).values  # [C]
        max_x = torch.max(X_sub, dim=0).values  # [C]

        # Grids: shape [C, n_grid]
        grid_steps = torch.linspace(0, 1, n_grid, device=device, dtype=dtype).unsqueeze(0)  # [1, n_grid]
        grid_start = (min_x - std_sub).unsqueeze(1)  # [C, 1]
        grid_end = (max_x + std_sub).unsqueeze(1)  # [C, 1]
        grids = grid_start + grid_steps * (grid_end - grid_start)  # [C, n_grid]

        # X_sub transposed: shape [C, N]
        X_T = X_sub.t()  # [C, N]

        # Precompute pairwise squared difference: (grids[:, :, None] - X_T[:, None, :])^2
        # Shape: [C, n_grid, N]
        diff_sq = (grids.unsqueeze(2) - X_T.unsqueeze(1)) ** 2

        for _ in range(max_iter):
            h_mid = 0.5 * (h_low + h_high)  # [C]
            var_2h = (2.0 * (h_mid ** 2)).unsqueeze(1).unsqueeze(2)  # [C, 1, 1]

            # Gaussian kernel exponent & summation over samples
            exp_term = torch.exp(-diff_sq / var_2h)  # [C, n_grid, N]
            density = exp_term.sum(dim=2)  # [C, n_grid]

            # Detect peaks (local maxima)
            peaks = (density[:, 1:-1] > density[:, :-2]) & (density[:, 1:-1] > density[:, 2:])
            num_peaks = peaks.sum(dim=1)  # [C]

            # Update bisection bounds
            is_unimodal = num_peaks <= 1
            h_high = torch.where(is_unimodal, h_mid, h_high)
            h_low = torch.where(is_unimodal, h_low, h_mid)

            if torch.all((h_high - h_low) < tol * std_sub):
                break

        h_crit[idx_chunk] = h_high

    return h_crit


def get_safe_device() -> torch.device:
    """Strictly enforces CUDA GPU device (RTX 5060) execution."""
    if not torch.cuda.is_available():
        raise RuntimeError("GPU acceleration requested ('use only gpu') but torch.cuda.is_available() is False!")
    dev = torch.device("cuda:0")
    # Quick probe to ensure CUDA memory and kernel launch work
    t = torch.zeros(1, device=dev)
    _ = t + 1
    return dev


def generate_scb_decoys_torch(
    X: np.ndarray,
    eligible_mask: np.ndarray,
    rng: np.random.Generator,
    device: Optional[torch.device] = None,
) -> np.ndarray:
    """
    Generates SCB decoy features using PyTorch on the specified device.
    Preserves exact smoothed bootstrap logic:
      decoy = X[b_idx, :] + Normal(0, h_crit)
      re-standardized to match original feature variance.
    """
    if device is None:
        device = get_safe_device()

    N, D = X.shape
    X_t = torch.tensor(X, dtype=torch.float32, device=device)

    # Compute critical bandwidths for all eligible features in parallel
    h_crit_t = compute_scb_bandwidths_torch(X_t)
    h_crit = h_crit_t.cpu().numpy()

    X_decoy = np.zeros_like(X, dtype=np.float64)

    for j in range(D):
        if not eligible_mask[j]:
            continue
        col = X[:, j]
        s_var = np.var(col)
        h = float(h_crit[j])

        # Smoothed bootstrap
        b_idx = rng.choice(N, size=N, replace=True)
        raw_decoy = col[b_idx] + rng.normal(0, h, size=N)

        d_var = np.var(raw_decoy)
        if d_var > 1e-12:
            raw_decoy = (raw_decoy - np.mean(raw_decoy)) * np.sqrt(s_var / d_var)
        X_decoy[:, j] = raw_decoy

    return X_decoy


def ncg_bc_gate_accelerated(
    X: np.ndarray,
    q: float = 0.10,
    rng: Optional[np.random.Generator] = None,
    device: Optional[torch.device] = None,
) -> Dict[str, Any]:
    """
    Null-Calibrated Gating with Sarle BC and Silverman Critical Bandwidth null.
    Accelerated via GPU / parallel tensor operations.
    """
    if rng is None:
        rng = np.random.default_rng(42)

    from experiments.study_null_gating.run_confirmatory_grid import (
        preprocess_features,
        compute_finite_sample_bc,
    )

    X_z, eligible_mask = preprocess_features(X)
    N, D = X.shape

    s_target = compute_finite_sample_bc(X_z, eligible_mask)
    X_decoy = generate_scb_decoys_torch(X_z, eligible_mask, rng=rng, device=device)
    s_decoy = compute_finite_sample_bc(X_decoy, eligible_mask)

    # Mirror statistic W_j = s_j - s_tilde_j
    W = np.zeros(D, dtype=np.float64)
    W[eligible_mask] = s_target[eligible_mask] - s_decoy[eligible_mask]

    # Knockoff+ thresholding
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
