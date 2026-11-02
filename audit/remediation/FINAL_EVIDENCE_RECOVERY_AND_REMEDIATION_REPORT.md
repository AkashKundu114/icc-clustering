# Forensic Evidence Recovery, Repository Audit, and Remediation Report

**Target Repository**: `AkashKundu114/icc-clustering`  
**Local Working Copy**: `D:\icc-clustering`  
**Remote Upstream**: `https://github.com/AkashKundu114/icc-clustering`  
**Current HEAD**: `7ddbe8301b8d27c94f388c40acbc88b0dee82723` (`origin/main`)  
**Target Venue**: *Data Mining and Knowledge Discovery* (DMKD)  
**Audit Date**: November 2026  
**Final Scientific Verdict**: **NO-GO FOR SUBMISSION** (Blocking P0/P1 Defects Identified)  

---

## 1. Executive Summary & Final Verdict

An independent forensic evidence-recovery and scientific integrity audit of the `icc-clustering` repository was conducted to verify its readiness for peer-reviewed submission to *Data Mining and Knowledge Discovery* (DMKD). The investigation encompassed repository Git history, unreleased artifact recovery, algorithmic correctness, statistical validity, reproducibility across random seeds, packaging integrity, continuous integration (CI), and end-to-end traceability between code and manuscript claims.

### The Verdict: NO-GO
The repository and manuscript are assigned a formal verdict of **NO-GO**. Submitting the work in its current state carries catastrophic risks of desk rejection, peer-review contradiction, and public retraction due to critical P0/P1 defects across multiple subsystems:

1. **[P0] Active Exposure of Historical Confidential Vaults**: Commit `e3f54cc0951d173f0e13a4b524628328f318e746` remains an active, reachable ancestor of `origin/main` on GitHub (12 commits behind HEAD). Twenty-two public pull request references (`refs/pull/1/head` to `refs/pull/22/head`) expose unreleased confirmatory modules (`src/icc/confirmatory/`), execution manifests, and author logs. A previous local `git rm` failed to sanitize Git history.
2. **[P0] Clinical Diagnostic Invalidation & Toxic Misclassifications**: Conformal Inductive Consensus Clustering (`cicc`) guarantees marginal coverage *only* with respect to its own internal pseudo-labels. When evaluated against ground-truth clinical pathology, empirical coverage collapses from $90\%$ to **$62.2\%$ on Leukemia** and **$37.0\%$ on SRBCT**, with **$20\%$ toxic single-label misclassifications** (e.g., Acute Lymphoblastic Leukemia classified as AML with probability $P > 0.99$).
3. **[P1] 100% Collapse of AutoK Model Order Selection**: In `src/icc/consensus/autok.py`, applying the Senbabaoglu Proportion of Ambiguous Clustering (PAC) metric to an $L_1$ row-normalized bipartite matrix forces inner products to concentrate below $0.10$. The ambiguity interval $(0.1, 0.9)$ is identically empty ($\text{PAC} \equiv 0.0000$), causing AutoK to collapse to $K_{min}=2$ across **510 out of 510 trials (100% failure rate)**.
4. **[P1] Methodological Breakdown of Knockoff Feature Gating**: In `src/cicc/decoy.py`, synthetic decoys are drawn as independent standard Gaussian noise, completely violating Model-X pairwise exchangeability ($\text{Cov}(X_j, \tilde{X}_j) = 0$). Furthermore, a fallback bug at line 122 selects arbitrary noise under null data, yielding **100% empirical FDR**, while selected features are completely ignored as dead code in `inductive.py`.
5. **[P1] Frozen Seed Leakage in Synthetic Benchmarks**: In `src/icc/core.py:build_dataset()`, cluster generation hardcodes `seed=42` inside `make_signal()`. Across all user seeds, cluster centroids and true labels are **100% identical and frozen**; only isotropic noise fluctuates.
6. **[P1] Falsified Baseline Speedup & Accuracy Claims**: Historical claims that Standard Consensus requires $0.3662\,\text{s}$ while ICC-v2 takes $0.0039\,\text{s}$ with perfect accuracy are falsified. Independent re-benchmarking reveals Standard Consensus runs in **$0.1210\,\text{s}$** (~3x faster than reported) with perfect $\text{ARI}=1.0$ across 10 seeds, while ICC-v2 collapses to $\text{ARI}=0.4396$ on Seed 101.
7. **[P1] Statistically Null Anchor Certification Lift**: Factorial ablation on real high-dimensional benchmarks shows Full ICC-v2 (Certified Anchors, $\text{ARI}=0.217$) vs Random Anchors ($\text{ARI}=0.198$) yields $\Delta = +0.019$ ($95\%\text{ CI } [-0.039, +0.082]$, Wilcoxon $p = 0.844$). The core anchor selection mechanism provides no statistically significant accuracy benefit.
8. **[P1] Fatal Console Script Packaging Breakdown**: Built wheels omit the `scripts/` directory and `src/icc/__main__.py` contains relative import errors. Executing `icc`, `icc-demo`, or `icc-run` from a wheel install crashes immediately with `ModuleNotFoundError`.

Crucially, **sound core components were also validated**: Bimodality-Gated Subspace Selection (BGSS) reliably recovers signal under high-dimensional distractor noise; the Linear Determinacy Identity is algebraically exact to machine precision ($2.78 \times 10^{-17}$); bipartite consensus scales with linear auxiliary memory $\mathcal{O}(NL)$; and committed CI passes on Python 3.10 through 3.14.

---

## 2. Repository Baseline State & Git History Forensics

### 2.1 Repository References & HEAD Resolution
Inspection of local and remote references resolves the previously reported commit SHA discrepancies:
- **Local HEAD**: `7ddbe8301b8d27c94f388c40acbc88b0dee82723` (`main`)
- **Remote HEAD (`origin/main`)**: `7ddbe8301b8d27c94f388c40acbc88b0dee82723`
- **Relationship**: Local `main` and `origin/main` are identical, synchronized, and clean (0 uncommitted changes, 0 untracked files).
- **Previous HEAD (`83728a441f44c1ed56a35a5bdb07490ff559de81`)**: Direct parent of `7ddbe8301b8d27c94f388c40acbc88b0dee82723`. Commit `7ddbe83` added Python 3.13 and 3.14 to `.github/workflows/ci.yml` at `Sun Nov 1 22:19:09 2026 +0530`.

### 2.2 Ancestry of Historical Commit `e3f54cc`
Independent graph traversal confirms that historical commit:
`e3f54cc0951d173f0e13a4b524628328f318e746`
is an **active direct ancestor of `origin/main`**:
```powershell
git merge-base --is-ancestor e3f54cc0951d173f0e13a4b524628328f318e746 main
# Exit Code: 0 (True)
git rev-list --count e3f54cc0951d173f0e13a4b524628328f318e746..main
# Output: 12 commits
```
The reported "candidate history rewrite" was never applied to the remote GitHub repository.

---

## 3. Confidentiality & Historical Exposure Audit

A forensic scan of the Git object database and public remote references identified **36 historical exposure records** spanning confidential research assets:

### 3.1 Exposure Classification
1. **Historical Confirmatory Pipeline (`src/icc/confirmatory/`)**: Completely retrievable from commit `e3f54cc` and intermediate commits. Contains internal confirmatory test suites, raw patient-level metadata, and private exploratory scripts.
2. **Execution Manifests (`EXECUTION_MANIFEST.csv`, `update_revision_log.py`)**: Accessible across historical commit trees, detailing internal research chronologies and machine hostnames.
3. **Remote Pull Request Head Exposure**: Twenty-two open/closed PR heads on GitHub (`refs/pull/1/head` through `refs/pull/22/head`) point directly to un-sanitized commit trees containing confidential files. Anyone cloning via `git clone` or fetching `refs/pull/*/head` can recover all deleted assets.

**Remediation Verdict**: The previous deletion (commit `0565abc`) was a simple tree deletion (`git rm`), leaving historical objects fully accessible in Git history. A complete history rewrite via `git-filter-repo` and PR ref purge is required.

---

## 4. Artifact Inventory & Missing Evidence Reconciliation

To establish an immutable empirical baseline, all recoverable raw benchmark artifacts were retrieved and cataloged into `results/evidence_recovery/recovered/`:

| Artifact Filename | Size (Bytes) | SHA-256 Digest | Status | Category |
| :--- | :---: | :--- | :---: | :--- |
| `stats.json` | 11,858 | `cb3eb402c524b0b1ce486667db793cf830ccefd140d046c820126ff32fb0327f` | RECOVERED | Master Statistics |
| `results.json` | 1,627,258 | `f1dbb12fb846ee454eb8aa0f55cf73a5a711413a96ae083bb723528b17b6059c` | RECOVERED | Microdata Partition Grid |
| `exp2_real_high_d_factorial.csv` | 43,385 | `20d20d778fb8f71aa7f8184f932e65860d5b2c75a401b3a2ea1297db2cff4fbb` | RECOVERED | Factorial Ablation |
| `adversarial_autok_raw_results.csv` | 104,264 | `3ecbfcb14f828a2a57891ea51c11e61bb16fe684bebf1be2eb31aa67e8efd600` | RECOVERED | 510-Trial AutoK Microdata |
| `adversarial_autok_summary.json` | 9,763 | `64455ae7738f6ee2227d8d2cc6770f80875e533036814b74bb8a1a3e9c52f200` | RECOVERED | AutoK Summary Metrics |
| `conformal_audit_results.json` | 3,796 | `2bf248d6896205cf90df94294c73e0a17dc6be8eec3b9d6288849646b3f1c841` | RECOVERED | Conformal Patient Pathology |
| `knockoff_audit_results.json` | 8,125 | `76d917f9e5c545305141aa50ae338a0c242207b5a83981fc1824efbcdd305419` | RECOVERED | Knockoff FDR Diagnostics |
| `subsample_stability_summary.csv` | 10,622 | `83ef9a8264e1c25ca4e50882ef9ff88d8b94873d91cf3ecb700f73f3ca0623d9` | RECOVERED | Subsample Stability Grid |
| `real_data_stability_summary.csv` | 16,630 | `fef6ba79e0004ff4dddafcfe49cf9d846a84c2eb49eb9a4a75412586b6a03e62` | RECOVERED | Real Data Stability Grid |
| `reproduction_benchmarks.csv` | 14,849 | `1cb54130005ca7091461f5f2fe4e883f3f09520cbfe038e2ea55ef9c0490b4bf` | RECOVERED | Timing & Speedup Data |
| `clean_env_results.json` | 4,185 | `2eb7e271bf386a605809ce99616d6ba5ea176a928baeb4eb17835d1f8cbff265` | RECOVERED | Clean Virtual Env Run |
| `leakage_audit_results.json` | 2,684 | `7f75f91f7574345266cbaf9b4fd5442dfc2826e7aa7c1664e4b4430cfc67340b` | RECOVERED | Data Leakage Diagnostics |
| `numbers.tex` | 4,087 | `f6ff84cbde45763266a87c126d4ca9d5d3690d74ee5723ee6f199343ca1575fb` | RECOVERED | LaTeX Number Macros |

**Permanently Missing Artifacts**: 5 non-critical exploratory artifacts could not be located in local or remote archives (`million_cell_scrnaseq_scaling_raw.csv`, `driver_gene_overlap_validation.json`, `model_x_knockoff_exact_matrices.npz`, `holdout_801010_patient_splits.parquet`, `singler_celltype_reference_annotations.h5ad`). These do not block the core manuscript.

---

## 5. Reconciled Arithmetic Discrepancy (Stability–Accuracy Discordance)

Previous audits flagged a potential numerical contradiction in the manuscript's core empirical thesis:
- Text reported stability-accuracy gaps of both $+0.485$ and $+0.687$.
- Discrepancy raised concerns of fabricated data.

### Forensic Reconciliation
Analysis of `stats.json` and `subsample_stability_summary.csv` completely resolves this discrepancy:
1. **The $+0.485$ Metric**: Represents the **global omnibus gap** across all non-degenerate configurations ($N=208$ evaluations), calculated as mean subsample stability minus mean external clustering accuracy ($0.582 - 0.097 = +0.485$, $95\%\text{ CI } [+0.379, +0.662]$).
2. **The $+0.687$ Metric**: Represents the **extreme noise subset mean gap** across the 9 high-dimensional cells ($D \ge 1000$) where signal is completely obscured by distractor features (mean stability $= 0.684$, mean $\text{ARI} = -0.003 \implies 0.684 - (-0.003) = 0.687$).

Both numbers are algebraically exact reflections of the recovered microdata. The manuscript simply conflated the subset metric with the global metric in two different paragraphs.

---

## 6. Factorial Ablation & The Null Anchor Certification Lift

A central conceptual claim of ICC-v2 is that certifying anchors using the Linear Determinacy Identity ($\sigma_i$) recovers superior consensus geometry over selecting anchors uniformly at random.

### Empirical Knockout Findings
Forensic extraction of `exp2_real_high_d_factorial.csv` across the 6 high-dimensional biomedical cohorts refutes this claim:

| Configuration ID | Variant Description | Mean ARI | Median ARI | Std Dev | Wilcoxon vs Full ($p$-value) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **V1** | Ambient Standard Consensus | 0.037 | 0.012 | 0.048 | $p = 0.031$ |
| **V2** | Ambient Random Anchors | 0.046 | 0.018 | 0.052 | $p = 0.031$ |
| **V3** | BGSS + Standard Consensus | 0.077 | 0.034 | 0.089 | $p = 0.031$ |
| **V4** | **BGSS + Random Anchors** | **0.198** | **0.058** | **0.251** | **$p = 0.844$ (Null)** |
| **V5** | **Full ICC-v2 (BGSS + Certified Core Anchors)** | **0.217** | **0.061** | **0.264** | **Reference** |

### Statistical Synthesis
The difference between Certified Core Anchors (V5) and Uniform Random Anchors (V4) is:
$$\Delta = +0.019 \quad (95\%\text{ CI } [-0.039, +0.082], \quad \text{Wilcoxon signed-rank } p = 0.844)$$

The null hypothesis cannot be rejected. Core anchor certification contributes **zero statistically significant accuracy improvement**. Signal recovery is driven overwhelmingly by BGSS feature gating ($0.037 \to 0.198$), while the anchor graph cut provides memory reduction ($\mathcal{O}(NL)$ vs $\mathcal{O}(N^2)$).

---

## 7. Theoretical & Numerical Correctness: Determinacy & Bipartite Cut

1. **Exact Linear-Memory Determinacy Identity (Proposition 2)**:
   $$\sigma_i = \frac{1}{M^2} \sum_{m=1}^M \sum_{m'=1}^M \mathbf{1}\{P_m(i) = P_{m'}(i)\} = \frac{1}{M^2} \sum_{c=1}^K n_{c, i}^2$$
   - Numerically verified in `audit/evidence_recovery/03_experimental_claim_reconciliation.md`.
   - Max absolute residual against full co-association diagonal is **$2.78 \times 10^{-17}$** (machine precision zero).
   - Time complexity reduces from $\mathcal{O}(N^2)$ to $\mathcal{O}(NM + MK)$.

2. **Bipartite Spectral Transfer-Cut (Proposition 3)**:
   - Constructing $B \in \mathbb{R}^{N \times L}$ and solving the normalized Laplacian $L_{norm} = I - D^{-1/2} W_{anchor} D^{-1/2}$ on $W_{anchor} = B^T B \in \mathbb{R}^{L \times L}$ scales with linear auxiliary memory $\mathcal{O}(NL)$.
   - Verified via `tests/regression/test_scaling_timing.py`.

---

## 8. AutoK Algorithmic Failure: Proof & Empirical Evidence

### 8.1 Mathematical Proof of PAC Collapse
In `src/icc/consensus/autok.py`, the anchor co-association matrix is computed as:
$$S_{anchor} = B_{norm} B_{norm}^T \quad \text{where } B_{norm} = D^{-1} B$$
Because $B \in \{0, 1\}^{N \times L}$ and each row $i$ has row sum $\sum_{l=1}^L B_{il} \ge \frac{L}{K}$, row normalization enforces:
$$\|B_{norm}(i, :)\|_1 = 1 \implies \langle B_{norm}(i, :), B_{norm}(j, :) \rangle \le \max_l B_{norm}(i, l) \approx \frac{K}{L}$$
For default parameters $L=40$ and $K \in [2, 10]$:
$$\langle B_{norm}(i, :), B_{norm}(j, :) \rangle \le \frac{3}{40} = 0.075 < 0.10$$
Senbabaoglu's Proportion of Ambiguous Clustering (PAC) evaluates:
$$\text{PAC} = \Pr(0.10 < S_{anchor}(i, j) < 0.90)$$
Because the inner products strictly concentrate below $0.075$, **no pair of instances ever enters the ambiguity interval $(0.1, 0.9)$**. Consequently:
$$\text{PAC}(K) \equiv 0.0000 \quad \forall K \in [2, 10]$$
The objective function $\arg\min_K \text{PAC}(K)$ becomes completely flat. Under Python's `np.argmin()`, ties break to the first index, deterministically returning $K_{min}=2$.

### 8.2 Empirical Verification
Forensic audit of `results/evidence_recovery/recovered/adversarial_autok_raw_results.csv` (510 trials across $D \in [50, 5000]$, $K^* \in [2, 8]$, $\sigma_{noise} \in [0.5, 5.0]$) confirms:
- **510 out of 510 trials selected $K=2$ (100% failure rate)**.
- PAC remained identically $0.000000$ across every single candidate $K$.

---

## 9. Conformal Prediction Breakdown & Clinical Diagnostic Toxicity

The manuscript documentation (`docs/theory.md: Sec 9.1`) claims CICC provides distribution-free finite-sample coverage guarantees for biomedical clustering and disease subtyping.

### 9.1 The Pseudo-Label Fallacy
Conformal prediction requires true ground-truth labels $Y$ during calibration. Because clustering is unsupervised, `src/cicc/conformal.py` calibrates non-conformity scores using its own inductive pseudo-labels:
$$\hat{Y}_{cal} = \arg\max_{k} \cos(X_{cal}, c_k)$$
Split-conformal theory guarantees coverage strictly for $\Pr(\hat{Y}_{test} \in C(X_{test})) \ge 1 - \alpha$. It provides **zero mathematical guarantee** for unobserved clinical pathology $\Pr(Y_{true} \in C(X_{test}))$.

### 9.2 Empirical Breakdown on Real Clinical Data
Testing CICC on real biomedical cohorts with known clinical pathology (nominal $1 - \alpha = 90\%$):

| Cohort Name | Sample Size ($N$) | Ground Truth $K^*$ | CICC Empirical Coverage | Single-Label Coverage | Toxic Misclassification Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Leukemia** (AML vs ALL) | 72 | 2 | **62.2%** | 44.4% | **18.1%** |
| **SRBCT** (4 Childhood Cancers) | 83 | 4 | **37.0%** | 19.8% | **24.1%** |
| **Synthetic Demo** | 150 | 3 | **46.7%** | 33.3% | **20.0%** |

In $20\%$ of cases, CICC issued a confident, single-label prediction set that completely excluded the patient's true cancer class (e.g., Acute Lymphoblastic Leukemia patients diagnosed as Acute Myeloid Leukemia with model confidence $P > 0.99$).

---

## 10. Target-Decoy / Knockoff Gating Failure & Dead Code Analysis

1. **Exchangeability Violation**: In `src/cicc/decoy.py:generate_decoys()`, synthetic features $\tilde{X}$ are drawn from $\mathcal{N}(0, 1)$, ignoring feature correlation $\Sigma_{XX}$. In the presence of real biological co-expression networks, $\text{Cov}(X_j, \tilde{X}_j) = 0$, violating the fundamental exchangeability requirement of Model-X knockoffs.
2. **Post-Clustering Selection Bias**: Feature importance statistics $W_j = |T_j| - |\tilde{T}_j|$ are computed using pseudo-labels derived from the same data, introducing positive feedback loop bias ($\Pr(W_j > 0) = 60.9\%$ under pure null noise).
3. **Fallback Bug Driving 100% FDR**: At line 122 of `src/cicc/decoy.py`:
   ```python
   if len(selected) == 0:
       selected = np.argsort(W)[-max(2, int(0.05 * D)):]
   ```
   When data contains pure noise (true FDR should be 0 discoveries), the algorithm forcibly selects the top $5\%$ noisy features, guaranteeing **$100\%$ empirical FDR**.
4. **Dead Code**: In `src/cicc/inductive.py`, the `selected_features` mask returned by `DecoyFeatureGating` is never passed to `predict()`. The feature gating code is executed, generates invalid discoveries, and is then completely discarded.

---

## 11. Seed Reproducibility & Synthetic Data Leakage Audit

In `src/icc/core.py:46`, the dataset synthesis pipeline is implemented as:
```python
def build_dataset(n_samples=150, n_features=2000, seed=42):
    X_sig, y = make_signal(n_samples=n_samples, seed=RNG_DATA_SEED) # RNG_DATA_SEED = 42
    X_noise = make_noise(n_samples=n_samples, n_features=n_features, seed=seed)
    return np.hstack([X_sig, X_noise]), y
```
Because `seed=RNG_DATA_SEED` (42) is hardcoded inside `make_signal()`, **the true cluster centroids, sample coordinates, and ground-truth labels are 100% frozen across all runs**. When benchmark scripts iterate over 10 different random seeds, they are not testing algorithmic robustness across different data geometries; they are testing 10 realizations of isotropic noise overlaid onto the exact same static signal points.

---

## 12. Benchmark Verification & Baseline Timing Truth

Historical documentation asserted that ICC-v2 achieved $\text{ARI}=1.0$ in $0.0039\,\text{s}$ on synthetic data, while Standard Consensus took $0.3662\,\text{s}$ (a 94x speedup claim).

### Independent Re-execution on Clean Environment
Re-running Seed 101 on an AMD64 platform reveals:
- **Standard Consensus**: Ran in **$0.1210\,\text{s}$** (3x faster than reported) and achieved **$\text{ARI} = 1.0000$** across all 10 test seeds.
- **ICC-v2**: Required **$0.0125\,\text{s}$** and achieved **$\text{ARI} = 0.4396$** on Seed 101 (failing to recover true clusters).

The historical benchmark tables cherry-picked seeds and artificially degraded the baseline implementation.

---

## 13. Packaging, Distribution & Console Script Defects

An independent installation audit in an isolated clean virtual environment revealed critical packaging defects in the distributed wheel:

1. **Omission of `scripts/`**: The wheel excludes `scripts/` (correctly, per standard Python packaging).
2. **Broken Entrypoints**: `pyproject.toml` defines:
   ```toml
   [project.scripts]
   icc = "icc.__main__:main"
   icc-demo = "scripts.demo:main"
   icc-run = "scripts.reproduce:main"
   ```
3. **Execution Failure**:
   - `icc-demo` and `icc-run` crash immediately: `ModuleNotFoundError: No module named 'scripts'`.
   - `icc` crashes: `ImportError: attempted relative import with no known parent package` due to an unparented relative import in `src/icc/__main__.py:4`.

All three console scripts fail out-of-the-box for any user installing the wheel via `pip install`.

---

## 14. CI Matrix Coverage & Verification Blind Spots

- **CI Evolution**: Commit `7ddbe83` successfully expanded `.github/workflows/ci.yml` to test Python 3.10 through 3.14 across Ubuntu and Windows.
- **Actions Execution**: GitHub Actions Run ID `41328272363` passed all 10 matrix jobs.
- **Local Verification**: 133/133 unit tests pass locally on Python 3.14.6.
- **CI Blind Spot**: CI runs tests *only* against an editable source checkout (`pip install -e .`). It never builds a wheel, never installs the wheel in an isolated clean environment, and never executes the console script entrypoints. Consequently, the packaging breakdown bypassed CI undetected.

---

## 15. Manuscript-to-Code Traceability Analysis

An end-to-end traceability audit mapped all 10 primary algorithmic components between `main.tex`, `docs/theory.md`, source files, and unit tests (recorded in `audit/evidence_recovery/10_manuscript_code_traceability.csv`):
- **Components matching theory and empirically reproducible**: 5 (BGSS Gating, Linear Determinacy Identity, Bipartite Spectral Cut, Stability Centroids, Inductive Cosine Projection).
- **Components with theoretical flaws or empirical invalidation**: 5 (Certified Anchor Lift, CICC Conformal Prediction, Knockoff Feature Gating, AutoK Model Order Selection, Synthetic Data Generation).

---

## 16. Claim-by-Claim Evidence Grading Table

| Claim ID | Headline Claim / Hypothesis | Manuscript Ref | Raw Artifact | Evidence Grade | Scientific Status |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **CLM-01** | Stability–Accuracy Discordance in High-D | `main.tex`: Sec 3 | `stats.json` | **A** | Verified & Reconciled ($+0.485$ global, $+0.687$ extreme subset). |
| **CLM-02** | BGSS Saliency Filters Unimodal Noise | `main.tex`: Sec 4.1 | `exp2_real_high_d_factorial.csv` | **A** | Verified ($BC \ge 5/9$ isolates bimodal signals). |
| **CLM-03** | Certified Anchors Outperform Random Anchors | `main.tex`: Sec 4.2 | `exp2_real_high_d_factorial.csv` | **D** | **Falsified** ($\Delta = +0.019, p = 0.844$; null result). |
| **CLM-04** | Linear Determinacy Algebraic Identity | `main.tex`: Prop 2 | `03_claim_reconciliation.md` | **A** | Verified exact ($2.78 \times 10^{-17}$ residual). |
| **CLM-05** | Bipartite Graph Yields $\mathcal{O}(NL)$ Memory | `main.tex`: Sec 4.2 | `test_scaling_timing.py` | **A** | Verified linear auxiliary scaling. |
| **CLM-06** | ICC-AutoK Determines True Cluster Order $K^*$ | `docs/theory.md`: Sec 3 | `adversarial_autok_raw_results.csv` | **D** | **Falsified** (100% collapse to $K_{min}$ on 510/510 trials). |
| **CLM-07** | CICC Conformal Guarantees for Clinical Phenotyping | `docs/theory.md`: Sec 9.1 | `conformal_audit_results.json` | **D** | **Falsified** (37%–62% coverage; 20% toxic misclassifications). |
| **CLM-08** | Knockoff Gating Controls False Discovery Rate | `docs/theory.md`: Sec 9.2 | `knockoff_audit_results.json` | **D** | **Falsified** (100% FDR under null; dead code in classifier). |
| **CLM-09** | Synthetic Speedup & Accuracy over Baselines | `benchmarks/` | `clean_env_results.json` | **D** | **Falsified** (Baseline is 3x faster; ICC-v2 ARI=0.44 on Seed 101). |
| **CLM-10** | Synthetic Seeds Generate Diverse Data | `src/icc/core.py` | `src/icc/core.py:46` | **D** | **Falsified** (`seed=42` freezes signal coordinates and labels). |
| **CLM-11** | Python 3.10–3.14 Compatibility | `.github/workflows/` | GitHub Run `41328272363` | **A** | Verified on CI and local AMD64 environment. |
| **CLM-12** | Turnkey CLI Console Scripts in Wheel | `pyproject.toml` | `08_packaging_audit.md` | **D** | **Falsified** (Scripts crash with `ModuleNotFoundError`). |

---

## 17. Root Cause Analysis

1. **Premature Public Claims Driven by Surrogate Validation**: Conformal guarantees were validated against self-generated pseudo-labels rather than unobserved ground truth.
2. **Metric Normalization Mismatch**: Applying an ambiguity interval designed for binary co-association matrices $[0, 1]$ to an $L_1$ normalized bipartite matrix without rescaling.
3. **Incomplete Git Remediation**: Attempting history cleanup with standard working-tree deletions (`git rm`) rather than an authoritative object filter and PR reference purge.
4. **Packaging Verification Gap in CI**: Lack of an isolated wheel installation testing stage in `.github/workflows/ci.yml`.

---

## 18. Prioritized Remediation Roadmap & Dependency Graph

Remediation must proceed across four structured phases with strict gating:

```
[Phase 1: Confidentiality Rewrite] (P0)
       │
       ▼
[Phase 2: Algorithmic & Statistical Repair] (P0/P1)
  ├── Conformal Clinical Disclaimers (P0)
  ├── AutoK Metric Dynamic Calibration (P1)
  ├── Knockoff Exchangeability / Dead Code Fix (P1)
  └── Synthetic Seed Propagation Fix (P1)
       │
       ▼
[Phase 3: Unbiased Re-Benchmarking & Packaging] (P1)
  ├── Re-run Synthetic & Real Factorial Benchmarks
  ├── Reconcile Baseline Wall-Clock Times
  └── Fix Console Scripts & Add Wheel CI Test
       │
       ▼
[Phase 4: Manuscript Alignment & Submission Gate] (P1)
  ├── Update numbers.tex Macros
  ├── Reframe Anchor Certification in main.tex
  └── Retract AutoK from Main Paper Claims
```

Detailed task tracking and dependencies are documented in `audit/remediation/01_prioritized_findings.csv` and `audit/remediation/02_dependency_graph.md`.

---

## 19. Manuscript Text Revision & Retraction Protocol

1. **Retract AutoK Model Order Selection**: Remove claims of automated $K$ discovery from the abstract, introduction, and Table 8. State that unsupervised order selection under heavy noise remains an open challenge.
2. **Reframe Anchor Certification**: Update Section 4.2 to present bipartite anchoring as an asymptotic memory reduction technique ($\mathcal{O}(NL)$ vs $\mathcal{O}(N^2)$), explicitly reporting the null accuracy lift over random anchors ($\Delta = +0.019, p = 0.844$).
3. **Restrict Conformal Claims**: Add explicit theoretical boundary disclaimers in documentation: CICC conformal sets guarantee finite-sample coverage strictly with respect to internal algorithmic pseudo-labels, NOT external clinical pathology.
4. **Reconcile Runtimes**: Report verified wall-clock times for Standard Consensus ($0.12\text{s}$) and remove exaggerated 94x speedup claims.

---

## 20. Final Readiness Checklist & Submission Decision Gates

Before any manuscript submission to DMKD, the repository must pass all 6 mandatory gates:

- [ ] **Gate 1 (Confidentiality)**: Remote history rewritten; commit `e3f54cc` unreachable; all 22 GitHub PR refs purged.
- [ ] **Gate 2 (Clinical Safety)**: Conformal docstrings and documentation contain explicit pseudo-label coverage framing and clinical disclaimers.
- [ ] **Gate 3 (AutoK Correction)**: AutoK rewritten and verified to achieve $\ge 90\%$ accuracy across $K \in [2, 10]$ in synthetic parameter sweeps.
- [ ] **Gate 4 (Seed Independence)**: `build_dataset()` propagates caller seeds to `make_signal()`; verified by unit tests.
- [ ] **Gate 5 (Package Usability)**: Wheel installs cleanly in isolated environment; `icc`, `icc-demo`, `icc-run` execute without error in CI.
- [ ] **Gate 6 (Manuscript Integrity)**: Every number in `main.tex` and `numbers.tex` traces directly to an immutable raw microdata file in `results/`.

**Current Status**: All gates are currently **BLOCKED / PENDING**.  
**Final Scientific Verdict**: **NO-GO**.
