# Usage Examples for codex-cli

This reference provides concrete examples of how to apply the permission tiers when using the `codex` CLI through this skill.

## Tier 0: Analysis & Research (Mode: `readonly`)

**Intent**: "Summarize the architecture of this project."
**Logic**: No changes or commands needed.
**Command**:

```bash
codex -q "Summarize the project architecture in README.md and the directory structure."
```

**Intent**: "Research the current state of Model Context Protocol (MCP) in early 2026."
**Logic**: Requires live web search but no file system changes.
**Command**:

```bash
codex -q "What is the current version and main features of MCP as of February 2026?"
```

## Tier 1: Workspace Modification (Mode: `editor`)

**Intent**: "Fix all typos in the documentation files."
**Logic**: Modifies files automatically but does not run external tools.
**Approval Required**: Yes.
**Command**:

```bash
codex --auto-edit "Find and fix spelling and grammar errors in all .md files in the docs/ directory."
```

## Tier 2: Sandbox Execution (Mode: `autonomous`)

**Intent**: "Update dependencies and ensure the build still passes."
**Logic**: Modifies files AND executes build commands in sandbox.
**Approval Required**: Yes.
**Command**:

```bash
codex --full-auto "Update all python dependencies to their latest compatible versions and run 'make build' to verify."
```

**Intent**: "Identify and fix the failing unit test in tests/test_api.py."
**Logic**: Needs to run tests to identify the failure and then edit the code to fix it.
**Approval Required**: Yes.
**Command**:

```bash
codex --full-auto "Run tests/test_api.py, analyze the failure, and fix the underlying issue."
```
