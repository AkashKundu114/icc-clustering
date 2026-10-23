# Security Policy

## Supported Versions

The following table lists the security support status for versions of the **Inductive Consensus Clustering (ICC)** framework:

| Version | Supported          | Security Status                                         |
| ------- | ------------------ | ------------------------------------------------------- |
| 2.1.x   | :white_check_mark: | Current active release (Springer Nature DAMI Baseline)  |
| 2.0.x   | :white_check_mark: | Previous release baseline                               |
| 1.0.x   | :x:                | Deprecated (v1 anchor-only prototype)                   |
| < 1.0   | :x:                | Unsupported                                             |

---

## Reporting a Vulnerability

We prioritize the security and integrity of our research software. If you identify a security vulnerability, data leakage vector, arbitrary code execution risk, or potential exploit in ICC-v2 (including in custom dataset loaders, baseline evaluation routines, or serialization pipelines), please report it responsibly.

### How to Report Privately

**Please do not open a public GitHub issue for security vulnerabilities.**

Instead, please send an encrypted or direct email to the maintainer:
* **Primary Contact**: Akash Kundu
* **Academic Email**: `akash231001001449@technoindiaeducation.com`
* **Personal Email**: `akashkundu11522@gmail.com`

### What to Include in Your Report

To help us investigate and triage the issue swiftly, please include:
1. **Type of issue**: (e.g., untrusted deserialization, arbitrary file overwrite in caching, dependency vulnerability, memory exhaustion / denial of service).
2. **Location**: Specific source file(s) and function names (e.g., `src/icc/datasets/registry.py`).
3. **Proof of Concept (PoC)**: Minimal reproducing script or steps to trigger the behavior.
4. **Impact Assessment**: Estimated severity and potential consequences for users or automated evaluation pipelines.

---

## Response & Disclosure Process

* **Acknowledgment**: We aim to acknowledge receipt of security reports within **48 hours**.
* **Investigation & Assessment**: We will investigate, verify the issue, and provide an initial assessment within **5 business days**.
* **Remediation**: Once verified, a patch will be prepared, tested, and released as a patch update (`v2.0.x`).
* **Coordinated Disclosure**: We adhere to coordinated vulnerability disclosure. A public security advisory and changelog credit will be published after the fix has been tagged and deployed.

---

## Security Best Practices for Users

* **Untrusted Datasets**: Always verify checksums and sources when downloading third-party scientific datasets or pre-computed embeddings.
* **Virtual Environments**: Run experiments in an isolated virtual environment (`python -m venv venv`) or containerized runner.
* **Dependencies**: Regularly update packages to receive security patches via `pip audit` or Dependabot.
