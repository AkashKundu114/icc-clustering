"""
Verification of Sarle's Bimodality Coefficient (BC) Failure Modes and Finite-Sample Power.

Validates:
1. Population BC values for standard unimodal vs bimodal distributions:
   - Gaussian, Student-t(5), Uniform, Beta(3,1), log1p Poisson-lognormal.
2. Finite-sample detection power P(BC >= 5/9) across sample sizes N in {60, 100, 250, 1000}.
3. Maximum population BC over the skew-normal distribution family.
"""

import numpy as np
from scipy import stats


def compute_bc(x: np.ndarray) -> float:
    """Compute finite-sample corrected Sarle's Bimodality Coefficient."""
    n = len(x)
    if n < 4:
        return 0.0
    var = np.var(x, ddof=1)
    if var < 1e-12:
        return 0.0
    g = stats.skew(x, bias=False)
    k = stats.kurtosis(x, fisher=True, bias=False)
    denom = k + 3.0 * (n - 1) ** 2 / ((n - 2) * (n - 3)) + 1e-5
    denom = max(denom, 1e-5)
    return float((g**2 + 1.0) / denom)


def draw_sample(family: str, n: int, rng: np.random.Generator) -> np.ndarray:
    """Draw random sample of size n from specified distribution."""
    if family == "F1 Gaussian":
        return rng.standard_normal(n)
    if family == "F2 Student-t(5)":
        return rng.standard_t(5, n)
    if family == "F3 Uniform":
        return rng.uniform(0, 1, n)
    if family == "F4 Beta(3,1)":
        return rng.beta(3, 1, n)
    if family == "F5 log1p Poisson-lognormal":
        lam = np.exp(rng.normal(1, 1, n))
        return np.log1p(rng.poisson(lam))
    if family == "Informative D=2 (sep=2.0)":
        s = rng.choice([-1, 1], n)
        return s * 2.0 + rng.standard_normal(n)
    if family == "Informative D=3 (sep=3.0)":
        s = rng.choice([-1, 1], n)
        return s * 3.0 + rng.standard_normal(n)
    raise ValueError(f"Unknown family: {family}")


def run_simulation(n_trials: int = 2000):
    print("=" * 80)
    print("SARLE'S BIMODALITY COEFFICIENT FINITE-SAMPLE POWER & POPULATION CHECK")
    print("=" * 80)

    families = [
        "F1 Gaussian",
        "F2 Student-t(5)",
        "F3 Uniform",
        "F4 Beta(3,1)",
        "F5 log1p Poisson-lognormal",
        "Informative D=2 (sep=2.0)",
        "Informative D=3 (sep=3.0)",
    ]

    rng = np.random.default_rng(10000)
    print("\n--- Finite-Sample Corrected BC: Mean (Std) and P(BC >= 5/9) ---")
    for fam in families:
        row = []
        for n in [60, 100, 250, 1000]:
            vals = np.array([compute_bc(draw_sample(fam, n, rng)) for _ in range(n_trials)])
            row.append(f"N={n:4d}: {vals.mean():.3f} ({vals.std():.3f}) P={np.mean(vals >= 5/9):.2f}")
        print(f"{fam:28s} | " + " | ".join(row))

    print("\n--- Population BC Approximations (Large Sample N = 200,000) ---")
    for fam in families:
        x_large = draw_sample(fam, 200000, rng)
        g = float(stats.skew(x_large))
        k = float(stats.kurtosis(x_large))
        b = (g**2 + 1.0) / (k + 3.0)
        print(f"{fam:28s} | Pop BC = {b:.4f} | Skewness = {g:+.3f} | Excess Kurtosis = {k:+.3f}")

    print("\n--- Optimization: Maximum Population BC over Skew-Normal Family ---")
    alphas = np.linspace(-40, 40, 4001)
    max_bc = 0.0
    opt_alpha = 0.0
    for al in alphas:
        m = stats.skewnorm.stats(al, moments="sk")
        g, k = float(m[0]), float(m[1])
        b = (g**2 + 1.0) / (k + 3.0)
        if b > max_bc:
            max_bc = b
            opt_alpha = al
    print(f"Max population BC over skew-normal: {max_bc:.4f} (at alpha = {opt_alpha:+.2f}) < 5/9 = 0.5556")
    print("=" * 80)


if __name__ == "__main__":
    run_simulation()
