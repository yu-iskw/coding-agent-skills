---
name: gemini-cli
description: Executes tasks using the Gemini CLI (`gemini`). Automatically determines the safest approval mode (plan, auto_edit, or yolo) based on the task type.
---

# executing-gemini

## Purpose

Use this skill to perform coding, research, or automation tasks using the `gemini` CLI. It maps requests to Gemini's native approval modes to balance automation with security.

## Permission Tiers

| Tier  | Gemini Mode | Capability                                   | Approval Required   | Typical Tasks                             |
| :---- | :---------- | :------------------------------------------- | :------------------ | :---------------------------------------- |
| **0** | `plan`      | Read-only access, analysis, research. *(experimental)* | **No** | Code review, audits, web research.        |
| **1** | `auto_edit` | Auto-approves file edits; prompts for shell. | **Yes**             | Refactoring, documentation, lint fixes.   |
| **2** | `yolo`      | Auto-approves ALL tools (edits + shell).     | **Yes (High Risk)** | CI/CD, complex builds, automated testing. |

## Implementation Workflow

### 1. Quota Verification (Optional but Recommended)

Before initiating tasks, verify the remaining request quota to avoid session suspension.

- **Tools**: Check Google AI Studio or Google Cloud project dashboard for current usage.
- **Constraints**:
  - Free/Unpaid: 250 requests/day, 10 requests/minute.
  - Paid/Enterprise: 1500-2000 requests/day, 120 requests/minute.

### 2. Analyze & Classify

Analyze the user's intent to determine the required permission tier.

- **Tier 0 (Plan)**: Does the task only involve reading code or searching for information?
- **Tier 1 (Auto-Edit)**: Does the task involve modifying files but no command execution?
- **Tier 2 (YOLO)**: Does the task require running tests, build scripts, or managing dependencies autonomously?

### 2. Approval Protocol

If the task maps to **Tier 1** or **Tier 2**, you **MUST** obtain user approval before executing the `gemini` command.

Use the `AskQuestion` tool to confirm:

> "I've detected that this task requires [Auto-Edit/YOLO] permissions to [modify files/run shell commands]. OK to proceed?"

### 3. Execution

Execute `gemini` using the mode determined by the tier. If resuming a session, you can check `/stats` within the interactive prompt for token usage.

```bash
# Tier 0 (Plan — experimental read-only + sandbox)
gemini -p "<prompt>" --approval-mode plan --sandbox

# Tier 1 (Auto-Edit + sandbox — file edits allowed, shell gated, sandboxed)
gemini -p "<prompt>" --approval-mode auto_edit --sandbox

# Tier 2 (YOLO — sandbox is auto-enabled by --yolo)
gemini -p "<prompt>" --yolo
# equivalent: gemini -p "<prompt>" --approval-mode yolo  (sandbox auto-enabled)
```

**Security Rules:**

- **ALWAYS** pass `--sandbox` for Tier 0 and Tier 1. `--yolo` enables it automatically for Tier 2.
- Default sandbox backend uses Seatbelt (macOS) or bubblewrap (Linux). For stronger isolation, use `GEMINI_SANDBOX=docker` (requires Docker installed).
- **NEVER** use `--yolo` / `--approval-mode yolo` without explicit confirmation of the risks.
- **ALWAYS** use the most restrictive mode possible (prefer `plan`).
- If you are unsure, default to `plan` and escalate only if `gemini` reports it cannot complete the task.
- **`yolo` mode can only be enabled via CLI flag.** It cannot be persisted in `settings.json` to prevent accidental system-wide auto-approval.

## Configuration

This skill leverages native `gemini` CLI flags to enforce the permission tiers.

### Model Selection

The default model is `gemini-2.5-pro`. Switch to `gemini-2.5-flash` for faster, lower-cost responses:

```bash
gemini -m gemini-2.5-flash -p "<prompt>" --approval-mode plan --sandbox
```

Available models: `gemini-2.5-pro` (default, 1M token context), `gemini-2.5-flash` (fast fallback), `gemini-3-flash`.

### Sandbox Backend and Network

For stronger container-level isolation use Docker as the sandbox backend:

```bash
GEMINI_SANDBOX=docker gemini -p "<prompt>" --approval-mode auto_edit --sandbox
```

Disable network access inside the sandbox via `settings.json`:

```json
{
  "tools": {
    "sandboxNetworkAccess": false
  }
}
```

`sandboxNetworkAccess` defaults to `false` when sandbox is enabled — set it explicitly to make the policy auditable.

## Remote Subagents *(experimental — v0.33.0+)*

Gemini CLI can delegate subtasks to remote agents via the **Agent-to-Agent (A2A) protocol** (JSON-RPC 2.0 over HTTPS). Delegation happens automatically when the main agent determines that a specialized subagent is better suited for a portion of the task.

```bash
# Enable experimental A2A features
gemini -p "<prompt>" --experimental-acp

# View active subagents in interactive mode
/subagents
```

> Remote subagents use short-lived scoped tokens (expire in minutes) and communicate over authenticated HTTPS.
> Use `--experimental-acp` only in environments where you trust the remote agent endpoints.

## Examples

Refer to [references/usage-examples.md](./references/usage-examples.md) for concrete scenarios.
