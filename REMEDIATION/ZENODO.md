# Instructions for Zenodo Integration and DOI Assignment

**Repository:** `AkashKundu114/icc-clustering`  
**Target Release Tag:** `v2.0.0`  

---

## 1. Connecting Zenodo to GitHub

1. Log in to [Zenodo](https://zenodo.org/) using your GitHub account.
2. Navigate to **GitHub settings** in Zenodo: `https://zenodo.org/account/settings/github/`.
3. Locate `AkashKundu114/icc-clustering` in the repository list and switch the toggle to **ON**.
4. Zenodo will configure a webhook on the repository.

---

## 2. Publishing Release `v2.0.0`

When you create the release tag on GitHub:
```bash
git tag -a v2.0.0 -m "Release v2.0.0: Inductive Consensus Clustering (ICC-v2)"
git push origin v2.0.0
```

Zenodo automatically triggers an archival snapshot, mints a permanent Digital Object Identifier (DOI), and provides citation records.

---

## 3. Data & Code Availability Statement for Manuscript

Update the manuscript's Availability section with the minted DOI:

```latex
\section*{Data and Code Availability}
The source code, benchmark configuration files, and reproduction scripts supporting the findings of this study are openly available on GitHub at \url{https://github.com/AkashKundu114/icc-clustering} (Release tag: \texttt{v2.0.0}) and permanently archived on Zenodo under DOI: \url{https://doi.org/10.5281/zenodo.XXXXXXX}.
```
