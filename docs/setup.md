# Setup and Installation Guide

## Requirements
- Python >= 3.10 (tested through 3.14 on Linux, macOS, and Windows)
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

## System Requirements & Resource Guidelines

### Recommended Hardware
- **CPU:** Multi-core x86_64 or ARM64 processor (8+ cores recommended for multi-seed benchmark evaluations).
- **RAM:** Minimum 8 GB (16+ GB recommended for large high-dimensional datasets and scRNA-seq matrices).
- **GPU (Optional):** NVIDIA GPU with CUDA support for optional deep clustering baselines (DEC, IDEC). All consensus and anchor clustering algorithms run natively and deterministically on CPU.

### Resource Limits and Safeguards
- **Memory Safeguard:** When executing extensive benchmark sweeps, ensure adequate host swap or container limits (e.g. 13 GB RAM limit threshold).
- **Disk Space:** At least 5 GB free disk space recommended for caching benchmark datasets and output logs.

## Verifying Installation

Run the test suite:
```bash
python -m pytest tests/ -q
```
