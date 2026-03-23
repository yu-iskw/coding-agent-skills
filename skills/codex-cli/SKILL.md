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

Execute `codex` using the flags corresponding to the tier. Always specify `--sandbox <mode>` explicitly.

```bash
# Tier 0 (Suggest + read-only sandbox — cannot write files or execute commands)
codex --sandbox read-only "<prompt>"

# Tier 0 (non-interactive quiet output)
codex --sandbox read-only -q "<prompt>"

# Tier 1 (Auto-Edit + workspace-write sandbox — writes confined to workspace, network off)
codex --sandbox workspace-write --auto-edit "<prompt>"

# Tier 2 (Full-Auto — workspace-write sandbox + on-request approval)
codex --full-auto "<prompt>"
# Equivalent: codex --sandbox workspace-write --ask-for-approval on-request "<prompt>"
```

**Security Rules:**

- **ALWAYS** specify `--sandbox <mode>` explicitly rather than relying on defaults.
- For Tier 0, `--sandbox read-only` is mandatory: Codex cannot write or execute any commands.
- Network access is disabled by default in `workspace-write` mode; only enable via `config.toml` when explicitly required.
- **NEVER** use `--sandbox danger-full-access` or `--dangerously-bypass-approvals-and-sandbox` without explicit confirmation of the risks.
- **ALWAYS** use the most restrictive mode possible (prefer `suggest` + `read-only`).
- If you are unsure, default to Tier 0 and escalate only if `codex` reports it cannot complete the task.

## Configuration

Codex resolves config in precedence order: CLI flags → profile → project `.codex/config.toml` (trusted only) → user `~/.codex/config.toml` → system → defaults.

For project-level guidance (team standards, style rules), create an `AGENTS.md` file at the repo root. Codex loads it automatically, similar to `CLAUDE.md` in Claude Code.

### Model Selection

The default model is `gpt-5.3-codex`. Override via `config.toml` or the `-m` flag:

```bash
codex -m gpt-5.4 "<prompt>"
```

Available models: `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.3-codex`, `gpt-5.3-codex-spark` (text-only, near-instant iteration).

## Cloud Agent Handoff

Codex can run tasks on OpenAI's cloud infrastructure without tying up your local machine.

```bash
# Launch a task in the cloud
codex cloud "<task>"

# Browse active and completed cloud tasks
codex cloud -l

# Apply resulting diffs to your local workspace
codex cloud -a
```

> Cloud containers are cached for up to **12 hours** after a task completes, making follow-up tasks fast.
> Completed task diffs are staged as a branch; review before merging.

## Examples

Refer to [references/usage-examples.md](./references/usage-examples.md) for concrete scenarios.
