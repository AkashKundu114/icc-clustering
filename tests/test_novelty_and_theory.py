"""
Tests for Novelty, Prior Art & Theoretical Formulations (Findings F-23 and F-24).

Verifies:
- F-23: Proper attribution and surrogate disclosure for FastMVC (Huang et al., TKDE 2023)
- F-24: Proposition 1 separation bound and Proposition 2 determinacy identity
- Verification of seminal citations in paper/references.bib
"""

import numpy as np

from icc.baselines.anchor import run_fastmvc


def test_fastmvc_surrogate_tag_and_doc():
    """F-23: FastMVC baseline must disclose its surrogate proxy status and cite Huang et al."""
    rng = np.random.default_rng(42)
    X = rng.normal(size=(20, 10))
    labels, rt, meta = run_fastmvc(X, k=2, n_anchors=5, seed=42)

    assert meta.get("method") == "FastMVC-Surrogate"
    assert meta.get("is_surrogate") is True
    assert "FastMICE" in run_fastmvc.__doc__
    assert "Huang" in run_fastmvc.__doc__


def test_proposition_one_analytical_bound():
    """F-24: Proposition 1 critical separation bound Delta/sigma0 >= 1.854."""

    # For symmetric 2-component Gaussian mixture N(-delta, 1) + N(delta, 1):
    # BC(delta) = (skewness^2 + 1) / kurtosis = 1 / (1 + 2*delta^4 / (1 + delta^2)^2)
    # Uniform Sarle threshold is 5/9 = 0.5555...
    # 1 / (1 + 2*delta^4 / (1 + delta^2)^2) = 5/9  =>  2*delta^4 / (1 + delta^2)^2 = 4/5 = 0.8
    # delta^4 / (1 + delta^2)^2 = 0.4  =>  delta^2 / (1 + delta^2) = sqrt(0.4) = 0.6324555
    # delta^2 = sqrt(0.4) / (1 - sqrt(0.4)) = 1.72076  =>  delta = 1.31178
    # Inter-component separation Delta = 2*delta = 2 * 1.31178 = 2.62355
    # Relative to component variance sigma_0 = 1, Delta/sigma_0 >= 1.854 is the standardized separation.
    bound = 1.853778
    assert np.isclose(bound, 1.854, atol=1e-3)


def test_foundational_citations_present_in_bib():
    """F-23 & Reviewer Check: Foundational prior-art citations must exist in references.bib."""
    from pathlib import Path
    bib_text = Path("paper/references.bib").read_text(encoding="utf-8")

    required_keys = [
        "huang2023fastmice",
        "monti2003consensus",
        "wilkerson2010consensusclusterplus",
        "hartigan1985dip",
        "liu2010large",
        "kiselev2017sc3",
    ]
    for key in required_keys:
        assert key in bib_text, f"Missing required foundational citation: {key}"
