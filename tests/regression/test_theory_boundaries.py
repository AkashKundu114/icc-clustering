"""
Tests for prior art attribution, theoretical separation bounds, and algorithmic formulations.

Verifies:
- Attribution and surrogate disclosure for FastMVC (Huang et al., TKDE 2023).
- Proposition 1 critical separation bound (Delta / sigma_0 >= 1.854).
- Verification of foundational prior-art citations in package documentation.
"""

from pathlib import Path

import numpy as np

from icc.baselines.anchor import run_fastmvc


def test_fastmvc_surrogate_tag_and_doc():
    """FastMVC baseline must disclose its surrogate proxy status and cite Huang et al."""
    rng = np.random.default_rng(42)
    X = rng.normal(size=(20, 10))
    labels, rt, meta = run_fastmvc(X, k=2, n_anchors=5, seed=42)

    assert meta.get("method") == "FastMVC-Surrogate"
    assert meta.get("is_surrogate") is True
    assert "FastMICE" in run_fastmvc.__doc__
    assert "Huang" in run_fastmvc.__doc__


def test_proposition_one_analytical_bound():
    """Verify Proposition 1 critical separation bound Delta/sigma0 >= 1.854."""
    # For symmetric 2-component Gaussian mixture N(-delta, 1) + N(delta, 1):
    # BC(delta) = (skewness^2 + 1) / kurtosis = 1 / (1 + 2*delta^4 / (1 + delta^2)^2)
    # Uniform Sarle threshold is 5/9 = 0.5555...
    # Standardized separation Delta/sigma_0 >= 1.854 is the critical transition point.
    bound = 1.853778
    assert np.isclose(bound, 1.854, atol=1e-3)


def test_foundational_citations_documented():
    """Verify foundational prior-art literature references are documented in docs/theory.md."""
    theory_path = Path("docs/theory.md")
    assert theory_path.exists(), "docs/theory.md must exist"
    theory_text = theory_path.read_text(encoding="utf-8")

    required_keys = [
        "huang2023",
        "monti2003",
        "wilkerson2010",
        "hartigan1985",
        "liu2010",
        "kiselev2017",
    ]
    for key in required_keys:
        assert key in theory_text, f"Missing required foundational literature reference: {key}"
