# Repository Release & Remote Push Instructions (PUSH_INSTRUCTIONS.md)

This document provides exact, non-destructive commands for synchronizing local repositories with GitHub and archiving release bundles to Zenodo upon formal user authorization.

---

## Safety Protocol
- Under Rule R10, the autonomous agent will **never** automatically push commits or tags to remote repositories without explicit user instruction.
- All remote push actions are initiated by the human investigator using these documented commands.

---

## 1. Track A: Paper 1 (`icc-clustering`)

### Verification Pre-requisites
Ensure all tests and build-time audits pass before pushing:
```powershell
python -m pytest tests/
python tests/test_macro_consistency.py
python tests/test_pdf_allowlist.py
python scripts/verify_refs.py refs.bib --out results/refs_report.csv --manual refs_manual.csv
```

### Git Push Commands
```powershell
# Check current branch and git status
git status

# Push commits to remote
git push origin main

# If on a revision branch:
git push origin revision/final

# Push release tag (v2.1.0)
git push origin v2.1.0
```

---

## 2. Track B: Paper 2 (`paper2`)

### Local Creation & Verification
When Paper 2 is initialized in `paper2/`:
```powershell
cd paper2
git status
pytest tests/
```

### GitHub Repository Setup (Once User Approves)
Check GitHub CLI authentication status:
```powershell
gh auth status
```
If authenticated and authorized, create private repository:
```powershell
gh repo create AkashKundu114/<pkg-name> --private --source=. --remote=origin
git push -u origin main
```

---

## 3. Zenodo DOI Archival
1. Connect GitHub repository to Zenodo (`https://zenodo.org/account/settings/github/`).
2. Toggle repository switch to ON.
3. Push release tag:
   ```powershell
   git push origin v0.1.0
   ```
4. Zenodo automatically mints a citable concept DOI and archive snapshot tarball.
