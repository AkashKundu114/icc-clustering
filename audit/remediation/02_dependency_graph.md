# Remediation Dependency Graph: ICC-Clustering Repository

**Target Repository**: `AkashKundu114/icc-clustering`  
**Current HEAD**: `7ddbe8301b8d27c94f388c40acbc88b0dee82723`  
**Audit Component**: Phase 7 — Structural Dependency Analysis and Remediation Scheduling  

---

## 1. Remediation Workflow Overview

The critical findings identified in the audit cannot be remediated in isolation. Mathematical and experimental dependencies dictate a strict order of operations:

1. **Pre-requisite (Git History & Confidentiality)**: Purging sensitive historical commits and PR refs must occur before freezing the codebase for publication.
2. **Phase 2A (Statistical Framing & Core Algorithms)**: Conformal prediction framing, AutoK inner-product repair, and Knockoff exchangeability fixes must occur prior to re-running experiments.
3. **Phase 2B (Data Generator & Leakage Fixes)**: The synthetic seed fix (`make_signal` seed propagation) must be implemented before any synthetic benchmarks are re-executed.
4. **Phase 3 (Benchmarking & Packaging)**: Full factorial benchmarks and wheel packaging tests can only execute after algorithmic and generator repairs are complete.
5. **Phase 4 (Manuscript & Documentation)**: Manuscript tables, text, figures, and macros in `main.tex` and `numbers.tex` are finalized using the verified artifacts from Phase 3.

---

## 2. Mermaid Directed Dependency Graph

```mermaid
flowchart TD
    subgraph Phase1["Phase 1: Confidentiality & Safety"]
        FND01["FND-01: Git History Rewrite & PR Purge"]
    end

    subgraph Phase2A["Phase 2A: Algorithmic & Statistical Repair"]
        FND02["FND-02: Conformal Clinical Reframing & Disclaimers"]
        FND03["FND-03: AutoK Inner-Product & PAC Threshold Repair"]
        FND04["FND-04: Knockoff Exchangeability Fix & Dead Code Removal"]
    end

    subgraph Phase2B["Phase 2B: Synthetic Data Generator Repair"]
        FND05["FND-05: Synthetic Seed Propagation (make_signal)"]
    end

    subgraph Phase3["Phase 3: Verification, Benchmarking & Packaging"]
        FND07["FND-07: Wheel Packaging & CLI Consolidation"]
        BENCH_SYNTH["Re-run Synthetic High-Dimensional Benchmarks"]
        BENCH_REAL["Re-run 13 Multi-Domain Biomedical Benchmarks"]
        FND06["FND-06: Accurate Baseline Speedup & Timing Reconciliation"]
        FND08["FND-08: Anchor Factorial Ablation (O(NL) Re-framing)"]
    end

    subgraph Phase4["Phase 4: Manuscript & Macro Alignment"]
        UPDATE_NUMBERS["Update numbers.tex Macro Definitions"]
        REVISE_TEXT["Revise main.tex (Sections 4.2, 5.3, 7)"]
        VERIFY_ARTIFACTS["Archive Immutable Raw Data Artifacts (Zenodo/DOI)"]
        FINAL_GATE["Final Submission Decision Gate (GO / NO-GO)"]
    end

    %% Dependencies
    FND01 --> FINAL_GATE
    
    FND02 --> REVISE_TEXT
    FND03 --> BENCH_SYNTH
    FND04 --> BENCH_REAL
    
    FND05 --> BENCH_SYNTH
    
    BENCH_SYNTH --> FND06
    BENCH_REAL --> FND08
    
    FND06 --> UPDATE_NUMBERS
    FND08 --> UPDATE_NUMBERS
    
    FND07 --> FINAL_GATE
    
    UPDATE_NUMBERS --> REVISE_TEXT
    REVISE_TEXT --> VERIFY_ARTIFACTS
    VERIFY_ARTIFACTS --> FINAL_GATE
```

---

## 3. Critical Path Analysis

The critical path for remediation comprises:

$$\text{FND-05 (Seed Fix)} \longrightarrow \text{FND-03 (AutoK Fix)} \longrightarrow \text{Synthetic & Real Benchmarks} \longrightarrow \text{FND-06 / FND-08 Reconciliation} \longrightarrow \text{numbers.tex Update} \longrightarrow \text{main.tex Alignment} \longrightarrow \text{Final Gate}$$

Any delay in resolving the core algorithmic bugs (AutoK $L_1$ concentration or synthetic seed freezing) will block the downstream benchmark suite and invalidate subsequent manuscript revisions.
