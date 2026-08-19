#!/usr/bin/env python3
"""Generate deterministic human- and machine-readable skill discovery surfaces."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from skilllib import ROOT, discover_skills


def build_outputs() -> dict[Path, str]:
    entries: list[dict[str, object]] = []
    for directory, frontmatter in discover_skills():
        metadata = frontmatter.get("metadata", {})
        entries.append(
            {
                "name": frontmatter.get("name"),
                "description": frontmatter.get("description"),
                "path": str(directory.relative_to(ROOT)),
                "license": frontmatter.get("license", "Apache-2.0"),
                "compatibility": frontmatter.get("compatibility", "Agent Skills compatible hosts"),
                "metadata": metadata,
            }
        )

    catalog = {
        "schema_version": 1,
        "repository": "yu-iskw/coding-agent-skills",
        "skills": entries,
    }
    catalog_text = json.dumps(catalog, indent=2, sort_keys=True) + "\n"

    llms_lines = [
        "# Coding Agent Skills",
        "",
        "Verified, portable engineering skills for agent-ready repositories.",
        "",
        "## Skills",
        "",
    ]
    for entry in entries:
        metadata = entry["metadata"] if isinstance(entry["metadata"], dict) else {}
        llms_lines.append(
            f"- {entry['name']}: {entry['description']} "
            f"[risk={metadata.get('risk', 'unknown')}; category={metadata.get('category', 'unknown')}; path={entry['path']}]"
        )
    llms_text = "\n".join(llms_lines) + "\n"

    compatibility_lines = [
        "# Compatibility",
        "",
        "The canonical artifacts are standard `SKILL.md` packages. This matrix describes packaging/discovery evidence; it is not a claim that every model/host version has passed behavioral evaluation.",
        "",
        "| Surface | Status | Notes |",
        "| --- | --- | --- |",
        "| Agent Skills specification | Canonical | `skills/*/SKILL.md` is the source of truth. |",
        "| Claude Code plugin | Packaged | `.claude-plugin` points at the canonical `skills/` directory. |",
        "| Codex plugin | Packaged | `.codex-plugin` points at the canonical `skills/` directory. |",
        "| Cursor | Compatible collection | Repository also carries maintainer-only Cursor skills under `.cursor/skills/`; canonical product skills stay under `skills/`. |",
        "| Pi | Compatible collection | Pi can discover Agent Skills from standard locations. |",
        "| fx | Compatible collection | fx can install/discover Agent Skills and also has a delegation adapter in this collection. |",
        "| GitHub Copilot / other Agent Skills hosts | Format-compatible | Behavioral evidence should be recorded per host/model/version using the eval harness. |",
        "",
        "## Evidence model",
        "",
        "- **Conformance:** deterministic Agent Skills syntax validation.",
        "- **Safety:** deterministic static security findings and declared R0-R4 capability metadata.",
        "- **Behavior:** observations scored against `evals/manifest.json`; results are evidence for a particular host/model/version, not certification.",
        "",
    ]
    compatibility_text = "\n".join(compatibility_lines)

    return {
        ROOT / "catalog" / "catalog.json": catalog_text,
        ROOT / "llms.txt": llms_text,
        ROOT / "docs" / "compatibility.md": compatibility_text,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    stale: list[str] = []
    for path, content in build_outputs().items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            print(f"wrote {path.relative_to(ROOT)}")

    if stale:
        print("Generated catalog files are stale:")
        for path in stale:
            print(f"- {path}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
