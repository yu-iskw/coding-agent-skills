# Usage Examples for claude-code-cli

This reference provides concrete examples of how to apply the permission tiers when using the `claude` CLI through this skill.

## Tier 0: Analysis & Research (Mode: `plan` + `--sandbox`)

**Intent**: "Summarize the architecture of this project."
**Logic**: No changes or commands needed. Safe read-only analysis with OS-level sandbox and shell blocked.
**Command**:

```bash
claude -p "Summarize the project architecture in README.md and the directory structure." \
  --permission-mode plan --sandbox --disallowedTools Bash
```

**Intent**: "Research the current state of Model Context Protocol (MCP) in early 2026."
**Logic**: Requires live web search but no file system changes.
**Command**:

```bash
claude -p "What is the current version and main features of MCP as of February 2026?" \
  --permission-mode plan --sandbox --disallowedTools Bash
```

## Tier 1: Workspace Modification (Mode: `acceptEdits` + `--sandbox`)

**Intent**: "Fix all typos in the documentation files."
**Logic**: Modifies files automatically; shell is gated behind prompts; OS-level sandbox isolates the process.
**Approval Required**: Yes.
**Command**:

```bash
claude -p "Find and fix spelling and grammar errors in all .md files in the docs/ directory." \
  --permission-mode acceptEdits --sandbox
```

## Tier 2: Autonomous Execution (Mode: `bypassPermissions`)

**Intent**: "Update dependencies and ensure the build still passes."
**Logic**: Modifies files AND executes build/test commands without interruption. `--sandbox` is omitted because shell commands must run freely; confine to a dedicated container or VM instead.
**Approval Required**: Yes (High Risk).
**Command**:

```bash
claude -p "Update all dependencies to their latest compatible versions and run 'make build' to verify." \
  --permission-mode bypassPermissions
```

**Intent**: "Identify and fix the failing unit test in tests/test_api.py."
**Logic**: Needs to run tests to identify the failure and then edit the code to fix it autonomously.
**Approval Required**: Yes (High Risk).
**Command**:

```bash
claude -p "Run tests/test_api.py, analyze the failure, and fix the underlying issue." \
  --permission-mode bypassPermissions
```

## Cloud Execution *(research preview)*

**Intent**: "Run a long database migration while I'm away."
**Logic**: Offloads the task to an Anthropic-managed VM so it continues even if the local machine is closed.
**Approval Required**: Yes (runs `--dangerously-skip-permissions` by default in cloud).

```bash
claude --remote "Run the database migration in scripts/migrate.py, execute the full test suite, and open a PR if all tests pass."
```

Monitor progress from `claude.ai/code` or with `/tasks` in any interactive session.

## Remote Control *(GA — Feb 2026)*

**Intent**: "Resume the same coding session from my phone."
**Logic**: Code stays on your local machine; Remote Control provides synchronized access from any device.

```bash
# From terminal: pull a web session back to the local CLI
claude --teleport

# Resume a specific session by ID
claude --teleport <session-id>
```

Open `claude.ai/code` on any device to start monitoring, then use `--teleport` to take back control from the terminal.
