#!/usr/bin/env python3
"""Validate repository-specific quality contracts beyond Agent Skills syntax."""

from __future__ import annotations

import json
from pathlib import Path

from skilllib import ROOT, discover_skills

REQUIRED_METADATA = {"maturity", "risk", "category", "network", "side-effects"}
MATURITY = {"experimental", "beta", "stable"}
RISKS = {"R0", "R1", "R2", "R3", "R4"}


def main() -> int:
    errors: list[str] = []
    names: set[str] = set()
    skills = discover_skills()

    for directory, frontmatter in skills:
        name = str(frontmatter.get("name", ""))
        description = str(frontmatter.get("description", ""))
        metadata = frontmatter.get("metadata", {})

        if not name:
            errors.append(f"{directory}: missing name")
        elif name in names:
            errors.append(f"{directory}: duplicate skill name {name}")
        else:
            names.add(name)
        if len(description) < 30:
            errors.append(f"{directory}: description is too short for reliable routing")
        if not isinstance(metadata, dict):
            errors.append(f"{directory}: metadata must be a mapping")
            continue

        missing = REQUIRED_METADATA - set(metadata)
        if missing:
            errors.append(f"{directory}: missing metadata: {', '.join(sorted(missing))}")
        if metadata.get("maturity") not in MATURITY:
            errors.append(f"{directory}: invalid maturity {metadata.get('maturity')!r}")
        if metadata.get("risk") not in RISKS:
            errors.append(f"{directory}: invalid risk {metadata.get('risk')!r}")
        if metadata.get("network") not in {"true", "false"}:
            errors.append(f"{directory}: network must be quoted true/false")

    manifest_path = ROOT / "evals" / "manifest.json"
    if not manifest_path.exists():
        errors.append("evals/manifest.json is required")
    else:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        entries = {entry.get("name"): entry for entry in manifest.get("skills", [])}
        missing_evals = names - set(entries)
        extra_evals = set(entries) - names
        if missing_evals:
            errors.append(f"missing eval fixtures: {', '.join(sorted(missing_evals))}")
        if extra_evals:
            errors.append(f"eval fixtures reference missing skills: {', '.join(sorted(extra_evals))}")
        for name, entry in entries.items():
            routing = entry.get("routing", {})
            behavior = entry.get("behavior", {})
            if len(routing.get("positive", [])) < 2:
                errors.append(f"{name}: needs at least two positive routing cases")
            if len(routing.get("negative", [])) < 2:
                errors.append(f"{name}: needs at least two negative routing cases")
            if not behavior.get("required"):
                errors.append(f"{name}: needs required behavior assertions")
            if not behavior.get("prohibited"):
                errors.append(f"{name}: needs prohibited behavior assertions")

    if errors:
        print("Skill contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated quality contracts for {len(skills)} canonical skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
