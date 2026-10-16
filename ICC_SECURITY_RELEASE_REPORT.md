# ICC Security and Threat Modeling Release Report

**Project:** Invariant Core Consensus (ICC-v2)  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Active Branch:** `fix/audit-remediation`  
**Report Classification:** Production Hardening & Pre-Release Security Audit  
**Date:** October 16, 2026  
**Auditor:** Specialized Research Security & Hardening Agent  

---

## 1. Executive Summary

This security release report establishes the threat model, vulnerability audit results, and defensive mitigations for the `icc-clustering` research repository. Research codebases frequently operate under the assumption of benign local use, making them susceptible to remote code execution (RCE) via unsafe deserialization, denial-of-service (DoS) via unvalidated array shapes or extreme dimensional allocations, path traversal vulnerabilities, and silent numerical corruption.

Through this hardening cycle, the repository was audited and hardened against adversarial exploitation:
1. **Unsafe Deserialization Eliminated:** All instances of `allow_pickle=True` in `.npz` data caches were eliminated and locked down to `allow_pickle=False`.
2. **Strict Input Sanitization & Bounds Checking:** Centralized validation now enforces strict 2D array dimensionality, finite float values (rejecting `NaN` and `\pm\infty`), valid parameter domains, and exact feature dimension matching between training and query data.
3. **Execution Safety:** Zero instances of `eval()`, `exec()`, or unescaped shell invocations exist across the codebase.
4. **Credential & Secret Auditing:** Zero hardcoded secrets, API tokens, private keys, or machine-specific absolute file paths exist in code or configuration files.
5. **Continuous Integration Security:** CI pipelines execute under unprivileged runner contexts with scoped matrix workflows on modern Python runtimes (3.10–3.12 on Linux and Windows).

---

## 2. Threat Model and Security Boundaries

```
[Untrusted External Sources]
   │
   ├──> Malformed Datasets (NaNs, Infs, 1D/3D shapes, N < K)
   ├──> Malicious Serialized Files (Pickle exploits, altered .npz)
   ├──> Extreme Dimension Workloads (Memory exhaustion / OOM DoS)
   └──> Adversarial Out-of-Sample Queries (Dimension mismatch, empty batches)
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│             ICC-v2 Hardened Perimeter                       │
│                                                             │
│  1. Parameter Domain Gatekeeper (__init__)                  │
│  2. Input Matrix Shape & Type Sanitizer (fit_predict)       │
│  3. Strict Feature Dimension Matching (_validate_X_new)     │
│  4. Safe Storage Layer (allow_pickle=False)                 │
│  5. Bounded Memory Anchor Consensus (O(N) Graph)            │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
[Protected Scientific Execution Environment]
```

### 2.1 Assets to Protect
- **User Compute Environment:** Preventing arbitrary code execution, file system tampering, or network exfiltration when researchers clone and run the repository.
- **System Memory and Availability:** Preventing unconstrained matrix allocations ($N \times N$ dense affinity matrices) that cause operating system Out-Of-Memory (OOM) kernel crashes.
- **Scientific Integrity:** Preventing silent numerical errors, NaN propagation, or dimension misalignments that corrupt downstream published findings.

### 2.2 Threat Actors and Attack Vectors
- **Attacker Submitting Contrived Data:** An adversary providing a malicious dataset designed to exploit NumPy deserialization or trigger infinite loops / division-by-zero crashes.
- **Accidental User Misconfiguration:** A user passing out-of-domain hyperparameters (e.g., negative cluster counts, invalid gating quantiles) leading to undefined behavior.
- **Adversarial Batch Inference:** Streaming query samples with mismatched feature dimensions ($D_{\text{test}} \neq D_{\text{train}}$) designed to cause out-of-bounds memory access.

---

## 3. Vulnerability Findings and Remediation Ledger

| Vulnerability ID | Category | Severity | File Location | Status | Remediation Description |
|---|---|---|---|---|---|
| **SEC-001** | Deserialization | High | `experiments/audit_controls/src/*.py` | **Remediated** | Removed `allow_pickle=True` across all cache loaders; enforced safe NumPy array loading (`allow_pickle=False`). |
| **SEC-002** | Input Validation | Medium | `src/icc/consensus_v2.py:__init__` | **Remediated** | Implemented domain assertions for `n_clusters >= 2`, `n_base_models >= 1`, `n_anchors >= 1`, $0 < q \le 1$, and whitelist for `pool_mode`. |
| **SEC-003** | Data Sanitization | High | `src/icc/consensus_v2.py:fit_predict` | **Remediated** | Enforced 2D array verification, $N \ge K$, non-empty matrix validation, and rejection of `NaN`/`Inf` inputs. |
| **SEC-004** | Dimensional Integrity | Medium | `src/icc/consensus_v2.py:_validate_X_new` | **Remediated** | Enforced exact feature dimension matching between training cohort and query batch ($X_{\text{new}}.shape[1] == n\_features\_in\_$). |
| **SEC-005** | Denial of Service | Medium | `src/icc/consensus_v2.py:predict*` | **Remediated** | Added zero-length batch guards returning empty arrays with expected shapes instead of raising unhandled index faults. |
| **SEC-006** | Supply Chain / Env | Low | `pyproject.toml`, `requirements.txt` | **Remediated** | Pinned minimal secure versions for dependencies, verified zero risky native extensions. |
| **SEC-007** | Pipeline Reliability | Low | `.github/workflows/ci.yml`, `demo.py` | **Remediated** | Harmonized root walkthrough entrypoint to prevent CI breakages and path confusion. |

---

## 4. Deserialization and Code Execution Audit

### 4.1 Audit for Unsafe Deserialization
A search for serialization routines across the codebase revealed no usage of Python standard library `pickle.load` or `pickle.loads` in core logic. In benchmark control modules, `np.load` was previously called with `allow_pickle=True`. Because `.npz` archives can embed arbitrary object arrays executing code on unpickling, this was a potential vulnerability if an untrusted user supplied cached results.

**Verification:** All calls in:
- `experiments/audit_controls/src/e1_extended_benchmarks.py`
- `experiments/audit_controls/src/e1_held_out_comparison.py`
- `results/audit_controls/src/e1_extended_benchmarks.py`
- `results/audit_controls/src/e1_held_out_comparison.py`

now explicitly specify `allow_pickle=False`. All caches contain solely primitive float64 and int64 numerical ndarrays, and all load operations pass without error.

### 4.2 Dynamic Code Execution
- `eval()` occurrences: **0**
- `exec()` occurrences: **0**
- `__import__()` with user input: **0**
- `subprocess` / `os.system` / `popen` with shell=True: **0**

### 4.3 Path Traversal and File Access Safety
File operations across `src/icc/` are restricted to reading datasets from configured directories and writing outputs to user-specified paths. All dataset loaders in `src/icc/datasets/` employ explicit path construction via `pathlib.Path` with directory containment checks, preventing directory traversal (`../`) attacks.

---

## 5. Security Regression Verification

To guarantee that these security layers remain functional across future releases, a dedicated adversarial test suite was authored in `tests/test_adversarial_inputs.py`.

```powershell
python -m pytest tests/test_adversarial_inputs.py -v
```
**Results:**
- 33 test cases executed.
- 33 passed in 4.55s.
- 0 failures, 0 regressions.

### Confirmed Defenses:
- Out-of-bounds parameters (`n_clusters=0`, `core_quantile=-0.1`, `pool_mode="eval"`) immediately raise descriptive `ValueError`.
- Malformed inputs (1D arrays, 3D tensors, empty matrices) immediately raise `ValueError`.
- Hostile numerical inputs (`NaN`, `+\infty`, `-\infty`) immediately raise `ValueError`.
- Feature dimension mismatches during out-of-sample inference immediately raise `ValueError`.
- Un-fitted estimator queries immediately raise `RuntimeError`.
- Empty test batches return clean zero-length arrays without crashing.

---

## 6. Pre-Release Security Recommendation

1. **Keep `allow_pickle=False` default:** Never re-enable `allow_pickle=True` in any experiment script or artifact loader.
2. **Automated Security Scanning:** Enable GitHub CodeQL analysis or Bandit in `.github/workflows/` to continuously check for AST vulnerabilities on all future pull requests.
3. **Data Ingestion Boundary:** When ingesting external CSV or TSV user files, ensure users pass them through `src/icc/datasets/` loaders which guarantee typecasting to `np.float64` prior to consensus clustering.

**Security Sign-Off:** **APPROVED FOR RESEARCH RELEASE.**
