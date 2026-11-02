# Security, External Input Handling, and Data Privacy Audit Report

**Repository:** `d:\icc-clustering` (`icc-clustering`)  
**Auditor:** Security and Data Handling Specialist  
**Date:** November 1, 2026  
**Target Package Versions:** ICC v2.2.0 / CICC v1.0.0  
**Scope:** Core library (`src/icc/`, `src/cicc/`), Dataset pipelines (`src/icc/datasets/`, `src/icc/data/`), CLI scripts (`scripts/`), Web demo (`examples/web_demo/`), Configurations (`configs/`, `data/`), Tests & Documentation.

---

## 1. Executive Summary

A comprehensive security, input validation, and data privacy audit was performed on the `icc-clustering` codebase. The repository demonstrates disciplined hygiene in secret isolation (zero hardcoded secrets or author paths detected, robust `.gitignore` rules) and clinical data privacy (purely numerical/categorical benchmark matrices with zero Protected Health Information).

However, **critical and high-priority vulnerabilities** were identified in remote data acquisition and the web demo interface:
1. **Arbitrary File Overwrite (TarSlip)** in `tarfile.extractall` without member filtering when unpacking scRNA-seq archives.
2. **Disabling of SSL/TLS certificate verification** (`ssl._create_unverified_context()`) across remote dataset fetchers.
3. **Missing cryptographic checksum validation** during dataset acquisition despite documentation asserting SHA-256 enforcement.
4. **Permissive CORS misconfiguration** (`allow_origins=["*"]` with `allow_credentials=True`) in the FastAPI web demo backend.
5. **Denial of Service (DoS) risks** via unbounded clustering parameters (`n_anchors`, `n_clusters`) executing synchronous heavy CPU workloads.

A total of **12 findings** were documented (1 High, 4 Medium, 4 Low, 3 Informational/Verified Positive).

---

## 2. Findings Taxonomy and Summary Table

| Finding ID | Title | Severity | CWE | File / Line Reference | Fact vs. Inference | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AUD-SEC-001** | Arbitrary File Overwrite via Unfiltered `tarfile.extractall` (TarSlip) | **High** | CWE-22 | `src/icc/datasets/scrnaseq.py:160-161` | Verified Fact | Open |
| **AUD-SEC-002** | Disabling of SSL/TLS Certificate Validation in Remote Dataset Downloaders | **Medium** | CWE-295 | `src/icc/datasets/image.py:27`<br>`src/icc/datasets/spectral.py:27`<br>`src/icc/datasets/scrnaseq.py:154` | Verified Fact | Open |
| **AUD-SEC-003** | Missing SHA-256 Checksum Verification During Dataset Ingestion (Documentation Discrepancy) | **Medium** | CWE-353 | `scripts/fetch_data.py:26-30`<br>`data/README.md:44`<br>`configs/datasets.yaml` | Verified Fact | Open |
| **AUD-SEC-004** | Insecure CORS Configuration (`allow_origins=["*"]` with `allow_credentials=True`) | **Medium** | CWE-346 / CWE-942 | `examples/web_demo/app/main.py:22-28` | Verified Fact | Open |
| **AUD-SEC-005** | Denial of Service (DoS) via Unbounded Clustering Hyperparameters & Blocking Execution | **Medium** | CWE-400 / CWE-770 | `examples/web_demo/app/main.py:119-152` | Verified Fact | Open |
| **AUD-SEC-006** | Insecure Cleartext HTTP Protocol Endpoints for Benchmark Dataset Downloads | **Low** | CWE-319 | `configs/datasets.yaml:249`<br>`src/icc/datasets/image.py:70`<br>`data/registry.yaml:227,247` | Verified Fact | Open |
| **AUD-SEC-007** | Predictable Temporary File Naming in Cohort Retrieval Pipeline | **Low** | CWE-377 / CWE-378 | `src/icc/data/cohorts.py:200` | Verified Fact | Open |
| **AUD-SEC-008** | Unclosed File Descriptor Handles in `np.load` Operations | **Low** | CWE-775 | `src/icc/datasets/genomics.py:126`<br>`examples/web_demo/app/main.py:37,80` | Verified Fact | Open |
| **AUD-SEC-009** | Missing Subresource Integrity (SRI) on Third-Party Web Assets (CDN Scripts/CSS) | **Low** | CWE-353 | `examples/web_demo/app/main.py:285-287` | Verified Fact | Open |
| **AUD-SEC-010** | Undeclared Web Demo Dependencies & Permissive Dependency Version Bounds | **Informational** | CWE-1104 | `pyproject.toml:28-76`<br>`requirements.txt:14-37` | Verified Fact | Open |
| **AUD-SEC-011** | Clinical Data Privacy & HIPAA Compliance Verification | **Informational** | N/A (Compliance) | `data/cache/*.npz`<br>`examples/clinical_cancer_subtyping.py`<br>`examples/realtime_patient_projection.py` | Verified Fact | Accepted |
| **AUD-SEC-012** | Secrets, Credentials, and Author Environment Isolation Audit | **Informational** | N/A (Clean) | Entire repository & Git commit history | Verified Fact | Resolved |

---

## 3. Detailed Technical Findings

### AUD-SEC-001: Arbitrary File Overwrite via Unfiltered `tarfile.extractall` (TarSlip)
- **Severity:** High
- **CWE:** CWE-22 (Improper Limitation of a Pathname to a Restricted Directory / Path Traversal)
- **Affected File:** `src/icc/datasets/scrnaseq.py:160-161`
- **Fact vs. Inference:** [Verified Fact]. Directly verified by inspecting `scrnaseq.py` and running static vulnerability analysis.
- **Vulnerability Mechanics:**
  In `load_zheng68k(mode="full")`, the code downloads a compressed `.tar.gz` from 10x Genomics and unpacks it:
  ```python
  160: with tarfile.open(tar_path, "r:gz") as tar:
  161:     tar.extractall(path=r_dir)
  ```
  `tarfile.extractall()` is invoked without member inspection or extraction filters. If a downloaded archive contains files with directory traversal paths (e.g. `../../etc/cron.d/malicious` or Windows drive paths `C:\...`), `tarfile` will extract members outside the target directory `r_dir`. When combined with AUD-SEC-002 (unverified SSL context), an active network attacker could deliver a weaponized archive resulting in arbitrary file overwrites or code execution.
- **Actionable Remediation Guidance:**
  Use Python 3.12+ / 3.14 PEP 706 `filter="data"` or an explicit path validation helper:
  ```python
  with tarfile.open(tar_path, "r:gz") as tar:
      if hasattr(tarfile, "data_filter"):
          tar.extractall(path=r_dir, filter="data")
      else:
          for member in tar.getmembers():
              member_path = (Path(r_dir) / member.name).resolve()
              if not member_path.is_relative_to(Path(r_dir).resolve()):
                  raise SecurityError(f"Attempted path traversal in tar archive: {member.name}")
          tar.extractall(path=r_dir)
  ```

---

### AUD-SEC-002: Disabling of SSL/TLS Certificate Validation in Remote Dataset Downloaders
- **Severity:** Medium
- **CWE:** CWE-295 (Improper Certificate Validation)
- **Affected Files:**
  - `src/icc/datasets/image.py:27`
  - `src/icc/datasets/spectral.py:27`
  - `src/icc/datasets/scrnaseq.py:154`
- **Fact vs. Inference:** [Verified Fact].
- **Vulnerability Mechanics:**
  The custom `_download_file` utility initializes an unverified SSL context:
  ```python
  ctx = ssl._create_unverified_context()
  with urllib.request.urlopen(req, timeout=45, context=ctx) as response, ...
  ```
  This disables certificate chain verification and hostname matching. Any network intermediary (e.g. public Wi-Fi, compromised DNS, or corporate proxy) can perform a TLS interception attack, injecting poisoned dataset matrices or corrupt binaries without warning.
- **Actionable Remediation Guidance:**
  Use default certificate validation via `ssl.create_default_context()`, or leverage the hardened standard library / `requests` session:
  ```python
  ctx = ssl.create_default_context()
  ```

---

### AUD-SEC-003: Missing SHA-256 Checksum Verification During Dataset Ingestion
- **Severity:** Medium
- **CWE:** CWE-353 (Missing Support for Integrity Check)
- **Affected Files:**
  - `scripts/fetch_data.py:26-30`
  - `data/README.md:44`
  - `configs/datasets.yaml`
  - `data/registry.yaml`
- **Fact vs. Inference:** [Verified Fact].
  - `data/README.md` line 44 states: *"This script validates SHA-256 checksums before caching tensors into `data/cache/`."*
  - Static code inspection of `scripts/fetch_data.py` reveals that it only asserts tensor shapes (`X.shape[0] == d.expected_N` and `X.shape[1] == d.expected_D`).
  - Neither `configs/datasets.yaml` nor `data/registry.yaml` includes expected SHA-256 hashes for the raw files or `.npz` caches.
- **Actionable Remediation Guidance:**
  1. Add expected SHA-256 checksums to `configs/datasets.yaml` and `data/registry.yaml` for all raw downloads and cached `.npz` arrays.
  2. Implement an automated digest verification check in `load_dataset()` and `scripts/fetch_data.py` using `hashlib.sha256()`.

---

### AUD-SEC-004: Insecure CORS Configuration (`allow_origins=["*"]` with `allow_credentials=True`)
- **Severity:** Medium
- **CWE:** CWE-346 / CWE-942 (Permissive Cross-Origin Resource Sharing Policy with Credential Leaks)
- **Affected File:** `examples/web_demo/app/main.py:22-28`
- **Fact vs. Inference:** [Verified Fact].
- **Vulnerability Mechanics:**
  The FastAPI application defines:
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```
  In browser security standards (W3C CORS spec and Starlette runtime), configuring `allow_origins=["*"]` alongside `allow_credentials=True` is an invalid and insecure combination. Any malicious webpage visited by a user running the demo locally can issue cross-origin requests to `http://127.0.0.1:8000/api/*`.
- **Actionable Remediation Guidance:**
  Restrict origins to localhost / loopback interfaces, or disable `allow_credentials`.

---

### AUD-SEC-005: Denial of Service (DoS) via Unbounded Clustering Hyperparameters & Blocking Execution
- **Severity:** Medium
- **CWE:** CWE-400 (Uncontrolled Resource Consumption) / CWE-770
- **Affected File:** `examples/web_demo/app/main.py:119-152`
- **Fact vs. Inference:** [Verified Fact].
- **Vulnerability Mechanics:**
  The endpoint `/api/run_clustering` accepts Form parameters without range validation (`n_anchors: int = Form(30)`). Submitting `n_anchors=100000` forces massive memory allocation and CPU starvation.
- **Actionable Remediation Guidance:**
  Add FastAPI / Pydantic validation bounds (`ge=2, le=50` for `n_clusters`, `ge=5, le=100` for `n_anchors`).

---

### AUD-SEC-006: Insecure Cleartext HTTP Protocol Endpoints for Benchmark Dataset Downloads
- **Severity:** Low
- **CWE:** CWE-319 (Cleartext Transmission of Sensitive Information)
- **Affected Files:**
  - `configs/datasets.yaml:249` (`http://vision.ucsd.edu/extyaleb/CroppedYaleB.zip`)
  - `src/icc/datasets/image.py:70` (`http://www.cad.zju.edu.cn/home/dengcai/Data/YaleB/YaleB_32x32.mat`)
  - `data/registry.yaml:227,247`
- **Fact vs. Inference:** [Verified Fact].
- **Actionable Remediation Guidance:**
  Migrate endpoints to HTTPS mirrors where available, and enforce cryptographic hash validation prior to caching.

---

### AUD-SEC-007: Predictable Temporary File Naming in Cohort Retrieval Pipeline
- **Severity:** Low
- **CWE:** CWE-377 (Insecure Temporary File) / CWE-378
- **Affected File:** `src/icc/data/cohorts.py:200`
- **Fact vs. Inference:** [Verified Fact].
- **Vulnerability Mechanics:** Fixed `.part` suffix creates predictable temporary file names susceptible to write collisions in multi-user environments.
- **Actionable Remediation Guidance:**
  Use `tempfile.NamedTemporaryFile(dir=target.parent, prefix=target.name, suffix=".part", delete=False)`.

---

### AUD-SEC-008: Unclosed File Descriptor Handles in `np.load` Operations
- **Severity:** Low
- **CWE:** CWE-775 (Missing Release of Resource after Effective Lifetime)
- **Affected Files:**
  - `src/icc/datasets/genomics.py:126`
  - `examples/web_demo/app/main.py:37,80`
- **Fact vs. Inference:** [Verified Fact].
- **Vulnerability Mechanics:** Missing context manager `with np.load(...) as data:` leaves open file locks on Windows.
- **Actionable Remediation Guidance:**
  Refactor all `np.load` calls to use `with np.load(...) as data:`.

---

### AUD-SEC-009: Missing Subresource Integrity (SRI) on Third-Party Web Assets
- **Severity:** Low
- **CWE:** CWE-353 (Missing Support for Integrity Check)
- **Affected File:** `examples/web_demo/app/main.py:285-287`
- **Fact vs. Inference:** [Verified Fact].
- **Actionable Remediation Guidance:**
  Add `integrity` and `crossorigin="anonymous"` attributes to external Tailwind and Plotly CDN scripts.

---

### AUD-SEC-010: Undeclared Web Demo Dependencies & Permissive Version Bounds
- **Severity:** Informational
- **CWE:** CWE-1104 (Use of Unmaintained Third Party Components)
- **Affected Files:** `pyproject.toml:28-76`, `requirements.txt:14-37`
- **Fact vs. Inference:** [Verified Fact].
- **Actionable Remediation Guidance:**
  Add an optional dependency group `[project.optional-dependencies] demo = ["fastapi>=0.110.0", "uvicorn>=0.28.0"]` and raise minimum Pillow version to `Pillow>=10.4.0`.

---

### AUD-SEC-011: Clinical Data Privacy & HIPAA Compliance Verification
- **Severity:** Informational (Verified Positive Posture)
- **Affected Files:** `data/cache/*.npz`, `examples/clinical_cancer_subtyping.py`
- **Fact vs. Inference:** [Verified Fact].
- **Audit Findings:** Zero Protected Health Information (PHI) detected. All matrices contain exclusively numerical feature values and integer labels. All cohorts are established public historical academic benchmarks (Golub 1999, Alon 1999, Khan 2001, Pomeroy 2002, Singh 2002, Petricoin 2002).

---

### AUD-SEC-012: Secrets, Credentials, and Author Environment Isolation Audit
- **Severity:** Informational (Verified Positive Posture)
- **Affected Files:** Entire repository and Git commit history
- **Fact vs. Inference:** [Verified Fact].
- **Audit Findings:** Zero API keys, passwords, bearer tokens, or private author workstation paths (`C:\Users\...`) detected in committed files or historical commits.


---

## 4. Workstream B & C: Public Documentation Sanitization & Git History Confidentiality Remediation

### 4.1 Workstream B: Public Content Sanitization Findings & Actions

| File Path | Exposed Information | Why Sensitive / Inaccurate | Remediation Applied | Private Preservation |
|---|---|---|---|---|
| `configs/baselines.yaml:120,135` | `"venue: IEEE TKDE Under Review"`, `"first_author: Ours"` | Discloses unpublished journal submission metadata. | Replaced with `"venue: Software Repository"`, `"first_author: ICC-Clustering"`. | Original citation preserved in private archive. |
| `src/icc/data/cohorts.py:248,254` | Default CLI paths pointing to `research_audit/cohort_discovery` | Leaks private audit path references in public CLI help. | Changed defaults to `data/cohort_discovery`. | Private audits kept in offline archive. |
| `tests/integration/test_cohort_discovery.py:211` | Docstring referencing `research_audit/.../COHORT_DISCOVERY_ELIGIBILITY_SPEC.md` | Leaks private audit filename in public test suite. | Changed to generic specification description. | Kept in offline archive. |
| `.github/PULL_REQUEST_TEMPLATE.md:8` | Checkbox item mentioning `(manuscript/figures)` | References internal publication workflow. | Changed to `Documentation or technical benchmark update`. | None needed. |
| `.gitignore:92-127` | Un-ignore rules mentioning `springer_manuscript`, `submission/arxiv_package`, `paper/numbers.tex` | Exposes internal manuscript naming and TeX build files. | Replaced with generic pattern rules (`submission/`, `manuscript/`, `paper/`, `*.tex`). | Kept in private repo config. |

---

### 4.2 Workstream C: Git History Confidentiality Audit & Clean Candidate Preparation

#### Historical Exposure Table

| Commit / Tag Reference | Disclosure Identified | Severity | Status & Proposed Remediation |
|---|---|---|---|
| `e3f54cc0951d173f0e13a4b524628328f318e746` (2026-11-01) | Commit message discloses: "Verified all 8 preflight checks against immutable baseline protocol commit f96d73c", "Ingested and sealed 4 independent Tier A cancer cohorts under strict label quarantine (GSE42568, GSE19188, GSE21653, GSE32894; N_total=769)", "Executed 1,440 trial runs across 12 candidate models", "fingerprinted all model prediction arrays prior to post-inference vault unsealing", and references `G2_validation_EXECUTION_REPORT.md`. Tracked file: `src/icc/confirmatory/vault.py`. | **CRITICAL** | **Rewritten in Candidate**: Replaced with clean commit message describing Hodges-Lehmann estimator and benchmark test harness; removed `src/icc/confirmatory/` from history. |
| `1f066d2bec6a4eb55a1117020c0c3aad95b5968a` (2026-11-01) | Commit message discloses: "Consolidate research-audit and results/cohort-independence", "Integrate EXP6 (cohort expansion), EXP7 (modern baselines), and EXP8 (unknown-K cluster discovery) benchmark suites", "Include complete data independence audit, provenance references, sample overlap matrices, and lineage DAGs", "Include 1,015 completed overnight experimental runs". | **HIGH** | **Rewritten in Candidate**: Replaced with clean commit message describing baseline algorithm integration and script cleanup. |
| `0565abc5bc7efe72d10bd07ce08c94f368066c51` (2026-11-01) | Deleted `src/icc/confirmatory/vault.py` while commit subject was `chore(confidentiality): remove non-code documentation assets`. | **MEDIUM** | **Rewritten in Candidate**: Replaced commit subject with `chore: standardize repository documentation and configuration guides`. |
| `e18767bda224575b9b2ffe04c22abae06a492018` (2026-10-24) | Commit message discloses `numbers.tex`, paper revision metrics, Knockout 2 sign flip, and `REVISION_LOG.md` 11-point remediation checklist. | **HIGH** | **Rewritten in Candidate**: Replaced with clean message focusing on benchmark metric formulas and hyperparameter documentation. |
| `2859dab36d4000182c2f24c5476418092c44fe30` (2026-10-24) | Commit message discloses `fix(ci): track numbers.tex in repo and support CI execution in test_macro_consistency`. | **MEDIUM** | **Rewritten in Candidate**: Replaced with `fix(ci): update continuous integration test configuration`. |
| `da0af15306b639b5abfc67909992e89194e76d7f` (2026-10-17) | Commit message discloses `generate numbers.tex from results.json`. | **MEDIUM** | **Rewritten in Candidate**: Replaced with `fix(benchmarks): harmonize evaluation metrics for benchmark datasets`. |
| `7d0fa95c9aefe4669d68871ef36ea133fd6d99a7` (2026-10-12) | Commit message discloses `audit(e1): add pre-registered held-out comparison protocol (e1_held_out_comparison.py)`. | **LOW** | **Rewritten in Candidate**: Replaced with `feat(evaluation): add held-out model comparison evaluation script`. |
| `c70f976c01330bc1bcf4ebd616777185aea80072` (2026-10-12) | Commit message discloses `reorganize(audit): merge research_audit into standard hierarchy`. | **LOW** | **Rewritten in Candidate**: Replaced with `refactor: organize package directory hierarchy, update author metadata, and refresh benchmark plots`. |
| Tag `v1.0.0` | Annotation: `Release v1.0.0 with Zenodo DOI 10.5281/zenodo.23852735` | **MEDIUM** | **Sanitized in Candidate**: Re-annotated as `Release v1.0.0: Initial release of Invariant Core Consensus`. |
| Tag `v2.2.0` | Annotation: `feat(release): prepare public v2.2.0 release for peer review and independent reproduction` | **LOW** | **Sanitized in Candidate**: Re-annotated as `Release v2.2.0: Public release of ICC-v2 and benchmarking suite`. |

---

### 4.3 Candidate Preparation & Fresh-Clone Verification Results

1. **Full Backup Verification (`d:\icc-clustering-backup.git`):**
   - Mirror clone created via `git clone --mirror`.
   - Verified via `git fsck --full`: **0 dangling refs, 0 errors**.
   - Original HEAD: `1761c1a30c522078bc22245ca56187a5d641a491`.
2. **Clean Candidate (`d:\icc-clustering-candidate`):**
   - History rewritten with `git-filter-repo` in 2.61s.
   - Filtered out historical sensitive paths: `src/icc/confirmatory/`, `scripts/update_revision_log.py`, `scripts/update_revision_logs.py`.
   - Rewrote all 9 sensitive commit messages and retargeted sanitized tags.
   - Re-scanned with regex over all 139 commits: **0 flagged commits remain**.
   - Re-scanned object database: **0 historical sensitive objects remain**.
3. **Fresh-Clone Verification (`d:\icc-clustering-fresh-clone`):**
   - Created fresh clone from candidate.
   - `git fsck --full`: **0 errors**.
   - Executed pytest suite: **69/69 unit tests passed (100%) in 40s**.
   - Working tree completely functional and identical in functionality.
