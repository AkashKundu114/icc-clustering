# Red flags
| ID | Sev | Cat | Location | Finding |
|---|---|---|---|---|
| R1 | CRIT | Exp validity | README:159 vs exp3 CSVs | headline claims contradicted |
| R2 | CRIT | Algorithm | consensus_v2.py step 2 | 15% floor; demo ARI ~0 |
| R3 | HIGH | Math | VSSG | marginal-BC assumption; sparse/heavy-tail failure; no theorem |
| R4 | HIGH | Complexity | consensus_v2.py step 4 | dense NxN <=2000; two branches |
| R5 | HIGH | Math | step 5 | embedding not shown equivalent to spectral |
| R6 | HIGH | Controls | exp2 | no BC-filter+KMeans control; ablation collapses |
| R7 | HIGH | Baselines | baselines/anchor.py | FastMVC stub; FCAG authors wrong |
| R8 | HIGH | Exp1 | exp1 CSV | +4.5% not reproduced |
| R9 | MED | Exp5/3.5 | missing-data | 3 datasets, claim contradicted |
| R10 | MED | Code | beta | dead hyperparameter |
| R11 | MED | Repro | tests | write to tracked results; 5 network tests; count mismatch |
| R12 | MED | Repro | demo.py | hard-coded 'Key Finding' (fixed on branch) |
| R13 | MED | Stats | exp3_4 | uncorrected raw-p reporting; n=6 subgroup cannot pass Holm |
| R14 | LOW | Docs | docstring | BC formula text differs from code |

## Status after A3/A4 (branch)
R4 PARTIAL: branches parameterized and shown to differ; not unified. R5 PARTIAL: opt-in transfer-cut embedding; equivalence at clustering level not established. R7 PARTIAL: docstrings/citations fixed, `stub: true` in configs; no faithful FastMICE/FCAG yet. R10 FIXED (deprecation + tests). Excluding the stub, Exp3 conclusions unchanged: ICC-v2 mean rank 5.15/10 (DEC 4.15), min raw p 0.244, Friedman p 0.448.

## E5 additions
R8 (Exp1 +4.5%) now VERIFIED non-reproducible by rerun. R9 (missing-data) VERIFIED non-reproducible by rerun. New R15 MED: Exp1 runner overwrites a tracked CSV irrespective of output_csv (now fixed in repository). New R16 MED: ground-truth Exp1 shows ICC-v1 core selection below full-data training at every D_noise>0.

## E6 additions
R4 refined: dense O(N^2) path VERIFIED (61 MB at N=2000 vs 6 MB at N=2001); scalable path near-linear to N=32,000 (D=200). Open: quality parity between branches; 1e6 / D=1e5 claims.
