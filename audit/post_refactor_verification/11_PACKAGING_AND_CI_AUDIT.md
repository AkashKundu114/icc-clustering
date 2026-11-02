# 11 Packaging, CLI Distribution, and CI Workflow Audit Report

**Audit Target:** ICC-Clustering (`D:\icc-clustering`)  
**Auditor:** Agent F (Packaging, Distribution & CI Specialist) & Lead Verification Auditor  
**Audit Timestamp:** 2026-11-01T22:44:00+05:30  
**Repository HEAD:** `83728a441f44c1ed56a35a5bdb07490ff559de81` / `7ddbe8301b8d27c94f388c40acbc88b0dee82723`  
**Execution Environment:** Windows 11 AMD64, CPython 3.14.6  
**Primary Files Audited:**
- `pyproject.toml`
- `src/icc/__main__.py`
- `.github/workflows/ci.yml`
- `README.md`, `docs/api.md`, `docs/usage.md`, `docs/reproducibility.md`

---

## 1. Executive Summary

This independent audit evaluated PEP 517/518/621 packaging specifications, built distribution artifacts (`.whl`), command-line entry points in an isolated virtual environment, continuous integration (CI) workflows, and public documentation integrity.

### Packaging Verdict: **ALL CONSOLE SCRIPTS BROKEN IN BUILT WHEEL DISTRIBUTION**

1. **Catastrophic CLI Entry Point Failure (P1 - PACKAGING):**
   When the built wheel (`icc-2.2.0-py3-none-any.whl`) is installed into a clean virtual environment outside the repository, **all three configured console scripts crash with fatal errors**:
   - `icc-run` raises `ModuleNotFoundError: No module named 'scripts'` because `scripts/` is excluded from wheel packaging by `where = ["src"]`.
   - `icc` and `icc-demo` raise `ModuleNotFoundError: No module named 'demo'` because `src/icc/__main__.py:11` attempts an uninstalled root relative import `from demo import main`.
2. **Import-Time Warning Emission (P2 - HYGIENE):**
   Simply executing `import icc` in a clean environment unconditionally prints two `ConvergenceWarning` stack traces to `stderr` from `src/icc/baselines/anchor.py:27` and `deep.py:27`.
3. **CI Matrix & Test Coverage (PASS):**
   GitHub Actions workflows test Python 3.10 through 3.14 on Ubuntu and Windows. Full 133/133 unit tests pass on local Python 3.14 and across CI runners.
4. **Documentation Discrepancies (P2 / P3 - DOCUMENTATION):**
   - `README.md` documents a non-existent `--visualize` CLI flag for `scripts/prepare_data.py`.
   - `docs/api.md` instructs users to import `bonferroni_correction` and `wilcoxon_signed_rank_test` from `icc.stats`, which fails with `ImportError`.
   - `docs/usage.md` documents invalid constructor arguments `ASPPConfig(n_bootstrap=10)`.

---

## 2. Packaging & Wheel Build Audit

### 2.1 Specification in `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "icc"
version = "2.2.0"
...
[project.scripts]
icc = "icc.__main__:main"
icc-demo = "icc.__main__:main"
icc-run = "scripts.run:main"

[tool.setuptools.packages.find]
where = ["src"]
```

### 2.2 Built Wheel Inspection

We built the release wheel using `python -m build --wheel --outdir results/post_refactor_verification/packaging/`:
- **Artifact:** `icc-2.2.0-py3-none-any.whl` (Size: 115,421 bytes).
- **Archive Contents (`top_level.txt`):**
  ```text
  cicc
  icc
  ```
- **Omission of `scripts`:** Because `[tool.setuptools.packages.find] where = ["src"]` is configured, the root directory `scripts/` is not discovered or packaged. No `scripts` module exists in the wheel distribution.

---

## 3. Clean Isolation Verification & Tracebacks

We created a fresh virtual environment at `C:\Users\Akash\AppData\Local\Temp\icc_clean_venv`, installed the wheel via pip, and executed tests from `C:\Users\Akash\AppData\Local\Temp` (strictly outside the repository root):

### 3.1 Python Import Test
```powershell
python -c "import icc; print('Version:', icc.__version__)"
```
- **Exit Code:** `0`
- **Output:**
  ```text
  ConvergenceWarning: Number of distinct clusters (1) found smaller than n_clusters (2). Possibly due to duplicate points in X.
  ConvergenceWarning: Number of distinct clusters (1) found smaller than n_clusters (2). Possibly due to duplicate points in X.
  Version: 2.2.0
  ```

### 3.2 Console Script: `icc --help`
- **Exit Code:** `1` (CRASH)
- **Traceback:**
  ```text
  Traceback (most recent call last):
    File "<frozen runpy>", line 203, in _run_module_as_main
    File "<frozen runpy>", line 88, in _run_code
    File "C:\Users\...\site-packages\icc\__main__.py", line 11, in <module>
      from demo import main  # noqa: E402
      ^^^^^^^^^^^^^^^^^^^^^
  ModuleNotFoundError: No module named 'demo'
  ```

### 3.3 Console Script: `icc-demo --help`
- **Exit Code:** `1` (CRASH)
- **Traceback:**
  ```text
  ModuleNotFoundError: No module named 'demo'
  ```

### 3.4 Console Script: `icc-run --help`
- **Exit Code:** `1` (CRASH)
- **Traceback:**
  ```text
  Traceback (most recent call last):
    File "<frozen runpy>", line 203, in _run_module_as_main
    File "<frozen runpy>", line 88, in _run_code
    File "C:\Users\...\site-packages\icc-run.exe\__main__.py", line 2, in <module>
      from scripts.run import main
  ModuleNotFoundError: No module named 'scripts'
  ```

---

## 4. Continuous Integration Matrix Audit

### 4.1 CI Configuration (`.github/workflows/ci.yml`)

- **Trigger:** Pushes and pull requests to `main`.
- **Operating Systems:** `ubuntu-latest`, `windows-latest`.
- **Python Versions:** `3.10`, `3.11`, `3.12`, `3.13`, `3.14`.
- **Jobs:**
  - `lint`: Runs `ruff check .` and `black --check .`.
  - `test`: Executes `pytest tests/ -v --cov=icc --cov-report=term-missing`.
  - `type-check`: Runs `mypy src/icc`.

### 4.2 CI Execution History
- Workflow run `41326511088`: Passed across all matrix jobs.
- Workflow run `41328272363`: Passed across all matrix jobs.
- **Why CI Failed to Catch Broken Console Scripts:**
  Existing test suites run inside the cloned repository root where `scripts/` and `demo.py` are present on `sys.path`. No CI test builds the wheel and installs it into an isolated environment to verify console script entry points.

---

## 5. Documentation Integrity Audit

| File Path | Documented Construct | Actual Code Reality | Severity |
|---|---|---|:---:|
| `README.md` | `python scripts/prepare_data.py --visualize` | Argument `--visualize` does not exist in `prepare_data.py` `argparse` | Medium |
| `docs/api.md` | `from icc.stats import wilcoxon_signed_rank_test, bonferroni_correction` | `src/icc/stats/__init__.py` does not export them (`ImportError`) | Medium |
| `docs/usage.md` | `ASPPConfig(n_bootstrap=10)` | Parameter does not exist (`n_base_models=5` is actual) | Medium |
| `docs/usage.md` | `summary.mean_pac` | Attribute does not exist on `ASPPProfile` | Low |
| `docs/reproducibility.md` | Code fence syntax (`` ` ash ``) | Fixed in commit `7ddbe83` | Resolved |

---

## 6. Remediation Plan

1. **Fix Console Script Packaging:**
   - Package CLI commands under `src/icc/cli/` (e.g., `src/icc/cli/run.py` and `src/icc/cli/demo.py`).
   - Update `[project.scripts]` in `pyproject.toml`:
     ```toml
     [project.scripts]
     icc = "icc.cli.main:main"
     icc-demo = "icc.cli.demo:main"
     icc-run = "icc.cli.run:main"
     ```
2. **Add Isolated Wheel Test to CI:**
   Add a CI step that builds the wheel, installs it into a fresh virtual environment, and executes `icc --help`, `icc-demo --help`, and `icc-run --help`.
3. **Correct Documentation:**
   Update `README.md`, `docs/api.md`, and `docs/usage.md` to match current function signatures and CLI flags.
