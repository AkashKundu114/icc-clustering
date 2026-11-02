# 06 Forensic Audit of Knockoff and Target-Decoy Feature Gating

**Audit Target:** ICC-Clustering (`D:\icc-clustering`)  
**Auditor:** Senior Statistical Methodologist & High-Dimensional Inference Specialist  
**Audit Timestamp:** 2026-11-01T23:14:00+05:30  
**Primary Evidence Recovered:**
- `results/evidence_recovery/recovered/knockoff_audit_results.json` (8.1 KB)
- `src/cicc/decoy.py` (`DecoyFeatureGating`, Lines 80–135)
- `src/cicc/inductive.py` (`InductiveConsensusClusterer`, Lines 147–179)
- `docs/theory.md` (Section 9.2)

---

## 1. Executive Summary

This forensic audit evaluated the theoretical assumptions, algorithmic implementation, and empirical error control of the knockoff and target-decoy feature selection engine in `src/cicc/decoy.py`.

### Key Audit Findings:
1. **Exchangeability Axiom Violation (P1 - THEORETICAL):**
   `src/cicc/decoy.py:86` samples Gaussian decoys independently from $\mathcal{N}(\mu, \Sigma)$. Under this construction, cross-covariance between real and decoy features is zero ($\text{Cov}(X_j, \tilde{X}_k) = 0$). Swapping a real feature with its decoy abruptly destroys the covariance structure, violating the foundational exchangeability requirement of Model-X Knockoffs (Barber & Candès 2015) with an empirical covariance distortion of **0.672**.
2. **Post-Clustering Double-Dipping Selection Bias (P1 - STATISTICAL):**
   Labels are derived from $X$ via spectral clustering *prior* to feature selection. Real feature saliencies are evaluated on data already partitioned to maximize cluster contrast, while decoys are independent. Under the global null, this shifts the distribution of feature statistics from symmetric coin flips to **$\Pr(W_j > 0) = 60.9\%$**.
3. **Catastrophic Fallback Bug Driving 100% Empirical FDR (P1 - SOFTWARE):**
   When the target FDR cannot be met, line 122 executes `best_tau = float(positive_W[-1])`. Instead of returning the empty set ($\emptyset$) as required by Knockoff theory, this forces the selection of false positive noise variables, driving empirical FDR to **100.0% under pure null and correlated noise regimes**.
4. **Dead Code in Inductive Consensus Pipeline (P1 - ARCHITECTURAL):**
   In `src/cicc/inductive.py:147-179`, decoy feature gating is executed and stored in `self.selected_features_`, but **all subsequent steps (calibration labels, centroids, conformal calibrator, and out-of-sample projections) use the full $D$-dimensional feature space**. The selected feature subset has zero downstream impact.

---

## 2. Theory of Model-X Knockoffs vs. `cicc.decoy`

```mermaid
flowchart TD
    subgraph "Model-X Knockoff Theory (Candès et al. 2018)"
        XReal["Real Feature Matrix X"] --> CondKnock["Conditional Knockoff Generator:\nX_tilde | X ~ N(X - X Sigma^{-1} diag(s), 2 diag(s) - ...)\nPairwise Exchangeability Strictly Preserved"]
        CondKnock --> SymStat["Antisymmetric Statistics W_j\nNull Coin-Flip: Pr(W_j > 0) <= 0.50"]
        SymStat --> SafeTau["Knockoff+ Threshold tau\nIf unachievable: Return Empty Set"]
    end

    subgraph "src/cicc/decoy.py Implementation"
        XCode["Real Feature Matrix X"] --> IndepMVN["rng.multivariate_normal(mu, cov)\nINDEPENDENT DRAW: Cov(X, X_decoy) == 0\nExchangeability VIOLATED (Distortion = 0.672)"]
        IndepMVN --> DoubleDip["Post-Clustering Double-Dipping:\nLabels derived from X BEFORE selection\nNull Bias: Pr(W_j > 0) == 60.9%!"]
        DoubleDip --> FallbackBug["Fallback Bug (Line 122):\nbest_tau = positive_W[-1]\nFORCES selection of false discoveries!"]
        FallbackBug --> CrashFDR["EMPIRICAL FDR = 100.0% (Under Null)"]
    end
```

### 2.1 Theoretical Foundations

Under the Model-X Knockoff framework (Candès et al. 2018), synthetic knockoff features $\tilde{X}$ must satisfy:
1. **Pairwise Exchangeability:**
   $$[X, \tilde{X}]_{\text{swap}(S)} \stackrel{d}{=} [X, \tilde{X}] \quad \forall S \subset \{1, \dots, D\}$$
   For Gaussian distributions $\mathcal{N}(\mu, \Sigma)$, this requires:
   $$\text{Cov}([X, \tilde{X}]) = \begin{bmatrix} \Sigma & \Sigma - \text{diag}(s) \\ \Sigma - \text{diag}(s) & \Sigma \end{bmatrix}, \quad \text{diag}(s) \succeq 0, \quad 2\Sigma - \text{diag}(s) \succeq 0$$
2. **Antisymmetry of Feature Statistics:**
   The feature statistic $W_j = f_j([X, \tilde{X}])$ must flip sign when $X_j$ and $\tilde{X}_j$ are swapped:
   $$W_j([X, \tilde{X}]_{\text{swap}(j)}) = -W_j([X, \tilde{X}])$$
   Under the null hypothesis, $W_j$ must satisfy the coin-flip property:
   $$\Pr(W_j > 0 \mid |W_j|) = \Pr(W_j < 0 \mid |W_j|) \le 0.50$$

---

## 3. Analysis of Implementation Defects in `src/cicc/decoy.py`

### 3.1 Defect K-01: Zero Cross-Covariance
Lines 84–89 of `src/cicc/decoy.py`:
```python
84: elif self.method == "gaussian_knockoff":
85:     mu = np.mean(X, axis=0)
86:     cov = np.cov(X, rowvar=False) + 1e-6 * np.eye(D)
87:     X_decoy = rng.multivariate_normal(mu, cov, size=N)
```
- $X_{\text{decoy}}$ is sampled **independently** from $\mathcal{N}(\mu, \Sigma)$.
- Consequently, $\text{Cov}(X_j, X_{\text{decoy}, k}) = 0$. But $\text{Cov}(X_j, X_k) = \Sigma_{jk}$.
- When column $j$ is swapped, the covariance structure between features drops from $\Sigma_{jk}$ to 0.
- In our empirical measurements on correlated Gaussian features ($\rho = 0.50$), the mean real off-diagonal correlation was $+0.376$, whereas the decoy cross-correlation was $+0.014$, yielding an exchangeability violation of **0.672**.

### 3.2 Defect K-02: Post-Clustering Selection Bias (Double-Dipping)
- In `InductiveConsensusClusterer.fit()` (`src/cicc/inductive.py#L148`), labels are learned from $X_{\text{disc}}$ via spectral clustering.
- Then, $X_{\text{disc}}$ and `disc_labels` are passed into `self.decoy_gating_.fit(X_disc, disc_labels)`.
- Real feature saliencies $S_{\text{real}}[j]$ are computed on the very partition optimized on $X$.
- Decoy features $X_{\text{decoy}}$ are generated independently after clustering and have zero association with `disc_labels`.
- **Measured Empirical Bias:** Under pure Gaussian noise with no true clusters:
  - Fixed independent labels: $\Pr(W_j > 0) = 49.7\% \approx 50.0\%$.
  - Clustered labels on noise: $\Pr(W_j > 0) = \mathbf{60.9\%}$.
  - The null symmetry condition is violated.

### 3.3 Defect K-03: The Fallback Bug
Lines 122–128 of `src/cicc/decoy.py`:
```python
122: if best_tau is None:
123:     # If target FDR cannot be met, fall back to the most conservative threshold
124:     best_tau = float(positive_W[-1])
125:     n_neg = np.sum(self.W_ <= -best_tau)
126:     n_pos = np.sum(self.W_ >= best_tau)
127:     best_fdr = float((1.0 + float(n_neg)) / max(1.0, float(n_pos)))
```
- In Knockoff+ theory, if no threshold $\tau > 0$ satisfies $\frac{1 + \#\{W \le -\tau\}}{\#\{W \ge \tau\} \vee 1} \le q$, the algorithm **must return the empty set $\emptyset$**.
- Setting `best_tau = float(positive_W[-1])` selects the single largest positive statistic and declares it a discovery.
- Under pure null data, this guarantees at least one false positive on 100% of runs.

---

## 4. Empirical Simulation Results from Recovered Evidence

From recovered microdata `results/evidence_recovery/recovered/knockoff_audit_results.json` (50 Monte Carlo trials per regime, $N=100, D=200$, nominal target $q = 0.10$):

### Table 1: Empirical FDR and Discovery Power Across Noise Regimes

| Noise Regime | Method | Nominal $q$ | Empirical FDR (Mean $\pm$ SD) | FDR Controlled? | Mean Discoveries | Fallback Rate | Status |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Independent Gaussian Null** | Permutation | 0.10 | **1.000 $\pm$ 0.000** | **NO** | 3.24 | 88.0% | **FAILED** |
| **Independent Gaussian Null** | Gaussian Knockoff | 0.10 | **1.000 $\pm$ 0.000** | **NO** | 1.00 | 100.0% | **FAILED** |
| **Correlated Gaussian Null ($\rho=0.6$)** | Permutation | 0.10 | **1.000 $\pm$ 0.000** | **NO** | 200.00 | 0.0% | **FAILED** |
| **Correlated Gaussian Null ($\rho=0.6$)** | Gaussian Knockoff | 0.10 | **1.000 $\pm$ 0.000** | **NO** | 200.00 | 0.0% | **FAILED** |
| **Heavy-Tailed Null (Student-$t$, df=3)**| Permutation | 0.10 | **1.000 $\pm$ 0.000** | **NO** | 1.88 | 94.0% | **FAILED** |
| **Heavy-Tailed Null (Student-$t$, df=3)**| Gaussian Knockoff | 0.10 | **1.000 $\pm$ 0.000** | **NO** | 3.10 | 86.0% | **FAILED** |
| **Block-Correlated Null (blocks of 20)**| Permutation | 0.10 | **1.000 $\pm$ 0.000** | **NO** | 164.28 | 0.0% | **FAILED** |
| **Block-Correlated Null (blocks of 20)**| Gaussian Knockoff | 0.10 | **1.000 $\pm$ 0.000** | **NO** | 157.34 | 0.0% | **FAILED** |
| **Mixed Signal + Null ($D_{\text{sig}}=20$)**| Permutation | 0.10 | 0.088 $\pm$ 0.084 | YES | 21.96 | 0.0% | Valid on Mixed |
| **Mixed Signal + Null ($D_{\text{sig}}=20$)**| Gaussian Knockoff | 0.10 | 0.096 $\pm$ 0.094 | YES | 22.20 | 0.0% | Valid on Mixed |
| **All-Null 100-Trial Test** | Permutation | 0.10 | **1.000 $\pm$ 0.000** | **NO** | 1.85 | 100.0% | **FAILED** |

### 4.1 Key Findings:
1. Under every pure-null regime, **empirical FDR is exactly 100.0%**.
2. Under correlated Gaussian and block-correlated noise, the algorithm selects **100% of all features** ($200 / 200$) because the cluster partition aligns with latent correlation factors, which independent/permuted decoys do not possess.

---

## 5. Architectural Defect: Dead Code in `src/cicc/inductive.py`

In `InductiveConsensusClusterer.fit()` (`src/cicc/inductive.py#L147-L179`):
```python
147: if self.enable_gating:
148:     self.decoy_gating_.fit(X_disc, disc_labels)
149:     self.selected_features_ = self.decoy_gating_.selected_indices_
150: else:
151:     self.selected_features_ = np.arange(D)
152: 
153: # Step 5: Compute Centroids (USES ALL D DIMENSIONS!)
154: centroids = np.zeros((self.k, D), dtype=np.float64)
155: for c in range(self.k):
156:     mask = (disc_labels == c)
157:     if np.any(mask):
158:         # Row-normalized unit vectors
159:         norms = np.linalg.norm(X_disc[mask], axis=1, keepdims=True)
160:         ...
163: cos_cal = X_cal @ centroids.T
```
- `self.selected_features_` is computed at line 149 and **never referenced again**.
- Centroids are computed across all $D$ dimensions.
- Calibrator is fitted on all $D$ dimensions.
- Out-of-sample projection (`predict`, line 191) projects across all $D$ dimensions.
- **The entire decoy feature selection subsystem is dead code.**

---

## 6. Remediation Plan

1. **Remove False Positive Fallback:** Replace line 122 with:
   ```python
   if best_tau is None:
       self.tau_ = float("inf")
       self.selected_indices_ = np.array([], dtype=int)
       self.estimated_fdr_ = 0.0
       return self
   ```
2. **Implement Second-Order Model-X Knockoffs:** Sample knockoffs from the conditional distribution $\tilde{X} \mid X$ satisfying $2\Sigma - \text{diag}(s) \succeq 0$.
3. **Connect Gated Features to Downstream Pipeline:** Slice $X_{\text{disc}}[:, \text{self.selected\_features\_}]$ before computing centroids, calibrator, and projections.
