# EXP8 / EXP6: Genuinely Unsupervised Model Order Selection Benchmark

## Overview
This experiment evaluates unsupervised cluster-number discovery when the true cluster count $K$ is completely unknown a priori.

## Experimental Structure
1. **Synthetic Phase Matrix (560 Configurations):**
   - True $K^* \in \{2, 3, 4, 5, 8, 10, 15\}$
   - Cluster balance: Equal vs. Dirichlet(0.5) unequal
   - Density: Isotropic ($\sigma = 1$) vs. Anisotropic heterogeneous
   - Distractor noise: $D_{\text{noise}} \in \{0, 100, 1000, 5000\}$
   - 5 independent seeds per configuration
2. **Real Biological Cohorts:**
   - Evaluated across high-dimensional oncology cohorts without supplying true $K$.
3. **Comparative Model Selectors:**
   - **ICC-AutoK (Proposed):** Linear-memory anchor PAC minimization
   - **HDBSCAN\*:** Density hierarchy excess of mass
   - **GMM with BIC:** Bayesian Information Criterion
   - **GMM with ICL:** Integrated Completed Likelihood
   - **Spectral Eigengap:** Maximum normalized Laplacian eigengap
   - **Silhouette Maximization:** Average silhouette width
