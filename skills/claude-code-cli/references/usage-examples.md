# Usage Examples for claude-code-cli

This reference provides concrete examples of how to apply the permission tiers when using the `claude` CLI through this skill.

## Tier 0: Analysis & Research (Mode: `plan`)

**Intent**: "Summarize the architecture of this project."
**Logic**: No changes or commands needed. Safe read-only analysis.
**Command**:

```bash
claude -p "Summarize the project architecture in README.md and the directory structure." --permission-mode plan
```

**Intent**: "Research the current state of Model Context Protocol (MCP) in early 2026."
**Logic**: Requires live web search but no file system changes.
**Command**:

```bash
claude -p "What is the current version and main features of MCP as of February 2026?" --permission-mode plan
```

## Tier 1: Workspace Modification (Mode: `acceptEdits`)

**Intent**: "Fix all typos in the documentation files."
**Logic**: Modifies files automatically but does not run external tools without prompt.
**Approval Required**: Yes.
**Command**:

```bash
claude -p "Find and fix spelling and grammar errors in all .md files in the docs/ directory." --permission-mode acceptEdits
```

## Tier 2: Autonomous Execution (Mode: `bypassPermissions`)

**Intent**: "Update dependencies and ensure the build still passes."
**Logic**: Modifies files AND executes build/test commands without interruption.
**Approval Required**: Yes (High Risk).
**Command**:

```bash
claude -p "Update all dependencies to their latest compatible versions and run 'make build' to verify." --permission-mode bypassPermissions
```

**Intent**: "Identify and fix the failing unit test in tests/test_api.py."
**Logic**: Needs to run tests to identify the failure and then edit the code to fix it autonomously.
**Approval Required**: Yes (High Risk).
**Command**:

```bash
claude -p "Run tests/test_api.py, analyze the failure, and fix the underlying issue." --permission-mode bypassPermissions
```
