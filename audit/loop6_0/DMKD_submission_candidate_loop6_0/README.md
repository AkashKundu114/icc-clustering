# DMKD submission candidate — Loop 6.0

This is an evidence-bounded revised candidate, not a final or submission-ready package. It narrows the paper to the six-cohort saved-output reconstruction and removes claims from unaudited GAC, causal, clinical, theory, scalability and benchmark workstreams. It does not replace the ignored local canonical manuscript.

`main.tex` is a standalone article-class source, not yet the Springer Nature `sn-jnl` submission class. Static validation passed; `pdflatex` was unavailable, so there is no compiled PDF or visual QA. The aggregate tables can be regenerated with `python build_candidate_tables.py` from the repository root; that reads `audit/loop5_9/statistics/cell_reconstruction.csv` and performs no fits. `python validate_candidate.py` checks static structure and output linkage.

The underlying partitions and records are not in the public clone, so this candidate's calculations are not Tier 2 reproducible publicly. The exact canonical source remains at its baseline SHA in the Loop 6.0 record; this candidate has a separate SHA in the manifest. `candidate_manifest.csv` lists all package files other than itself.
