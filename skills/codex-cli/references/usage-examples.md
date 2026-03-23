# Usage Examples for codex-cli

This reference provides concrete examples of how to apply the permission tiers when using the `codex` CLI through this skill.

## Tier 0: Analysis & Research (Mode: `suggest` + `--sandbox read-only`)

**Intent**: "Summarize the architecture of this project."
**Logic**: No changes or commands needed. Read-only sandbox prevents any file writes.
**Command**:

```bash
codex --sandbox read-only -q "Summarize the project architecture in README.md and the directory structure."
```

**Intent**: "Research the current state of Model Context Protocol (MCP) in early 2026."
**Logic**: Requires live web search but no file system changes.
**Command**:

```bash
codex --sandbox read-only -q "What is the current version and main features of MCP as of early 2026?"
```

## Tier 1: Workspace Modification (Mode: `auto-edit` + `--sandbox workspace-write`)

**Intent**: "Fix all typos in the documentation files."
**Logic**: Modifies files automatically; writes confined to workspace; network disabled; shell commands still require approval.
**Approval Required**: Yes.
**Command**:

```bash
codex --sandbox workspace-write --auto-edit \
  "Find and fix spelling and grammar errors in all .md files in the docs/ directory."
```

## Tier 2: Sandbox Execution (Mode: `full-auto`)

**Intent**: "Update dependencies and ensure the build still passes."
**Logic**: Modifies files AND executes build commands. `--full-auto` implies `--sandbox workspace-write --ask-for-approval on-request` — shell commands still require user approval, network disabled.
**Approval Required**: Yes.
**Command**:

```bash
codex --full-auto "Update all python dependencies to their latest compatible versions and run 'make build' to verify."
# Equivalent: codex --sandbox workspace-write --ask-for-approval on-request "..."
```

**Intent**: "Identify and fix the failing unit test in tests/test_api.py."
**Logic**: Needs to run tests to identify the failure and then edit the code to fix it.
**Approval Required**: Yes.
**Command**:

```bash
codex --full-auto "Run tests/test_api.py, analyze the failure, and fix the underlying issue."
```

## Cloud Execution (`codex cloud`)

**Intent**: "Run a full migration and test suite without tying up my local machine."
**Logic**: Offloads the task to OpenAI cloud infrastructure; diffs are applied locally when complete.
**Approval Required**: Yes.

```bash
# Launch the task on OpenAI cloud
codex cloud "Run the database migration in scripts/migrate.py, execute the full test suite, and create a PR if tests pass."

# List and monitor running cloud tasks
codex cloud -l

# Apply resulting diffs to local workspace
codex cloud -a
```
