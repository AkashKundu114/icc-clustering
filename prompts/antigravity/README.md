# Antigravity Multi-Subagent Prompt Library

This directory provides a structured protocol for autonomous and pair-programming AI coding agents. It enforces a strict **Deep Dive Research $\rightarrow$ Custom Prompt Synthesis $\rightarrow$ Implementation Plan Execution** workflow using specialized subagents.

---

## The Canonical Multi-Subagent Workflow

When approaching any repository (new or existing), coding agents must not make ad-hoc edits. Agents must strictly follow this three-phase lifecycle:

```text
┌────────────────────────────────────────────────────────┐
│ Phase 1: Multi-Subagent Codebase Deep Dive             │
│ • Researcher Subagents map symbols, modules, & flows   │
│ • Auditor Subagent runs baseline tests & static checks │
│ • Architect Subagent identifies gaps & boundaries      │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ Phase 2: Custom Prompt Synthesis                       │
│ • Distill findings into repo-tailored prompt specs     │
│ • Bind exact file paths, symbols, metrics, & commands  │
│ • Establish unambiguous acceptance criteria            │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ Phase 3: Phased Implementation Plan Execution          │
│ • Formulate structured Implementation Plan             │
│ • Dispatch Coder Subagents for surgical edits          │
│ • Run Debugger & Reviewer Subagents at every gate     │
│ • Record outcomes in iteration logs & final report     │
└────────────────────────────────────────────────────────┘
```

---

## Specialized Subagent Roles

When orchestrating subagents (`invoke_subagent` or persona adoption), assign distinct responsibilities:

1. **Codebase Researcher (`research` / `roo_ask`)**: Read-only exploration. Traces call trees, symbol hierarchies, entrypoints, and test coverage across the entire project before any code is modified.
2. **System Architect (`roo_architect`)**: Reviews overall module boundaries, design patterns, schema contracts, and algorithmic invariants.
3. **Quality & Security Auditor (`roo_reviewer`)**: Dissects static analysis baselines (`ruff`, `mypy`), audits test suites (`pytest`), scans for secrets/credentials, and inspects data leakage boundaries.
4. **Engineer / Implementation Specialist (`roo_coder`)**: Performs surgical, minimal code edits implementing one approved phase of the plan at a time.
5. **Debugger / Verification Gate (`roo_debugger`)**: Isolates stack traces, inspects runtime regressions, and verifies acceptance criteria.

---

## Directory Organization

### Goals (`goals/`)
Define what outcomes the agent team should pursue:
- `00-repository-baseline-and-plan.md`: Mandatory entrypoint. Conducts the multi-subagent deep dive, synthesizes custom prompts, and builds the implementation plan.
- `01-multi-agent-codebase-research-and-custom-prompts.md`: Dedicated protocol for performing a 360-degree deep dive and compiling repo-specific prompt suites.
- `02-hypothesis-and-claim-matrix-audit.md`: Formal verification of mathematical assertions, propositions, and claim-to-evidence links.
- `10-code-quality-and-maintainability.md`: Code modularity, refactoring, typing, and lint standards.
- `15-test-suite-expansion-and-edge-cases.md`: Adversarial testing, degenerate geometries, and boundary stress tests.
- `20-security-privacy-and-prompt-injection.md`: Secret detection, untrusted input boundaries, and privacy audits.
- `25-data-pipeline-and-leakage-audit.md`: Data split hygiene, transformer fitting, and dataset immutability.
- `30-performance-and-resource-efficiency.md`: Computational bottlenecks, memory footprint, and asymptotic scaling.
- `35-gpu-acceleration-and-memory-profiling.md`: GPU VRAM tracking, PyTorch tensor acceleration, and Numba JIT kernels.
- `40-research-reproducibility-and-paper-audit.md`: Single-source metric traceability and reproducibility audits.
- `45-manuscript-and-typesetting-audit.md`: Camera-ready LaTeX typography, overfull box remediation, and BibTeX validation.
- `50-production-readiness-and-documentation.md`: Release packaging, CI/CD validation, and deployment readiness.
- `60-baseline-fairness-and-benchmarking-parity.md`: Non-parametric statistical tests (Friedman/Nemenyi) and baseline parity.

### Loops (`loops/`)
Define bounded, test-driven repeat workflows:
- `01-bounded-improvement-loop.md`: Standard bounded execution loop (max 5 iterations per run) driven by the synthesized implementation plan.
- `02-research-reproducibility-loop.md`: Rigorous audit loop for scientific data integrity and claim verification.
- `03-regression-and-release-gate.md`: Final release verification gate before git tagging or publishing.
- `04-red-team-adversarial-audit-loop.md`: Attacker/defender subagent loop stress-testing edge cases and numerical singularities.
- `05-ablation-and-hypotheses-verification-loop.md`: Systematic module ablation and hypothesis testing loop with statistical significance tests.
- `06-performance-profiling-and-optimization-loop.md`: cProfile/tracemalloc profiling and numerical equivalence verification loop.
- `07-manuscript-macro-sync-and-typesetting-loop.md`: PDF compilation, numbers macro synchronization, and overfull box resolution loop.
- `08-data-integrity-and-leakage-detection-loop.md`: Cross-validation split isolation and unsupervised label boundary loop.

### Custom Prompts (`custom_prompts/`)
Ready-to-run, actionable prompts targeting concrete technical tasks:
- `01-fix-type-annotations-and-imports.md`: Strict static typing (`mypy`) and import formatting (`ruff`).
- `02-audit-unverified-citations-and-bibtex.md`: Cross-checking citations and resolving missing bibliography items.
- `03-verify-single-source-numbers.md`: Binding manuscript values directly to `numbers.tex` and `results.json`.
- `04-stress-test-adversarial-inputs.md`: Writing parameterized unit tests for NaN, zero-variance, and rank-deficient inputs.
- `05-data-split-leakage-check.md`: Verifying train/test preprocessing isolation.

### Templates (`templates/`) & Logs (`logs/`)
- `templates/iteration-log.md`: Standardized record for each iteration step.
- `templates/final-report.md`: Structured report delivered upon plan completion.
- `logs/`: Directory for local iteration logs (never commit secrets or sensitive data here).
