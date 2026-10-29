.PHONY: help install dev test lint format clean reproduce-small reproduce-paper

PYTHON ?= python
PIP ?= pip

help:
	@echo "nullconsensus Makefile targets:"
	@echo "  install          : Install package in editable mode"
	@echo "  dev              : Install development extras"
	@echo "  test             : Run full test suite"
	@echo "  lint             : Check code formatting and static types"
	@echo "  format           : Auto-format source code"
	@echo "  reproduce-small  : Run small DEV reproduction pipeline"
	@echo "  reproduce-paper  : Run full frozen TEST benchmark pipeline"
	@echo "  clean            : Clean caches and build directories"

install:
	$(PIP) install -e .

dev:
	$(PIP) install -e ".[dev]"

test:
	$(PYTHON) -m pytest tests/ -v

lint:
	$(PYTHON) -m ruff check src/
	$(PYTHON) -m mypy src/nullconsensus

format:
	$(PYTHON) -m ruff format src/
	$(PYTHON) -m ruff check src/ --fix

reproduce-small:
	$(PYTHON) scripts/run_dev_pilots.py

reproduce-paper:
	$(PYTHON) scripts/run_test_benchmark.py

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache/ .ruff_cache/ .mypy_cache/ .coverage
