# Package Naming Verification (NAMING.md)

This document records the namespace collision check for the Paper 2 repository and Python package name.

---

## 1. Selected Package Name: `nullconsensus`
- **Module Name:** `nullconsensus`
- **Canonical Repository:** `AkashKundu114/nullconsensus`
- **Formal Title:** *Permutation-Null Calibrated Consensus Clustering: Resolving the Stability-Accuracy Trap in High-Dimensional Manifolds*

---

## 2. Namespace Collision Checks (Conducted: 2026-10-28)

| Registry / Platform | Target Name | Status | Verified Evidence |
| :--- | :--- | :---: | :--- |
| **PyPI** | `nullconsensus` | **AVAILABLE** | Verified via PyPI JSON API (`https://pypi.org/pypi/nullconsensus/json` returned HTTP 404 Not Found). |
| **GitHub** | `nullconsensus` | **AVAILABLE** | Verified via GitHub Repository Search API (`items: 0` matches across all public repositories). |
| **User Org** | `AkashKundu114/nullconsensus` | **AVAILABLE** | Target repository is uncreated and ready for initialization. |

---

## 3. Alternative Considered
- `nullgate`: Taken on PyPI (HTTP 200).
- `nullcluster`: Available on PyPI (HTTP 404), but `nullconsensus` better reflects the ensemble co-association and permutation-null stability mechanics.
