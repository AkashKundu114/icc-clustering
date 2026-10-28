# Contributing to nullconsensus

Thank you for your interest in contributing to **nullconsensus**!

## Development Setup
```bash
git clone https://github.com/AkashKundu114/nullconsensus.git
cd nullconsensus
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Running Tests
```bash
pytest tests/
```

## Code Quality
```bash
ruff check src/
mypy src/nullconsensus
```
