# Setup and Installation Guide

## Requirements
- Python >= 3.10 (tested through 3.14)
- Pip >= 22.0

## Installation

### Standard Installation
Clone the repository and install core dependencies:

```bash
git clone https://github.com/AkashKundu114/icc-clustering.git
cd icc-clustering
pip install -e .
```

### Optional Dependencies

1. **Deep Learning Baselines (DEC, IDEC):**
   ```bash
   pip install -e ".[deep]"
   ```

2. **Single-cell & Genomics (Scanpy, AnnData):**
   ```bash
   pip install -e ".[bio]"
   ```

3. **Development and Testing:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **All Components:**
   ```bash
   pip install -e ".[all]"
   ```

## Verifying Installation

Run the test suite:
```bash
python -m pytest tests/
```
