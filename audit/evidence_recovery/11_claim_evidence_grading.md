# Evidence Grading Report: Headline Research and Technical Claims

**Repository**: `AkashKundu114/icc-clustering`  
**Current HEAD**: `7ddbe8301b8d27c94f388c40acbc88b0dee82723`  
**Audit Component**: Phase 6 — Scientific and Methodological Evidence Verification  
**Evaluation Target**: DMKD Submission Readiness  

---

## 1. Grading Standard and Taxonomy

To ensure objective evaluation, every claim presented in the manuscript (`main.tex`, `numbers.tex`), technical documentation (`docs/theory.md`), and historical audit reports is evaluated against empirical microdata and mathematical rigor, categorized under the following grading scale:

- **Grade A (Independently Reproduced)**: The claim is verified by exact raw microdata artifacts, executes reproducibly via automated scripts, and matches theoretical derivations within machine precision.
- **Grade B (Reproducible with Minor Adjustments)**: The claim holds empirically, but required minor parameter alignment, notation reconciliation, or pipeline reconstruction.
- **Grade C (Partially Supported / Ambiguous)**: Evidence supports the claim only under specific unstated boundary conditions; significant variance or methodological caveats exist.
- **Grade D (Unsupported / Contradicted / Falsified)**: The claim is mathematically invalid, empirically refuted by experiments, driven by statistical leakage, or contradicted by recovered raw data.
- **Grade N/A (Definitional / Tautological)**: Architectural definitions or notation requiring no empirical proof.

---

## 2. Headline Claims Evidence Grading Matrix

| Claim ID | Headline Claim / Hypothesis | Manuscript / Doc Reference | Empirical Evidence & Artifacts | Assigned Grade | Rationale and Technical Findings |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **CLM-01** | **Stability–Accuracy Discordance Exists in High Dimensions** | `main.tex`: Sec 3, Fig 1; `numbers.tex` | `stats.json`, `subsample_stability_summary.csv`, `real_data_stability_summary.csv` | **A** | **Fully Verified & Reconciled**. Recovered raw data demonstrates that consensus subsample stability diverges from true clustering accuracy under high-dimensional noise. The mathematical arithmetic discrepancy ($0.687$ extreme subset mean vs $+0.485$ global gap) was fully resolved. |
| **CLM-02** | **BGSS Saliency Filtering Isolates True Clusters** | `main.tex`: Sec 4.1; `docs/theory.md`: Sec 2 | `exp2_real_high_d_factorial.csv`, `test_consensus.py` | **A** | **Fully Verified**. Sarle's bimodality coefficient threshold ($BC \ge 5/9$) successfully filters unimodal distractor noise in synthetic and high-dimensional genomic benchmarks. |
| **CLM-03** | **Certified Anchor Selection Yields Superior Consensus Accuracy Over Random Anchors** | `main.tex`: Sec 4.2; `docs/theory.md`: Sec 3 | `exp2_real_high_d_factorial.csv` | **D** | **Falsified / Null Result**. Controlled factorial knockout reveals Full ICC-v2 (V5, Certified Core Anchors, $\text{ARI}=0.217$) vs Random Anchors (V4, Uniform Anchors, $\text{ARI}=0.198$) yields $\Delta = +0.019$ ($95\%\text{ CI } [-0.039, +0.082]$, Wilcoxon $p = 0.844$). The certified anchor mechanism adds zero statistically significant accuracy lift. |
| **CLM-04** | **Exact Linear-Memory Determinacy Identity** | `main.tex`: Sec 4.2 (Prop 2); `docs/theory.md`: Sec 3 | `audit/evidence_recovery/03_experimental_claim_reconciliation.md` | **A** | **Mathematically and Numerically Exact**. The sample-level co-association diagonal is algebraically identical to the sum of partition-wise cluster memberships. Residual error against raw co-association matrix is $2.78 \times 10^{-17}$ (machine precision zero). |
| **CLM-05** | **Reduced Bipartite Spectral Consensus Achieves Linear Complexity $\mathcal{O}(NL)$** | `main.tex`: Sec 4.2, Table 1; `docs/theory.md`: Sec 4 | `test_scaling_timing.py`, `stats.json` | **A** | **Empirically Verified**. Construction of the $N \times L$ bipartite affinity matrix avoids the full $N \times N$ co-association matrix, reducing auxiliary memory from quadratic to strictly linear in $N$. |
| **CLM-06** | **ICC-AutoK Reliably Discovers True Number of Clusters $K^*$** | `docs/theory.md`: Sec 3-4; `research_audit/14_unknown_k_results.md` | `adversarial_autok_raw_results.csv`, `adversarial_autok_summary.json` | **D** | **Systemic Mathematical Collapse**. $L_1$ row normalization forces anchor inner products to satisfy $\langle B_i, B_j \rangle \le K/L \approx 0.075 < 0.10$. Senbabaoglu's ambiguity interval $(0.1, 0.9)$ is completely empty, forcing $\text{PAC} \equiv 0.0000$ across all $K \in [2, 10]$. AutoK collapses to $K_{min}=2$ in **510 out of 510 trials (100% failure rate)**. |
| **CLM-07** | **CICC Conformal Prediction Provides Rigorous Error Guarantees for Clinical Diagnosis** | `docs/theory.md`: Sec 9.1; `cicc/conformal.py` | `conformal_audit_results.json`, `test_cicc.py` | **D** | **Severe Diagnostic Misattribution / Statistical Invalidation**. CICC split-conformal prediction provides valid coverage *only* against its own internal cosine-softmax pseudo-labels. Evaluated against real clinical pathology, empirical coverage collapses to **62.2% on Leukemia** and **37.0% on SRBCT** (target $1 - \alpha = 90\%$). In synthetic demos, **20% of samples receive confident, single-label toxic misclassifications** (e.g., Acute Lymphoblastic Leukemia falsely certified as AML with $P > 0.99$). |
| **CLM-08** | **Model-X Knockoff / Target-Decoy Feature Gating Controls FDR** | `docs/theory.md`: Sec 9.2; `src/cicc/decoy.py` | `knockoff_audit_results.json`, `src/cicc/inductive.py` | **D** | **Methodologically Flawed & Dead Code**. Decoys are drawn as independent standard Gaussian noise, violating Model-X pairwise exchangeability ($\text{Cov}(X_j, \tilde{X}_j) = 0$). Feature statistics conditioned on post-clustering labels introduce selection bias. Furthermore, a fallback bug at `decoy.py:122` forces arbitrary noise selection under null data, yielding **100% empirical FDR**. Selected features are completely ignored by `inductive.py`. |
| **CLM-09** | **ICC-v2 Outperforms Standard Consensus in Speed and Accuracy Across All Benchmark Seeds** | `benchmarks/`; historical audit reports | `results/evidence_recovery/recovered/clean_env_results.json` | **D** | **Falsified**. Historical claim stated ICC-v2 achieved $\text{ARI}=1.0$ in $0.0039\text{s}$ while Standard Consensus took $0.3662\text{s}$. Independent re-execution on Seed 101 reveals Standard Consensus runs in **$0.1210\text{s}$** (3x faster than reported) with **$\text{ARI} = 1.0$** across all 10 seeds. Conversely, ICC-v2 collapses to **$\text{ARI} = 0.4396$** on Seed 101. |
| **CLM-10** | **Synthetic Signal Generation Validates Diverse Data Regimes Across User Seeds** | `src/icc/core.py`; `tests/unit/test_core.py` | `src/icc/core.py:46`, `audit/evidence_recovery/07_seed_reproducibility.md` | **D** | **Frozen Seed Leakage**. `build_dataset()` hardcodes `seed=42` inside `make_signal()`. Across all seeds passed to `build_dataset()`, true cluster centroids and sample labels are **100% identical and frozen**. Only isotropic noise coordinates vary. |
| **CLM-11** | **Python Compatibility Across Modern Releases (3.10 through 3.14)** | `.github/workflows/ci.yml`; `pyproject.toml` | `python_compatibility_matrix.csv`, GitHub Run `41328272363` | **A** | **Fully Verified**. CI matrix tests 3.10–3.14 across Ubuntu and Windows; Run `41328272363` passed all 10 jobs; 133/133 unit tests pass on local Python 3.14.6 environment. |
| **CLM-12** | **Wheel Distribution Provides Turnkey CLI Console Scripts** | `pyproject.toml: [project.scripts]` | `audit/evidence_recovery/08_packaging_audit.md` | **D** | **Fatal Packaging Breakdown**. Built wheel omits `scripts/` directory and `src/icc/__main__.py` contains relative import errors. Executing `icc`, `icc-demo`, or `icc-run` from a wheel install crashes immediately with `ModuleNotFoundError`. |

---

## 3. Summary of Evidence Grading

- **Grade A (Independently Verified)**: 4 claims (Stability-Accuracy Discordance, BGSS Saliency, Linear Determinacy Identity, Bipartite Scalability, Python 3.10–3.14 Matrix).
- **Grade B / C**: 0 claims.
- **Grade D (Falsified / Contradicted / Scientifically Invalid)**: 7 claims (Anchor Certification Lift, ICC-AutoK Order Selection, Conformal Diagnostic Guarantees, Knockoff FDR Control, Benchmark Speedup/Accuracy, Synthetic Seed Independence, Console Script Packaging).

### Scientific Consequence for DMKD Submission
Because the manuscript and companion documentation elevate AutoK, Conformal Prediction Sets, and Knockoff Gating as headline theoretical contributions, and because the empirical anchor certification lift is statistically null, **the repository and manuscript CANNOT be submitted in their current form**.
