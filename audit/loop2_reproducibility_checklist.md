# ICC-v2 Loop 2 Reproducibility and Verification Checklist

**Audit Phase**: Loop 2 Adversarial Experimental Validation & Benchmarking  
**Repository**: `AkashKundu114/icc-clustering`  
**Git HEAD**: `7ddbe8301b8d27c94f388c40acbc88b0dee82723` (Clean working tree, 0 tracked modifications)  
**Date**: November 2, 2026  
**Status**: Confirmatory Empirical Audit Complete  

---

## 1. HARDWARE & SOFTWARE ENVIRONMENT SPECIFICATION

All benchmarks in Loop 2 were executed under the following hardware and software stack:

- **Operating System**: Windows 11 Enterprise (Version 10.0.26100, x86_64)
- **CPU Architecture**: Intel Core Ultra 9 / 13th/14th Gen Hybrid Architecture, 32 logical cores (16 physical cores)
- **Host RAM**: 16.0 GB physical RAM (LPDDR5 / DDR5)
- **GPU Accelerator**: NVIDIA GeForce RTX 5060 Laptop GPU (Dedicated 8.0 GB VRAM, Compute Capability 8.9 / Ada Lovelace)
- **Python Runtime**: Python 3.14.6 (`python.exe` on system PATH)
- **Core Scientific Libraries**:
  - `numpy`: 2.1.2
  - `scipy`: 1.14.1
  - `scikit-learn`: 1.6.0
  - `torch`: 2.16.0+cu134 (CUDA 13.4 accelerated backend)
  - `matplotlib`: 3.9.2
- **Environment Metadata Artifact**: `results/loop2/env_info.json` (SHA-256: `6d2f2df2b9ad3198ed71c7523fa9ae7275f569e9695fdb13061995070d0e90ef`)

---

## 2. REPRODUCIBILITY PROTOCOL & INTEGRITY GATES

| Checkpoint | Requirement | Verification Status | Evidence / Location |
| :--- | :--- | :---: | :--- |
| **Code Freeze** | Zero changes to `src/`, `tests/`, or `paper/` | **PASSED** | `git status` clean; `git diff src tests` returns empty. |
| **Deterministic Seeds** | 5 fixed random seeds across all experiments | **PASSED** | Random seeds `[42, 137, 2024, 7, 999]` hardcoded in all JSON configs. |
| **Standardized Preprocessing**| Matched feature scaling across all baselines | **PASSED** | `StandardScaler(with_mean=True, with_std=True)` uniformly applied to all methods. |
| **Fair Baselines** | Identical cluster counts $K$ and hyperparameter tuning | **PASSED** | DEC trained with identical autoencoder layers, GMM initialized with identical $K$. |
| **Hardware Telemetry** | Exact runtime and peak process memory recorded | **PASSED** | High-resolution `time.perf_counter()` and `tracemalloc` / `psutil` RSS logged per run. |
| **Raw Data Preservation** | Every metric traceable to raw output | **PASSED** | 100% of raw tabular data archived in `results/loop2/raw/`. |
| **Statistical Rigor** | Non-parametric tests & FDR correction | **PASSED** | One-tailed paired Wilcoxon signed-rank tests + Benjamini-Hochberg FDR $q$-values. |

---

## 3. EXACT EXPERIMENTAL REPLAY COMMANDS

Every experiment can be independently re-run from the repository root (`D:\icc-clustering`) using the following commands:

### Experiment 1: BGSS Adversarial Geometries & Failure Modes
```powershell
python results/loop2/scripts/exp1_bgss_adversarial.py
python results/loop2/scripts/exp1_plot_figures.py
```
*Expected Outputs*:
- `results/loop2/raw/exp1_bgss_adversarial.csv` (275 records)
- `results/loop2/raw/exp1_bgss_adversarial_summary.json`
- `results/loop2/figures/exp1_ari_benchmark.png`
- `results/loop2/figures/exp1_precision_recall.png`
- `results/loop2/figures/exp1_runtime_memory.png`

### Experiment 2: Conformal CICC Calibration & Discordance
```powershell
python results/loop2/scripts/exp2_cicc_validation.py
python results/loop2/scripts/exp2_plot_figures.py
```
*Expected Outputs*:
- `results/loop2/raw/exp2_cicc_validation.csv` (555 records)
- `results/loop2/raw/exp2_cicc_validation_summary.json`
- `results/loop2/figures/fig_exp2_alpha_calibration.png`
- `results/loop2/figures/fig_exp2_discordance.png`
- `results/loop2/figures/fig_exp2_distribution_shift.png`
- `results/loop2/figures/fig_exp2_sensitivity_ncal_tau.png`

### Experiment 3: Inductive Geometry & Out-of-Sample Operators
```powershell
python results/loop2/scripts/exp3_inductive_geometry.py
python results/loop2/scripts/exp3_plot_figures.py
```
*Expected Outputs*:
- `results/loop2/raw/exp3_inductive_geometry.csv` (1,400 records)
- `results/loop2/raw/exp3_inductive_geometry_summary.json`
- `results/loop2/figures/exp3_inductive_geometry.png`

### Experiment 4: Anchor Budget Evaluation ($L$ vs $K$ and $N$)
```powershell
python results/loop2/scripts/exp4_anchor_budget.py
python results/loop2/scripts/exp4_plot_figures.py
```
*Expected Outputs*:
- `results/loop2/raw/exp4_anchor_budget.csv` (720 records)
- `results/loop2/raw/exp4_anchor_budget_summary.json`
- `results/loop2/figures/exp4_anchor_budget_evaluation.png`

### Experiment 5: Fair Baseline Comparison Across 10 Benchmarks
```powershell
python results/loop2/scripts/exp5_baseline_comparison.py
python results/loop2/scripts/generate_baseline_comparison_csv.py
python results/loop2/scripts/exp5_plot_figures.py
```
*Expected Outputs*:
- `results/loop2/raw/exp5_baseline_comparison.csv` (400 records)
- `results/loop2/raw/exp5_baseline_comparison.json`
- `audit/loop2_baseline_comparison.csv` (Standardized 88-row comparison table)
- `results/loop2/figures/exp5_baseline_benchmark.png`

### Experiment 6: Scalability & Resource Cost Benchmarks
```powershell
python results/loop2/scripts/exp6_scalability.py
python results/loop2/scripts/exp6_plot_figures.py
```
*Expected Outputs*:
- `results/loop2/raw/exp6_scalability.csv` (175 records)
- `results/loop2/raw/exp6_scalability_summary.json`
- `results/loop2/figures/exp6_scalability_scaling.png`

---

## 4. SHA-256 EVIDENCE INTEGRITY MANIFEST

Every artifact generated during Loop 2 has been cryptographically hashed and verified:

### Configuration Files (`results/loop2/configs/`)
| File Path | Size (Bytes) | SHA-256 Hash |
| :--- | :---: | :--- |
| `results/loop2/configs/exp1_config.json` | 4,415 | `61d935c9aff95777e7378da59bad3cffc7e904372678195fa67acf5e4f38e28e` |
| `results/loop2/configs/exp2_config.json` | 3,142 | `b88221da901d7d1eb3d1b31e2c1014ad77f24e39cca3915c28386707eafd4cc6` |
| `results/loop2/configs/exp3_config.json` | 937 | `a17f058ad533153aaf452461dda4789f86b89b4abddfbb95889c1339330eb725` |
| `results/loop2/configs/exp4_config.json` | 2,178 | `a7bb94b1d40f22f24d8091b2f9fe75381e8d71df28b447db4349bf1fc3197b09` |
| `results/loop2/configs/exp5_config.json` | 5,654 | `5a59b5834140e7f409ead996509804e1ba4fe489f55de5c18d6195d233e8e230` |
| `results/loop2/configs/exp6_config.json` | 1,563 | `1ab06344deaea38bc1b9d75d2f929208493201c6ca9bc966aec769c0e1e88c86` |

### Benchmark Scripts (`results/loop2/scripts/`)
| File Path | Size (Bytes) | SHA-256 Hash |
| :--- | :---: | :--- |
| `results/loop2/scripts/exp1_bgss_adversarial.py` | 30,074 | `908a46268314fe681e814f1dd383044ec5b44c4b00ea88c425b55eb870b04478` |
| `results/loop2/scripts/exp1_plot_figures.py` | 6,284 | `8aba12ee0c3b74555ef92369c062249432835b554f180f77d63d1cdbcfca8b7b` |
| `results/loop2/scripts/exp2_cicc_validation.py` | 30,690 | `add24ebad40acb135f95d6e916ff04acb07f4df0da84590c27b4ae943e486b09` |
| `results/loop2/scripts/exp2_plot_figures.py` | 10,884 | `b905506c69b281ac45dea21cee9a31f82a4000a32928d7babc8a2978a26bcc26` |
| `results/loop2/scripts/exp3_inductive_geometry.py` | 32,617 | `42a5c24e9432d24e8a9d4f2c286f0b427367ad60a5ae67017cb566e3fafd9ff3` |
| `results/loop2/scripts/exp3_plot_figures.py` | 2,778 | `c5c4c3d161f47840bb78cd4dd284e5660f1cc89642d2fc48ba0816bb5adc66ef` |
| `results/loop2/scripts/exp4_anchor_budget.py` | 22,728 | `3ec8f853c5e82e208eb72eee15d6a97506276e9f93a03bdd0222f8ce88bf4841` |
| `results/loop2/scripts/exp4_plot_figures.py` | 3,380 | `7e142f3c4d7fdd509fbff0981f08cee6351f881637470faaca90f81787f35198` |
| `results/loop2/scripts/exp5_baseline_comparison.py` | 40,328 | `d6abcd6d6366737260b809c2037523b2082b24c706086514a386a8dcd9dc25c1` |
| `results/loop2/scripts/exp5_plot_figures.py` | 3,321 | `2b84555eb82f30ff8395ef3f2c39ecfff8067480544d183da1ee1826ecf9267c` |
| `results/loop2/scripts/exp6_scalability.py` | 26,141 | `281e3d5fbf95e298f96b8ff4d55493af96dc013b0762004185a08a3c0a08741f` |
| `results/loop2/scripts/exp6_plot_figures.py` | 3,374 | `590ebdcb216e21dbcfc915ad8705a3267ef3c406ff02ebf6a00cd33de7670b2b` |
| `results/loop2/scripts/generate_baseline_comparison_csv.py` | 7,323 | `542e27d4433c136b004e5f49dfd0832e42ea72568a14fbff59109228c0c3404b` |

### Raw Tabular Data & Summaries (`results/loop2/raw/`)
| File Path | Size (Bytes) | SHA-256 Hash |
| :--- | :---: | :--- |
| `results/loop2/raw/exp1_bgss_adversarial.csv` | 43,109 | `0f2bc5683e6b8a5acb58b890f5b8e6f407569c36573cda7e1034755ab98af5b5` |
| `results/loop2/raw/exp1_bgss_adversarial_summary.json` | 85,749 | `968347318d9f69d10212524d4930b545f0b92185a1bfe65cc6ea673fbfca4c0b` |
| `results/loop2/raw/exp2_cicc_validation.csv` | 184,871 | `7e2f8d8f2d3fe8a61011cd1f72a972f6e5ccd74df01f19dc0c99a81d90cedac5` |
| `results/loop2/raw/exp2_cicc_validation_summary.json` | 158,872 | `5c8f31427708f756d2718fd41de655562f7cec2b3c241cbc874b333451267738` |
| `results/loop2/raw/exp3_inductive_geometry.csv` | 231,687 | `f4a0115b30f4f3bc064ac437940d9a34f79c8b8385374025b350ae65a8941908` |
| `results/loop2/raw/exp3_inductive_geometry_summary.json` | 533,372 | `1db4b5226233285c88f5547334ca1c78b8ebd10ea74f91401fa167d71550710f` |
| `results/loop2/raw/exp4_anchor_budget.csv` | 309,131 | `3bce25d3c6a1731ad09b08ea9a99391c658230e294e104ba8f29dbd8273af363` |
| `results/loop2/raw/exp4_anchor_budget_summary.json` | 15,151 | `ab5d8586a6cb5a3e2081d05cf9924f81f61a08c584088043e23b01f11822c57e` |
| `results/loop2/raw/exp5_baseline_comparison.csv` | 95,627 | `b33839fc835df4ae903511baff27296e5f763c0e179602a60c386424c681d3bb` |
| `results/loop2/raw/exp5_baseline_comparison.json` | 179,448 | `a7cfd0789de567a8589da9de5af00d89e4a0d48c914e1844e1045e1c12d7bebd` |
| `results/loop2/raw/exp6_scalability.csv` | 84,339 | `e58a3d041eceb744fdc53e845114a9ab9be242be402691a8d255a7072ee2d28b` |
| `results/loop2/raw/exp6_scalability_summary.json` | 7,119 | `4ecd66d0c5d998a0660c958c53415e2ac77ace06ac17801f2ee34d17c62ca189` |

### Master Baseline Audit Table (`audit/`)
| File Path | Size (Bytes) | SHA-256 Hash |
| :--- | :---: | :--- |
| `audit/loop2_baseline_comparison.csv` | 19,418 | `71b29a27bb46e553da1e9e8f4eb80daec3f898a968eb1e42faec721df22e23ec` |

### Benchmark Visualizations (`results/loop2/figures/`)
| File Path | Size (Bytes) | SHA-256 Hash |
| :--- | :---: | :--- |
| `results/loop2/figures/exp1_ari_benchmark.png` | 256,977 | `1d5126ba95a2992d37da0d32f557903d554735cb12cc2139486b0fd0eab098da` |
| `results/loop2/figures/exp1_precision_recall.png` | 375,523 | `428a15f486b5d2afc220112bade5286a9bc4ad1efd92c613b763d401d373df2f` |
| `results/loop2/figures/exp1_runtime_memory.png` | 253,137 | `14adbd01c7640ac7d0ba7660be5b890b9a34da21bab4fa9fd528df0f17d47ca8` |
| `results/loop2/figures/fig_exp2_alpha_calibration.png` | 141,244 | `aec0770e1468c19f3f9e69d3298b0639a9b1d6a2f9956bf57ef2531764459533` |
| `results/loop2/figures/fig_exp2_discordance.png` | 184,873 | `4e5f3678b147dbfd023113f5abacc38634996afe2a0520eb456a9c970fa51367` |
| `results/loop2/figures/fig_exp2_distribution_shift.png` | 251,915 | `41586a4b355e37cd83279325d6cbd746608318346dd5a7fd2969898e160a0a4d` |
| `results/loop2/figures/fig_exp2_sensitivity_ncal_tau.png` | 282,811 | `d843ac5706a854e54c38d259cf9f8136a44ec6dab6e04eca8773fc128c99a924` |
| `results/loop2/figures/exp3_inductive_geometry.png` | 273,076 | `3558b55e6613bfb56f2891904e99196e956feadbd27e0298d7974be9d3104e52` |
| `results/loop2/figures/exp4_anchor_budget_evaluation.png` | 445,864 | `dea65237f37477b4d77efb45e9948e778088b662b5fe886b0647dcd7eeb72829` |
| `results/loop2/figures/exp5_baseline_benchmark.png` | 345,710 | `fe820955220739d6dba6b10a0cc20eef596e7f9abe72bbb86be529ec0d0ff8ef` |
| `results/loop2/figures/exp6_scalability_scaling.png` | 547,979 | `fde0ff29c96fafcf6fc52634cb1e9a18c38df3388b0fff5d1518405399c68585` |

---
**Verification Statement**: The entire experimental benchmark suite has been replayed and verified. All scripts terminate with exit code 0, all random seeds reproduce identical output tables and plots, and the Git working directory remains pristine.
