# Usage Examples for gemini-cli

This reference provides concrete examples of how to apply the permission tiers when using the `gemini` CLI through this skill.

## Tier 0: Analysis & Research (Mode: `plan`)

**Intent**: "Summarize the architecture of this project."
**Logic**: No changes or commands needed. Safe read-only analysis.
**Command**:

```bash
gemini -p "Summarize the project architecture in README.md and the directory structure." --approval-mode plan --sandbox
```

**Intent**: "Research the current state of Model Context Protocol (MCP) in early 2026."
**Logic**: Requires live web search but no file system changes.
**Command**:

```bash
gemini -p "What is the current version and main features of MCP as of February 2026?" --approval-mode plan --sandbox
```

## Tier 1: Workspace Modification (Mode: `auto_edit`)

**Intent**: "Fix all typos in the documentation files."
**Logic**: Modifies files automatically but does not run external tools without prompt.
**Approval Required**: Yes.
**Command**:

```bash
gemini -p "Find and fix spelling and grammar errors in all .md files in the docs/ directory." --approval-mode auto_edit
```

## Tier 2: Autonomous Execution (Mode: `yolo`)

**Intent**: "Update dependencies and ensure the build still passes."
**Logic**: Modifies files AND executes build/test commands without interruption.
**Approval Required**: Yes (High Risk).
**Command**:

```bash
gemini -p "Update all dependencies to their latest compatible versions and run 'make build' to verify." --approval-mode yolo
```

**Intent**: "Identify and fix the failing unit test in tests/test_api.py."
**Logic**: Needs to run tests to identify the failure and then edit the code to fix it autonomously.
**Approval Required**: Yes (High Risk).
**Command**:

```bash
gemini -p "Run tests/test_api.py, analyze the failure, and fix the underlying issue." --approval-mode yolo
```
