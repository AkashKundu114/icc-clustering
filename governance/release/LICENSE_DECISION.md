# License Decision and Recommendations (Phase E)

**Date:** 2026-10-17  
**Repository:** `AkashKundu114/icc-clustering`  

---

## 1. Codebase License Options (3-Line Trade-offs)

### Option A: MIT License (Recommended & Current Default)
- **Trade-off 1 (Permissiveness):** Highly permissive; maximizes academic adoption, citation, and industry benchmarking without restrictive viral obligations.
- **Trade-off 2 (Patent Protection):** Does not include an explicit patent grant clause unlike Apache-2.0, though standard in academic ML repos (scikit-learn, PyTorch).
- **Trade-off 3 (Ecosystem Match):** Exactly aligns with existing `LICENSE`, `pyproject.toml`, and `CITATION.cff` already committed in the project.

### Option B: Apache License 2.0
- **Trade-off 1 (Patent Clarity):** Provides explicit, irrevocable patent grants from contributors and automatic patent litigation retaliation clauses.
- **Trade-off 2 (Attribution Rigor):** Requires explicit state changes to be documented in modified source files and preservation of NOTICE files.
- **Trade-off 3 (Complexity):** Slightly more formal for quick academic forks; requires updating existing metadata headers and license text.

---

## 2. Research Data & Manuscript Text Licensing
- **Results & Data Outputs (`results/`):** Recommended Creative Commons Attribution 4.0 International (`CC-BY-4.0`) so scientific benchmarks can be cited and quoted freely.
- **Paper Manuscript (`paper/`, `springer_manuscript/`):** Retained under journal copyright agreement upon formal acceptance, with preprint sharing permitted per publisher policies.
- **Third-Party Datasets:** Datasets remain under their respective upstream licenses (e.g. OpenML Public Domain, UCI Open Data, 10x Genomics open access).

---

## 3. Approval Recommendation
**Keep MIT License for software code** as currently defined in `LICENSE` file.
*(Approval Gate 1 requirement satisfied; awaiting user confirmation).*
