---
name: claude-code-cli
description: Executes tasks using the Claude Code CLI (`claude`). Automatically determines the safest permission mode (plan, acceptEdits, or bypassPermissions) based on the task type.
---

# executing-claude

## Purpose

Use this skill to perform coding, research, or automation tasks using the `claude` CLI. It maps requests to Claude's native permission modes to balance automation with security.

## Permission Tiers

| Tier  | Claude Mode         | Capability                                   | Approval Required   | Typical Tasks                             |
| :---- | :------------------ | :------------------------------------------- | :------------------ | :---------------------------------------- |
| **0** | `plan`              | Read-only access, analysis, research.        | **No**              | Code review, audits, web research.        |
| **1** | `acceptEdits`       | Auto-approves file edits; prompts for shell. | **Yes**             | Refactoring, documentation, lint fixes.   |
| **2** | `bypassPermissions` | Auto-approves ALL tools (edits + shell); respects deny list. | **Yes (High Risk)** | CI/CD, complex builds, automated testing. |
| **–** | `delegate`          | Subagents inherit parent's permission level. | **Varies**          | Multi-agent / parallel task workflows.    |

## Implementation Workflow

### 1. Budget Verification (Optional but Recommended)

Before initiating complex or long-running tasks, verify the remaining token/cost budget to avoid suspension.

- **Tools**: Use `ccusage daily --json` to check current consumption.
- **Constraints**: If the daily cost is approaching the limit, alert the user or use the `--max-budget-usd` flag for the session.

### 2. Analyze & Classify

Analyze the user's intent to determine the required permission tier.

- **Tier 0 (Plan)**: Does the task only involve reading code or searching for information?
- **Tier 1 (Accept Edits)**: Does the task involve modifying files but no command execution?
- **Tier 2 (Bypass Permissions)**: Does the task require running tests, build scripts, or managing dependencies autonomously?

### 2. Approval Protocol

If the task maps to **Tier 1** or **Tier 2**, you **MUST** obtain user approval before executing the `claude` command.

Use the `AskQuestion` tool to confirm:

> "I've detected that this task requires [Accept Edits/Bypass Permissions] permissions to [modify files/run shell commands]. OK to proceed?"

### 3. Execution

Execute `claude` using the mode determined by the tier. Use `--max-budget-usd` for non-interactive tasks where cost control is critical.

```bash
# Tier 0 (Plan + sandbox — read-only, OS-level isolation, shell blocked)
claude -p "<prompt>" --permission-mode plan --sandbox \
  --disallowedTools Bash --max-budget-usd 1.0

# Tier 1 (Accept Edits + sandbox — file writes allowed, shell gated, OS-level isolation)
claude -p "<prompt>" --permission-mode acceptEdits --sandbox

# Tier 2 (Bypass Permissions — sandbox omitted; must run shell commands freely)
claude -p "<prompt>" --permission-mode bypassPermissions
```

**Security Rules:**

- **ALWAYS** pass `--sandbox` for Tier 0 and Tier 1. Skip only when OS prerequisites are unavailable (Linux requires `bubblewrap` + `socat`: `sudo apt-get install bubblewrap socat`; macOS uses built-in Seatbelt).
- For Tier 0, also pass `--disallowedTools Bash` to block shell execution at the tool layer.
- **NEVER** use `--permission-mode bypassPermissions` without explicit confirmation of the risks.
- **ALWAYS** use the most restrictive mode possible (prefer `plan`).
- If you are unsure, default to `plan` and escalate only if `claude` reports it cannot complete the task.
- **`--permission-mode bypassPermissions` vs `--dangerously-skip-permissions`**: `bypassPermissions` still respects explicit deny rules in `settings.json`. The `--dangerously-skip-permissions` flag bypasses ALL checks including the deny list — never use it outside a fully isolated container.

## Configuration

This skill leverages native `claude` CLI flags to enforce the permission tiers.

### Model Selection

The default model depends on your Claude plan:

| Plan | Default Model | Shorthand |
| :--- | :------------ | :-------- |
| Max / Team / Enterprise | `claude-opus-4-6` | `opus` |
| Pro | `claude-sonnet-4-6` | `sonnet` |

Override at invocation time with `--model <shorthand-or-id>`, or change mid-session with `/model <shorthand>`:

```bash
claude --model sonnet -p "<prompt>" --permission-mode plan
claude --model opus   -p "<prompt>" --permission-mode acceptEdits
```

Available model IDs: `claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5`.

## Cloud Agent Handoff

Claude Code offers two remote execution modes beyond local CLI.

### Cloud Execution *(research preview — Pro / Max / Team / Enterprise)*

Tasks run on Anthropic-managed VMs with pre-installed runtimes. Code is cloned to an isolated container; no local machine required.

```bash
# Kick off a cloud task
claude --remote "<task>"

# Monitor all running cloud tasks (in any interactive session)
/tasks
```

> **Security note:** Cloud tasks run with `--dangerously-skip-permissions` by default.
> Only committed repo hooks and a `setup.sh` script apply; user-level `settings.json` is ignored.
> Use for well-defined, async tasks where local oversight is not required.

### Remote Control *(GA — Feb 2026)*

Code stays on your local machine. Remote Control synchronizes access so you can monitor and steer the same agent session from another device (phone, tablet, web at `claude.ai/code`).

```bash
# Pull a web or mobile session back to your terminal
claude --teleport
claude --teleport <session-id>
```

| | Cloud Execution | Remote Control |
| :--- | :--- | :--- |
| **Where code runs** | Anthropic VM | Your local machine |
| **Parallelism** | Multiple tasks | Single session |
| **Offline continuation** | Yes | No (requires local machine) |
| **Permissions** | `dangerously-skip-permissions` | Respects local settings |

## Examples

Refer to [references/usage-examples.md](./references/usage-examples.md) for concrete scenarios.
