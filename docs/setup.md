# Installation and tested environments

## Requirements

The package metadata declares Python 3.10 or later. The GitHub Actions workflow on the latest inspected `main` commit (`8a97edcbe1b62269fdb36cd2070c94fad1e8eeef`) completed successfully for Ubuntu and Windows across Python 3.10–3.14 on 2026-11-02. A separate local editable-install check was run on Windows 11 with Python 3.14.6. These checks do not establish macOS support or a guarantee of bitwise-identical results across systems.

## Install from source

```bash
git clone https://github.com/AkashKundu114/icc-clustering.git
cd icc-clustering
python -m venv .venv
# Activate the environment using the instructions for your shell.
python -m pip install --upgrade pip
python -m pip install -e .
```

The project distribution name is `icc-clustering`; the Python import package remains `icc`. Install from this repository rather than assuming that a similarly named package on a package index is this project.

Optional dependency groups are declared in `pyproject.toml`: `.[deep]` for selected deep-learning baselines, `.[bio]` for Scanpy/AnnData integrations, and `.[dev]` for tests and development tools. The `.[all]` group is broad and may require substantial platform-specific dependencies. For contributor/test setup, `python -m pip install -r requirements-dev.txt` installs the current checkout with the `dev` extra.

## Verify the software installation

```bash
python -c "import icc; print(icc.__version__)"
```

To install development tools and run the unit/regression tests:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest tests/unit tests/regression -q
```

The full integration suite also contains a Yale B loader test that attempts to download the dataset. Yale B is not bundled here, redistribution rights are not cleared, and the upstream mirror timed out in the fresh-clone check. Consequently, a fresh clone did not pass `python -m pytest tests/ -q`; see [reproducibility status](reproducibility.md). The test should not be treated as an offline check.

The synthetic smoke workflow is:

```bash
python scripts/reproduce.py --scope smoke
```

This runs the synthetic example configuration only. It does not reproduce the historical six-cohort analysis or the 13-dataset result tables. Only `smoke` and `verify` are accepted scopes; requests for `tables`, `figures`, or `full` now fail instead of returning success without producing results. See [reproducibility](reproducibility.md).
