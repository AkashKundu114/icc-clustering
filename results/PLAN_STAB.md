# Subsample Stability and Null Control Protocol (PLAN_STAB)

**Document Status:** Pre-Registered Experimental Protocol  
**Date:** 2026-10-29  
**Target:** Item 1 of Revision Loop for *"Stable but Wrong: Why Consensus Clustering Can Fail in High Dimensions, and What Helps"*

---

## 1. Problem Formulation & Objective

In classical ensemble clustering literature and in preliminary drafts of Section 3.1, stability was evaluated by clustering the *same full dataset* repeatedly across varying random seeds and taking the mean pairwise Adjusted Rand Index (ARI). 

However, this metric possesses a fundamental flaw:
1. **Trivial Stability for Deterministic Solvers:** Deterministic algorithms (such as Agglomerative Ward clustering and Spectral clustering with fixed deterministic eigensolvers) achieve an ARI across seeds of $\text{Stab}_{\text{seed}} = 1.000$ purely as a mathematical artifact of zero internal randomness, regardless of whether the partition captures true cluster structure or noise.
2. **Artificial Penalization of Stochastic Solvers:** Randomized methods (such as GAC with random subspace sampling or CoHiRF with random tree projections) have $\text{Stab}_{\text{seed}} < 1.000$ by design.
3. **Invalid Gap Metric:** Consequently, a "stability-accuracy gap" based on seed variation conflates algorithmic determinism with structural stability under data perturbation.

**Objective:** Replace seed-based stability with **subsample perturbation stability** and an independent **permutation-null control**, testing whether algorithms converge consistently on spurious partitions when the underlying data points are perturbed.

---

## 2. Experimental Specifications

### 2.1 Benchmark Cohorts ($D/N > 20$)
The protocol evaluates the six high-dimensional real-world biomedical cohorts from the main benchmark suite:
1. **Colon:** $N = 62, D = 2{,}000, K = 2$ ($D/N = 32.26$)
2. **SRBCT:** $N = 83, D = 2{,}308, K = 4$ ($D/N = 27.81$)
3. **CNS:** $N = 60, D = 7{,}129, K = 2$ ($D/N = 118.82$)
4. **Leukemia:** $N = 72, D = 7{,}129, K = 2$ ($D/N = 99.01$)
5. **Prostate:** $N = 102, D = 12{,}600, K = 2$ ($D/N = 123.53$)
6. **Ovarian:** $N = 253, D = 15{,}154, K = 2$ ($D/N = 59.90$)

### 2.2 Evaluated Algorithms (12 Methods of Table 7)
All methods operate under the frozen benchmark configurations and ground-truth cluster count $K$:
1. **K-Means:** Lloyd algorithm with $k$-means++ seeding ($n_{\text{init}} = 1$).
2. **Ward:** Agglomerative hierarchical clustering with Ward minimum variance criterion.
3. **Spectral:** Normalized spectral clustering (Ng-Jordan-Weiss formulation).
4. **FCM:** Fuzzy C-Means ($m = 2.0$, max iter 100).
5. **Standard Consensus:** Dense $N \times N$ co-association consensus ($M = 25$ base clusterers).
6. **Core-Halo Consensus:** Stability-pruned core consensus (Li et al., 2019, $M = 25$).
7. **FCAG:** Fast Clustering with Anchor Guidance (Nie et al., 2024, $L = 40$).
8. **FastMVC:** Fast Multi-View Bipartite Graph Consensus ($L = 40$).
9. **CoHiRF:** Hierarchical Random Forest Consensus (Belucci et al., 2025, $d_{\text{rf}} = 20$).
10. **Ungated AC:** Bipartite anchor graph consensus without feature gating ($M = 25, L = 40$).
11. **DEC:** Deep Embedded Clustering (Xie et al., 2016, autoencoder + Student-t refinement).
12. **GAC Pipeline (Ours):** Bimodality-Gated Subspace Selection + Bipartite Anchor Consensus ($M = 25, L = 40, \alpha = 0.15$).

---

## 3. Subsample Stability & Null Control Protocol

### 3.1 Data Subsampling Protocol
- For each dataset, draw $B = 30$ independent random subsamples of size $\lfloor 0.80 \times N \rfloor$ without replacement.
- Sampling is **class-stratified** across the true label distribution.
- Subsample random seeds: fixed sequentially to $\{5000, 5001, \dots, 5029\}$ across all methods.
- For each subsample $b \in \{0, \dots, 29\}$, cluster the subsample once with the algorithm's internal random seed fixed to $0$.

### 3.2 Subsample Stability Metric
- For every pair of subsamples $(i, j)$ with $0 \le i < j < 30$ (total $\binom{30}{2} = 435$ pairs), identify the overlapping instance subset $I_{ij} = S_i \cap S_j$.
- Compute the Adjusted Rand Index between the two predicted clusterings restricted to the intersection:
  $$\text{ARI}_{ij} = \text{ARI}\left(\hat{y}_i[I_{ij}], \hat{y}_j[I_{ij}]\right)$$
- **Subsample Stability:**
  $$\text{Stab}_{\text{sub}} = \frac{1}{435} \sum_{i < j} \text{ARI}_{ij}$$

### 3.3 Subsample Accuracy Metric
- For each subsample $b \in \{0, \dots, 29\}$, compute the accuracy against ground-truth clinical labels:
  $$\text{Acc}_b = \text{ARI}\left(\hat{y}_b, y_{\text{true}}[S_b]\right)$$
- **Empirical Accuracy:**
  $$\overline{\text{Acc}} = \frac{1}{30} \sum_{b=0}^{29} \text{Acc}_b$$

### 3.4 Subsample Stability-Accuracy Gap
$$\Delta_{\text{sub}} = \text{Stab}_{\text{sub}} - \overline{\text{Acc}}$$

### 3.5 Permutation Null Control
- For each subsample draw $b \in \{0, \dots, 29\}$, generate an independent permutation-null copy of the dataset:
  - Every feature column $d \in \{1, \dots, D\}$ is independently permuted across the $N$ sample rows using seed $6000 + b$.
  - This completely destroys class-conditional cluster structure and inter-feature correlations while preserving exact 1D empirical marginal distributions.
- Apply the identical 80% subsampling protocol (subsample seed $5000 + b$) and cluster with method seed 0.
- Compute the 435 pairwise intersection ARIs:
  $$\text{Stab}_{\text{null}} = \frac{1}{435} \sum_{i < j} \text{ARI}_{\text{null}, ij}$$
- (Null accuracy is not defined because class labels are disconnected from the permuted data).

---

## 4. Pre-Specified Decision Rules

To maintain absolute scientific integrity and prevent post-hoc rationalization, all decision boundaries are locked prior to running:

1. **Rule (i) — "Stable but Wrong" Pathology:**  
   A method-dataset pair is defined as displaying the "Stable but Wrong" pathology if and only if:
   $$\text{Stab}_{\text{sub}} \ge 0.50 \quad \text{AND} \quad \overline{\text{Acc}} \le 0.05$$

2. **Rule (ii) — "Stability is Uninformative":**  
   Stability is classified as uninformative / non-signal-reflecting if:
   $$\left(\text{Stab}_{\text{sub}} - \text{Stab}_{\text{null}}\right) < 0.10 \quad \text{AND} \quad \overline{\text{Acc}} \le 0.05$$
   (i.e., the algorithm's partition agreement on real data is virtually indistinguishable from its agreement on pure noise).

3. **Rule (iii) — Paper-Level Claim Verification:**  
   The macro claim *"Consensus clustering frequently exhibits a severe stability-accuracy trap on real-world high-dimensional cohorts"* is statistically supported if and only if:
   - At least $3$ of the $12$ methods satisfy Rule (i) on at least $3$ of the $6$ cohorts; **AND**
   - A paired bootstrap 95% confidence interval for the stability-minus-accuracy gap $\Delta_{\text{sub}}$ (resampling cohorts with replacement, $B = 10{,}000$) strictly excludes $0$ ($\text{CI}_{\text{lower}} > 0$).

### 4.1 Narrative Contingency Protocol (If Rules Fail)
- If Rule (iii) fails (e.g. if subsampling destabilizes the classical baselines such that real subsample stability is low on real cohorts):
  1. We will **not** force or massage the real-data claim.
  2. The paper's primary evidence for "Stable but Wrong" will be explicitly situated in the **rigorously controlled high-dimensional simulations** (Theorem 1, Proposition 1, and Experiment 0 distance concentration regimes where isotropic noise is proven to create spurious consensus attractors).
  3. The title and abstract will be updated to reflect empirical reality: shifting from a universal claim to an empirical investigation of *when* the gap appears versus when subsampling induces instability.
  4. All discrepancies between prior seed stability and new subsample stability will be documented transparently in `NARRATIVE_CHANGES.md`.

---

## 5. Execution Architecture & Guards

- **Execution Script:** `scripts/stability_subsample.py`
- **Output Storage:** `results/stability/runs/*.parquet` (or `.csv` records), with individual partition labels saved in `results/stability/partitions/`.
- **Resumability:** The script checks disk for existing completed records `(method, dataset, subsample_id, mode)` and resumes without repeating completed fits.
- **Resource Constraints:**
  - Memory cap: 13 GB per process.
  - Timeout cap: 30 minutes per fit.
  - Failed or timed-out fits are recorded as `status="failed"`, runtime logged, and accuracy set to $0.0$.
- **Historical Traceability:** The existing seed-stability metrics are retained as a secondary reference column in the comprehensive report, explicitly annotated: `"Seed stability (transductive; reflects algorithmic determinism)"`.
