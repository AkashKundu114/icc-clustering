"""Verification of Sarle's Bimodality Coefficient (BC) across analytical distributions.
Formula: BC = (skewness^2 + 1) / pearson_kurtosis
"""
import numpy as np
from scipy import stats

dists = {
    "Exponential(1)": stats.expon(),
    "Uniform(0, 1)": stats.uniform(),
    "Lognormal(s=1)": stats.lognorm(s=1),
    "Beta(3, 1)": stats.beta(3, 1),
}

print(f"{'Distribution':<18} | {'Skewness':<10} | {'Kurtosis(Pearson)':<18} | {'Analytical BC':<14} | {'Sample BC (N=1M)':<16}")
print("-" * 85)

np.random.seed(42)
for name, d in dists.items():
    # Analytical
    gamma = d.stats(moments="s")
    kappa = d.stats(moments="k") + 3.0  # scipy stats returns excess kurtosis
    bc_analytic = (gamma**2 + 1.0) / kappa
    
    # Numerical sample
    x = d.rvs(size=1_000_000)
    g_samp = stats.skew(x)
    k_samp = stats.kurtosis(x, fisher=False)  # Pearson kurtosis
    bc_sample = (g_samp**2 + 1.0) / k_samp
    
    print(f"{name:<18} | {float(gamma):<10.4f} | {float(kappa):<18.4f} | {float(bc_analytic):<14.4f} | {float(bc_sample):<16.4f}")
