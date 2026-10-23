# GitHub Repository Settings & Metadata Recommendations

**Repository:** `AkashKundu114/icc-clustering`  
**Canonical Manuscript Title:** "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Version:** `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*  
**Auditor:** Senior Research Governance Auditor

---

## 1. Repository Metadata
- **Description:**  
  `Official implementation of "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination" (ICC-v2 & CICC).`
- **Website Link:**  
  `https://github.com/AkashKundu114/icc-clustering` (and permanent Zenodo DOI upon archiving)
- **Repository Topics:**  
  `clustering`, `consensus-clustering`, `cluster-ensemble`, `high-dimensional-data`, `bipartite-graph`, `anchor-graph`, `spectral-clustering`, `conformal-prediction`, `bioinformatics`, `machine-learning`, `python`

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
Once approved by user, run:
```bash
gh repo edit AkashKundu114/icc-clustering \
  --description "Official implementation of 'When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination' (ICC-v2 & CICC)." \
  --add-topic "clustering,consensus-clustering,cluster-ensemble,high-dimensional-data,bipartite-graph,anchor-graph,spectral-clustering,conformal-prediction,bioinformatics,machine-learning,python" \
  --enable-squash-merge \
  --delete-branch-on-merge
```
