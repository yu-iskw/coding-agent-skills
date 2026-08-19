#!/usr/bin/env python3
"""Deterministic static checks for common malicious skill supply-chain patterns."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from skilllib import ROOT, SKILLS_DIR

TEXT_SUFFIXES = {".md", ".txt", ".sh", ".py", ".js", ".ts", ".json", ".yaml", ".yml", ".toml"}
EXECUTABLE_SUFFIXES = {".sh", ".py", ".js", ".ts"}
PATTERNS = [
    ("critical", "remote-pipe-shell", re.compile(r"(?:curl|wget)[^\n|]*\|\s*(?:ba)?sh\b", re.I)),
    ("critical", "decoded-payload-exec", re.compile(r"base64\s+(?:--decode|-d)[^\n|]*\|\s*(?:ba)?sh\b", re.I)),
    ("critical", "private-key-read", re.compile(r"(?:cat|read|open)\s+[^\n]*(?:\.ssh/(?:id_|config)|\.aws/credentials|application_default_credentials\.json)", re.I)),
    ("warning", "destructive-root-delete", re.compile(r"rm\s+-rf\s+(?:/|~|\$HOME)(?:\s|$)", re.I)),
    ("warning", "approval-bypass", re.compile(r"dangerously-bypass|bypassPermissions", re.I)),
    ("warning", "external-upload", re.compile(r"(?:curl|wget)[^\n]*(?:--data|-d|--upload-file|-T)\b", re.I)),
]


def scan() -> dict[str, object]:
    findings: list[dict[str, object]] = []
    scanned = 0
    for path in sorted(SKILLS_DIR.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for severity, rule, pattern in PATTERNS:
                if not pattern.search(line):
                    continue
                effective_severity = severity
                if severity == "critical" and path.suffix.lower() not in EXECUTABLE_SUFFIXES:
                    effective_severity = "warning"
                findings.append(
                    {
                        "severity": effective_severity,
                        "rule": rule,
                        "path": str(path.relative_to(ROOT)),
                        "line": line_number,
                    }
                )
    return {
        "schema_version": 1,
        "scanned_files": scanned,
        "findings": findings,
        "critical_count": sum(f["severity"] == "critical" for f in findings),
        "warning_count": sum(f["severity"] == "warning" for f in findings),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path, help="compare deterministic report with a committed file")
    args = parser.parse_args()

    report = scan()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    if args.check:
        if not args.check.exists() or args.check.read_text(encoding="utf-8") != rendered:
            print(f"Security report is stale: regenerate {args.check}")
            return 1

    print(rendered, end="")
    return 1 if report["critical_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
