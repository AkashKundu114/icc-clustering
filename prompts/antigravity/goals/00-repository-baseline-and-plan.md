# Goal: Multi-Subagent Repository Deep Dive and Implementation Plan

You are reviewing this repository as a senior software architect and research collaborator.

## Mission
Before making any direct code modifications, deploy multiple specialized subagents to perform an exhaustive, 360-degree deep dive into the whole codebase, synthesize custom repository-tailored execution prompts, and construct an actionable implementation plan.

---

## Required Protocol

### Phase 1: Multi-Subagent Deep Dive
Do not guess or assume. Launch specialized subagents (or assume explicit subagent roles) to investigate distinct facets of the repository:

1. **Architecture & Symbol Research (Subagent: `Codebase Researcher` / `roo_ask`)**:
   - Map all repository entrypoints, CLI scripts, server hooks, and demo pipelines.
   - Trace full module dependencies (`src/`), class hierarchies, and data structures.
   - Document data flows: ingestion $\rightarrow$ preprocessing $\rightarrow$ execution $\rightarrow$ metric export $\rightarrow$ reporting.
   - Identify unused dead code, circular dependencies, or fragile monkey-patches.

2. **Quality, Typing & Test Suite Audit (Subagent: `Auditor` / `roo_debugger`)**:
   - Run safe, non-destructive baseline checks available in the environment (`pytest`, `mypy`, `ruff`, `flake8`).
   - Catalog failing tests, flaky fixtures, mock over-reliance, and uncovered code paths.
   - Check type compliance (`py.typed`, strict typing flags).

3. **Security, Privacy & Data Leakage Review (Subagent: `Security Auditor`)**:
   - Scan for hardcoded credentials, API keys, tokens, or private absolute paths.
   - Verify that untrusted inputs (model outputs, external URLs, retrieved docs) are sanitized.
   - Confirm raw benchmark datasets and cached binaries are strictly excluded from version control.

4. **Domain / Publication Integrity Review (Subagent: `Domain Specialist`)**:
   - If a research repository: verify that all quantitative claims and tables trace directly to frozen data registries or numbers files.
   - Verify that test/train evaluation boundaries prevent data leakage.

---

### Phase 2: Custom Prompt Synthesis
Synthesize the findings from Phase 1 into **custom, repository-tailored prompts**. Do not leave generic placeholders. Each custom prompt must include:
- **Exact File Targets:** Explicit file paths, class names, and line ranges.
- **Root Cause & Evidence:** Specific stack traces, linter codes, or behavioral discrepancies observed.
- **Precision Acceptance Criteria:** Unambiguous criteria that define when the task is done (e.g. `pytest tests/test_aspp.py passes with 0 warnings`, `mypy reports 0 errors`).
- **Safety Boundaries:** Concrete files that must remain untouched, backward compatibility requirements, and memory/compute budgets.

Save or present these custom prompts for the specific repository to guide execution.

---

### Phase 3: Implementation Plan Construction
Convert the custom prompts into a sequenced, prioritized **Implementation Plan**:
- **Phase Breakdown:** Group tasks into discrete, logically isolated phases (e.g., Phase 1: Core Bugfixes $\rightarrow$ Phase 2: Interface Modularity $\rightarrow$ Phase 3: Test Expansion $\rightarrow$ Phase 4: Docs & Release).
- **Subagent Assignment:** Designate which subagent persona executes each step (e.g. `roo_coder` for implementation, `roo_debugger` for test fixing, `roo_reviewer` for diff audit).
- **Verification Gates:** Specify the exact command that must exit 0 before proceeding to the next phase.

---

## Deliverables
1. **Repository Topology Map:** Comprehensive summary of modules, interfaces, and test coverage.
2. **Baseline Audit Results:** Exact test/lint/typing command outputs and failure inventory.
3. **Custom Repository Prompts:** Tailored execution prompts addressing prioritized findings.
4. **Structured Implementation Plan:** Phased execution roadmap with explicit verification gates.

## Constraints
- **Read-Only Baseline:** Make zero code changes during this discovery phase.
- **Zero Fabrication:** Never fabricate test outcomes, benchmark scores, or module capabilities.
- **Local Sandbox:** Do not access the internet, upload repo data, or run destructive commands without approval.
