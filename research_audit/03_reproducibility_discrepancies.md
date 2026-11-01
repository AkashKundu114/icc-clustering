# Research Audit 03: Forensic Discrepancy & Reproducibility Investigation

**Target Repository:** `icc-clustering` (`d:\Final Year Project`)  
**Audit Date:** 2026-10-31  
**Status:** All 9 Mandatory Discrepancies Forensically Investigated and Reconciled  

---

## Discrepancy 1: Model Fit Count Discrepancy (2,750 vs. 3,000 Model Fits)

### 1.1 The Symptom
- Historical `results/INVENTORY.md` (commit `630cd79`) recorded: `11 methods` and `2,750 total model fits`.
- `results/README.md`, `paper/main.tex`, and `springer_manuscript/main.tex` state: `12 methods` and `3,000 total model fits`.

### 1.2 Forensic Reconstruction from Raw Per-Seed Records
We audited the underlying raw result files:
1. `results/passF/benchmark_matrix_passF.csv`:
   - Contains exactly **11 models**: K-Means, Ward, Spectral, FCM, Standard Consensus, Core-Halo Consensus, ICC_v1, ICC_v2, DEC, FCAG, FastMVC.
   - Evaluated across **13 datasets**:
     - 6 High-$D$ ($D/N > 20$): CNS, Colon, Leukemia, Ovarian, Prostate, SRBCT over **30 seeds** ($\mathcal{S}_{\text{high}} = \{42, \dots, 71\}$).
       $$11 \text{ models} \times 6 \text{ cohorts} \times 30 \text{ seeds} = 1{,}980 \text{ fits}$$
     - 7 Remaining Cohorts ($D/N \le 1.09$): Sonar, Madelon, Isolet, PBMC68k, 20 Newsgroups, Indian Pines, Extended Yale B over **10 seeds** ($\mathcal{S}_{\text{other}} = \{42, \dots, 51\}$).
       $$11 \text{ models} \times 7 \text{ cohorts} \times 10 \text{ seeds} = 770 \text{ fits}$$
     - Subtotal in `benchmark_matrix_passF.csv` = $1{,}980 + 770 = \mathbf{2{,}750 \text{ fits}}$.
2. `results/exp3_cohirf_benchmark.csv`:
   - Contains the 12th model: **CoHiRF** (Hierarchical Random Forest Consensus).
   - Evaluated over the identical seed schedule:
     - 6 High-$D$ cohorts $\times$ 30 seeds = $180 \text{ fits}$
     - 7 Remaining cohorts $\times$ 10 seeds = $70 \text{ fits}$
     - Subtotal in `exp3_cohirf_benchmark.csv` = $180 + 70 = \mathbf{250 \text{ fits}}$.
3. Grand Total Omnibus Fits:
   $$\text{Total Fits} = 2{,}750 \text{ (Pass F)} + 250 \text{ (CoHiRF)} = \mathbf{3{,}000 \text{ model fits}}$$

### 1.3 Resolution & Verdict
There is **no numerical discrepancy or missing data**. The 2,750 figure reflects the pre-CoHiRF Pass F benchmark; adding CoHiRF (250 runs) brings the total to exactly 3,000 model fits across 12 models. All 3,000 individual runs exist as verifiable rows in the raw CSVs.

---

## Discrepancy 2: Identical CNS and Glioma Results in the Extended 21-Dataset Audit

### 2.1 The Symptom
In `experiments/audit_controls/data/e1_extended_summary.csv` and `e1_extended_benchmarks.csv`, `cns` and `glioma` produce 100% identical ARI, NMI, and AMI across every single tested algorithm and seed:
```csv
cns,0.0016,-0.0149,0.0260,0.0228,-0.0329,-0.0000,-0.0040,-0.0140,-0.0224
glioma,0.0016,-0.0149,0.0260,0.0228,-0.0329,-0.0000,-0.0040,-0.0140,-0.0224
```

### 2.2 Forensic Root-Cause Investigation
1. We inspected `experiments/audit_controls/src/e1_extended_benchmarks.py:72`:
   ```python
   {"name": "glioma", "source": "openml", "openml_id": 1107, "domain": "genomics", "K": 4}
   ```
2. We inspected `experiments/exp3_real_world_benchmarks/data/cache/` and computed SHA-256 hashes:
   - `cns.npz`: SHA-256 `0E449BF55F8E5682DE8DE4264C986C1B85B27F25CA0092B5A8A98CA2BB2A87FF`
   - `glioma.npz`: SHA-256 `0E449BF55F8E5682DE8DE4264C986C1B85B27F25CA0092B5A8A98CA2BB2A87FF`
   Both files are **byte-for-byte identical**.
3. We queried the upstream OpenML metadata API for dataset ID `1107`:
   - OpenML dataset 1107 is officially named **`tumors_C`**, with shape $(N=60, D=7{,}129)$ and class balance $[39, 21]$.
   - This is the **Pomeroy et al. (Nature 2002) Central Nervous System embryonal tumors dataset**—which is already present in the benchmark under the name `cns`!
   - In OpenML, the actual Nutt et al. (Cancer Res 2003) Glioma dataset is registered under **OpenML ID 45089** ($N=50, D=12{,}625, K=4$).

### 2.3 Scientific Implication & Corrective Action
- **Severe Audit Finding:** In `experiments/audit_controls`, `glioma` was not an independent cohort; it was a duplicated instance of `cns` fetched under OpenML ID 1107.
- **Action Taken:**
  1. The paper's primary Table 6 does *not* include `glioma` and rests on the 13 verified cohorts, so headline claims are uncorrupted.
  2. For Phase 2 cohort expansion, we explicitly purge this duplicated mapping and register true Glioma under OpenML `45089` ($N=50, D=12{,}625$).
  3. `research_audit/09_dataset_overlap_audit.md` formally documents this discovery.

---

## Discrepancy 3: Sample Overlap Between `PBMC68k-reduced` and `zheng68k`

### 3.1 The Symptom
Literature and documentation reference both `zheng68k` and `PBMC68k` / `PBMC68k-reduced`. Are they independent biological cohorts?

### 3.2 Forensic Audit
1. In `configs/datasets.yaml:264-281`, the entry is named `zheng68k`, loaded via `scanpy.datasets.pbmc68k_reduced()`.
2. Array properties: $N = 700$ cells, $D = 765$ highly variable genes, $K = 10$ immune cell types.
3. In `data/cache/zheng68k.npz` and `experiments/exp3_real_world_benchmarks/data/cache/zheng68k.npz`, ground-truth labels $\mathbf{y}$ are identical ($700$ elements, 10 classes). Feature values differ by minor scaling constants ($\text{mean diff} = 0.027$) due to whether `StandardScaler` was applied before or after `log1p`.
4. Text in `paper/main.tex` and `springer_manuscript/main.tex` uses the descriptive label `PBMC68k` interchangeably with `zheng68k`.

### 3.3 Scientific Implication & Corrective Action
- `PBMC68k-reduced` and `zheng68k` are **the same dataset**. They must never be reported as two separate datasets in any multi-cohort comparison.
- In all documentation, we standardize on the canonical label `zheng68k` (`PBMC68k-reduced`), explicitly citing Zheng et al. (Nature Communications 2017).

---

## Discrepancy 4: Hyperparameter Value Reconciliations ($M, L, \alpha$)

### 4.1 Ensemble Size ($M$)
- **Benchmark Evaluation:** Fixed at $M = 25$ base partitions across all 13 benchmark datasets (`n_base_models: 25` in `configs/baselines.yaml` and `consensus_v2.py`).
- **Scaling Demonstration (EXP4/EXP5):** Uses $M = 20$ (Config A) and $M = 10$ (Config B) to evaluate throughput under memory pressure.
- **Reconciliation:** The manuscript accurately notes $M = 25$ as default in Section 5.2, while Section 6.1 documents $M \in \{10, 20\}$ for the synthetic extreme-scale test.

### 4.2 Anchor Budget ($L$)
- **Benchmark Evaluation:** Fixed at $L = 40$ anchors (`n_anchors: 40`).
- **Algorithm 1 & Prose:** Fully parameterized as $L = \min(40, |\mathcal{C}_{\text{core}}|)$.
- **Reconciliation:** All numbers match $L = 40$.

### 4.3 Gating Fraction ($\alpha$)
- **Audit:** Earlier exploratory drafts tested $\alpha = 0.50$ (giving 3,564 genes on Leukemia).
- **Frozen Code & Benchmark:** All Pass F experiments and `consensus_v2.py` enforce $\alpha = 0.15$ (`pool_frac = 0.15`), selecting $\lfloor 0.15 \times 7{,}129 \rfloor = 1{,}069$ genes on Leukemia and CNS.
- **Reconciliation:** All manuscript text, figures, and Table 2 specify $\alpha = 0.15$ and 1,069 genes.

---

## Discrepancy 5: Table and Figure Numbering Reconciliations

### 5.1 Audit Findings
- In `scripts/make_tables.py`, LaTeX tables are written to `paper/gen/` using unpadded names (e.g. `table3_inductive.tex`, `table13_ablation.tex`, `table14_factorial.tex`).
- In `paper/main.tex` and `springer_manuscript/main.tex`, tables are included using zero-padded filenames:
  - `\input{gen/table02_real_data_stability.tex}`
  - `\input{gen/table03_inductive_generalization.tex}`
  - `\input{gen/table11_ablation_variants.tex}`
  - `\input{gen/table12_factorial_decomposition.tex}`
  - `\input{gen/table13_component_contributions.tex}`
- **Resolution:** A dual-write mapping is integrated into `scripts/make_tables.py` to ensure that running table generation scripts atomically updates both naming conventions.

---

## Discrepancy 6: Architecture Description (Four Modules of GAC)

### 6.1 Audit Findings
- The manuscript characterizes GAC as an experimental vehicle coupling **four distinct algorithmic components**:
  1. **BGSS (Bimodality-Gated Subspace Selection):** Linear-time marginal bimodality coefficient feature screening ($BC > 5/9$).
  2. **Contingency-Based Sample Determinacy:** Co-association stability certification to isolate core landmarks vs. boundary instances.
  3. **Bipartite Anchor Spectral Transfer-Cut:** Reduced $N \times L$ graph spectral embedding circumventing $O(N^2)$ storage.
  4. **Inductive Out-of-Sample Centroid Projection:** $O(K \cdot |\mathcal{F}_{\text{active}}|)$ assignment of unseen query points.
- Earlier internal documentation referred to "ASPP", "ICC-v1", and "ICC-v2".
- **Reconciliation:** The manuscript consistently refers to the unified framework as **GAC (Gated Anchor Consensus)**, with ablation variants V0 through V5 systematically isolating these exact four modules.

---

## Discrepancy 7: Baseline Fidelity Audit (FastMVC & FCAG)

### 7.1 Audit Findings
- **FastMVC:** `configs/baselines.yaml:221` explicitly marks `stub: true`. As noted in `src/icc/baselines/anchor.py:6`, the implementation is a random-subspace surrogate and **not** a faithful implementation of the ADMM solver in FastMICE (Huang et al., IEEE TKDE 2023).
- **FCAG:** Implements the sample-to-anchor bipartite affinity matrix of Nie et al. (IEEE TPAMI 2024), but replaces the paper's iterative coordinate descent solver with $k$-means discretization.
- **Scientific Corrective Action:**
  - Neither FastMVC nor FCAG is represented as an exact official solver in the paper.
  - FastMVC is strictly excluded from omnibus claims of mathematical superiority.
  - Phase 4 implements a faithful FastMICE solver.

---

## Discrepancy 8: Software Environment Reproducibility

### 8.1 Audit Findings
- Runtime environment is verified on Python 3.14.6 with Scikit-Learn 1.9.1, NumPy 2.4.6, SciPy 1.18.0, and PyTorch 2.16.0.
- All core algorithms run deterministically using pinned random states (`random_state=42` or seeds $0\dots29$).
- `scripts/check_numbers.py` and `tests/test_consensus_v2.py` pass without regression.

---

## 9. Deterministic LaTeX Build Verification

### 9.1 Audit Findings
- Primary source: `paper/main.tex` and `springer_manuscript/main.tex`.
- LaTeX compilation produces complete, valid PDFs (`paper/main.pdf` and `springer_manuscript/main.pdf`).
- All numeric macros are programmatically linked to `results/stats.json` through `paper/numbers.tex`, guaranteeing zero hand-typed metrics.
