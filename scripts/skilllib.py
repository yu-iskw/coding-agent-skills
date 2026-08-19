#!/usr/bin/env python3
"""Small standard-library helpers for repository skill tooling."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: missing YAML frontmatter")

    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError(f"{path}: unterminated YAML frontmatter") from exc

    result: dict[str, object] = {}
    section: str | None = None
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  ") and section:
            key, sep, value = raw.strip().partition(":")
            if sep:
                mapping = result.setdefault(section, {})
                if isinstance(mapping, dict):
                    mapping[key.strip()] = _unquote(value)
            continue

        key, sep, value = raw.partition(":")
        if not sep:
            continue
        key = key.strip()
        value = value.strip()
        if value:
            result[key] = _unquote(value)
            section = None
        else:
            result[key] = {}
            section = key

    return result


def discover_skills() -> list[tuple[Path, dict[str, object]]]:
    skills: list[tuple[Path, dict[str, object]]] = []
    for skill_file in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        skills.append((skill_file.parent, parse_frontmatter(skill_file)))
    return skills
