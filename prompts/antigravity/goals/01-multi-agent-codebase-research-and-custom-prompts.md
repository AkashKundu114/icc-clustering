# Goal: Multi-Subagent Codebase Deep Dive & Custom Prompt Generator

Use this prompt to perform an exhaustive, multi-perspective examination of a target codebase and generate ready-to-run, custom execution prompts.

---

## 1. Multi-Subagent Research Protocol

Launch or assume the following subagent personas to analyze the repository concurrently:

### Subagent A: Symbol & Architecture Researcher (`roo_ask`)
- **Action:** Traverse all source trees (`src/`, `lib/`, `app/`).
- **Target Outputs:**
  - Complete list of exported classes, public functions, and data schemas.
  - Identification of coupling hot-spots, cyclic imports, or god classes.
  - Runtime dependency graph and environmental prerequisites.

### Subagent B: Test & Quality Auditor (`roo_debugger`)
- **Action:** Inspect test configurations (`pytest.ini`, `pyproject.toml`, `tests/`).
- **Target Outputs:**
  - Execute full test suite: capture exact pass/fail counts, execution time, and warnings.
  - Execute static analysis: `ruff check .`, `mypy --strict .` (or framework equivalent).
  - Identify untested modules or mock implementations masking real behavior.

### Subagent C: Security & Boundary Inspector (`roo_reviewer`)
- **Action:** Audit `.gitignore`, environment files, file trees, and input parsers.
- **Target Outputs:**
  - Scan for accidental credential exposure, private API keys, or embedded tokens.
  - Audit `.gitignore` completeness against heavy datasets, models, and build products.
  - Verify untrusted input sanitation across network endpoints or file deserializers.

---

## 2. Custom Prompt Synthesis Template

Collate the findings from Subagents A, B, and C into tailored, high-fidelity prompts for this specific repository. Use the following structure for each synthesized prompt:

```markdown
### [Custom Prompt for: <Subsystem/Module Name>]
- **Context & Motivation:** <Describe the exact observed issue with file and line citations>
- **Target Files:**
  - `<file_path_1>#L<start>-L<end>`
  - `<file_path_2>`
- **Assigned Persona:** `roo_coder` (Implementation) / `roo_debugger` (Testing) / `roo_reviewer` (Audit)
- **Concrete Task Instructions:**
  1. <Step-by-step technical instructions using specific method/class names>
  2. <Preserve invariants, avoid collateral refactors>
- **Acceptance Criteria & Verification:**
  - Run: `<exact_test_command>` (Must exit 0 with 0 regressions)
  - Run: `<exact_lint_command>` (Must pass cleanly)
- **Safety Boundary:** <Specify files and interfaces that must remain strictly unchanged>
```

---

## 3. Implementation Plan Output
Assemble the custom prompts into an ordered, chronological **Implementation Plan**:
1. **Phase 1: Foundation & High-Priority Fixes** (Defects breaking tests, type safety, or security).
2. **Phase 2: Core Feature / Research Implementation** (Subsystem changes advancing the primary objective).
3. **Phase 3: Integration, Performance & End-to-End Testing** (Full regression suite and scale testing).
4. **Phase 4: Documentation & Release Packaging** (READMEs, API docs, and release gates).

Every phase must end with an automated verification checkpoint.
