.PHONY: help install dev test lint format run clean

PYTHON ?= python
PIP ?= pip

help:
	@echo "Invariant Core Consensus (ICC) Makefile"
	@echo "Targets:"
	@echo "  install      : Install core package in editable mode"
	@echo "  dev          : Install development tools and test extras"
	@echo "  test         : Run full pytest test suite"
	@echo "  lint         : Check formatting and static types (ruff, mypy)"
	@echo "  format       : Auto-format source code using ruff"
	@echo "  run          : Run demo script"
	@echo "  clean        : Clean build and cache artifacts"

install:
	$(PIP) install -e .

dev:
	$(PIP) install -e ".[dev]"

test:
	$(PYTHON) -m pytest tests/

lint:
	$(PYTHON) -m ruff check src/
	$(PYTHON) -m mypy -p icc

format:
	$(PYTHON) -m ruff format src/
	$(PYTHON) -m ruff check src/ --fix

run:
	$(PYTHON) demo.py

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache/ .ruff_cache/ .mypy_cache/ .coverage
