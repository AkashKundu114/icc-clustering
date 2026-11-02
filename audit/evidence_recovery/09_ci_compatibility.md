# Forensic Evidence Report: CI Compatibility, Workflow Matrix, and Verification Blind Spots

**Target Repository**: `AkashKundu114/icc-clustering`  
**Current HEAD**: `7ddbe8301b8d27c94f388c40acbc88b0dee82723`  
**Audit Component**: Phase 4 — Continuous Integration, Matrix Coverage, and Packaging Discrepancies  
**Status**: INVESTIGATION COMPLETE — BLIND SPOT IDENTIFIED  

---

## 1. Executive Summary

A previous audit report claimed Python 3.14 compatibility was unverified and that CI only tested Python 3.10 through 3.12. An independent forensic investigation of `.github/workflows/ci.yml` and GitHub Actions execution logs demonstrates that:

1. **Matrix Expansion**: In commit `7ddbe8301b8d27c94f388c40acbc88b0dee82723` (committed `Sun Nov 1 22:19:09 2026 +0530`), the matrix was formally expanded from `["3.10", "3.11", "3.12"]` to `["3.10", "3.11", "3.12", "3.13", "3.14"]` across both `ubuntu-latest` and `windows-latest`.
2. **Workflow Execution**: GitHub Actions Run ID `41328272363` triggered on commit `7ddbe83` executed all 10 matrix jobs, plus code quality and static typing, with an aggregate status of **SUCCESS**.
3. **Local 3.14 Verification**: On the local audit environment (Python 3.14.6, Windows 11 AMD64), 133/133 unit tests pass with zero failures.
4. **Critical CI Blind Spot**: CI tests *only* editable source installs (`pip install -e ".[dev]"`), followed by direct script invocation (`python demo.py`, `python scripts/reproduce.py --scope smoke`). CI **never** builds a wheel, never installs the built wheel in an isolated clean environment, and never executes the declared entrypoints (`icc`, `icc-demo`, `icc-run`). Consequently, the fatal packaging defect documented in `08_packaging_audit.md` (console scripts crashing with `ModuleNotFoundError`) completely bypassed CI.

---

## 2. CI Evolution and Commit Forensic History

### 2.1 Git History of `.github/workflows/ci.yml`

| Commit SHA | Tag / Ref | Matrix Python Versions | Matrix Operating Systems | Install Command | Entrypoint / Packaging Tested? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `943e55e` | `v2.2.0` | `["3.10", "3.11", "3.12"]` | `ubuntu-latest`, `windows-latest` | `pip install -e ".[dev]"` | NO |
| `83728a4` | `HEAD~1` | `["3.10", "3.11", "3.12"]` | `ubuntu-latest`, `windows-latest` | `pip install -e ".[dev]"` | NO |
| `7ddbe83` | `HEAD` (`origin/main`) | `["3.10", "3.11", "3.12", "3.13", "3.14"]` | `ubuntu-latest`, `windows-latest` | `pip install -e ".[dev]"` | NO |

In commit `7ddbe83`, the matrix was updated to support modern Python releases (3.13 and 3.14) with `allow-prereleases: true` enabled in `actions/setup-python@v5`.

---

## 3. GitHub Actions Run Verification

Forensic inspection of GitHub Actions runs using `gh run list --workflow=ci.yml` and `gh run view` establishes the following execution records:

### 3.1 Run ID: 41328272363 (Trigger: Commit `7ddbe83`)
- **Workflow**: `ICC CI/CD`
- **Head SHA**: `7ddbe8301b8d27c94f388c40acbc88b0dee82723`
- **Conclusion**: `SUCCESS`
- **Event**: `push` to `main`
- **Jobs Executed**:
  1. `lint` (Ubuntu, Python 3.11, Ruff + Mypy) — **SUCCESS**
  2. `test (3.10, ubuntu-latest)` — **SUCCESS**
  3. `test (3.10, windows-latest)` — **SUCCESS**
  4. `test (3.11, ubuntu-latest)` — **SUCCESS**
  5. `test (3.11, windows-latest)` — **SUCCESS**
  6. `test (3.12, ubuntu-latest)` — **SUCCESS**
  7. `test (3.12, windows-latest)` — **SUCCESS**
  8. `test (3.13, ubuntu-latest)` — **SUCCESS**
  9. `test (3.13, windows-latest)` — **SUCCESS**
  10. `test (3.14, ubuntu-latest)` — **SUCCESS**
  11. `test (3.14, windows-latest)` — **SUCCESS**

### 3.2 Run ID: 41326511088 (Trigger: Commit `83728a4`)
- **Workflow**: `ICC CI/CD`
- **Head SHA**: `83728a441f44c1ed56a35a5bdb07490ff559de81`
- **Conclusion**: `SUCCESS`
- **Event**: `push` to `main`
- **Jobs Executed**: 6 matrix test jobs (3.10, 3.11, 3.12 on Ubuntu/Windows) + lint — **SUCCESS**

---

## 4. Python Compatibility Matrix

The verified status across Python versions 3.10 through 3.14 is summarized below (derived from `audit/evidence_recovery/python_compatibility_matrix.csv`):

| Python Version | Declared in Committed CI (`ci.yml`) | GitHub Actions Run ID | Remote CI Status | Local Verification Status (AMD64 Windows 11) | Verified Status |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **3.10** | YES (at `7ddbe83`) | `41328272363` | SUCCESS (Ubuntu & Windows) | NOT RUN (Host is 3.14) | **CI VERIFIED** |
| **3.11** | YES (at `7ddbe83`) | `41328272363` | SUCCESS (Ubuntu & Windows) | NOT RUN (Host is 3.14) | **CI VERIFIED** |
| **3.12** | YES (at `7ddbe83`) | `41328272363` | SUCCESS (Ubuntu & Windows) | NOT RUN (Host is 3.14) | **CI VERIFIED** |
| **3.13** | YES (at `7ddbe83`) | `41328272363` | SUCCESS (Ubuntu & Windows) | NOT RUN (Host is 3.14) | **CI VERIFIED** |
| **3.14** | YES (at `7ddbe83`) | `41328272363` | SUCCESS (Ubuntu & Windows) | SUCCESS (133/133 tests pass) | **LOCALLY & CI VERIFIED** |

All core algorithmic modules (Numpy 2.4.6, Scipy 1.18.0, Scikit-learn 1.9.1) run without ABI or syntax incompatibility on Python 3.14.

---

## 5. Critical CI Verification Blind Spot: Packaging & Console Scripts

While the test suite passes on all Python versions, the CI workflow suffers from a systemic architectural blind spot:

```yaml
# Lines 53-68 of .github/workflows/ci.yml
- name: Install Package and Core Dependencies
  run: |
    python -m pip install --upgrade pip
    python -m pip install -e ".[dev]"

- name: Run Pytest Test Suite
  run: |
    python -m pytest tests -v --cov=src/icc

- name: Run Interactive Demo Walkthrough
  run: |
    python demo.py

- name: Run Smoke Reproduction Verification
  run: |
    python scripts/reproduce.py --scope smoke
```

### 5.1 Root Causes of the Blind Spot
1. **Editable Installation Masking**: `pip install -e .` exposes the root working tree to the Python path. Code that references `scripts/` or assumes it is running from the root repository directory succeeds.
2. **Omission of Wheel Build Step**: CI never invokes `python -m build --wheel`.
3. **Omission of Clean Virtual Environment Wheel Test**: CI never creates an isolated temporary directory, executes `pip install dist/*.whl`, and verifies CLI execution outside the Git tree.
4. **Console Scripts Left Untested**: The three console scripts defined in `pyproject.toml`:
   - `icc = "icc.__main__:main"`
   - `icc-demo = "scripts.demo:main"`
   - `icc-run = "scripts.reproduce:main"`
   are completely uncalled in CI. In a real wheel installation, `scripts.demo` and `scripts.reproduce` do not exist (omitted by `packages.find`), and `icc.__main__` raises `ImportError: attempted relative import with no known parent package`.

---

## 6. Remediation Requirement for CI

To prevent false confidence, `.github/workflows/ci.yml` must be patched with a mandatory wheel validation stage:

```yaml
  package-test:
    name: Build & Verify Wheel Distribution
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Build Wheel
        run: |
          pip install build twine
          python -m build
          twine check dist/*
      - name: Test Wheel in Isolated Clean Environment
        run: |
          python -m venv test_env
          test_env/bin/pip install dist/*.whl
          # Verify entrypoints outside source repository
          cd /tmp
          /github/workspace/test_env/bin/icc --version
          /github/workspace/test_env/bin/icc-demo --help
          /github/workspace/test_env/bin/icc-run --help
```
