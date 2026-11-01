# Reproducibility & Acquisition Verification Report

**Date:** November 1, 2026  
**Environment:** Python 3.14.6, Windows 10/11, PowerShell, curl 8.22.0  
**Repository Branch:** `research/cohort-discovery` (commit synced with `main`)  

---

## 1. Verified Software & API Endpoints

- **NCBI E-utilities API:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils`
  - ESearch db=gds
  - ESummary db=gds
  - ESummary db=pubmed
- **NCBI GEO FTP Repository:** `https://ftp.ncbi.nlm.nih.gov/geo/series/`
- **EMBL-EBI BioStudies API:** `https://www.ebi.ac.uk/biostudies/api/v1/studies/`
- **NCI GDC API:** `https://api.gdc.cancer.gov/data`

---

## 2. Reproduction Commands

To reproduce the candidate discovery run:
```powershell
# 1. Run systematic discovery across disease families
python tools/discover_biological_cohorts.py discover --retmax 50 --email research@icc-clustering.org --delay 0.4

# 2. Run unit tests verifying downloader guards, path safety, and label ontologies
python -m pytest tests/test_cohort_discovery.py -v

# 3. Build comprehensive audit deliverables
python scripts/build_cohort_discovery_audit.py
python scripts/build_audit_markdown_reports.py

# 4. Download reviewed candidate matrix with SHA-256 verification
python tools/discover_biological_cohorts.py download `
  --manifest research_audit/cohort_discovery/test_download_manifest.csv `
  --report research_audit/cohort_discovery/download_manifest.csv `
  --timeout 90
```

---

## 3. Cryptographic Hashes of Downloaded Benchmark Files

| Cohort Accession | File Name | Size (Bytes) | SHA-256 Digest | Status |
| :--- | :--- | :---: | :--- | :--- |
| **GSE42568** | `GSE42568_series_matrix.txt.gz` | $22{,}565{,}943$ | `43b93f72f1d81838dcd2a5b6ccc3bc1875e46230dad0d7346236773a99e32b76` | **VERIFIED** |

---

## 4. Policy on Raw Data Retention

In accordance with repository `.gitignore` conventions:
- Large binary files (`*.txt.gz`, `*.npz`) remain in `data/raw/` and are not tracked in Git.
- Provenance manifests (`download_manifest.csv`, `download_manifest_reviewed.csv`) are committed to Git to ensure 100% deterministic re-acquisition.
