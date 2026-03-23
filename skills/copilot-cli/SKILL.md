---
name: copilot-cli
description: Executes tasks using the GitHub Copilot CLI (`copilot`). Automatically determines the safest permission mode (plan, editor, or autopilot) based on the task type.
---

# executing-copilot

## Purpose

Use this skill to perform coding, research, or automation tasks using the `copilot` CLI. It maps requests to Copilot's native tool-permission flags to balance automation with security.

## Permission Tiers

| Tier  | Mode           | Flag(s)                  | Capability                                   | Approval Required   | Typical Tasks                             |
| :---- | :------------- | :----------------------- | :------------------------------------------- | :------------------ | :---------------------------------------- |
| **0** | `plan`         | _(none)_                 | Read-only analysis; prompts for every tool.  | **No**              | Code review, audits, research.            |
| **1** | `editor`       | `--allow-tool='write'`   | Auto-approves file edits; prompts for shell. | **Yes**             | Refactoring, documentation, lint fixes.   |
| **2** | `autopilot`    | `--allow-all-tools`      | Auto-approves ALL tools (edits + shell).     | **Yes (High Risk)** | CI/CD, complex builds, automated testing. |

## Implementation Workflow

### 1. Analyze & Classify

Analyze the user's intent to determine the required permission tier.

- **Tier 0 (Plan)**: Does the task only involve reading code, analyzing architecture, or gathering information?
- **Tier 1 (Editor)**: Does the task involve modifying files but no autonomous shell command execution?
- **Tier 2 (Autopilot)**: Does the task require running tests, build scripts, or managing dependencies without interruption?

### 2. Approval Protocol

If the task maps to **Tier 1** or **Tier 2**, you **MUST** obtain user approval before executing the `copilot` command.

Use the `AskQuestion` tool to confirm:

> "I've detected that this task requires [Editor/Autopilot] permissions to [modify files/run shell commands]. OK to proceed?"

### 3. Execution

Execute `copilot` using the flags determined by the tier. Use `-p` for non-interactive (programmatic) execution suitable for the calling agent.

```bash
# Tier 0 (Plan — read-only analysis)
copilot -p "<prompt>"

# Tier 1 (Editor — file edits auto-approved, shell still prompts)
copilot -p "<prompt>" --allow-tool='write'

# Tier 2 (Autopilot — all tools auto-approved)
copilot -p "<prompt>" --allow-all-tools
```

**Security Rules:**

- **NEVER** use `--allow-all-tools` without explicit user confirmation of the risks.
- **ALWAYS** use the most restrictive permission level possible (prefer no flags / Tier 0).
- To block a specific dangerous tool, add `--deny-tool='<tool>'` to any command.
- If you are unsure, default to Tier 0 and escalate only if `copilot` reports it cannot complete the task.

### 4. Advanced Tool Control

For fine-grained control, combine `--allow-tool` and `--deny-tool` flags:

```bash
# Allow shell commands but deny network access
copilot -p "<prompt>" --allow-tool='shell' --deny-tool='url'

# Allow a specific MCP server tool only
copilot -p "<prompt>" --allow-tool='mcp-server-name'
```

## Configuration

This skill leverages native `copilot` CLI flags to enforce permission tiers. Global defaults can be set in `~/.copilot/config.json`. Authentication requires running `copilot auth login` or having a valid `GITHUB_TOKEN` in the environment.

## Examples

Refer to [references/usage-examples.md](./references/usage-examples.md) for concrete scenarios.
