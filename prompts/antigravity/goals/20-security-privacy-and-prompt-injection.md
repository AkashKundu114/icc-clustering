# Goal: Security, Privacy, and Prompt-Injection Review

Perform a defensive review of the repository and its user-facing workflows.

## Scope
Inspect trust boundaries, authentication/authorization, input validation, secrets handling, logging, file/path access, subprocesses, dependency risks, local service exposure, data retention, model/tool permissions, prompt injection, retrieval poisoning, and unsafe output handling.

## Method
- Trace untrusted inputs through the system into privileged actions.
- Verify controls by tests or safe local reproduction; do not exploit external systems.
- Use synthetic fixtures and redacted evidence.
- Do not copy secrets or personal data into findings.
- Do not upload code/data to external scanners without explicit approval.
- Do not disable protections as a workaround.

## Deliverables
- Findings with severity, evidence, exploit preconditions, impact, and remediation.
- Regression tests for confirmed issues.
- A retest result for each remediated finding.
- Explicitly state coverage gaps and untested assumptions.

## Stop conditions
Stop and ask if validation would require production access, real personal data, external targets, destructive behavior, or expanded permissions.
