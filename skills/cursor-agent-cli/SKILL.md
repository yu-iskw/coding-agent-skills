---
name: cursor-agent-cli
description: Executes tasks using the Cursor Agent CLI (`cursor-agent`). Provides structured modes for planning, Q&A, and full automation with safety guardrails.
---

# executing-cursor-agent

## Purpose

Use this skill to perform coding, research, or automation tasks using the `cursor-agent` CLI. It leverages Cursor's native execution modes to balance autonomy with safety.

## Execution Modes

| Mode        | Flag          | Capability                                  | Approval Required | Typical Tasks                             |
| :---------- | :------------ | :------------------------------------------ | :---------------- | :---------------------------------------- |
| **Plan**    | `--mode plan` | Read-only analysis, research, and planning. | **No**            | Code audits, architectural planning.      |
| **Ask**     | `--mode ask`  | Q&A style for explanations and questions.   | **No**            | Explaining code, searching documentation. |
| **Default** | (none)        | Full access (edits + shell execution).      | **Yes**           | Feature implementation, bug fixes.        |

## Implementation Workflow

### 1. Analyze & Classify

Analyze the user's intent to determine the appropriate mode.

- **Plan Mode**: Does the task only involve analyzing the codebase or proposing a plan without making changes?
- **Ask Mode**: Is the user asking a specific question or seeking an explanation?
- **Default Mode**: Does the task require modifying files or running shell commands?

### 2. Security Protocol

If the task requires **Default Mode**, you **MUST** obtain user approval before execution, as `cursor-agent` has full access to tools like `bash` and `write`.

Use the `AskQuestion` tool to confirm:

> "I've detected that this task requires full agent permissions to modify files and execute commands. OK to proceed with `cursor-agent`?"

### 3. Execution

Execute `cursor-agent` using the determined mode. Use `--print` for non-interactive output suitable for the calling agent.

```bash
# Plan Mode
cursor-agent --print --mode plan "<prompt>"

# Ask Mode
cursor-agent --print --mode ask "<prompt>"

# Default Mode (requires approval)
cursor-agent --print "<prompt>"
```

### 4. Advanced Commands

#### MCP Management

- `cursor-agent mcp list`: View configured MCP servers.
- `cursor-agent mcp list-tools <id>`: Inspect tools available in a specific MCP.

#### Rule Generation

- `cursor-agent generate-rule`: Create new `.cursorrules` or project-specific rules.

## Configuration

This skill uses native `cursor-agent` flags. Ensure `CURSOR_API_KEY` is set in the environment if required, or run `cursor-agent login` first.

## Examples

Refer to [references/usage-examples.md](./references/usage-examples.md) for concrete scenarios.
