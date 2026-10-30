# ICC Documentation Index

Welcome to the documentation for **Inductive Consensus Clustering (`icc`)**. This directory contains comprehensive technical specifications, empirical replication protocols, theoretical proofs, dataset audits, and computational environment profiles.

---

## Documentation Roadmap

| Document | Primary Audience | Description |
| :--- | :--- | :--- |
| **[REPRODUCIBILITY.md](REPRODUCIBILITY.md)** | Peer Reviewers, Evaluators | Push-button guide mapping every paper Table (Table 1--16) and Figure (Figure 1--9) to exact CLI commands, underlying data files in `results/passF`, runtime expectations, and determinism protocols. |
| **[DATA.md](DATA.md)** | Researchers, Data Scientists | Comprehensive audit of all 13 benchmark datasets: sample size ($N$), dimensionality ($D$), cluster count ($K$), $D/N$ ratio, data sources, verified open-access licenses, and cryptographic SHA-256 signatures for cached local arrays. |
| **[api.md](api.md)** | Developers, ML Engineers | Full Python API reference for the scikit-learn-compatible `ICC` estimator, feature gating (`BGSS`), bipartite anchor graph construction, inductive out-of-sample prediction, and conformal uncertainty quantification (`cicc`). |
| **[THEORETICAL_FOUNDATIONS.md](THEORETICAL_FOUNDATIONS.md)** | Theoretical ML Researchers | Rigorous mathematical foundations, formal propositions, and proofs: Bipartite Transfer-Cut Laplacian spectra, finite-sample Sarle's Bimodality Coefficient null bounds, and closed-form inductive centroid projections. |
| **[ENV.md](ENV.md)** | Systems Engineers, Reviewers | Complete computational environment verification: host operating system, CPU architecture, GPU specifications, memory constraints, and single-thread BLAS determinism settings. |

---

## Quick Navigation

- **Need to verify paper claims quickly?**  
  Jump to [REPRODUCIBILITY.md#1-executive-push-button-verification--1-minute](REPRODUCIBILITY.md#1-executive-push-button-verification--1-minute).
- **Need to understand the mathematical derivation of Transfer-Cut?**  
  See [THEORETICAL_FOUNDATIONS.md](THEORETICAL_FOUNDATIONS.md).
- **Need code snippets and estimator parameter documentation?**  
  See [api.md](api.md).
- **Need dataset download URLs and licensing information?**  
  See [DATA.md](DATA.md).
