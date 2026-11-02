# Loop 6.0 remediation and submission candidate audit

This package records the baseline, independent saved-output reconstruction, evidence-bounded revised candidate, provenance work, benchmark reanalysis, reproducibility/rights checks, independent review, and remaining blockers. The verdict is **HOLD**. The candidate in `DMKD_submission_candidate_loop6_0/` is not a final or submission-ready Springer package.

The canonical local `paper/manuscript/main.tex` remains unchanged at its Loop 5.9 SHA and is not tracked in the public repository. No original clustering fits were rerun, no historical results were overwritten, and no third-party data were bundled.

Reconstruction scripts require local FYP evidence at `D:\Final Year Project`; they cannot run from a clean public clone. Public Tier 1 aggregate arithmetic passes, Tier 2 inputs are absent, and Tier 3 is not run. See `FINAL_LOOP6_0_REPORT.md` for the exact findings and next actions.

All Loop 6.0 files are inventoried in `loop6_0_artifact_manifest.csv` with dynamically computed SHA-256; `SHA256SUMS` verifies the manifest and files (the manifest excludes itself and `SHA256SUMS`; the checksum file excludes itself because self-hashing is not possible).
