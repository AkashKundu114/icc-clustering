# MANUSCRIPT QUANTITATIVE CLAIMS DIRECTORY

Master register of all quantitative claims extracted from the manuscript (*Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes*).

Columns:
- **Claim ID**: Unique identifier for tracking and script verification.
- **Source**: Table, figure, or section citation in paper/main.pdf.
- **Context / Regime**: Dataset, sample size, or experimental configuration.
- **Metric / Statement**: Quantitative measure.
- **Paper Value**: Published value in manuscript text or table.
- **Producing Script**: Target script in the repository expected to produce this value.
- **Reproduced Value**: Value obtained during Phase 1 frozen execution (populated in Phase 1).
- **Delta**: Difference (Absolute / Relative).
- **Status**: PENDING_REPRODUCTION, MATCH (|dARI| <= 0.02, rel error <= 5%), MISMATCH, or BLOCKED.

---

## 1. Table 3: Real-World Multi-Domain Benchmark Matrix (ARI)

| Claim ID | Source | Dataset / Regime | Method | Paper Value | Producing Script | Reproduced Value | Delta | Status |
|---|---|---|---|---|---|---|---|---|
| **CLM-T3-CNS-K-ME** | Table 3 | CNS | K-Means | -0.0273 ± 0.0228 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-CNS-WARD** | Table 3 | CNS | Ward | -0.0224 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-CNS-SPEC** | Table 3 | CNS | Spectral | -0.0040 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-CNS-FCM** | Table 3 | CNS | FCM | 0.0016 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-CNS-STAN** | Table 3 | CNS | Standard_Consensus | -0.0227 ± 0.0188 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-CNS-LI_E** | Table 3 | CNS | Li_et_al_2019 | -0.0055 ± 0.0101 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-CNS-DEC** | Table 3 | CNS | DEC | 0.0124 ± 0.0193 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-CNS-FCAG** | Table 3 | CNS | FCAG | -0.0045 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-CNS-FAST** | Table 3 | CNS | FastMVC | 0.0070 ± 0.0059 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-CNS-ICC_** | Table 3 | CNS | ICC_v1 | -0.0071 ± 0.0269 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-CNS-ICC_** | Table 3 | CNS | ICC_v2 | 0.0281 ± 0.0153 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-COL-K-ME** | Table 3 | COLON | K-Means | 0.0322 ± 0.0600 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-COL-WARD** | Table 3 | COLON | Ward | -0.0158 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-COL-SPEC** | Table 3 | COLON | Spectral | -0.0232 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-COL-FCM** | Table 3 | COLON | FCM | 0.0177 ± 0.0344 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-COL-STAN** | Table 3 | COLON | Standard_Consensus | -0.0050 ± 0.0181 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-COL-LI_E** | Table 3 | COLON | Li_et_al_2019 | -0.0035 ± 0.0124 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-COL-DEC** | Table 3 | COLON | DEC | 0.0379 ± 0.0701 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-COL-FCAG** | Table 3 | COLON | FCAG | -0.0160 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-COL-FAST** | Table 3 | COLON | FastMVC | -0.0163 ± 0.0011 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-COL-ICC_** | Table 3 | COLON | ICC_v1 | -0.0000 ± 0.0110 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-COL-ICC_** | Table 3 | COLON | ICC_v2 | 0.0286 ± 0.0857 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-IND-K-ME** | Table 3 | INDIAN_PINES | K-Means | 0.2114 ± 0.0073 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-IND-WARD** | Table 3 | INDIAN_PINES | Ward | 0.2228 ± 0.0075 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-IND-SPEC** | Table 3 | INDIAN_PINES | Spectral | 0.2291 ± 0.0005 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-IND-FCM** | Table 3 | INDIAN_PINES | FCM | 0.1705 ± 0.0122 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-IND-STAN** | Table 3 | INDIAN_PINES | Standard_Consensus | 0.2235 ± 0.0026 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-IND-LI_E** | Table 3 | INDIAN_PINES | Li_et_al_2019 | 0.1163 ± 0.0349 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-IND-DEC** | Table 3 | INDIAN_PINES | DEC | 0.2071 ± 0.0094 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-IND-FCAG** | Table 3 | INDIAN_PINES | FCAG | 0.2004 ± 0.0096 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-IND-FAST** | Table 3 | INDIAN_PINES | FastMVC | 0.1984 ± 0.0092 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-IND-ICC_** | Table 3 | INDIAN_PINES | ICC_v1 | 0.1294 ± 0.0249 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-IND-ICC_** | Table 3 | INDIAN_PINES | ICC_v2 | 0.1382 ± 0.0312 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ISO-K-ME** | Table 3 | ISOLET | K-Means | 0.4488 ± 0.0267 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ISO-WARD** | Table 3 | ISOLET | Ward | 0.5004 ± 0.0038 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ISO-SPEC** | Table 3 | ISOLET | Spectral | 0.4174 ± 0.0005 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ISO-FCM** | Table 3 | ISOLET | FCM | 0.0588 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ISO-STAN** | Table 3 | ISOLET | Standard_Consensus | 0.4696 ± 0.0185 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ISO-LI_E** | Table 3 | ISOLET | Li_et_al_2019 | 0.3689 ± 0.0357 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ISO-DEC** | Table 3 | ISOLET | DEC | 0.4963 ± 0.0293 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ISO-FCAG** | Table 3 | ISOLET | FCAG | 0.4325 ± 0.0266 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ISO-FAST** | Table 3 | ISOLET | FastMVC | 0.4327 ± 0.0273 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ISO-ICC_** | Table 3 | ISOLET | ICC_v1 | 0.3667 ± 0.0258 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ISO-ICC_** | Table 3 | ISOLET | ICC_v2 | 0.2858 ± 0.0202 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-LEU-K-ME** | Table 3 | LEUKEMIA | K-Means | 0.1010 ± 0.0928 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-LEU-WARD** | Table 3 | LEUKEMIA | Ward | 0.0816 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-LEU-SPEC** | Table 3 | LEUKEMIA | Spectral | 0.1389 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-LEU-FCM** | Table 3 | LEUKEMIA | FCM | 0.1034 ± 0.0082 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-LEU-STAN** | Table 3 | LEUKEMIA | Standard_Consensus | 0.1729 ± 0.0668 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-LEU-LI_E** | Table 3 | LEUKEMIA | Li_et_al_2019 | 0.1144 ± 0.0476 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-LEU-DEC** | Table 3 | LEUKEMIA | DEC | 0.1481 ± 0.0630 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-LEU-FCAG** | Table 3 | LEUKEMIA | FCAG | 0.3234 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-LEU-FAST** | Table 3 | LEUKEMIA | FastMVC | 0.1817 ± 0.1644 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-LEU-ICC_** | Table 3 | LEUKEMIA | ICC_v1 | 0.1329 ± 0.0824 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-LEU-ICC_** | Table 3 | LEUKEMIA | ICC_v2 | 0.6799 ± 0.3634 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-MAD-K-ME** | Table 3 | MADELON | K-Means | 0.0343 ± 0.0215 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-MAD-WARD** | Table 3 | MADELON | Ward | 0.0077 ± 0.0034 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-MAD-SPEC** | Table 3 | MADELON | Spectral | 0.0381 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-MAD-FCM** | Table 3 | MADELON | FCM | 0.0183 ± 0.0148 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-MAD-STAN** | Table 3 | MADELON | Standard_Consensus | 0.0291 ± 0.0067 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-MAD-LI_E** | Table 3 | MADELON | Li_et_al_2019 | 0.0358 ± 0.0042 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-MAD-DEC** | Table 3 | MADELON | DEC | 0.0188 ± 0.0162 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-MAD-FCAG** | Table 3 | MADELON | FCAG | 0.0000 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-MAD-FAST** | Table 3 | MADELON | FastMVC | 0.0000 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-MAD-ICC_** | Table 3 | MADELON | ICC_v1 | 0.0307 ± 0.0068 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-MAD-ICC_** | Table 3 | MADELON | ICC_v2 | 0.0247 ± 0.0195 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-NEW-K-ME** | Table 3 | NEWSGROUPS20 | K-Means | 0.0413 ± 0.0534 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-NEW-WARD** | Table 3 | NEWSGROUPS20 | Ward | 0.1135 ± 0.0126 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-NEW-SPEC** | Table 3 | NEWSGROUPS20 | Spectral | 0.0001 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-NEW-FCM** | Table 3 | NEWSGROUPS20 | FCM | 0.0062 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-NEW-STAN** | Table 3 | NEWSGROUPS20 | Standard_Consensus | 0.1032 ± 0.0068 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-NEW-LI_E** | Table 3 | NEWSGROUPS20 | Li_et_al_2019 | 0.0769 ± 0.0124 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-NEW-DEC** | Table 3 | NEWSGROUPS20 | DEC | 0.0084 ± 0.0043 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-NEW-FCAG** | Table 3 | NEWSGROUPS20 | FCAG | 0.0451 ± 0.0105 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-NEW-FAST** | Table 3 | NEWSGROUPS20 | FastMVC | 0.0006 ± 0.0004 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-NEW-ICC_** | Table 3 | NEWSGROUPS20 | ICC_v1 | 0.0589 ± 0.0053 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-NEW-ICC_** | Table 3 | NEWSGROUPS20 | ICC_v2 | 0.0000 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-OVA-K-ME** | Table 3 | OVARIAN | K-Means | 0.0081 ± 0.0052 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-OVA-WARD** | Table 3 | OVARIAN | Ward | 0.0110 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-OVA-SPEC** | Table 3 | OVARIAN | Spectral | 0.0186 ± 0.0014 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-OVA-FCM** | Table 3 | OVARIAN | FCM | 0.0011 ± 0.0005 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-OVA-STAN** | Table 3 | OVARIAN | Standard_Consensus | 0.0095 ± 0.0023 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-OVA-LI_E** | Table 3 | OVARIAN | Li_et_al_2019 | 0.0079 ± 0.0040 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-OVA-DEC** | Table 3 | OVARIAN | DEC | 0.0050 ± 0.0062 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-OVA-FCAG** | Table 3 | OVARIAN | FCAG | -0.0115 ± 0.0077 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-OVA-FAST** | Table 3 | OVARIAN | FastMVC | -0.0115 ± 0.0074 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-OVA-ICC_** | Table 3 | OVARIAN | ICC_v1 | 0.0173 ± 0.0090 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-OVA-ICC_** | Table 3 | OVARIAN | ICC_v2 | 0.0523 ± 0.1608 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-PRO-K-ME** | Table 3 | PROSTATE | K-Means | 0.0465 ± 0.0042 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-PRO-WARD** | Table 3 | PROSTATE | Ward | 0.0264 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-PRO-SPEC** | Table 3 | PROSTATE | Spectral | -0.0034 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-PRO-FCM** | Table 3 | PROSTATE | FCM | 0.0483 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-PRO-STAN** | Table 3 | PROSTATE | Standard_Consensus | 0.0491 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-PRO-LI_E** | Table 3 | PROSTATE | Li_et_al_2019 | 0.0000 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-PRO-DEC** | Table 3 | PROSTATE | DEC | 0.0143 ± 0.0074 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-PRO-FCAG** | Table 3 | PROSTATE | FCAG | 0.0039 ± 0.0013 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-PRO-FAST** | Table 3 | PROSTATE | FastMVC | 0.0006 ± 0.0013 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-PRO-ICC_** | Table 3 | PROSTATE | ICC_v1 | 0.0181 ± 0.0191 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-PRO-ICC_** | Table 3 | PROSTATE | ICC_v2 | 0.0138 ± 0.0169 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SON-K-ME** | Table 3 | SONAR | K-Means | 0.0050 ± 0.0115 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SON-WARD** | Table 3 | SONAR | Ward | -0.0014 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SON-SPEC** | Table 3 | SONAR | Spectral | -0.0047 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SON-FCM** | Table 3 | SONAR | FCM | 0.0251 ± 0.0215 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SON-STAN** | Table 3 | SONAR | Standard_Consensus | -0.0001 ± 0.0022 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SON-LI_E** | Table 3 | SONAR | Li_et_al_2019 | 0.0113 ± 0.0031 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SON-DEC** | Table 3 | SONAR | DEC | 0.0161 ± 0.0235 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SON-FCAG** | Table 3 | SONAR | FCAG | -0.0045 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SON-FAST** | Table 3 | SONAR | FastMVC | -0.0030 ± 0.0029 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SON-ICC_** | Table 3 | SONAR | ICC_v1 | 0.0063 ± 0.0050 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SON-ICC_** | Table 3 | SONAR | ICC_v2 | 0.0048 ± 0.0129 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SRB-K-ME** | Table 3 | SRBCT | K-Means | 0.1405 ± 0.0589 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SRB-WARD** | Table 3 | SRBCT | Ward | 0.1091 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SRB-SPEC** | Table 3 | SRBCT | Spectral | 0.0802 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SRB-FCM** | Table 3 | SRBCT | FCM | 0.1022 ± 0.0199 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SRB-STAN** | Table 3 | SRBCT | Standard_Consensus | 0.0398 ± 0.0130 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SRB-LI_E** | Table 3 | SRBCT | Li_et_al_2019 | 0.0850 ± 0.0305 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SRB-DEC** | Table 3 | SRBCT | DEC | 0.0865 ± 0.0926 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SRB-FCAG** | Table 3 | SRBCT | FCAG | 0.0945 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SRB-FAST** | Table 3 | SRBCT | FastMVC | 0.1498 ± 0.0632 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SRB-ICC_** | Table 3 | SRBCT | ICC_v1 | 0.1101 ± 0.0349 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-SRB-ICC_** | Table 3 | SRBCT | ICC_v2 | 0.5378 ± 0.1095 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-YAL-K-ME** | Table 3 | YALE_B | K-Means | 0.0167 ± 0.0020 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-YAL-WARD** | Table 3 | YALE_B | Ward | 0.0485 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-YAL-SPEC** | Table 3 | YALE_B | Spectral | 0.0658 ± 0.0014 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-YAL-FCM** | Table 3 | YALE_B | FCM | -0.0010 ± 0.0005 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-YAL-STAN** | Table 3 | YALE_B | Standard_Consensus | 0.0159 ± 0.0010 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-YAL-LI_E** | Table 3 | YALE_B | Li_et_al_2019 | 0.0109 ± 0.0020 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-YAL-DEC** | Table 3 | YALE_B | DEC | 0.1308 ± 0.0146 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-YAL-FCAG** | Table 3 | YALE_B | FCAG | 0.0410 ± 0.0030 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-YAL-FAST** | Table 3 | YALE_B | FastMVC | 0.0404 ± 0.0035 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-YAL-ICC_** | Table 3 | YALE_B | ICC_v1 | 0.0072 ± 0.0027 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-YAL-ICC_** | Table 3 | YALE_B | ICC_v2 | 0.0453 ± 0.0074 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ZHE-K-ME** | Table 3 | ZHENG68K | K-Means | 0.4828 ± 0.1002 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ZHE-WARD** | Table 3 | ZHENG68K | Ward | 0.4953 ± 0.0000 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ZHE-SPEC** | Table 3 | ZHENG68K | Spectral | 0.4128 ± 0.0009 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ZHE-FCM** | Table 3 | ZHENG68K | FCM | 0.3701 ± 0.0514 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ZHE-STAN** | Table 3 | ZHENG68K | Standard_Consensus | 0.5615 ± 0.0104 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ZHE-LI_E** | Table 3 | ZHENG68K | Li_et_al_2019 | 0.4825 ± 0.0738 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ZHE-DEC** | Table 3 | ZHENG68K | DEC | 0.5199 ± 0.0716 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ZHE-FCAG** | Table 3 | ZHENG68K | FCAG | 0.3520 ± 0.1109 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ZHE-FAST** | Table 3 | ZHENG68K | FastMVC | 0.4587 ± 0.0657 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ZHE-ICC_** | Table 3 | ZHENG68K | ICC_v1 | 0.4843 ± 0.0663 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-T3-ZHE-ICC_** | Table 3 | ZHENG68K | ICC_v2 | 0.2400 ± 0.0775 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |

## 2. Table 3 Aggregates and Statistical Tests

| Claim ID | Source | Dataset / Regime | Metric / Statement | Paper Value | Producing Script | Reproduced Value | Delta | Status |
|---|---|---|---|---|---|---|---|---|
| **CLM-AGG-GM-K-ME** | Table 3 | Omnibus (13 Datasets) | Grand Mean ARI (K-Means) | 0.1186 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-AGG-GM-WARD** | Table 3 | Omnibus (13 Datasets) | Grand Mean ARI (Ward) | 0.1213 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-AGG-GM-SPEC** | Table 3 | Omnibus (13 Datasets) | Grand Mean ARI (Spectral) | 0.1050 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-AGG-GM-FCM** | Table 3 | Omnibus (13 Datasets) | Grand Mean ARI (FCM) | 0.0710 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-AGG-GM-STAN** | Table 3 | Omnibus (13 Datasets) | Grand Mean ARI (Standard_Consensus) | 0.1266 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-AGG-GM-LI_E** | Table 3 | Omnibus (13 Datasets) | Grand Mean ARI (Li_et_al_2019) | 0.1001 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-AGG-GM-DEC** | Table 3 | Omnibus (13 Datasets) | Grand Mean ARI (DEC) | 0.1309 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-AGG-GM-FCAG** | Table 3 | Omnibus (13 Datasets) | Grand Mean ARI (FCAG) | 0.1120 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-AGG-GM-FAST** | Table 3 | Omnibus (13 Datasets) | Grand Mean ARI (FastMVC) | 0.1107 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-AGG-GM-ICC_** | Table 3 | Omnibus (13 Datasets) | Grand Mean ARI (ICC_v1) | 0.1042 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-AGG-GM-ICC_** | Table 3 | Omnibus (13 Datasets) | Grand Mean ARI (ICC_v2) | 0.1599 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-AGG-RANK-ALL-ICCV2** | Table 3 / Fig 7 | All 13 Datasets | Mean Rank (ICC-v2) | 5.46 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-AGG-RANK-ALL-DEC** | Table 3 / Fig 7 | All 13 Datasets | Mean Rank (DEC) | 4.31 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-AGG-RANK-ALL-STDCONS** | Table 3 / Fig 7 | All 13 Datasets | Mean Rank (StdCons) | 5.08 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-AGG-RANK-ALL-KMEANS** | Table 3 / Fig 7 | All 13 Datasets | Mean Rank (K-Means) | 5.31 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-AGG-RANK-SUB-ICCV2-T3** | Table 3 | D/N > 20 Subgroup | Mean Rank (ICC-v2 Table 3) | 2.33 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-AGG-RANK-SUB-ICCV2-TXT** | Sec 5.4 / Fig 7 | D/N > 20 Subgroup | Mean Rank (ICC-v2 Text Claim) | 1.50 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-AGG-FRIEDMAN-P** | Sec 5.4 | All 13 Datasets | Friedman omnibus test p-value | 0.33 | experiments/exp3_real_world_benchmarks/src/run_exp3_4_statistical_significance.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-AGG-NEMENYI-CD** | Sec 5.4 | All 13 Datasets | Nemenyi Critical Difference (CD) | 2.62 | experiments/audit_controls/src/plot_audit_figures.py | PENDING | - | PENDING_REPRODUCTION |

## 3. Biomedical Genomics Discrepancies (Leukemia, SRBCT, Ovarian)

| Claim ID | Source | Dataset / Regime | Metric / Statement | Paper Value | Producing Script | Reproduced Value | Delta | Status |
|---|---|---|---|---|---|---|---|---|
| **CLM-BIO-LEUK-S52** | Sec 5.2 | Leukemia (N=72, D=7129) | ICC-v2 ARI (Exp 2 Ablation V5) | 0.846 +/- 0.154 | experiments/exp2_ablation/src/run_ablation_sweep.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-BIO-LEUK-S54** | Sec 5.4 / Table 3 | Leukemia (N=72, D=7129) | ICC-v2 ARI (Exp 3.1 Benchmark) | 0.680 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-BIO-LEUK-FIG6** | Fig 6 (Legacy Heatmap) | Leukemia (N=72, D=7129) | ICC-v2 ARI in 21-dataset audit | 0.798 (Adapt) / 0.323 (15%) | experiments/audit_controls/src/e1_extended_benchmarks.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-BIO-SRBCT-S52** | Sec 5.2 | SRBCT (N=83, D=2308) | ICC-v2 ARI (Exp 2 Ablation V5) | 0.681 +/- 0.037 | experiments/exp2_ablation/src/run_ablation_sweep.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-BIO-SRBCT-S54** | Sec 5.4 / Table 3 | SRBCT (N=83, D=2308) | ICC-v2 ARI (Exp 3.1 Benchmark) | 0.538 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-BIO-SRBCT-FIG6** | Fig 6 (Legacy Heatmap) | SRBCT (N=83, D=2308) | ICC-v2 ARI in 21-dataset audit | 0.578 (Adapt) / 0.607 (15%) | experiments/audit_controls/src/e1_extended_benchmarks.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-BIO-OVAR-ARI** | Sec 5.4 / Table 3 | Ovarian (N=253, D=15154) | ICC-v2 ARI | 0.052 | experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-BIO-OVAR-SPEED** | Sec 5.4 | Ovarian (N=253, D=15154) | Consensus extraction speedup | 17.0x (3.41s vs 57.98s) | experiments/exp3_real_world_benchmarks/src/run_benchmark.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-BIO-LEUK-V1** | Sec 5.2 | Leukemia | V1 (VSSG + KMeans) ARI | 0.019 +/- 0.078 | experiments/exp2_ablation/src/run_ablation_sweep.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-BIO-LEUK-V2** | Sec 5.2 | Leukemia | V2 (VSSG + StdCons) ARI | 0.032 +/- 0.136 | experiments/exp2_ablation/src/run_ablation_sweep.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-BIO-SRBCT-V1** | Sec 5.2 | SRBCT | V1 (VSSG + KMeans) ARI | 0.176 +/- 0.191 | experiments/exp2_ablation/src/run_ablation_sweep.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-BIO-SRBCT-V2** | Sec 5.2 | SRBCT | V2 (VSSG + StdCons) ARI | 0.361 +/- 0.191 | experiments/exp2_ablation/src/run_ablation_sweep.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-BIO-LEUK-VSSG-COUNT** | Sec 5.2 | Leukemia (D=7129) | VSSG candidate feature count | 1,522 features | experiments/exp2_ablation/src/ablation_engine.py | PENDING | - | PENDING_REPRODUCTION |

## 4. Synthetic Ablation Study (Exp 2 & Exp 2.1)

| Claim ID | Source | Dataset / Regime | Metric / Statement | Paper Value | Producing Script | Reproduced Value | Delta | Status |
|---|---|---|---|---|---|---|---|---|
| **CLM-ABL-D50-V0** | Sec 5.2 / Fig 4a | Synthetic Dnoise=50 | V0 (Std Consensus) ARI | 0.359 | experiments/exp2_ablation/src/run_ablation_sweep.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-ABL-D50-V3** | Sec 5.2 / Fig 4a | Synthetic Dnoise=50 | V3 (Anchors Only) ARI | 0.411 | experiments/exp2_ablation/src/run_ablation_sweep.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-ABL-D50-VSSG** | Sec 5.2 / Fig 4a | Synthetic Dnoise=50 | VSSG Variants (V1, V2, V4, V5) ARI | >= 0.94 | experiments/exp2_ablation/src/run_ablation_sweep.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-ABL-D200-BASE** | Sec 5.2 / Fig 4a | Synthetic Dnoise >= 200 | Non-VSSG Baselines (V0, V3) ARI | <= 0.006 | experiments/exp2_ablation/src/run_ablation_sweep.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-ABL-D50-LIFT** | Sec 5.2 / Fig 4a | Synthetic Dnoise=50 | Lift of V5 over V0 | +0.640 ARI | experiments/exp2_ablation/src/run_ablation_sweep.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-VSSG-MADELON-PRAUC** | Sec 5.3 / Fig 5a | Madelon (D=500, Dsig=20) | VSSG PR-AUC vs Uncalibrated | 0.892 vs 0.354 | experiments/exp2_ablation/src/vssg_interpretability.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-VSSG-MADELON-REC50** | Sec 5.3 / Fig 5a | Madelon (D=500, Dsig=20) | Recall@50 | 0.95 | experiments/exp2_ablation/src/vssg_interpretability.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-VSSG-SYN-PRAUC** | Sec 5.3 / Fig 5b | Synthetic D=10,000 | VSSG PR-AUC | 0.974 | experiments/exp2_ablation/src/vssg_interpretability.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-VSSG-SYN-REC50** | Sec 5.3 / Fig 5b | Synthetic D=10,000 | Recall@50 | > 0.85 | experiments/exp2_ablation/src/vssg_interpretability.py | PENDING | - | PENDING_REPRODUCTION |

## 5. Inductive Generalization (Exp 1)

| Claim ID | Source | Dataset / Regime | Metric / Statement | Paper Value | Producing Script | Reproduced Value | Delta | Status |
|---|---|---|---|---|---|---|---|---|
| **CLM-GEN-PSEUDO-ACC** | Sec 5.1 / Fig 3b | Synthetic D >= 1,000 | Pseudo-label accuracy gain | 33.3% vs 28.8% | experiments/exp1_generalization/src/exp1_pseudolabel_generalization.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-GEN-SVM-ADV** | Sec 5.1 / Fig 3b | Synthetic D >= 1,000 | SVM Core vs Full Advantage | +4.5% points | experiments/exp1_generalization/src/exp1_pseudolabel_generalization.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-GEN-RF-ADV** | Sec 5.1 / Fig 3b | Synthetic D >= 1,000 | RF Core vs Full Advantage | +3.8% points | experiments/exp1_generalization/src/exp1_pseudolabel_generalization.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-GEN-MLP-ADV** | Sec 5.1 / Fig 3b | Synthetic D >= 1,000 | MLP Core vs Full Advantage | +4.2% points | experiments/exp1_generalization/src/exp1_pseudolabel_generalization.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-GEN-KNN-RESULT** | Sec 5.1 | Synthetic D >= 1,000 | KNN Generalization Result | Present in text / audit | experiments/exp1_generalization/src/exp1_pseudolabel_generalization.py | PENDING | - | PENDING_REPRODUCTION |

## 6. Scalability, Memory & Anchor Fidelity (Exp 4 & Exp 4.3)

| Claim ID | Source | Dataset / Regime | Metric / Statement | Paper Value | Producing Script | Reproduced Value | Delta | Status |
|---|---|---|---|---|---|---|---|---|
| **CLM-SCA-MEM-8K** | Sec 5.5 / Fig 9a | Synthetic N=8,000 | Peak RAM reduction (Exact vs Reduced) | 1,709.6 MB vs 1,040.5 MB (39.1%) | experiments/exp4_scalability_and_sensitivity/src/scaling_benchmark.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-SCA-MEM-10K** | Sec 5.5 / Fig 8d | Synthetic N=10,000 | Auxiliary memory reduction | 1,529.8 MB vs 45.8 MB (97.0%) | experiments/exp4_scalability_and_sensitivity/src/anchor_fidelity_benchmark.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-SCA-TIME-10K** | Sec 5.5 / Fig 8c | Synthetic N=10,000 | Runtime speedup (Exact vs Reduced) | 29.91s vs 1.34s (22.4x) | experiments/exp4_scalability_and_sensitivity/src/anchor_fidelity_benchmark.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-SCA-VSSG-SPEED** | Sec 5.5 / Fig 9b | Synthetic D=20,000 | VSSG Gating Speedup | 1.523s -> 0.964s (36.7%) | experiments/exp4_scalability_and_sensitivity/src/scaling_benchmark.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-FID-GAP-BOUND** | Sec 5.5 / Fig 8a | Synthetic N in [200, 10k] | Anchor approximation discrepancy | |dARI| <= 0.05 | experiments/exp4_scalability_and_sensitivity/src/anchor_fidelity_benchmark.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-FID-N5K-REDUCED** | Sec 5.5 / Fig 8b | Synthetic N=5,000 | Reduced vs Exact ARI | Reduced 0.618 vs Exact 0.583 | experiments/exp4_scalability_and_sensitivity/src/anchor_fidelity_benchmark.py | PENDING | - | PENDING_REPRODUCTION |

## 7. Extreme Scale, Missing Data & Misspecification (Exp 5 & Exp 3.5)

| Claim ID | Source | Dataset / Regime | Metric / Statement | Paper Value | Producing Script | Reproduced Value | Delta | Status |
|---|---|---|---|---|---|---|---|---|
| **CLM-EXT-N1M-TIME** | Sec 5.6 / Fig 10a | Synthetic N=1,000,000 | ICC-v2 Execution Time | 55.6s | experiments/exp5_extreme_scale/src/extreme_scale_benchmark.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-EXT-N1M-RAM** | Sec 5.6 / Fig 10b | Synthetic N=1,000,000 | ICC-v2 Peak RAM | 3.05 GB | experiments/exp5_extreme_scale/src/extreme_scale_benchmark.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-EXT-N1M-ARI** | Sec 5.6 / Fig 10d | Synthetic N=1,000,000 | ICC-v2 vs MiniBatchKMeans ARI | 0.382 vs 0.150 | experiments/exp5_extreme_scale/src/extreme_scale_benchmark.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-EXT-D100K-TIME** | Sec 5.6 / Fig 10c | Synthetic N=1,000, D=100k | ICC-v2 Execution Time | 8.28s | experiments/exp5_extreme_scale/src/extreme_scale_benchmark.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-MISS-SRBCT-RHO5** | Sec 5.6 / Fig 11a | SRBCT (Missing rho=0.5) | ICC-v2 ARI vs baselines | ARI > 0.40 (all baselines < 0.10) | experiments/exp3_real_world_benchmarks/src/missing_data_experiment.py | PENDING | - | PENDING_REPRODUCTION |
| **CLM-KMISS-SYN-K9** | Sec 5.6 | Synthetic (Ktrue=3, K=9) | Single KMeans vs ICC-v2 ARI | KMeans drops to 0.23, ICC-v2 >= 0.72 | experiments/exp4_scalability_and_sensitivity/src/k_misspecification_sweep.py | PENDING | - | PENDING_REPRODUCTION |
