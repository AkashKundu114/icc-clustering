.PHONY: help install dev test lint format clean check reproduce smoke verify tables figures benchmarks all

PYTHON ?= python
PIP ?= pip

help:
	@echo "Inductive Consensus Clustering (ICC-v2) Makefile"
	@echo "Targets:"
	@echo "  install      : Install core package in editable mode"
	@echo "  dev          : Install development tools and test extras"
	@echo "  test         : Run full pytest test suite"
	@echo "  lint         : Check formatting and static type checking (ruff, mypy)"
	@echo "  format       : Auto-format source code using ruff"
	@echo "  check        : Run automated scientific and empirical consistency check"
	@echo "  reproduce    : Run complete paper reproduction suite (tables + figures + benchmarks)"
	@echo "  tables       : Reproduce all paper empirical tables (Tables 1-16)"
	@echo "  figures      : Reproduce and audit all paper figures (Figures 1-10)"
	@echo "  benchmarks   : Run live benchmark evaluations on real microarray cohorts"
	@echo "  smoke        : Run fast fixed-seed smoke reproduction CLI (< 3 seconds)"
	@echo "  verify       : Verify mathematical proofs, determinacy identities, and invariants (< 3 seconds)"
	@echo "  clean        : Clean build and cache artifacts"

install:
	$(PIP) install -e .

dev:
	$(PIP) install -e ".[dev]"

test:
	$(PYTHON) -m pytest tests/ -v

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m mypy -p icc

format:
	$(PYTHON) -m ruff format .
	$(PYTHON) -m ruff check . --fix

check:
	$(PYTHON) tools/check_consistency.py

reproduce:
	$(PYTHON) scripts/reproduce.py --scope all

tables:
	$(PYTHON) scripts/reproduce_tables.py

figures:
	$(PYTHON) scripts/reproduce_figures.py

benchmarks:
	$(PYTHON) scripts/reproduce_benchmarks.py

smoke:
	$(PYTHON) scripts/reproduce.py --scope smoke

verify:
	$(PYTHON) scripts/reproduce.py --scope verify

all: check test tables figures benchmarks

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache/ .ruff_cache/ .mypy_cache/ .coverage
