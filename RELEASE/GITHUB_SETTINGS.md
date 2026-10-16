# GitHub Repository Settings & Metadata Recommendations

**Repository:** `AkashKundu114/icc-clustering`  
**Auditor:** Subagent G (Phase E)  

---

## 1. Repository Metadata
- **Description:**  
  `Official implementation of Inductive Consensus Clustering (ICC-v2): geometry-calibrated ensemble distillation for high-dimensional noise regimes.`
- **Website Link:**  
  `https://github.com/AkashKundu114/icc-clustering` (or Zenodo DOI once reserved)
- **Repository Topics:**  
  `clustering`, `consensus-clustering`, `cluster-ensemble`, `high-dimensional-data`, `bipartite-graph`, `anchor-graph`, `spectral-clustering`, `bioinformatics`, `machine-learning`, `python`

---

## 2. Recommended Branch Protection Rules (`main`)
- Require pull request before merging (Require approvals: 1).
- Require status checks to pass before merging:
  - `Test Python 3.10 on ubuntu-latest`
  - `Test Python 3.11 on ubuntu-latest`
  - `Test Python 3.12 on ubuntu-latest`
  - `Test Python 3.11 on windows-latest`
- Require branches to be up to date before merging.
- Require conversation resolution before merging.
- Do not allow force pushes or deletions.

---

## 3. Merge Strategies
- Allow squash merging (Recommended default: keeps history linear and clean).
- Automatically delete head branches upon merge.

---

## 4. Security & Vulnerability Alerts
- Dependabot alerts: **Enabled**
- Dependabot security updates: **Enabled**
- Secret scanning alerts: **Enabled**
- Code scanning (CodeQL): **Recommended**

---

## 5. Applying Settings via GitHub CLI (`gh`)
Once approved by user (Gate 3), run:
```bash
gh repo edit AkashKundu114/icc-clustering \
  --description "Official implementation of Inductive Consensus Clustering (ICC-v2): geometry-calibrated ensemble distillation for high-dimensional noise regimes." \
  --add-topic "clustering,consensus-clustering,cluster-ensemble,high-dimensional-data,bipartite-graph,anchor-graph,spectral-clustering,bioinformatics,machine-learning,python" \
  --enable-squash-merge \
  --delete-branch-on-merge
```
