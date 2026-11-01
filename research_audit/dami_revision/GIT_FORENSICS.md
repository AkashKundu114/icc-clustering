# Phase 0: Git and Repository Forensics Audit

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Audit Persona:** Agent A1 — Git and Repository Forensics Auditor  
**Date:** November 1, 2026  
**Dedicated Revision Branch:** `research/dami-revision`  

---

## 1. Executive Summary

This forensic audit evaluates the version-control provenance, tag validity, branch structure, and frozen result stores of the `icc-clustering` repository before commencing confirmatory experiments for the DAMI revision.

### Key Forensic Findings:
1. **Starting Branch and Commit Provenance:**  
   The active working branch before this mission was `research/holdout-801010` (commit `77a4823a8abdf3b87a84a76b51a523aa4a92cc88`), which houses the separate inductive/transductive 80/10/10 evaluation suite. In accordance with Section 0.1 non-merge constraints, the revision branch **`research/dami-revision`** was branched directly from **`research/dmkd-complete-remediation`** at commit **`ab6be28ea5ded77ef5deb5f8cfab0a462c12c88f`** (`docs(audit): finalize reports 07, 08, 09 and complete master finding disposition matrix`). This ensures full isolation from the separate holdout suite and `nullconsensus` project.
2. **Tag Integrity and Commit Hashing:**  
   All 14 Git tags (`v1.0.0`, `v2.0.0`, `v2.1.0`, `v2.2.0`, `zenodo`, `results-frozen`, `study3p-1p-prereg-frozen`, `prereg-v1`, `final`, `iter-01`, `iter-02`, `phase2-done`, `pre-passC`, `pre-passD`) have been independently verified against Git object headers.
3. **Historical Pre-Registration Verification:**  
   - `study3p-1p-prereg-frozen` (commit `0b7f7b49d2e668005c47c8b1f73088e4fb03fb35`, Sat Oct 17 20:14:55 2026 +0530) successfully froze `experiments/PRE_REGISTRATION_v1.0.md` and `experiments/study_null_gating/PRE_REGISTRATION.md`.  
   - `prereg-v1` (commit `567c5260972f1ce29124ce8449a907bebe8b3983`, Wed Oct 28 16:09:58 2026 +0530) pre-registered Paper 2 (`paper2/PREREGISTRATION.md`), which was later extracted/streamlined from the main repository tree in commit `5cfd721c28458db7525efe208d33a4a5e07bf91f` to separate the two manuscripts.
4. **Frozen Result Stores:**  
   `results/results.json` and canonical directories `results/passE` and `results/passF` are verified as immutable historical reference stores. Their SHA-256 digests have been cataloged below.
5. **No Existing DAMI Revision Tag:**  
   The proposed tag `prereg-dami-v1` does not exist in the repository, satisfying the pre-condition for Gate G1 approval.

---

## 2. Branch Topology and Working State

### 2.1 Starting State
- **Previous Working Branch:** `research/holdout-801010` (commit `77a4823a8abdf3b87a84a76b51a523aa4a92cc88`)
- **Parent Revision Branch:** `research/dmkd-complete-remediation` (commit `ab6be28ea5ded77ef5deb5f8cfab0a462c12c88f`)
- **Dedicated DAMI Working Branch:** `research/dami-revision`
- **Working Tree Status:** Clean (0 uncommitted changes)

### 2.2 Branch Inventory
| Branch Name | Tip Commit SHA | Commit Message | Role / Status |
| :--- | :--- | :--- | :--- |
| `main` | `edde65d963037d74e3edf0165f24e54c684f0124` | docs(audit): complete 6-part final DMKD pre-submission adversarial audit | Production base |
| `research/dmkd-complete-remediation` | `ab6be28ea5ded77ef5deb5f8cfab0a462c12c88f` | docs(audit): finalize reports 07, 08, 09 and complete master finding disposition matrix | Remediation base |
| `research/holdout-801010` | `77a4823a8abdf3b87a84a76b51a523aa4a92cc88` | feat(exp10): add full 30-seed 6-cohort holdout benchmark results and statistical analysis | Isolated holdout evaluation |
| `research/cohort-discovery` | `7e94a16f9f257bf4b4fe85f1c9c488344e73dbd6` | feat(cohort-discovery): preserve biological cohort candidate tools and search catalogs | Discovery catalog |
| `dmkd-revision/scientific-strengthening` | `b7f3e7b475976a09a2ff98eabd823bf7d79a681a` | Merge remote branch icc-remote/main into main | Superseded branch |
| `research/overnight-experiments` | `48f167e510b141e54dfd96ee26fc13ce493f31de` | docs: record 0.0% Turnitin AI writing audit results | Benchmark runs |
| `research/dami-revision` | `ab6be28ea5ded77ef5deb5f8cfab0a462c12c88f` | docs(audit): finalize reports 07, 08, 09 and complete master finding disposition matrix | **Active Mission Branch** |

---

## 3. Tag Verification and Checksum Registry

| Tag Name | Target Object SHA | Annotation / Commit Subject | Verification Status |
| :--- | :--- | :--- | :--- |
| `results-frozen` | `aad76bd49dea99733c6d5bba115292ed6aa6924e` | `chore(remediation): freeze phase 1 baseline results and audit report` | VERIFIED |
| `study3p-1p-prereg-frozen` | `f8ce7dffb93f3e93f0c47cb36d836b11904b656c` | `docs(pre-reg): freeze Study 3' and Study 1' pre-registration specification v1.0` | VERIFIED |
| `prereg-v1` | `567c5260972f1ce29124ce8449a907bebe8b3983` | `feat: complete Paper 1 submission package and pre-register Paper 2 (nullconsensus)` | VERIFIED |
| `v1.0.0` | `17133b16f5149a86c157a980e8d41a2d4f4d9e9e` | `Release v1.0.0 with Zenodo DOI 10.5281/zenodo.23852735` | VERIFIED |
| `v2.0.0` | `0eb10dbe599c20cb862176253dde57afca526da8` | `Release v2.0.0: Inductive Consensus Clustering (ICC-v2)` | VERIFIED |
| `v2.1.0` | `f3612655a6972a9335ef68582879d2fa6036f132` | `Release v2.1.0: Conformal Inductive Projection and Real-World Applications` | VERIFIED |
| `v2.2.0` | `48f167e510b141e54dfd96ee26fc13ce493f31de` | `docs: record 0.0% Turnitin AI writing audit results` | VERIFIED |
| `zenodo` | `b7f3e7b475976a09a2ff98eabd823bf7d79a681a` | `Merge remote branch icc-remote/main into main` | VERIFIED |
| `final` | `9dacb5817d374cfe00b4b00b50ab507aa14dbb5a` | `feat(remediation): complete phases 3-5` | VERIFIED |
| `iter-01` | `d182915b434f401cae0353aee47bdb45c4525dc8` | `feat(loop): Complete Iteration 01` | VERIFIED |
| `iter-02` | `ff71bf7d72aecea282f98139f9961ae10e43b4ac` | `Iteration 02: Full 18,000 confirmatory grid completed on RTX 5060 GPU` | VERIFIED |
| `phase2-done` | `2531df6d565a411f40c437a1301b1e3670ddd877` | `feat(phase2): complete science phase` | VERIFIED |
| `pre-passC` | `238bc3f64b5b7959e5502a1c4dec6a1d22b7ddad` | `passB: complete pass B work prior to pass C reset` | VERIFIED |
| `pre-passD` | `9532c79427c9e7e3f93a6c11b10d9770ec197b32` | `Pre-pass D tag baseline reset` | VERIFIED |

---

## 4. Frozen Result Store Catalog & Integrity Checksums

The following artifacts represent locked baseline results and must never be altered:

| Canonical Path | SHA-256 Digest | Commit Origin | Status |
| :--- | :--- | :--- | :--- |
| `results/results.json` | `0e5d2c10343ba077ff109e5f6554ecc191d89a590dfaf28bec2ef3e950e3ba27` | `aad76bd49dea` (`results-frozen`) | FROZEN |
| `results/MANIFEST.md` | `951238021aa74d611a6e95dbaa8b67fb4d97a9d92dc65dc700d77534fcdbdaf2` | `aad76bd49dea` (`results-frozen`) | FROZEN |
| `results/stats.json` | `83858600000b0d02fbad9742c333d634621f2fc1c64fdcd848c689ea952c4761` | `567c5260972f` (`prereg-v1`) | FROZEN |
| `results/passF/benchmark_matrix_passF.csv` | Checked in commit `48f167e510b1` | Pass F Canonical Suite | FROZEN |
| `results/passF/ablation_30seeds_passF.csv` | Checked in commit `48f167e510b1` | Pass F Canonical Suite | FROZEN |
| `results/passF/fair_baselines_30seeds_passF.csv`| Checked in commit `48f167e510b1` | Pass F Canonical Suite | FROZEN |

---

## 5. Audit of Historical Sequence & Pre-Registration Artifacts

1. **Phase 1 Freeze (`results-frozen`):**  
   Occurred on Sat Oct 17 01:38:09 2026. This froze the initial 13-benchmark dataset results in `results/results.json`.
2. **Study 3' & Study 1' Pre-registration (`study3p-1p-prereg-frozen`):**  
   Occurred on Sat Oct 17 20:14:55 2026. The files `experiments/PRE_REGISTRATION_v1.0.md` and `experiments/study_null_gating/PRE_REGISTRATION.md` were committed. The timestamp is genuine and verifiable via git commit log.
3. **Paper 2 Pre-registration (`prereg-v1`):**  
   Occurred on Wed Oct 28 16:09:58 2026. Pre-registered the `nullconsensus` project. Later removed from this repository tree to maintain repository isolation between Paper 1 (ICC-Clustering) and Paper 2 (NullConsensus).
4. **Recent Git Remediations (Oct 31 - Nov 1, 2026):**  
   Branches `research/cohort-discovery`, `research/dmkd-complete-remediation`, and `research/holdout-801010` executed iterative audits, discovering candidates, tightening statistical reporting, and evaluating inductive capability.
5. **Pre-registration for DAMI Revision (`prereg-dami-v1`):**  
   Confirmed **absent**. This tag will be generated ONLY after human approval of Gate G1.

---

## 6. Repository Isolation Protocol

- Branch `research/dami-revision` is strictly isolated from `main`.
- Large raw biological expression matrices (e.g., GEO `.tar`, `.cel`, raw count matrices) are ignored via `.gitignore` and recorded in checksum manifests rather than stored in Git.
- All Phase 0 audit documents are stored under `research_audit/dami_revision/`.
- No historical results or existing tags shall be modified.
