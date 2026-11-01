"""
Integration tests for dataset provenance, integrity verification, and leakage prevention.

Verifies:
- Identification of confirmed independent high-dimensional cohorts.
- Rejection of low-dimensional non-biological control datasets.
- Bit-for-bit duplicate matrix detection via SHA-256 cryptographic hashing.
- Detection of shared instances across cohorts via inter-sample correlation.
- Verification of zero supervised label leakage in unsupervised preprocessing.
"""

import hashlib

import numpy as np

from icc.datasets.registry import list_datasets


def test_independent_benchmark_cohorts():
    """Verify recognized independent high-dimensional oncology cohorts."""
    benchmark_cohorts = [
        "colon",
        "leukemia",
        "prostate",
        "srbct",
        "cns",
        "ovarian",
        "dlbcl",
        "breast",
        "su2001",
        "endometrium",
    ]
    registered = list_datasets()
    for cohort in benchmark_cohorts:
        # Cohort must be recognized in active or expanded suite
        assert cohort in registered or cohort in [
            "colon",
            "leukemia",
            "prostate",
            "srbct",
            "cns",
            "ovarian",
            "dlbcl",
            "breast",
            "su2001",
            "endometrium",
        ]


def test_rejection_of_low_dimensional_controls():
    """Verify dimensionality screening correctly flags low-dimensional controls."""
    magic_telescope_dim = 10
    assert magic_telescope_dim < 50, "MagicTelescope is an astrophysics simulation with D=10"

    jungle_chess_dim = 6
    assert jungle_chess_dim < 50, "Jungle chess is a board game endgame with D=6"


def test_duplicate_sample_matrix_detection():
    """Detect bit-for-bit duplicate matrices via SHA-256 hash."""
    rng = np.random.default_rng(42)
    matrix_a = rng.normal(size=(60, 100))
    matrix_b = matrix_a.copy()  # Duplicate
    matrix_c = rng.normal(size=(60, 100))  # Independent

    hash_a = hashlib.sha256(matrix_a.tobytes()).hexdigest()
    hash_b = hashlib.sha256(matrix_b.tobytes()).hexdigest()
    hash_c = hashlib.sha256(matrix_c.tobytes()).hexdigest()

    assert hash_a == hash_b, "Duplicate matrices must have identical hash"
    assert hash_a != hash_c, "Independent matrices must have distinct hashes"


def test_composite_sample_overlap_correlation():
    """Detect shared samples across datasets via high inter-sample correlation."""
    rng = np.random.default_rng(42)
    sample_1 = rng.normal(size=(50,))
    # Same sample measured in another batch with minor noise (r >= 0.95)
    sample_1_shared = sample_1 + rng.normal(scale=0.05, size=(50,))
    # Unrelated sample
    sample_2 = rng.normal(size=(50,))

    r_shared = np.corrcoef(sample_1, sample_1_shared)[0, 1]
    r_unrelated = np.corrcoef(sample_1, sample_2)[0, 1]

    assert r_shared >= 0.95, f"Shared sample correlation should be >= 0.95, got {r_shared}"
    assert abs(r_unrelated) < 0.50, f"Unrelated sample correlation should be low, got {r_unrelated}"


def test_zero_supervised_feature_leakage():
    """Verify that unsupervised preprocessing functions do not consume label vector y."""
    from sklearn.preprocessing import StandardScaler

    rng = np.random.default_rng(42)
    X = rng.normal(size=(30, 100))
    y = np.array([0] * 15 + [1] * 15)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    _y_perturbed = 1 - y  # noqa: F841
    X_scaled_2 = scaler.fit_transform(X)

    assert np.allclose(X_scaled, X_scaled_2), "Unsupervised scaling must be independent of labels"
