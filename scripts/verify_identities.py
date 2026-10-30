"""
Mathematical verification suite for Proposition 2: Exact Sample Determinacy Identity.

Verifies the mathematical equivalence between dense quadratic co-association accumulation
and the O(N * M^2) contingency matrix determinacy identity.

Mathematical Formulation:
--------------------------
Given an ensemble of M partitions {pi_m}_{m=1}^M of N samples into K clusters, the
pairwise co-association matrix S has entries:
    S_ij = (1 / M) * sum_{m=1}^M I(pi_m(i) == pi_m(j))

The determinacy score d_i of sample i measures the consistency of its cluster co-membership:
    d_i = (1 / (N - 1)) * sum_{j != i} S_ij^2

Direct computation requires forming the full N x N dense matrix S in O(N^2) memory.
Proposition 2 proves that the full squared row sum obeys the contingency-matrix identity:
    sum_{j=1}^N S_ij^2 = (1 / M^2) * sum_{m1=1}^M sum_{m2=1}^M C_{m1, m2}(pi_m1(i), pi_m2(i))

where C_{m1, m2} is the K x K contingency table counting joint cluster assignments between
base partition m1 and base partition m2. This identity allows exact computation of d_i in
O(N * M^2 + M^2 * K^2) operations and O(N + K^2) memory without ever instantiating S.

Verification Process:
---------------------
1. Generates random partition ensembles across diverse (N, M, K) configurations.
2. Constructs the brute-force dense N x N matrix S and sums squared off-diagonal entries.
3. Computes the contingency matrix identity across all partition pairs.
4. Asserts that the maximum absolute numerical discrepancy is strictly bounded below 1e-12.
5. Tests degenerate boundaries: M=1, K=N, and identical repeated partitions.

Outputs:
--------
Console audit log with PASS/FAIL status for each test case.

Usage:
------
    python scripts/verify_identities.py
"""

import numpy as np


def verify_identity_case(N: int, M: int, K: int, seed: int = 42):
    """
    Evaluate Proposition 2 discrepancy for a specific (N, M, K) configuration.

    Parameters
    ----------
    N : int
        Number of samples.
    M : int
        Number of base partitions in the consensus ensemble.
    K : int
        Number of clusters per partition.
    seed : int, default=42
        Random seed for reproducible partition generation.

    Returns
    -------
    tuple of float
        (max_diff_full_sum, max_diff_determinacy)
    """
    rng = np.random.default_rng(seed)

    # Generate random partitions: M x N with labels in {0, ..., K-1}
    P_stack = rng.integers(0, K, size=(M, N))

    # 1. Brute-force dense co-association matrix S: (N x N)
    S = np.zeros((N, N), dtype=np.float64)
    for m in range(M):
        S += (P_stack[m, :, None] == P_stack[m, None, :]).astype(np.float64)
    S /= M

    # 2. Direct calculation of sample determinacy: sum_{j != i} S_ij^2
    np.fill_diagonal(S, 0.0)  # Exclude self-co-association
    det_direct = np.sum(S ** 2, axis=1) / max(1, N - 1)

    # Full row sum including diagonal self-match (S_ii = 1.0)
    S_full = S.copy()
    np.fill_diagonal(S_full, 1.0)
    full_sum_sq_direct = np.sum(S_full ** 2, axis=1)

    # 3. Proposition 2: Contingency matrix closed-form formulation
    full_sum_sq_identity = np.zeros(N, dtype=np.float64)
    for m1 in range(M):
        for m2 in range(M):
            joint = P_stack[m1] * K + P_stack[m2]
            counts = np.bincount(joint, minlength=K * K)
            full_sum_sq_identity += counts[joint]
    full_sum_sq_identity /= (M ** 2)

    # Subtract self-diagonal match S_ii^2 = 1.0 and normalize by (N - 1)
    det_identity = np.maximum(0.0, (full_sum_sq_identity - 1.0) / max(1, N - 1))

    # Numerical discrepancies
    diff_full_sum = float(np.max(np.abs(full_sum_sq_direct - full_sum_sq_identity)))
    diff_det = float(np.max(np.abs(det_direct - det_identity)))

    return diff_full_sum, diff_det


def run_all_checks():
    """
    Run the full test suite of mathematical verification cases for Proposition 2.
    """
    test_cases = [
        # (N, M, K, description)
        (10, 5, 2, "Tiny K=2"),
        (25, 10, 3, "Small K=3"),
        (50, 25, 4, "Standard M=25, K=4"),
        (100, 15, 8, "Moderate K=8"),
        (200, 30, 2, "Binary K=2, M=30"),
        (15, 20, 15, "Edge case K=N"),
        (30, 1, 3, "Edge case M=1"),
        (50, 50, 5, "Large M=50"),
    ]

    print("=" * 75)
    print("MATHEMATICAL AUDIT: PROPOSITION 2 CONTINGENCY IDENTITY VERIFICATION")
    print("=" * 75)

    all_passed = True
    for N, M, K, desc in test_cases:
        diff_full, diff_det = verify_identity_case(N, M, K, seed=123)
        passed = (diff_full < 1e-12 and diff_det < 1e-12)
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        print(f"[{status}] {desc:<25} (N={N:3d}, M={M:2d}, K={K:2d}): max_diff_full={diff_full:.2e}, max_diff_det={diff_det:.2e}")

    # Degenerate case: Identical ensemble partitions across all base models
    rng = np.random.default_rng(999)
    P_identical = np.tile(rng.integers(0, 3, size=(1, 40)), (10, 1))

    S_ident = np.zeros((40, 40))
    for m in range(10):
        S_ident += (P_identical[m, :, None] == P_identical[m, None, :]).astype(float)
    S_ident /= 10
    np.fill_diagonal(S_ident, 0.0)
    det_ident_direct = np.sum(S_ident ** 2, axis=1) / 39

    full_ident = np.zeros(40)
    for m1 in range(10):
        for m2 in range(10):
            joint = P_identical[m1] * 3 + P_identical[m2]
            counts = np.bincount(joint, minlength=9)
            full_ident += counts[joint]
    det_ident_id = np.maximum(0.0, (full_ident / 100.0 - 1.0) / 39)
    diff_ident = float(np.max(np.abs(det_ident_direct - det_ident_id)))

    ident_passed = diff_ident < 1e-12
    print(f"[{'PASS' if ident_passed else 'FAIL'}] Degenerate (Identical M)   (N= 40, M=10, K= 3): max_diff={diff_ident:.2e}")

    assert all_passed and ident_passed, "Proposition 2 verification failed numerical tolerance!"
    print("\n[+] ALL PROPOSITION 2 IDENTITY CHECKS VERIFIED MATHEMATICALLY (Discrepancy < 1e-12)!\n")


if __name__ == "__main__":
    run_all_checks()
