# Claim -> evidence
| Claim (README) | Evidence | Status |
|---|---|---|
| ARI 0.1718, Rank #1, p<0.05 | CSV: mean ARI 0.1599; mean rank 5.46/11; Holm n.s.; Friedman p=0.33 | CONTRADICTED |
| +4.5% accuracy (Exp1, D>=1000) | CORE-ALL = -0.010; accuracies ~chance; 4 classifiers not 5 | CONTRADICTED |
| VSSG maintains recovery at D_noise>=5000 | Ablation ARI~0 for all variants at D>=200; only feature P/R exists | UNSUPPORTED |
| +34% core certification (D=0) | 0.549->0.736 (relative), D_noise=0 only | SUPPORTED (narrow) |
| >80% retention at 40% MCAR | 3 datasets; 38% at rho=0.3; grid lacks 0.4 | CONTRADICTED |
| O(NL) memory / exact spectral | dense NxN for N<=2000; embedding lacks D_L^-1/2; fidelity test tiny | UNSUPPORTED |
| Linear time to N=1e6 | different code path for N>2000; exp5 not re-run | UNVERIFIED |
| FastMVC baseline (TKDE 2023) | docstring says STUB; closest real paper is FastMICE (multi-view) | MISLABELED |
