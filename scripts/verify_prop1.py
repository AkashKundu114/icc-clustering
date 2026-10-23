"""
Numerical Verification of Proposition 1: Bimodality Coefficient Separation Bound.

Analytically and numerically solves for the minimum separation Delta / sigma0 required
for Sarle's Bimodality Coefficient to exceed the uniform threshold b >= 5/9.
Evaluates both standard Gaussian and Student-t heavy-tailed distributions (nu in [5, 100]).

Usage:
    python scripts/verify_prop1.py
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import gamma


def kurtosis_bimodal_gaussian(delta, sigma0=1.0):
    theta = (delta / sigma0) ** 2
    beta2 = (3.0 + 6.0 * theta + theta ** 2) / ((1.0 + theta) ** 2)
    b = 1.0 / beta2
    return beta2, b

def target_equation(delta, sigma0=1.0):
    _, b = kurtosis_bimodal_gaussian(delta, sigma0)
    return b - (5.0 / 9.0)

exact_root = np.sqrt((3.0 + np.sqrt(15.0)) / 2.0)
num_root = brentq(target_equation, 1.0, 2.5)

print(f"Proposition 1 Exact Separation Bound (Gaussian): {exact_root:.6f}")
print(f"Proposition 1 Numerical Root:                  {num_root:.6f}")
assert abs(exact_root - num_root) < 1e-5
assert abs(exact_root - 1.853778) < 1e-4

def student_t_pdf(t, nu):
    c = gamma((nu + 1.0) / 2.0) / (np.sqrt(np.pi * nu) * gamma(nu / 2.0))
    return c * (1.0 + (t ** 2) / nu) ** (-(nu + 1.0) / 2.0)

nu_vals = [5.0, 6.0, 8.0, 10.0, 20.0, 50.0, 100.0]
t_roots = []
for nu in nu_vals:
    sigma0 = np.sqrt(nu / (nu - 2.0))
    def eq(delta):
        def m2_i(t): return (t ** 2) * 0.5 * (student_t_pdf(t - delta, nu) + student_t_pdf(t + delta, nu))
        def m4_i(t): return (t ** 4) * 0.5 * (student_t_pdf(t - delta, nu) + student_t_pdf(t + delta, nu))
        m2, _ = quad(m2_i, -60, 60)
        m4, _ = quad(m4_i, -60, 60)
        return (m2 ** 2) / m4 - (5.0 / 9.0)
    delta_root = brentq(eq, 1.0, 5.0)
    ratio = delta_root / sigma0
    t_roots.append((nu, delta_root, ratio))
    print(f"nu = {nu:5.1f} | delta = {delta_root:.4f} | sigma0 = {sigma0:.4f} | Delta/sigma0 = {ratio:.4f}")

asymptotic_ratio = t_roots[-1][2]
assert abs(asymptotic_ratio - exact_root) < 0.01
print("VERIFICATION_SUCCESSFUL: Proposition 1 separation bound Delta/sigma0 >= 1.854 confirmed.")
