# Artificial Intelligence Disclosure Options (Human Gate B)

**Document Reference:** `LOOP/DISCLOSURE_OPTIONS.md`  
**Date:** 2026-10-21  
**Status:** APPROVED BY HUMAN AUTHOR (GATE B) - OPTION B SELECTED
**Decision Date:** 2026-10-21

---

## 1. Springer Nature Editorial Policy on Generative AI

From the official Springer Nature Policy on AI Authorship & Declarations:
> **1. Authorship Criteria:** Large Language Models (LLMs) and generative AI technologies do not satisfy the criteria for authorship because they cannot take legal, ethical, or scientific responsibility for the submitted work. Accountability for the integrity and accuracy of the scholarly work remains strictly with human authors.
> 
> **2. Transparency & Disclosure:** Authors who use generative AI tools to assist in creating, writing, structuring, or coding any part of the manuscript must provide a transparent declaration within the manuscript (e.g., in the Declarations or Methods section). The disclosure must explicitly state:
>   - The name of the AI tool and model version used.
>   - The specific tasks performed by the tool.
>   - Confirmation that the human authors have reviewed, verified, and take full responsibility for the contents.

---

## 2. Documented Evidence from Repository and Execution Logs

Based on the Git commit history and execution run logs (`LOOP/DECISIONS.md`, `LOOP/STATE.json`, `LOOP/dev/`, `experiments/`):
- **Tools Used:** Google Antigravity / Claude / Gemini Agentic Coding System (incorporating CodeRabbit CLI, Python 3.14/3.10+ execution engines, and Tectonic LaTeX compilation).
- **Tasks Performed by the AI Agent:**
  1. Automated execution of benchmark reproduction runs, synthetic falsification experiments, and scaling evaluations.
  2. Data parsing and automated extraction of empirical performance metrics into LaTeX macros (`numbers.tex`).
  3. Code refactoring, test generation, and static typing compliance (`py.typed`, `mypy -p icc`).
  4. Drafting, structural restructuring, and stylistic revision of LaTeX text in `springer_manuscript/main.tex`.
  5. Compilation troubleshooting, BibTeX reference verification, and Nemenyi critical difference diagram rendering.
- **Human Author Role:**
  - Conceptualization of research hypotheses, mathematical formulation of BGSS and bipartite determinacy consensus, selection of benchmark datasets, and final approval of all text, tables, and claims.

---

## 3. The Three Factual Options for Human Author Selection

The human author (Akash Kundu) must select one of the following three options:

### Option A: Minimal Grammar & Language Editing
> *"Use of Artificial Intelligence Disclosure: During the preparation of this work, the authors used an AI coding assistant solely for code optimization, automated grammar checks, and LaTeX formatting. All research hypotheses, mathematical formulations, experimental analyses, and interpretations were conceived, drafted, and verified exclusively by the authors."*
> 
> **Note:** Select this option if you consider the AI's role strictly auxiliary (polishing and code formatting) without substantive generative input on the core prose.

### Option B: AI-Assisted Research Workflow & Drafting with Human Verification (Recommended)
> *"Use of Artificial Intelligence Disclosure: During the preparation of this manuscript and codebase, the authors utilized an agentic AI coding assistant (Google Antigravity / Claude / Gemini) to assist with automated execution of benchmark scripts, data extraction into LaTeX macro registries, code refactoring, and iterative drafting and proofreading of the manuscript text. The conceptual framework, experimental design, theoretical proofs, and data analysis were formulated and directed by the authors. The authors have reviewed, audited, and verified all text, tables, figures, and code, and take full responsibility for the scientific integrity and reproducibility of this work."*
> 
> **Note:** This option is the most transparent and factually aligned with the comprehensive automated loop logs, satisfying Springer Nature's policy without ambiguity.

### Option C: Custom Text Specified by Authors
> The author provides their own custom text here:
> `[ENTER CUSTOM TEXT]`

---

## 4. Current Status in Manuscript
In `springer_manuscript/main.tex` (Line 547), the declaration currently contains a provisional statement. Once the author selects Option A, B, or C, line 547 will be updated with the exact wording chosen.
