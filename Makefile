.PHONY: help install dev test lint format clean reproduce smoke numbers check-macros check-pdf refs-check figures compile package

PYTHON ?= python
PIP ?= pip

help:
	@echo "Inductive Consensus Clustering (ICC-v2) Makefile"
	@echo "Targets:"
	@echo "  install      : Install core package in editable mode"
	@echo "  dev          : Install development tools and test extras"
	@echo "  test         : Run full pytest test suite"
	@echo "  lint         : Check formatting and static type typing (ruff, mypy)"
	@echo "  format       : Auto-format source code using ruff"
	@echo "  reproduce    : Run demo reproduction check"
	@echo "  smoke        : Run fast fixed-seed smoke reproduction CLI"
	@echo "  numbers      : Re-synchronize LaTeX numbers.tex from Pass F results store"
	@echo "  check-macros : Verify numbers.tex consistency against Pass F store"
	@echo "  check-pdf    : Verify compiled PDF decimals against Pass F numerical allowlist"
	@echo "  refs-check   : Verify bibliography against CrossRef and arXiv APIs"
	@echo "  figures      : Regenerate experiment figures from frozen caches"
	@echo "  compile      : Compile Springer Nature manuscript main.pdf via Tectonic"
	@echo "  package      : Build Springer Nature and Overleaf submission packages"
	@echo "  clean        : Clean build and cache artifacts"

install:
	$(PIP) install -e .

dev:
	$(PIP) install -e ".[dev]"

test:
	$(PYTHON) -m pytest tests/ -v

lint:
	$(PYTHON) -m ruff check src/
	$(PYTHON) -m mypy -p icc

format:
	$(PYTHON) -m ruff format src/
	$(PYTHON) -m ruff check src/ --fix

reproduce:
	$(PYTHON) demo.py

smoke:
	$(PYTHON) scripts/reproduce.py --scope smoke

numbers:
	$(PYTHON) scripts/make_numbers.py

check-macros:
	$(PYTHON) tests/test_macro_consistency.py

check-pdf:
	$(PYTHON) tests/test_pdf_allowlist.py

refs-check:
	$(PYTHON) scripts/verify_refs.py refs.bib --out results/refs_report.csv --manual refs_manual.csv

figures:
	$(PYTHON) scripts/sync_figures.py

compile:
	@echo "Compiling Springer Nature manuscript..."
	tectonic -X compile springer_manuscript/main.tex --outdir springer_manuscript || pdflatex -output-directory=springer_manuscript springer_manuscript/main.tex


clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache/ .ruff_cache/ .mypy_cache/ .coverage
