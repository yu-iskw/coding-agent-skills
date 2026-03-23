---
name: codex-cli
description: Executes tasks using the Codex CLI (`codex`). Automatically determines the least privilege required (Suggest, Auto-Edit, or Full-Auto) based on the user's request and handles security approvals.
---

# executing-codex

## Purpose

Use this skill to perform coding tasks, research, or system analysis using the `codex` CLI. This skill follows the Principle of Least Privilege by automatically mapping requests to the safest possible approval mode and gating dangerous operations behind user approval.

> **Note:** The Codex CLI has been rewritten in Rust (v0.106.0+). The TypeScript implementation is now legacy. This skill targets the current Rust-based CLI.

## Permission Tiers

| Tier  | Codex Mode  | Capability                                    | Approval Required | Typical Tasks                          |
| :---- | :---------- | :-------------------------------------------- | :---------------- | :------------------------------------- |
| **0** | `suggest`   | Read files, propose edits (requires approval). | **No**            | Research, code review, explanation.    |
| **1** | `auto-edit` | Apply file edits automatically; prompts before shell commands. | **Yes** | Refactoring, bug fixes, formatting.    |
| **2** | `full-auto` | Edits + sandbox shell commands, no prompts.   | **Yes**           | Testing, building, dependency updates. |

## Implementation Workflow

### 1. Quota Verification (Optional but Recommended)

Before initiating tasks, verify the remaining message quota to avoid session suspension.

- **Tools**: Check `codex cloud status` (if applicable) or refer to the ChatGPT plan limits.
- **Constraints**:
  - Rolling 5-hour window: ~30–150 messages (Plus) or ~300–1500 messages (Pro).
  - Heavy local usage reduces available cloud task quota.

### 2. Analyze & Classify

Analyze the user's intent to determine the required permission tier.

- **Tier 0 (Suggest)**: Does the task only involve reading code or searching for information?
- **Tier 1 (Auto-Edit)**: Does the task involve modifying files but no command execution?
- **Tier 2 (Full-Auto)**: Does the task require running tests, build scripts, or managing dependencies?

### 3. Approval Protocol

If the task maps to **Tier 1** or **Tier 2**, you **MUST** obtain user approval before executing the `codex` command.

Use the `AskQuestion` tool to confirm:

> "I've detected that this task requires [Auto-Edit/Full-Auto] permissions to [modify files/run commands]. OK to proceed?"

### 4. Execution

Execute `codex` using the flags corresponding to the tier. Use `-q` for non-interactive quiet output.

```bash
# Tier 0 (Suggest — default mode, proposes all changes before applying)
codex "<prompt>"

# Tier 0 (non-interactive quiet output)
codex -q "<prompt>"

# Tier 1 (Auto-Edit — applies file edits automatically, prompts for shell)
codex --auto-edit "<prompt>"

# Tier 2 (Full-Auto — edits + shell in sandbox, no prompts)
codex --full-auto "<prompt>"
```

**Security Rules:**

- **NEVER** use `--dangerously-bypass-approvals-and-sandbox` without explicit confirmation of the risks.
- **ALWAYS** use the most restrictive mode possible (prefer `suggest`).
- If you are unsure, default to Tier 0 and escalate only if `codex` reports it cannot complete the task.

## Configuration

Codex resolves config in precedence order: CLI flags → profile → project `.codex/config.toml` (trusted only) → user `~/.codex/config.toml` → system → defaults.

For project-level guidance (team standards, style rules), create an `AGENTS.md` file at the repo root. Codex loads it automatically, similar to `CLAUDE.md` in Claude Code.

## Examples

Refer to [references/usage-examples.md](./references/usage-examples.md) for concrete scenarios.
