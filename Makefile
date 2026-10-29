.PHONY: help install dev test lint format clean reproduce smoke

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

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache/ .ruff_cache/ .mypy_cache/ .coverage
