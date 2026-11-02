"""Validate public dataset rights metadata and software release identifiers.

Run from any directory with: python scripts/validate_registry_and_release_metadata.py
This checks document consistency only; it is not a license determination.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib

import yaml

ROOT = Path(__file__).resolve().parents[1]
RIGHTS_FIELDS = {
    "name", "upstream_source", "upstream_url", "license", "license_evidence",
    "license_evidence_status", "license_evidence_url", "redistribution_status",
    "derivative_redistribution_status", "attribution", "rights_notes",
}
RIGHTS = {"VERIFIED", "UNKNOWN", "UNVERIFIED", "REDISTRIBUTION_NOT_CLEARED", "RESTRICTED"}
EVIDENCE = {"VERIFIED_SOURCE_TERMS", "PARTIAL", "UNKNOWN", "UNVERIFIED"}


def fail(errors: list[str]) -> int:
    if errors:
        print("FAILED")
        print("\n".join(f"- {item}" for item in errors))
        return 1
    print("PASS: dataset registry, runtime dimensions, and release identifiers are consistent")
    print("This is a structural metadata check, not legal clearance or DOI verification.")
    return 0


def main() -> int:
    errors: list[str] = []
    registry = yaml.safe_load((ROOT / "data/registry.yaml").read_text(encoding="utf-8"))
    runtime = yaml.safe_load((ROOT / "configs/datasets.yaml").read_text(encoding="utf-8"))
    rows = registry.get("datasets", {})
    configs = runtime.get("datasets", {})
    if len(rows) != 13 or set(rows) != set(configs):
        errors.append(f"Expected matching 13-dataset registries; found public={len(rows)}, runtime={len(configs)}")
    for key, row in rows.items():
        if not isinstance(row, dict):
            errors.append(f"{key}: expected a mapping")
            continue
        for field in sorted(RIGHTS_FIELDS - row.keys()):
            errors.append(f"{key}: missing rights field {field}")
        if row.get("redistribution_status") not in RIGHTS:
            errors.append(f"{key}: invalid redistribution status")
        if row.get("derivative_redistribution_status") not in RIGHTS:
            errors.append(f"{key}: invalid derivative redistribution status")
        if row.get("license_evidence_status") not in EVIDENCE:
            errors.append(f"{key}: invalid license evidence status")
        for field in ("upstream_url", "license_evidence_url"):
            if not str(row.get(field, "")).startswith(("https://", "http://")):
                errors.append(f"{key}: {field} must identify an evidence/access URL")
        if key in configs:
            cfg = configs[key]
            for a, b in (("n_samples", "expected_N"), ("n_features", "expected_D"), ("n_clusters", "expected_K")):
                if row.get(a) != cfg.get(b):
                    errors.append(f"{key}: {a}={row.get(a)!r} disagrees with {b}={cfg.get(b)!r}")

    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8")).get("project", {})
    project_name = project.get("name")
    project_version = project.get("version")
    runtime_version = re.search(r'^__version__\s*=\s*["\']([^"\']+)', (ROOT / "src/icc/__init__.py").read_text(encoding="utf-8"), re.M)
    cff = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    zenodo = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    versions = {
        "pyproject": str(project_version) if project_version else None,
        "runtime": runtime_version.group(1) if runtime_version else None,
        "CITATION.cff": str(cff.get("version")),
        ".zenodo.json": str(zenodo.get("version")),
    }
    if project_name != "icc-clustering":
        errors.append("pyproject distribution name must be icc-clustering (import package remains icc)")
    if len(set(versions.values())) != 1 or None in versions.values():
        errors.append(f"version metadata mismatch: {versions}")
    if zenodo.get("upload_type") != "software" or zenodo.get("license") != "MIT":
        errors.append("Zenodo draft must identify software and the project MIT license")
    creators = [item.get("name") for item in zenodo.get("creators", [])]
    cff_authors = [" ".join(filter(None, [item.get("given-names"), item.get("family-names")])) for item in cff.get("authors", [])]
    project_authors = [item.get("name") for item in project.get("authors", [])]
    if creators != cff_authors or project_authors != cff_authors:
        errors.append("Zenodo creators, CITATION.cff authors, and pyproject authors disagree")
    if not (ROOT / "CHANGELOG.md").read_text(encoding="utf-8").startswith("# Changelog"):
        errors.append("CHANGELOG.md could not be read")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    first_heading = next((line for line in changelog.splitlines() if line.startswith("## ")), "")
    if first_heading.startswith("## [Unreleased]"):
        if project_version not in first_heading:
            errors.append("Unreleased changelog section should identify the candidate project version")
    elif not first_heading.startswith(f"## [{project_version}]"):
        errors.append(f"Top changelog section must match project version {project_version}")
    return fail(errors)


if __name__ == "__main__":
    sys.exit(main())
